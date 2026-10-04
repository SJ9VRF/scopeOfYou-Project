# Dataset Card - PersonalBench v3.1

The primary dataset is `data/samples/personalbench_v31.jsonl`, a controlled synthetic corpus for personalized post-training research.

**Size and split:** 6,000 interactions from 100 users; 3,900 train (65 users), 900 validation (15 users), 1,200 test (20 users). Splits are user-held-out. The audited release has zero exact duplicate records, zero exact query overlap across splits, zero users crossing splits, and zero schema-error records.

**Behavioral variation:** user state includes verbosity, directness, technical depth, proactivity preference, confirmation policy, and correction tolerance. Preference drift changes the current verbosity state. Personalization targets are current-state dependent; proactivity targets are scenario dependent.

**Scenarios:** technical assistance, factuality traps, autonomy constraints, deadline pressure, and ambiguous requests. Queries are composed from natural task/context/constraint/purpose combinations without embedding user IDs or split labels.

**Preference data:** 11,700 pairwise preferences are generated from train interactions only. They contain personalized concise/balanced/detailed candidates plus generic, sycophantic, and over-proactive alternatives.

**Intended use:** controlled algorithm/eval debugging. **Not intended as evidence about real-user preference distributions, demographics, or production deployment.**
