from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class ContractState(str, Enum):
    APPLY = "apply"
    SUPPRESS = "suppress"
    MUST_NOT_AFFECT = "must_not_affect"


@dataclass
class ContractClause:
    preference: str
    state: ContractState
    scope: str = "response"
    protected_dimensions: list[str] = field(default_factory=list)
    source: str = "benchmark"


@dataclass
class NormalizedExample:
    benchmark: str
    example_id: str
    prompt: str
    user_context: Any
    chosen: str | None = None
    rejected: str | None = None
    contracts: list[ContractClause] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        raw = asdict(self)
        for c in raw["contracts"]:
            if isinstance(c["state"], ContractState):
                c["state"] = c["state"].value
        return raw


def _str_id(record: dict[str, Any], fallback: int) -> str:
    for key in ("id", "example_id", "uid"):
        if key in record and record[key] not in (None, ""):
            return str(record[key])
    return str(fallback)


def adapt_benchpres(record: dict[str, Any], index: int = 0) -> NormalizedExample:
    attrs = list(record.get("preference_attribute") or [])
    labels = list(record.get("preference_label") or [])
    if len(attrs) != len(labels):
        raise ValueError("BenchPreS preference_attribute and preference_label lengths differ")
    contracts = [
        ContractClause(
            preference=str(pref),
            state=ContractState.APPLY if bool(label) else ContractState.SUPPRESS,
            scope="communicative_context",
            source="BenchPreS",
        )
        for pref, label in zip(attrs, labels)
    ]
    return NormalizedExample(
        benchmark="BenchPreS",
        example_id=_str_id(record, index),
        prompt=str(record.get("prompt", "")),
        user_context={
            "name": record.get("name"),
            "task": record.get("task"),
            "recipient": record.get("recipient"),
            "domain": record.get("domain"),
        },
        contracts=contracts,
        metadata={"license": "CC-BY-NC-4.0"},
    )


def adapt_personalized_rewardbench(record: dict[str, Any], index: int = 0) -> NormalizedExample:
    # The benchmark intentionally hides rubric_aspects/narrative from the model input.
    # We retain them only as metadata for offline analysis and never place them in user_context.
    return NormalizedExample(
        benchmark="PersonalizedRewardBench",
        example_id=_str_id(record, index),
        prompt=str(record.get("question", record.get("prompt", ""))),
        user_context={"profile": record.get("profile", []), "category": record.get("category")},
        chosen=record.get("chosen"),
        rejected=record.get("rejected"),
        contracts=[],
        metadata={
            "rubric_aspects": record.get("rubric_aspects"),
            "narrative": record.get("narrative"),
            "no_leak_fields": ["rubric_aspects", "narrative"],
        },
    )


def adapt_alignx(record: dict[str, Any], index: int = 0) -> NormalizedExample:
    pref_direction = record.get("Preference Direction", record.get("preference_direction"))
    return NormalizedExample(
        benchmark="AlignX",
        example_id=_str_id(record, index),
        prompt=str(record.get("prompt", "")),
        user_context={
            "preference_direction": pref_direction,
            "demographic_information": record.get("Demographic Information", record.get("demographic_information")),
            "user_generated_content": record.get("User-Generated Content", record.get("user_generated_content")),
            "pairwise_feedback": record.get("Pair-wise Comparative Feedback", record.get("pairwise_feedback")),
        },
        chosen=record.get("chosen"),
        rejected=record.get("rejected"),
        contracts=[],
        metadata={"preference_dimensions": len(pref_direction) if isinstance(pref_direction, list) else None},
    )


ADAPTERS = {
    "benchpres": adapt_benchpres,
    "personalized-rewardbench": adapt_personalized_rewardbench,
    "personalized_rewardbench": adapt_personalized_rewardbench,
    "alignx": adapt_alignx,
}


def normalize_records(records: Iterable[dict[str, Any]], benchmark: str) -> list[NormalizedExample]:
    key = benchmark.lower()
    if key not in ADAPTERS:
        raise ValueError(f"Unknown benchmark {benchmark!r}; choose from {sorted(ADAPTERS)}")
    fn = ADAPTERS[key]
    return [fn(r, i) for i, r in enumerate(records)]


