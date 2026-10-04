from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .dataio import load_jsonl


def interaction_to_sft(record: Any) -> dict[str, Any]:
    prefs = record.user_state or {}
    preference_lines = [f"{k}: {v}" for k, v in sorted(prefs.items()) if v is not None]
    system = (
        "You are a personalized assistant. Adapt style and proactivity to the supplied user state, "
        "while preserving factuality, calibrated uncertainty, and user autonomy.\nUser state:\n"
        + "\n".join(preference_lines)
    )
    response = record.candidate_response or ""
    return {
        "id": f"{record.conversation_id}:{record.user_id}",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": record.current_query},
            {"role": "assistant", "content": response},
        ],
        "metadata": {
            "user_id": record.user_id,
            "provenance": record.provenance,
            "confidence": record.confidence,
            "split": record.split,
        },
    }


def export_sft(source: str | Path, output: str | Path) -> dict[str, int]:
    records = load_jsonl(source)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            row = interaction_to_sft(r)
            counts[r.split] = counts.get(r.split, 0) + 1
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return counts



def export_sft_splits(source: str | Path, output_dir: str | Path) -> dict[str, int]:
    records = load_jsonl(source)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    handles = {}
    counts: dict[str, int] = {}
    try:
        for r in records:
            split = r.split or "train"
            if split not in handles:
                handles[split] = (out_dir / f"sft_{split}.jsonl").open("w", encoding="utf-8")
            handles[split].write(json.dumps(interaction_to_sft(r), ensure_ascii=False) + "\n")
            counts[split] = counts.get(split, 0) + 1
    finally:
        for h in handles.values():
            h.close()
    return counts

def main() -> None:
    p = argparse.ArgumentParser(description="Export internal interactions to chat-format JSONL.")
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    print(json.dumps(export_sft(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
