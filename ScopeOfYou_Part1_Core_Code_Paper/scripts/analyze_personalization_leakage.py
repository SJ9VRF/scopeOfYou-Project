from __future__ import annotations
import json, sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.learned_policy import LearnedPersonalPolicy
from personal_agi_pt.contract_eval import user_swap

DATA=ROOT/'data/samples/personalbench_v31.jsonl'
METHODS={
 'SFT':ROOT/'checkpoints/sft_behavior_v31.pt',
 'Raw':ROOT/'checkpoints/post_trained_v31_raw.pt',
 'Constrained':ROOT/'checkpoints/post_trained_v31_constrained.pt',
 'BATPO':ROOT/'checkpoints/post_trained_v31_boundary.pt',
 'PCO-Robust':ROOT/'checkpoints/pco_robust_seed_41.pt',
}
OUT=ROOT/'reports/personalization_leakage.json'

def main():
    recs=[r for r in load_jsonl(DATA) if r.split=='test']
    result={}
    for name,ck in METHODS.items():
        p=LearnedPersonalPolicy(str(ck)); fact=[]; nonsyc=[]; pers=[]
        for r in recs:
            b=p.predict(r).behavior; s=p.predict(user_swap(r)).behavior
            fact.append(abs(float(s['factuality'])-float(b['factuality'])))
            # convert sycophancy to non-sycophancy before difference; absolute difference is same, but explicit here.
            nonsyc.append(abs((1-float(s['sycophancy']))-(1-float(b['sycophancy']))))
            pers.append(abs(float(s['personalization'])-float(b['personalization'])))
        result[name]={
          'protected_leakage_mean':mean((a+b)/2 for a,b in zip(fact,nonsyc)),
          'factuality_leakage':mean(fact),
          'non_sycophancy_leakage':mean(nonsyc),
          'personalization_response_magnitude':mean(pers),
          'n':len(recs)
        }
    OUT.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
