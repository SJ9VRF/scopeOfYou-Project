from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.contractbench import build_contractbench
recs=[r for r in load_jsonl(ROOT/'data/samples/personalbench_v31.jsonl') if r.split=='test']
cases=build_contractbench(recs,811)
out=ROOT/'data/contractbench_implicit.jsonl'
with out.open('w',encoding='utf-8') as f:
    for c in cases: f.write(json.dumps(c.to_dict(),ensure_ascii=False,default=str)+'\n')
print(json.dumps({'examples':len(cases),'users':len({c.user_id for c in cases}),'output':str(out)},indent=2))
