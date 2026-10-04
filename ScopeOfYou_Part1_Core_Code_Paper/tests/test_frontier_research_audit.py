from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("frontier_research_audit", Path("scripts/frontier_research_audit.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_frontier_research_audit_passes_repo():
    result = mod.audit(Path('.'))
    assert result['passed']
    assert result['agentic_result_correctly_scoped']
    assert not result['missing_required_artifacts']
