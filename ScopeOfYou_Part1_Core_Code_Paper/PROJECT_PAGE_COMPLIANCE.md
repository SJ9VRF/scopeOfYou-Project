# Scope of You — Project Page Compliance Matrix

**Author:** Aura Yavary

This matrix maps every requested project-page requirement to the implemented artifact. Project dates are intentionally omitted everywhere.

| # | Required section | Implemented evidence |
|---|---|---|
| 1 | Hero | Project name, one-line problem, main result, Aura Yavary, and Paper / Code / Demo / Benchmark / Video CTAs at the top of `index.html`. |
| 2 | Why this problem matters | Explicit problem, difficulty, and “why current approaches fail” explanation. |
| 3 | Core idea | 2–3 sentence formulation plus exact novelty: typed APPLY / SUPPRESS / MUST-NOT-AFFECT personalization contracts and PCO. |
| 4 | Architecture | End-to-end system diagram plus post-training/RL, contract-eval, failure-recovery, agent, and permission loops. |
| 5 | My contribution | Explicitly states what Aura Yavary designed, implemented, and which technical decisions are project-owned. |
| 6 | Experiments | Data/tasks, baselines, ablations, and an explicit held-out evaluation setup. |
| 7 | Results | Clean baseline-to-method tables with Contract Score / PersonalBench plus success-pass rate, recovery, latency, and cost disclosure. |
| 8 | Failure analysis | Concrete falsification, reward-exploitation, scope-leakage, and rejected-regularizer failures with causes and recovery/decision paths. |
| 9 | Interactive demo | Live checkpoint inspector plus embedded contract trace explorer and agentic trajectory viewers. |
| 10 | Scaling | Explicit model size, task horizon, tool count, cost/latency, robustness, and training-signal scale. |
| 11 | Safety / limitations | Remaining failures, irreversible-action boundaries, permission constraints, and human escalation. |
| 12 | Technical deep dive | Technical report, ML systems design, benchmark methodology, and claims/limitations links. |
| 13 | Artifacts | Paper, Code, GitHub-ready repository guide, Benchmark, Dataset, Demo, Video, Technical report, and Blog post. |
| 14 | Citation | Copy-ready BibTeX with Aura Yavary and publication year 2026. |

## 60-second hiring-manager test

The page is intentionally ordered so the first viewport and first results section answer four questions quickly:

1. **What problem?** Personalization can overreach into contexts or protected behavior where it should not apply.
2. **What contribution?** Personalization Contract Optimization with APPLY / SUPPRESS / MUST-NOT-AFFECT behavior.
3. **What result?** +10.46 percentage points ContractBench-Implicit over BATPO, a 95% hierarchical-bootstrap CI of [+8.65, +12.24] pp, and positive deltas for 20/20 held-out users.
4. **Does it work?** The page links directly to executed checkpoints, demo, trajectory, benchmark, paper, failure analysis, and reproducibility artifacts.

## Automated enforcement

Run:

```bash
make project-page-audit
make date-audit
```

`project-page-audit` checks both `index.html` and `portfolio/index.html`, verifies the required content and all relative artifact links, and fails if a required project-page element is missing.

## Evidence Layer — required second layer

The polished 14-section project page is not sufficient on its own. The release must also preserve an inspectable research-process layer containing:

- `evidence/EXPERIMENT_JOURNAL.md` — hypothesis → setup → result → interpretation → next decision;
- `evidence/FAILED_EXPERIMENTS.md` — retained negative results and repairs;
- `evidence/DECISION_LOG.md` — Decision → Alternatives → Evidence → Trade-off → Outcome;
- `evidence/REAL_EVAL_TABLES.md` — baselines, seeds, N, confidence intervals, reliability, latency, and cost boundaries;
- `evidence/UNEXPECTED_FINDINGS.md` — findings that changed the story;
- `evidence/FAILURE_TRACE.md` — one end-to-end falsification → redesign → trade-off trace;
- `evidence/GIT_HISTORY.md` + `history/` — honest incremental history beginning at the audited baseline import;
- `artifacts/` — raw eval outputs, failures, plots, configs, qualitative cases, and ablations.

Run `make verify-evidence` to enforce this layer.
