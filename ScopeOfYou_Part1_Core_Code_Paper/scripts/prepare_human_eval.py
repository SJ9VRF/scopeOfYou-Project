from __future__ import annotations
import argparse,csv,json,random
from collections import defaultdict
from pathlib import Path

def read_jsonl(p):
    with open(p,encoding='utf-8') as f:
        for line in f:
            if line.strip(): yield json.loads(line)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',default='data/contractbench_implicit.jsonl'); ap.add_argument('--out',default='human_eval/phase_a_items.csv'); ap.add_argument('--n',type=int,default=500); ap.add_argument('--seed',type=int,default=1701); a=ap.parse_args()
    rows=list(read_jsonl(a.input)); rng=random.Random(a.seed)
    groups=defaultdict(list)
    for r in rows: groups[(r['contract'],bool(r['ood_domain']))].append(r)
    keys=sorted(groups,key=str); chosen=[]
    # round-robin stratification prevents one large contract class from dominating.
    for g in groups.values(): rng.shuffle(g)
    i=0
    while len(chosen)<min(a.n,len(rows)):
        k=keys[i%len(keys)]; g=groups[k]
        if g: chosen.append(g.pop())
        i+=1
        if not any(groups.values()): break
    rng.shuffle(chosen)
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    fields=['item_id','user_history','current_query','preference_context','domain','model_target_hidden','rater_label','confidence_1_5','rationale']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for j,r in enumerate(chosen):
            rec=r['record']; hist=' | '.join(x.get('content','') for x in rec.get('history',[]))
            w.writerow({'item_id':f'HEA-{j:04d}','user_history':hist,'current_query':rec['current_query'],'preference_context':json.dumps(rec.get('user_state',{}),sort_keys=True),'domain':r['domain'],'model_target_hidden':r['contract'],'rater_label':'','confidence_1_5':'','rationale':''})
    print(json.dumps({'items':len(chosen),'output':str(out),'seed':a.seed},indent=2))
if __name__=='__main__': main()
