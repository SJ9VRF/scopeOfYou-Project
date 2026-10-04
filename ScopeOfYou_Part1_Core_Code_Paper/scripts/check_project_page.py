from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
PAGES=[ROOT/'index.html', ROOT/'portfolio'/'index.html']
REQUIRED_TEXT=[
    # exact 14-section structure
    '01 · Hero','02 · Why this problem matters','03 · Core idea','04 · Architecture',
    '05 · My contribution','06 · Experiments','07 · Results','08 · Failure analysis',
    '09 · Interactive demo','10 · Scaling','11 · Safety / limitations',
    '12 · Technical deep dive','13 · Artifacts','14 · Citation',
    # hero + five required CTAs
    'Scope of You','Aura Yavary','Paper','Code','Demo','Benchmark','Video',
    '+10.46 pp','20 / 20','Independent implicit evaluation',
    # problem / novelty / contract states
    'This project makes that boundary explicit and directly testable.',
    'APPLY','SUPPRESS','MUST-NOT-AFFECT','PCO-Robust',
    # architecture + required loops
    'Post-training / RL loop','Contract eval loop','Failure recovery loop','Agent loop','Permission loop',
    # contribution ownership
    'Research design','Implementation','Evaluation','Agentic extension','Aura Yavary',
    # experiment structure
    'Data / tasks','Baselines','Ablations','Setup','held-out','5 independent PCO-Robust seeds',
    # results requested fields
    'Baseline → method','Success rate / reliability','Recovery','Latency','Cost',
    # scaling exact requested items
    'Model size','Task horizon','Tool count','Cost / latency','Robustness',
    # safety exact requested items
    'Still fails','Irreversible actions','permission','Human escalation',
    # technical deep dive
    'Technical Report','ML Systems Design','Contract Benchmark',
    # artifacts exact requested items
    'GitHub','Dataset','Technical report','Blog post','Experiment ledger',
    # citation
    'BibTeX','year = {2026}',
    # honesty gates
    'not an LLM capability result','7–8B','human validation','fails the strict 2-point utility non-inferiority gate',
]
REQUIRED_IDS=['problem','idea','architecture','contribution','experiments','results','failures','demo','scaling','safety','deep','artifacts','citation']

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs=[]; self.ids=set(); self.buttons=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='a' and 'href' in d:self.hrefs.append(d['href'])
        if 'id' in d:self.ids.add(d['id'])
        if tag=='button':self.buttons += 1

def check(page: Path):
    text=page.read_text(encoding='utf-8')
    missing=[x for x in REQUIRED_TEXT if x.lower() not in text.lower()]
    if missing:
        print(f'Missing required project-page content in {page}:',missing); return False
    p=P();p.feed(text)
    missing_ids=[x for x in REQUIRED_IDS if x not in p.ids]
    if missing_ids:
        print(f'Missing required section IDs in {page}:',missing_ids); return False
    broken=[]
    for href in p.hrefs:
        if href.startswith(('#','http://','https://','mailto:','javascript:')): continue
        target=(page.parent/href).resolve()
        if not target.exists(): broken.append((href,str(target)))
    if broken:
        print(f'Broken project-page links in {page}:')
        for x in broken: print(' ',x)
        return False
    if p.buttons < 5:
        print(f'Expected interactive controls in {page}, saw only {p.buttons} buttons.'); return False
    print(f'Project page audit passed for {page.relative_to(ROOT)}: {len(p.hrefs)} links, {len(REQUIRED_TEXT)} content checks, {len(REQUIRED_IDS)} sections.')
    return True

ok=all(check(p) for p in PAGES)
if not ok: sys.exit(1)
print('PROJECT PAGE COMPLIANCE: PASS')
