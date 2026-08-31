# Cost Analysis & Prompt Caching Optimization

## Workload Baseline (1,000 Requests/Day = 30,000 Requests/Month)
* **Static Input Prefix (System/Tools):** 1,222 tokens
* **Dynamic Input (User Query):** 14 tokens
* **Output Tokens:** 80 tokens
* **Cache Strategy:** 5-minute ephemeral TTL (720 writes/month, 29,280 cache hits/month)

---

## Token Pricing Matrix (Per Million Tokens)

| Model Tier | Base Input | Output | 5-min Cache Write | Cache Hit (Read) |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Haiku 4.5** | $1.00 | $5.00 | $1.25 | $0.10 |
| **Claude Sonnet 3.5 / 3.7** | $3.00 | $15.00 | $3.75 | $0.30 |
| **Claude Opus** | $5.00 | $25.00 | $6.25 | $0.50 |

---

## Monthly Cost Breakdown (30,000 Total Requests)

### 1. Claude Haiku 4.5
* **Standard API Cost:**
  * Input: 30,000 × 1,236 tokens × ($1.00 / 1M) = **$37.08**
  * Output: 30,000 × 80 tokens × ($5.00 / 1M) = **$12.00**
  * **Total Standard Cost:** **$49.08 / month**

* **Prompt Caching Cost:**
  * Cache Writes (720): 720 × 1,222 tokens × ($1.25 / 1M) = **$1.10**
  * Cache Reads (29,280): 29,280 × 1,222 tokens × ($0.10 / 1M) = **$3.58**
  * Uncached Input: 30,000 × 14 tokens × ($1.00 / 1M) = **$0.42**
  * Output: 30,000 × 80 tokens × ($5.00 / 1M) = **$12.00**
  * **Total Cached Cost:** **$17.10 / month** *(Savings: 65.2%)*

---

### 2. Claude Sonnet 3.5 / 3.7
* **Standard API Cost:**
  * Input: 30,000 × 1,236 tokens × ($3.00 / 1M) = **$111.24**
  * Output: 30,000 × 80 tokens × ($15.00 / 1M) = **$36.00**
  * **Total Standard Cost:** **$147.24 / month**

* **Prompt Caching Cost:**
  * Cache Writes (720): 720 × 1,222 tokens × ($3.75 / 1M) = **$3.30**
  * Cache Reads (29,280): 29,280 × 1,222 tokens × ($0.30 / 1M) = **$10.73**
  * Uncached Input: 30,000 × 14 tokens × ($3.00 / 1M) = **$1.26**
  * Output: 30,000 × 80 tokens × ($15.00 / 1M) = **$36.00**
  * **Total Cached Cost:** **$51.29 / month** *(Savings: 65.2%)*

---

### 3. Claude Opus
* **Standard API Cost:**
  * Input: 30,000 × 1,236 tokens × ($5.00 / 1M) = **$185.40**
  * Output: 30,000 × 80 tokens × ($25.00 / 1M) = **$60.00**
  * **Total Standard Cost:** **$245.40 / month**

* **Prompt Caching Cost:**
  * Cache Writes (720): 720 × 1,222 tokens × ($6.25 / 1M) = **$5.50**
  * Cache Reads (29,280): 29,280 × 1,222 tokens × ($0.50 / 1M) = **$17.89**
  * Uncached Input: 30,000 × 14 tokens × ($5.00 / 1M) = **$2.10**
  * Output: 30,000 × 80 tokens × ($25.00 / 1M) = **$60.00**
  * **Total Cached Cost:** **$85.49 / month** *(Savings: 65.2%)*

---

## Break-Even Analysis

Let $N$ be the number of requests inside the 5-minute TTL window, $W$ be write cost, and $R$ be read cost:

$$\text{Cost}_{\text{cached}} \le \text{Cost}_{\text{standard}} \implies W + R(N - 1) \le N$$

**Break-even Threshold:** **2 requests per 5-minute TTL window**

*Any system prompt reused more than once every 5 minutes produces net cost savings.*