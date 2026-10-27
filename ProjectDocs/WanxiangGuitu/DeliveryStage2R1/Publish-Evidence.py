"""Publish ended S2-R1 diagnostics through the existing redactor. Never saves/builds."""
import argparse,hashlib,importlib.util,json,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args();root=a.run.resolve(strict=True);target=a.target.resolve()
if not a.run.is_absolute() or 'locallow' in str(root).lower() or not (root/'owner.json').exists() or target.exists():raise ValueError('Owned isolated run and fresh publication required')
if not (root/'preserved-processes.json').exists() or json.loads((root/'preserved-processes.json').read_text(encoding='utf-8-sig'))!=[]:raise ValueError('Cannot publish active/preserved run')
spec=importlib.util.spec_from_file_location('redactor',Path(__file__).resolve().parents[1]/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
allowed={'owner.json','results.json','results.csv','counts.json','REPORT.md','preserved-processes.json','execution-inputs.json','selected-plan.json','selected-inputs.json','attempt.json','setup.json','case-actions.txt','failure.txt','combat-measure.json','combat-observations.jsonl','observation-checkpoint.json','recovery-result.json','recovery-actions.txt','stage2-input.json','stage2-metrics.json','stage2-transactions.jsonl','stage-result-Normal.json','stage-result-Resume.json','stage-result-FinalResume.json','process-result-Normal.json','process-result-Resume.json','process-result-FinalResume.json','attack-actions.csv','dodge-actions.csv','boss-combat.csv','boss-world.csv','normal-results.txt','normal-ai.csv','s2r1-boundaries.txt','s2r1-observation-probe.txt','stage2-damage-metric.txt','validation-interruption.json','owned-editor-close.json','environment.json','BuildSummary.txt','storage-audit.jsonl'}
diagnostics=[];logs=[];screens=[]
for f in root.rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(root)
 if any(x in ('Project','Library','Worker','Deferred','Protected','Player','WanxiangGuitu','BoundaryPlayer','Dumps','Release') or x.startswith('ExecutedDrivers-') for x in rel.parts):continue
 if f.name in ('save.json','save.backup.json') or 'ground-loot' in str(rel).lower():continue
 if f.suffix=='.log':logs.append(rel.as_posix())
 elif f.suffix=='.png' and f.name.startswith('boss-telegraph-'):screens.append(rel)
 elif f.name in allowed or f.name.endswith(('.exit.json','.command.json','.desktop-process.json','.launch-spec.json','.resources-before.json')):diagnostics.append(rel.as_posix())
m.publish(root,target/'Diagnostics',sorted(diagnostics));m.publish(root,target/'Logs',sorted(logs),archive=True)
for rel in screens:
 dst=target/'Screens'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/rel,dst)
files=[dict(path=f.relative_to(target).as_posix(),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(target.rglob('*')) if f.is_file()]
(target/'publication-manifest.json').write_text(json.dumps(dict(source=str(root),scope='Redacted diagnostics; exact PNG bytes; no full save/pages/build/dump/cache. Originals remain external.',logs=len(logs),screens=len(screens),files=files),ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(diagnostics=len(diagnostics),logs=len(logs),screens=len(screens))))
