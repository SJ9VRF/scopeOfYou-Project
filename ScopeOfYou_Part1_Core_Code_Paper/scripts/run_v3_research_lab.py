from __future__ import annotations
import json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.synthetic_users import generate_profiles, save_profiles
from personal_agi_pt.synthetic_dataset import generate_interactions_v3, save_jsonl
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
    t=time.perf_counter()
    dataset=ROOT/'data/samples/personalbench_v3.jsonl'
    profiles=generate_profiles(100,7); save_profiles(profiles,ROOT/'synthetic/user_profiles/profiles_v3.json')
    rows=generate_interactions_v3(profiles, interactions_per_user=60, drift_probability=.20, seed=47)
    save_jsonl(rows,dataset)
    quality=audit(dataset); (ROOT/'reports/data_quality_v3.json').write_text(json.dumps(quality,indent=2))

    sft_path=ROOT/'checkpoints/sft_behavior_v3.pt'
    rm_path=ROOT/'checkpoints/reward_model_v3.pt'
    raw_path=ROOT/'checkpoints/post_trained_v3_raw.pt'
    constrained_path=ROOT/'checkpoints/post_trained_v3_constrained.pt'
    sft=train_sft(dataset,sft_path,epochs=24,seed=13)
    pairs=gen_pairs(dataset,ROOT/'data/samples/preferences_v3.jsonl',split='train')
    rm=train_rm(ROOT/'data/samples/preferences_v3.jsonl',rm_path,epochs=16,seed=19)
    raw=raw_optimize(sft_path,rm_path,dataset,raw_path,steps=50,beta=.15,lr=8e-4)
    constrained=constrained_optimize(sft_path,rm_path,dataset,constrained_path,steps=80,beta=.5,anchor=4.0,lr=2e-4)

    recs=load_jsonl(dataset)
    test=[r for r in recs if r.split=='test']; val=[r for r in recs if r.split=='validation']
    sft_pol=LearnedPersonalPolicy(str(sft_path)); raw_pol=LearnedPersonalPolicy(str(raw_path)); con_pol=LearnedPersonalPolicy(str(constrained_path))
    results={
        'validation': {'sft':evaluate(val,sft_pol),'raw':evaluate(val,raw_pol),'constrained':evaluate(val,con_pol)},
        'test': {'sft':evaluate(test,sft_pol),'raw':evaluate(test,raw_pol),'constrained':evaluate(test,con_pol)},
    }
    stats={
        'sft_to_raw': paired_user_bootstrap(test,sft_pol,raw_pol,n_boot=2000,seed=101),
        'sft_to_constrained': paired_user_bootstrap(test,sft_pol,con_pol,n_boot=2000,seed=102),
    }
    fail_raw=mine(dataset,str(raw_path),ROOT/'reports/failures_v3_raw_test.jsonl',split='test')
    fail_con=mine(dataset,str(constrained_path),ROOT/'reports/failures_v3_constrained_test.jsonl',split='test')
    summary={
        'status':'complete','benchmark_version':'v3','examples':len(rows),'profiles':len(profiles),
        'quality':quality,'preference_pairs':pairs['pairs'],'sft_training':sft,'reward_model':rm,
        'raw_optimization':raw,'constrained_optimization':constrained,
        'test_summary':{k:v['summary'] for k,v in results['test'].items()},
        'bootstrap_test':stats,'raw_test_failures':fail_raw,'constrained_test_failures':fail_con,
        'wall_seconds':time.perf_counter()-t,
    }
    (ROOT/'reports/personalbench_v3_full_results.json').write_text(json.dumps(results,indent=2))
    (ROOT/'reports/personalbench_v3_statistics.json').write_text(json.dumps(stats,indent=2))
    (ROOT/'reports/personalbench_v3_summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
