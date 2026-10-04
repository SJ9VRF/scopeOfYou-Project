from __future__ import annotations

"""Optional open-weight LLM backend.

This module is deliberately lazy-imported so the core CPU research loop remains runnable
without downloading external models. It supports supervised LoRA fine-tuning through
Transformers + PEFT and exposes a dependency doctor for GPU environments.
"""

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class LLMTrainConfig:
    model_name_or_path: str
    train_file: str
    eval_file: str | None
    output_dir: str
    max_seq_length: int = 2048
    learning_rate: float = 2e-4
    num_train_epochs: float = 1.0
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    gradient_accumulation_steps: int = 16
    warmup_ratio: float = 0.03
    weight_decay: float = 0.0
    logging_steps: int = 10
    save_steps: int = 200
    eval_steps: int = 200
    seed: int = 13
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    bf16: bool = True
    gradient_checkpointing: bool = True


def dependency_status() -> dict[str, Any]:
    result: dict[str, Any] = {}
    for pkg in ("torch", "transformers", "datasets", "accelerate", "peft"):
        try:
            module = __import__(pkg)
            result[pkg] = {"installed": True, "version": getattr(module, "__version__", "unknown")}
        except Exception as exc:
            result[pkg] = {"installed": False, "error": type(exc).__name__}
    try:
        import torch
        result["cuda"] = {
            "available": bool(torch.cuda.is_available()),
            "device_count": int(torch.cuda.device_count()),
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        }
    except Exception:
        result["cuda"] = {"available": False, "device_count": 0, "device_name": None}
    return result


def _require_stack() -> None:
    status = dependency_status()
    missing = [k for k in ("torch", "transformers", "datasets", "accelerate", "peft") if not status[k]["installed"]]
    if missing:
        raise RuntimeError(
            "Missing optional LLM training dependencies: " + ", ".join(missing)
            + ". Install with `pip install -e '.[train]'`."
        )


def train_lora_sft(cfg: LLMTrainConfig) -> dict[str, Any]:
    _require_stack()
    import torch
    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model
    import inspect
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name_or_path, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dtype = torch.bfloat16 if cfg.bf16 and torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(cfg.model_name_or_path, torch_dtype=dtype)
    if cfg.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    peft_cfg = LoraConfig(
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        lora_dropout=cfg.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules="all-linear",
    )
    model = get_peft_model(model, peft_cfg)

    files = {"train": cfg.train_file}
    if cfg.eval_file:
        files["validation"] = cfg.eval_file
    ds = load_dataset("json", data_files=files)

    def tokenize(batch: dict[str, list[Any]]) -> dict[str, Any]:
        texts = []
        for msgs in batch["messages"]:
            texts.append(tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False))
        enc = tokenizer(texts, truncation=True, max_length=cfg.max_seq_length, padding=False)
        enc["labels"] = [ids[:] for ids in enc["input_ids"]]
        return enc

    tokenized = ds.map(tokenize, batched=True, remove_columns=ds["train"].column_names)
    ta_kwargs = dict(
        output_dir=cfg.output_dir,
        learning_rate=cfg.learning_rate,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        per_device_eval_batch_size=cfg.per_device_eval_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        warmup_ratio=cfg.warmup_ratio,
        weight_decay=cfg.weight_decay,
        logging_steps=cfg.logging_steps,
        save_steps=cfg.save_steps,
        eval_steps=cfg.eval_steps,
        save_strategy="steps",
        bf16=bool(cfg.bf16 and torch.cuda.is_available()),
        fp16=False,
        report_to=[],
        seed=cfg.seed,
        remove_unused_columns=False,
    )
    # Transformers renamed evaluation_strategy -> eval_strategy in newer releases.
    params = inspect.signature(TrainingArguments.__init__).parameters
    eval_key = "eval_strategy" if "eval_strategy" in params else "evaluation_strategy"
    ta_kwargs[eval_key] = "steps" if cfg.eval_file else "no"
    args = TrainingArguments(**ta_kwargs)

    # A tiny collator is used instead of relying on TRL so this path stays minimally coupled.
    def collate(features: list[dict[str, Any]]) -> dict[str, torch.Tensor]:
        max_len = max(len(x["input_ids"]) for x in features)
        ids, mask, labels = [], [], []
        for x in features:
            n = len(x["input_ids"])
            pad = max_len - n
            ids.append(x["input_ids"] + [tokenizer.pad_token_id] * pad)
            mask.append(x["attention_mask"] + [0] * pad)
            labels.append(x["labels"] + [-100] * pad)
        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(mask, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized.get("validation"),
        data_collator=collate,
    )
    result = trainer.train()
    trainer.save_model(cfg.output_dir)
    tokenizer.save_pretrained(cfg.output_dir)
    metrics = dict(result.metrics)
    metrics["config"] = asdict(cfg)
    metrics["backend"] = "transformers_peft_lora"
    Path(cfg.output_dir).mkdir(parents=True, exist_ok=True)
    Path(cfg.output_dir, "train_metrics.json").write_text(json.dumps(metrics, indent=2, default=str), encoding="utf-8")
    return metrics
