# External Execution Handoff

This directory is the boundary between executed evidence in this repository and the two remaining external studies: GPU-scale generative-model experiments and human evaluation.

## GPU study

The experiment matrix is frozen in `configs/frontier/llm_experiment_matrix.json`. `python scripts/plan_frontier_runs.py` expands it to 36 planned runs: two 7--8B backbones × six methods × three seeds. A debugging run may be added, but it must not replace a preregistered headline cell.

Every completed run must emit one JSON record matching `external_runs/result.schema.json`, including exact model/tokenizer revisions, dataset hashes, hardware, GPU-hours, tokens processed, metrics, and output/checkpoint hashes. `scripts/validate_external_results.py` rejects incomplete records.

### Test discipline
- Hyperparameters are selected on validation data only.
- Test data is opened once after method/config freeze.
- Utility-preservation claims require the predeclared 2 percentage-point non-inferiority margin.
- Results are aggregated over all three seeds; single-seed wins are not headline evidence.
- Failed/aborted runs remain in the run ledger.

## Human study

The human study files live under `human_eval/`. The study is intentionally not marked executed. Before collection:

1. freeze model outputs;
2. randomize/blind method identity;
3. assign at least three independent raters to contract-label validation items;
4. retain disagreement rather than majority-filtering it away;
5. report inter-rater agreement and confidence;
6. analyze pairwise response preference at the user/scenario cluster level;
7. separately report over-personalization / intrusiveness judgments.

## What may change after external execution
Only result tables, statistical summaries, and claims directly supported by the frozen protocols may change. Benchmark definitions, primary endpoints, non-inferiority margin, and seed matrix should not be retrofitted to observed test outcomes.
