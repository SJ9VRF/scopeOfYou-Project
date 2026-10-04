#!/usr/bin/env python3
import json, hashlib
from pathlib import Path
m = json.loads(Path("configs/frontier/llm_experiment_matrix.json").read_text())
runs=[]
for b in m["backbones"]:
  for method in m["methods"]:
    for seed in m["seeds"]:
      key=f'{b["id"]}|{method}|{seed}'
      rid=hashlib.sha256(key.encode()).hexdigest()[:12]
      runs.append({"run_id":rid,"backbone":b["id"],"method":method,"seed":seed,"status":"planned"})
out={"status":"plan only; contains no results","n_runs":len(runs),"runs":runs}
Path("external_runs/run_plan.json").write_text(json.dumps(out,indent=2))
print(json.dumps({"n_runs":len(runs),"backbones":len(m["backbones"]),"methods":len(m["methods"]),"seeds":len(m["seeds"])},indent=2))
