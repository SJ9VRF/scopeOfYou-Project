# Public SOTA Evaluation Gate — Release 1.1.0

## Status
**Not yet SOTA.** Current evidence is controlled synthetic evidence with a small executable behavioral model.

## Public benchmark matrix
| Capability | Benchmark | Required comparison |
|---|---|---|
| Personalized reward inference | Personalized RewardBench / PersonalRewardBench | P-GenRM, VRF, general RM, user-specific RM |
| Heterogeneous user preferences | PersonalLLM | meta-learning / in-context / reward-factorization baselines |
| Preference reversal/evolution | AlignX / AlignXplore-compatible splits; ALOE-Unseen where applicable | AlignXpert, PersonalAgent |
| Context preference selectivity | BenchPreS | zero-shot/reasoning/mitigation baselines; RP-Reasoner where compatible |
| Rational memory use | RPEval | RP-Reasoner and memory-selection baselines |
| Over-personalization | OP-Bench | BASE, memory baselines, Self-ReCheck |
| Personalized agentic RL | ETAPP / ETAPP-Hard / SJAgent if accessible | PARPO and non-personalized RL baselines |

## LLM matrix
At least two open-weight model families, ideally one 3B-class development model and one 7B/8B-class main model. Match baseline model scale and training budget.

## Statistical requirements
- >=3 seeds for training comparisons
- user-level bootstrap confidence intervals
- official test splits
- contamination/dedup audit
- report both ordinary utility and contract/selectivity metrics
- report Pareto frontier rather than hiding utility-vs-contract tradeoffs

## Claim policy
Use "SOTA" only if PCO is best on the official metric of at least two public benchmarks under matched scale and remains non-inferior on generic quality/safety. Otherwise say exactly what is best (e.g., "best contract score among tested methods") without global SOTA language.


## Implemented in release 1.0.0
- BenchPreS schema adapter + AAR/MR/selectivity scorer
- Personalized RewardBench schema adapter with rubric/narrative no-leak guard
- AlignX schema adapter preserving its preference-direction/persona evidence
- machine-readable smoke fixtures and unit tests

See `docs/PUBLIC_BENCHMARKS.md` and `reports/SOTA_BASELINE_MATRIX.md`.
