# Unexpected Findings

Results that changed interpretation, method choice, or reporting.

## U-01 — More optimization was not automatically better
Direct reward optimization increased its own objective while destroying factuality. Constraining the optimizer mattered more than making it more aggressive.

## U-02 — The first win disappeared under independent wording
Explicit-template PCO looked successful until ContractBench-Implicit removed lexical cues. The benchmark invalidated the method and forced redesign.

## U-03 — The ablation did not support every component
The context-selective term drove the largest effect; some invariant/attack removals were nearly redundant in this controlled backend.

## U-04 — A higher macro score could still be the wrong model
The paraphrase-consistency variant slightly improved aggregate contract score but worsened paraphrase robustness, so it was rejected.

## U-05 — Better selectivity was not free
PCO-Robust improves implicit scope control but loses ~4.56 pp of PersonalBench utility against SFT; the frozen 2-pp non-inferiority gate fails.

## U-06 — Uncertainty was weaker than expected
Five-seed disagreement had AUROC ~0.635 and only 1.032× disagreement on ambiguous vs determinate cases.

## U-07 — Contract score and protected leakage are different
PCO-Robust has strong contract score but higher direct protected leakage than BATPO; both endpoints remain separate.

## U-08 — Reliability metrics disagree
For noisy risk-aware agentic behavior, pass@5 is 0.840 while all-success@5 is 0.566. Capability-at-least-once and reliability are not the same.
