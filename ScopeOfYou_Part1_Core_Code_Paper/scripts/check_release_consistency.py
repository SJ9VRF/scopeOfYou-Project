from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
expected=(root/'VERSION').read_text().strip()
problems=[]
pyproject=(root/'pyproject.toml').read_text()
m=re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M)
if not m or m.group(1)!=expected: problems.append(f'pyproject version != {expected}')
readme=(root/'README.md').read_text()
if f'Release {expected}' not in readme: problems.append('README release version mismatch')
required=[
 'docs/README.md','docs/ARCHITECTURE.md','docs/architecture.svg','paper/main.pdf',
 'portfolio/index.html','dashboard/index.html','demo/live.html','BENCHMARK_CARD.md',
 'DATASET_CARD.md','MODEL_CARD.md','CLAIMS_AND_LIMITATIONS.md','SECURITY.md','NOVELTY_AUDIT.md','BENCHMARK_CF_CARD.md','docs/SOTA_EVALUATION_PLAN.md','docs/RELATED_WORK.md',
 'reports/personalbench_v31_summary.json','reports/personalbench_v31_statistics.json',
 'reports/personalbench_v31_ablations.json','reports/boundary_novelty_results.json','reports/release_audit.json']
for rel in required:
    if not (root/rel).exists(): problems.append(f'missing {rel}')
# conservative placeholder scan; local-path examples are intentional, opaque placeholders are not.
patterns=['TODO','FIXME','PLACEHOLDER','YOUR_MODEL_NAME_OR_LOCAL_PATH','TBD']
for path in root.rglob('*'):
    if not path.is_file() or path.suffix.lower() in {'.pt','.png','.pdf','.pyc','.zip','.bundle'}: continue
    if '.git' in path.parts or path.name in {'check_release_consistency.py','build_reviewer_bundle.py','verify_reviewer_bundle.py'}: continue
    try: txt=path.read_text(errors='ignore')
    except Exception: continue
    for pat in patterns:
        if pat in txt: problems.append(f'{path.relative_to(root)} contains {pat}')
if problems:
    print('\n'.join('ERROR: '+p for p in problems)); sys.exit(1)
print(f'Consistency check passed for release {expected}.')
