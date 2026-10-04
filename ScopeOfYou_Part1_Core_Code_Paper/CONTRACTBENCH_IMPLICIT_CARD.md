# ContractBench-Implicit

ContractBench-Implicit is an evaluation-only stress suite for **where personalization is allowed to act**. It was added after the original explicit contract suite proved too close to the training interventions.

## What it tests

The suite contains matched cases for four contract states:

- **Apply** — a preference should affect the response.
- **Suppress** — a real preference is not decision-relevant in the current context.
- **Uncertain** — the context is ambiguous enough that aggressive personalization should be attenuated.
- **Must-not-affect** — personalized pressure must not move protected behavior such as factuality or non-sycophancy.

It also contains a history-inference condition: verbosity is removed from the explicit user state and expressed only through natural-language interaction history.

## Independence from training prompts

Training and evaluation use disjoint phrasing banks. Evaluation contexts describe user intent indirectly (for example, exploring options versus actively implementing a decision) rather than issuing literal control instructions such as “do not suggest next steps.”

## Coverage

The exported suite spans multiple domains, includes in-distribution and held-out domain groups, matched paraphrase groups, ambiguity cases, and protected-property attacks. The current controlled release uses 20 held-out synthetic users.

## Metrics

The primary metric is macro contract score. We additionally report:

- score by contract state;
- worst-contract score;
- in-domain and held-out-domain scores;
- paraphrase robustness;
- hierarchical paired bootstrap over users and cases.

## Important limitation

This is still a controlled synthetic benchmark. It does not replace public-benchmark or human evaluation. Its purpose is to prevent the method from being evaluated only on interventions that share wording with its own training objective.
