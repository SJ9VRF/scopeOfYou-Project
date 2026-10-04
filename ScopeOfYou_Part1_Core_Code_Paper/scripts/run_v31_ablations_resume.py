from __future__ import annotations
import json,random,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.synthetic_users import generate_profiles
from personal_agi_pt.synthetic_dataset import generate_interactions_v31,save_jsonl
from personal_agi_pt.train_sft import train as train_sft
from personal_agi_pt.learned_policy import LearnedPersonalPolicy
from personal_agi_pt.eval import evaluate
from personal_agi_pt.preference_opt import optimize as raw_opt
from personal_agi_pt.constrained_opt import optimize as con_opt
DATA=ROOT/'data/samples/personalbench_v31.jsonl';SFT=ROOT/'checkpoints/sft_behavior_v31.pt';RM=ROOT/'checkpoints/reward_model_v31.pt'

def write_subset(recs,frac,seed,path):
 tr=[r for r in recs if r.split=='train'];other=[r for r in recs if r.split!='train'];rng=random.Random(seed);rng.shuffle(tr);keep=tr[:max(1,int(len(tr)*frac))]
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('w') as f:
  for r in keep+other:
   raw=r.__dict__.copy();raw['feedback']=r.feedback.__dict__;f.write(json.dumps(raw)+'\n')
 return len(keep)
def score(ck):
 recs=[r for r in load_jsonl(DATA) if r.split=='test'];return evaluate(recs,LearnedPersonalPolicy(str(ck)))['summary']
def main():
 t=time.perf_counter();recs=load_jsonl(DATA);out={'data_scale':[],'drift':[],'raw_beta':[],'constraint_anchor':[]}
 for frac in [.10,.25,.50,1.0]:
  for seed in [11,13,17]:
   ds=ROOT/f'experiments/data_scale/dataset_f{int(frac*100)}_s{seed}.jsonl';n=write_subset(recs,frac,seed,ds)
   ck=ROOT/f'experiments/data_scale/sft_f{int(frac*100)}_s{seed}.pt'
   if not ck.exists():train_sft(ds,ck,epochs=10,seed=seed)
   m=json.loads(ck.with_suffix('.metrics.json').read_text())
   out['data_scale'].append({'fraction':frac,'seed':seed,'train_examples':n,'best_val_mse':m['best_val_mse'],'test':score(ck)})
 profiles=generate_profiles(100,7);nodrift=ROOT/'experiments/drift/no_drift.jsonl';ck=ROOT/'experiments/drift/sft_no_drift.pt'
 if not ck.exists():save_jsonl(generate_interactions_v31(profiles,60,0.0,59),nodrift);train_sft(nodrift,ck,epochs=12,seed=13)
 out['drift']=[{'train_drift_probability':0.0,'test':score(ck)},{'train_drift_probability':0.2,'test':score(SFT)}]
 for beta in [.05,.15,.5,2.0]:
  ck=ROOT/f'experiments/raw_beta/post_beta_{str(beta).replace(".","p")}.pt';ck.parent.mkdir(parents=True,exist_ok=True)
  if not ck.exists():raw_opt(SFT,RM,DATA,ck,steps=25,beta=beta,lr=8e-4)
  out['raw_beta'].append({'beta':beta,'test':score(ck)})
 for anchor in [1.0,4.0,12.0]:
  ck=ROOT/f'experiments/constraint_anchor/post_anchor_{str(anchor).replace(".","p")}.pt';ck.parent.mkdir(parents=True,exist_ok=True)
  if not ck.exists():con_opt(SFT,RM,DATA,ck,steps=35,beta=.5,anchor=anchor,lr=2e-4)
  out['constraint_anchor'].append({'anchor':anchor,'test':score(ck)})
 out['wall_seconds_this_resume']=time.perf_counter()-t
 (ROOT/'reports/personalbench_v31_ablations.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
