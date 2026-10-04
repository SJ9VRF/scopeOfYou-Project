from __future__ import annotations

import random
from collections import defaultdict
from statistics import mean

from .eval import evaluate, METRICS


def _user_metric_rows(eval_result: dict) -> dict[str, dict[str, float]]:
    grouped = defaultdict(lambda: defaultdict(list))
    for row in eval_result["examples"]:
        uid = row["user_id"]
        for m in METRICS:
            grouped[uid][m].append(float(row[m]))
    out = {}
    for uid, vals in grouped.items():
        out[uid] = {m: mean(vals[m]) for m in METRICS}
        out[uid]["personalbench_mean"] = mean(out[uid][m] for m in METRICS)
    return out


def paired_user_bootstrap(records, policy_a, policy_b, n_boot=2000, seed=101) -> dict:
    """Paired bootstrap over held-out users; positive delta means B is better."""
    a = _user_metric_rows(evaluate(records, policy_a))
    b = _user_metric_rows(evaluate(records, policy_b))
    users = sorted(set(a) & set(b))
    if not users:
        raise ValueError("No shared users for paired bootstrap")
    metrics = list(METRICS) + ["personalbench_mean"]
    point = {m: mean(b[u][m] - a[u][m] for u in users) for m in metrics}
    rng = random.Random(seed)
    draws = {m: [] for m in metrics}
    for _ in range(n_boot):
        sample = [rng.choice(users) for _ in users]
        for m in metrics:
            draws[m].append(mean(b[u][m] - a[u][m] for u in sample))
    cis = {}
    for m in metrics:
        xs = sorted(draws[m])
        lo = xs[int(0.025 * (len(xs)-1))]
        hi = xs[int(0.975 * (len(xs)-1))]
        cis[m] = {"delta": point[m], "ci95": [lo, hi]}
    return {"users": len(users), "bootstrap_draws": n_boot, "metrics": cis}
