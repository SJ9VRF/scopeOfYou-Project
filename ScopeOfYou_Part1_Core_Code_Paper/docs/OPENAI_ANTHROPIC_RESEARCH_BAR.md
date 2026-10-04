# Frontier Research Bar: OpenAI + Anthropic

This document explains what Scope of You demonstrates today, what it deliberately does not claim, and how the repository maps to the research and engineering bar described publicly by OpenAI and Anthropic.

## The bar

### OpenAI: Personal AGI / Model Experience / North Stars
Public role descriptions emphasize:

- owning a research agenda rather than executing a fixed benchmark;
- personalization and memory grounded in user signals and human data;
- reward models, reinforcement learning, synthetic data, and post-training;
- robust evaluations that expose capability and behavior regressions;
- model behavior spanning factuality, safety, instruction following, personality, interactivity, multilingual behavior, and world interaction;
- research engineering: implement, test, debug, and iterate across the stack.

Primary sources:
- https://openai.com/careers/research-engineer-research-scientist-personal-agi-personalization-san-francisco/
- https://openai.com/careers/research-engineerresearch-scientist-personal-agi-model-experience-san-francisco/
- https://openai.com/careers/research-engineerresearch-scientist-personal-agi-north-stars-san-francisco/
- https://openai.com/careers/research-engineer-research-scientist-personal-agi-personality-and-model-behavior-san-francisco/

### Anthropic: model evaluations, RL, production post-training, agents
Anthropic's public evaluation guidance treats an agent evaluation as a collection of **tasks**, repeated **trials**, independent **graders**, and complete **trajectories/transcripts**. For state-changing agents, end-state verification and permission boundaries matter more than requiring one exact trajectory. Their public roles also span Model Evaluations, Production Model Post-Training, RL Engineering, RL Velocity, Universes, Computer Use, and RL Data Platform.

Primary sources:
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- https://www.anthropic.com/engineering/building-effective-agents
- https://www.anthropic.com/engineering/writing-tools-for-agents
- https://www.anthropic.com/careers/jobs

## Evidence map

| Research capability | Evidence in Scope of You | Status |
|---|---|---|
| Own a research question | typed personalization contracts; failure-driven method revision | Executed |
| Negative-result discipline | explicit-template PCO fails on ContractBench-Implicit; consistency regularizer rejected | Executed |
| Synthetic data | held-out user generation, preference drift, counterfactual interventions | Executed |
| Reward modeling | pairwise reward model + raw reward-optimization failure | Executed |
| Post-training | SFT, preference/reward optimization, constrained repair, PCO-Robust | Executed on controlled backend |
| Robust evals | user-held-out split, independent implicit suite, OOD/paraphrase stress, hierarchical bootstrap | Executed |
| Model-behavior invariants | factuality/non-sycophancy, leakage measurement, must-not-affect contracts | Executed |
| Human-data design | blinded contract-label and response-preference study kit | Protocol frozen; labels not collected |
| Agentic state eval | task/trial/grader/trajectory suite with state and permission graders | Harness executed; not an LLM result |
| Public benchmark integration | BenchPreS, Personalized RewardBench, AlignX adapters | Adapter smoke-tested; official model outcomes pending |
| Frontier LLM training | Transformers + PEFT/LoRA backend, fixed model/seed matrix | External GPU execution required |
| Production/research engineering | tests, configs, checkpoints, service, Docker, CI, provenance, SBOM, audit gates | Executed |

## What a research lead should notice

The strongest signal is not the controlled score itself. It is the research loop:

1. define a behavioral hypothesis;
2. build an eval that can falsify it;
3. discover that the first method overfits explicit contract phrasing;
4. change the training distribution rather than relax the eval;
5. rerun across held-out users and multiple seeds;
6. expose the resulting utility/selectivity tradeoff and residual paraphrase weakness;
7. freeze the next LLM-scale and human-validation gates before seeing their outcomes.

That is the intended research artifact.

## External evidence gates

The following must remain labeled as **pending** until executed:

- two independent 7--8B generative model families;
- official public-benchmark outcomes at matched scale;
- real human preference / contract-scope labels;
- calibrated uncertainty for ambiguous contracts;
- real tool/API execution with production permission systems.

The repository fails its frontier-audit if these are presented as completed results.
