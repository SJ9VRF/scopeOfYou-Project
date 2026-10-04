from personal_agi_pt.statistics import paired_user_bootstrap
from personal_agi_pt.schema import InteractionRecord, Feedback
from personal_agi_pt.policy import PolicyOutput

class P:
    def __init__(self,v): self.v=v
    def predict(self,r):
        return PolicyOutput(response='',behavior={'personalization':self.v,'factuality':1.0,'sycophancy':0.0,'proactivity':0.5,'helpfulness':1.0})

def test_paired_bootstrap_direction():
    rows=[]
    for u in range(4):
        for i in range(3):
            rows.append(InteractionRecord(conversation_id=f'{u}-{i}',user_id=str(u),user_state={'verbosity':'detailed'},history=[],current_query='x',candidate_response='y',feedback=Feedback(factuality=1,sycophancy=0,proactivity=.5),provenance='synthetic',metadata={'personalization_target':.9,'proactivity_target':.5}))
    out=paired_user_bootstrap(rows,P(.5),P(.9),n_boot=100,seed=1)
    assert out['metrics']['personalization']['delta'] > 0
    assert out['users']==4
