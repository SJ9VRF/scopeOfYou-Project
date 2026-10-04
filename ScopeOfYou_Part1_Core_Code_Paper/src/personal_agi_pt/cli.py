from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .hf_export import export_sft, export_sft_splits
from .llm_backend import LLMTrainConfig, dependency_status, train_lora_sft
from .preference_export import export_dpo


def _json(x):
    print(json.dumps(x, indent=2, default=str))


def doctor(_: argparse.Namespace) -> int:
    root = Path(__file__).resolve().parents[2]
    status = dependency_status()
    status["project_root"] = str(root)
    status["core_files"] = {
        "dataset": (root / "data/samples/lab_v1.jsonl").exists(),
        "sft_checkpoint": (root / "checkpoints/sft_behavior.pt").exists(),
        "reward_checkpoint": (root / "checkpoints/reward_model.pt").exists(),
        "technical_report": (root / "reports/TECHNICAL_REPORT.md").exists(),
    }
    _json(status)
    return 0


def do_export(args: argparse.Namespace) -> int:
    _json(export_sft(args.source, args.output))
    return 0


def do_export_splits(args: argparse.Namespace) -> int:
    _json(export_sft_splits(args.source, args.output_dir))
    return 0


def do_export_dpo(args: argparse.Namespace) -> int:
    _json(export_dpo(args.source, args.output))
    return 0


def do_llm_sft(args: argparse.Namespace) -> int:
    cfg = LLMTrainConfig(
        model_name_or_path=args.model,
        train_file=args.train_file,
        eval_file=args.eval_file,
        output_dir=args.output_dir,
        max_seq_length=args.max_seq_length,
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        seed=args.seed,
    )
    _json(train_lora_sft(cfg))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bounded-self", description="Scope of You — Learning Where Personalization Is Allowed to Matter")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("doctor", help="Inspect runtime and optional LLM dependencies")
    d.set_defaults(func=doctor)

    e = sub.add_parser("export-sft", help="Export internal interactions to chat JSONL")
    e.add_argument("--source", default="data/samples/lab_v1.jsonl")
    e.add_argument("--output", default="data/exports/sft_chat.jsonl")
    e.set_defaults(func=do_export)

    es = sub.add_parser("export-sft-splits", help="Export one chat JSONL per dataset split")
    es.add_argument("--source", default="data/samples/lab_v1.jsonl")
    es.add_argument("--output-dir", default="data/exports")
    es.set_defaults(func=do_export_splits)

    pexp = sub.add_parser("export-dpo", help="Export synthetic preference pairs to conversational DPO JSONL")
    pexp.add_argument("--source", default="data/samples/preferences_v1.jsonl")
    pexp.add_argument("--output", default="data/exports/dpo_pairs.jsonl")
    pexp.set_defaults(func=do_export_dpo)

    s = sub.add_parser("llm-sft", help="Run LoRA SFT on an open-weight causal LM")
    s.add_argument("--model", required=True)
    s.add_argument("--train-file", required=True)
    s.add_argument("--eval-file")
    s.add_argument("--output-dir", required=True)
    s.add_argument("--max-seq-length", type=int, default=2048)
    s.add_argument("--learning-rate", type=float, default=2e-4)
    s.add_argument("--epochs", type=float, default=1.0)
    s.add_argument("--batch-size", type=int, default=1)
    s.add_argument("--grad-accum", type=int, default=16)
    s.add_argument("--seed", type=int, default=13)
    s.set_defaults(func=do_llm_sft)
    return p


def main() -> None:
    args = build_parser().parse_args()
    try:
        raise SystemExit(args.func(args))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
