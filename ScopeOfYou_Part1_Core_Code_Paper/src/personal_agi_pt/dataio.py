from __future__ import annotations

import json
from pathlib import Path

from .schema import InteractionRecord


def load_jsonl(path: str | Path) -> list[InteractionRecord]:
    records: list[InteractionRecord] = []
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
                record = InteractionRecord.from_dict(raw)
            except Exception as exc:
                raise ValueError(f"{path}:{lineno}: invalid record: {exc}") from exc
            errors = record.validate()
            if errors:
                raise ValueError(f"{path}:{lineno}: " + "; ".join(errors))
            records.append(record)
    return records


def dataset_stats(records: list[InteractionRecord]) -> dict:
    provenance: dict[str, int] = {}
    splits: dict[str, int] = {}
    users = set()
    for r in records:
        provenance[r.provenance] = provenance.get(r.provenance, 0) + 1
        splits[r.split] = splits.get(r.split, 0) + 1
        users.add(r.user_id)
    return {
        "num_records": len(records),
        "num_users": len(users),
        "provenance": provenance,
        "splits": splits,
    }
