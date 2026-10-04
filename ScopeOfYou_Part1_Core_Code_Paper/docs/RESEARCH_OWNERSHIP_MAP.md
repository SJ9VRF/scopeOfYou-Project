# Research Ownership Map

**Public author:** Aura Yavary

This map makes the intellectual and implementation ownership legible without turning the page into a résumé. Each row points to executable or inspectable artifacts.

| Research choice / artifact | Ownership demonstrated by | Inspect |
|---|---|---|
| Problem formulation: scope of known preference effects | APPLY / SUPPRESS / MUST-NOT-AFFECT contract formulation and paper framing | `paper/main.tex`, `CLAIMS_AND_LIMITATIONS.md` |
| Independent falsification benchmark | ContractBench-Implicit generator/export/evaluator | `src/personal_agi_pt/contractbench.py`, `src/personal_agi_pt/contractbench_eval.py`, `data/contractbench_implicit.jsonl` |
| Redesign after shortcut failure | PCO-Robust semantic/context-history interventions | `src/personal_agi_pt/contract_opt.py`, `evidence/FAILURE_TRACE.md` |
| Statistical design | five-seed aggregation, hierarchical bootstrap, non-inferiority analysis | `scripts/analyze_uncertainty_and_noninferiority.py`, `reports/paper_grade_robust_study.json` |
| Negative-result discipline | raw reward failure + rejected consistency regularizer | `reports/FAILURE_REPORT.md`, `reports/consistency_regularization_negative.json` |
| Agentic extension | task/trial/grader/trajectory evaluator with permission transitions | `src/personal_agi_pt/agentic_eval_v2.py`, `docs/AGENTIC_EVAL_DESIGN.md` |
| External validation plan | frozen 36-run two-family LLM matrix + result schema | `external_runs/run_plan.json`, `external_runs/result.schema.json` |
| Human evaluation design | blinded, multi-rater protocol with clustered analysis | `docs/HUMAN_EVAL_PROTOCOL.md`, `human_eval/EXECUTION_CHECKLIST.md` |
| Reproducibility / claim discipline | experiment ledger, evidence manifest, citation provenance, release audits | `experiments/EXPERIMENT_LEDGER.jsonl`, `scripts/verify_frontier_artifact.py` |
| Evidence-rich project page | 14-section homepage + experiment journal + failure/decision/raw-artifact layer | `index.html`, `evidence/` |

## What this map does not assert

It does not claim that every dependency, baseline idea, or research concept originated here. Prior work is explicitly separated in `NOVELTY_AUDIT.md` and `docs/RELATED_WORK.md`. The point is to show which **problem-definition, implementation, evaluation, debugging, and decision-making artifacts** belong to this project.
