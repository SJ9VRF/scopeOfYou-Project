# SOTA Baseline Matrix — Release 1.1.0

No SOTA claim is permitted until all rows marked **required** have matched-scale results.

| Capability | Public benchmark | Required baselines | PCO result status |
|---|---|---|---|
| Personalized reward inference | Personalized RewardBench | P-GenRM, public RM baselines, matched discriminative/generative RM | Adapter ready; not executed |
| User-level alignment | AlignX testbeds | AlignXpert ICA/PBA, same backbone SFT/DPO | Adapter ready; not executed |
| Preference selectivity | BenchPreS | frontier/base prompting baseline, benchmark authors' reported setup where reproducible | Adapter + scorer ready; not executed |
| Rational memory use | RPEval | RP-Reasoner, direct-memory baseline | Planned adapter |
| Causal personalization | personalization generation benchmarks | NextQuill, same-backbone SFT | Planned matched-scale comparison |
| Agentic personalized RL | ETAPP / ETAPP-Hard / SJAgent | PARPO, generic RL, memory/RL baselines | Out of current controlled scope |

## Claim policy

A paper/homepage may use **SOTA** only when:

1. the official public test split is used;
2. benchmark canaries are excluded from training data;
3. the model backbone and parameter budget are matched or normalized;
4. at least 3 seeds are reported for trained methods;
5. confidence intervals or paired significance tests are reported;
6. official evaluation scripts or faithful reimplementations are used;
7. hyperparameters are not selected on the test set;
8. all negative/regression dimensions are reported alongside headline gains.
