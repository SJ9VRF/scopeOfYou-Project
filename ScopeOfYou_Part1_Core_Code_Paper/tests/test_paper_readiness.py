import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_frozen_llm_matrix_has_two_families_three_seeds():
    x=json.loads((ROOT/'configs/llm_paper/matrix.json').read_text())
    assert len(x['backbones']) >= 2
    assert len(x['seeds']) >= 3
    assert 'pco_robust' in x['methods']
    assert 'ContractBench-Implicit' in x['required_evaluations']

def test_human_eval_phase_a_is_preregistered_sample_size():
    with (ROOT/'human_eval/phase_a_items.csv').open() as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==500
    assert all(not r['rater_label'] for r in rows)

def test_negative_consistency_result_is_not_headline():
    x=json.loads((ROOT/'reports/consistency_regularization_negative.json').read_text())
    assert x['decision']=='rejected_from_headline_method'
    assert x['delta']['paraphrase_robustness'] < 0

def test_rigor_reports_expose_failed_strict_noninferiority():
    x=json.loads((ROOT/'reports/uncertainty_noninferiority.json').read_text())
    assert x['utility_noninferiority']['margins']['0.01']['passes'] is False
    assert x['utility_noninferiority']['margins']['0.02']['passes'] is False
    assert x['utility_noninferiority']['margins']['0.03']['passes'] is False
    assert x['utility_noninferiority']['delta'] < 0


def test_uncertainty_is_diagnostic_not_claimed_calibrated():
    x=json.loads((ROOT/'reports/uncertainty_noninferiority.json').read_text())
    u=x['ensemble_uncertainty']
    assert u['error_detection_auroc_score_lt_0p70'] > .5
    assert u['uncertain_to_determinate_sd_ratio'] < 1.2
    assert 'not a calibrated probability' in u['interpretation']


def test_claim_evidence_matrix_blocks_unexecuted_sota_claims():
    txt=(ROOT/'reports/CLAIM_EVIDENCE_MATRIX.md').read_text()
    assert 'PCO is SOTA on public personalization benchmarks' in txt
    assert '**Not executed**' in txt
    assert 'prohibited claim' in txt

def test_personalization_leakage_is_reported_without_overclaim():
    x=json.loads((ROOT/'reports/personalization_leakage.json').read_text())
    assert x['PCO-Robust']['protected_leakage_mean'] < .0015
    assert x['PCO-Robust']['protected_leakage_mean'] > x['BATPO']['protected_leakage_mean']


def test_llm_matrix_has_strict_future_utility_gate_and_broader_protected_dims():
    x=json.loads((ROOT/'configs/llm_paper/matrix.json').read_text())
    assert x['utility_noninferiority_margin_absolute'] <= .02
    assert 'privacy' in x['planned_protected_dimensions']
    assert 'autonomy' in x['planned_protected_dimensions']
    assert len(x['planned_agentic_actions']) >= 4
