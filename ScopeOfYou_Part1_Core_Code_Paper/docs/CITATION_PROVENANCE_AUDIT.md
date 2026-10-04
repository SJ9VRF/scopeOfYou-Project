# Citation Provenance Audit — 26 September 2026

**Project:** Scope of You  
**Author:** Aura Yavary  
**Purpose:** make the closest-prior-art claims independently checkable. This file records stable identifiers for the papers used to bound the novelty claim. A work appears here only when its title and identifier were re-verified against an arXiv, conference-proceedings, ACL Anthology, or official project/author source.

## Closest personalization and selectivity work

| Work | Stable identifier / venue | Why it constrains the claim |
|---|---|---|
| Personalized Language Modeling from Personalized Human Feedback | arXiv:2402.05133 | Personalized RLHF/user-conditioned policy learning is prior art. |
| SynthesizeMe! | ACL 2025, DOI 10.18653/v1/2025.acl-long.397; arXiv:2506.05598 | Persona induction and personalized reward modeling are prior art. |
| NextQuill | ICLR 2026; arXiv:2506.02368 | Causal preference-effect modeling itself is prior art. |
| P-GenRM | ICLR 2026; arXiv:2602.12116 | Personalized generative reward modeling and unseen-user transfer are prior art. |
| AlignX — From 1,000,000 Users to Every User | ACL 2026 Long, DOI 10.18653/v1/2026.acl-long.1391 | Large-scale user-level preference alignment/controllability are prior art. |
| PersonalAgent | Findings of ACL 2026, DOI 10.18653/v1/2026.findings-acl.159; arXiv:2512.15302 | Lifelong profile adaptation and cold-start personalization are prior art. |
| MIPO | arXiv:2603.19294 | Mutual-information preference optimization is prior art. |
| BenchPreS | arXiv:2603.16557; accepted EMNLP 2026 (oral, author/lab listings) | Apply-vs-suppress preference selectivity is explicitly prior art. |
| RPEval | arXiv:2601.16621 | Rational/irrational utilization of personalized memory is prior art. |
| OP-Bench | arXiv:2601.13722 | Over-personalization through irrelevance/repetition/sycophancy is prior art. |
| Personalized RewardBench | arXiv:2604.07343; COLM 2026 project release | Personalized reward-model evaluation is prior art. |
| Personalized Benchmarking | Findings of ACL 2026, DOI 10.18653/v1/2026.findings-acl.31; arXiv:2604.18943 | User-specific model ranking/evaluation is prior art. |
| Cautious Context Steering | arXiv:2608.05813 | Learned token-level control of how strongly user context affects generation is prior art. |
| PARPO — From Correctness to Preference | arXiv:2605.23382 | Personalized agentic RL and reward decoupling are prior art. |
| STAGE | arXiv:2608.16553 | Controlled admission/timing of preference objectives is prior art. |

## Closest causal-boundary and agent-scope work

| Work | Stable identifier / venue | Why it constrains the claim |
|---|---|---|
| Resist and Update | arXiv:2607.12985 | “Causal contract” and licensed-vs-forbidden influence are prior art outside personalization. |
| AgentCIBench / Capable but Careless | arXiv:2606.23189 | Executable contextual-integrity boundaries for computer-use agents are prior art. |
| CI-Work | ACL 2026 Industry, DOI 10.18653/v1/2026.acl-industry.103; arXiv:2604.21308 | Contextual integrity/information-flow control in enterprise agents is prior art. |
| Scope Before You Persist | arXiv:2609.29144 (submitted 24 Sep 2026) | The principle that locally valid adaptation should not propagate globally is explicit prior art for persistent skill memory. |

## What survives this audit

The novelty candidate is **not** “selective personalization,” “causal personalization,” “behavioral contracts,” “context gating,” “personalized agentic RL,” or “scope” as a generic idea.

The defensible object is narrower:

> **Learn the behavioral scope of an already-known user-preference effect as typed `APPLY / SUPPRESS / MUST-NOT-AFFECT` obligations, train those obligations with matched user/context/protected interventions, and extend the same scope logic to state-changing action permission transitions.**

The empirical contribution is also part of the claim: an explicit-template implementation failed on an independently worded implicit suite; the benchmark was retained; the intervention design changed; the repaired method improved the controlled contract metric while preserving the utility tradeoff and unresolved paraphrase sensitivity.

## Verification discipline

- A title/venue claim about a recent work is not treated as verified merely because it appeared in a search snippet.
- For arXiv-only work, the artifact records the arXiv identifier rather than implying peer review.
- For accepted/published work, a proceedings/ACL Anthology/official conference or author/lab record is preferred.
- This audit is about bibliographic provenance, **not** an exhaustive patent/trademark or all-language literature search.
- The release still does not claim public-benchmark SOTA for Scope of You.
