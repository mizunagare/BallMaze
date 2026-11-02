"""Read-only external observer. Never alters a watched Unity input."""
import argparse,json,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--spec',type=Path,required=True);a=p.parse_args();s=json.loads(a.spec.read_text(encoding='utf-8-sig'));project=Path(s['project']);out=Path(s['output']);out.mkdir(exist_ok=False);last={};start=time.monotonic();count=0
files=['Assets/Settings/PC_RPAsset.asset','Assets/Settings/UniversalRenderPipelineGlobalSettings.asset','ProjectSettings/GraphicsSettings.asset','ProjectSettings/ProjectSettings.asset','ProjectSettings/UnityConnectSettings.asset']
with (out/'changes.jsonl').open('w',encoding='utf-8') as log:
 while not Path(s['stop']).exists() and time.monotonic()-start<1800:
  for rel in files:
   try:
    f=project/rel;raw=f.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    if last.get(rel)!=sha:
     count+=1;folder=out/str(count).zfill(4);folder.mkdir();(folder/'bytes.txt').write_bytes(raw);item=dict(event='initial' if rel not in last else 'changed',utcNs=time.time_ns(),path=rel,sha256=sha,bytes=len(raw),lastWriteUtcNs=f.stat().st_mtime_ns)
     logfile=Path(s['log']);item['unityLogBytesAtObservation']=logfile.stat().st_size if logfile.exists() else 0
     if logfile.exists():(folder/'log-tail.txt').write_text(logfile.read_text(encoding='utf-8',errors='replace')[-12000:],encoding='utf-8')
     log.write(json.dumps(item)+'\n');log.flush();last[rel]=sha
   except OSError as e:log.write(json.dumps(dict(event='read-error',utcNs=time.time_ns(),path=rel,error=repr(e)))+'\n');log.flush()
  time.sleep(.05)
(out/'completion.json').write_text(json.dumps(dict(stopped=Path(s['stop']).exists(),seconds=time.monotonic()-start,changes=count)),encoding='utf-8')
