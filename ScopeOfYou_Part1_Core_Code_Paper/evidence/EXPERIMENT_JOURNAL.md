# Experiment Journal — Scope of You

> Curated from retained artifacts in this repository. It is not reconstructed shell history. Every entry links to evidence.

## Exp-001 — Clean SFT baseline
**Status:** `executed`

**Hypothesis.** A clean held-out-user SFT baseline is needed before reward or contract optimization is interpretable.

**Setup.** Clean v2 split with user-level holdout; baseline checkpoint evaluated on PersonalBench dimensions.

**Result.** PersonalBench 0.9930 on 500 held-out validation interactions; factuality 0.9966; proactivity 0.9826.

**Interpretation.** The supervised baseline is already strong; later gains must be selective rather than generic.

**Next decision.** Use SFT as utility anchor and report all later regressions against it.

**Evidence.** `reports/FAILURE_REPORT.md`

## Exp-002 — Unconstrained reward optimization
**Status:** `failed`

**Hypothesis.** Directly optimizing learned personalized reward should improve preference fit without harming protected behavior.

**Setup.** Learned reward optimized with a weak drift penalty.

**Result.** PersonalBench collapsed to 0.6240; factuality to 0.0360; proactivity to 0.4637; 850 threshold failures.

**Interpretation.** In-distribution reward accuracy did not prevent off-support exploitation.

**Next decision.** Add reference regularization, supervised anchors, protected dimensions, and clipping.

**Evidence.** `reports/FAILURE_REPORT.md`

## Exp-003 — Constrained reward repair
**Status:** `executed`

**Hypothesis.** Anchoring optimization to the supervised region should recover protected behavior while retaining personalization.

**Setup.** Stronger reference regularization + supervised anchor loss + protected dimensions + reward-domain clipping.

**Result.** PersonalBench recovered to 0.9752; personalization 0.9988; factuality 0.9990; threshold failures 0/500.

**Interpretation.** The repair prevents catastrophic reward exploitation, but still does not beat SFT overall because proactivity is worse.

**Next decision.** Keep the trade-off visible and stop treating one scalar reward as the main claim.

**Evidence.** `reports/FAILURE_REPORT.md`

## Exp-004 — Explicit-template PCO
**Status:** `failed`

**Hypothesis.** A contract optimizer that succeeds on explicit APPLY/SUPPRESS cues will generalize to equivalent implicit language.

**Setup.** Initial PCO trained/evaluated with explicit contract phrases, then tested on independently worded ContractBench-Implicit.

**Result.** The first PCO looked strong internally but underperformed SFT/BATPO on the independent implicit suite.

**Interpretation.** The method learned lexical/template shortcuts rather than semantic scope.

**Next decision.** Keep the harder benchmark and redesign training around disjoint natural paraphrases + history-inferred preference interventions.

**Evidence.** `reports/paper_grade_study.json`, `docs/RESEARCH_DECISION_LOG.md`

## Exp-005 — PCO-Robust five-seed study
**Status:** `executed`

**Hypothesis.** Semantic scope training should recover implicit contract generalization across users and seeds.

**Setup.** PCO-Robust; 5 seeds (41, 53, 67, 79, 97); 1,460 implicit cases; 20 held-out users.

**Result.** ContractBench-Implicit 0.7910 ± 0.0008; PersonalBench 0.9449 ± 0.0005; +10.46 pp over BATPO, 95% CI [8.65, 12.24], 20/20 users improved.

**Interpretation.** The redesign repairs the independent selectivity failure, but creates a measurable generic-utility cost.

**Next decision.** Treat selectivity and utility as a Pareto problem; add non-inferiority analysis.

**Evidence.** `reports/paper_grade_robust_study.json`

## Exp-006 — Contract-objective ablations
**Status:** `executed`

**Hypothesis.** Every PCO objective term is necessary for the headline improvement.

**Setup.** Remove one objective component at a time from controlled PCO training.

