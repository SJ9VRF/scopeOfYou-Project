from __future__ import annotations
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.synthetic_users import generate_profiles,save_profiles
from personal_agi_pt.synthetic_dataset import generate_interactions,save_jsonl
from personal_agi_pt.train_sft import train as train_sft
from personal_agi_pt.preference_data import generate as gen_pairs
from personal_agi_pt.train_reward import train as train_rm
from personal_agi_pt.preference_opt import optimize
from personal_agi_pt.compare import run as compare
from personal_agi_pt.failure_miner import mine
from personal_agi_pt.hard_case_generator import generate as gen_hard

def main():
 t=time.perf_counter();
 profiles=generate_profiles(100,7);save_profiles(profiles,ROOT/'synthetic/user_profiles/profiles_v1.json')
 rows=generate_interactions(profiles,interactions_per_user=50,drift_probability=.2,seed=11);save_jsonl(rows,ROOT/'data/samples/lab_v1.jsonl')
 sft=train_sft(ROOT/'data/samples/lab_v1.jsonl',ROOT/'checkpoints/sft_behavior.pt',epochs=24)
 pairs=gen_pairs(ROOT/'data/samples/lab_v1.jsonl',ROOT/'data/samples/preferences_v1.jsonl')
 rm=train_rm(ROOT/'data/samples/preferences_v1.jsonl',ROOT/'checkpoints/reward_model.pt',epochs=16)
 po=optimize(ROOT/'checkpoints/sft_behavior.pt',ROOT/'checkpoints/reward_model.pt',ROOT/'data/samples/lab_v1.jsonl',ROOT/'checkpoints/post_trained_behavior.pt',steps=50)
 comp=compare(ROOT/'data/samples/lab_v1.jsonl',ROOT/'checkpoints/sft_behavior.pt',ROOT/'checkpoints/post_trained_behavior.pt',ROOT/'reports/model_comparison.json')
 fails=mine(ROOT/'data/samples/lab_v1.jsonl',ROOT/'checkpoints/post_trained_behavior.pt',ROOT/'reports/failures.jsonl')
 hard=gen_hard(ROOT/'reports/failures.jsonl',ROOT/'data/samples/failure_mined_candidates.jsonl')
 summary={'status':'complete','dataset_examples':len(rows),'profiles':len(profiles),'preference_pairs':pairs['pairs'],'sft':sft,'reward_model':rm,'preference_optimization':po,'comparison':{k:v['summary'] for k,v in comp.items() if isinstance(v,dict) and 'summary' in v},'deltas_post_vs_sft':comp['deltas_post_vs_sft'],'failure_mining':fails,'hard_cases':hard,'wall_seconds':time.perf_counter()-t}
 (ROOT/'reports/full_lab_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
