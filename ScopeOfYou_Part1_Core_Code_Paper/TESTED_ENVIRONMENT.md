# Tested environment

The controlled artifact has been verified in the current release environment with:

- Python 3.13.5
- PyTorch 2.10.0+cpu
- pytest 9.0.2
- NumPy 2.3.5
- pandas 2.2.3
- SciPy 1.17.0
- Matplotlib 3.10.8

The package itself declares Python >=3.10. GPU/open-weight LLM dependencies are optional and intentionally separated from the controlled CPU evidence. Exact external-model revisions, tokenizer revisions, hardware, GPU-hours, output hashes, and dataset hashes are required by `external_runs/result.schema.json` before any LLM-scale result can be promoted into the evidence manifest.
