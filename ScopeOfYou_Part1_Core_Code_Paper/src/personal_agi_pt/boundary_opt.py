from __future__ import annotations
import argparse, json, copy, random
from pathlib import Path
import torch
from .dataio import load_jsonl
from .features import FeatureEncoder, target_behavior
from .models import BehaviorAdapter, RewardModel
from .schema import InteractionRecord

VERB = ['concise','balanced','detailed']


def _counterfactual(r: InteractionRecord, rng: random.Random) -> InteractionRecord:
    raw = copy.deepcopy(r.__dict__)
    # dataclass contains Feedback object; copy is enough for direct construction
    cur = str(r.user_state.get('verbosity','balanced'))
    options = [v for v in VERB if v != cur]
    nxt = rng.choice(options)
    raw['user_state'] = dict(r.user_state)
    raw['user_state']['verbosity'] = nxt
    raw['metadata'] = dict(r.metadata)
    raw['metadata']['personalization_target'] = {'concise':.10,'balanced':.50,'detailed':.90}[nxt]
    raw['metadata']['counterfactual_of'] = r.conversation_id
    return InteractionRecord(**raw)


def optimize(sft_checkpoint, reward_checkpoint, dataset, output, steps=100, beta=0.35,
             invariant_weight=100.0, cf_weight=24.0, mutable_anchor_weight=28.0, uncertainty_weight=3.0,
             lr=2e-4, seed=37):
    torch.manual_seed(seed); rng=random.Random(seed)
    s=torch.load(sft_checkpoint,map_location='cpu',weights_only=False)
    rr=torch.load(reward_checkpoint,map_location='cpu',weights_only=False)
    enc=FeatureEncoder(**s.get('encoder',{}))
    model=BehaviorAdapter(s['input_dim']); model.load_state_dict(s['state_dict'])
    ref=BehaviorAdapter(s['input_dim']); ref.load_state_dict(s['state_dict']); ref.eval()
    rm=RewardModel(rr['input_dim']); rm.load_state_dict(rr['state_dict']); rm.eval()
    recs=[r for r in load_jsonl(dataset) if r.split=='train']
    X=torch.stack([enc.encode(r) for r in recs]); Y=torch.stack([target_behavior(r) for r in recs])
    cf=[_counterfactual(r,rng) for r in recs]
    Xcf=torch.stack([enc.encode(r) for r in cf]); Ycf=torch.stack([target_behavior(r) for r in cf])
    confidence=torch.tensor([float(r.confidence) for r in recs],dtype=torch.float32).unsqueeze(1)
    # High-confidence user states allow more movement from reference; uncertain states get a tighter budget.
    budget=0.015 + 0.12*confidence
    opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=1e-4); hist=[]
    for step in range(steps):
        pred=model(X); pred_cf=model(Xcf)
        with torch.no_grad(): base=ref(X); base_cf=ref(Xcf)
        rewards=rm(torch.cat([X,pred.clamp(.03,.97)],dim=1))
        # Adaptive trust region: personalization changes must be earned by confidence.
        trust=(((pred-base)/budget)**2).mean()
        # Factuality + non-sycophancy are protected invariants. Helpfulness is softly protected.
        invariant=((pred[:,1:3]-Y[:,1:3])**2).mean() + .25*((pred[:,4]-Y[:,4])**2).mean()
        # Keep the base mutable controls grounded while the reward proposes improvements.
        mutable_anchor=((pred[:,0]-Y[:,0])**2).mean()+1.3*((pred[:,3]-Y[:,3])**2).mean()
        # Counterfactual user-state swap: mutable controls should follow the changed user state.
        mutable_cf=((pred_cf[:,0]-Ycf[:,0])**2).mean() + .6*((pred_cf[:,3]-Ycf[:,3])**2).mean()
        # Invariants should remain stable when only preference state changes.
        inv_cf=((pred_cf[:,1:3]-pred[:,1:3].detach())**2).mean()
        # Under low confidence, do not over-steer mutable dimensions away from the SFT reference.
        low_conf=(1-confidence.squeeze(1))
        uncertainty_guard=(low_conf*((pred[:,0]-base[:,0])**2 + (pred[:,3]-base[:,3])**2)).mean()
        loss=-rewards.mean()+beta*trust+invariant_weight*invariant+mutable_anchor_weight*mutable_anchor+cf_weight*(mutable_cf+4*inv_cf)+uncertainty_weight*uncertainty_guard
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),.5); opt.step()
        hist.append({'step':step+1,'loss':float(loss.detach()),'reward':float(rewards.mean().detach()),
                     'trust':float(trust.detach()),'invariant':float(invariant.detach()),
                     'mutable_anchor':float(mutable_anchor.detach()),'mutable_cf':float(mutable_cf.detach()),'inv_cf':float(inv_cf.detach()),
                     'uncertainty_guard':float(uncertainty_guard.detach())})
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':model.state_dict(),'input_dim':enc.dim,'encoder':{'text_dim':enc.text_dim},
                'history':hist,'backend':'boundary_aware_temporal_personalized_optimization',
                'method':{'mutable':['personalization','proactivity'],
                          'invariants':['factuality','non_sycophancy'],
                          'counterfactual_user_state_swaps':True,'confidence_scaled_trust_region':True}},out)
    m={'steps':steps,'checkpoint':str(out),**hist[-1]}
    out.with_suffix('.metrics.json').write_text(json.dumps(m,indent=2)); return m


def main():
    p=argparse.ArgumentParser(); p.add_argument('--sft',required=True);p.add_argument('--reward',required=True);p.add_argument('--dataset',required=True);p.add_argument('--output',required=True)
    a=p.parse_args(); print(json.dumps(optimize(a.sft,a.reward,a.dataset,a.output),indent=2))
if __name__=='__main__': main()
