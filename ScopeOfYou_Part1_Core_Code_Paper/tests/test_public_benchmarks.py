import json
from pathlib import Path
from personal_agi_pt.public_benchmarks import (
    ContractState, adapt_alignx, adapt_benchpres, adapt_personalized_rewardbench,
    normalize_records, score_selectivity, load_json_or_jsonl
)

FIX=Path(__file__).parent/'fixtures'/'public_benchmarks'

def test_benchpres_contract_mapping():
    r=load_json_or_jsonl(FIX/'benchpres.jsonl')[0]
    ex=adapt_benchpres(r)
    assert [c.state for c in ex.contracts] == [ContractState.APPLY, ContractState.SUPPRESS, ContractState.SUPPRESS]
    assert ex.user_context['domain']=='finance'

def test_rewardbench_hides_rubric_from_user_context():
    r=load_json_or_jsonl(FIX/'rewardbench.jsonl')[0]
    ex=adapt_personalized_rewardbench(r)
    assert 'rubric_aspects' not in ex.user_context
    assert ex.metadata['no_leak_fields']==['rubric_aspects','narrative']
    assert ex.chosen and ex.rejected

def test_alignx_preserves_preference_vector():
    r=load_json_or_jsonl(FIX/'alignx.jsonl')[0]
    ex=adapt_alignx(r)
    assert ex.metadata['preference_dimensions']==3
    assert ex.user_context['preference_direction']==[1,0.5,0]

def test_selectivity_metrics_perfect_predictions():
    r=load_json_or_jsonl(FIX/'benchpres.jsonl')
    ex=normalize_records(r,'benchpres')
    out=score_selectivity(ex, {'bp1':['apply','suppress','suppress']})
    assert out['AAR']==1.0
    assert out['MR']==0.0
    assert out['selectivity_score']==1.0
