# Scope of You

**Learning Where Personalization Is Allowed to Matter**  
**Aura Yavary**  
Release 1.1.0

> **When should an AI adapt to a person, when should it suppress a known preference, and what must personalization never be allowed to change?**

## If you have 90 seconds

- **Question:** where is a known user preference allowed to change model behavior?
- **Falsification:** the first PCO implementation looked good on an explicit co-designed test and failed on an independently worded implicit suite.
- **Revision:** PCO-Robust replaces shortcut-like contract phrasing with disjoint semantic/context-history interventions.
- **Executed evidence:** 0.7912 vs 0.6866 BATPO on ContractBench-Implicit; +0.1046 hierarchical-bootstrap delta; positive for 20/20 held-out users across the comparison.
- **Tradeoff:** PersonalBench utility is lower than SFT; the preregistered 2-point non-inferiority gate is not met.
- **Not claimed:** frontier-LLM SOTA, human superiority, or production agent safety. No calibrated-uncertainty claim is made.
- **Start here:** `HIRING_MANAGER_60_SECOND.md`, then `RESEARCH_LEAD_BRIEF.md`, `reports/EXECUTED_EVIDENCE_MANIFEST.json`, and `experiments/EXPERIMENT_LEDGER.jsonl`.

Scope of You is a reproducible research system for learning the **scope of known user-preference effects**. Its executable method, **Personalization Contract Optimization (PCO)**, replaces the assumption that every remembered preference is globally applicable with typed obligations:

- **APPLY** — the preference should change behavior.
- **SUPPRESS** — the preference is known, but should not affect the current context.
- **MUST-NOT-AFFECT** — personalization must not move protected behavior such as factuality or non-sycophancy.

The project combines synthetic user-state generation, SFT-style adaptation, preference/reward modeling, counterfactual interventions, contract-aware post-training, held-out evaluation, failure mining, public-benchmark adapters, and an open-weight LoRA scale-up path.

**60-second project page:** open `index.html` (or `portfolio/index.html`). It links the paper, code, live demo, benchmark, video, dataset card, technical report, and blog post.

**Evidence Layer:** open `evidence/index.html` for the experiment journal, failed hypotheses, decision log, real eval tables, unexpected findings, raw artifacts, and the honest Git-history boundary. Run `make verify-evidence` to verify this layer.

**Failure / safety layer:** `docs/FAILURE_TAXONOMY.md` separates observed failures from evaluator stressors and external gates; `docs/THREAT_MODEL.md` maps stale memory, tool injection, permission confusion, irreversible actions, protected-property drift, and reward hacking; `docs/RESEARCH_OWNERSHIP_MAP.md` connects the project's research choices to code and evidence. Run `make verify-ownership` to verify this layer.

## Headline controlled result

The paper-grade controlled study uses **ContractBench-Implicit**: 1,460 cases over 20 held-out users, with disjoint evaluation phrasing, history-only preference inference cases, held-out domains, ambiguity, paraphrases, and protected-property attacks.

| Method | PersonalBench | ContractBench-Implicit |
|---|---:|---:|
| SFT | **0.9905** | 0.7135 |
| Raw reward optimization | 0.8399 | 0.4817 |
| Constrained repair | 0.9481 | 0.6615 |
| BATPO | 0.9614 | 0.6866 |
| **PCO-Robust** | 0.9448 | **0.7912** |

Across five training seeds, PCO-Robust reaches **0.7910 +/- 0.0008** on ContractBench-Implicit and **0.9449 +/- 0.0005** on PersonalBench. Hierarchical user->case bootstrap gives **+0.1046** over BATPO (95% CI **[+0.0865, +0.1224]**) and **+0.0777** over SFT (**[+0.0632, +0.0917]**), with positive per-user deltas for all 20 held-out users.

The result is deliberately not presented as a universal win: PCO-Robust trades some general PersonalBench utility for substantially better selective personalization. It also remains more paraphrase-sensitive than SFT/BATPO. A consistency regularizer was tested and rejected because it did not improve that weakness.

## Why this is a research project, not a fine-tuning demo

The central object is the **behavioral scope of a known preference effect**, implemented as a typed personalization contract rather than a single personalized reward. The training and evaluation stack uses three matched intervention families:

1. **User-state swaps** — should the response change when the relevant preference changes?
2. **Context swaps** — should a known preference be suppressed when it is not appropriate to apply?
3. **Invariant-pressure prompts** — can personalized pressure change protected properties?

The same repository also retains the earlier negative result: unconstrained learned-reward optimization can raise its training objective while degrading actual personalized behavior. That failure motivated the boundary-aware and contract-aware methods.

## Novelty discipline

The repository deliberately does **not** claim that personalized reward models, causal intervention, preference drift, or context-aware suppression are individually new. Prior work covers each of those ideas. The candidate contribution is the **training-time typed contract formulation** that jointly optimizes `APPLY / SUPPRESS / MUST-NOT-AFFECT` obligations with matched interventions.

See:

