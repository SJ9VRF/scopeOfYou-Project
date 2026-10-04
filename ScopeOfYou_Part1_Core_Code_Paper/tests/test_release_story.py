from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TITLE = "Scope of You: Learning Where Personalization Is Allowed to Matter"


def test_canonical_title_is_consistent_in_release_docs():
    for rel in ["CITATION.cff", "CHANGELOG.md", "RELEASE_NOTES.md", "paper/main.tex", "README.md"]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "Personalization Contracts for When AI Should Adapt, Suppress, or Stay Invariant" not in text
    assert TITLE in (ROOT / "CITATION.cff").read_text(encoding="utf-8")


def test_executed_evidence_manifest_separates_pending_claims():
    data = json.loads((ROOT / "reports/EXECUTED_EVIDENCE_MANIFEST.json").read_text())
    cbi = data["executed"]["contractbench_implicit"]
    assert cbi["cases"] == 1460
    assert cbi["held_out_users"] == 20
    assert cbi["pco_robust"] > cbi["sft"] > cbi["batpo"]
    assert data["pending_external_gates"]
    assert data["frozen_external_plan"]["headline_runs"] == 36


def test_research_lead_brief_is_failure_first_and_claim_bounded():
    text = (ROOT / "RESEARCH_LEAD_BRIEF.md").read_text(encoding="utf-8")
    for phrase in ["failed on ContractBench-Implicit", "not proven", "2-point utility non-inferiority", "36-run"]:
        assert phrase.lower() in text.lower()
