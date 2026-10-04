from __future__ import annotations
from pathlib import Path
import zipfile, hashlib, json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'/'scope-of-you-reviewer-bundle.zip'
OUT.parent.mkdir(exist_ok=True)

exact=[
 'REVIEWER_README.md','HIRING_MANAGER_60_SECOND.md','RESEARCH_LEAD_BRIEF.md','FINAL_NOVELTY_AND_SOTA_STATUS.md',
 'CLAIMS_AND_LIMITATIONS.md','NOVELTY_AUDIT.md','REPRODUCIBILITY.md','TESTED_ENVIRONMENT.md',
 'CITATION.cff','LICENSE','pyproject.toml','index.html','PROJECT_PAGE_COMPLIANCE.md',
 'BENCHMARK_CONTRACT_CARD.md','DATASET_CARD.md','HIRING_MANAGER_WALKTHROUGH.md',
 'paper/main.pdf','paper/main.tex','paper/supplement.pdf','paper/supplementary_appendix.tex',
 'reports/EXECUTED_EVIDENCE_MANIFEST.json','reports/CLAIM_EVIDENCE_MATRIX.md',
 'reports/RESULTS_TABLE.md','reports/FAILURE_REPORT.md','reports/REVIEWER_ATTACK_MATRIX.md',
 'reports/OPENAI_ANTHROPIC_REVIEW_PACKET.md','reports/FRONTIER_READINESS_MATRIX.md',
 'reports/paper_grade_study.json','reports/paper_grade_robust_study.json','reports/uncertainty_noninferiority.json',
 'reports/failures_v31_raw_test.jsonl','reports/failures_v31_constrained_test.jsonl',
 'reports/personalization_leakage.json','reports/agentic_contract_suite_v2.json',
 'reports/AGENTIC_EVAL_V2_SUMMARY.md',
 'reports/RED_TEAM_COVERAGE_MATRIX.md','reports/red_team_coverage.json',
 'docs/RESEARCH_DECISION_LOG.md','docs/RELATED_WORK.md','docs/CITATION_PROVENANCE_AUDIT.md','docs/FORMAL_PROPERTIES.md',
 'docs/AGENTIC_EVAL_DESIGN.md','docs/EXTERNAL_EXECUTION_HANDOFF.md',
 'docs/FAILURE_TAXONOMY.md','docs/THREAT_MODEL.md','docs/RESEARCH_OWNERSHIP_MAP.md',
 'docs/HUMAN_EVAL_PROTOCOL.md','docs/SOTA_EVALUATION_PLAN.md','docs/GITHUB_PUBLISHING.md','docs/ML_SYSTEMS_DESIGN.md',
 'reports/TECHNICAL_REPORT.md','blog/index.html','video/scope-of-you-overview.mp4',
 'demo/live.html','demo/index.html','demo/trajectory.html','demo/agentic_eval_v2.html',
 'data/contractbench_implicit.jsonl','data/agentic_contract_suite_v2.jsonl',
 'configs/frontier/llm_experiment_matrix.json','external_runs/run_plan.json','external_runs/result.schema.json',
 'scripts/verify_reviewer_bundle.py','scripts/verify_frontier_artifact.py','scripts/frontier_research_audit.py',
 'scripts/run_agentic_contract_suite_v2.py','scripts/analyze_uncertainty_and_noninferiority.py',
 'scripts/analyze_personalization_leakage.py','scripts/verify_experiment_ledger.py','scripts/verify_citation_provenance.py',
 'scripts/build_red_team_coverage.py','scripts/verify_research_ownership.py',
 'experiments/EXPERIMENT_LEDGER.jsonl'
]
# Source/tests are included so the bundle remains inspectable and executable.
paths=[]
for rel in exact:
    p=ROOT/rel
    if p.exists(): paths.append(p)
for base in ['src','tests','evidence','artifacts','history']:
    for p in sorted((ROOT/base).rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc'):
            paths.append(p)
# De-duplicate and sort by relative path.
uniq={p.relative_to(ROOT).as_posix():p for p in paths}
items=sorted(uniq.items())

forbidden = ['TODO','FIXME','PLACEHOLDER','YOUR_MODEL_NAME_OR_LOCAL_PATH','TBD']
for rel,p in items:
    if rel in {'scripts/build_reviewer_bundle.py','scripts/verify_reviewer_bundle.py','scripts/verify_experiment_ledger.py','scripts/check_release_consistency.py'}:
        continue
    if p.suffix.lower() in {'.pt','.png','.pdf','.pyc','.zip','.bundle'}:
        continue
    try:
        txt=p.read_text(errors='ignore')
    except Exception:
        continue
    hits=[x for x in forbidden if x in txt]
    if hits:
        raise SystemExit(f'reviewer bundle rejected: {rel} contains forbidden placeholders {hits}')

fixed=(2026,1,1,0,0,0)
virtual = {
    'README.md': (ROOT/'REVIEWER_README.md').read_bytes(),
    'Makefile': b"PYTHONPATH ?= src\n\n.PHONY: verify-reviewer\nverify-reviewer:\n\tPYTHONPATH=$(PYTHONPATH) python scripts/verify_research_ownership.py\n\tPYTHONPATH=$(PYTHONPATH) python scripts/verify_experiment_ledger.py\n\tPYTHONPATH=$(PYTHONPATH) python scripts/verify_citation_provenance.py\n\tPYTHONPATH=$(PYTHONPATH) python scripts/verify_reviewer_bundle.py\n",
}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for rel,p in items:
        info=zipfile.ZipInfo(rel, fixed)
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644 << 16
        z.writestr(info,p.read_bytes())
    for rel,data in virtual.items():
        info=zipfile.ZipInfo(rel, fixed)
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644 << 16
        z.writestr(info,data)
sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
manifest={'name':'Scope of You reviewer bundle','files':len(items)+len(virtual),'sha256':sha,
          'scope':'curated hiring/reviewer artifact; full audit archive remains separate'}
(OUT.with_suffix('.manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
