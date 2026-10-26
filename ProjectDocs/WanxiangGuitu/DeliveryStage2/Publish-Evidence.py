"""Publish ended-run Stage2 diagnostics via the existing redactor, never saves.
Raw logs/dumps/builds remain in the owned external root; screenshots copied raw.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args()
root=a.run.resolve(strict=True);target=a.target.resolve();here=Path(__file__).resolve().parent
if not a.run.is_absolute() or 'locallow' in {s.lower() for s in root.parts} or not (root/'owner.json').exists() or target.exists():raise ValueError('Owned external run and fresh publication required')
if not (root/'preserved-processes.json').exists():raise ValueError('Ended All receipt absent; do not publish a live partial run')
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB10/Publish-Evidence.py'),'--run',str(root),'--target',str(target/'ExistingFramework')],check=True)
spec=importlib.util.spec_from_file_location('publisher',here.parent/'DeliveryUI01/Automation/publish-evidence.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
allowed={'results.json','results.csv','REPORT.md','owner.json','execution-inputs.json','selected-inputs.json',
 'stage2-input.json','stage2-metrics.json','stage2-transactions.jsonl','normal-ai.csv','normal-results.txt','metadata.txt',
 'attack-actions.csv','dodge-actions.csv','boss-combat.csv','boss-world.csv','storage-audit.jsonl',
 'process-result-Normal.json','process-result-Resume.json','process-result-FinalResume.json',
 'matrix-summary.json','matrix-results.csv','stage2-controller-shape.json','stage2-physical.csv',
 'stage2-physical.txt','stage2-physical-paths.jsonl','stage2-builds.csv','stage2-seeds.txt','stage2-100-seeds.csv',
 'stage2-retry.txt','stage2-retry-boundaries.jsonl','stage2-damage-metric.txt','preserved-processes.json','environment.json'}
paths=[];logs=[];images=[];drivers=[]
for parent in ('Stage2Matrix','Stage2Summary','Stage2LogGateProbes','Stage2Environment','Rules'):
 for f in (root/parent).rglob('*'):
  if not f.is_file():continue
  rel=f.relative_to(root)
  if f.name=='save.json' or 'ground-loot' in str(rel).lower():continue
  if f.suffix=='.log' and parent=='Stage2Matrix':logs.append(rel)
  elif f.suffix=='.png' and parent=='Stage2Matrix':images.append(rel)
  elif parent=='Stage2Matrix' and f.suffix=='.cs' and any(x.startswith('ExecutedDrivers-') for x in f.parts):drivers.append(rel)
  elif f.name in allowed or f.name.startswith('score-normal-') or f.name.endswith(('.exit.json','.command.json','.desktop-process.json','.launch-spec.json','.resources-before.json')):paths.append(rel)
module.publish(root,target/'Diagnostics',sorted(p.as_posix() for p in set(paths)))
if logs:module.publish(root,target/'Logs',sorted(p.as_posix() for p in set(logs)),archive=True)
for rel in images:
 dst=target/'Screens'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/rel,dst)
for rel in drivers:
 dst=target/'ExecutedSources'/Path(str(rel)+'.txt');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/rel,dst)
proofs=[]
for folder in (root/'Stage2Matrix').glob('w*-s*'):
 if not folder.is_dir():continue
 proof=dict(case=folder.name,scope='Synthetic identity projection only; no full saves/commit plans published',checkpoints=[])
 for stage in (1,2):
  f=folder/f'b4-checkpoint-{stage}.json'
  if not f.exists():continue
  raw=f.read_bytes();d=json.loads(raw.decode('utf-8-sig'))
  selected={k:d.get(k) for k in ('profile','run','region','seed','firstRun','exitId','receipt','stage')}
  selected.update({k+'Sha256':hashlib.sha256(str(d.get(k,'')).encode()).hexdigest() for k in ('layout','streams','ledger','gear','entities','ground','warehouse','recipes','hunts')})
  selected['originalSha256']=hashlib.sha256(raw).hexdigest();proof['checkpoints'].append(selected)
 marks=folder/'normal-results.txt';text=marks.read_text(encoding='utf-8-sig') if marks.exists() else ''
 proof['runtimeAssertions']={s:s in text for s in ('NEW_PROCESS_FULL_STATE_PASS stage=1','NEW_PROCESS_FULL_STATE_PASS stage=2','REAL_SETTLEMENT_STORE_WITHDRAW_CRAFT','SECOND_FOREST_DEPARTED','ALL_PASS')}
 proofs.append(proof)
(target/'restore-projections.json').write_text(json.dumps(proofs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest=[dict(path=p.relative_to(target).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(target.rglob('*')) if p.is_file()]
(target/'publication-manifest.json').write_text(json.dumps(dict(scope='Inherited redacted diagnostic publisher; Stage2 screenshot/source files copied raw; no full saves, pages, dumps, build/cache',files=manifest),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(stage2Screens=len(images),stage2RawLogs=len(logs),executedSources=len(drivers),restoreCases=len(proofs),publishedFiles=len(manifest))))
