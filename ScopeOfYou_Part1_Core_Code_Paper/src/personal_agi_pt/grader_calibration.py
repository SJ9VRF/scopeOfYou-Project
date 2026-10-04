from __future__ import annotations
import argparse, json, math
from pathlib import Path


def calibrate(rows: list[dict], human_key='human', grader_key='grader', threshold=0.5) -> dict:
    pairs=[]
    for r in rows:
        if human_key in r and grader_key in r:
            pairs.append((float(r[human_key]),float(r[grader_key])))
    if not pairs:
        return {'n':0,'mae':None,'rmse':None,'binary_accuracy':None,'false_positive_rate':None,'false_negative_rate':None}
    mae=sum(abs(h-g) for h,g in pairs)/len(pairs)
    rmse=math.sqrt(sum((h-g)**2 for h,g in pairs)/len(pairs))
    tp=tn=fp=fn=0
    for h,g in pairs:
        hb=h>=threshold; gb=g>=threshold
        if hb and gb: tp+=1
        elif (not hb) and (not gb): tn+=1
        elif (not hb) and gb: fp+=1
        else: fn+=1
    return {
        'n':len(pairs),'mae':mae,'rmse':rmse,'binary_accuracy':(tp+tn)/len(pairs),
        'false_positive_rate': fp/max(1,fp+tn),'false_negative_rate':fn/max(1,fn+tp),
        'threshold':threshold
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output');a=p.parse_args()
    rows=[json.loads(x) for x in Path(a.input).read_text().splitlines() if x.strip()]
    out=calibrate(rows);txt=json.dumps(out,indent=2)
    if a.output: Path(a.output).write_text(txt)
    print(txt)
if __name__=='__main__':main()