def load_json_or_jsonl(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    raw = json.loads(text)
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("data", "test", "records", "examples"):
            if isinstance(raw.get(key), list):
                return raw[key]
    raise ValueError("Expected a JSON list/object with data/test/records/examples, or JSONL")


def write_normalized(examples: Iterable[NormalizedExample], path: str | Path) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex.to_dict(), ensure_ascii=False) + "\n")


def score_selectivity(gold_examples: Iterable[NormalizedExample], predictions: dict[str, list[str]]) -> dict[str, float | int]:
    """Score apply/suppress decisions using BenchPreS-style AAR and MR.

    predictions maps example_id -> list of states in the same order as contracts.
    Accepted predicted states are 'apply' and 'suppress'.
    """
    apply_total = apply_hit = suppress_total = suppress_misapplied = 0
    examples = 0
    for ex in gold_examples:
        if not ex.contracts:
            continue
        pred = predictions.get(ex.example_id)
        if pred is None:
            continue
        if len(pred) != len(ex.contracts):
            raise ValueError(f"Prediction length mismatch for {ex.example_id}")
        examples += 1
        for clause, p in zip(ex.contracts, pred):
            state = ContractState(p)
            if clause.state == ContractState.APPLY:
                apply_total += 1
                apply_hit += int(state == ContractState.APPLY)
            elif clause.state == ContractState.SUPPRESS:
                suppress_total += 1
                suppress_misapplied += int(state == ContractState.APPLY)
    aar = apply_hit / apply_total if apply_total else 0.0
    mr = suppress_misapplied / suppress_total if suppress_total else 0.0
    balanced = (aar + (1.0 - mr)) / 2.0 if (apply_total or suppress_total) else 0.0
    return {
        "examples_scored": examples,
        "apply_total": apply_total,
        "suppress_total": suppress_total,
        "AAR": aar,
        "MR": mr,
        "selectivity_score": balanced,
    }


def _read_predictions(path: str | Path) -> dict[str, list[str]]:
    rows = load_json_or_jsonl(path)
    out: dict[str, list[str]] = {}
    for row in rows:
        rid = str(row.get("id", row.get("example_id")))
        vals = row.get("decisions", row.get("predictions"))
        if not isinstance(vals, list):
            raise ValueError("Prediction rows require decisions/predictions list")
        out[rid] = [str(v) for v in vals]
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Normalize and score public personalization benchmarks")
    sp = p.add_subparsers(dest="cmd", required=True)
    n = sp.add_parser("normalize")
    n.add_argument("--benchmark", required=True, choices=["benchpres", "personalized-rewardbench", "alignx"])
    n.add_argument("--input", required=True); n.add_argument("--output", required=True)
    s = sp.add_parser("score-selectivity")
    s.add_argument("--gold", required=True); s.add_argument("--predictions", required=True); s.add_argument("--output")
    a = p.parse_args()
    if a.cmd == "normalize":
        ex = normalize_records(load_json_or_jsonl(a.input), a.benchmark)
        write_normalized(ex, a.output)
        print(json.dumps({"benchmark": a.benchmark, "examples": len(ex), "output": a.output}, indent=2))
    else:
        gold_raw = load_json_or_jsonl(a.gold)
        examples = []
        for row in gold_raw:
            contracts = [ContractClause(preference=c["preference"], state=ContractState(c["state"]), scope=c.get("scope","response"), protected_dimensions=c.get("protected_dimensions",[]), source=c.get("source","benchmark")) for c in row.get("contracts",[])]
            examples.append(NormalizedExample(benchmark=row.get("benchmark","unknown"), example_id=str(row["example_id"]), prompt=row.get("prompt",""), user_context=row.get("user_context"), chosen=row.get("chosen"), rejected=row.get("rejected"), contracts=contracts, metadata=row.get("metadata",{})))
        result = score_selectivity(examples, _read_predictions(a.predictions))
        if a.output:
            Path(a.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
