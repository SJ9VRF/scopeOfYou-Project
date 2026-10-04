from __future__ import annotations
import json, subprocess, sys, time, urllib.request
from pathlib import Path

root=Path(__file__).resolve().parents[1]
proc=subprocess.Popen([sys.executable,'-m','personal_agi_pt.service','--checkpoint','checkpoints/sft_behavior_v31.pt','--port','8876'],cwd=root,env={**__import__('os').environ,'PYTHONPATH':'src'},stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
    for _ in range(40):
        try:
            with urllib.request.urlopen('http://127.0.0.1:8876/health',timeout=.3) as r:
                assert json.loads(r.read())['status']=='ok'; break
        except Exception: time.sleep(.1)
    else: raise RuntimeError('service did not become ready')
    body=json.dumps({'user_id':'smoke','user_state':{'verbosity':'concise','directness':'high','technical_depth':'advanced','confirmation_policy':'irreversible_only','correction_tolerance':'direct','proactivity':.4},'current_query':'What is the capital of Germany?'}).encode()
    req=urllib.request.Request('http://127.0.0.1:8876/predict',data=body,headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=3) as r: payload=json.loads(r.read())
    assert 'Berlin' in payload['response']
    print(json.dumps({'service_smoke':'passed','behavior':payload['behavior']},indent=2))
finally:
    proc.terminate()
    try: proc.wait(timeout=3)
    except subprocess.TimeoutExpired: proc.kill()
