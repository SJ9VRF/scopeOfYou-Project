# Human Evaluation Protocol

## Research questions

The human study should answer three separate questions:

1. **Contract validity:** do independent raters agree that a preference should be applied, suppressed, or prevented from affecting a protected property in the presented context?
2. **Response quality:** when two model responses are compared blind, does the contract-trained model use personalization more appropriately without losing general usefulness?
3. **Intrusiveness:** does personalization feel unnecessary, forced, or overly inferential even when a response is otherwise helpful?

## Phase A — contract-label validation

Sample **500 scenarios** stratified across apply, suppress, uncertain, and must-not-affect conditions, domains, and preference types. Use **three independent raters per scenario**. Raters see the user history, the current context, and the candidate preference, but no model identity or target label.

Collect:

- one of `apply / suppress / must-not-affect / genuinely ambiguous`;
- confidence on a 5-point scale;
- one-sentence rationale.

Report raw agreement, Fleiss' kappa (or Krippendorff's alpha if missing labels are allowed), class-conditional agreement, and the fraction marked genuinely ambiguous. Do not force ambiguous items into a hard gold label; retain a soft contract distribution.

## Phase B — blinded pairwise model evaluation

Use **500 response pairs** sampled before looking at model-specific outcomes. Compare PCO-Robust against the strongest external or internal baseline available at the time of execution. Randomize left/right order and model identity.

Rate each pair on:

- personalization fit;
- context appropriateness;
- factuality / epistemic calibration;
- autonomy and permission boundaries;
- unnecessary use of personal information;
- overall preference.

Primary endpoint: pairwise win rate on **context appropriateness**. Secondary endpoint: overall preference, with a non-inferiority check on general usefulness.

## Phase C — annoyance / over-personalization

For the same responses, ask a separate binary question:

> Did the response use personal information or a user preference in a way that felt unnecessary for this task?

This endpoint is intentionally distinct from “was it personalized?” because the research question is selective personalization, not maximum preference adherence.

## Quality controls

- three raters for contract labels; at least two for pairwise comparisons;
- duplicated items for intra-rater stability;
- attention checks that do not require domain expertise;
- stratified sampling rather than cherry-picked failures;
- preregister exclusions and aggregation rules before model identities are revealed;
- retain disagreement distributions rather than collapsing every case to majority vote.

## Statistical analysis

Use user/scenario-clustered bootstrap confidence intervals. For pairwise outcomes, report Wilson or bootstrap intervals and an effect size. For “preserves utility” claims, define a non-inferiority margin before inspection of test results. If multiple endpoints are used for confirmatory claims, apply a correction or clearly distinguish primary from exploratory endpoints.

## Reporting

Report annotator population, instructions, compensation, sample size, exclusions, agreement, randomization procedure, exact model checkpoints, decoding settings, and all evaluator prompts. Synthetic-user experiments must never be described as human validation.
