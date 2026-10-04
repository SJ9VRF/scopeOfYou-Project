# Real Evaluation Tables

Executed controlled evidence only. Frontier 7–8B and human-study results remain pending.

## Independent ContractBench-Implicit

| Variant | Contract score | PersonalBench | N / seeds | Notes |
|---|---:|---:|---|---|
| SFT | 0.7135 | 0.9905 | 1,460 cases / 20 users | utility anchor |
| Raw | 0.4817 | 0.8399 | 1,460 cases / 20 users | controlled baseline |
| Constrained | 0.6615 | 0.9481 | 1,460 cases / 20 users | controlled baseline |
| BATPO | 0.6866 | 0.9614 | 1,460 cases / 20 users | strongest non-PCO baseline |
| PCO-Robust | 0.7912 | 0.9448 | 1,460 cases / 20 users | headline method |

**PCO-Robust, 5 seeds:** CBI 0.7910 ± 0.0008; PersonalBench 0.9449 ± 0.0005.
**vs BATPO:** +10.46 pp; 95% CI [8.65, 12.24]; wins 20/20 users.

## Agentic evaluator stress test — not an LLM capability result

| Policy | Trial success | Recovery | Hard-safe | pass@5 | all-success@5 |
|---|---:|---:|---:|---:|---:|
| naive_personalize | 0.271 | 0.000 | 0.417 | 0.271 | 0.271 |
| risk_aware | 0.812 | 0.375 | 1.000 | 0.812 | 0.812 |
| noisy_risk_aware | 0.765 | 0.324 | 0.983 | 0.840 | 0.566 |
| contract_oracle | 1.000 | 0.188 | 1.000 | 1.000 | 1.000 |

N = 288 scenarios × 5 trials/policy.

## Runtime

| Backend | N | Median | p95 | Cloud cost |
|---|---:|---:|---:|---|
| CPU behavioral checkpoint | 1000 | 0.134 ms | 0.273 ms | not measured / local execution |