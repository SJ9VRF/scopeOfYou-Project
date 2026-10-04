from __future__ import annotations
import json,time
from contextlib import contextmanager
from pathlib import Path
@contextmanager
def track(path,label,metadata=None):
 start=time.perf_counter(); t0=time.time(); yield; elapsed=time.perf_counter()-start
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);row={'label':label,'wall_seconds':elapsed,'started_unix':t0,**(metadata or {})};
 with p.open('a') as f:f.write(json.dumps(row)+'\n')
