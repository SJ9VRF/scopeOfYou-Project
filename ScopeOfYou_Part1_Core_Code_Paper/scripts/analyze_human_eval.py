from __future__ import annotations
import argparse,csv,json,math
from collections import Counter,defaultdict

def wilson(k,n,z=1.96):
    if n==0:return [None,None]
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [c-h,c+h]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--phase-a'); ap.add_argument('--phase-b'); ap.add_argument('--output',default='human_eval/analysis.json'); a=ap.parse_args(); out={}
    if a.phase_a:
        rows=list(csv.DictReader(open(a.phase_a,encoding='utf-8'))); by=defaultdict(list)
        for r in rows:
            if r.get('rater_label'): by[r['item_id']].append(r['rater_label'])
        complete={k:v for k,v in by.items() if len(v)>=2}; agree=[]
        for v in complete.values(): agree.append(Counter(v).most_common(1)[0][1]/len(v))
        out['phase_a']={'items_with_2plus_ratings':len(complete),'mean_majority_fraction':sum(agree)/len(agree) if agree else None,'note':'Use Krippendorff/Fleiss implementation in final statistical environment for confirmatory agreement.'}
    if a.phase_b:
        rows=list(csv.DictReader(open(a.phase_b,encoding='utf-8'))); vals=[r for r in rows if r.get('context_winner') in {'A','B','tie'}]
        a_w=sum(r['context_winner']=='A' for r in vals); b_w=sum(r['context_winner']=='B' for r in vals); denom=a_w+b_w
        out['phase_b']={'rated_pairs':len(vals),'A_wins':a_w,'B_wins':b_w,'A_win_rate_excluding_ties':a_w/denom if denom else None,'wilson95':wilson(a_w,denom)}
    open(a.output,'w',encoding='utf-8').write(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
