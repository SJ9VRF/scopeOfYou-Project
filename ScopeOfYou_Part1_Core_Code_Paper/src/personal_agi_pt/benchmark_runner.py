from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataio import load_jsonl
from .eval import evaluate
from .learned_policy import LearnedPersonalPolicy
from .statistics import paired_user_bootstrap


def run_benchmark(dataset: str, checkpoint: str, split: str = "test") -> dict:
    records = [r for r in load_jsonl(dataset) if r.split == split]
    if not records:
        raise ValueError(f"no records found for split={split!r}")
    policy = LearnedPersonalPolicy(checkpoint)
    result = evaluate(records, policy)
    return {
        "dataset": dataset,
        "checkpoint": checkpoint,
        "split": split,
        "n_examples": len(records),
        "n_users": len({r.user_id for r in records}),
        **result,
    }


def compare_benchmarks(dataset: str, reference_checkpoint: str, candidate_checkpoint: str, split: str = "test", draws: int = 3000, seed: int = 17) -> dict:
    ref = run_benchmark(dataset, reference_checkpoint, split)
    cand = run_benchmark(dataset, candidate_checkpoint, split)
    records = [r for r in load_jsonl(dataset) if r.split == split]
    ref_policy = LearnedPersonalPolicy(reference_checkpoint)
    cand_policy = LearnedPersonalPolicy(candidate_checkpoint)
    stats = paired_user_bootstrap(records, ref_policy, cand_policy, n_boot=draws, seed=seed)
    return {"reference": ref, "candidate": cand, "paired_bootstrap": stats}


def main() -> None:
    p = argparse.ArgumentParser(description="Run PersonalBench against one or two checkpoints")
    p.add_argument("--dataset", default="data/samples/personalbench_v31.jsonl")
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--reference-checkpoint")
    p.add_argument("--split", default="test")
    p.add_argument("--draws", type=int, default=3000)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--output")
    a = p.parse_args()
    if a.reference_checkpoint:
        result = compare_benchmarks(a.dataset, a.reference_checkpoint, a.checkpoint, a.split, a.draws, a.seed)
    else:
        result = run_benchmark(a.dataset, a.checkpoint, a.split)
    text = json.dumps(result, indent=2)
    if a.output:
        Path(a.output).parent.mkdir(parents=True, exist_ok=True)
        Path(a.output).write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
