# Decision Log

Format: **Decision → Alternatives → Evidence → Trade-off → Outcome**.

## D-01 — Stop treating personalization as a scalar reward
**Alternatives.** Direct reward optimization; stronger reward model; explicit protected objectives
**Evidence.** Raw reward optimization collapsed factuality and proactivity despite optimizing its learned objective.
**Trade-off.** Protected objectives add complexity and can constrain adaptation.
**Outcome.** Moved to protected dimensions and contract-scoped intervention.

## D-02 — Keep the independent benchmark, reject the first PCO win
**Alternatives.** Tune the benchmark; keep explicit templates; redesign training
**Evidence.** PCO failed independently worded implicit scope while looking strong on co-designed language.
**Trade-off.** The redesign makes training harder and reduces the apparent headline win.
**Outcome.** Kept ContractBench-Implicit fixed and changed the method.

## D-03 — Use semantic scope training instead of literal control phrases
**Alternatives.** More control tokens; prompt-only contracts; disjoint paraphrases + history inference
**Evidence.** Template overlap explained the failure; PCO-Robust recovered across 20/20 users and five seeds.
**Trade-off.** Natural-language diversity is less controllable and more expensive to validate.
**Outcome.** Adopted disjoint phrase banks and history-inferred interventions.

## D-04 — Report a Pareto frontier instead of one score
**Alternatives.** Optimize contract score only; optimize utility only; report joint frontier
**Evidence.** Contract weight improves selectivity but eventually degrades PersonalBench.
**Trade-off.** No single operating point dominates all others.
**Outcome.** Added Pareto sweep and frozen utility non-inferiority gate.

## D-05 — Reject the paraphrase-consistency variant
**Alternatives.** Keep because macro score rose; reject because target robustness worsened
**Evidence.** Paraphrase robustness fell by 0.00136 despite a +0.00067 contract-score change.
**Trade-off.** Rejecting a superficially positive result lowers the headline but preserves metric intent.
**Outcome.** Variant excluded from headline method and retained as negative result.

## D-06 — Do not call seed disagreement calibrated uncertainty
**Alternatives.** Calibrate post hoc; use as confidence; use as diagnostic only
**Evidence.** Ambiguous/determinate disagreement ratio 1.032; AUROC 0.635.
**Trade-off.** Diagnostic uncertainty is less convenient downstream.
**Outcome.** Use abstention/selective-risk curves only; no calibrated-confidence claim.

## D-07 — Separate personalization from permission to act
**Alternatives.** Treat autonomy preference as authorization; prompt every action; model permission transition
**Evidence.** Agentic stress tests separate personalization from authorization under stale memory/tool injection.
**Trade-off.** Explicit permission states add complexity and may reduce convenience.
**Outcome.** Added ASK→ACT transitions, irreversible-action gates, and end-state verification.

## D-08 — Freeze expensive external gates before outcomes
**Alternatives.** Choose models/benchmarks after pilots; freeze matrix and margins first
**Evidence.** The controlled backend cannot establish frontier-model SOTA; post-hoc choice would weaken credibility.
**Trade-off.** Frozen plans may produce negative results and prevent opportunistic tuning.
**Outcome.** Fixed 36-run two-family matrix, public evals, seeds, and 2-pp utility margin before execution.
