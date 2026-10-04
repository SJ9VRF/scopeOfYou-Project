import argparse, json
from pathlib import Path
from personal_agi_pt.agentic_eval import run_suite

p = argparse.ArgumentParser()
p.add_argument('--output', default='reports/agentic_contract_suite.json')
a = p.parse_args()
r = run_suite()
out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(r, indent=2))
print(json.dumps({"n_tasks": r["n_tasks"], "policies": r["policies"]}, indent=2))
