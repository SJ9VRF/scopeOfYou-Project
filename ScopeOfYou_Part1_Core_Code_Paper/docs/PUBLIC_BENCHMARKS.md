# Public Benchmark Integration

Release 1.1.0 adds executable adapters for three public personalization benchmark families. The adapters do **not** bundle third-party benchmark data; users must obtain each dataset under its original license and terms.

## BenchPreS

Purpose: context-aware preference application vs suppression. The public dataset exposes `prompt`, `preference_attribute`, and `preference_label`, where `True` means the preference should be applied and `False` means it should be suppressed in the current communicative context.

Normalize:

```bash
bounded-self-public-bench normalize \
  --benchmark benchpres \
  --input /path/to/benchpres.jsonl \
  --output reports/benchpres.normalized.jsonl
```

Score a contract-decision file:

```bash
bounded-self-public-bench score-selectivity \
  --gold reports/benchpres.normalized.jsonl \
  --predictions reports/benchpres.predictions.jsonl \
  --output reports/benchpres.metrics.json
```

Predictions use:

```json
{"id":"example-id","decisions":["apply","suppress","suppress"]}
```

Metrics match the benchmark semantics: Appropriate Application Rate (AAR), Misapplication Rate (MR), and an additional balanced selectivity score `(AAR + 1 - MR)/2` for internal comparison.

## Personalized RewardBench

Purpose: pairwise personalized reward-model evaluation with user history. The adapter preserves `question`, `profile`, `chosen`, and `rejected`. `rubric_aspects` and `narrative` are stored only as offline metadata and are explicitly marked as no-leak fields so they are not passed to the model as user context.

```bash
bounded-self-public-bench normalize \
  --benchmark personalized-rewardbench \
  --input /path/to/rewardbench.jsonl \
  --output reports/rewardbench.normalized.jsonl
```

This adapter supports the SOTA evaluation matrix but does not pretend that pairwise personalized preference is identical to a three-state personalization contract.

## AlignX

Purpose: large-scale user-level alignment with a 90-dimensional preference direction and multiple persona evidence channels.

```bash
bounded-self-public-bench normalize \
  --benchmark alignx \
  --input /path/to/alignx.jsonl \
  --output reports/alignx.normalized.jsonl
```

The adapter preserves the preference vector, demographic/persona text, user-generated content, and pairwise feedback in a common schema.

## Important scope distinction

Public adapters are infrastructure, **not public benchmark results**. Release 1.1.0 does not claim PCO scores on these datasets because this runtime did not execute the official LLM baselines or public test suites. The purpose of the adapters is to remove bespoke data plumbing from the next GPU experiment and make the public SOTA gate concrete and auditable.
