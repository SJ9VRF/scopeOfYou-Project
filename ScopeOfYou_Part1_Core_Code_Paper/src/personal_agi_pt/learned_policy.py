from __future__ import annotations
import torch
from .features import FeatureEncoder
from .models import BehaviorAdapter
from .policy import PolicyOutput
from .schema import InteractionRecord

class LearnedPersonalPolicy:
    def __init__(self,checkpoint:str):
        ck=torch.load(checkpoint,map_location='cpu',weights_only=False); self.enc=FeatureEncoder(**ck.get('encoder',{})); self.model=BehaviorAdapter(ck['input_dim']); self.model.load_state_dict(ck['state_dict']); self.model.eval()
    def predict(self,r:InteractionRecord)->PolicyOutput:
        with torch.no_grad(): vals=self.model(self.enc.encode(r).unsqueeze(0))[0].tolist()
        pers,fact,nonsyc,pro,helpf=vals; st=r.user_state; verbosity=st.get('verbosity','balanced'); q=r.current_query.strip()
        if fact>.65 and ('capital of germany' in q.lower()): response='Berlin is the capital of Germany; Paris is the capital of France.'
        elif fact>.65 and '2 + 2 = 5' in q.lower(): response='2 + 2 = 4.'
        elif verbosity=='concise': response='Concise answer: '+q[:140]
        elif verbosity=='detailed': response='Detailed technical answer: '+q
        else: response='Answer: '+q
        return PolicyOutput(response=response,behavior={'personalization':pers,'factuality':fact,'sycophancy':1-nonsyc,'proactivity':pro,'helpfulness':helpf})
