from personal_agi_pt.contract_eval import evaluate_contract
from personal_agi_pt.schema import InteractionRecord, Feedback
from personal_agi_pt.policy import PolicyOutput

class ContractPolicy:
    def predict(self,r):
        v={'concise':.1,'balanced':.5,'detailed':.9}[r.user_state.get('verbosity','balanced')]
        q=r.current_query.lower()
        pro=.1 if r.metadata.get('contract_intervention')=='context_suppress' else float(r.metadata.get('proactivity_target',r.user_state.get('proactivity',.5)))
        return PolicyOutput(response='',behavior={'personalization':v,'factuality':1.0,'sycophancy':0.0,'proactivity':pro,'helpfulness':1.0})

def test_contract_policy_scores_high():
    r=InteractionRecord(conversation_id='c',user_id='u',user_state={'verbosity':'concise','proactivity':.8},history=[],current_query='Explain x',candidate_response='y',feedback=Feedback(factuality=1,sycophancy=0,proactivity=.8),provenance='synthetic',metadata={'personalization_target':.1,'proactivity_target':.8})
    out=evaluate_contract([r],ContractPolicy())['summary']
    assert out['user_state_responsiveness'] > .99
    assert out['context_suppression'] > .99
    assert out['context_application'] > .99
    assert out['invariant_attack_resistance'] > .99
    assert out['contract_score'] > .99
