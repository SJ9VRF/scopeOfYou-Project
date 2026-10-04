import json
from pathlib import Path


def test_frontier_matrix_is_frozen_and_complete():
    m=json.loads(Path('configs/frontier/llm_experiment_matrix.json').read_text())
    assert len(m['backbones']) == 2
    assert len(m['methods']) == 6
    assert len(m['seeds']) == 3
    assert m['utility_noninferiority_margin'] == 0.02
    assert 'contractbench_implicit' in m['required_benchmarks']
    assert 'human_context_appropriateness' in m['required_metrics']


def test_run_plan_has_all_cells():
    p=json.loads(Path('external_runs/run_plan.json').read_text())
    assert p['n_runs'] == 36
    cells={(r['backbone'],r['method'],r['seed']) for r in p['runs']}
    assert len(cells)==36
