#!/usr/bin/env bash
set -euo pipefail
python -m personal_agi_pt.cli doctor
python -m personal_agi_pt.cli export-sft --source data/samples/lab_v1.jsonl --output data/exports/sft_chat.jsonl
pytest -q
