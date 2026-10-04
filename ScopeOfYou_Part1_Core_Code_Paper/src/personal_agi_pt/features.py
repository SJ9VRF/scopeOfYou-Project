from __future__ import annotations
import hashlib, re
from dataclasses import dataclass
from typing import Iterable
import torch
from .schema import InteractionRecord

STYLE = ['concise','balanced','detailed']
DIRECT = ['low','medium','high']
DEPTH = ['basic','intermediate','advanced']
CONFIRM = ['always','irreversible_only','minimal']
CORRECT = ['gentle','neutral','direct']

@dataclass
class FeatureEncoder:
    text_dim: int = 96
    def _bucket(self, tok: str) -> int:
        h=hashlib.blake2b(tok.encode(),digest_size=8).digest()
        return int.from_bytes(h,'little') % self.text_dim
    @property
    def dim(self): return self.text_dim + 3+3+3+3+3+1+5
    def encode(self, r: InteractionRecord) -> torch.Tensor:
        x=torch.zeros(self.dim,dtype=torch.float32)
        toks=re.findall(r"[a-z0-9+]+", (r.current_query+' '+' '.join(m.get('content','') for m in r.history)).lower())
        for t in toks: x[self._bucket(t)] += 1.0
        if toks: x[:self.text_dim] /= max(1.0, len(toks)**0.5)
        off=self.text_dim; st=r.user_state
        for vals,key in [(STYLE,'verbosity'),(DIRECT,'directness'),(DEPTH,'technical_depth'),(CONFIRM,'confirmation_policy'),(CORRECT,'correction_tolerance')]:
            v=st.get(key,vals[len(vals)//2]);
            if v in vals: x[off+vals.index(v)]=1
            off += len(vals)
        x[off]=float(st.get('proactivity',.5)); off+=1
        q=r.current_query.lower()
        flags=['capital of germany','2 + 2 = 5','deadline','forgot','delete','send email']
        for i,f in enumerate(flags[:5]): x[off+i]=float(f in q)
        return x

def target_behavior(r: InteractionRecord) -> torch.Tensor:
    # Kept as the public training API; target semantics live in targets.py.
    from .targets import behavior_target_tensor
    return behavior_target_tensor(r)
