# Scope of You — reviewer path

**Aura Yavary**  
**Question:** When a model knows a user's preference, where is that preference allowed to change behavior?

## 2-minute read

1. `HIRING_MANAGER_60_SECOND.md` — the whole research story in one minute.
2. `RESEARCH_LEAD_BRIEF.md` — question, failed hypothesis, executed evidence, tradeoff, next decisive test.
3. `reports/EXECUTED_EVIDENCE_MANIFEST.json` — machine-readable list of what was actually executed.
4. `experiments/EXPERIMENT_LEDGER.jsonl` — artifact hashes and reproduction entrypoints for executed/pending experiments.
5. `paper/main.pdf` — full paper.
6. `docs/CITATION_PROVENANCE_AUDIT.md` — stable IDs/venues for the closest recent prior art.

## What is actually new here

The project does **not** claim that personalization, context gating, causal interventions, over-personalization, or permission boundaries are individually new. The candidate contribution is a **training-time scope formulation for a known user-preference effect** using three obligations: `APPLY`, `SUPPRESS`, and `MUST-NOT-AFFECT`, paired with matched interventions and an agentic permission extension.

## Strongest executed evidence

On the independently worded ContractBench-Implicit controlled suite, PCO-Robust scores **0.7912** versus **0.6866** for BATPO. The user→case hierarchical bootstrap difference is **+0.1046** with 95% CI **[+0.0865, +0.1224]**, positive for **20/20** held-out users.

The result is **not** a universal win. PersonalBench utility drops relative to SFT and the predeclared **2-point non-inferiority gate is not met**. Paraphrase sensitivity also remains unresolved.

## The failure that changed the project

The first PCO version looked successful on its explicit, co-designed contract test and **failed on the independent implicit benchmark**. The benchmark was not weakened. The method was redesigned to use disjoint semantic/context-history interventions; the failed implementation and negative results remain in the repository.

## What is not proven

No claim is made yet of frontier-LLM SOTA, human superiority, calibrated uncertainty, or production-agent safety. The repository freezes a 36-run two-family 7–8B study and a blinded human-evaluation protocol; those are external execution gates, not completed results.

## Reproduce / verify

```bash
make verify-reviewer
```

This self-contained check validates the reviewer package itself: headline evidence against source reports, dataset cardinalities, frozen external plan, non-LLM scoping of agentic stress tests, identity/title consistency, and unfinished-placeholder hygiene.

The **full research archive** has a separate, stronger contract: `make verify-frontier`, which additionally runs the complete repository test suite and checks fixtures/checkpoints intentionally omitted from this lean bundle.


## Provenance

`experiments/EXPERIMENT_LEDGER.jsonl` records each preserved experiment as `executed` or `planned_not_executed`, with content hashes for its input/output artifacts and a reproduction entrypoint. Historical shell commands are **not** retroactively invented; the ledger says so explicitly. `make verify-reviewer` rejects hash drift or an external gate that starts looking like a completed result.
