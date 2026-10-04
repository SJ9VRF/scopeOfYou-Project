from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
import torch
from .dataio import load_jsonl
from .features import FeatureEncoder, target_behavior
from .models import BehaviorAdapter, RewardModel
from .contract_eval import user_swap, history_preference_swap, context_swap, invariant_attack

@dataclass
class ContractTrainingContext:
    enc: FeatureEncoder
    X: torch.Tensor
    Y: torch.Tensor
    Xus: torch.Tensor
    Yus: torch.Tensor
    Xuh: torch.Tensor
    Yuh: torch.Tensor
    Xuh2: torch.Tensor
    Xcs: torch.Tensor
    Xcs2: torch.Tensor
    Xca: torch.Tensor
    Xca2: torch.Tensor
    Yca: torch.Tensor
    Xia: torch.Tensor
    budget: torch.Tensor
    sft_state: dict
    reward_state: dict
    sft_input_dim: int
    reward_input_dim: int


def prepare_context(sft_checkpoint, reward_checkpoint, dataset) -> ContractTrainingContext:
    s=torch.load(sft_checkpoint,map_location='cpu',weights_only=False)
    rr=torch.load(reward_checkpoint,map_location='cpu',weights_only=False)
    enc=FeatureEncoder(**s.get('encoder',{}))
    recs=[r for r in load_jsonl(dataset) if r.split=='train']
    X=torch.stack([enc.encode(r) for r in recs]); Y=torch.stack([target_behavior(r) for r in recs])
    us=[user_swap(r) for r in recs]; Xus=torch.stack([enc.encode(r) for r in us]); Yus=torch.stack([target_behavior(r) for r in us])
    uh=[history_preference_swap(r) for r in recs]; Xuh=torch.stack([enc.encode(r) for r in uh]); Yuh=torch.stack([target_behavior(r) for r in uh])
    uh2=[history_preference_swap(r,variant=i+1) for i,r in enumerate(recs)]; Xuh2=torch.stack([enc.encode(r) for r in uh2])
    cs=[context_swap(r, True) for r in recs]; Xcs=torch.stack([enc.encode(r) for r in cs])
    cs2=[context_swap(r, True, variant=i+1) for i,r in enumerate(recs)]; Xcs2=torch.stack([enc.encode(r) for r in cs2])
    ca=[context_swap(r, False) for r in recs]; Xca=torch.stack([enc.encode(r) for r in ca]); Yca=torch.stack([target_behavior(r) for r in ca])
    ca2=[context_swap(r, False, variant=i+1) for i,r in enumerate(recs)]; Xca2=torch.stack([enc.encode(r) for r in ca2])
    ia=[invariant_attack(r) for r in recs]; Xia=torch.stack([enc.encode(r) for r in ia])
    conf=torch.tensor([float(r.confidence) for r in recs],dtype=torch.float32).unsqueeze(1)
    budget=.012+.10*conf
    return ContractTrainingContext(enc,X,Y,Xus,Yus,Xuh,Yuh,Xuh2,Xcs,Xcs2,Xca,Xca2,Yca,Xia,budget,s['state_dict'],rr['state_dict'],s['input_dim'],rr['input_dim'])



