# Novelty Audit — Scope of You

**Audit date:** 26 September 2026  
**Author:** Aura Yavary  
**Project subtitle:** *Learning Where Personalization Is Allowed to Matter*

## Executive verdict

**Novel enough to be an interesting research direction: yes, if framed narrowly.**  
**Already demonstrated SOTA: no.**  
**Safe claim:** a controlled feasibility result for learning the *scope of a known preference effect* across `APPLY / SUPPRESS / MUST-NOT-AFFECT` obligations, with matched counterfactual interventions and explicit agentic permission transitions.

The broad idea “an AI should not always personalize” is no longer novel. By 2026, BenchPreS evaluates context-aware preference application versus suppression; OP-Bench evaluates over-personalization; Cautious Context Steering learns when user context should influence generation; and PersonalAgent, AlignX, P-GenRM, SynthesizeMe, and related work cover preference inference, personalized reward modeling, user adaptation, and long-term personalization.

The generic phrase **behavioral contract** is also prior art in the broader agent ecosystem, and **causal contract** has appeared in contemporaneous alignment work. Therefore this project does **not** claim either phrase as an invention.

The defensible research delta is narrower:

> **Given a user preference that is already known, learn where its behavioral effect is licensed to propagate, where it should be suppressed, and which protected dimensions it must not change — and test those obligations with matched user, context, pressure, and action-permission interventions.**

That is the central contribution of **Scope of You**.

## Closest 2024–2026 neighbors

| Neighbor | What it already establishes | Why it threatens a broad novelty claim | Remaining distinction for Scope of You |
|---|---|---|---|
| **BenchPreS (2026)** | Evaluates whether persistent preferences should be applied or suppressed by context | “Knowing when not to personalize” is prior art | Scope of You makes scope a *training-time typed obligation* and adds protected invariants |
| **OP-Bench (2026)** | Formalizes over-personalization via irrelevance, repetition, sycophancy | Avoiding excessive personalization is prior art | Scope of You targets counterfactual preference-effect propagation, not only output overuse |
| **Cautious Context Steering (2026)** | Learns token-level gating of user context and preserves the base model when context is unhelpful | Learned context gating is directly adjacent | Scope of You tests three obligation types, including protected dimensions and action permissions |
| **NextQuill (ICLR 2026)** | Causal preference modeling / isolation | Causal intervention on preference-bearing signal is prior art | Scope of You asks what downstream behaviors the isolated effect is permitted to change |
| **P-GenRM (ICLR 2026)** | Personalized generative reward modeling and test-time scaling | Personalized reward inference is mature prior art | Scope is the target, not preference inference or user-specific scoring itself |
| **SynthesizeMe (ACL 2025)** | Persona induction and personalized reward modeling from interactions | Inferring user-specific evaluators is prior art | Scope of You assumes the preference is known and constrains effect propagation |
| **PersonalAgent (ACL Findings 2026)** | Lifelong profile adaptation and cold-start personalization | Long-term user adaptation is prior art | Scope of You focuses on when known preferences should *not* affect behavior |
| **PARPO (2026)** | Personalized agentic RL with reward decoupling and user anchors | Generic-vs-personal reward decomposition is adjacent | Scope of You adds typed causal obligations and permission-transition evaluation |
| **AgentCIBench / CI-Work (2026)** | Contextual-integrity failures in agents and enterprise information flow | Context-sensitive boundaries are prior art in privacy/agent settings | Scope of You studies user-preference effects, not primarily information-flow privacy |
| **Resist and Update (2026)** | “Causal contract” separating licensed evidence from forbidden pressure in reporting | Generic causal-contract framing is prior art | Scope of You applies typed scope specifically to personalization across user/context/action interventions |
| **Scope Before You Persist (24 Sep 2026)** | Matching memory retrieval scope to certification scope prevents cross-family interference | The principle “locally valid adaptation should not propagate globally” is now explicit prior art | Scope of You concerns *user preference effect scope* and learns apply/suppress/invariant behavior rather than skill-memory retrieval scope |
| **STAGE (2026)** | Controls when preference objectives enter multi-preference optimization | Selective objective admission is prior art | Scope of You controls where a preference may causally affect behavior, not when an objective joins optimization |

