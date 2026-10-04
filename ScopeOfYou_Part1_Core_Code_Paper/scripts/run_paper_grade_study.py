from __future__ import annotations
import json, sys
from pathlib import Path
from statistics import mean, pstdev
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.contract_opt import optimize, prepare_context, optimize_prepared, save_context, load_context
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.learned_policy import LearnedPersonalPolicy
from personal_agi_pt.eval import evaluate
from personal_agi_pt.contract_eval import evaluate_contract
from personal_agi_pt.contractbench import build_contractbench
from personal_agi_pt.contractbench_eval import evaluate_contractbench, hierarchical_paired_bootstrap

DATA=ROOT/'data/samples/personalbench_v31.jsonl'; SFT=ROOT/'checkpoints/sft_behavior_v31.pt'; RM=ROOT/'checkpoints/reward_model_v31.pt'
REPORT=ROOT/'reports/paper_grade_study.json'

def score(ck, test, cb):
    p=LearnedPersonalPolicy(str(ck)); return {
        'personalbench':evaluate(test,p)['summary'],
        'contract':evaluate_contract(test,p)['summary'],
        'implicit_contractbench':evaluate_contractbench(cb,p),
    }

def main():
    recs=load_jsonl(DATA); test=[r for r in recs if r.split=='test']; cb=build_contractbench(test,811)
    cache=ROOT/'data/cache/contract_training_context.pt'
    if cache.exists(): ctx=load_context(cache)
    else:
        ctx=prepare_context(SFT,RM,DATA); save_context(ctx,cache)
    seeds=[41,53,67,79,97]; seed_results=[]
    for seed in seeds:
        ck=ROOT/f'checkpoints/pco_seed_{seed}.pt'
        if not ck.exists(): optimize_prepared(ctx,ck,steps=180,seed=seed,batch_size=512)
        seed_results.append({'seed':seed,**score(ck,test,cb)})
    # Component ablations; fixed seed isolates objective components.
    ablations={
      'full':{}, 'no_user_contract':{'user_weight':0.0}, 'no_context_contract':{'context_weight':0.0},
      'no_invariant_preservation':{'invariant_weight':0.0}, 'no_attack_training':{'attack_weight':0.0}, 'no_trust_region':{'beta':0.0},
    }
    abl_results={}
    for name,kw in ablations.items():
        ck=ROOT/f'checkpoints/pco_ablation_{name}.pt';
        if not ck.exists(): optimize_prepared(ctx,ck,steps=20,seed=41,batch_size=128,**kw)
        abl_results[name]=score(ck,test,cb)
    # Pareto / sensitivity sweep: scale all contract enforcement while preserving base reward/trust machinery.
    pareto=[]
    for scale in [0.0,.25,.5,1.0,1.5,2.0]:
        ck=ROOT/f'checkpoints/pco_scale_{str(scale).replace(".","p")}.pt'
        if not ck.exists(): optimize_prepared(ctx,ck,steps=20,seed=41,batch_size=128,user_weight=28*scale,context_weight=34*scale,invariant_weight=120*scale,attack_weight=45*scale)
        sc=score(ck,test,cb); pareto.append({'scale':scale,**sc})
    # Baseline comparisons on independent implicit suite.
    baseline_ck={
      'SFT':SFT,'Raw':ROOT/'checkpoints/post_trained_v31_raw.pt','Constrained':ROOT/'checkpoints/post_trained_v31_constrained.pt',
      'BATPO':ROOT/'checkpoints/post_trained_v31_boundary.pt','PCO':ROOT/'checkpoints/pco_seed_41.pt'}
    base={k:score(v,test,cb) for k,v in baseline_ck.items()}
    stats={
      'BATPO_to_PCO_implicit':hierarchical_paired_bootstrap(base['BATPO']['implicit_contractbench'],base['PCO']['implicit_contractbench'],5000,1201),
      'SFT_to_PCO_implicit':hierarchical_paired_bootstrap(base['SFT']['implicit_contractbench'],base['PCO']['implicit_contractbench'],5000,1202),
    }
    seed_contract=[x['implicit_contractbench']['summary']['contract_score'] for x in seed_results]
    seed_pb=[x['personalbench']['personalbench_mean'] for x in [r['personalbench'] for r in seed_results]] if False else [x['personalbench']['personalbench_mean'] for x in seed_results]
    aggregate={'pco_implicit_contract_mean':mean(seed_contract),'pco_implicit_contract_std':pstdev(seed_contract),
               'pco_personalbench_mean':mean(seed_pb),'pco_personalbench_std':pstdev(seed_pb)}
    out={'contractbench':{'cases':len(cb),'users':len(set(c.user_id for c in cb)),'independent_templates':True,'implicit_scope_language':True},
         'five_seed_results':seed_results,'aggregate':aggregate,'ablations':abl_results,'pareto':pareto,'baselines':base,'statistics':stats}
    REPORT.write_text(json.dumps(out,indent=2)); print(json.dumps({'aggregate':aggregate,'stats':stats,'report':str(REPORT)},indent=2))
if __name__=='__main__': main()
