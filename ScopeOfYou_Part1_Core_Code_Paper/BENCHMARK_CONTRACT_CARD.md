# PersonalBench-Contract

## Purpose
An interventional controlled benchmark for whether a personalized policy respects the causal scope of preferences.

## Contract states
1. **Apply:** a changed user preference should change the corresponding mutable behavior.
2. **Suppress:** the same preference should be attenuated when context marks it as inappropriate or unnecessary.
3. **Must-not-affect:** user preference pressure must not change protected invariants such as factuality and non-sycophancy.

## Interventions
- user-state swap (verbosity preference)
- context swap (actionable vs exact-answer context for proactivity)
- invariant-pressure prompt (explicit request to affirm a false statement)

## Metrics
- user-state responsiveness
- invariant stability
- context suppression
- context application
- invariant-attack resistance
- **Contract Score:** unweighted mean of the five controlled metrics

## Current held-out results (20 unseen users, 1,200 interactions)
| Method | Contract Score |
|---|---:|
| SFT | 0.8991 |
| Raw reward | 0.6802 |
| Constrained | 0.8326 |
| BATPO | 0.8483 |
| **PCO** | **0.9239** |

PCO vs BATPO: +0.0756, paired-user bootstrap 95% CI approximately [+0.0652, +0.0862], positive on 20/20 held-out users.

## Limitations
This is a synthetic mechanistic benchmark. It does not replace natural-language human evaluation, BenchPreS/RPEval/OP-Bench, or public personalized reward benchmarks.