## What is actually new enough to defend

The strongest candidate contribution is the **conjunction** below, not any single item:

1. **Preference-effect scope as the object of learning.** The question is not whether a preference exists, but where it is licensed to influence behavior.
2. **Three typed obligations.** `APPLY`, `SUPPRESS`, and `MUST-NOT-AFFECT` distinguish desirable adaptation, contextually inappropriate adaptation, and protected invariants.
3. **Matched interventions.** User-state swaps test responsiveness; context swaps test suppression; invariant-pressure prompts test leakage into protected dimensions.
4. **Evaluation wording separated from training wording.** The original explicit-template method failed on implicit contexts, and that negative result is retained rather than hidden.
5. **Agentic extension.** Stateful permission transitions test whether personalization expands authority, including stale-memory and tool-injection perturbations, repeated trials, recovery, and hard safety gates.
6. **Claim discipline.** Controlled behavioral-model evidence is explicitly separated from future LLM-scale, public-benchmark, and human-evaluation claims.

## Why this can be interesting to OpenAI / Anthropic

The project is strongest as a **research taste + evals + post-training** artifact rather than as a claim of beating frontier models. It demonstrates:

- a concrete model-behavior question relevant to persistent personalization;
- adversarial evaluation designed to falsify the first implementation;
- retention of a negative result and method redesign after shortcut discovery;
- a measurable selectivity–utility tradeoff rather than a one-number success story;
- counterfactual evaluation and hierarchical uncertainty reporting;
- an agentic extension from response style to permission-sensitive action;
- reproducibility and claim/evidence gates that prevent local controlled results from being marketed as frontier-model evidence.

A strong hiring reviewer should see a falsifiable research program rather than a decorative demo.

## SOTA status — do not blur this

**Current status: NOT an established state-of-the-art result.**

The project has a strong controlled result, but SOTA in personalized LLM alignment requires matched experiments on real generative LLMs and public benchmarks. Until those runs exist, the phrase “state of the art” must not appear as a project-performance claim.

### Minimum SOTA gate

- two open-weight 7–8B-class model families;
- matched SFT / preference-optimization / context-gating / personalized-alignment baselines;
- public evaluation covering at least:
  - BenchPreS;
  - OP-Bench and/or RPEval;
  - PersonalRewardBench / Personalized RewardBench;
  - AlignX/ALOE-Unseen or another dynamic/cold-start benchmark;
  - an agentic task benchmark where permission-sensitive actions can be measured;
- >=3 independent training seeds;
- preregistered utility non-inferiority margin;
- no benchmark-specific tuning on test data;
- human validation of scope labels and response appropriateness;
- contamination and data-overlap checks.

If Scope of You wins that matrix while preserving the preregistered utility margin, a SOTA claim becomes defensible. Before then, it does not.

## Naming audit

### Chosen public name

# **Scope of You**
### *Learning Where Personalization Is Allowed to Matter*

Why this name is better:

- directly expresses the scientific object: the scope of personalization;
- human-centered without sounding like a generic safety framework;
- avoids collision with the increasingly crowded “behavioral contract” naming space;
- avoids the ambiguity of “Bounded Self,” which can be confused with self-refinement / recursive-self-improvement work;
- exact-title web searches performed for this audit did not surface a directly matching AI/LLM research project.

This is a search-based uniqueness check, **not** a trademark or exhaustive global-name clearance.

## One-sentence research pitch

> **Scope of You learns where a known user preference is allowed to matter — when an AI should adapt, when it should suppress personalization, and which behaviors personalization must never be allowed to move.**

## One-sentence honest evidence pitch

> In a controlled held-out-user study, a first contract optimizer failed under implicit contexts; the redesigned PCO-Robust recovered selective-personalization performance across five seeds, while exposing a real utility tradeoff and leaving LLM-scale SOTA as an explicit external gate.


## Citation provenance gate

The exact identifiers and publication status of the closest 2025–2026 works are recorded in `docs/CITATION_PROVENANCE_AUDIT.md`. Recent preprints are labeled as preprints rather than silently promoted to peer-reviewed results.
