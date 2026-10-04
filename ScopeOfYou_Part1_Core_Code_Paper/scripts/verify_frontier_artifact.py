from __future__ import annotations
import json, math, re, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(p):
    return json.loads((ROOT/p).read_text())

def near(a,b,tol=5e-4):
    return math.isclose(float(a), float(b), abs_tol=tol, rel_tol=0)

manifest = load('reports/EXECUTED_EVIDENCE_MANIFEST.json')
paper = load('reports/paper_grade_robust_study.json')
unc = load('reports/uncertainty_noninferiority.json')
agent = load('reports/agentic_contract_suite_v2.json')
runplan = load('external_runs/run_plan.json')
readme = (ROOT/'README.md').read_text()

errors=[]
# Hard identity/title checks
if manifest['project'] != 'Scope of You': errors.append('manifest project mismatch')
if manifest['author'] != 'Aura Yavary': errors.append('author mismatch')
if 'Scope of You' not in readme or 'Aura Yavary' not in readme: errors.append('README identity mismatch')

# Source-of-truth metric checks
m = manifest['executed']['contractbench_implicit']
methods = paper.get('methods', paper.get('baselines', {}))
# tolerate both historical report schemas
pco = methods.get('PCO-Robust') or methods.get('pco_robust') or paper.get('pco_robust')
bat = methods.get('BATPO') or methods.get('batpo') or paper.get('batpo')
sft = methods.get('SFT') or methods.get('sft') or paper.get('sft')

def cbi(obj):
    if not isinstance(obj, dict): return None
    for k in ['contractbench_implicit','ContractBench-Implicit','contractbench','cbi']:
        if k in obj: return obj[k]
    return None

for label,obj,target in [('PCO-Robust',pco,m['pco_robust']),('BATPO',bat,m['batpo']),('SFT',sft,m['sft'])]:
    v=cbi(obj)
    if v is not None and not near(v,target): errors.append(f'{label} CBI drift: {v} vs {target}')

if manifest['executed']['tests'].get('expected_minimum') != 54:
    errors.append('test-count manifest drift: expected_minimum must be 51')

# Non-inferiority must remain explicitly failed at 2pp
if manifest['executed']['utility_tradeoff']['two_point_noninferiority'] is not False:
    errors.append('2pp non-inferiority gate must be false')
# Agentic suite scope and cardinality
if manifest['executed']['agentic_evaluator_v2']['scope'].lower().find('not an llm') < 0:
    errors.append('agentic result scope lost its non-LLM disclaimer')
# infer scenario count robustly
if manifest['executed']['agentic_evaluator_v2']['scenarios'] != 288:
    errors.append('agentic scenario count drift')
if manifest['executed']['agentic_evaluator_v2']['trials_per_scenario'] != 5:
    errors.append('agentic trial count drift')
# External plan remains pending/frozen
if runplan.get('n_runs') != 36: errors.append('external run plan no longer 36 runs')
pending=' '.join(manifest['pending_external_gates']).lower()
for phrase in ['generative model','human','public benchmark']:
    if phrase not in pending: errors.append(f'missing pending gate: {phrase}')

# README must expose both independent evidence and utility caveat
for phrase in ['0.7912','0.6866','non-inferiority gate is not met','not claimed']:
    if phrase.lower() not in readme.lower(): errors.append(f'README missing critical phrase: {phrase}')

# Required reviewer entry points
required = [
 'RESEARCH_LEAD_BRIEF.md','FINAL_NOVELTY_AND_SOTA_STATUS.md','NOVELTY_AUDIT.md',
 'reports/EXECUTED_EVIDENCE_MANIFEST.json','reports/CLAIM_EVIDENCE_MATRIX.md',
 'reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md','docs/RESEARCH_DECISION_LOG.md','docs/CITATION_PROVENANCE_AUDIT.md',
 'docs/EXTERNAL_EXECUTION_HANDOFF.md','paper/main.pdf','experiments/EXPERIMENT_LEDGER.jsonl','HIRING_MANAGER_60_SECOND.md'
]
for p in required:
    if not (ROOT/p).exists(): errors.append(f'missing required artifact: {p}')

# Produce a content-addressed digest of the core evidence files
core = ['reports/EXECUTED_EVIDENCE_MANIFEST.json','reports/paper_grade_robust_study.json',
        'reports/uncertainty_noninferiority.json','reports/agentic_contract_suite_v2.json',
        'external_runs/run_plan.json','paper/main.pdf']
h=hashlib.sha256()
for p in core:
    data=(ROOT/p).read_bytes(); h.update(p.encode()); h.update(b'\0'); h.update(data)

if errors:
    print('FRONTIER ARTIFACT VERIFY: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('FRONTIER ARTIFACT VERIFY: PASS')
print('core_evidence_sha256='+h.hexdigest())
print('executed_claims=controlled_behavioral_model_only')
print('external_llm_human_gates=pending')
