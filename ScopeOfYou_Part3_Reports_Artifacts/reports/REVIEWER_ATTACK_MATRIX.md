# Reviewer Attack Matrix

Likely skeptical questions and the evidence needed to answer them.

1. **“The benchmark was designed for the method.”**  
   Response: the first co-designed benchmark produced an inflated result; ContractBench-Implicit was built after that failure with disjoint phrase banks, masked structured state in history-inference cases, OOD domains, and independent wording. The negative result is retained.

2. **“This is still a toy model.”**  
   Correct. The current paper is controlled feasibility evidence. The frozen LLM matrix requires two independent 7–8B families, three seeds, public benchmarks, and external baselines before a general/SOTA claim.

3. **“Why not just SFT?”**  
   SFT has higher generic utility but lower independent selective-contract score. The paper reports a frontier, not dominance.

4. **“You claim no utility cost.”**  
   We do not. PCO-Robust is −0.0456 vs SFT on PersonalBench; 1–3pp non-inferiority margins fail. Only a permissive 5pp margin passes.

5. **“Are confidence/uncertainty claims calibrated?”**  
   No. Five-seed disagreement is an epistemic diagnostic (error-detection AUROC ≈0.635), not a calibrated probability. Ambiguous cases show only ~3% higher mean seed disagreement.

6. **“Protected invariance is trivial/saturated.”**  
   In this backend it is close to ceiling. Ablations show context selectivity drives most of the remaining gain. This is stated rather than presented as a broad safety result.

7. **“PCO leaks into protected dimensions anyway.”**  
   Counterfactual protected leakage is small in absolute magnitude but higher for PCO-Robust than BATPO in the controlled model. The paper reports this; it is an LLM-scale stress target.

8. **“Hyperparameters were tuned on test.”**  
   Main objective weights are fixed for the five headline seeds; diagnostic loss-scale sweeps are labeled diagnostic and not used to redefine the headline method.

9. **“The five seeds are not independent data.”**  
   Seed variability and user/case variability are separated. Headline method comparisons use hierarchical user→case bootstrap; training-seed mean/std is reported separately.

10. **“Contract labels are normative.”**  
    Agreed. The human study separately measures contract-label agreement and blinded response preference. No human consensus is claimed before those labels exist.

11. **“Why equal-weight a macro contract score?”**  
    Main reporting includes every contract state and worst-contract performance; the macro score is not the sole endpoint.

12. **“Could the method memorize phrases?”**  
    ContractBench uses disjoint phrase banks and held-out domains, but paraphrase robustness is still weaker than SFT/BATPO. This unresolved failure is reported.
