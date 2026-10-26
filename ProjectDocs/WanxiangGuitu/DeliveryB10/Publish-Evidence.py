"""Extend existing redaction publisher with explicit B10 outputs. Never publish saves/cache/builds."""
import argparse,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--directed',action='store_true');a=p.parse_args();here=Path(__file__).resolve().parent
if a.target.exists():raise ValueError('Fresh publication required')
a.target.mkdir(parents=True)
spec=importlib.util.spec_from_file_location('publish',here.parent/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if not a.directed:subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB09/Publish-Evidence.py'),'--run',str(a.run),'--target',str(a.target/'ExistingFramework')],check=True)
allowed={'results.json','results.csv','REPORT.md','owner.json','build-hashes.json','controlled-build.txt','baseline-export.json','preserved-processes.json','command.json','process.json','entry-audit.jsonl','storage-audit.jsonl','save-exit-audit.json','save-exit-audit.jsonl'}
paths=[];logs=[];images=[]
for f in sorted(a.run.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(a.run);parts=rel.parts
 if any(x in ('Project','Library','Build','Worker','Packages','WanxiangGuitu','legacy-forest-v9','fixtures') for x in parts):continue
 if f.suffix=='.png' and (f.name.startswith('b10-') or f.name=='title-player.png'):
  raw=f.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';out=a.target/'Screens'/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);w,h=struct.unpack('>II',raw[16:24]);images.append(dict(path=out.relative_to(a.target).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),width=w,height=h,scope='Actual rendered capture; controlled or observational, NOT native/human'))
 elif f.name in allowed or f.name.startswith('b10-') and f.suffix in {'.json','.txt','.jsonl','.csv'}:
  # Expected checkpoint strings include complete synthetic world state; use assertions, not raw snapshots.
  if f.name.endswith(('expected.txt','rig-before.txt','fixture-path.txt')):continue
  paths.append(rel.as_posix())
 elif f.suffix=='.log' and ('B10' in f.name or f.name.startswith(('player-','build-','prepare-'))):logs.append(rel.as_posix())
if paths:m.publish(a.run,a.target/'Diagnostics',paths)
if logs:m.publish(a.run,a.target/'Logs',logs,archive=True)
(a.target/'screens.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(images=len(images),diagnostics=len(paths),logs=len(logs))))