**Result.** Full CBI 0.7354; no-context-contract 0.6403; several invariant/attack removals were nearly unchanged.

**Interpretation.** The context-selective term is dominant here; not every objective term is empirically necessary in this backend.

**Next decision.** Do not overclaim component necessity; carry redundant-looking terms forward only as hypotheses for harder LLM settings.

**Evidence.** `reports/paper_grade_robust_study.json`

## Exp-007 — Selectivity–utility Pareto sweep
**Status:** `executed`

**Hypothesis.** Increasing contract weight should improve selectivity without a meaningful utility cliff.

**Setup.** Sweep contract scale from 0.0 to 2.0 with fixed evaluation.

**Result.** Contract score rises from 0.6193 at scale 0.0 to ~0.735 around 1.0, while PersonalBench peaks earlier (~0.979 at 0.5) and then declines.

**Interpretation.** The objective creates a real frontier rather than a uniformly better solution.

**Next decision.** Report the frontier and freeze a utility non-inferiority gate before external LLM runs.

**Evidence.** `reports/paper_grade_robust_study.json`, `paper/figures/utility_selectivity_tradeoff.png`

## Exp-008 — Paraphrase-consistency regularizer
**Status:** `failed`

**Hypothesis.** Explicit paraphrase consistency should improve wording robustness without degrading other metrics.

**Setup.** Add a consistency regularizer to PCO-Robust and compare on the same implicit suite.

**Result.** Contract score +0.0007, but paraphrase robustness -0.0014 (worse).

**Interpretation.** A tiny macro-score gain hid deterioration on the intended robustness target.

**Next decision.** Reject the variant from the headline method and keep it as a negative result.

**Evidence.** `reports/consistency_regularization_negative.json`

## Exp-009 — Uncertainty + non-inferiority analysis
**Status:** `executed`

**Hypothesis.** Five-seed disagreement can serve as calibrated ambiguity confidence, and utility loss may fit a 2-point non-inferiority margin.

**Setup.** Ensemble disagreement across five PCO-Robust seeds + paired user bootstrap against SFT.

**Result.** Error-detection AUROC 0.635; uncertain/determinate disagreement ratio 1.032; utility delta -4.56 pp, 90% CI [-4.75, -4.36]; 2-pp gate fails.

**Interpretation.** Disagreement is diagnostic, not calibrated confidence; utility preservation cannot be claimed under the frozen margin.

**Next decision.** Use disagreement only for selective-risk diagnostics and keep the utility trade-off explicit.

**Evidence.** `reports/uncertainty_noninferiority.json`

## Exp-010 — Personalization leakage measurement
**Status:** `executed`

**Hypothesis.** Improved contract score should imply lower protected-dimension leakage.

**Setup.** Counterfactually change preferences and measure unintended factuality/non-sycophancy movement over 1,200 cases.

**Result.** PCO-Robust protected leakage 0.000927; BATPO 0.000195.

**Interpretation.** Absolute leakage is small, but PCO-Robust is not better than BATPO on this metric.

**Next decision.** Keep leakage as a separate endpoint and avoid claiming protected-dimension superiority.

**Evidence.** `reports/personalization_leakage.json`

## Exp-011 — Stateful agentic contract stress test
**Status:** `executed_stress_test`

**Hypothesis.** A task/trial/grader harness should distinguish naive personalization from permission-aware behavior under stale memory and tool injection.

**Setup.** 288 scenarios × 5 trials across clean, stale-memory, and tool-injection variants; deterministic/noisy reference policies.

**Result.** Naive trial success 0.271; risk-aware 0.812; noisy risk-aware pass@5 0.840 vs all-success@5 0.566.

**Interpretation.** The evaluator exposes permission, perturbation, and repeated-trial reliability failures; this is evaluator validation, not an LLM capability result.

**Next decision.** Use the harness in the frozen external LLM matrix only after real model outputs exist.

**Evidence.** `reports/agentic_contract_suite_v2_summary.json`
