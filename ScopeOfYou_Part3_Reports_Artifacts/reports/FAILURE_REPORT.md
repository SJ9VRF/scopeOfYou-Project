# Failure Analysis — Clean v2

## Baseline state
The SFT checkpoint reaches PersonalBench 0.9930 on 500 validation interactions from users never observed during training. Factuality is 0.9966 and proactivity matching is 0.9826.

## Failure introduced by unconstrained reward optimization
The learned reward is optimized directly with only a weak drift penalty. The resulting checkpoint increases the learned reward objective but collapses important behavior dimensions:

- PersonalBench: 0.6240
- Factuality: 0.0360
- Proactivity: 0.4637
- Threshold failures: 850
- FACT-01 failures: 500
- PRO-01 failures: 350

This is retained as a negative result rather than discarded.

## Diagnosis
The reward model fits the synthetic preference pairs extremely well, but the optimizer pushes model outputs outside the region represented by those pairs. Pairwise in-distribution accuracy therefore does not imply safe optimization under distribution shift. The optimization target can be exploited.

## Repair
The constrained optimizer adds:

1. stronger reference regularization to the SFT checkpoint,
2. supervised anchor loss on known target behavior,
3. protected treatment of high-priority behavior dimensions,
4. reward-domain clipping to limit extrapolation.

## Repaired result
- PersonalBench: 0.9752
- Personalization: 0.9988
- Factuality: 0.9990
- Non-sycophancy: 0.9990
- Proactivity: 0.9041
- Threshold failures: 0 / 500 validation examples

The repair restores protected behavior but does not beat SFT overall because proactivity matching remains worse. This tradeoff is preserved in the report.

## Dataset lesson
An earlier v1 dataset had 3,201 exact duplicate records and users crossing train/validation. The quality audit caught this, so the primary benchmark was rebuilt as clean v2 with user-level held-out splits and zero exact duplicates. Older v1 outputs remain only for audit history.
