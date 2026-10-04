from __future__ import annotations
import json, random, sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev
import torch
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.contractbench import build_contractbench
from personal_agi_pt.features import FeatureEncoder, target_behavior
from personal_agi_pt.models import BehaviorAdapter

DATA=ROOT/'data/samples/personalbench_v31.jsonl'
REPORT=ROOT/'reports/paper_grade_study.json'

def load_model(ck):
    z=torch.load(ck,map_location='cpu',weights_only=False); enc=FeatureEncoder(**z.get('encoder',{})); m=BehaviorAdapter(z['input_dim']); m.load_state_dict(z['state_dict']); m.eval(); return enc,m

def precompute(records,cases):
    enc=FeatureEncoder()
    X=torch.stack([enc.encode(r) for r in records]); Y=torch.stack([target_behavior(r) for r in records])
    Xc=torch.stack([enc.encode(c.record) for c in cases])
    return enc,X,Y,Xc

def score_ck(ck,records,cases,X,Y,Xc):
    _,m=load_model(ck)
    with torch.no_grad(): P=m(X); Pc=m(Xc)
    # PersonalBench: nonsycophancy is stored at col2, matching Y directly.
    dim_scores=(1.0-(P-Y).abs()).clamp(0,1).mean(0).tolist()
    pb={'personalization':dim_scores[0],'factuality':dim_scores[1],'sycophancy':dim_scores[2],'proactivity':dim_scores[3]}
    pb['personalbench_mean']=mean(pb.values())
    rows=[]
    for i,c in enumerate(cases):
        vals=Pc[i]
        if c.dimension in {'proactivity','personalization'}:
            pred=float(vals[3] if c.dimension=='proactivity' else vals[0]); sc=max(0,min(1,1-abs(pred-c.target)))
        else: pred=(float(vals[1])+float(vals[2]))/2; sc=max(0,min(1,pred))
        rows.append({'case_id':c.case_id,'user_id':c.user_id,'domain':c.domain,'contract':c.contract,'score':sc,
                     'prediction':pred,'paraphrase_group':c.paraphrase_group,'ood_domain':c.ood_domain})
    bc=defaultdict(list); bu=defaultdict(list); pg=defaultdict(list); ids=[]; oods=[]
    for r in rows:
        bc[r['contract']].append(r['score']); bu[r['user_id']].append(r['score']); pg[r['paraphrase_group']].append(r['prediction']); (oods if r['ood_domain'] else ids).append(r['score'])
    ranges=[max(v)-min(v) for v in pg.values() if len(v)>1]
    cb={'contract_score':mean(r['score'] for r in rows),'id_score':mean(ids),'ood_score':mean(oods),
        'paraphrase_robustness':1-mean(ranges),'worst_contract':min(mean(v) for v in bc.values()),
        'contracts':{k:mean(v) for k,v in sorted(bc.items())},'users':len(bu),'cases':len(rows)}
    return {'personalbench':pb,'implicit_contractbench':{'summary':cb,'rows':rows,'per_user':{u:mean(v) for u,v in bu.items()}}}

def hboot(a,b,n=5000,seed=13):
    ab=defaultdict(dict); bb=defaultdict(dict)
    for r in a['rows']: ab[r['user_id']][r['case_id']]=r['score']
    for r in b['rows']: bb[r['user_id']][r['case_id']]=r['score']
    users=sorted(set(ab)&set(bb)); rng=random.Random(seed)
    point=mean(mean(bb[u][i]-ab[u][i] for i in set(ab[u])&set(bb[u])) for u in users); draws=[]
    for _ in range(n):
        su=[rng.choice(users) for _ in users]; vals=[]
        for u in su:
            ids=list(set(ab[u])&set(bb[u])); si=[rng.choice(ids) for _ in ids]; vals.extend(bb[u][i]-ab[u][i] for i in si)
        draws.append(mean(vals))
    draws.sort(); return {'users':len(users),'delta':point,'ci95':[draws[int(.025*(n-1))],draws[int(.975*(n-1))]],'wins':sum(mean(bb[u][i]-ab[u][i] for i in set(ab[u])&set(bb[u]))>0 for u in users)}

def main():
    recs=[r for r in load_jsonl(DATA) if r.split=='test']; cases=build_contractbench(recs,811); enc,X,Y,Xc=precompute(recs,cases)
    seeds=[41,53,67,79,97]; seed_results=[]
    for seed in seeds:
        seed_results.append({'seed':seed,**score_ck(ROOT/f'checkpoints/pco_seed_{seed}.pt',recs,cases,X,Y,Xc)})
    ablations={}
    for name in ['full','no_user_contract','no_context_contract','no_invariant_preservation','no_attack_training','no_trust_region']:
        ablations[name]=score_ck(ROOT/f'checkpoints/pco_ablation_{name}.pt',recs,cases,X,Y,Xc)
    pareto=[]
    for scale in [0.0,.25,.5,1.0,1.5,2.0]: pareto.append({'scale':scale,**score_ck(ROOT/f'checkpoints/pco_scale_{str(scale).replace(".","p")}.pt',recs,cases,X,Y,Xc)})
    bcks={'SFT':ROOT/'checkpoints/sft_behavior_v31.pt','Raw':ROOT/'checkpoints/post_trained_v31_raw.pt','Constrained':ROOT/'checkpoints/post_trained_v31_constrained.pt','BATPO':ROOT/'checkpoints/post_trained_v31_boundary.pt','PCO':ROOT/'checkpoints/pco_seed_41.pt'}
    baselines={k:score_ck(v,recs,cases,X,Y,Xc) for k,v in bcks.items()}
    cvals=[r['implicit_contractbench']['summary']['contract_score'] for r in seed_results]; pvals=[r['personalbench']['personalbench_mean'] for r in seed_results]
    out={'contractbench':{'cases':len(cases),'users':len(set(c.user_id for c in cases)),'independent_templates':True,'implicit_scope_language':True},
         'five_seed_results':seed_results,'aggregate':{'pco_implicit_contract_mean':mean(cvals),'pco_implicit_contract_std':pstdev(cvals),'pco_personalbench_mean':mean(pvals),'pco_personalbench_std':pstdev(pvals)},
         'ablations':ablations,'pareto':pareto,'baselines':baselines,
         'statistics':{'BATPO_to_PCO_implicit':hboot(baselines['BATPO']['implicit_contractbench'],baselines['PCO']['implicit_contractbench'],5000,1201),'SFT_to_PCO_implicit':hboot(baselines['SFT']['implicit_contractbench'],baselines['PCO']['implicit_contractbench'],5000,1202)}}
    REPORT.write_text(json.dumps(out,indent=2)); print(json.dumps({'aggregate':out['aggregate'],'statistics':out['statistics'],'report':str(REPORT)},indent=2))
if __name__=='__main__': main()
