# Personalization Contracts
## Interventional Post-Training for When AI Should Adapt, Suppress, or Stay Invariant

### Abstract
Personalized RLHF, temporal preference evolution, personalized reward models, user-specific anchors, and context-aware preference suppression all have strong prior art. This project therefore studies a narrower problem: **the causal scope of personalization**. We introduce Personalization Contract Optimization (PCO), which assigns behavior/context pairs one of three obligations: apply a preference, suppress it, or prevent it from affecting a protected invariant. PCO trains against matched user-state, context, and invariant-pressure interventions. On 1,200 held-out interactions from 20 unseen synthetic users, PCO reaches 0.9239 PersonalBench-Contract versus 0.8483 for BATPO, with a paired-user delta of +0.0756 (95% bootstrap CI approximately [+0.0652,+0.0862], positive on 20/20 users). PCO scores 0.9545 on ordinary PersonalBench versus BATPO's 0.9614, making the utility/selectivity tradeoff explicit. SFT remains the ordinary-score ceiling at 0.9905. The public-benchmark and open-weight LLM comparisons remain the next validation step.

## 1. Research question
A personal agent should not treat every stored or inferred preference as globally binding. The operational question is:

> Under an intervention on user state or context, which outputs should change, which should be suppressed, and which must remain invariant?

## 2. Contract formalization
PCO uses three contract states:
- **Apply:** a relevant user-state change should produce the corresponding mutable behavior shift.
- **Suppress:** a known preference should be attenuated when the task context makes it irrelevant or inappropriate.
- **Must-not-affect:** preference pressure must not move protected properties such as factuality and non-sycophancy.

The controlled lab maps personalization/verbosity to a mutable control, proactivity to a context-gated control, and factuality/non-sycophancy to protected invariants.

## 3. Interventions
- user-state swap: change verbosity preference while holding task content fixed;
- context swap: hold the user fixed while changing whether proactivity is appropriate;
- invariant attack: explicitly pressure the model to affirm a false statement as a personal preference.

## 4. Executed results
| Method | PersonalBench | Contract Score |
|---|---:|---:|
| SFT | **0.9905** | 0.8991 |
| Raw learned-reward optimization | 0.8399 | 0.6802 |
| Previous constrained repair | 0.9481 | 0.8326 |
| BATPO | 0.9614 | 0.8483 |
| **PCO** | 0.9545 | **0.9239** |

PCO vs BATPO Contract Score: +0.0756, paired-user bootstrap 95% CI approximately [+0.0652,+0.0862], positive for all 20 held-out users.

## 5. What is and is not novel
Not claimed as novel: personalized RLHF, reward decomposition, user-specific anchors, preference reversal/evolution, counterfactual user simulation, over-personalization detection, preference suppression, or generic causal reward robustness.

Candidate contribution: **joint training-time optimization of apply/suppress/must-not-affect personalization contracts using distinct causal intervention families plus one joint contract metric.**

## 6. SOTA boundary
The project is not yet SOTA by a public standard. A SOTA claim requires real LLM experiments on public datasets/benchmarks including Personalized RewardBench or PersonalRewardBench, PersonalLLM, AlignX/ALOE-Unseen preference-change settings, BenchPreS/RPEval, OP-Bench, and an agentic setting compatible with PARPO if making an agentic-RL claim.

## 7. Limitations
Synthetic users, programmatic contract labels, small behavioral model, and no executed longitudinal human study. Literature search cannot prove absolute priority. The contribution should therefore be described as a sharply differentiated candidate method with controlled evidence, not as a guaranteed first or SOTA result.
