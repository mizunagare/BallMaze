"""Curated diagnostic-only history; no full saves, dumps, builds or caches."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

p=argparse.ArgumentParser();p.add_argument('--catalog',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args()
if a.target.exists():raise ValueError('Fresh target required')
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('redactor',here.parent/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
catalog=json.loads(a.catalog.read_text(encoding='utf-8-sig'));summary=[]
allow={'results.json','results.csv','counts.json','owner.json','REPORT.md','metadata.txt','normal-results.txt','normal-ai.csv','stage2-input.json','stage2-metrics.json','stage2-transactions.jsonl','gate.json','process.json',
 'process-result-Normal.json','process-result-Resume.json','process-result-FinalResume.json','validation-interruption.json','owned-normal-close.json','owned-editor-normal-close.json','input.json'}
for entry in catalog:
 root=Path(entry['root']).resolve(strict=True)
 if not Path(entry['root']).is_absolute() or 'locallow' in {s.lower() for s in root.parts}:raise ValueError('Explicit isolated roots only')
 paths=[];logs=[]
 for f in root.rglob('*'):
  if not f.is_file():continue
  rel=f.relative_to(root)
  if any(s in {'Project','Library','Build','ground-loot'} for s in rel.parts):continue
  if f.suffix=='.log':logs.append(rel)
  elif f.name in allow or f.name.endswith(('.command.json','.exit.json','.resources-before.json')):paths.append(rel)
 target=a.target/entry['id'];m.publish(root,target/'Diagnostics',sorted(p.as_posix() for p in paths))
 if logs:m.publish(root,target/'Logs',sorted(p.as_posix() for p in logs),archive=True)
 summary.append(dict(**entry,publishedDiagnostics=len(paths),redactedLogs=len(logs),rawLogsRetained=True,notFinalAll=True))
a.target.mkdir(parents=True,exist_ok=True)
(a.target/'INDEX.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(attempts=len(summary),logs=sum(r['redactedLogs'] for r in summary))))
