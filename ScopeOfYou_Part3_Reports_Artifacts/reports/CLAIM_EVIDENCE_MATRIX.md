# Claim → Evidence Matrix

This file is a release gate: every substantive paper claim is mapped to executed evidence. Claims without executed evidence are labeled **planned** and must not be phrased as results.

| Claim | Status | Evidence | Allowed wording |
|---|---|---|---|
| Explicit-template contract training does not generalize to implicit contexts | Executed | `reports/paper_grade_study.json`, `reports/paper_grade_robust_study.json`, `ContractBench-Implicit` | “fails/regresses on the independent implicit suite” |
| PCO-Robust improves independent contract selectivity vs BATPO | Executed | five seeds; hierarchical bootstrap in `reports/paper_grade_robust_study.json` | `+0.1046`, 95% CI `[+0.0865,+0.1224]` |
| PCO-Robust improves independent contract selectivity vs SFT | Executed | same report | `+0.0777`, 95% CI `[+0.0632,+0.0917]` |
| Gains hold across held-out users | Executed | per-user paired comparison | positive delta on 20/20 users |
| Context-selective training is the dominant ablation in the controlled backend | Executed | fixed-budget ablation suite | “largest diagnostic degradation when removed” |
| PCO-Robust improves OOD and worst-contract scores | Executed | `reports/paper_grade_robust_study.json` | report exact controlled values |
| PCO-Robust is more paraphrase-sensitive than SFT/BATPO | Executed negative result | stress table + rejected consistency variant | must be disclosed as limitation |
| PCO-Robust preserves general PersonalBench utility | **Not established under strict margins** | `reports/uncertainty_noninferiority.json` | do **not** say “without hurting utility”; 1–3pp NI margins fail |
| A permissive 5pp non-inferiority margin passes | Executed | same report | may be reported only with the precondition that 5pp is permissive |
| Five-seed disagreement is a useful uncertainty signal | Partially executed | AUROC ≈0.635; selective coverage curve | call it an epistemic diagnostic, not calibrated confidence |
| Ambiguous contracts are intrinsically more uncertain | **Not established** | uncertain/determinate SD ratio ≈1.03 | do not claim meaningful separation |
| Protected personalization leakage is negligible | Executed only in controlled backend | `reports/personalization_leakage.json` | report absolute values and note PCO-Robust leaks more than BATPO though magnitude <0.001 |
| PCO is SOTA on public personalization benchmarks | **Not executed** | public benchmark adapters only | prohibited claim |
| PCO improves generative LLM behavior | **Not executed** | frozen 7–8B experiment matrix only | planned validation only |
| Human raters prefer PCO responses / validate contracts | **Not executed** | human protocol + unlabeled sample only | planned validation only |

## Release rule

A result can move from **planned** to **executed** only when the corresponding raw outputs, evaluation code, model/checkpoint identity, and statistical report are bundled. Website copy and the abstract must obey the same gate.
