# Claims and Limitations - 1.0.0

## Supported controlled claims
1. The broad personalized-post-training thesis is not novel by itself; the paper's narrower object is **selective personalization scope**.
2. PCO formalizes typed obligations over personalization effects: apply, suppress, and must-not-affect.
3. An explicit-template PCO variant failed to generalize to a disjoint implicit contract suite. This negative result motivated PCO-Robust.
4. Across five training seeds, PCO-Robust reaches **0.7910 +/- 0.0008** on ContractBench-Implicit and **0.9449 +/- 0.0005** on PersonalBench.
5. Relative to BATPO, hierarchical user->case bootstrap gives a ContractBench-Implicit delta of **+0.1046** (95% CI **[+0.0865,+0.1224]**); relative to SFT the delta is **+0.0777** (**[+0.0632,+0.0917]**). Both comparisons are positive for all 20 held-out users.
6. The improvement is not free: PCO-Robust does not maximize general PersonalBench utility and remains more sensitive to paraphrase wording than SFT/BATPO.
7. A paired-paraphrase consistency regularizer was executed and rejected because it slightly reduced paraphrase robustness despite a negligible macro-score increase.

## Unsupported claims
- "first ever" personalization-boundary method;
- public-benchmark state of the art;
- natural-language generation superiority;
- human preference superiority;
- 3B-8B LLM improvement;
- production readiness for consequential decisions.

## Main limitations
The executed evidence uses synthetic users, programmatic behavior targets, and a small behavioral adapter rather than a generative LLM. ContractBench-Implicit reduces template leakage but remains synthetic. No human study or public-benchmark LLM run is presented as executed evidence. The release includes fixed protocols and adapters for those falsification tests rather than substituting simulated results.
