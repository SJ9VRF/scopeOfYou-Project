from __future__ import annotations
import argparse,json,random
from pathlib import Path

def generate(failures,output,copies=3,seed=23):
 rng=random.Random(seed); fs=[json.loads(x) for x in Path(failures).read_text().splitlines() if x.strip()];rows=[]
 for f in fs:
  for i in range(copies):
   q=f['query']; prefix=rng.choice(['Be precise. ','Given my current preference, ','Double-check before answering. '])
   rows.append({'source_failure':f['code'],'user_id':f['user_id'],'user_state':f['user_state'],'query':prefix+q,'provenance':'failure_mined','confidence':.75})
 p=Path(output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text('\n'.join(json.dumps(x) for x in rows)+ ('\n' if rows else ''));return {'generated':len(rows),'source_failures':len(fs)}
def main():
 p=argparse.ArgumentParser();p.add_argument('--failures',required=True);p.add_argument('--output',required=True);a=p.parse_args();print(json.dumps(generate(a.failures,a.output),indent=2))
if __name__=='__main__':main()
