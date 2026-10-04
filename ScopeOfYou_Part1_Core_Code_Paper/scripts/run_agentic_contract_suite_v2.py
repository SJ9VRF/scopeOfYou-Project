#!/usr/bin/env python3
import json
from pathlib import Path
from personal_agi_pt.agentic_eval_v2 import run_suite

out = Path("reports/agentic_contract_suite_v2.json")
out.parent.mkdir(parents=True, exist_ok=True)
result = run_suite(n_trials_per_task=5)
out.write_text(json.dumps(result, indent=2), encoding="utf-8")
summary = {
    "benchmark": result["benchmark"],
    "status": result["status"],
    "n_scenarios": result["n_scenarios"],
    "trials_per_scenario": result["trials_per_scenario"],
    "policies": result["policies"],
}
Path("reports/agentic_contract_suite_v2_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
