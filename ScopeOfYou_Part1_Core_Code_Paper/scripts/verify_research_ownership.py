from pathlib import Path
import json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
required=[
 'docs/FAILURE_TAXONOMY.md','docs/THREAT_MODEL.md','docs/RESEARCH_OWNERSHIP_MAP.md',
 'reports/RED_TEAM_COVERAGE_MATRIX.md','reports/red_team_coverage.json'
]
for p in required:
    assert (ROOT/p).is_file(), p
cov=json.loads((ROOT/'reports/red_team_coverage.json').read_text())
assert cov['artifact_scope']=='evaluator_stress_suite_not_model_capability'
assert cov['n_scenarios']==288
assert cov['dimensions']['variant']=={'clean':96,'stale_memory':96,'tool_injection':96}
assert cov['dimensions']['domain']=={'calendar':48,'email':48,'files':48,'purchase':48,'settings':48,'travel':48}
assert cov['dimensions']['target_action']=={'ACT':18,'ASK':198,'SUGGEST':72}
# Raw failure evidence must still carry the two observed threshold codes used in the taxonomy.
for fname,total in [('reports/failures_v31_raw_test.jsonl',1172),('reports/failures_v31_constrained_test.jsonl',79)]:
    rows=[json.loads(x) for x in (ROOT/fname).read_text().splitlines() if x.strip()]
    assert len(rows)==total, (fname,len(rows))
    assert set(r['code'] for r in rows) <= {'PERS-01','PRO-01'}
# Guard against converting evaluator stress coverage into a model capability claim.
text=(ROOT/'reports/RED_TEAM_COVERAGE_MATRIX.md').read_text().lower()
assert 'not a production-security or llm-capability claim' in text
assert 'not evidence that pco-robust' in text
print('Research ownership / failure-taxonomy / red-team coverage verification: PASS')
