from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'experiments'/'EXPERIMENT_LEDGER.jsonl'
errors=[]
if not LEDGER.exists():
    raise SystemExit('EXPERIMENT LEDGER VERIFY: FAIL\n - missing ledger')
entries=[json.loads(x) for x in LEDGER.read_text().splitlines() if x.strip()]
ids=[e.get('id') for e in entries]
if len(ids)!=len(set(ids)): errors.append('duplicate experiment id')
if len(entries)<6: errors.append('ledger unexpectedly small')
def check_art(a, eid):
    p=ROOT/a['path']
    if not p.exists(): errors.append(f'{eid}: missing {a["path"]}'); return
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=a['sha256']: errors.append(f'{eid}: hash drift for {a["path"]}')
    if p.stat().st_size!=a['bytes']: errors.append(f'{eid}: byte-size drift for {a["path"]}')
for e in entries:
    for a in e.get('input_artifacts',[]): check_art(a,e['id'])
    for a in e.get('output_artifacts',[]): check_art(a,e['id'])
    if e.get('decision_artifact'): check_art(e['decision_artifact'],e['id'])
    if e['status']=='executed' and not e.get('output_artifacts'):
        errors.append(f'{e["id"]}: executed entry has no output')
    if e['status']=='planned_not_executed' and e.get('output_artifacts'):
        errors.append(f'{e["id"]}: planned gate has outputs and risks looking executed')
neg=[e for e in entries if e['kind']=='negative_result' and e['status']=='executed']
if not neg: errors.append('no preserved executed negative result')
extg=[e for e in entries if e['id']=='frontier_external_llm_matrix']
if len(extg)!=1 or extg[0]['status']!='planned_not_executed': errors.append('external LLM gate not explicitly pending')
if errors:
    print('EXPERIMENT LEDGER VERIFY: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('EXPERIMENT LEDGER VERIFY: PASS')
print(f'entries={len(entries)} executed={sum(e["status"]=="executed" for e in entries)} pending={sum(e["status"]!="executed" for e in entries)}')
