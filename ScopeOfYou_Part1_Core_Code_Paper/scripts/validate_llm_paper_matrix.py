import json,sys
from pathlib import Path
p=Path('configs/llm_paper/matrix.json'); x=json.loads(p.read_text())
errors=[]
if len(x.get('backbones',[]))<2: errors.append('need >=2 backbones')
if len(x.get('seeds',[]))<3: errors.append('need >=3 seeds')
for m in ['sft_personalization','dpo_personalization','pco_robust']:
    if m not in x.get('methods',[]): errors.append('missing '+m)
for e in ['ContractBench-Implicit','BenchPreS','Personalized RewardBench']:
    if e not in x.get('required_evaluations',[]): errors.append('missing '+e)
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f"LLM paper matrix validated: {len(x['backbones'])} backbones x {len(x['seeds'])} seeds, {len(x['methods'])} method slots.")
