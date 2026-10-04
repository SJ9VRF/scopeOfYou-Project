# Scope of You — Final Novelty & SOTA Status

**Aura Yavary**  
*Learning Where Personalization Is Allowed to Matter*

## 30-second answer

**What is new enough to test?**  
Learning the behavioral scope of an already-known user preference as a joint `APPLY / SUPPRESS / MUST-NOT-AFFECT` problem, evaluated with matched user-state, context, protected-pressure, and state-changing action interventions.

**What is not new?**  
Personalized RLHF, user modeling, reward models, causal intervention, context gating, over-personalization, behavioral contracts, causal contracts, contextual integrity, and the broad idea that locally useful adaptation should not apply globally all have prior art.

**What did the project actually discover?**  
The first explicit-template contract optimizer looked good on a co-designed evaluation but failed when the same semantics were expressed implicitly. The project keeps that negative result, redesigns training with disjoint semantic/context-history interventions, and recovers selective-personalization performance across five seeds while exposing a real utility tradeoff.

**Is it SOTA?**  
Not yet by a public LLM benchmark standard. The real-LLM/public-benchmark/human gate is frozen but not executed. Calling the current controlled result “SOTA” would be scientifically misleading.

## Closest 2026 threats explicitly accounted for

- BenchPreS — apply vs suppress evaluation.
- OP-Bench — over-personalization.
- Cautious Context Steering — learned context influence gating.
- NextQuill — causal preference modeling.
- P-GenRM / SynthesizeMe — personalized reward modeling.
- PersonalAgent — lifelong personalization.
- PARPO — personalized agentic RL.
- AgentCIBench / CI-Work — contextual integrity for agents.
- Resist and Update — licensed vs forbidden causal influence.
- Scope Before You Persist — scope-matched persistent adaptation.
- STAGE — controlled multi-preference objective admission.

## Why the project remains interesting

The research object is not “personalization” in general. It is **preference-effect scope**:

> A model can know a preference and still need to decide whether that preference is allowed to affect this behavior, in this context, at this level of authority.

That question becomes more important, not less, as assistants gain persistent memory and state-changing tools.

## Evidence boundary

Executed evidence supports a controlled mechanism claim. It does not establish frontier-LLM generation quality, human preference superiority, production safety, or public-benchmark SOTA. Those claims are blocked by the repository’s external execution gates until the corresponding experiments exist.
