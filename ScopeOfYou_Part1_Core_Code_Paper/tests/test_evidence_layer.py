from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_evidence_layer_files_exist():
    required = [
        'evidence/index.html','evidence/EXPERIMENT_JOURNAL.md','evidence/FAILED_EXPERIMENTS.md',
        'evidence/DECISION_LOG.md','evidence/REAL_EVAL_TABLES.md','evidence/UNEXPECTED_FINDINGS.md',
        'evidence/GIT_HISTORY.md','artifacts/experiment_logs/experiment_log.jsonl','artifacts/README.md'
    ]
    for rel in required:
        assert (ROOT/rel).exists(), rel

def test_experiment_journal_is_grounded():
    rows=[json.loads(x) for x in (ROOT/'artifacts/experiment_logs/experiment_log.jsonl').read_text().splitlines() if x.strip()]
    assert len(rows) == 11
    assert sum(r['status']=='failed' for r in rows) == 3
    for r in rows:
        assert all(k in r for k in ['hypothesis','setup','result','interpretation','next_decision','evidence'])
        assert r['evidence']

def test_homepage_surfaces_research_process():
    text=(ROOT/'index.html').read_text()
    for phrase in ['Inside the research process','View experiment journal','Failure analysis','View decisions','Open tables','Read findings','Browse evidence']:
        assert phrase in text
    for count in ['>11<','>4<','>8<','>5<']:
        assert count in text

def test_raw_artifact_tree_has_all_categories():
    for d in ['experiment_logs','eval_runs','failure_examples','plots','configs','qualitative_cases','ablations']:
        p=ROOT/'artifacts'/d
        assert p.is_dir() and any(p.iterdir()), d
