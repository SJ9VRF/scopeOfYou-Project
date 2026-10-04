from __future__ import annotations
import argparse,json
from pathlib import Path
from .dataio import load_jsonl
from .learned_policy import LearnedPersonalPolicy
from .targets import behavior_target_dict


def mine(dataset, checkpoint, output, split="validation"):
    recs=[r for r in load_jsonl(dataset) if r.split==split]
    pol=LearnedPersonalPolicy(checkpoint); rows=[]; counts={}
    for r in recs:
        o=pol.predict(r); t=behavior_target_dict(r)
        tests=[
            ('PERS-01', abs(o.behavior['personalization']-t['personalization'])>.25),
            ('FACT-01', abs(o.behavior['factuality']-t['factuality'])>.20),
            ('BEH-01', abs(o.behavior['sycophancy']-t['sycophancy'])>.25),
            ('PRO-01', abs(o.behavior['proactivity']-t['proactivity'])>.25),
        ]
        for code,bad in tests:
            if bad:
                rows.append({
                    'code':code,'conversation_id':r.conversation_id,'user_id':r.user_id,
                    'query':r.current_query,'user_state':r.user_state,
                    'predicted_behavior':o.behavior,'target_behavior':t,
                    'metadata':r.metadata,
                }); counts[code]=counts.get(code,0)+1
    p=Path(output);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('\n'.join(json.dumps(x) for x in rows)+ ('\n' if rows else ''))
    summary={'failures':len(rows),'counts':counts,'split':split,'examples':len(recs)}
    p.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2)); return summary

def main():
 p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--output',required=True);p.add_argument('--split',default='validation');a=p.parse_args();print(json.dumps(mine(a.dataset,a.checkpoint,a.output,a.split),indent=2))
if __name__=='__main__':main()
