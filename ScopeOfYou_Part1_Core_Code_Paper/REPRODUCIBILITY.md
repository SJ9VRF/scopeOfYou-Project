# Reproducibility

## CPU environment
The core executed stack requires Python and PyTorch. Tests are deterministic at the configured seeds.

## Clean v2 run
```bash
PYTHONPATH=src python scripts/run_v2_clean_lab.py
```

Primary inputs/artifacts:
- `data/samples/lab_v2_clean.jsonl`
- `data/samples/preferences_v2.jsonl`
- `checkpoints/sft_behavior_v2.pt`
- `checkpoints/reward_model_v2.pt`
- `checkpoints/post_trained_v2_raw.pt`
- `checkpoints/post_trained_v2_constrained.pt`
- `reports/full_lab_v2_summary.json`
- `reports/data_quality_v2.json`
- `reports/model_comparison_v2_raw.json`
- `reports/model_comparison_v2_constrained.json`

## Tests and export smoke tests
```bash
make smoke
```

## Optional LLM backend
```bash
pip install -e '.[train]'
make export-llm
bounded-self doctor
```
The LLM backend requires a model checkpoint plus sufficient hardware. This release does not claim that path was trained in the CPU-only execution environment.


## Offline editable install
If the runtime has no network access but local build dependencies are already installed, use:

```bash
python -m pip install -e . --no-build-isolation
```

The ordinary isolated build may attempt to download setuptools/wheel and can therefore fail in an offline sandbox even when the package itself is valid. This release was successfully installed with the offline command above.

## Paper verification
`make paper` regenerates paper figures from executed JSON artifacts and compiles `paper/main.pdf`. The release PDF was rendered to images and visually checked for clipping, overlap, and broken figures.
