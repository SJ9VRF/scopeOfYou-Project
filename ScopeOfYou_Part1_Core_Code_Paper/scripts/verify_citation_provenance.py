from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = {
    'paper/main.tex': [
        'arXiv:2402.05133','10.18653/v1/2025.acl-long.397','arXiv:2506.02368',
        'arXiv:2602.12116','10.18653/v1/2026.acl-long.1391',
        '10.18653/v1/2026.findings-acl.159','arXiv:2603.19294','arXiv:2603.16557',
        'arXiv:2601.16621','arXiv:2601.13722','arXiv:2604.07343',
        '10.18653/v1/2026.findings-acl.31','arXiv:2504.07070','arXiv:2608.05813',
        'arXiv:2605.23382','arXiv:2608.16553','arXiv:2607.12985','arXiv:2606.23189',
        '10.18653/v1/2026.acl-industry.103','arXiv:2609.29144'
    ],
    'docs/CITATION_PROVENANCE_AUDIT.md': [
        'arXiv:2603.16557','arXiv:2601.13722','arXiv:2601.16621',
        'arXiv:2608.05813','arXiv:2607.12985','arXiv:2606.23189',
        '10.18653/v1/2026.acl-industry.103','arXiv:2609.29144','arXiv:2608.16553'
    ],
}
errors=[]
for rel, needles in required.items():
    p=ROOT/rel
    if not p.exists():
        errors.append(f'missing {rel}')
        continue
    text=p.read_text(errors='ignore')
    for needle in needles:
        if needle not in text:
            errors.append(f'{rel} missing {needle}')
if errors:
    print('CITATION PROVENANCE VERIFY: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('CITATION PROVENANCE VERIFY: PASS')
print('recent_prior_art_identifiers=verified_in_release')
