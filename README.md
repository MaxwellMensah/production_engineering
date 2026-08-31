```markdown
# Production AI Engineering & Evaluation Suite

A modular repository housing production-ready LLM infrastructure, cost optimization patterns, and automated evaluation harnesses. Designed to bridge the gap between raw model outputs and deterministic enterprise business logic.

> **Status:** Active Development (Modular Expansion in Progress)

---

## Architecture & Module Overview

| Module | Location | Description | Status |
| :--- | :--- | :--- | :--- |
| **Cost Optim & Caching** | [`eval_harness/cost_optim_and_prompt_caching/`](./eval_harness/cost_optim_and_prompt_caching/) | FastAPI microservice utilizing Anthropic prompt caching to cut input token overhead by ~65–90%. | Production Ready |
| **Scoring Engine** | [`eval_harness/config_grading_and_scoring_engine/`](./eval_harness/config_grading_and_scoring_engine/) | Domain-agnostic weighted evaluation engine with automated config bootstrapping via Claude Haiku. | Production Ready |
| **Pipeline Extensions** | `eval_harness/...` | CI/CD quality gates, hallucination checks, and LLM-as-a-judge pipelines. | In Development |

---

## Key Capabilities

* **Prompt Caching Microservices:** Optimized endpoints designed for high-frequency workloads using ephemeral cache control headers.
* **Deterministic Quality Scoring:** Multi-field weighted scoring models that break composite quality metrics down into field-level failure analyses.
* **LLM-Assisted Bootstrapping:** Natural language to JSON config translation for cold-starting evaluation suites without manual weight guessing.
* **Cloud-Native Deployment:** Containerized modules configured out-of-the-box for Google Cloud Run and serverless environments.

---

## Tech Stack

* **Language:** Python 3.11+
* **Frameworks:** FastAPI, Pydantic v2, Uvicorn
* **LLM Providers:** Anthropic Claude SDK (`claude-4-6-sonnet`, `claude-haiku-4-5-20251001`)
* **Environment Management:** Pixi / virtualenv
* **Cloud & Containerization:** Docker, Google Cloud Run

---

## Quick Start

### 1. Repository Setup

Clone the repository and set up your local environment:

```bash
git clone [https://github.com/your-username/production_engineering.git](https://github.com/your-username/production_engineering.git)
cd production_engineering

```

### 2. Configure Environment Variables

Create a root `.env` file (ensure this remains git-ignored):

```bash
ANTHROPIC_API_KEY="your-anthropic-api-key-here"

```

### 3. Running Module Demos

**Run the Scoring Engine & LLM Bootstrapper:**

```bash
python eval_harness/config_grading_and_scoring_engine/scoring_engine.py

```

**Run the Prompt Caching API Service:**

```bash
cd eval_harness/cost_optim_and_prompt_caching
uvicorn test_caching:app --host 0.0.0.0 --port 8000 --reload

```

---

## Development Roadmap

* [x] Prompt Caching, Token Cost Analysis & Cloud Run Integration
* [x] Configurable Grading & Scoring Engine + Haiku Rule Generation
* [ ] Automated CI/CD Quality Gates & LLM-as-a-Judge Evaluation Suites
* [ ] Latency Benchmarking & Vector Retrieval Optimizations

---

## License

Internal Production Engineering Repository - All rights reserved.