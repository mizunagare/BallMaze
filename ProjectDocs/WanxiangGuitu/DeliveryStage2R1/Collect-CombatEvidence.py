"""Bind completed shared Editor process receipts to case evidence, then reuse matrix audit.
No metric/transaction is edited. Output is diagnostic and fresh; live inputs refused.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.run.resolve(strict=True)
if not a.run.is_absolute() or not (root/'owner.json').exists() or a.output.exists():raise ValueError('Owned ended run and fresh output required')
if not (root/'preserved-processes.json').exists() or json.loads((root/'preserved-processes.json').read_text(encoding='utf-8-sig'))!=[]:raise ValueError('Run not ended or owned processes preserved')
rows=json.loads((root/'results.json').read_text(encoding='utf-8-sig'));a.output.mkdir(parents=True);reports=[]
for group in sorted((root/'Rules').glob('*-*')):
 plan=group/'selected-plan.json'
 if not plan.exists() or not (group/'owner.json').exists():continue
 cases=json.loads(plan.read_text(encoding='utf-8-sig'))['cases']
 for case in cases:
  folder=group/case['id'];meta=folder/'attempt.json'
  if not meta.exists():continue
  attempt=json.loads(meta.read_text(encoding='utf-8-sig'));process=[r for r in rows if r['name']==attempt.get('parentMethod')]
  if len(process)!=1:continue
  r=process[0];dest=folder/'process-result-Normal.json'
  if dest.exists():raise ValueError('Refuse to overwrite prior observation '+str(dest))
  record=dict(mode='Normal',exitCode=r.get('exitCode'),timedOut=r.get('timedOut'),scope='Shared Editor group process; not one OS process per case. Bound by actual executeMethod in pre-trial attempt.',sourceMethod=r['name'],sourceResultSha256=hashlib.sha256((root/'results.json').read_bytes()).hexdigest(),sourceCommand=r['command'])
  dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 # Only after the real parent process exit evidence above, never in running C#.
 (group/'results.json').write_text(json.dumps([dict(r,name=c['id']+'.Normal') for c in cases if (group/c['id']/'attempt.json').exists() for r in rows if r['name']==json.loads((group/c['id']/'attempt.json').read_text(encoding='utf-8-sig')).get('parentMethod')],ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (group/'preserved-processes.json').write_text('[]\n',encoding='utf8')
 target=a.output/group.name
 child=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve().parent.parent/'DeliveryStage2/Summarize-Matrix.py'),'--matrix',str(group),'--output',str(target)],capture_output=True,text=True,encoding='utf8')
 (a.output/(group.name+'.stdout.txt')).write_text(child.stdout,encoding='utf8');(a.output/(group.name+'.stderr.txt')).write_text(child.stderr,encoding='utf8')
 reports.append(dict(group=group.name,exitCode=child.returncode,status=json.loads((target/'matrix-summary.json').read_text())['status'] if (target/'matrix-summary.json').exists() else 'FAIL'))
(a.output/'collection.json').write_text(json.dumps(dict(scope='Post-exit process binding and reuse of existing summary; originals preserved, no game/save access',groups=reports),indent=2)+'\n',encoding='utf8');print(json.dumps(reports));raise SystemExit(0 if reports and all(x['exitCode']==0 for x in reports) else 1)
