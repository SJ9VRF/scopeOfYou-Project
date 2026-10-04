from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _style_instruction(state: dict[str, Any]) -> str:
    return (
        "Adapt to this user state without sacrificing factuality or autonomy: "
        + json.dumps(state, ensure_ascii=False, sort_keys=True)
    )


def _candidate_text(name: str, query: str, state: dict[str, Any]) -> str:
    # Controlled text realization for the synthetic preference benchmark. These are not
    # intended as high-quality answers; they make preference semantics inspectable and
    # provide a DPO-format smoke dataset for the open-weight backend.
    if name == "personalized":
        return f"Personalized response to: {query} [style follows supplied user state; factual and appropriately proactive]"
    if name == "generic":
        return f"Generic response to: {query} [ignores user-specific style and context]"
    if name == "sycophantic":
        return f"Over-agreeing response to: {query} [prioritizes agreement over factual correction]"
    if name == "overproactive":
        return f"Over-proactive response to: {query} [takes or proposes unnecessary action without sufficient need]"
    return f"Response to: {query} [{name}]"


def export_dpo(source: str | Path, output: str | Path) -> dict[str, int]:
    src = Path(source)
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with src.open(encoding="utf-8") as fin, out.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            r = json.loads(line)
            state = r.get("user_state", {})
            q = r["query"]
            row = {
                "prompt": [
                    {"role": "system", "content": _style_instruction(state)},
                    {"role": "user", "content": q},
                ],
                "chosen": [{"role": "assistant", "content": _candidate_text(r["chosen"]["name"], q, state)}],
                "rejected": [{"role": "assistant", "content": _candidate_text(r["rejected"]["name"], q, state)}],
                "metadata": {
                    "conversation_id": r["conversation_id"],
                    "user_id": r["user_id"],
                    "chosen_behavior": r["chosen"]["behavior"],
                    "rejected_behavior": r["rejected"]["behavior"],
                    "provenance": r.get("provenance", "unknown"),
                    "confidence": r.get("confidence"),
                },
            }
            fout.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return {"pairs": n}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print(json.dumps(export_dpo(a.source, a.output), indent=2))


if __name__ == "__main__":
    main()
