from pathlib import Path

from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.pipeline import run


ROOT = Path(__file__).resolve().parents[1]


def test_seed_dataset_validates():
    records = load_jsonl(ROOT / "data" / "samples" / "seed.jsonl")
    assert len(records) == 3


def test_pipeline_writes_report(tmp_path):
    out = tmp_path / "report.json"
    payload = run(ROOT / "data" / "samples" / "seed.jsonl", out)
    assert out.exists()
    assert payload["evaluation"]["summary"]["factuality"] >= 0.95
