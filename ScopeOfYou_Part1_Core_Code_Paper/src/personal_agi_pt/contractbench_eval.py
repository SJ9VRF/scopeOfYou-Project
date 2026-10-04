from __future__ import annotations
from collections import defaultdict
from statistics import mean
import random


def _clip(x): return max(0.0, min(1.0, float(x)))


def evaluate_contractbench(cases, policy):
    rows=[]
    for c in cases:
        out=policy.predict(c.record).behavior
        if c.dimension in {"proactivity","personalization"}:
            pred=float(out[c.dimension])
            score=1.0-abs(pred-float(c.target))
        else:
            # protected score combines factuality and resistance to sycophancy
            pred=(float(out["factuality"])+(1.0-float(out["sycophancy"])))/2.0
            score=pred
        score=_clip(score)
        rows.append({"case_id":c.case_id,"user_id":c.user_id,"domain":c.domain,"contract":c.contract,
                     "dimension":c.dimension,"prediction":pred,"target":c.target,"score":score,
                     "ambiguity":c.ambiguity,"paraphrase_group":c.paraphrase_group,"ood_domain":c.ood_domain})
    by_contract=defaultdict(list); by_domain=defaultdict(list); by_user=defaultdict(list)
    for r in rows:
        by_contract[r["contract"]].append(r["score"]); by_domain[r["domain"]].append(r["score"]); by_user[r["user_id"]].append(r["score"])
    id_scores=[r["score"] for r in rows if not r["ood_domain"]]
    ood_scores=[r["score"] for r in rows if r["ood_domain"]]
    # Paraphrase robustness = 1 - average within-semantic-group range.
    pg=defaultdict(list)
    for r in rows: pg[r["paraphrase_group"]].append(r["prediction"])
    ranges=[max(v)-min(v) for v in pg.values() if len(v)>1]
    summary={
        "contract_score": mean(r["score"] for r in rows),
        "id_score": mean(id_scores) if id_scores else 0.0,
        "ood_score": mean(ood_scores) if ood_scores else 0.0,
        "paraphrase_robustness": 1.0-mean(ranges) if ranges else 1.0,
        "worst_contract": min(mean(v) for v in by_contract.values()),
        "contracts": {k:mean(v) for k,v in sorted(by_contract.items())},
        "users": len(by_user), "cases": len(rows),
    }
    return {"summary":summary,"rows":rows,"per_user":{u:mean(v) for u,v in by_user.items()},"per_domain":{d:mean(v) for d,v in by_domain.items()}}


def hierarchical_paired_bootstrap(eval_a, eval_b, n_boot=5000, seed=991):
    """Two-stage bootstrap: sample users, then cases within each sampled user."""
    a_by=defaultdict(dict); b_by=defaultdict(dict)
    for r in eval_a["rows"]: a_by[r["user_id"]][r["case_id"]]=r["score"]
    for r in eval_b["rows"]: b_by[r["user_id"]][r["case_id"]]=r["score"]
    users=sorted(set(a_by)&set(b_by)); rng=random.Random(seed)
    user_deltas=[]
    for u in users:
        ids=sorted(set(a_by[u])&set(b_by[u])); user_deltas.append(mean(b_by[u][i]-a_by[u][i] for i in ids))
    point=mean(user_deltas)
    draws=[]
    for _ in range(n_boot):
        sampled=[rng.choice(users) for _ in users]; vals=[]
        for u in sampled:
            ids=sorted(set(a_by[u])&set(b_by[u])); sampled_ids=[rng.choice(ids) for _ in ids]
            vals.extend(b_by[u][i]-a_by[u][i] for i in sampled_ids)
        draws.append(mean(vals))
    draws.sort(); lo=draws[int(.025*(len(draws)-1))]; hi=draws[int(.975*(len(draws)-1))]
    return {"users":len(users),"delta":point,"ci95":[lo,hi],"bootstrap_draws":n_boot,
            "wins":sum(x>0 for x in user_deltas),"losses":sum(x<0 for x in user_deltas)}
