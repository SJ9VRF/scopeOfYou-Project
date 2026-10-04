# Contributing

1. Create a focused branch.
2. Add or update tests for behavior changes.
3. Run `make test` and `make reproduce` when touching the core loop.
4. Do not replace negative results with hand-edited metrics.
5. New datasets require provenance and a dataset-card update.
6. New model backends must report dependency and hardware requirements explicitly.
7. Keep benchmark test sets isolated from training and hard-case generation.
