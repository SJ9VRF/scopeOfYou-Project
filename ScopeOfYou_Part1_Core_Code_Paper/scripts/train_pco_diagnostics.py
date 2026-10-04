from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from personal_agi_pt.contract_opt import load_context,optimize_prepared
ctx=load_context(ROOT/'data/cache/contract_training_context.pt')
ablations={
  'full':{}, 'no_user_contract':{'user_weight':0.0}, 'no_context_contract':{'context_weight':0.0},
  'no_invariant_preservation':{'invariant_weight':0.0}, 'no_attack_training':{'attack_weight':0.0}, 'no_trust_region':{'beta':0.0},
}
for name,kw in ablations.items():
    ck=ROOT/f'checkpoints/pco_robust_ablation_{name}.pt'
    if not ck.exists():
        print('training',name,flush=True); optimize_prepared(ctx,ck,steps=20,seed=41,batch_size=128,**kw)
for scale in [0.0,.25,.5,1.0,1.5,2.0]:
    ck=ROOT/f'checkpoints/pco_robust_scale_{str(scale).replace(".","p")}.pt'
    if not ck.exists():
        print('training scale',scale,flush=True); optimize_prepared(ctx,ck,steps=20,seed=41,batch_size=128,user_weight=28*scale,context_weight=34*scale,invariant_weight=120*scale,attack_weight=45*scale)
print('done')