def save_context(ctx: ContractTrainingContext, path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    torch.save({
        'encoder': {'text_dim': ctx.enc.text_dim}, 'X':ctx.X,'Y':ctx.Y,'Xus':ctx.Xus,'Yus':ctx.Yus,
        'Xuh':ctx.Xuh,'Yuh':ctx.Yuh,'Xuh2':ctx.Xuh2,'Xcs':ctx.Xcs,'Xcs2':ctx.Xcs2,'Xca':ctx.Xca,'Xca2':ctx.Xca2,'Yca':ctx.Yca,'Xia':ctx.Xia,'budget':ctx.budget,
        'sft_state':ctx.sft_state,'reward_state':ctx.reward_state,'sft_input_dim':ctx.sft_input_dim,'reward_input_dim':ctx.reward_input_dim
    },path)

def load_context(path):
    z=torch.load(path,map_location='cpu',weights_only=False); enc=FeatureEncoder(**z['encoder'])
    return ContractTrainingContext(enc,z['X'],z['Y'],z['Xus'],z['Yus'],z['Xuh'],z['Yuh'],z['Xuh2'],z['Xcs'],z['Xcs2'],z['Xca'],z['Xca2'],z['Yca'],z['Xia'],z['budget'],z['sft_state'],z['reward_state'],z['sft_input_dim'],z['reward_input_dim'])

def optimize_prepared(ctx: ContractTrainingContext, output, steps=120, lr=2e-4, beta=0.40,
             user_weight=28.0, context_weight=34.0, invariant_weight=120.0, attack_weight=45.0,
             seed=41, batch_size=None, consistency_weight=0.0):
    torch.manual_seed(seed)
    model=BehaviorAdapter(ctx.sft_input_dim); model.load_state_dict(ctx.sft_state)
    ref=BehaviorAdapter(ctx.sft_input_dim); ref.load_state_dict(ctx.sft_state); ref.eval()
    rm=RewardModel(ctx.reward_input_dim); rm.load_state_dict(ctx.reward_state); rm.eval()
    X,Y,Xus,Yus,Xuh,Yuh,Xuh2,Xcs,Xcs2,Xca,Xca2,Yca,Xia,budget = ctx.X,ctx.Y,ctx.Xus,ctx.Yus,ctx.Xuh,ctx.Yuh,ctx.Xuh2,ctx.Xcs,ctx.Xcs2,ctx.Xca,ctx.Xca2,ctx.Yca,ctx.Xia,ctx.budget
    opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=1e-4); hist=[]
    n=X.shape[0]; g=torch.Generator().manual_seed(seed+1009)
    for step in range(steps):
        if batch_size is not None and batch_size < n:
            idx=torch.randint(0,n,(int(batch_size),),generator=g)
            xb,yb,xusb,yusb,xuhb,yuhb,xuh2b,xcsb,xcs2b,xcab,xca2b,ycab,xiab,bbudget = X[idx],Y[idx],Xus[idx],Yus[idx],Xuh[idx],Yuh[idx],Xuh2[idx],Xcs[idx],Xcs2[idx],Xca[idx],Xca2[idx],Yca[idx],Xia[idx],budget[idx]
        else:
            xb,yb,xusb,yusb,xuhb,yuhb,xuh2b,xcsb,xcs2b,xcab,xca2b,ycab,xiab,bbudget = X,Y,Xus,Yus,Xuh,Yuh,Xuh2,Xcs,Xcs2,Xca,Xca2,Yca,Xia,budget
        p=model(xb); pus=model(xusb); puh=model(xuhb); puh2=model(xuh2b); pcs=model(xcsb); pcs2=model(xcs2b); pca=model(xcab); pca2=model(xca2b); pia=model(xiab)
        with torch.no_grad(): b=ref(xb)
        rew=rm(torch.cat([xb,p.clamp(.03,.97)],1))
        trust=(((p-b)/bbudget)**2).mean(); base_anchor=((p-yb)**2).mean()
        user_mut=((pus[:,0]-yusb[:,0])**2).mean()+((puh[:,0]-yuhb[:,0])**2).mean(); user_inv=((pus[:,1:3]-p[:,1:3].detach())**2).mean()
        context=((pcs[:,3]-.10)**2).mean()+((pca[:,3]-ycab[:,3])**2).mean()
        attack=((pia[:,1]-1.0)**2).mean()+((pia[:,2]-1.0)**2).mean()
        invariants=((p[:,1:3]-yb[:,1:3])**2).mean()
        consistency=((puh[:,0]-puh2[:,0])**2).mean()+((pcs[:,3]-pcs2[:,3])**2).mean()+((pca[:,3]-pca2[:,3])**2).mean()
        loss=-rew.mean()+beta*trust+12.0*base_anchor+user_weight*(user_mut+4*user_inv)+context_weight*context+invariant_weight*invariants+attack_weight*attack+consistency_weight*consistency
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),.5); opt.step()
        hist.append({'step':step+1,'loss':float(loss.detach()),'reward':float(rew.mean().detach()),'trust':float(trust.detach()),
                     'base_anchor':float(base_anchor.detach()),'user_mut':float(user_mut.detach()),'user_inv':float(user_inv.detach()),
                     'context':float(context.detach()),'attack':float(attack.detach()),'invariants':float(invariants.detach()),'consistency':float(consistency.detach())})
    out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':model.state_dict(),'input_dim':ctx.enc.dim,'encoder':{'text_dim':ctx.enc.text_dim},'history':hist,
                'backend':'personalization_contract_optimization','batch_size':batch_size,'method':{'contracts':['apply','suppress','must_not_affect'],
                'interventions':['user_state_swap','context_swap','invariant_attack'],'temporal_state_compatible':True}},out)
    met={'steps':steps,'checkpoint':str(out),**hist[-1]}; out.with_suffix('.metrics.json').write_text(json.dumps(met,indent=2)); return met


def optimize(sft_checkpoint, reward_checkpoint, dataset, output, **kwargs):
    return optimize_prepared(prepare_context(sft_checkpoint,reward_checkpoint,dataset), output, **kwargs)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--sft',required=True); p.add_argument('--reward',required=True); p.add_argument('--dataset',required=True); p.add_argument('--output',required=True)
    a=p.parse_args(); print(json.dumps(optimize(a.sft,a.reward,a.dataset,a.output),indent=2))
if __name__=='__main__': main()
