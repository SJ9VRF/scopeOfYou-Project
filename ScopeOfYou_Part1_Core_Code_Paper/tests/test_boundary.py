from personal_agi_pt.counterfactual_eval import evaluate_counterfactual
from personal_agi_pt.schema import InteractionRecord, Feedback
from personal_agi_pt.policy import PolicyOutput

class PreferencePolicy:
    def predict(self,r):
        v={'concise':.1,'balanced':.5,'detailed':.9}[r.user_state['verbosity']]
        return PolicyOutput(response='',behavior={'personalization':v,'factuality':1.0,'sycophancy':0.0,'proactivity':.5,'helpfulness':1.0})

def test_counterfactual_boundary_perfect_policy():
    r=InteractionRecord(conversation_id='c',user_id='u',user_state={'verbosity':'concise'},history=[],current_query='Explain x',candidate_response='y',feedback=Feedback(factuality=1,sycophancy=0,proactivity=.5),provenance='synthetic',metadata={'personalization_target':.1,'proactivity_target':.5})
    out=evaluate_counterfactual([r],PreferencePolicy())['summary']
    assert out['direction_accuracy']==1.0
    assert out['counterfactual_responsiveness'] > .99
    assert out['invariant_stability'] > .99
