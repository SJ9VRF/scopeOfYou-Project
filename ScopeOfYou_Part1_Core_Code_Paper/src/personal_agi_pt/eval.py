from __future__ import annotations

from statistics import mean

from .targets import behavior_target_dict

METRICS = ("personalization", "factuality", "sycophancy", "proactivity")


def evaluate(records, policy) -> dict:
    rows = []
    aggregate = {m: [] for m in METRICS}

    for record in records:
        out = policy.predict(record)
        targets = behavior_target_dict(record)
        row = {"conversation_id": record.conversation_id, "user_id": record.user_id}
        for metric in METRICS:
            pred = float(out.behavior[metric])
            target = float(targets[metric])
            score = 1.0 - abs(pred - target)
            score = max(0.0, min(1.0, score))
            aggregate[metric].append(score)
            row[metric] = score
            row[f"{metric}_prediction"] = pred
            row[f"{metric}_target"] = target
        rows.append(row)

    summary = {m: mean(v) if v else 0.0 for m, v in aggregate.items()}
    summary["personalbench_mean"] = mean(summary.values()) if summary else 0.0
    return {"summary": summary, "examples": rows}
