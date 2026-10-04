# NeurIPS checklist preparation notes

The official checklist is supplied by the official conference LaTeX template and must be included verbatim in the submission PDF. These are the prepared answers/evidence mappings for all 16 current checklist questions; they are **not** a substitute for the template checklist.

1. **Claims — Yes.** Abstract/Introduction explicitly limit the result to the executed controlled backend and separate it from the unexecuted LLM/human validation plan.
2. **Limitations — Yes.** Dedicated limitations section covers synthetic users, structured state access, narrow protected dimensions, paraphrase sensitivity, and lack of LLM/human evidence.
3. **Theory, assumptions, proofs — Yes, limited scope.** The paper proves an average protected-leakage bound and the analogous suppression bound via Cauchy--Schwarz. The text explicitly states that these certify only measured behavior coordinates, not global LLM safety.
4. **Experimental reproducibility — Yes for the executed controlled study.** Code, deterministic benchmark construction, exact checkpoints, five seeds, configs, bootstrap, and negative-result artifacts are bundled.
5. **Open access to data/code — Yes for submission supplement, subject to anonymization.** The controlled generated dataset/code/checkpoints are packaged; external public datasets retain their own licenses/terms.
6. **Experimental setting/details — Yes.** User-level splits, training budgets, fixed objective weights, diagnostic-vs-headline budgets, and evaluation construction are described in paper/release artifacts.
7. **Statistical significance — Yes.** Five training seeds are reported; headline selectivity comparisons use hierarchical paired user->case bootstrap with 5,000 draws. Utility non-inferiority uses a paired user bootstrap with 10,000 draws and reports both failed strict margins and the permissive margin that passes.
8. **Compute resources — Yes for executed evidence.** `COMPUTE_DISCLOSURE.md` records CPU type, memory, wall time, CPU time, and peak RSS for a representative headline run. No unexecuted GPU compute is claimed.
9. **Code of Ethics — Author confirmation required at submission.** No human study or private-user data was executed in the current evidence; the author must still personally confirm the current NeurIPS Code of Ethics before submission.
10. **Broader impacts — Yes.** Limitations/broader-implications discuss over-personalization, intrusive use of user information, suppression mistakes, privacy, autonomy, and protected behavior.
11. **Safeguards — N/A for the controlled behavioral adapter.** No high-risk pretrained model is released as a contribution. Future LLM releases must be assessed separately.
12. **Licenses — Yes/verify before submission.** The project includes its license; public benchmarks/models must be used under their original licenses and exact model revisions/licenses must be recorded for the LLM study.
13. **New assets — Yes.** Dataset/benchmark/model cards, construction details, limitations, schemas, and reproducibility artifacts are bundled for the generated controlled assets.
14. **Crowdsourcing/human subjects — N/A for current results.** No human outcome is reported. Full planned instructions/endpoints are in `docs/HUMAN_EVAL_PROTOCOL.md` and `human_eval/` for later approved execution.
15. **IRB/ethics approval — N/A for current results.** No human-subject experiment has been executed. Before running the human protocol, determine and obtain the institutionally required review/approval without breaking submission anonymity.
16. **Declaration of LLM usage — N/A for the core executed method.** The controlled method does not use an LLM as a core experimental component. Writing/editing assistance does not require declaration under the current checklist guidance unless it materially affects the core research method; any future LLM-scale experiment would be described as part of the method/experiments.
