# Model Card - Executed Behavioral Backends

The empirical results in this repository use small PyTorch behavioral networks so the full post-training loop is executable on CPU. They predict behavioral control signals; they are not natural-language LMs.

## Primary checkpoints
- `sft_behavior_v31.pt`: supervised baseline.
- `reward_model_v31.pt`: pairwise reward model trained on 11,700 train-only preferences.
- `post_trained_v31_raw.pt`: unconstrained reward-guided checkpoint; retained as a negative result.
- `post_trained_v31_constrained.pt`: constrained repair checkpoint.

## Held-out result
SFT PersonalBench = 0.9905; raw reward optimization = 0.8399; constrained repair = 0.9481 on 1,200 interactions from 20 unseen users. Raw optimization creates 1,172 threshold failures; repair reduces this to 79.

## Interpretation
The constrained model is **not** promoted as better than SFT. It demonstrates repair of reward-induced regression. The repository includes a separate Transformers + PEFT LoRA implementation for scale-up, but no LM-scale empirical result is claimed without execution.
