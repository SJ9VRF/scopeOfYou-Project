from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class RunRecord:
    run_id: str
    name: str
    stage: str
    started_at_unix: float
    finished_at_unix: float | None
    status: str
    seed: int
    git_commit: str | None
    python: str
    platform: str
    config_sha256: str | None
    dataset_sha256: str | None
    metrics: dict[str, Any]
    artifacts: list[str]


def _sha256(path: str | Path | None) -> str | None:
    if path is None:
        return None
    p = Path(path)
    if not p.exists() or not p.is_file():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_commit(root: str | Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None


def start_run(root: str | Path, name: str, stage: str, seed: int, config: str | Path | None = None,
              dataset: str | Path | None = None) -> RunRecord:
    now = time.time()
    entropy = f"{name}|{stage}|{seed}|{now}|{os.getpid()}".encode()
    run_id = hashlib.sha256(entropy).hexdigest()[:12]
    return RunRecord(
        run_id=run_id,
        name=name,
        stage=stage,
        started_at_unix=now,
        finished_at_unix=None,
        status="running",
        seed=seed,
        git_commit=_git_commit(root),
        python=platform.python_version(),
        platform=platform.platform(),
        config_sha256=_sha256(config),
        dataset_sha256=_sha256(dataset),
        metrics={},
        artifacts=[],
    )


def finish_run(root: str | Path, run: RunRecord, metrics: dict[str, Any], artifacts: list[str] | None = None,
               status: str = "completed") -> Path:
    run.finished_at_unix = time.time()
    run.status = status
    run.metrics = metrics
    run.artifacts = artifacts or []
    out_dir = Path(root) / "experiments" / "runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{run.run_id}.json"
    out.write_text(json.dumps(asdict(run), indent=2, sort_keys=True), encoding="utf-8")
    return out
