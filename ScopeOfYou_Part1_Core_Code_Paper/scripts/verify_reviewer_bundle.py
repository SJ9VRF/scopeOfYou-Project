from __future__ import annotations
import json, hashlib, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_json(rel: str):
    return json.loads((ROOT / rel).read_text())

def fail(errors):
    print('REVIEWER BUNDLE VERIFY: FAIL')
    for e in errors:
        print(' -', e)
    raise SystemExit(1)

errors=[]
required = [
    'REVIEWER_README.md','HIRING_MANAGER_60_SECOND.md','index.html','PROJECT_PAGE_COMPLIANCE.md','BENCHMARK_CONTRACT_CARD.md','DATASET_CARD.md','video/scope-of-you-overview.mp4','demo/live.html','demo/trajectory.html','demo/agentic_eval_v2.html','RESEARCH_LEAD_BRIEF.md','paper/main.pdf','paper/supplement.pdf','paper/main.tex',
    'reports/EXECUTED_EVIDENCE_MANIFEST.json','reports/CLAIM_EVIDENCE_MATRIX.md',
    'reports/paper_grade_robust_study.json','reports/uncertainty_noninferiority.json',
    'reports/agentic_contract_suite_v2.json','docs/RESEARCH_DECISION_LOG.md','docs/CITATION_PROVENANCE_AUDIT.md',
    'docs/EXTERNAL_EXECUTION_HANDOFF.md','external_runs/run_plan.json',
    'external_runs/result.schema.json','data/contractbench_implicit.jsonl',
    'data/agentic_contract_suite_v2.jsonl','src/personal_agi_pt/contract_opt.py',
    'src/personal_agi_pt/agentic_eval_v2.py','experiments/EXPERIMENT_LEDGER.jsonl','scripts/verify_experiment_ledger.py',
    'evidence/index.html','evidence/EXPERIMENT_JOURNAL.md','evidence/FAILED_EXPERIMENTS.md','evidence/DECISION_LOG.md',
    'evidence/REAL_EVAL_TABLES.md','evidence/UNEXPECTED_FINDINGS.md','evidence/FAILURE_TRACE.md','evidence/GIT_HISTORY.md',
    'artifacts/README.md','artifacts/experiment_logs/experiment_log.jsonl',
    'docs/FAILURE_TAXONOMY.md','docs/THREAT_MODEL.md','docs/RESEARCH_OWNERSHIP_MAP.md',
    'reports/RED_TEAM_COVERAGE_MATRIX.md','reports/red_team_coverage.json','scripts/verify_research_ownership.py'
]
for rel in required:
    if not (ROOT/rel).exists():
        errors.append(f'missing required reviewer artifact: {rel}')

if errors: fail(errors)

manifest=load_json('reports/EXECUTED_EVIDENCE_MANIFEST.json')
paper=load_json('reports/paper_grade_robust_study.json')
unc=load_json('reports/uncertainty_noninferiority.json')
agent=load_json('reports/agentic_contract_suite_v2.json')
runplan=load_json('external_runs/run_plan.json')
readme=(ROOT/'REVIEWER_README.md').read_text()
brief=(ROOT/'RESEARCH_LEAD_BRIEF.md').read_text()

if manifest.get('project') != 'Scope of You': errors.append('project identity drift')
if manifest.get('author') != 'Aura Yavary': errors.append('author identity drift')
for txt,name in [(readme,'REVIEWER_README.md'),(brief,'RESEARCH_LEAD_BRIEF.md')]:
    for phrase in ['Scope of You','Aura Yavary','0.7912','0.6866','not proven']:
        if phrase.lower() not in txt.lower(): errors.append(f'{name} missing critical phrase: {phrase}')

m=manifest['executed']['contractbench_implicit']
methods=paper.get('methods', paper.get('baselines', {}))
def pick(name):
    return methods.get(name) or methods.get(name.lower().replace('-','_')) or paper.get(name.lower().replace('-','_'))
def cbi(obj):
    if not isinstance(obj, dict): return None
    for k in ['contractbench_implicit','ContractBench-Implicit','contractbench','cbi']:
        if k in obj: return float(obj[k])
    return None
for label,target in [('PCO-Robust',m['pco_robust']),('BATPO',m['batpo']),('SFT',m['sft'])]:
    val=cbi(pick(label))
    if val is not None and not math.isclose(val,float(target),abs_tol=5e-4,rel_tol=0):
        errors.append(f'{label} ContractBench drift: {val} vs {target}')

