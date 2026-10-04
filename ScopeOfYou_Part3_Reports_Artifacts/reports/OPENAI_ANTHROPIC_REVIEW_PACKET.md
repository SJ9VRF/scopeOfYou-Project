# Scope of You — Frontier Lab Review Packet

## One-line research question
Can a personalized assistant learn not only *what* a user prefers, but *where that preference is allowed to change behavior*?

## Core contribution
**Personalization Contract Optimization (PCO-Robust)** models three obligations: `APPLY`, `SUPPRESS`, and `MUST-NOT-AFFECT`, and trains with matched user-state, context, and protected-property interventions.

## Strongest executed evidence
- independent implicit stress suite exposes failure of the first PCO method;
- revised PCO-Robust improves ContractBench-Implicit across 20/20 held-out users and five seeds;
- hierarchical user→case bootstrap is reported;
- utility/selectivity tradeoff is visible rather than hidden;
- ablations identify context-selective training as the dominant controlled component;
- reward-optimization and consistency-regularization failures are retained;
- protected leakage and non-inferiority tests constrain claims.

## Systems/evaluation signal
- reproducible checkpoints/configs;
- user-held-out data audits;
- public-benchmark adapters;
- local service + benchmark CLI;
- Docker/CI/provenance/SBOM;
- human-eval execution kit;
- agentic task/trial/grader/trajectory harness with end-state and permission graders.

## What is intentionally not claimed
- no frontier-LLM SOTA claim;
- no official public-benchmark model result;
- no human-preference result;
- no production tool-use claim;
- no calibrated uncertainty claim.

## Best 10-minute review path
1. `paper/main.pdf`
2. `reports/RESULTS_TABLE.md`
3. `reports/CLAIM_EVIDENCE_MATRIX.md`
4. `reports/REVIEWER_ATTACK_MATRIX.md`
5. `docs/RESEARCH_DECISION_LOG.md`
6. `docs/AGENTIC_EVAL_DESIGN.md`
7. `src/personal_agi_pt/contract_opt.py`
8. `src/personal_agi_pt/agentic_eval.py`
9. `reports/paper_grade_robust_study.json`
10. `CLAIMS_AND_LIMITATIONS.md`

## Frontier handoff additions
- `reports/AGENTIC_EVAL_V2_SUMMARY.md` — repeated-trial agentic evaluator stress test with stale-memory/tool-injection variants and hard safety gates.
- `reports/FRONTIER_READINESS_MATRIX.md` — claim ceiling and evidence-status map.
- `configs/frontier/llm_experiment_matrix.json` — frozen 36-run external LLM matrix.
- `external_runs/result.schema.json` — required provenance/result schema for external GPU runs.
- `docs/EXTERNAL_EXECUTION_HANDOFF.md` — exact handoff from controlled evidence to GPU/human studies.
- `human_eval/EXECUTION_CHECKLIST.md` — fail-closed checklist before any human-validated claim.

## What v2 agentic evaluation adds
The earlier agentic harness checked one action per task. The v2 suite adds repeated stochastic trials, permission acquisition and second-step recovery, stale-memory conflicts, untrusted tool-text injection, and two complementary reliability endpoints (`pass@5` and `all-success@5`). This is still an evaluator sanity check, not model capability evidence.
