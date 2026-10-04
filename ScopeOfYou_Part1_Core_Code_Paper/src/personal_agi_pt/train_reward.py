from __future__ import annotations
import argparse,json,random
from pathlib import Path
import torch
from torch.utils.data import DataLoader,TensorDataset
from .schema import InteractionRecord,Feedback
from .features import FeatureEncoder
from .models import RewardModel

def _rec(row):
 return InteractionRecord(conversation_id=row['conversation_id'],user_id=row['user_id'],user_state=row['user_state'],history=[],current_query=row['query'],candidate_response='',feedback=Feedback(),provenance='synthetic')
def train(pairs_path,output,epochs=20,seed=19):
 torch.manual_seed(seed); random.seed(seed); enc=FeatureEncoder(); rows=[json.loads(x) for x in Path(pairs_path).read_text().splitlines() if x.strip()]
 def feat(row,which): return torch.cat([enc.encode(_rec(row)),torch.tensor(row[which]['behavior'],dtype=torch.float32)])
 XC=torch.stack([feat(r,'chosen') for r in rows]); XR=torch.stack([feat(r,'rejected') for r in rows]);
 model=RewardModel(enc.dim+5);opt=torch.optim.AdamW(model.parameters(),lr=3e-3);dl=DataLoader(TensorDataset(XC,XR),batch_size=min(128,len(rows)),shuffle=True);hist=[]
 for ep in range(epochs):
  ls=[];correct=0;n=0
  for c,r in dl:
   opt.zero_grad(); sc,sr=model(c),model(r); loss=-torch.nn.functional.logsigmoid(sc-sr).mean();loss.backward();opt.step();ls.append(loss.item());correct += int((sc>sr).sum());n+=len(c)
  hist.append({'epoch':ep+1,'loss':sum(ls)/len(ls),'train_pair_accuracy':correct/n})
 out=Path(output);out.parent.mkdir(parents=True,exist_ok=True);torch.save({'state_dict':model.state_dict(),'input_dim':enc.dim+5,'encoder':{'text_dim':enc.text_dim},'history':hist},out)
 metrics={'pairs':len(rows),'final_pair_accuracy':hist[-1]['train_pair_accuracy'],'checkpoint':str(out)};out.with_suffix('.metrics.json').write_text(json.dumps(metrics,indent=2));return metrics
def main():
 p=argparse.ArgumentParser();p.add_argument('--pairs',required=True);p.add_argument('--output',required=True);p.add_argument('--epochs',type=int,default=20);a=p.parse_args();print(json.dumps(train(a.pairs,a.output,a.epochs),indent=2))
if __name__=='__main__':main()
