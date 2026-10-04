# Release 1.1.0 — Scope of You

- Renamed the flagship research system to **Scope of You**.
- Public/project author identity standardized to **Aura Yavary**.
- Canonical subtitle: **Learning Where Personalization Is Allowed to Matter**.
- Canonical paper title: **Scope of You: Learning Where Personalization Is Allowed to Matter**.
- Added `bounded-self` as the primary CLI while retaining existing compatibility entry points.
- Research method remains **Personalization Contract Optimization (PCO)**; the rename changes branding, not empirical claims.

## 0.9.0 — Public benchmark integration

- Added public benchmark adapters for BenchPreS, Personalized RewardBench, and AlignX.
- Added BenchPreS-compatible AAR/MR selectivity scoring and a unified normalized schema.
- Tightened the novelty claim after identifying NextQuill as prior art for causal preference isolation.
- Added explicit SOTA baseline matrix and no-leak handling for Personalized RewardBench rubric/narrative fields.
- Added public-benchmark adapter tests and release-check smoke coverage.

# Release 0.8.0

Release 0.8.0 follows a second, stricter novelty audit. New literature identified direct overlap between BATPO components and PARPO, AlignX/AlignXplore, BenchPreS/RPEval, WMG-RL, and causal reward-modeling work.

## New research contribution
- **Personalization Contract Optimization (PCO)**
- three contract states: apply / suppress / must-not-affect
- user-state, context, and invariant-pressure interventions
- **PersonalBench-Contract**

## Executed result
PCO Contract Score 0.9239 vs BATPO 0.8483 (+0.0756; paired-user 95% CI approx [+0.0652,+0.0862], 20/20 users positive). Ordinary PersonalBench is 0.9545 for PCO vs 0.9614 BATPO, so the release reports a real tradeoff.

## Claim discipline
No public SOTA or priority claim is made. `docs/SOTA_EVALUATION_PLAN.md` defines the required public-benchmark gate.

## Project page artifact

- Added a standalone hiring-manager project page at `index.html` and `portfolio/index.html`.
- Added the full 14-part project narrative: problem, core idea, architecture, contribution, experiments, results, failures, demo, scaling, safety, deep dive, artifacts, citation, and 60-second summary.
- Added a real 60-second overview video, technical blog post, and contract trajectory viewer.
- Added project-page QA that checks required content and local artifact links.
- Project dates remain intentionally absent from public content and metadata.
