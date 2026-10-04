# Research Decision Log

This is not a release chronology. It records the scientific decisions that changed the project.

## Decision 1 — Do not treat personalization as scalar preference fit
Early reward optimization improved its own objective while degrading behavior. The project moved from scalar personalization reward to explicit protected dimensions and contract-scoped intervention.

## Decision 2 — Reject the first apparent PCO win
The first PCO formulation scored well on an evaluation suite that shared explicit contract language with training. A separately phrased implicit suite reversed the conclusion: the method did not generalize. The evaluation was kept; the method changed.

## Decision 3 — Train semantic scope rather than literal scope cues
PCO-Robust replaced fixed suppression/application phrases with disjoint paraphrase families and history-inferred preference interventions. The revised method recovered contract performance on the implicit suite across all held-out users and five training seeds.

## Decision 4 — Keep the utility tradeoff visible
PCO-Robust improves selective personalization but reduces aggregate PersonalBench utility relative to SFT. The project therefore reports a Pareto frontier and non-inferiority analysis rather than collapsing the result into one score.

## Decision 5 — Reject a consistency regularizer that did not work
A paraphrase-consistency variant was trained to target the remaining wording sensitivity. It failed to improve the desired robustness metric and is retained as a negative result instead of becoming part of the method.

## Decision 6 — Do not promote ensemble disagreement to calibrated uncertainty
Five-seed disagreement has some error-detection signal but does not cleanly separate ambiguous from determinate cases. It is reported as an epistemic diagnostic, not calibrated confidence.

## Decision 7 — Separate response personalization from permission to act
For agentic settings, user autonomy preference is not treated as authorization. A separate task/trial/grader/trajectory harness tests state mutation and permission boundaries. Its current outputs are benchmark sanity checks, not frontier-model results.

## Decision 8 — Freeze external gates before seeing outcomes
Model families, seeds, public benchmarks, human-study endpoints, non-inferiority margins, and claim rules are fixed before external LLM/human execution. This is intended to reduce post-hoc benchmark and claim selection.
