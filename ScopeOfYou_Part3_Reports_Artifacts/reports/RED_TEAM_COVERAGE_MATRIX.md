# Red-Team Coverage Matrix

> **Scope:** designed evaluator coverage, not a production-security or LLM-capability claim.

The agentic stress suite contains **288 scenarios** across six state-changing domains. Every base task is instantiated as clean, stale-memory, and tool-injection variants.

## Coverage dimensions

| Dimension | Coverage |
|---|---|
| domain | `calendar`: 48, `email`: 48, `files`: 48, `purchase`: 48, `settings`: 48, `travel`: 48 |
| variant | `clean`: 96, `stale_memory`: 96, `tool_injection`: 96 |
| target_action | `ACT`: 18, `ASK`: 198, `SUGGEST`: 72 |
| ambiguity | `high`: 144, `low`: 144 |
| autonomy | `high`: 144, `low`: 144 |
| reversibility | `irreversible`: 144, `reversible`: 144 |
| stakes | `high`: 144, `low`: 144 |

## Domain × perturbation

| Domain | Clean | Stale memory | Tool injection |
|---|---:|---:|---:|
| calendar | 16 | 16 | 16 |
| email | 16 | 16 | 16 |
| files | 16 | 16 | 16 |
| purchase | 16 | 16 | 16 |
| settings | 16 | 16 | 16 |
| travel | 16 | 16 | 16 |

## Threats represented by the suite

- **Stale preference application:** remembered preferences can outlive their validity.
- **Tool-text instruction injection:** external tool content can try to bypass confirmation boundaries.
- **Permission confusion:** personalization can be mistaken for authorization to take an action.
- **Irreversible-action overreach:** a preference may justify a suggestion but not a destructive or committing action.
- **Ambiguity under pressure:** uncertain intent should increase ASK/SUGGEST behavior rather than silent execution.
- **Repeated-trial instability:** a policy that succeeds once can still be unreliable across repeats.

## What this matrix does *not* prove

The suite currently validates evaluator sensitivity using reference policies. It is **not evidence that PCO-Robust, a frontier LLM, or a deployed agent resists these threats**. Real-model red teaming is an external execution gate.
