from pathlib import Path
from personal_agi_pt.data_quality import audit
from personal_agi_pt.grader_calibration import calibrate


def test_data_quality_runs():
    root=Path(__file__).parents[1]
    r=audit(root/'data/samples/seed.jsonl')
    assert r['records'] > 0
    assert r['schema_error_records'] == 0


def test_grader_calibration():
    r=calibrate([{'human':1,'grader':0.9},{'human':0,'grader':0.2}])
    assert r['n']==2
    assert r['binary_accuracy']==1.0


def test_v31_primary_dataset_has_strict_split_quality():
    from pathlib import Path
    from personal_agi_pt.data_quality import audit
    p=Path('data/samples/personalbench_v31.jsonl')
    if not p.exists():
        return
    q=audit(p)
    assert q['schema_error_records']==0
    assert q['exact_duplicate_rows']==0
    assert q['queries_seen_in_multiple_splits']==0
    assert q['users_seen_in_multiple_splits']==0
    assert q['split_counts']=={'train':3900,'test':1200,'validation':900}
