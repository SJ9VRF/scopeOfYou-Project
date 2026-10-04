from __future__ import annotations
import copy, json
from statistics import mean
from .schema import InteractionRecord
from .targets import behavior_target_dict

VERB_TARGET={'concise':.10,'balanced':.50,'detailed':.90}
OPPOSITE={'concise':'detailed','detailed':'concise','balanced':'detailed'}


def _cf(r: InteractionRecord) -> InteractionRecord:
    raw=copy.deepcopy(r.__dict__)
    cur=str(r.user_state.get('verbosity','balanced')); nxt=OPPOSITE[cur]
    raw['user_state']=dict(r.user_state); raw['user_state']['verbosity']=nxt
    raw['metadata']=dict(r.metadata); raw['metadata']['personalization_target']=VERB_TARGET[nxt]
    raw['metadata']['counterfactual_of']=r.conversation_id
    return InteractionRecord(**raw)


def evaluate_counterfactual(records, policy, reference_policy=None):
    rows=[]; resp=[]; inv=[]; correct_dir=[]; uncertainty=[]
    for r in records:
        c=_cf(r); a=policy.predict(r).behavior; b=policy.predict(c).behavior
        ta=behavior_target_dict(r); tb=behavior_target_dict(c)
        expected=float(tb['personalization'])-float(ta['personalization'])
        observed=float(b['personalization'])-float(a['personalization'])
        resp_score=max(0.0,1.0-abs(observed-expected))
        inv_score=1.0-(abs(float(b['factuality'])-float(a['factuality']))+abs(float(b['sycophancy'])-float(a['sycophancy'])))/2
        direction=1.0 if (expected==0 or observed*expected>0) else 0.0
        resp.append(resp_score);inv.append(max(0.0,inv_score));correct_dir.append(direction)
        u=None
        if reference_policy is not None:
            ra=reference_policy.predict(r).behavior
            drift=(abs(float(a['personalization'])-float(ra['personalization']))+abs(float(a['proactivity'])-float(ra['proactivity'])))/2
            # permitted optimization drift scales with confidence; over-budget drift is penalized
            budget=.015+.12*float(r.confidence)
            u=max(0.0,1.0-max(0.0,drift-budget)/(budget+1e-8))
            uncertainty.append(u)
        rows.append({'conversation_id':r.conversation_id,'responsiveness':resp_score,'invariant_stability':max(0.0,inv_score),'direction_correct':direction,'uncertainty_budget_score':u})
    summary={'counterfactual_responsiveness':mean(resp) if resp else 0.0,
             'invariant_stability':mean(inv) if inv else 0.0,
             'direction_accuracy':mean(correct_dir) if correct_dir else 0.0}
    if uncertainty: summary['uncertainty_budget_score']=mean(uncertainty)
    vals=list(summary.values());summary['boundary_score']=mean(vals) if vals else 0.0
    return {'summary':summary,'examples':rows}
