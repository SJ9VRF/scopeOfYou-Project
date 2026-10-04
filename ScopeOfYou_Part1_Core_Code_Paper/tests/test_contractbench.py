from personal_agi_pt.contractbench import build_contractbench
from personal_agi_pt.contractbench_eval import evaluate_contractbench
from personal_agi_pt.synthetic_users import generate_profiles
from personal_agi_pt.synthetic_dataset import generate_interactions_v31
from personal_agi_pt.schema import InteractionRecord

class Dummy:
    def predict(self,r):
        class O: pass
        o=O(); o.behavior={'personalization':.5,'factuality':1.0,'sycophancy':0.0,'proactivity':.4,'helpfulness':.8}; return o

def test_contractbench_has_implicit_contracts_and_ood():
    rows=generate_interactions_v31(generate_profiles(4,7),4,0.1,59)
    records=[InteractionRecord.from_dict(r) for r in rows]
    cases=build_contractbench(records,max_users=2)
    labels={c.contract for c in cases}
    assert {'apply','suppress','uncertain','must_not_affect'} <= labels
    assert any(c.ood_domain for c in cases)
    assert all('Do not suggest' not in c.record.current_query for c in cases)
    out=evaluate_contractbench(cases,Dummy())
    assert 0 <= out['summary']['contract_score'] <= 1
