# Related Work and Differentiation — 26 September 2026

This document is intentionally adversarial. If another work already establishes an idea, Scope of You does not claim it as new.

## Closest literature

| Work | Year / venue | Already established | Scope of You distinction |
|---|---|---|---|
| Personalized-RLHF | 2024 | User-conditioned preference optimization | Preference-effect scope rather than personalized RLHF itself |
| SynthesizeMe | ACL 2025 | Persona induction and personalized reward modeling | Assumes a known preference; constrains where it may affect behavior |
| AlignX | 2026 | Large-scale user-level preference alignment and controllability | Scope obligations rather than preference representation scale |
| NextQuill | ICLR 2026 | Causal preference modeling | Downstream license/suppression/protection of a preference effect |
| P-GenRM | ICLR 2026 | Personalized generative reward modeling and unseen-user transfer | Scope control, not personalized RM inference |
| PersonalAgent | ACL Findings 2026 | Lifelong profile adaptation and cold start | Selective application of known preferences |
| BenchPreS | 2026 | Apply-vs-suppress benchmark for persistent preferences | Training-time typed obligations + protected invariants |
| OP-Bench | 2026 | Over-personalization evaluation | Counterfactual scope and must-not-affect obligations |
| Cautious Context Steering | 2026 | Learned token-level gating of user context | Three-state behavior scope + protected dimensions + agentic actions |
| PARPO | 2026 | Personalized agentic RL and reward decoupling | Scope-specific intervention objective and permission boundaries |
| AgentCIBench | 2026 | Contextual-integrity failures in computer-use agents | User-preference effect scope rather than privacy flow alone |
| CI-Work | ACL Industry 2026 | Contextual integrity in enterprise agents | Same distinction: information flow vs preference effect propagation |
| Resist and Update | 2026 | Causal contract for licensed vs forbidden influence on reports | Personalization-specific scope across user/context/action interventions |
| Scope Before You Persist | 24 Sep 2026 | Retrieval scope should match certification scope for persistent skills | Preference-effect scope rather than memory-skill retrieval scope |
| STAGE | 2026 | Controlled admission of multiple preference objectives | Where effects may propagate rather than when objectives enter optimization |

## What cannot be claimed as novel

Scope of You does **not** claim novelty for:

- personalized reward modeling;
- per-user alignment;
- preference inference from history;
- context-aware suppression by itself;
- over-personalization detection;
- causal intervention by itself;
- protected invariants / robustness by themselves;
- behavioral contracts as a generic concept;
- causal contracts as a generic concept;
- dynamic user profiles;
- long-term memory;
- agent permissioning or contextual integrity by itself.

## Candidate contribution

The candidate contribution is a unified training/evaluation object for the **scope of an already-known user preference effect**:

- `APPLY`: the relevant behavior should respond to a user-state intervention;
- `SUPPRESS`: the effect should disappear when context makes it inappropriate;
- `MUST-NOT-AFFECT`: protected behavior should remain invariant even under personalized pressure;
- agentic extension: personalization must not silently expand permission to state-changing actions.

The empirical story matters as much as the ontology: an explicit-template implementation initially overfit to the evaluation format, an independently worded implicit suite exposed the shortcut, and PCO-Robust was redesigned around semantically diverse/context-history interventions.

## Closest conceptual collision: Resist and Update

Resist and Update is especially important because it uses the language of a **causal contract** to distinguish licensed evidence from forbidden pressure. Scope of You therefore does not claim that the general idea of “licensed vs forbidden causal influence” is new. Its narrower delta is the personalization setting: the same learned user preference can be licensed for one mutable behavior, suppressed in another context, and forbidden from changing protected behavior, with an action-level permission extension.

## Newest scope-related collision: Scope Before You Persist

The 24 September 2026 preprint *Scope Before You Persist* shows that a persistent skill edit validated in one task family can harm unrelated families when retrieved globally; scoping retrieval to the certified family removes those harmful deployments in its setting. This is a strong conceptual neighbor because both projects reject global propagation of locally valid adaptation. The distinction is the adapted object and mechanism: that work scopes persistent skill-memory retrieval; Scope of You learns and tests the behavioral scope of user preferences across user/context/protected/action interventions.

## SOTA discipline

No public SOTA claim is permitted until the frozen external matrix is executed on real generative LLMs with matched baselines, public benchmarks, multiple seeds, a preregistered utility gate, and human validation. Controlled results can support a mechanism claim only.
