from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import sys
from pathlib import Path

SENSITIVE_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "generic_secret_assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
}

TEXT_EXTENSIONS = {".py", ".md", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".txt", ".html", ".tex", ".cff", ".sh"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def audit_tree(root: Path) -> dict:
    findings = []
    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = str(p.relative_to(root))
        files.append({"path": rel, "size": p.stat().st_size, "sha256": sha256(p)})
        if p.suffix.lower() in TEXT_EXTENSIONS and p.stat().st_size <= 5_000_000:
            text = p.read_text(errors="ignore")
            for name, pattern in SENSITIVE_PATTERNS.items():
                if pattern.search(text):
                    findings.append({"file": rel, "type": name})
    return {
        "root": str(root),
        "file_count": len(files),
        "secret_findings": findings,
        "clean": not findings,
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "files": files,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Generate release provenance and scan text artifacts for obvious secrets")
    p.add_argument("--root", default=".")
    p.add_argument("--output", default="reports/release_audit.json")
    a = p.parse_args()
    root = Path(a.root).resolve()
    report = audit_tree(root)
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("file_count", "secret_findings", "clean", "environment")}, indent=2))
    raise SystemExit(0 if report["clean"] else 3)


if __name__ == "__main__":
    main()
