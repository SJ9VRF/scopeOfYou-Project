from __future__ import annotations
from pathlib import Path
import re, sys, subprocess
ROOT=Path(__file__).resolve().parents[1]
SKIP_EXT={'.pt','.pyc','.png','.jpg','.jpeg','.gif','.zip','.npy','.npz','.bin'}
SKIP_DIR={'.pytest_cache','__pycache__'}
patterns=[
    re.compile(r'\b20\d{2}-\d{2}-\d{2}\b'),
    re.compile(r'\b\d{2}/\d{2}/20\d{2}\b'),
    re.compile(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+20\d{2}\b',re.I),
]
forbidden_keys=('date-released:','date-created:','date-modified:','created_at','updated_at','generated_at','"timestamp"')
findings=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.lower() in SKIP_EXT or any(part in SKIP_DIR for part in p.parts):
        continue
    if p.resolve() == Path(__file__).resolve():
        continue
    try: text=p.read_text(errors='ignore')
    except Exception: continue
    for i,line in enumerate(text.splitlines(),1):
        if any(k in line for k in forbidden_keys) or any(rx.search(line) for rx in patterns):
            findings.append(f'{p.relative_to(ROOT)}:{i}: {line[:200]}')
# PDF metadata dates
pdf=ROOT/'paper'/'main.pdf'
if pdf.exists():
    try:
        info=subprocess.check_output(['pdfinfo',str(pdf)],text=True,stderr=subprocess.STDOUT)
        for line in info.splitlines():
            if line.startswith(('CreationDate:','ModDate:')):
                findings.append(f'paper/main.pdf metadata: {line}')
    except Exception as e:
        findings.append(f'Could not inspect PDF metadata: {e}')
if findings:
    print('PROJECT DATE AUDIT: FAIL')
    print('\n'.join(findings[:200]))
    sys.exit(1)
print('PROJECT DATE AUDIT: PASS')