if manifest['executed']['tests'].get('expected_minimum') != 54:
    errors.append('test-count manifest drift: expected_minimum must be 54')
if manifest['executed']['utility_tradeoff']['two_point_noninferiority'] is not False:
    errors.append('2pp non-inferiority must remain failed')
if manifest['executed']['agentic_evaluator_v2']['scenarios'] != 288:
    errors.append('agentic scenario count drift')
if manifest['executed']['agentic_evaluator_v2']['trials_per_scenario'] != 5:
    errors.append('agentic trial count drift')
if 'not an llm' not in manifest['executed']['agentic_evaluator_v2']['scope'].lower():
    errors.append('agentic evaluator lost non-LLM scope disclaimer')
if runplan.get('n_runs') != 36:
    errors.append('frozen external run plan is not 36 runs')

pending=' '.join(manifest.get('pending_external_gates',[])).lower()
for phrase in ['generative model','public benchmark','human']:
    if phrase not in pending: errors.append(f'missing external gate: {phrase}')


# Standalone project-page structure + local link integrity.
from html.parser import HTMLParser
page=(ROOT/'index.html').read_text(encoding='utf-8')
for token in ['02 · Why this problem matters','03 · Core idea','04 · Architecture','05 · My contribution',
              '06 · Experiments','07 · Results','08 · Failure analysis','09 · Interactive demo','10 · Scaling',
              '11 · Safety / limitations','12 · Technical deep dive','13 · Artifacts','14 · Citation',
              'Paper','Code','Demo','Benchmark','Video','Aura Yavary','+10.46 pp','ContractBench-Implicit',
              'not an LLM capability result','Model size','Task horizon','Tool count','Cost / latency','Robustness']:
    if token.lower() not in page.lower(): errors.append(f'project page missing: {token}')
class _LinkParser(HTMLParser):
    def __init__(self): super().__init__(); self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            d=dict(attrs)
            if 'href' in d:self.hrefs.append(d['href'])
_lp=_LinkParser(); _lp.feed(page)
for href in _lp.hrefs:
    if href.startswith(('#','http://','https://','mailto:','javascript:')): continue
    if not (ROOT/href).resolve().exists(): errors.append(f'broken project-page link in reviewer bundle: {href}')

# Dataset integrity checks without requiring the full training fixtures/checkpoints.
def line_count(path):
    with path.open(encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())
if line_count(ROOT/'data/contractbench_implicit.jsonl') != 1460:
    errors.append('ContractBench-Implicit line count drift')
if line_count(ROOT/'data/agentic_contract_suite_v2.jsonl') != 288:
    errors.append('agentic suite line count drift')

# Reject unfinished placeholders in reviewer-facing text, excluding the verifier itself.
for p in ROOT.rglob('*'):
    if not p.is_file() or p.name in {Path(__file__).name,'build_reviewer_bundle.py','check_release_consistency.py'} or p.suffix.lower() in {'.pdf','.pt','.png','.zip','.pyc','.bundle'}:
        continue
    if any(part in {'.git','__pycache__'} for part in p.parts): continue
    try: txt=p.read_text(errors='ignore')
    except Exception: continue
    for token in ['TODO','FIXME','PLACEHOLDER','YOUR_MODEL_NAME_OR_LOCAL_PATH','TBD']:
        if token in txt:
            errors.append(f'forbidden placeholder {token} in {p.relative_to(ROOT)}')
            break

# Content-addressed digest for the evidence actually included in the reviewer package.
core=['reports/EXECUTED_EVIDENCE_MANIFEST.json','reports/paper_grade_robust_study.json',
      'reports/uncertainty_noninferiority.json','reports/agentic_contract_suite_v2.json',
      'external_runs/run_plan.json','paper/main.pdf','paper/supplement.pdf']
h=hashlib.sha256()
for rel in core:
    h.update(rel.encode()); h.update(b'\0'); h.update((ROOT/rel).read_bytes())

if errors: fail(errors)
print('REVIEWER BUNDLE VERIFY: PASS')
print('scope=curated_evidence_package_not_full_training_archive')
print('core_evidence_sha256='+h.hexdigest())
print('executed_claims=controlled_behavioral_model_only')
print('external_llm_human_gates=pending')
