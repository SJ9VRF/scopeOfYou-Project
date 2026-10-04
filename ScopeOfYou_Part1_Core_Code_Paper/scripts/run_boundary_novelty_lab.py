from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.dataio import load_jsonl
from personal_agi_pt.learned_policy import LearnedPersonalPolicy
from personal_agi_pt.boundary_opt import optimize as boundary_opt
from personal_agi_pt.eval import evaluate
from personal_agi_pt.counterfactual_eval import evaluate_counterfactual
from personal_agi_pt.statistics import paired_user_bootstrap

D=ROOT/'data/samples/personalbench_v31.jsonl'; S=ROOT/'checkpoints/sft_behavior_v31.pt'; R=ROOT/'checkpoints/reward_model_v31.pt'
RAW=ROOT/'checkpoints/post_trained_v31_raw.pt'; CON=ROOT/'checkpoints/post_trained_v31_constrained.pt'; B=ROOT/'checkpoints/post_trained_v31_boundary.pt'
metrics=boundary_opt(S,R,D,B,steps=120)
records=[x for x in load_jsonl(D) if x.split=='test']
policies={'sft':LearnedPersonalPolicy(S),'raw':LearnedPersonalPolicy(RAW),'constrained':LearnedPersonalPolicy(CON),'boundary':LearnedPersonalPolicy(B)}
regular={k:evaluate(records,p) for k,p in policies.items()}
cf={k:evaluate_counterfactual(records,p,policies['sft'] if k!='sft' else None) for k,p in policies.items()}
stats={'boundary_vs_raw': paired_user_bootstrap(records, policies['raw'], policies['boundary'], n_boot=2000, seed=71), 'boundary_vs_constrained': paired_user_bootstrap(records, policies['constrained'], policies['boundary'], n_boot=2000, seed=72)}
out={'method':'Boundary-Aware Temporal Personalized Optimization (BATPO)','optimization':metrics,
     'regular_test':{k:v['summary'] for k,v in regular.items()},
     'counterfactual_test':{k:v['summary'] for k,v in cf.items()},'bootstrap':stats,
     'notes':['Mutable dimensions: personalization/proactivity','Protected invariants: factuality/non-sycophancy','Confidence-scaled trust region','Counterfactual user-state swaps during optimization and evaluation']}
(ROOT/'reports/boundary_novelty_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
