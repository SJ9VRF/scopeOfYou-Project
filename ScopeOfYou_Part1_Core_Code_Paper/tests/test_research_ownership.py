import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_failure_taxonomy_and_threat_model_are_present():
    taxonomy = (ROOT / 'docs/FAILURE_TAXONOMY.md').read_text()
    threat = (ROOT / 'docs/THREAT_MODEL.md').read_text()
    assert 'Observed' in taxonomy
    assert 'Evaluator stressor' in taxonomy
    assert 'External validation needed' in taxonomy
    assert 'Stale memory' in threat
    assert 'Tool injection' in threat
    assert 'Security claims deliberately not made' in threat


def test_red_team_coverage_matches_agentic_suite():
    cov = json.loads((ROOT / 'reports/red_team_coverage.json').read_text())
    assert cov['n_scenarios'] == 288
    assert cov['dimensions']['variant'] == {
        'clean': 96,
        'stale_memory': 96,
        'tool_injection': 96,
    }
    assert sum(cov['dimensions']['domain'].values()) == 288
    assert cov['artifact_scope'] == 'evaluator_stress_suite_not_model_capability'


def test_homepage_surfaces_ownership_layer():
    html = (ROOT / 'index.html').read_text()
    for rel in [
        './docs/FAILURE_TAXONOMY.md',
        './docs/THREAT_MODEL.md',
        './reports/RED_TEAM_COVERAGE_MATRIX.md',
        './docs/RESEARCH_OWNERSHIP_MAP.md',
    ]:
        assert rel in html
