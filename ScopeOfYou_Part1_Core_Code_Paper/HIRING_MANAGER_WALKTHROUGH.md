# How to review Scope of You in 10 minutes

## 2-minute version

1. Read `RESEARCH_LEAD_BRIEF.md`.
2. Verify the independent result in `reports/EXECUTED_EVIDENCE_MANIFEST.json`.
3. Inspect `docs/RESEARCH_DECISION_LOG.md` for the failed first hypothesis and method change.
4. Check `reports/FRONTIER_READINESS_MATRIX.md` to see what is still unproven.


## 1. Start with the failure mode
Most personalization systems ask, "What does this user prefer?" The harder question is, "When is that preference allowed to influence behavior?" A model can personalize too much, carry preferences into the wrong context, or let personal agreement pressure degrade truthfulness.

## 2. Check the novelty boundary
Show `NOVELTY_AUDIT.md`. P-GenRM/VRF cover personalized rewards; AlignX/AlignXplore cover preference controllability/evolution; PARPO covers generic-vs-personalized reward decoupling with anchors; BenchPreS/RPEval cover apply-vs-suppress; OP-Bench covers over-personalization. The project therefore focuses on a narrower conjunction: **three-state personalization contracts under causal interventions.**

## 3. Read the PCO objective
Show `src/personal_agi_pt/contract_opt.py`. PCO trains three obligations:
1. apply the preference after a user-state intervention;
2. suppress it after a context intervention;
3. resist personalized pressure on protected invariants.

## 4. Inspect the contract benchmark
Show `BENCHMARK_CONTRACT_CARD.md` and `contract_eval.py`. PersonalBench-Contract reports responsiveness, invariant stability, context suppression, context application, and invariant-attack resistance.

## 5. Look at the result
PCO Contract Score = 0.9239 versus BATPO = 0.8483. Delta +0.0756, 95% paired-user bootstrap CI approximately [+0.0652,+0.0862], positive on 20/20 unseen users.

## 6. Notice the tradeoff
PCO ordinary PersonalBench = 0.9545 versus BATPO = 0.9614 and SFT = 0.9905. The method improves selective causal personalization, not every metric. The project reports the Pareto tradeoff explicitly.

## 7. Trace the research-engineering loop
Show the end-to-end stack: deterministic generation, SFT, preference pairs, reward model, raw reward failure, constrained/BATPO/PCO methods, user-held-out evaluation, bootstrap, failure mining, service, Docker, CI, release audit, and paper build.

## 8. End with the next decisive experiment
Open `docs/SOTA_EVALUATION_PLAN.md`. The next decisive experiment is a matched-scale 3B–8B open-weight LLM comparison against P-GenRM, VRF, AlignX-family methods, PARPO and selectivity baselines on public benchmarks. That experiment is what would determine whether the controlled result survives at realistic model scale.
