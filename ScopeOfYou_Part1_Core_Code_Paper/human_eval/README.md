# Human evaluation execution kit

This directory contains **study materials, not human results**.

## Phase A - contract validity

Generate the preregistered 500-item stratified sample:

```bash
PYTHONPATH=src python scripts/prepare_human_eval.py
```

Duplicate each item for three independent raters in the annotation platform. Do not expose `model_target_hidden` to raters; it exists only for post-hoc comparison with the controlled benchmark label. Allowed rater labels are `apply`, `suppress`, `must_not_affect`, and `genuinely_ambiguous`.

## Phase B - blinded response comparison

`phase_b_pairs.template.csv` defines the required fields. Populate it only after all candidate model outputs have been generated and frozen. Randomize A/B identity externally and retain the mapping in a restricted analysis file.

## Analysis

`analyze_human_eval.py` provides a dependency-light integrity summary and Wilson interval for the primary pairwise endpoint. The confirmatory analysis should additionally report Fleiss' kappa or Krippendorff's alpha, user/scenario-clustered bootstrap intervals, and the predeclared non-inferiority test described in `docs/HUMAN_EVAL_PROTOCOL.md`.
