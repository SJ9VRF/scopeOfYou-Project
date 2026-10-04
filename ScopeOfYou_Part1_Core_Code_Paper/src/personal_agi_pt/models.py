from __future__ import annotations
import torch
from torch import nn

class BehaviorAdapter(nn.Module):
    def __init__(self,input_dim:int,hidden:int=96,out_dim:int=5):
        super().__init__(); self.net=nn.Sequential(nn.Linear(input_dim,hidden),nn.ReLU(),nn.LayerNorm(hidden),nn.Linear(hidden,out_dim))
    def forward(self,x): return torch.sigmoid(self.net(x))

class RewardModel(nn.Module):
    def __init__(self,input_dim:int,hidden:int=96):
        super().__init__(); self.net=nn.Sequential(nn.Linear(input_dim,hidden),nn.Tanh(),nn.Linear(hidden,1))
    def forward(self,x): return self.net(x).squeeze(-1)
