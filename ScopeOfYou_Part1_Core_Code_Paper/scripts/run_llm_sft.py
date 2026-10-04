from __future__ import annotations
import argparse
import json
from pathlib import Path
from personal_agi_pt.llm_backend import LLMTrainConfig, train_lora_sft

p = argparse.ArgumentParser()
p.add_argument('--config', required=True)
a = p.parse_args()
cfg = LLMTrainConfig(**json.loads(Path(a.config).read_text()))
print(json.dumps(train_lora_sft(cfg), indent=2, default=str))
