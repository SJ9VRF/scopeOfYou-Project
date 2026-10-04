from __future__ import annotations
import json
from pathlib import Path
from statistics import mean, pstdev
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; REPORTS=ROOT/'reports'; FIGS=ROOT/'paper'/'figures'; FIGS.mkdir(parents=True,exist_ok=True)
summary=json.loads((REPORTS/'personalbench_v31_summary.json').read_text())
results=json.loads((REPORTS/'personalbench_v31_full_results.json').read_text())
abl=json.loads((REPORTS/'personalbench_v31_ablations.json').read_text())
models={k:v['summary'] for k,v in results['test'].items()}
metrics=['personalization','factuality','sycophancy','proactivity','personalbench_mean']
labels=['Personalization','Factuality','Non-sycophancy','Proactivity','PersonalBench']
pretty={'sft':'SFT','raw':'Unconstrained','constrained':'Constrained'}

fig,ax=plt.subplots(figsize=(9.5,5));x=range(len(labels));w=.24
for i,(name,vals) in enumerate(models.items()):
 ax.bar([j+(i-1)*w for j in x],[vals[m] for m in metrics],width=w,label=pretty[name])
ax.set_xticks(list(x),labels,rotation=12,ha='right');ax.set_ylim(0,1.03);ax.set_ylabel('Held-out test score');ax.set_title('PersonalBench v3.1: held-out-user behavior');ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(FIGS/'main_results.png',dpi=220);plt.close(fig)

raw=summary['raw_test_failures'];con=summary['constrained_test_failures'];cats=['PERS-01','PRO-01','Total'];rv=[raw['counts'].get('PERS-01',0),raw['counts'].get('PRO-01',0),raw['failures']];cv=[con['counts'].get('PERS-01',0),con['counts'].get('PRO-01',0),con['failures']]
fig,ax=plt.subplots(figsize=(7.6,4.6));x=range(3);ax.bar([i-.18 for i in x],rv,.36,label='Unconstrained');ax.bar([i+.18 for i in x],cv,.36,label='Constrained');ax.set_xticks(list(x),cats);ax.set_ylabel('Threshold violations');ax.set_title('Failure repair on 1,200 held-out test interactions');ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(FIGS/'failure_repair.png',dpi=220);plt.close(fig)

base=models['sft'];fig,ax=plt.subplots(figsize=(8.8,4.6));x=range(len(labels));rd=[models['raw'][m]-base[m] for m in metrics];cd=[models['constrained'][m]-base[m] for m in metrics];ax.axhline(0,linewidth=1);ax.bar([i-.18 for i in x],rd,.36,label='Unconstrained - SFT');ax.bar([i+.18 for i in x],cd,.36,label='Constrained - SFT');ax.set_xticks(list(x),labels,rotation=12,ha='right');ax.set_ylabel('Absolute score delta');ax.set_title('Regression profile relative to SFT');ax.legend();ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(FIGS/'deltas_vs_sft.png',dpi=220);plt.close(fig)

# Data-scaling curve: mean +/- population std across seeds.
by={}
for r in abl['data_scale']: by.setdefault(r['fraction'],[]).append(r['test']['personalbench_mean'])
xs=sorted(by);ys=[mean(by[x]) for x in xs];es=[pstdev(by[x]) for x in xs]
fig,ax=plt.subplots(figsize=(7.6,4.5));ax.errorbar([x*100 for x in xs],ys,yerr=es,marker='o',capsize=4);ax.set_xlabel('Training data used (%)');ax.set_ylabel('Held-out PersonalBench');ax.set_title('Data scaling across three random seeds');ax.set_ylim(.94,1.0);ax.grid(alpha=.2);fig.tight_layout();fig.savefig(FIGS/'data_scaling.png',dpi=220);plt.close(fig)

# Optimization sensitivity.
fig,ax=plt.subplots(figsize=(7.6,4.5));xb=[r['beta'] for r in abl['raw_beta']];yb=[r['test']['personalbench_mean'] for r in abl['raw_beta']];xa=[r['anchor'] for r in abl['constraint_anchor']];ya=[r['test']['personalbench_mean'] for r in abl['constraint_anchor']];ax.plot(xb,yb,marker='o',label='Unconstrained: beta sweep');ax.plot(xa,ya,marker='o',label='Constrained: anchor sweep');ax.set_xscale('log');ax.set_ylabel('Held-out PersonalBench');ax.set_xlabel('Regularization / anchor coefficient (log scale)');ax.set_title('Reward optimization sensitivity');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(FIGS/'optimization_sensitivity.png',dpi=220);plt.close(fig)

paper_results={'benchmark':'PersonalBench v3.1','examples':summary['examples'],'profiles':summary['profiles'],'split_counts':summary['quality']['split_counts'],'preference_pairs':summary['preference_pairs'],'models':models,'bootstrap_test':summary['bootstrap_test'],'failures':{'raw':raw,'constrained':con},'ablations':abl}
(REPORTS/'paper_results.json').write_text(json.dumps(paper_results,indent=2))
print(json.dumps({'figures':5,'benchmark':'v3.1'},indent=2))
