# Frontier Research Readiness Matrix

| Evidence layer | What exists | Gate before stronger claim |
|---|---|---|
| Research question | Typed personalization contracts + scope control | None; executed framing |
| Controlled mechanism | Five-seed PCO-Robust study, negative results, ablations, hierarchical statistics | Do not extrapolate to generative quality |
| Independent evaluation | ContractBench-Implicit with OOD/paraphrase/history stress | Add human validity + public-benchmark LLM outcomes |
| Reward/post-training | SFT, reward model, raw optimization failure, constrained repair, PCO-Robust | Repeat on token-generating 7–8B models |
| Agentic behavior | 288-scenario task/trial/grader/trajectory harness with repeated trials and hard gates | Replace reference policies with real model/tool trajectories |
| Public benchmarks | BenchPreS/Personalized RewardBench/AlignX adapters | Execute official splits at matched scale |
| Human data | Frozen 500-item labeling/pairwise protocol | Collect independent labels; report disagreement and clustered statistics |
| Uncertainty | Five-seed disagreement diagnostic | Calibrate against human ambiguity before calling it confidence |
| Utility preservation | Controlled non-inferiority analysis | Meet predeclared 2pp LLM-scale margin before “no utility cost” claim |
| Production evidence | Docker/CI/service/audit/SBOM | Real external-tool permission system remains out of scope |
| Reproducibility | Checkpoints, data hashes, configs, run plans, result schema, audits | External runs must populate frozen ledger without changing endpoints |

## Claim ceiling today
The strongest defensible statement is: **the controlled study provides evidence that typed, context-selective personalization can improve contract adherence under a deliberately independent stress suite, while exposing a measurable utility and paraphrase-robustness tradeoff.**

It is not yet evidence of frontier-LLM SOTA, human preference superiority, calibrated uncertainty, or production-agent safety.
