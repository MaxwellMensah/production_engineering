import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()  # Load environment variables from .env file


class ScoreBreakdownItem(BaseModel):
    raw_value: float
    weight: float
    weighted_contribution: float


class ScoringResult(BaseModel):
    composite_score: float
    normalized_score_100: float
    breakdown: dict[str, ScoreBreakdownItem]


class ScoringEngine:
    def __init__(self, config: dict[str, float]):
        """
        Initialize the engine with a config mapping fields to weights.
        Weights are automatically normalized to sum to 1.0.
        """
        if not config:
            raise ValueError("Scoring configuration cannot be empty.")

        total_weight = sum(config.values())
        if total_weight <= 0:
            raise ValueError("Sum of weights must be greater than zero.")

        # Normalize weights
        self.config: dict[str, float] = {
            field: weight / total_weight for field, weight in config.items()
        }

    def evaluate(self, metrics: dict[str, float]) -> ScoringResult:
        """
        Calculates composite weighted score (0.0 - 1.0 and 0 - 100) along with field breakdowns.
        Missing fields default to 0.0.
        """
        breakdown: dict[str, ScoreBreakdownItem] = {}
        composite_score = 0.0

        for field, weight in self.config.items():
            raw_value = float(metrics.get(field, 0.0))
            # Clamp raw value between 0.0 and 1.0
            clamped_value = max(0.0, min(1.0, raw_value))
            contribution = clamped_value * weight
            composite_score += contribution

            breakdown[field] = ScoreBreakdownItem(
                raw_value=raw_value,
                weight=round(weight, 4),
                weighted_contribution=round(contribution, 4),
            )

        return ScoringResult(
            composite_score=round(composite_score, 4),
            normalized_score_100=round(composite_score * 100, 2),
            breakdown=breakdown,
        )

    @classmethod
    def suggest_config_from_llm(
        cls, domain_description: str, fields: list[str], api_key: str | None = None
    ) -> dict[str, float]:
        """
        Sends domain context to Claude and generates a suggested weighting configuration in JSON.
        """
        client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

        prompt = f"""
                    You are an expert scoring system architect.
                    Given the following domain description and list of metric fields, assign relative weights (floats between 0.0 and 1.0) to each field reflecting its importance in overall evaluation. The weights must sum to 1.0.

                    Domain Description:
                    "{domain_description}"

                    Fields to weight:
                    {json.dumps(fields, indent=2)}

                    Return ONLY a raw JSON object mapping each field name to its float weight. Do not include markdown formatting or extra text.
                    Example format:
                    {{"field_a": 0.6, "field_b": 0.4}}
                """

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_content = response.content[0].text.strip()
        # Clean potential markdown wrapping
        if raw_content.startswith("```"):
            raw_content = raw_content.split("```")[1]
            raw_content = raw_content.removeprefix("json")

        weights: dict[str, float] = json.loads(raw_content.strip())
        return weights


# Execution Demonstration
if __name__ == "__main__":
    print("=== Domain 1: Fraud Document Quality ===")
    with open("config_fraud_doc.json") as f:
        fraud_config = json.load(f)

    fraud_engine = ScoringEngine(fraud_config)
    sample_doc_metrics = {
        "ocr_confidence": 0.92,
        "image_resolution_dpi": 0.85,
        "tampering_risk_score": 0.10,  # low tampering risk = high quality component
        "metadata_consistency": 0.98,
        "font_anomaly_score": 0.95,
    }
    fraud_result = fraud_engine.evaluate(sample_doc_metrics)
    print(f"Composite Score: {fraud_result.normalized_score_100}/100")
    print(
        "Breakdown:",
        json.dumps(fraud_result.breakdown, indent=2, default=lambda o: o.__dict__),
    )

    print("\n=== Domain 2: RAG Response Quality ===")
    with open("config_rag_eval.json") as f:
        rag_config = json.load(f)

    rag_engine = ScoringEngine(rag_config)
    sample_rag_metrics = {
        "faithfulness_score": 0.95,
        "answer_relevance": 0.88,
        "context_recall": 0.75,
        "latency_score": 0.60,
        "conciseness": 0.90,
    }
    rag_result = rag_engine.evaluate(sample_rag_metrics)
    print(f"Composite Score: {rag_result.normalized_score_100}/100")
    print(
        "Breakdown:",
        json.dumps(rag_result.breakdown, indent=2, default=lambda o: o.__dict__),
    )

    # LLM-assisted rule suggestion test (Requires ANTHROPIC_API_KEY in environment)
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\n=== LLM-Assisted Rule Suggestion ===")
        domain_desc = (
            "Candidate resume evaluation for a Senior Backend Cloud Engineer position."
        )
        candidate_fields = [
            "python_experience",
            "system_design_score",
            "culture_fit",
            "salary_expectation_alignment",
        ]

        suggested_config = ScoringEngine.suggest_config_from_llm(
            domain_desc, candidate_fields
        )
        print("Suggested Config from Claude:", json.dumps(suggested_config, indent=2))