- `NOVELTY_AUDIT.md`
- `docs/RELATED_WORK.md`
- `docs/SOTA_EVALUATION_PLAN.md`
- `CLAIMS_AND_LIMITATIONS.md`

## What remains to validate

The reported results come from the controlled PyTorch behavioral model so the entire loop can be reproduced locally. The repository also includes adapters for **BenchPreS, Personalized RewardBench, and AlignX**, plus a Transformers + PEFT/LoRA path for open-weight models.

The next decisive test is a matched-scale open-weight LLM comparison on public benchmarks against current personalized-alignment baselines.

## Dataset and evaluation integrity

Primary controlled benchmark:

- 6,000 unique interactions
- 100 synthetic users
- 3,900 train / 900 validation / 1,200 test
- user-level held-out splits
- 20 unseen test users
- zero exact duplicate records
- zero users crossing splits
- zero exact query strings crossing splits
- 11,700 train-only preference pairs
- paired-user bootstrap uncertainty

## What is implemented

- deterministic synthetic user/profile generation and temporal preference drift
- clean user-held-out dataset construction and audits
- CPU behavioral SFT training
- pairwise preference data and trainable reward model
- raw reward optimization retained as a negative result
- constrained repair and BATPO historical baselines
- **Personalization Contract Optimization (PCO)**
- **PersonalBench-Contract** intervention suite
- failure taxonomy, mining, and hard-case generation
- experiment registry with config/dataset hashing
- SFT and DPO-style data export
- public benchmark normalization/scoring adapters
- optional Transformers + PEFT LoRA backend
- local inference service and browser demo
- human-eval / grader-calibration scaffolding
- Docker, CI, release provenance, SBOM, and secret audit
- paper, benchmark cards, dataset/model cards, and portfolio UI

> **Compatibility note:** the public research name is **Scope of You**. The Python package and CLI keep the legacy `bounded-self` entry points so existing checkpoints, scripts, and reproduction commands remain stable.

## Quick start

```bash
python -m pip install -e . --no-build-isolation
bounded-self --help
make test
make contract
make verify-frontier
```

Run the local checkpoint service:

```bash
bounded-self-serve --checkpoint checkpoints/sft_behavior_v31.pt
```

Run independent benchmark comparison:

```bash
bounded-self-benchmark --help
```

Normalize a supported public benchmark:

```bash
bounded-self-public-bench --help
```

Audit a release:

```bash
bounded-self-audit --root . --output reports/release_audit.json
```

## Open-weight LLM scale-up

Install optional training dependencies:

```bash
pip install -e '.[train]'
```

Export chat-format data:

```bash
make export-llm
```

Then run LoRA SFT on a model you are permitted to access:

```bash
bounded-self llm-sft \
  --model /models/instruct-3b \
  --train-file data/exports/sft_train.jsonl \
  --eval-file data/exports/sft_validation.jsonl \
  --output-dir checkpoints/llm_lora_sft
```

## Frontier-lab review additions

- `docs/OPENAI_ANTHROPIC_RESEARCH_BAR.md` — evidence map against publicly described personalization, post-training, eval, and agent-research expectations.
- `docs/RESEARCH_DECISION_LOG.md` — scientific decisions, failed hypotheses, and why the method changed.
- `docs/AGENTIC_EVAL_DESIGN.md` — stateful task/trial/grader/trajectory evaluation with permission boundaries.
- `reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md` — compact research-lead review path.
- `reports/agentic_contract_suite.json` — executed evaluator sanity check; explicitly not an LLM capability result.
- `reports/agentic_contract_suite_v2.json` — 288-scenario repeated-trial extension with stale-memory/tool-injection stress, recovery, hard safety, `pass@5`, and `all-success@5`.
- `configs/frontier/llm_experiment_matrix.json` — frozen 36-run 7–8B external experiment matrix.
- `docs/EXTERNAL_EXECUTION_HANDOFF.md` — exact GPU/human execution handoff and claim gates.

## Read first

1. `portfolio/index.html` — hiring-facing overview
2. `paper/main.pdf` — research paper
3. `NOVELTY_AUDIT.md` — adversarial novelty audit
4. `BENCHMARK_CONTRACT_CARD.md` — contract benchmark definition
5. `HIRING_MANAGER_WALKTHROUGH.md` — 10-minute technical walkthrough
6. `CLAIMS_AND_LIMITATIONS.md` — exactly what is and is not claimed
7. `docs/PUBLIC_BENCHMARKS.md` — public benchmark adapters
8. `docs/ML_SYSTEMS_DESIGN.md` — system architecture
9. `REPRODUCIBILITY.md` — reproduction instructions

## Scope

The executed results use the local trainable behavioral model. The larger open-weight LLM path is implemented as the next validation tier, and the repository includes a human-evaluation protocol but no collected longitudinal human study. The paper keeps those future experiments separate from the controlled results reported here.

---

**Scope of You** · *Learning Where Personalization Is Allowed to Matter*  
**Aura Yavary**


## Citation provenance

See `docs/CITATION_PROVENANCE_AUDIT.md` for stable identifiers and publication status of the closest recent prior art.
