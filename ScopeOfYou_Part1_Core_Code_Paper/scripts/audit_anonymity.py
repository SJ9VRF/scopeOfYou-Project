from __future__ import annotations
import argparse, re, sys
from pathlib import Path

TEXT_SUFFIXES={'.md','.txt','.tex','.py','.json','.jsonl','.yaml','.yml','.toml','.html','.css','.js','.cff','.csv'}
PATTERNS=[
    re.compile(r'\bAura\s+Yavary\b',re.I),
    re.compile(r'\bArefeh\s+Yavary\b',re.I),
    re.compile(r'\bauthor\s*:\s*Aura\b',re.I),
]
SKIP_NAMES={'audit_anonymity.py'}

def scan(root:Path):
    findings=[]
    for p in root.rglob('*'):
        if not p.is_file() or p.name in SKIP_NAMES or p.suffix.lower() not in TEXT_SUFFIXES: continue
        try: txt=p.read_text(errors='ignore')
        except Exception: continue
        for i,line in enumerate(txt.splitlines(),1):
            for pat in PATTERNS:
                if pat.search(line): findings.append((str(p.relative_to(root)),i,line.strip()[:200]))
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',nargs='?',default='.'); a=ap.parse_args()
    f=scan(Path(a.root))
    if f:
        for x in f[:100]: print(f'{x[0]}:{x[1]}: {x[2]}')
        print(f'ANONYMITY AUDIT: FAIL ({len(f)} findings)'); sys.exit(1)
    print('ANONYMITY AUDIT: PASS')
if __name__=='__main__': main()
