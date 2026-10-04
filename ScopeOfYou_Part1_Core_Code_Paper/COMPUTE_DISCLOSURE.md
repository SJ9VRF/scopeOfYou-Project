# Controlled-study compute disclosure

A representative headline PCO-Robust training run was timed with the frozen precomputed intervention tensor cache and the same 180-step / batch-512 budget used by the five headline seeds.

- CPU: AMD EPYC 7763; 5 logical CPUs available to the runtime.
- System memory available to the runtime: 5.8 GiB.
- Accelerator: none used for the controlled study.
- Representative wall time: **7.49 s**.
- User CPU time: **16.67 s**; system CPU time: **0.81 s**.
- Peak resident memory: **345,880 KiB** (~338 MiB).
- Five headline seeds therefore require roughly 37.5 s of model-optimization wall time on this runtime when the cached training tensors are available; preprocessing, evaluation, ablations, failed experiments, and artifact generation are additional and are not folded into that estimate.

This disclosure describes only the executed controlled backend. The planned 7-8B LLM study has not been executed and therefore has no GPU-hour claim. Its runbook requires reporting GPU model/count, GPU-hours, tokens processed, exact model/tokenizer revisions, and decoding configuration for every reported LLM experiment.
