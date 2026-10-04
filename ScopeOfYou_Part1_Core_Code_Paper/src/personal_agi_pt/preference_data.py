from __future__ import annotations
import argparse,json,random
from pathlib import Path
from .dataio import load_jsonl
from .features import target_behavior

CANDIDATES={
 'concise_personalized':[.10,.95,.95,.45,.90],
 'balanced_personalized':[.50,.95,.95,.55,.90],
 'detailed_personalized':[.90,.95,.95,.60,.90],
 'generic':[.50,.92,.92,.30,.60],
 'sycophantic':[.70,.35,.15,.55,.72],
 'overproactive':[.65,.85,.80,.98,.72],
}

def utility(target,cand):
 # Match user-dependent controls; preserve truthfulness/non-sycophancy as invariants.
 personalization_match=1-abs(float(cand[0])-float(target[0]))
 proactivity_match=1-abs(float(cand[3])-float(target[3]))
 return 1.8*personalization_match+2.2*cand[1]+2.2*cand[2]+1.3*proactivity_match+1.1*cand[4]

def generate(dataset,output,seed=17,split='train'):
 rng=random.Random(seed); recs=[r for r in load_jsonl(dataset) if r.split==split]; rows=[]
 for r in recs:
  t=target_behavior(r).tolist(); names=list(CANDIDATES); rng.shuffle(names)
  ranked=sorted(names,key=lambda n:utility(t,CANDIDATES[n]),reverse=True)
  for j in range(1,min(4,len(ranked))):
   rows.append({
      'conversation_id':r.conversation_id,'user_id':r.user_id,'query':r.current_query,
      'user_state':r.user_state,'chosen':{'name':ranked[0],'behavior':CANDIDATES[ranked[0]]},
      'rejected':{'name':ranked[j],'behavior':CANDIDATES[ranked[j]]},
      'provenance':'synthetic_pair','confidence':.9,
   })
 p=Path(output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(json.dumps(x) for x in rows)+'\n'); return {'pairs':len(rows),'output':str(p),'split':split}

def main():
 p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--output',required=True);p.add_argument('--split',default='train');a=p.parse_args();print(json.dumps(generate(a.dataset,a.output,split=a.split),indent=2))
if __name__=='__main__':main()
