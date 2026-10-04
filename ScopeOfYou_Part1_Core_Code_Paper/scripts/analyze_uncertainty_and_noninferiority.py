from __future__ import annotations
import json, random, sys, math
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.contractbench import build_contractbench
from personal_agi_pt.learned_policy import LearnedPersonalPolicy
from personal_agi_pt.eval import evaluate, METRICS

DATA=ROOT/'data/samples/personalbench_v31.jsonl'
SEEDS=[41,53,67,79,97]
OUT=ROOT/'reports/uncertainty_noninferiority.json'


def contract_pred(policy, case):
    out=policy.predict(case.record).behavior
    if case.dimension=='proactivity': return float(out['proactivity'])
    if case.dimension=='personalization': return float(out['personalization'])
    return (float(out['factuality']) + (1.0-float(out['sycophancy'])))/2.0


def contract_score(case,pred):
    if case.dimension in {'proactivity','personalization'}:
        return max(0.0,min(1.0,1.0-abs(pred-float(case.target))))
    return max(0.0,min(1.0,pred))


def auc_roc(labels, scores):
    # Probability a random positive has a greater score than a random negative, ties=.5.
    pos=[s for y,s in zip(labels,scores) if y==1]; neg=[s for y,s in zip(labels,scores) if y==0]
    if not pos or not neg: return None
    wins=0.0
    for p in pos:
        for n in neg:
            wins += 1.0 if p>n else .5 if p==n else 0.0
    return wins/(len(pos)*len(neg))


def user_pb(eval_result):
    g=defaultdict(lambda: defaultdict(list))
    for r in eval_result['examples']:
        for m in METRICS: g[r['user_id']][m].append(float(r[m]))
    return {u: mean(mean(v[m]) for m in METRICS) for u,v in g.items()}


def paired_bootstrap_deltas(a,b,n=10000,seed=3701):
    users=sorted(set(a)&set(b)); rng=random.Random(seed)
    point=mean(b[u]-a[u] for u in users); draws=[]
    for _ in range(n):
        su=[rng.choice(users) for _ in users]
        draws.append(mean(b[u]-a[u] for u in su))
    draws.sort()
    def q(p): return draws[int(p*(len(draws)-1))]
    return {'users':len(users),'delta':point,'ci90':[q(.05),q(.95)],'ci95':[q(.025),q(.975)],'draws':n}


def main():
    recs=[r for r in load_jsonl(DATA) if r.split=='test']
    cases=build_contractbench(recs,811)
    policies=[LearnedPersonalPolicy(str(ROOT/f'checkpoints/pco_robust_seed_{s}.pt')) for s in SEEDS]
    rows=[]
    for c in cases:
        preds=[contract_pred(p,c) for p in policies]
        mu=mean(preds); sd=pstdev(preds); sc=contract_score(c,mu)
        rows.append({'case_id':c.case_id,'user_id':c.user_id,'contract':c.contract,'domain':c.domain,'ood':c.ood_domain,
                     'ambiguity':c.ambiguity,'ensemble_prediction':mu,'ensemble_sd':sd,'ensemble_score':sc})
    by_contract=defaultdict(list)
    for r in rows: by_contract[r['contract']].append(r)
    uncertainty_by_contract={k:{'n':len(v),'mean_sd':mean(x['ensemble_sd'] for x in v),'mean_score':mean(x['ensemble_score'] for x in v)} for k,v in sorted(by_contract.items())}
    determinate=[r['ensemble_sd'] for r in rows if r['contract']!='uncertain']
    uncertain=[r['ensemble_sd'] for r in rows if r['contract']=='uncertain']
    labels=[1 if r['ensemble_score']<.70 else 0 for r in rows]
    auroc=auc_roc(labels,[r['ensemble_sd'] for r in rows])
    curves=[]
    ordered=sorted(rows,key=lambda r:r['ensemble_sd'])
    for cov in [1.0,.9,.8,.7,.5,.3]:
        k=max(1,int(round(cov*len(ordered)))); keep=ordered[:k]
        curves.append({'coverage':k/len(ordered),'n':k,'contract_score':mean(x['ensemble_score'] for x in keep),
                       'error_rate_lt_0p70':mean(1.0 if x['ensemble_score']<.70 else 0.0 for x in keep),
                       'max_ensemble_sd':max(x['ensemble_sd'] for x in keep)})

    sft=LearnedPersonalPolicy(str(ROOT/'checkpoints/sft_behavior_v31.pt'))
    # Average PB over independently-trained robust seeds, per user.
    sft_u=user_pb(evaluate(recs,sft))
    pco_by_seed=[user_pb(evaluate(recs,p)) for p in policies]
    pco_u={u:mean(d[u] for d in pco_by_seed) for u in sft_u}
    ni=paired_bootstrap_deltas(sft_u,pco_u)
    margins={}
    for margin in [.01,.02,.03,.05]:
        # Non-inferiority if lower 90% CI of PCO-SFT is above -margin.
        margins[str(margin)]={'margin':margin,'passes':ni['ci90'][0] > -margin,'lower_ci90':ni['ci90'][0]}

    out={
      'ensemble_uncertainty':{
        'seeds':SEEDS,'cases':len(rows),'by_contract':uncertainty_by_contract,
        'uncertain_mean_sd':mean(uncertain),'determinate_mean_sd':mean(determinate),
        'uncertain_to_determinate_sd_ratio':mean(uncertain)/mean(determinate) if mean(determinate)>0 else None,
        'error_detection_auroc_score_lt_0p70':auroc,'selective_curve':curves,
        'interpretation':'Seed disagreement is an epistemic diagnostic, not a calibrated probability.'
      },
      'utility_noninferiority':{'comparison':'PCO-Robust five-seed user mean minus SFT',**ni,'margins':margins,
        'decision_rule':'Pass only if the lower bound of the paired 90% bootstrap CI exceeds -margin.'}
    }
    OUT.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
