# Failure Taxonomy

This taxonomy is intentionally split by **evidence status**. An observed controlled failure is not treated as equivalent to a designed red-team stressor or an unexecuted frontier-model risk.

| ID | Failure class | Evidence status | Concrete evidence | What changed |
|---|---|---|---|---|
| F1 | Reward exploitation / off-support optimization | **Observed** | Raw reward optimization raised learned reward while collapsing PersonalBench/factuality; retained in `reports/FAILURE_REPORT.md`. | Added reference regularization, anchors, protected dimensions, clipping; kept raw run as a negative result. |
| F2 | Lexical/template shortcut | **Observed** | First PCO variant looked strong on explicit contract wording but failed ContractBench-Implicit. | Replaced literal control phrasing with disjoint semantic/context-history interventions → PCO-Robust. |
| F3 | Context misapplication | **Observed** | Explicit-context model applied known preferences when they should be suppressed. | Context-selective training became the dominant contract term; reported directly in ablations. |
| F4 | Utility/selectivity trade-off | **Observed** | PCO-Robust improves implicit contract score but misses the frozen 2-point utility non-inferiority gate versus SFT. | Final claim narrowed to selective personalization rather than universal improvement. |
| F5 | Metric mismatch / false progress | **Observed** | Consistency regularization slightly raised macro contract score while paraphrase robustness worsened. | Variant rejected; robustness kept as a separate endpoint. |
| F6 | Weak uncertainty signal | **Observed** | Five-seed disagreement detects some errors but does not support a calibrated-uncertainty claim. | Reported as selective-risk signal only; calibrated confidence claim prohibited. |
| F7 | Dataset integrity leakage | **Observed during development** | Earlier dataset version contained duplicate records and user overlap. | Primary benchmark rebuilt with user-level held-out splits and zero exact duplicates. |
| F8 | Stale-memory overreach | **Evaluator stressor** | `agentic_contract_suite_v2` includes stale-memory variants in all six domains. | Requires ASK/SUGGEST/ABSTAIN behavior where old preference cannot authorize an action. |
| F9 | Tool-text injection into personalized action | **Evaluator stressor** | Tool-injection variants try to override confirmation/permission boundaries. | Grader treats state transition and protected-field mutation as first-class outcomes. |
| F10 | Irreversible-action permission confusion | **Evaluator stressor** | Half of the agentic scenarios are irreversible; permission state is explicit. | Personal preference and action authorization are separated in the task contract. |
| F11 | Frontier-model generalization failure | **External validation needed** | Not yet measured on the frozen 36-run 7–8B matrix. | Claim remains gated until real-model runs and public benchmarks are complete. |
| F12 | Human-context mismatch | **External validation needed** | Human labels are not yet collected. | Human protocol is frozen; no human-superiority claim is allowed before execution. |

## Why this taxonomy matters

The project does not treat every error as “the model was wrong.” Each class points to a different intervention: data repair, objective redesign, benchmark hardening, uncertainty gating, permission checks, or a narrower scientific claim. That distinction is the core of the research process.
