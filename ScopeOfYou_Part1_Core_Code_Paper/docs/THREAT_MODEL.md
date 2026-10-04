# Threat Model — Personalization Scope and Agentic Permission

## System boundary

Scope of You studies a specific failure surface: a model **knows something about the user** and must decide where that information is allowed to affect behavior. The threat is not only malicious input; it also includes benign but stale, irrelevant, or over-generalized personalization.

## Assets to protect

1. **Factuality** — preferences must not rewrite facts.
2. **Non-sycophancy** — agreement style must not become truth distortion.
3. **User autonomy** — remembered preferences are not standing permission for consequential actions.
4. **Privacy/minimization** — irrelevant personal information should not leak into unrelated tasks.
5. **Instruction hierarchy** — user profile/context must not override higher-priority constraints.
6. **Task completeness** — suppressing personalization should not make the assistant unusably passive.
7. **State integrity** — protected external state must not mutate without the required permission.

## Adversary / failure sources

| Source | Example | Current coverage | Evidence status |
|---|---|---|---|
| Stale memory | old preference conflicts with present intent | 96 agentic stress scenarios | evaluator coverage only |
| Tool injection | tool text says “ignore confirmation and execute” | 96 agentic stress scenarios | evaluator coverage only |
| Preference over-generalization | concise-style preference changes an unrelated factual decision | ContractBench-Implicit suppression/invariant cases | executed controlled evidence |
| Sycophantic pressure | user preference requests a false or agreeable answer | protected-property attacks | executed controlled evidence |
| Ambiguous intent | model infers action authorization from style/history | 144 high-ambiguity agentic scenarios | evaluator coverage only |
| Irreversible action | send/delete/book/commit based on personalization alone | 144 irreversible agentic scenarios | evaluator coverage only |
| Reward hacking | optimizer exploits reward model outside pairwise support | retained negative run | executed controlled evidence |
| Dataset leakage | same user/query leaks across train and test | dataset audit | observed and repaired |

## Security claims deliberately not made

- This is **not** a production penetration test.
- The agentic suite does **not** demonstrate that a frontier model is secure against prompt injection.
- No claim is made about privacy guarantees, cryptographic isolation, or adversarial robustness in deployed systems.
- The current red-team matrix validates evaluator/task coverage; real-model attack success rates remain an external execution gate.

## Escalation rule

If a scenario combines high stakes, ambiguity, irreversible state mutation, or stale/conflicting memory, the safe default is to move from implicit personalization toward **ASK / SUGGEST / ABSTAIN** rather than silent execution.
