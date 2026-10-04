# Paper Readiness Audit

## Executed evidence

- Controlled PersonalBench v3.1 study with user-held-out train/validation/test splits.
- ContractBench-Implicit: 1,460 cases over 20 held-out users with disjoint evaluation phrasing, history-only preference cases, OOD domains, ambiguity, paraphrase groups, and protected-property attacks.
- Five independent PCO-Robust training seeds.
- Hierarchical user->case paired bootstrap with 5,000 draws.
- Component ablations and loss-scale/selectivity-utility sensitivity study.
- Executed utility non-inferiority analysis: PCO-Robust − SFT = -0.0456; strict 1–3pp margins fail, 5pp margin passes.
- Executed five-seed uncertainty/selective-abstention analysis; error-detection AUROC is ~0.635, so disagreement is treated as diagnostic rather than calibrated confidence.
- Executed counterfactual protected-leakage audit across SFT, raw, constrained, BATPO, and PCO-Robust.
- Explicit-template negative result and subsequent method repair.
- Follow-up paraphrase-consistency regularizer executed and rejected because it did not improve paraphrase robustness.
- Public-benchmark adapters and smoke tests.
- Human-study sampling/randomization/analysis kit, with no human outcome represented as executed.
- Two-family, three-seed LLM paper matrix and LoRA SFT path, with no 7-8B outcome represented as executed.

## Controlled headline

Across five seeds, PCO-Robust reaches 0.7910 +/- 0.0008 on ContractBench-Implicit and 0.9449 +/- 0.0005 on PersonalBench. Hierarchical paired bootstrap gives +0.1046 over BATPO (95% CI [+0.0865,+0.1224]) and +0.0777 over SFT ([+0.0632,+0.0917]), with positive per-user deltas for all 20 held-out users.

## Known weaknesses retained in the paper

PCO-Robust paraphrase robustness is 0.8703 versus 0.9523 for SFT and 0.9531 for BATPO. General PersonalBench utility is also lower than SFT; strict 1–3pp non-inferiority margins fail. Protected leakage is tiny in absolute scale but higher for PCO-Robust than BATPO in the controlled behavior-vector model. A paired-paraphrase consistency penalty slightly increased macro contract score (0.7912 -> 0.7918) but reduced paraphrase robustness (0.8703 -> 0.8689), so it was rejected rather than promoted.

## Evidence still required before an LLM-scale SOTA claim

1. Execute the frozen two-family 7-8B matrix on real generative models.
2. Run official public benchmark splits rather than adapter smoke fixtures.
3. Execute the preregistered human contract-validity and blinded response studies.
4. Report GPU-hours/tokens/model revisions and at least three seeds for trainable headline LLM methods.
5. Satisfy the predeclared utility non-inferiority gate.

Until those are executed, the defensible claim is **controlled evidence for a selective-personalization mechanism**, not public-benchmark state of the art.
