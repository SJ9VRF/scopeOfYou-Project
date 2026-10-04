from __future__ import annotations
from pathlib import Path
from html.parser import HTMLParser
import zipfile, hashlib, json, shutil, tempfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'/'scope-of-you-project-page.zip'
OUT.parent.mkdir(exist_ok=True)

class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        for key in ('href','src'):
            val=d.get(key)
            if val and not val.startswith(('#','http://','https://','mailto:','javascript:')):
                self.links.append(val)

def add_linked_html(rel: Path, selected: set[Path]):
    src=ROOT/rel
    if not src.is_file(): return
    selected.add(rel)
    if src.suffix.lower() not in {'.html','.htm'}: return
    p=Parser(); p.feed(src.read_text(errors='ignore'))
    for raw in p.links:
        target=(rel.parent/raw).resolve()
        try: sub=target.relative_to(ROOT.resolve())
        except ValueError: continue
        if target.is_dir(): sub=sub/'index.html'; target=ROOT/sub
        if target.is_file() and sub not in selected:
            selected.add(sub)
            if target.suffix.lower() in {'.html','.htm'}:
                add_linked_html(sub,selected)

selected:set[Path]=set()
add_linked_html(Path('index.html'), selected)
# Evidence page is a key second layer and is already linked, but keep all its companion markdown.
for p in (ROOT/'evidence').glob('*'):
    if p.is_file(): selected.add(p.relative_to(ROOT))
# Raw evidence and demos are intentionally included so page claims are inspectable offline.
for base in ['artifacts','demo','video','blog','portfolio']:
    b=ROOT/base
    if b.exists():
        for p in b.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts: selected.add(p.relative_to(ROOT))
# Core identity and release context.
for rel in ['README.md','RESEARCH_LEAD_BRIEF.md','HIRING_MANAGER_60_SECOND.md','HIRING_MANAGER_WALKTHROUGH.md',
            'CITATION.cff','DATASET_CARD.md','MODEL_CARD.md','CLAIMS_AND_LIMITATIONS.md','BENCHMARK_CONTRACT_CARD.md',
            'PROJECT_PAGE_COMPLIANCE.md','reports/EXECUTED_EVIDENCE_MANIFEST.json','experiments/EXPERIMENT_LEDGER.jsonl']:
    if (ROOT/rel).is_file(): selected.add(Path(rel))

fixed=(2026,1,1,0,0,0)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for rel in sorted(selected, key=lambda x:x.as_posix()):
        p=ROOT/rel
        info=zipfile.ZipInfo(rel.as_posix(), fixed); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o644<<16
        z.writestr(info,p.read_bytes())
sha=hashlib.sha256(OUT.read_bytes()).hexdigest()
manifest={'name':'Scope of You standalone project page','files':len(selected),'sha256':sha,'entrypoint':'index.html'}
OUT.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
