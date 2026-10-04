from __future__ import annotations
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.synthetic_users import generate_profiles,save_profiles
from personal_agi_pt.synthetic_dataset import generate_interactions_v31,save_jsonl
from personal_agi_pt.data_quality import audit
from personal_agi_pt.train_sft import train as train_sft
from personal_agi_pt.preference_data import generate as gen_pairs
from personal_agi_pt.train_reward import train as train_rm
from personal_agi_pt.preference_opt import optimize as raw_optimize
from personal_agi_pt.constrained_opt import optimize as constrained_optimize
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.learned_policy import LearnedPersonalPolicy
from personal_agi_pt.eval import evaluate
from personal_agi_pt.statistics import paired_user_bootstrap
from personal_agi_pt.failure_miner import mine

def main():
 t=time.perf_counter(); dataset=ROOT/'data/samples/personalbench_v31.jsonl'
 profiles=generate_profiles(100,7);save_profiles(profiles,ROOT/'synthetic/user_profiles/profiles_v31.json')
 rows=generate_interactions_v31(profiles,60,.20,59);save_jsonl(rows,dataset)
 quality=audit(dataset);(ROOT/'reports/data_quality_v31.json').write_text(json.dumps(quality,indent=2))
 sft_p=ROOT/'checkpoints/sft_behavior_v31.pt'; rm_p=ROOT/'checkpoints/reward_model_v31.pt'; raw_p=ROOT/'checkpoints/post_trained_v31_raw.pt'; con_p=ROOT/'checkpoints/post_trained_v31_constrained.pt'
 sft=train_sft(dataset,sft_p,epochs=24,seed=13);pairs=gen_pairs(dataset,ROOT/'data/samples/preferences_v31.jsonl',split='train');rm=train_rm(ROOT/'data/samples/preferences_v31.jsonl',rm_p,epochs=16,seed=19)
 raw=raw_optimize(sft_p,rm_p,dataset,raw_p,steps=50,beta=.15,lr=8e-4);con=constrained_optimize(sft_p,rm_p,dataset,con_p,steps=80,beta=.5,anchor=4.0,lr=2e-4)
 recs=load_jsonl(dataset);test=[r for r in recs if r.split=='test'];val=[r for r in recs if r.split=='validation']
 ps,pr,pc=LearnedPersonalPolicy(str(sft_p)),LearnedPersonalPolicy(str(raw_p)),LearnedPersonalPolicy(str(con_p))
 results={'validation':{'sft':evaluate(val,ps),'raw':evaluate(val,pr),'constrained':evaluate(val,pc)},'test':{'sft':evaluate(test,ps),'raw':evaluate(test,pr),'constrained':evaluate(test,pc)}}
 stats={'sft_to_raw':paired_user_bootstrap(test,ps,pr,3000,201),'sft_to_constrained':paired_user_bootstrap(test,ps,pc,3000,202)}
 fail_raw=mine(dataset,str(raw_p),ROOT/'reports/failures_v31_raw_test.jsonl','test');fail_con=mine(dataset,str(con_p),ROOT/'reports/failures_v31_constrained_test.jsonl','test')
 summary={'status':'complete','benchmark_version':'v3.1','examples':len(rows),'profiles':len(profiles),'quality':quality,'preference_pairs':pairs['pairs'],'sft_training':sft,'reward_model':rm,'raw_optimization':raw,'constrained_optimization':con,'test_summary':{k:v['summary'] for k,v in results['test'].items()},'bootstrap_test':stats,'raw_test_failures':fail_raw,'constrained_test_failures':fail_con,'wall_seconds':time.perf_counter()-t}
 (ROOT/'reports/personalbench_v31_full_results.json').write_text(json.dumps(results,indent=2));(ROOT/'reports/personalbench_v31_statistics.json').write_text(json.dumps(stats,indent=2));(ROOT/'reports/personalbench_v31_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
