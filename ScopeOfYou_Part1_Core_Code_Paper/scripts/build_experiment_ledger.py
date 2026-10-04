from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'experiments'/'EXPERIMENT_LEDGER.jsonl'
OUT.parent.mkdir(exist_ok=True)

def sha(rel: str) -> str:
    p=ROOT/rel
    return hashlib.sha256(p.read_bytes()).hexdigest()

def art(rel: str):
    p=ROOT/rel
    if not p.exists():
        raise FileNotFoundError(rel)
    return {'path':rel,'sha256':sha(rel),'bytes':p.stat().st_size}

entries=[
  {
    'id':'pco_explicit_template_failure',
    'kind':'negative_result',
    'status':'executed',
    'claim':'The original explicit-template PCO did not generalize to the independently worded implicit contract suite.',
    'reproduction_entrypoint':'PYTHONPATH=src python scripts/run_paper_grade_study.py',
    'historical_shell_invocation_asserted':False,
    'inputs':['data/contractbench_implicit.jsonl'],
    'outputs':['reports/paper_grade_study.json'],
    'decision_link':'docs/RESEARCH_DECISION_LOG.md'
  },
  {
    'id':'pco_robust_five_seed_controlled_study',
    'kind':'headline_result',
    'status':'executed',
    'claim':'PCO-Robust improves ContractBench-Implicit selectivity over SFT and BATPO in the controlled behavioral backend, with a utility tradeoff.',
    'reproduction_entrypoint':'PYTHONPATH=src python scripts/finalize_robust_paper_grade_results.py',
    'historical_shell_invocation_asserted':False,
    'inputs':['data/contractbench_implicit.jsonl'],
    'outputs':['reports/paper_grade_robust_study.json'],
    'decision_link':'reports/CLAIM_EVIDENCE_MATRIX.md'
  },
  {
    'id':'uncertainty_and_noninferiority',
    'kind':'rigor_analysis',
    'status':'executed',
    'claim':'The 2 percentage-point utility non-inferiority gate fails; seed disagreement is diagnostic but not claimed as calibrated uncertainty.',
    'reproduction_entrypoint':'PYTHONPATH=src python scripts/analyze_uncertainty_and_noninferiority.py',
    'historical_shell_invocation_asserted':False,
    'inputs':['reports/paper_grade_robust_study.json'],
    'outputs':['reports/uncertainty_noninferiority.json'],
    'decision_link':'CLAIMS_AND_LIMITATIONS.md'
  },
  {
    'id':'personalization_leakage',
    'kind':'rigor_analysis',
    'status':'executed',
    'claim':'Protected-dimension personalization leakage is measured directly rather than inferred from contract score.',
    'reproduction_entrypoint':'PYTHONPATH=src python scripts/analyze_personalization_leakage.py',
    'historical_shell_invocation_asserted':False,
    'inputs':['reports/paper_grade_robust_study.json'],
    'outputs':['reports/personalization_leakage.json'],
    'decision_link':'docs/FORMAL_PROPERTIES.md'
  },
  {
    'id':'agentic_contract_suite_v2',
    'kind':'evaluator_stress_test',
    'status':'executed',
    'claim':'The stateful evaluator distinguishes naive, risk-aware, noisy, and oracle policies across permission, recovery, stale-memory, and untrusted-tool perturbations. This is not an LLM capability result.',
    'reproduction_entrypoint':'PYTHONPATH=src python scripts/run_agentic_contract_suite_v2.py',
    'historical_shell_invocation_asserted':False,
    'inputs':['data/agentic_contract_suite_v2.jsonl'],
    'outputs':['reports/agentic_contract_suite_v2.json','reports/AGENTIC_EVAL_V2_SUMMARY.md'],
    'decision_link':'docs/AGENTIC_EVAL_DESIGN.md'
  },
  {
    'id':'frontier_external_llm_matrix',
    'kind':'external_gate',
    'status':'planned_not_executed',
    'claim':'No frontier-LLM or public-benchmark result is claimed until this frozen 36-run matrix is executed.',
    'reproduction_entrypoint':'See docs/EXTERNAL_EXECUTION_HANDOFF.md',
    'historical_shell_invocation_asserted':False,
    'inputs':['configs/frontier/llm_experiment_matrix.json','external_runs/run_plan.json','external_runs/result.schema.json'],
    'outputs':[],
    'decision_link':'FINAL_NOVELTY_AND_SOTA_STATUS.md'
  },
]
for e in entries:
    e['input_artifacts']=[art(x) for x in e.pop('inputs')]
    e['output_artifacts']=[art(x) for x in e.pop('outputs')]
    dl=e.get('decision_link')
    if dl and (ROOT/dl).exists(): e['decision_artifact']=art(dl)
with OUT.open('w') as f:
    for e in entries:
        f.write(json.dumps(e,sort_keys=True)+'\n')
print(f'wrote {len(entries)} entries to {OUT.relative_to(ROOT)}')
