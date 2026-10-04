from __future__ import annotations
import argparse,json
from pathlib import Path
import torch
from .dataio import load_jsonl
from .features import FeatureEncoder,target_behavior
from .models import BehaviorAdapter,RewardModel

def optimize(sft_checkpoint,reward_checkpoint,dataset,output,steps=80,beta=.5,anchor=4.0,lr=2e-4):
    s=torch.load(sft_checkpoint,map_location='cpu',weights_only=False); r=torch.load(reward_checkpoint,map_location='cpu',weights_only=False)
    enc=FeatureEncoder(**s.get('encoder',{})); model=BehaviorAdapter(s['input_dim']); model.load_state_dict(s['state_dict'])
    ref=BehaviorAdapter(s['input_dim']); ref.load_state_dict(s['state_dict']); ref.eval()
    rm=RewardModel(r['input_dim']); rm.load_state_dict(r['state_dict']); rm.eval()
    recs=[x for x in load_jsonl(dataset) if x.split=='train']; X=torch.stack([enc.encode(x) for x in recs]); Y=torch.stack([target_behavior(x) for x in recs])
    opt=torch.optim.AdamW(model.parameters(),lr=lr); hist=[]
    for step in range(steps):
        pred=model(X)
        with torch.no_grad(): base=ref(X)
        # Critical defense against RM extrapolation: score only within calibrated behavior domain.
        rm_in=torch.cat([X,pred.clamp(.05,.95)],dim=1); rewards=rm(rm_in)
        ref_pen=((pred-base)**2).mean(); anchor_loss=((pred-Y)**2).mean()
        # factuality/non-sycophancy are hard-ish anchors (indices 1,2)
        invariants=((pred[:,1:4]-Y[:,1:4])**2).mean()
        loss=-rewards.mean()+beta*ref_pen+anchor*anchor_loss+120.0*invariants
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),.5); opt.step()
        hist.append({'step':step+1,'loss':loss.detach().item(),'reward':rewards.detach().mean().item(),'reference_penalty':ref_pen.detach().item(),'anchor_loss':anchor_loss.detach().item(),'invariant_loss':invariants.detach().item()})
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':model.state_dict(),'input_dim':enc.dim,'encoder':{'text_dim':enc.text_dim},'history':hist,'backend':'constrained_reward_guided_optimization'},out)
    m={'steps':steps,'final_reward':hist[-1]['reward'],'reference_penalty':hist[-1]['reference_penalty'],'anchor_loss':hist[-1]['anchor_loss'],'checkpoint':str(out)}
    out.with_suffix('.metrics.json').write_text(json.dumps(m,indent=2)); return m

def main():
 p=argparse.ArgumentParser(); p.add_argument('--sft',required=True);p.add_argument('--reward',required=True);p.add_argument('--dataset',required=True);p.add_argument('--output',required=True);a=p.parse_args();print(json.dumps(optimize(a.sft,a.reward,a.dataset,a.output),indent=2))
if __name__=='__main__':main()
