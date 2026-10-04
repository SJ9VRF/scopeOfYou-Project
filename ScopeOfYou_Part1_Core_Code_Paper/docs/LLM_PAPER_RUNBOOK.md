# LLM Paper Runbook

The controlled CPU study establishes the mechanism. A Main-Track-strength claim requires token-generating LLM experiments. This runbook fixes the experiment matrix before those runs are launched.

## Backbone families

Use two independent 7–8B instruction-tuned families:

- Qwen/Qwen3-8B
- meta-llama/Meta-Llama-3.1-8B-Instruct

A smaller model may be used for debugging, but it must not replace the two-family headline comparison.

## Methods

For each backbone, run at least:

1. base instruct model;
2. SFT personalization;
3. prompt/profile-conditioned personalization;
4. DPO on personalized preference pairs;
5. strongest reproducible personalized-alignment baseline available (for example P-RLHF/MIPO/NextQuill-compatible setup depending released code and data);
6. PCO-Robust.

Run at least three seeds for trainable headline methods. All method selection and hyperparameter tuning must use validation data only.

## Evaluation sets

Required:

- ContractBench-Implicit;
- BenchPreS;
- Personalized RewardBench when evaluating the reward-model component;
- at least one dynamic/cold-start personalization benchmark (AlignX/ALOE-Unseen or comparable released data);
- OP-Bench or RPEval for over-/irrational-personalization stress testing.

## Headline endpoints

Report all of the following, not a single composite score:

- apply accuracy / preference fit;
- suppress accuracy or misapplication rate;
- protected-invariant preservation;
- general utility / task quality;
- worst-contract performance;
- out-of-domain contract score;
- human context-appropriateness preference.

## Non-inferiority gate

A claim that PCO improves selectivity *without materially degrading utility* is allowed only if the predeclared utility non-inferiority criterion is met. Do not infer this from overlapping error bars.

## Reproducibility

Record exact model revision, tokenizer revision, package lock, hardware, number of GPUs, GPU-hours, tokens processed, decoding configuration, seeds, data hashes, and checkpoint hashes. Produce model outputs before running final human evaluation to avoid selection on human outcomes.

## Current execution status

This repository contains the LoRA/SFT backend, benchmark adapters, normalized result schemas, and exact evaluation plan. The current runtime does not provide the GPU stack/model weights required for the two-family experiment, so no LLM-scale result is represented as executed evidence.
