```markdown
# Configurable Grading & Scoring Engine

A domain-agnostic evaluation micro-module that calculates normalized composite quality scores and per-metric breakdowns for AI system outputs. Features an LLM-assisted bootstrap utility to generate field weighting configurations automatically via Claude Haiku.
```
---

## Repository Structure

```text
.
├── config_fraud_doc.json   # Weighting configuration for document fraud evaluation
├── config_rag_eval.json    # Weighting configuration for RAG response evaluation
└── scoring_engine.py       # Core ScoringEngine class & LLM configuration helper

```

---

## Key Features

* **Normalized Composite Scoring:** Scales arbitrary weights to sum to 1.0 and outputs both decimal (0.0–1.0) and percentage (0–100) scores.
* **Granular Field Breakdowns:** Provides raw values, normalized weights, and exact mathematical contributions per field for failure analysis.
* **Domain Agnostic:** Decouples domain rules from application logic via standard JSON configs.
* **LLM Rule Suggestion:** Generates domain-tailored metric weighting configs from plain-text requirements using `claude-3-haiku-20240307`.

---

## LLM-Assisted Config Generation

### What It Means

Instead of manually guessing and hardcoding numeric weights (`{field: weight}`) for a new evaluation domain, you can pass a plain-text domain description and a list of metrics to Claude Haiku. The model analyzes the domain context and automatically computes appropriate, normalized weights.

### How It Works

1. **Inputs:** Provide a plain-text domain context (e.g., *"Automated code review assistant evaluation"*) and a target metric list (e.g., `["syntax_correctness", "security_risk", "performance_impact", "readability"]`).
2. **Analysis:** Claude evaluates the relative importance of each field within that specific domain (e.g., prioritizing `security_risk` over `readability`).
3. **JSON Output:** It outputs a clean, normalized JSON object mapping each field to a float weight, strictly guaranteed to sum to `1.0`.

### Why We Use It

* **Solves the Cold-Start Problem:** Setting up evaluation harnesses for brand-new domains usually requires guesswork. This utility creates an immediate, sensible baseline config in seconds.
* **Reduces Manual Friction:** Team members can bootstrap domain configs simply by describing what they want to evaluate in plain English rather than tweaking raw numbers manually.
* **Domain Adaptation:** Easily generate custom scoring profiles for drastically different roles or tasks without writing custom configuration code.

---

## Quick Start

### Run Evaluation Demo

```bash
python scoring_engine.py

```

### Basic Engine Usage

```python
import json
from scoring_engine import ScoringEngine

# Load domain configuration
with open("config_rag_eval.json") as f:
    config = json.load(f)

engine = ScoringEngine(config)

# Evaluate metric dict (values normalized 0.0 - 1.0)
metrics = {
    "faithfulness_score": 0.95,
    "answer_relevance": 0.88,
    "context_recall": 0.75,
    "latency_score": 0.60,
    "conciseness": 0.90
}

result = engine.evaluate(metrics)
print(f"Composite Score: {result.normalized_score_100}/100")

```

### Auto-Generate Config with Claude Haiku

```python
from scoring_engine import ScoringEngine

domain_desc = "Automated code review assistant evaluation"
fields = ["syntax_correctness", "security_risk", "performance_impact", "readability"]

suggested_config = ScoringEngine.suggest_config_from_llm(domain_desc, fields)
print(suggested_config)
```

