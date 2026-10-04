#!/usr/bin/env python3
import argparse,json,hashlib
from pathlib import Path

REQUIRED={"run_id","backbone","method","seed","model_revision","data_hashes","hardware","compute","metrics","artifact_hashes"}

def validate_one(p: Path):
    obj=json.loads(p.read_text())
    missing=sorted(REQUIRED-set(obj))
    errors=[]
    if missing: errors.append(f"missing fields: {missing}")
    c=obj.get("compute",{})
    if "gpu_hours" not in c or "tokens_processed" not in c: errors.append("compute must include gpu_hours and tokens_processed")
    if obj.get("status","completed") == "completed" and not obj.get("metrics"): errors.append("completed run has empty metrics")
    return errors

ap=argparse.ArgumentParser()
ap.add_argument("paths",nargs="+")
a=ap.parse_args()
failed=False
for s in a.paths:
    p=Path(s); errs=validate_one(p)
    print(f"{p}: {'PASS' if not errs else 'FAIL'}")
    for e in errs: print('  -',e)
    failed |= bool(errs)
raise SystemExit(1 if failed else 0)
