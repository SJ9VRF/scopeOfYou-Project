from __future__ import annotations
import argparse, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path
from .dataio import load_jsonl


def _norm(s: str) -> str:
    return ' '.join((s or '').lower().split())


def audit(dataset: str | Path) -> dict:
    recs = load_jsonl(dataset)
    validation_errors = []
    exact = Counter()
    by_split = Counter()
    by_prov = Counter()
    query_splits = defaultdict(set)
    user_splits = defaultdict(set)
    confidences = []
    for i, r in enumerate(recs):
        errs = r.validate()
        if errs:
            validation_errors.append({'index': i, 'errors': errs})
        by_split[r.split] += 1
        by_prov[r.provenance] += 1
        confidences.append(float(r.confidence))
        key = hashlib.sha256((_norm(r.current_query)+'\n'+_norm(r.candidate_response)+'\n'+json.dumps(r.user_state,sort_keys=True)).encode()).hexdigest()
        exact[key] += 1
        query_splits[_norm(r.current_query)].add(r.split)
        user_splits[r.user_id].add(r.split)
    duplicate_rows = sum(c-1 for c in exact.values() if c > 1)
    cross_split_queries = sum(1 for v in query_splits.values() if len(v) > 1)
    cross_split_users = sum(1 for v in user_splits.values() if len(v) > 1)
    return {
        'records': len(recs),
        'schema_error_records': len(validation_errors),
        'exact_duplicate_rows': duplicate_rows,
        'split_counts': dict(by_split),
        'provenance_counts': dict(by_prov),
        'mean_confidence': sum(confidences)/len(confidences) if confidences else None,
        'unique_users': len(user_splits),
        'queries_seen_in_multiple_splits': cross_split_queries,
        'users_seen_in_multiple_splits': cross_split_users,
        'notes': {
            'query_overlap': 'Expected in controlled benchmark templates; do not treat template overlap as semantic leakage by itself.',
            'user_overlap': ('No user crosses splits; this is user-held-out.' if cross_split_users == 0 else 'Users cross splits; use a user-held-out split for strict generalization.')
        },
        'validation_errors': validation_errors[:20],
    }


def main():
    p=argparse.ArgumentParser();p.add_argument('--dataset',required=True);p.add_argument('--output');a=p.parse_args()
    result=audit(a.dataset)
    text=json.dumps(result,indent=2)
    if a.output:
        Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(text)
    print(text)
if __name__=='__main__': main()
