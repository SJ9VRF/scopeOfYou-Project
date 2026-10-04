from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataio import dataset_stats, load_jsonl
from .eval import evaluate
from .policy import BootstrapPersonalPolicy
from .regression import apply_gates


def run(dataset: str, report: str) -> dict:
    records = load_jsonl(dataset)
    stats = dataset_stats(records)
    policy = BootstrapPersonalPolicy()
    evaluation = evaluate(records, policy)
    gates = apply_gates(evaluation["summary"])
    payload = {
        "stage": "bootstrap",
        "dataset": stats,
        "evaluation": evaluation,
        "regression_gates": gates,
    }
    output = Path(report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    payload = run(args.dataset, args.report)
    print(json.dumps({
        "dataset": payload["dataset"],
        "metrics": payload["evaluation"]["summary"],
        "ship": payload["regression_gates"]["ship"],
        "report": args.report,
    }, indent=2))


if __name__ == "__main__":
    main()
