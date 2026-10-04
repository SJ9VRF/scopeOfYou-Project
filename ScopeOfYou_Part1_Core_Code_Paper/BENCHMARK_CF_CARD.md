# PersonalBench-CF: Counterfactual Personalization Boundary Stress Suite

## Purpose
PersonalBench-CF asks a narrower question than standard personalization benchmarks:

> If only the user's mutable preference state changes, does the policy change the personalized behavior that should change while preserving behavior that should not change?

## Intervention
For each held-out test interaction, construct a counterfactual with the query fixed and the verbosity preference intervened upon (for example concise -> detailed). All protected factual/task context remains unchanged.

## Metrics
- **Counterfactual responsiveness:** agreement between the expected preference-induced change and the model's change.
- **Invariant stability:** factuality and non-sycophancy stability under the user-state intervention.
- **Direction accuracy:** whether the personalized control moves in the correct direction.
- **Uncertainty budget score:** whether optimization-induced movement remains within the confidence-scaled trust budget relative to the SFT reference.
- **Boundary score:** mean of the applicable components above.

## Executed results
| Method | Responsiveness | Invariant stability | Direction | Budget | Boundary score |
|---|---:|---:|---:|---:|---:|
| SFT | 0.9906 | 0.9996 | 1.0000 | n/a | 0.9967 |
| Raw reward optimization | 0.7466 | 0.9999 | 1.0000 | 0.2519 | 0.7496 |
| Constrained repair | 0.8578 | 0.9996 | 1.0000 | 0.9377 | 0.9488 |
| Boundary-aware optimization | **0.8810** | **0.9998** | **1.0000** | **0.9943** | **0.9688** |

## Limitations
The current suite uses controlled behavioral outputs and synthetic preference states. It is a mechanistic stress test, not a substitute for public language-generation benchmarks or longitudinal human evaluation.
