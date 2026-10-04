from __future__ import annotations
import importlib.metadata as md
import json, platform, sys
from pathlib import Path

packages=[]
for d in md.distributions():
    name=d.metadata.get('Name')
    if name:
        packages.append({'name':name,'version':d.version})
packages=sorted({(p['name'].lower(),p['version']):(p) for p in packages}.values(),key=lambda x:x['name'].lower())
out={'format':'lightweight-python-sbom-v1','python':sys.version.split()[0],'platform':platform.platform(),'packages':packages}
Path('reports/software_bill_of_materials.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'packages':len(packages),'python':out['python'],'platform':out['platform']},indent=2))
