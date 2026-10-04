from __future__ import annotations
from pathlib import Path
from html.parser import HTMLParser
import sys
HERE=Path(__file__).resolve()
ROOT = HERE.parent.parent if HERE.parent.name == 'scripts' else Path.cwd().resolve()
class P(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,t,a):
        d=dict(a)
        for k in ('href','src'):
            v=d.get(k)
            if v:self.links.append(v)
errors=[]; checked=0
for html in ROOT.rglob('*.html'):
    if any(x in html.parts for x in ('.git','__pycache__')):continue
    p=P();p.feed(html.read_text(errors='ignore'))
    for raw in p.links:
        if raw.startswith(('#','http://','https://','mailto:','javascript:')):continue
        target=(html.parent/raw).resolve(); checked+=1
        if not target.exists(): errors.append(f'{html.relative_to(ROOT)} -> {raw}')
if not (ROOT/'index.html').is_file(): errors.append('missing index.html')
for rel in ['docs/FAILURE_TAXONOMY.md','docs/THREAT_MODEL.md','docs/RESEARCH_OWNERSHIP_MAP.md','reports/RED_TEAM_COVERAGE_MATRIX.md']:
    if not (ROOT/rel).is_file(): errors.append('missing '+rel)
if errors:
    print('PROJECT PAGE BUNDLE VERIFY: FAIL'); [print(' -',e) for e in errors]; raise SystemExit(1)
print(f'PROJECT PAGE BUNDLE VERIFY: PASS links_checked={checked}')
