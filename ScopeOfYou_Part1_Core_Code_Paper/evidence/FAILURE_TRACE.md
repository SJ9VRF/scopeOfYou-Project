# Failure Trace — From Apparent Win to Narrower Claim

This is one complete research trace from a result that initially looked good to the final, narrower claim.

1. **Initial result looked successful.** The first personalization-contract optimizer performed well on the internal explicit-contract evaluation.
2. **Independent test reversed the conclusion.** On ContractBench-Implicit, the method underperformed SFT/BATPO.
3. **Failure class identified: lexical contract shortcut.** Training and evaluation shared explicit APPLY/SUPPRESS language; the model had learned phrasing rather than semantic scope.
4. **Targeted intervention.** Replace literal control phrases with disjoint natural paraphrase families and history-inferred preference interventions.
5. **Retrain across five seeds.** PCO-Robust was trained with seeds 41, 53, 67, 79, and 97.
6. **Selectivity recovered.** Five-seed ContractBench-Implicit mean reached 0.7910 ± 0.0008; the user-level delta over BATPO was +10.46 pp with 95% CI [+8.65, +12.24], positive for 20/20 held-out users.
7. **A new regression appeared.** PersonalBench utility was lower than SFT by ~4.56 pp.
8. **Frozen utility gate failed.** The paired 90% bootstrap CI did not satisfy the 2-pp non-inferiority margin.
9. **Reporting changed instead of hiding the regression.** The final result is presented as a selectivity–utility trade-off, not “better personalization for free.”
10. **Next gate frozen before scale-up.** The two-family, 36-run 7–8B matrix and human-study endpoints remain planned—not executed or backfilled.

## Why this trace matters

The important contribution is not that every experiment worked. It is that the independent evaluation was allowed to falsify the first method, the method changed instead of the benchmark, and the final claim became narrower after the utility regression was measured.

## Raw evidence

- `reports/paper_grade_study.json` — first-method failure on the harder suite
- `reports/paper_grade_robust_study.json` — five-seed recovery, baselines, ablations, Pareto sweep
- `reports/uncertainty_noninferiority.json` — utility non-inferiority failure and selective-risk analysis
- `docs/RESEARCH_DECISION_LOG.md` — research decisions that followed the failures
