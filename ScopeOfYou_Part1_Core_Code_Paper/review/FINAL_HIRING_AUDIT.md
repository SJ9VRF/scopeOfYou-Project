# Scope of You — Final Hiring Audit

**Aura Yavary**  
**Purpose:** assess whether the repository reads like a serious research artifact rather than a polished demo.

## What is unusually strong

### 1. The project contains a falsification, not just a success
The first contract optimizer performed well on an evaluation sharing its explicit intervention language and then failed on an independently worded implicit suite. The project keeps that failure, changes the training distribution, and reruns the harder evaluation.

### 2. The strongest homepage metric now comes from the harder evaluation
The public project page headlines ContractBench-Implicit (PCO-Robust 0.7912 vs BATPO 0.6866) rather than the easier internal contract metric. This prevents the presentation layer from cherry-picking the friendliest score.

### 3. The utility cost is visible
PCO-Robust improves selective personalization but reduces PersonalBench utility versus SFT. The 2-point non-inferiority gate is not met. The result is therefore presented as a frontier/tradeoff, not an all-axis win.

### 4. The ablation is allowed to be asymmetric
Context-selective intervention is the dominant controlled component. Near-ceiling invariant/attack terms do not receive artificial “every module matters” language.

### 5. Agentic evaluation is scoped correctly
The stateful permission/recovery suite is an evaluator stress test. It is not presented as evidence that an LLM agent is safe or capable.

### 6. Expensive evidence is frozen before execution
The external two-family 7-8B matrix, seeds, utility gate, result schema, and human-evaluation protocol are committed before the results exist. This reduces room for post-hoc claim drift.

## Strongest novelty statement that remains defensible

> The candidate contribution is learning the **behavioral scope of a known user-preference effect** as typed `APPLY / SUPPRESS / MUST-NOT-AFFECT` obligations, trained and evaluated with matched user-state, context, protected-behavior, and action-permission interventions.

Do **not** broaden this into claims that selective personalization, context gating, causal intervention, behavioral contracts, contextual integrity, or over-personalization are themselves new; the novelty audit documents direct prior art for each.

## Four likely attacks and the answer

### “This is just selective personalization.”
Selective application/suppression is prior art. The narrower object is preference-*effect scope*, including protected dimensions and permission transitions. Whether that narrower formulation survives LLM-scale comparison remains an explicit experimental question.

### “The benchmark was made for the method.”
That concern was valid for the first evaluation. ContractBench-Implicit was specifically constructed with disjoint phrasing, implicit cues, history-only preference inference, held-out domains, ambiguity, paraphrases, and protected-property attacks. The first method fails it.

### “The model is too small to support a frontier-model claim.”
Correct. The repository labels the result controlled mechanism evidence and blocks a public-benchmark/SOTA claim until the frozen 7-8B and human studies are executed.

### “The project looks over-produced.”
The best evidence against that is not more polish; it is the retained failures, claim/evidence matrix, raw reports/checkpoints, tests, negative regularizer result, and exact external handoff. Review those before the portfolio page.

## What would change the project from strong artifact to strong research result

1. Execute the frozen two-family 7-8B matrix.
2. Run official public personalization/selectivity benchmarks at matched scale.
3. Add blinded human contract-scope and response-appropriateness judgments.
4. Demonstrate that the gain survives the preregistered utility gate.
5. Repeat the failure analysis on generated text, not only the controlled behavior-vector backend.

Until those are complete, the most credible positioning is **strong research artifact with a novel, falsifiable candidate formulation and controlled evidence**, not “SOTA personalization.”

## Hiring signal

The artifact is designed to show research behavior that frontier-model teams publicly ask for: turning ambiguous model behavior into a measurable research agenda, building evaluations that expose failures, iterating on post-training interventions, debugging across the stack, and keeping product/model tradeoffs explicit.
