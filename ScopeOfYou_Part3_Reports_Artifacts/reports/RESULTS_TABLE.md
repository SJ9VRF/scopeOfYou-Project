# Executed Clean-v2 Results

| Model | Personalization | Factuality | Non-sycophancy | Proactivity | PersonalBench mean | Threshold failures |
|---|---:|---:|---:|---:|---:|---:|
| Bootstrap | 0.8460 | 1.0000 | 1.0000 | 1.0000 | 0.9615 | — |
| SFT | 0.9961 | 0.9966 | 0.9968 | 0.9826 | 0.9930 | — |
| Unconstrained reward optimization | 0.9983 | 0.0360 | 0.9981 | 0.4637 | 0.6240 | 850 |
| Constrained post-training | 0.9988 | 0.9990 | 0.9990 | 0.9041 | 0.9752 | 0 |

The benchmark is user-held-out: 80 training users, 10 validation users, and 10 test users. Data-quality audit: 0 exact duplicates and 0 users crossing splits.

The central result is failure detection and repair. The constrained model improves protected factuality/non-sycophancy relative to SFT by small amounts but reduces proactivity matching, leaving its aggregate score below SFT. This tradeoff is reported rather than hidden.
