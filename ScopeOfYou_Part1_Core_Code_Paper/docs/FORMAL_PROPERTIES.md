# Formal properties of personalization contracts

The controlled method uses squared penalties as a Lagrangian approximation to contract constraints. Two simple bounds clarify what these penalties can certify and what they cannot.

## Proposition 1 — average protected leakage bound

Let `P` be the protected behavior dimensions and let

`Δ_d(x,u) = b_d(x, I_u(u)) - b_d(x,u)`.

If, for every `d ∈ P`,

`E[Δ_d²] ≤ ε_d²`,

then the average absolute protected leakage satisfies

`Leak_P = E[(1/|P|) Σ_d |Δ_d|] ≤ (1/|P|) Σ_d ε_d`.

**Proof.** For each dimension, Cauchy–Schwarz (equivalently Jensen applied to the square root) gives `E|Δ_d| ≤ sqrt(E[Δ_d²]) ≤ ε_d`. Sum over protected dimensions and divide by `|P|`. ∎

This proposition only bounds the measured behavior coordinates. It does not imply semantic safety of an unrestricted language model.

## Proposition 2 — suppressed-context variation bound

Let `z_d(x,u)` be the preference-sensitive behavior coordinate in a context where the preference should be suppressed, and let `z_d^0(x)` be the neutral target. If

`E[(z_d - z_d^0)²] ≤ ε_s²`,

then `E|z_d-z_d^0| ≤ ε_s`.

The same proof applies. This motivates a squared suppression penalty but does not establish that the chosen neutral target is normatively correct; human validation is required for that assumption.

## Why there is no theorem claiming global alignment

PCO constrains selected evaluator dimensions. It does not prove that all unmeasured behavior remains invariant, and the controlled adapter has a finite behavior vector that makes this limitation especially important. The generative-LLM study must use broader evaluators and human judgments.
