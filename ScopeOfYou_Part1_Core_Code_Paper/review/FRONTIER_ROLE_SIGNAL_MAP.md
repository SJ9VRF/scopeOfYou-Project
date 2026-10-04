# Frontier Role Signal Map

**Purpose:** hiring-facing navigation only. This file does not change the scientific claims of the project.

Checked against public role descriptions on **25 September 2026**.

## OpenAI

Public Personal AGI / post-training roles emphasize owning a research agenda, personalization and memory, user signals and human data, synthetic data, reward modeling, reinforcement learning, robust evaluations, model-behavior judgment, debugging, and turning qualitative product problems into training interventions.

Project evidence:

- research agenda: typed preference-effect scope and explicit external validation gates;
- synthetic data: user-state/history/context counterfactual construction;
- reward modeling + post-training: SFT, learned reward, constrained repair, PCO-Robust;
- robust evals: held-out users, phrase-disjoint implicit benchmark, OOD/paraphrase stress, bootstrap, non-inferiority;
- model-behavior judgment: explicit APPLY/SUPPRESS/MUST-NOT-AFFECT distinctions;
- debugging/research iteration: first PCO method fails the independent implicit suite; training distribution is redesigned rather than the eval weakened;
- product/agent direction: action-permission and recovery evals without claiming production safety.

Primary public role sources:
- https://openai.com/careers/research-engineer-research-scientist-personal-agi-personalization-san-francisco/
- https://openai.com/careers/research-engineerresearch-scientist-personal-agi-model-experience-san-francisco/
- https://openai.com/careers/research-engineer-research-scientist-personal-agi-personality-and-model-behavior-san-francisco/
- https://openai.com/careers/agent-post-training-artifacts-research-san-francisco/

## Anthropic

Anthropic's current AI Research & Engineering listings include Model Evaluations, Computer Use, Production Model Post-Training, RL Engineering, RL Velocity, and related agent/environment roles, including New York City availability for several of them. Its public agent-evaluation guidance emphasizes tasks, repeated trials, graders, trajectories, and end-state verification.

Project evidence:

- model evaluations: failure-oriented independent benchmark, repeated-trial reliability, hard safety gates;
- post-training: train/eval loop with negative-result retention and explicit intervention redesign;
- computer-use/agent relevance: state-changing action contracts, permission acquisition, stale-memory conflict, untrusted tool-text perturbations;
- research engineering: testable package, configs/checkpoints, CLI/service, CI, provenance and external handoff;
- evaluation integrity: evaluator sanity checks are explicitly separated from model-capability evidence.

Primary public sources:
- https://www.anthropic.com/careers/jobs
- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## What this artifact should signal

The intended signal is not "I implemented many components." It is:

> I can take an ambiguous model-behavior problem, make it falsifiable, build an eval that breaks my first idea, revise the training intervention, quantify the tradeoff, keep the negative result, and leave the next expensive experiment frozen before seeing its answer.
