from __future__ import annotations
import argparse,json,random
from pathlib import Path
import torch
from torch.utils.data import DataLoader,TensorDataset
from .dataio import load_jsonl
from .features import FeatureEncoder,target_behavior
from .models import BehaviorAdapter

def train(dataset,output,epochs=30,lr=3e-3,seed=13):
    random.seed(seed); torch.manual_seed(seed)
    recs=load_jsonl(dataset); enc=FeatureEncoder()
    train=[r for r in recs if r.split=='train']; val=[r for r in recs if r.split=='validation'] or train[-max(1,len(train)//5):]
    X=torch.stack([enc.encode(r) for r in train]); Y=torch.stack([target_behavior(r) for r in train])
    model=BehaviorAdapter(enc.dim); opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=1e-4); lossfn=torch.nn.MSELoss()
    hist=[]
    dl=DataLoader(TensorDataset(X,Y),batch_size=min(128,len(X)),shuffle=True)
    best=1e9; best_state=None
    for ep in range(epochs):
        model.train(); ls=[]
        for xb,yb in dl:
            opt.zero_grad(); pred=model(xb); loss=lossfn(pred,yb); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step(); ls.append(loss.item())
        model.eval()
        with torch.no_grad():
            VX=torch.stack([enc.encode(r) for r in val]); VY=torch.stack([target_behavior(r) for r in val]); vl=lossfn(model(VX),VY).item()
        hist.append({'epoch':ep+1,'train_loss':sum(ls)/len(ls),'val_loss':vl})
        if vl<best: best=vl; best_state={k:v.detach().clone() for k,v in model.state_dict().items()}
    model.load_state_dict(best_state); out=Path(output); out.parent.mkdir(parents=True,exist_ok=True)
    torch.save({'state_dict':model.state_dict(),'input_dim':enc.dim,'encoder':{'text_dim':enc.text_dim},'history':hist,'backend':'torch_behavior_adapter'},out)
    metrics={'backend':'torch_behavior_adapter','train_examples':len(train),'validation_examples':len(val),'best_val_mse':best,'epochs':epochs,'checkpoint':str(out)}
    out.with_suffix('.metrics.json').write_text(json.dumps(metrics,indent=2)); return metrics

def main():
 p=argparse.ArgumentParser(); p.add_argument('--dataset',required=True); p.add_argument('--output',required=True); p.add_argument('--epochs',type=int,default=30); a=p.parse_args(); print(json.dumps(train(a.dataset,a.output,a.epochs),indent=2))
if __name__=='__main__': main()
