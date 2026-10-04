# Benchmark Card - PersonalBench v3.1

## Purpose
A controlled benchmark for testing whether a post-training pipeline preserves personalized control signals while optimizing a learned preference reward.

## Composition
- 6,000 interactions from 100 synthetic users.
- 3,900 train / 900 validation / 1,200 test interactions.
- 65 / 15 / 20 users respectively; users never cross splits.
- 11,700 pairwise preference examples generated from train interactions only.

## Quality gates
The release audit reports: 0 schema-error records, 0 exact duplicate records, 0 exact query strings crossing splits, and 0 users crossing splits.

## Dimensions
- **Personalization:** user-state-dependent control target: concise 0.1, balanced 0.5, detailed 0.9.
- **Factuality:** preservation of correct behavior, including factuality traps.
- **Non-sycophancy:** avoid incorrect agreement.
- **Proactivity:** user preference combined with context; autonomy contexts lower intervention, deadline contexts raise it, ambiguous contexts favor clarification.

## Scenario families
Technical explanation/evaluation, factuality traps, autonomy constraints, deadline pressure, and ambiguous requests. Temporal preference drift changes the current user state during synthetic longitudinal interaction.

## Primary protocol
All headline scores are reported on the 1,200-example test set from 20 unseen users. Uncertainty is estimated with paired bootstrap resampling over users, not individual interactions.

## Known limitations
Synthetic profiles are controlled instruments, not representative human populations. Natural-language quality is not measured by the CPU behavioral backend. Query composition is programmatic. Results should not be generalized to production assistants without human evaluation and an executed LM-scale study.
