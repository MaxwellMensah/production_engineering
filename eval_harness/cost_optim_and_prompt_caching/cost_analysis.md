# Cost Analysis & Prompt Caching Optimization

## Workload Baseline (1,000 Requests/Day = 30,000 Requests/Month)
* **Static Input Prefix (System/Tools):** 1,222 tokens
* **Dynamic Input (User Query):** 14 tokens
* **Output Tokens:** 80 tokens
* **Cache Strategy:** 5-minute ephemeral TTL (1 cache write per active hour = 720 writes/month, 29,280 cache hits/month)

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
  $$\text{Input: } 30,000 \times 1,236 \text{ tokens} \times \frac{\$1.00}{1\text{M}} = \$37.08$$
  $$\text{Output: } 30,000 \times 80 \text{ tokens} \times \frac{\$5.00}{1\text{M}} = \$12.00$$
  $$\mathbf{\text{Total Standard Cost: } \$49.08/\text{month}}$$

* **Prompt Caching Cost:**
  $$\text{Cache Writes (720): } 720 \times 1,222 \times \frac{\$1.25}{1\text{M}} = \$1.10$$
  $$\text{Cache Reads (29,280): } 29,280 \times 1,222 \times \frac{\$0.10}{1\text{M}} = \$3.58$$
  $$\text{Uncached Input: } 30,000 \times 14 \times \frac{\$1.00}{1\text{M}} = \$0.42$$
  $$\text{Output: } 30,000 \times 80 \times \frac{\$5.00}{1\text{M}} = \$12.00$$
  $$\mathbf{\text{Total Cached Cost: } \$17.10/\text{month} \quad (\text{Savings: } 65.2\%)}$$

---

### 2. Claude Sonnet 3.5 / 3.7
* **Standard API Cost:**
  $$\text{Input: } 30,000 \times 1,236 \text{ tokens} \times \frac{\$3.00}{1\text{M}} = \$111.24$$
  $$\text{Output: } 30,000 \times 80 \text{ tokens} \times \frac{\$15.00}{1\text{M}} = \$36.00$$
  $$\mathbf{\text{Total Standard Cost: } \$147.24/\text{month}}$$

* **Prompt Caching Cost:**
  $$\text{Cache Writes (720): } 720 \times 1,222 \times \frac{\$3.75}{1\text{M}} = \$3.30$$
  $$\text{Cache Reads (29,280): } 29,280 \times 1,222 \times \frac{\$0.30}{1\text{M}} = \$10.73$$
  $$\text{Uncached Input: } 30,000 \times 14 \times \frac{\$3.00}{1\text{M}} = \$1.26$$
  $$\text{Output: } 30,000 \times 80 \times \frac{\$15.00}{1\text{M}} = \$36.00$$
  $$\mathbf{\text{Total Cached Cost: } \$51.29/\text{month} \quad (\text{Savings: } 65.2\%)}$$

---

### 3. Claude Opus
* **Standard API Cost:**
  $$\text{Input: } 30,000 \times 1,236 \text{ tokens} \times \frac{\$5.00}{1\text{M}} = \$185.40$$
  $$\text{Output: } 30,000 \times 80 \text{ tokens} \times \frac{\$25.00}{1\text{M}} = \$60.00$$
  $$\mathbf{\text{Total Standard Cost: } \$245.40/\text{month}}$$

* **Prompt Caching Cost:**
  $$\text{Cache Writes (720): } 720 \times 1,222 \times \frac{\$6.25}{1\text{M}} = \$5.50$$
  $$\text{Cache Reads (29,280): } 29,280 \times 1,222 \times \frac{\$0.50}{1\text{M}} = \$17.89$$
  $$\text{Uncached Input: } 30,000 \times 14 \times \frac{\$5.00}{1\text{M}} = \$2.10$$
  $$\text{Output: } 30,000 \times 80 \times \frac{\$25.00}{1\text{M}} = \$60.00$$
  $$\mathbf{\text{Total Cached Cost: } \$85.49/\text{month} \quad (\text{Savings: } 65.2\%)}$$

---

## Break-Even Analysis

Let $N$ be the number of requests inside the 5-minute TTL window, $W = 1.25$ (write rate), and $R = 0.10$ (read rate):

$$\text{Cost}_{\text{cached}} \le \text{Cost}_{\text{standard}} \implies W + R(N - 1) \le N$$

$$1.25 + 0.10(N - 1) \le N \implies 1.15 \le 0.90N \implies N \ge 1.28$$

$$\mathbf{N_{\text{break-even}} = 2 \text{ requests per 5-minute TTL window}}$$

*Any system prompt reused more than once every 5 minutes produces net cost savings.*