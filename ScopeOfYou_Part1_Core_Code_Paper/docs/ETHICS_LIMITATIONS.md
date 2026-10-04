# Ethics and Limitations

The synthetic benchmark is intentionally controlled and does not establish real-world user benefit. Synthetic users may encode the assumptions of their generator. A model can also optimize benchmark structure rather than learn robust personalization.

The current executable CPU backend predicts behavioral targets rather than natural-language responses. It validates the post-training machinery but is not evidence that the same gains transfer to a frontier language model. Open-weight LoRA support is provided as a scale-up path, and any future LLM results must be reported separately.

Personalization can create risks including over-inference, stale beliefs, privacy leakage, sycophancy, reduced viewpoint diversity, and inappropriate autonomy. The project therefore treats factuality, non-sycophancy, and autonomy as protected dimensions instead of optimizing user satisfaction alone.

Human preference labels are not objective truth. Disagreement should be measured and preserved when it reflects legitimate preference heterogeneity. Grader models should be calibrated against independent human labels before being used as primary evidence.
