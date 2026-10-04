from pathlib import Path

from personal_agi_pt.benchmark_runner import run_benchmark, compare_benchmarks
from personal_agi_pt.release_audit import audit_tree
from personal_agi_pt.service import PolicyService

ROOT = Path(__file__).resolve().parents[1]


def test_policy_service_predicts():
    svc = PolicyService(str(ROOT / 'checkpoints/sft_behavior_v31.pt'))
    out = svc.predict({
        'user_id': 'smoke',
        'user_state': {
            'verbosity': 'concise',
            'directness': 'high',
            'technical_depth': 'advanced',
            'confirmation_policy': 'irreversible_only',
            'correction_tolerance': 'direct',
            'proactivity': 0.4,
        },
        'current_query': 'What is the capital of Germany?',
    })
    assert 'Berlin' in out['response']
    assert 0.0 <= out['behavior']['factuality'] <= 1.0


def test_independent_benchmark_runner():
    res = run_benchmark(
        str(ROOT / 'data/samples/personalbench_v31.jsonl'),
        str(ROOT / 'checkpoints/sft_behavior_v31.pt'),
        'test',
    )
    assert res['n_examples'] == 1200
    assert res['n_users'] == 20
    assert res['summary']['personalbench_mean'] > 0.95


def test_checkpoint_comparison_bootstrap():
    res = compare_benchmarks(
        str(ROOT / 'data/samples/personalbench_v31.jsonl'),
        str(ROOT / 'checkpoints/sft_behavior_v31.pt'),
        str(ROOT / 'checkpoints/post_trained_v31_raw.pt'),
        'test',
        draws=100,
        seed=3,
    )
    delta = res['paired_bootstrap']['metrics']['personalbench_mean']['delta']
    assert delta < -0.10


def test_release_audit_has_no_obvious_secrets(tmp_path):
    (tmp_path / 'a.py').write_text('x = 1\n')
    report = audit_tree(tmp_path)
    assert report['clean'] is True
    assert report['file_count'] == 1
