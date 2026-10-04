# Scope of You — Project Status

**Author: Aura Yavary**  
**Release: 1.1.0**

# Project Status — Release 1.1.0

## Current research thesis
**Personalization Contract Optimization (PCO):** personal AI behavior is governed by intervention-conditioned obligations to apply a preference, suppress it in the current context, or prevent it from affecting protected invariants.

## Why 0.7.0 was not enough
A deeper literature search found direct threats to BATPO's broader novelty: PARPO already decouples generic and personalized rewards with user-specific anchors; AlignX/AlignXplore cover preference reversal/evolution; BenchPreS and RPEval cover context-selective application/suppression; WMG-RL uses counterfactual user simulation; robust reward modeling already uses causal/counterfactual invariance.

## Executed result
- SFT: PersonalBench 0.9905 / Contract 0.8991
- Raw reward: 0.8399 / 0.6802
- Constrained: 0.9481 / 0.8326
- BATPO: 0.9614 / 0.8483
- **PCO: 0.9545 / 0.9239**
- PCO vs BATPO contract delta: **+0.0756**
- paired-user 95% bootstrap CI: **[+0.0652,+0.0862]**
- positive delta: **20/20 held-out users**

## Claim status
- Novelty: **candidate research contribution**, conservatively scoped to the joint three-state interventional contract.
- SOTA: **not established**. Public LLM benchmark gate remains required.

## Project homepage

The release now includes a complete standalone project homepage at `index.html` / `portfolio/index.html`. It is designed for a 60-second hiring-manager pass and links directly to the paper, code, demo, benchmark, video, dataset card, technical report, blog post, and limitations. A dedicated automated audit verifies the required page content and local links.
