# Scope of You — Research Lead Brief

**Aura Yavary**  
**Scope of You: Learning Where Personalization Is Allowed to Matter**

## The question

A personalized model can know a user's preference and still apply it in the wrong place. The research question is therefore not only **what does this user prefer?** but **where is that preference allowed to change behavior?**

Scope of You represents that scope with three typed obligations:

- `APPLY` — the preference should change behavior here.
- `SUPPRESS` — the preference is known, but should not affect this context.
- `MUST-NOT-AFFECT` — personalization must not move protected behavior such as factuality or non-sycophancy; the agentic extension separately tests action authority and permission boundaries.

## The falsification that changed the project

The first implementation looked strong on an explicit, co-designed contract evaluation. It then **failed on ContractBench-Implicit**, where the same semantics were expressed indirectly through natural context and conversational history. That failure is retained in the release.

The response was not to weaken the benchmark. The training intervention changed: explicit control-like phrasing was replaced with disjoint semantic/context-history interventions, producing **PCO-Robust**.

## Strongest executed evidence

On **ContractBench-Implicit** (1,460 cases; 20 held-out users):

| Method | ContractBench-Implicit | PersonalBench |
|---|---:|---:|
| SFT | 0.7135 | **0.9905** |
| BATPO | 0.6866 | 0.9614 |
| **PCO-Robust** | **0.7912** | 0.9448 |

Across five independent training seeds, PCO-Robust reaches **0.7910 +/- 0.0008** ContractBench-Implicit and **0.9449 +/- 0.0005** PersonalBench. Hierarchical user->case bootstrap gives **+0.1046** over BATPO (95% CI **[+0.0865, +0.1224]**) with positive per-user deltas for **20/20** held-out users.

The result is intentionally a tradeoff, not a victory lap: selective personalization improves while generic PersonalBench utility drops relative to SFT. A 2-point utility non-inferiority gate is **not** met in the controlled study.

## What the ablation says

The strongest controlled driver is the **context-selective intervention**. Several invariant/attack components are near ceiling in this small backend and do not show equally strong marginal necessity. The release therefore does not claim that every loss term is independently essential.

## Why this is more than a benchmark demo

The repository includes:

- trainable personalization and reward-modeling stack;
- negative raw-reward optimization result;
- user-held-out and phrase-disjoint evaluation;
- counterfactual user/context/invariant interventions;
- hierarchical bootstrap and non-inferiority analysis;
- agentic permission/recovery evaluator with repeated trials, stale memory, and untrusted tool text;
- public-benchmark adapters;
- frozen two-family 7-8B external experiment matrix;
- human-evaluation protocol and fail-closed claim gates;
- reproducible configs, checkpoints, tests, provenance, Docker/CI, SBOM, and release audit.

## What is not proven

This release does **not** claim frontier-model SOTA, production agent safety, real-user longitudinal robustness, human-preference superiority, or calibrated uncertainty. Those claims remain blocked until the external LLM/public-benchmark/human gates are executed.

## The next decisive experiment

Run the frozen 36-run matrix on two independent 7-8B model families, evaluate on public personalization/selectivity benchmarks plus the agentic contract suite, preserve the preregistered utility gate, and collect blinded human scope/appropriateness judgments. If the typed-scope advantage survives that matrix, the contribution graduates from controlled mechanism evidence to an LLM-scale result.

## 2-minute review path

1. `RESEARCH_LEAD_BRIEF.md` — question, falsification, evidence, limitation.
2. `paper/main.pdf` — full research argument.
3. `reports/CLAIM_EVIDENCE_MATRIX.md` — every headline claim mapped to evidence.
4. `experiments/EXPERIMENT_LEDGER.jsonl` — hashes and reproduction entrypoints for executed experiments.
5. `docs/RESEARCH_DECISION_LOG.md` — what failed and why decisions changed.
6. `reports/FRONTIER_READINESS_MATRIX.md` — executed vs pending evidence.
7. `src/personal_agi_pt/contract_opt.py` — training intervention.
8. `src/personal_agi_pt/agentic_eval_v2.py` — stateful reliability evaluator.

## One-sentence pitch

> **Scope of You learns where a known user preference is allowed to matter - when an AI should adapt, when personalization should disappear, and what it must never be allowed to change.**
