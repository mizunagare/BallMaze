"""Audit the exact 12 input roots emitted by the unmodified supplied reproducer.
Does not alter the supplied package, inputs, original results or source hash guard.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if not a.inputs.is_absolute() or not a.output.is_absolute() or a.output.exists():raise ValueError('Absolute original input root and fresh output required')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
original=read(a.inputs/'review-results.json');source=Path(__file__).resolve().parent.parent/'DeliveryStage2';a.output.mkdir(parents=True);rows=[]
for observed in original['observations']:
 name=observed['case'];work=(a.inputs/name).resolve()
 if not work.is_relative_to(a.inputs.resolve()):raise ValueError('Unsafe case name')
 command=[sys.executable,'-B',str(source/'Summarize-Matrix.py'),'--matrix',str(work/'matrix'),'--plan',str(work/'plan.json'),'--output',str(a.output/name)]
 child=subprocess.run(command,capture_output=True,text=True,encoding='utf8');(a.output/(name+'.stdout.txt')).write_text(child.stdout,encoding='utf8');(a.output/(name+'.stderr.txt')).write_text(child.stderr,encoding='utf8')
 try:
  s=read(a.output/name/'matrix-summary.json');rejected=child.returncode!=0 and not s['finalAcceptanceEligible'];ok=False
  if name=='01-control':ok=child.returncode==0 and s['status']=='PASS'
  elif name.startswith(('02-','03-')):ok=rejected
  elif name.startswith('04-'):ok=rejected and any('stage-result-Resume.json' in i for r in s['rows'] for i in r['issues'])
  elif name.startswith('05-'):ok=rejected and s['started']==2 and s['departed']==2 and s['knownTerminal']==1 and s['unknown']==1
  elif name.startswith('06-'):ok=rejected and s['completeTerminalStatistics']['Safety']['elapsedSeconds']['mean']==60 and s['partialWindows'][0]['elapsedSeconds']==2
  elif name.startswith('07-'):ok=child.returncode==2 and s['status']=='NOT_RUN' and s['started']==0 and s['departed']==0 and s['notStarted']==1 and s['extractionSuccessRate'] is None
  elif name.startswith('08-'):ok=rejected and s['knownTerminal']==0 and s['extracted']==0 and s['extractionSuccessRate'] is None and s['statisticsDiagnosticOnly'] is True
  elif name.startswith('09-'):ok=rejected and any('contract' in i for r in s['rows'] for i in r['issues'])
  ok=ok and s['inputManifest']==s['inputManifestAfter'];error=''
 except Exception as e:s={};ok=False;error=repr(e)
 rows.append(dict(case=name,status='PASS' if ok else 'FAIL',exitCode=child.returncode,command=command,originalObserved=observed,now={k:s.get(k) for k in ('status','finalAcceptanceEligible','statisticsDiagnosticOnly','registered','started','departed','knownTerminal','extracted','unknown','notStarted','extractionSuccessRate')},sourceInputsUnchanged=s.get('inputManifest')==s.get('inputManifestAfter'),error=error))
result=dict(status='PASS' if len(rows)==12 and all(x['status']=='PASS' for x in rows) else 'FAIL',scope='Same exact original 12 synthetic input roots; fixed CLI, independent assertions. No rewritten inputs, package source or game execution.',sources=[dict(path=str(source/n),sha256=hashlib.sha256((source/n).read_bytes()).hexdigest()) for n in ('MatrixEvidence.py','Summarize-Matrix.py')],cases=rows)
(a.output/'supplied-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(status=result['status'],PASS=sum(x['status']=='PASS' for x in rows),FAIL=sum(x['status']=='FAIL' for x in rows))));raise SystemExit(0 if result['status']=='PASS' else 1)
