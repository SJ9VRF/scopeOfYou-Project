# Scope of You — 60-second walkthrough

**Aura Yavary** · *Learning Where Personalization Is Allowed to Matter*

### 1. The question
Knowing a user's preference is not enough. The model also needs to know **where that preference is allowed to change behavior**. Scope of You treats preference effects as typed obligations: `APPLY`, `SUPPRESS`, and `MUST-NOT-AFFECT`.

### 2. The part that failed
The first optimizer looked strong on its explicit, co-designed contract test and **failed on the independently worded implicit suite**. The test was kept; the training intervention changed. The failed result remains in the release.

### 3. The strongest executed result
On ContractBench-Implicit (1,460 cases, 20 held-out users), PCO-Robust scores **0.7912** vs **0.6866 BATPO** and **0.7135 SFT**. User→case bootstrap vs BATPO: **+0.1046**, 95% CI **[+0.0865,+0.1224]**, positive on **20/20 users**.

### 4. The catch
This is **not** a universal win. PersonalBench utility falls to **0.9448** from **0.9905 SFT**, and the predeclared **2-point utility non-inferiority gate fails**. The project reports that tradeoff rather than hiding it.

### 5. Why it is more than a benchmark score
The release includes matched counterfactual interventions, a retained negative result, hierarchical statistics, non-inferiority testing, protected-dimension leakage analysis, a stateful agentic permission/recovery evaluator, a frozen two-family 36-run LLM matrix, and a blinded human-eval protocol.

### 6. What is still not proven
No frontier-LLM SOTA, human-preference superiority, calibrated uncertainty, production-agent safety, or real-user longitudinal result is claimed. Those remain explicit external gates.

**If you have 5 more minutes:** read `RESEARCH_LEAD_BRIEF.md`, then `reports/CLAIM_EVIDENCE_MATRIX.md`, then `docs/RESEARCH_DECISION_LOG.md`.

**If you want to audit the numbers:** run `make verify-reviewer` in the lean bundle, or `make verify-frontier` in the full archive.
