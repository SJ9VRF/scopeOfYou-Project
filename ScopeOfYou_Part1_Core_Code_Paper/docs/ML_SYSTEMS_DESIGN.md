# ML Systems Design

## Objective
Build a closed-loop post-training system where user feedback becomes training data, candidate models are evaluated across multiple behavior dimensions, regressions are blocked, and observed failures generate the next curriculum.

## Data plane
1. Interaction records are immutable, schema-validated events.
2. Derived datasets are versioned artifacts, not in-place mutations.
3. Provenance is preserved: human, synthetic, adversarial, or failure-mined.
4. Train/validation boundaries are assigned before augmentation to avoid leakage.
5. Exporters transform internal records into model-specific formats.

## Training plane
The CPU reference backend is a small PyTorch behavioral model that exercises the full machinery without downloads. The scalable backend uses Transformers + PEFT LoRA and consumes chat-format JSONL. Both backends emit checkpoints and metrics into explicit run directories.

## Evaluation plane
Candidate checkpoints are compared on personalization, factuality, non-sycophancy, and proactivity. Each metric is treated independently before aggregation. Regression gates protect invariant dimensions instead of allowing one scalar reward to mask severe degradation.

## Failure loop
Evaluation examples below thresholds are serialized with failure codes. Failure clusters are converted into hard-case candidates. The next training iteration mixes hard cases with anchor data so optimization targets observed weaknesses while retaining previously-good behavior.

## Reproducibility
Every run should record: git commit, dataset hash, config hash, seed, runtime, hardware, checkpoint path, and metrics. `experiment_registry.py` provides a minimal local registry that can later be mirrored into W&B/MLflow without changing experiment semantics.

## Scaling path
- 1–4B: single GPU, LoRA, short experiments and CI smoke tests.
- 7–14B: multi-GPU LoRA/QLoRA, distributed evaluation, long-horizon rollouts.
- Larger scale: external scheduler, sharded datasets, asynchronous rollout workers, central artifact store, and isolated grader workers.

## Reliability requirements
- deterministic seeds where supported
- resumable checkpoints
- immutable dataset versions
- regression gates before promotion
- explicit failure artifacts
- no hidden human edits between reported runs
- cost and wall-clock capture for every expensive experiment

## Promotion policy
A candidate may be promoted only if protected metrics stay within configured regression tolerances and the target behavior improves or an explicit research exception is documented. Aggregate score alone is insufficient.
