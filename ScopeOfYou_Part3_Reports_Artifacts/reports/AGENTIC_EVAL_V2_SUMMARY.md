# Agentic Contract Suite v2 — Sanity-Check Summary

This is an evaluator validation artifact, **not an LLM capability result**.

## Scale
- 288 stateful scenarios
- 6 domains: email, calendar, files, settings, travel, purchase
- 3 perturbation families: clean, stale memory, tool injection
- 5 repeated trials per scenario
- 1,440 trials per reference policy

## Reference-policy results

| Policy | Trial success | Hard-safe | Injection resistance | Stale-memory resistance | pass@5 | all-success@5 |
|---|---:|---:|---:|---:|---:|---:|
| Naive personalization | 0.271 | 0.417 | 0.688 | 0.771 | 0.271 | 0.271 |
| Risk-aware | 0.813 | 1.000 | 1.000 | 0.938 | 0.813 | 0.813 |
| Noisy risk-aware | 0.765 | 0.983 | 0.992 | 0.921 | 0.840 | 0.566 |
| Contract oracle | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

The deliberately noisy policy illustrates why repeated-trial reliability matters: it succeeds at least once on many scenarios (`pass@5 = 0.840`) while succeeding on every repeat far less often (`all-success@5 = 0.566`).

## Perturbation stress

Naive personalization degrades sharply under tool injection (`trial success = 0.063`, `hard-safe = 0.125`), while the risk-aware policy remains hard-safe across all three perturbation families. This demonstrates that the evaluator can distinguish preference-following from permission-aware behavior.

## Interpretation
The suite validates evaluator sensitivity and trajectory accounting. It does not establish that PCO-Robust, an LLM, or any deployed assistant achieves these numbers. The next step is to plug real model policies into the same task/trial/grader/trajectory interface.
