Using `--env-vars-file env.yaml` is cleaner, more readable, and avoids potential shell expansion bugs if an API key contains special characters like `$` or `!`.

Here is the updated `README.md` reflecting the `env.yaml` workflow:

```markdown
# Cost Optimization & Prompt Caching Service

A production-ready FastAPI microservice demonstrating Anthropic Claude prompt caching and cost optimization. This service optimizes input token overhead by caching static system prompts and tool definitions in memory, reducing API input costs by ~65% in high-frequency workloads.

---

## Repository Structure

```text
eval_harness/cost_optim_and_prompt_caching/
├── Dockerfile          # Container configuration for Cloud Run
├── README.md           # Module overview and setup guide
├── cost_analysis.md    # Detailed cost breakdown & break-even math
├── requirements.txt    # Python dependencies
└── test_caching.py     # FastAPI application with prompt caching

```

---

## Key Features

* **Prompt Caching Integration:** Utilizes Anthropic's `ephemeral` cache control header to store static system instructions.
* **Cost Efficiency:** Reduces input token charges from standard rates down to cache read rates on warm cache hits.
* **Serverless Ready:** Containerized with Uvicorn and configured to bind dynamically to Cloud Run execution environments.

---

## Local Development

### 1. Environment Setup

Create a `.env` file in this directory:

```bash
ANTHROPIC_API_KEY="your-anthropic-api-key"

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Run Application

```bash
uvicorn test_caching:app --host 0.0.0.0 --port 8000 --reload

```

### 4. Test Caching Behavior

**Write to Cache (Call 1):**

```bash
curl -X POST "[http://127.0.0.1:8000/v1/chat](http://127.0.0.1:8000/v1/chat)" \
     -H "Content-Type: application/json" \
     -d '{"user_query": "What are your core rules?"}'

```

**Read from Cache (Call 2):**

```bash
curl -X POST "[http://127.0.0.1:8000/v1/chat](http://127.0.0.1:8000/v1/chat)" \
     -H "Content-Type: application/json" \
     -d '{"user_query": "Summarize rule number 1."}'

```

---

## Production Deployment (Google Cloud Run)

1. Create a local `env.yaml` file (ignored by Git):

```yaml
ANTHROPIC_API_KEY: "your-actual-api-key-here"

```

2. Deploy to Cloud Run using the environment file:

```bash
gcloud run deploy prompt-caching-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --env-vars-file env.yaml

```

---

## Cost Optimization Summary

Detailed calculations and token unit economics can be found in [`cost_analysis.md`](https://www.google.com/search?q=./cost_analysis.md).

* **Standard API Cost (Sonnet 3.5/3.7):** ~$147.24 / 30k requests
* **Prompt Caching Cost (Sonnet 3.5/3.7):** ~$51.29 / 30k requests
* **Break-Even Threshold:** 2 requests within any 5-minute cache TTL window.

```

**Update and Push to Repository**

Run these commands from `/home/maxie/Documents/production_engineering/eval_harness/cost_optim_and_prompt_caching`:

```bash
cat << 'EOF' > README.md
# Cost Optimization & Prompt Caching Service

A production-ready FastAPI microservice demonstrating Anthropic Claude prompt caching and cost optimization. This service optimizes input token overhead by caching static system prompts and tool definitions in memory, reducing API input costs by ~65% in high-frequency workloads.

---

## Repository Structure

```text
eval_harness/cost_optim_and_prompt_caching/
├── Dockerfile          # Container configuration for Cloud Run
├── README.md           # Module overview and setup guide
├── cost_analysis.md    # Detailed cost breakdown & break-even math
├── requirements.txt    # Python dependencies
└── test_caching.py     # FastAPI application with prompt caching

```

---

## Key Features

* **Prompt Caching Integration:** Utilizes Anthropic's `ephemeral` cache control header to store static system instructions.
* **Cost Efficiency:** Reduces input token charges from standard rates down to cache read rates on warm cache hits.
* **Serverless Ready:** Containerized with Uvicorn and configured to bind dynamically to Cloud Run execution environments.

---

## Local Development

### 1. Environment Setup

Create a `.env` file in this directory:

```bash
ANTHROPIC_API_KEY="your-anthropic-api-key"

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Run Application

```bash
uvicorn test_caching:app --host 0.0.0.0 --port 8000 --reload

```

### 4. Test Caching Behavior

**Write to Cache (Call 1):**

```bash
curl -X POST "[http://127.0.0.1:8000/v1/chat](http://127.0.0.1:8000/v1/chat)" \
     -H "Content-Type: application/json" \
     -d '{"user_query": "What are your core rules?"}'

```

**Read from Cache (Call 2):**

```bash
curl -X POST "[http://127.0.0.1:8000/v1/chat](http://127.0.0.1:8000/v1/chat)" \
     -H "Content-Type: application/json" \
     -d '{"user_query": "Summarize rule number 1."}'

```

---

## Production Deployment (Google Cloud Run)

1. Create a local `env.yaml` file (ignored by Git):

```yaml
ANTHROPIC_API_KEY: "your-actual-api-key-here"

```

2. Deploy to Cloud Run using the environment file:

```bash
gcloud run deploy prompt-caching-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --env-vars-file env.yaml

```

---

## Cost Optimization Summary

Detailed calculations and token unit economics can be found in [`cost_analysis.md`](https://www.google.com/search?q=./cost_analysis.md).

* **Standard API Cost (Sonnet 3.5/3.7):** ~$147.24 / 30k requests
* **Prompt Caching Cost (Sonnet 3.5/3.7):** ~$51.29 / 30k requests
* **Break-Even Threshold:** 2 requests within any 5-minute cache TTL window.