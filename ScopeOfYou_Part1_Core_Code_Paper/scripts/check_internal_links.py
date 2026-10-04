from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
problems=[]
link_re=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
for md in root.rglob('*.md'):
    txt=md.read_text(errors='ignore')
    for target in link_re.findall(txt):
        if target.startswith(('http://','https://','#','mailto:')): continue
        clean=target.split('#',1)[0]
        if not clean: continue
        dest=(md.parent/clean).resolve()
        try: dest.relative_to(root.resolve())
        except ValueError: continue
        if not dest.exists(): problems.append(f'{md.relative_to(root)} -> {target}')
if problems:
    print('\n'.join('BROKEN: '+p for p in problems)); sys.exit(1)
print('Internal Markdown links passed.')
