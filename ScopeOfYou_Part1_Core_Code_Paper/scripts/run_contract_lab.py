from __future__ import annotations
import json, random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from personal_agi_pt.contract_opt import optimize
from personal_agi_pt.contract_eval import evaluate_contract
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.eval import evaluate
from personal_agi_pt.learned_policy import LearnedPersonalPolicy

DATA='data/samples/personalbench_v31.jsonl'
OUT='checkpoints/post_trained_v31_contract.pt'

def main():
    optimize('checkpoints/sft_behavior_v31.pt','checkpoints/reward_model_v31.pt',DATA,OUT)
    recs=[r for r in load_jsonl(DATA) if r.split=='test']
    methods={'SFT':'checkpoints/sft_behavior_v31.pt','Raw':'checkpoints/post_trained_v31_raw.pt','Constrained':'checkpoints/post_trained_v31_constrained.pt','BATPO':'checkpoints/post_trained_v31_boundary.pt','PCO':OUT}
    results={}
    per_user={}
    uid={r.conversation_id:r.user_id for r in recs}
    for name,ck in methods.items():
        p=LearnedPersonalPolicy(ck); ce=evaluate_contract(recs,p)
        results[name]={'personalbench':evaluate(recs,p)['summary'],'contract':ce['summary']}
        d=defaultdict(list)
        for row in ce['examples']:
            sc=mean([row['user_responsiveness'],row['invariant_stability'],row['context_suppression'],row['context_application'],row['invariant_attack_resistance']])
            d[uid[row['conversation_id']]].append(sc)
        per_user[name]={u:mean(v) for u,v in d.items()}
    users=sorted(set(per_user['BATPO'])&set(per_user['PCO']))
    diffs={u:per_user['PCO'][u]-per_user['BATPO'][u] for u in users}
    rng=random.Random(73); draws=[]
    for _ in range(5000):
        samp=[rng.choice(users) for _ in users]; draws.append(mean(diffs[u] for u in samp))
    draws.sort(); n=len(draws)
    stats={'n_users':len(users),'mean_delta':mean(diffs.values()),'ci95':[draws[int(.025*n)],draws[int(.975*n)-1]],'wins':sum(v>0 for v in diffs.values())}
    Path('reports/personalization_contract_results.json').write_text(json.dumps(results,indent=2))
    Path('reports/personalization_contract_statistics.json').write_text(json.dumps(stats,indent=2))
    print(json.dumps({'results':results,'statistics':stats},indent=2))
if __name__=='__main__': main()
