from __future__ import annotations
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.synthetic_users import generate_profiles,save_profiles
from personal_agi_pt.synthetic_dataset import generate_interactions_v2,save_jsonl
from personal_agi_pt.data_quality import audit
from personal_agi_pt.train_sft import train as train_sft
from personal_agi_pt.preference_data import generate as gen_pairs
from personal_agi_pt.train_reward import train as train_rm
from personal_agi_pt.preference_opt import optimize
from personal_agi_pt.constrained_opt import optimize as constrained_optimize
from personal_agi_pt.compare import run as compare
from personal_agi_pt.failure_miner import mine
from personal_agi_pt.hard_case_generator import generate as gen_hard


def main():
    t=time.perf_counter()
    dataset=ROOT/'data/samples/lab_v2_clean.jsonl'
    profiles=generate_profiles(100,7);save_profiles(profiles,ROOT/'synthetic/user_profiles/profiles_v2.json')
    rows=generate_interactions_v2(profiles,interactions_per_user=50,drift_probability=.2,seed=31);save_jsonl(rows,dataset)
    quality=audit(dataset); (ROOT/'reports/data_quality_v2.json').write_text(json.dumps(quality,indent=2))
    sft=train_sft(dataset,ROOT/'checkpoints/sft_behavior_v2.pt',epochs=24)
    pairs=gen_pairs(dataset,ROOT/'data/samples/preferences_v2.jsonl')
    rm=train_rm(ROOT/'data/samples/preferences_v2.jsonl',ROOT/'checkpoints/reward_model_v2.pt',epochs=16)
    raw=optimize(ROOT/'checkpoints/sft_behavior_v2.pt',ROOT/'checkpoints/reward_model_v2.pt',dataset,ROOT/'checkpoints/post_trained_v2_raw.pt',steps=50)
    comp_raw=compare(dataset,ROOT/'checkpoints/sft_behavior_v2.pt',ROOT/'checkpoints/post_trained_v2_raw.pt',ROOT/'reports/model_comparison_v2_raw.json')
    fail_raw=mine(dataset,ROOT/'checkpoints/post_trained_v2_raw.pt',ROOT/'reports/failures_v2_raw.jsonl')
    constrained=constrained_optimize(ROOT/'checkpoints/sft_behavior_v2.pt',ROOT/'checkpoints/reward_model_v2.pt',dataset,ROOT/'checkpoints/post_trained_v2_constrained.pt')
    comp_c=compare(dataset,ROOT/'checkpoints/sft_behavior_v2.pt',ROOT/'checkpoints/post_trained_v2_constrained.pt',ROOT/'reports/model_comparison_v2_constrained.json')
    fail_c=mine(dataset,ROOT/'checkpoints/post_trained_v2_constrained.pt',ROOT/'reports/failures_v2_constrained.jsonl')
    hard=gen_hard(ROOT/'reports/failures_v2_raw.jsonl',ROOT/'data/samples/failure_mined_v2.jsonl')
    summary={
      'status':'complete','dataset':'lab_v2_clean','examples':len(rows),'profiles':len(profiles),
      'data_quality':quality,'preference_pairs':pairs['pairs'],'sft':sft,'reward_model':rm,
      'unconstrained':raw,'constrained':constrained,
      'raw_deltas':comp_raw['deltas_post_vs_sft'],'constrained_deltas':comp_c['deltas_post_vs_sft'],
      'raw_failures':fail_raw,'constrained_failures':fail_c,'hard_cases':hard,'wall_seconds':time.perf_counter()-t
    }
    (ROOT/'reports/full_lab_v2_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
