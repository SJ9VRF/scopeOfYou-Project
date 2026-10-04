from pathlib import Path
import torch
from personal_agi_pt.features import FeatureEncoder,target_behavior
from personal_agi_pt.models import BehaviorAdapter,RewardModel
from personal_agi_pt.dataio import load_jsonl

def test_feature_encoder_dimensions():
 r=load_jsonl('data/samples/seed.jsonl')[0]; e=FeatureEncoder(); assert e.encode(r).shape==(e.dim,)
def test_behavior_adapter_bounded():
 m=BehaviorAdapter(120); y=m(torch.randn(4,120)); assert y.shape==(4,5); assert bool(((y>=0)&(y<=1)).all())
def test_target_dimensions():
 r=load_jsonl('data/samples/seed.jsonl')[0]; assert target_behavior(r).shape==(5,)
def test_reward_model_pair_shape():
 m=RewardModel(125); assert m(torch.randn(7,125)).shape==(7,)
