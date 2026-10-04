import json
from pathlib import Path

from personal_agi_pt.hf_export import export_sft, export_sft_splits
from personal_agi_pt.preference_export import export_dpo


def test_sft_export(tmp_path):
    src = Path(__file__).parents[1] / "data" / "samples" / "seed.jsonl"
    out = tmp_path / "sft.jsonl"
    counts = export_sft(src, out)
    assert out.exists()
    first = json.loads(out.read_text().splitlines()[0])
    assert first["messages"][0]["role"] == "system"
    assert sum(counts.values()) > 0


def test_dpo_export(tmp_path):
    root = Path(__file__).parents[1]
    src = root / "data" / "samples" / "preferences_v1.jsonl"
    out = tmp_path / "dpo.jsonl"
    counts = export_dpo(src, out)
    assert counts["pairs"] > 0
    first = json.loads(out.read_text().splitlines()[0])
    assert first["chosen"][0]["role"] == "assistant"
    assert first["rejected"][0]["role"] == "assistant"


def test_sft_split_export(tmp_path):
    root = Path(__file__).parents[1]
    src = root / "data" / "samples" / "lab_v2_clean.jsonl"
    counts = export_sft_splits(src, tmp_path)
    assert counts == {"train": 4000, "test": 500, "validation": 500}
    assert (tmp_path / "sft_train.jsonl").exists()
    assert (tmp_path / "sft_validation.jsonl").exists()
    assert (tmp_path / "sft_test.jsonl").exists()
