"""Read-only re-audit of the already owned 19 + 26 + three-stage evidence.
Runs the existing CLI into fresh outputs; never updates inputs or reconstructs receipts.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if not a.output.is_absolute() or a.output.exists():raise ValueError('Fresh absolute output required')
here=Path(__file__).resolve().parent;source=here.parent/'DeliveryStage2';a.output.mkdir(parents=True)
old=Path('D:/WanxiangValidationRuns/Stage2FinalAll/20261027-010900-ab700d91')
r1=Path('D:/WanxiangValidationRuns/S2R1');frozen=r1/'FrozenValidation/20261027-102526-ad379719/Rules'
jobs=[('Historical19',old/'Stage2Matrix',old/'Stage2Summary/matrix-summary.json',True)]
for group in sorted(frozen.iterdir()):
 if (group/'selected-plan.json').exists() and (group/'owner.json').exists():jobs.append((group.name,group,r1/'FrozenCollection'/group.name/'matrix-summary.json',False))
jobs.append(('NormalThreeStage',r1/'BoundaryRecovery2/20261027-101700-1a9ec735/Stage2Protocol',r1/'Stage2ProtocolAudit/matrix-summary.json',False))
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
reports=[]
major=('run','profile','region','secondRun','secondRegion','elapsedSeconds','damageTaken','potionsUsed','meters','obtained','kept','lost','assetsStart','assetsEnd','extracted','committed','acknowledged','secondForest')
for name,root,previous,legacy in jobs:
 command=[sys.executable,'-B',str(source/'Summarize-Matrix.py'),'--matrix',str(root),'--output',str(a.output/name)]
 if legacy:command.append('--legacy-audit')
 child=subprocess.run(command,capture_output=True,text=True,encoding='utf8');(a.output/(name+'.stdout.txt')).write_text(child.stdout,encoding='utf8');(a.output/(name+'.stderr.txt')).write_text(child.stderr,encoding='utf8')
 checks=[];diffs=[]
 try:
  now=read(a.output/name/'matrix-summary.json');before=read(previous);by={r['input']['id']:r for r in before['rows']}
  for row in now['rows']:
   prior=by.get(row['input']['id'],{})
   for key in major:
    if row.get(key)!=prior.get(key):diffs.append(dict(case=row['input']['id'],field=key,before=prior.get(key),after=row.get(key)))
    checks.append(dict(case=row['input']['id'],field=key,equal=row.get(key)==prior.get(key)))
  for key in ('planned','validSorties','extractionSuccessRate','counts','groupsDescriptiveOnly'):
   if now.get(key)!=before.get(key):diffs.append(dict(field=key,before=before.get(key),after=now.get(key)))
  unchanged=now['inputManifest']==now['inputManifestAfter']
  status='PASS' if child.returncode==0 and now['status']=='PASS' and not diffs and unchanged else 'FAIL'
  row=dict(name=name,status=status,exitCode=child.returncode,command=command,sourceRoot=str(root),previousSummary=str(previous),legacyProjection=legacy,rows=len(now['rows']),rawValuesCompared=len(checks),rawValueChecks=checks,majorDifferences=diffs,sourceInputManifestUnchanged=unchanged,counts={k:now.get(k) for k in ('planned','registered','started','departed','knownTerminal','terminalConflicts','unknown','counts','statisticsDiagnosticOnly')},newFields='Registration, normalized contract and trusted-terminal qualifiers are explicit; no historical input was backfilled.',issues=[dict(case=r['input']['id'],issues=r['issues']) for r in now['rows'] if r['issues']])
 except Exception as e:row=dict(name=name,status='FAIL',exitCode=child.returncode,command=command,error=repr(e))
 reports.append(row)
csv=here.parent/'DeliveryStage2R1/Evidence/FrozenCombat/combat-results.csv';rawcsv=csv.read_bytes();csvproof=dict(path=str(csv),sha256=hashlib.sha256(rawcsv).hexdigest(),matchesReviewedBytes=hashlib.sha256(rawcsv).hexdigest()=='e3ea4b3358e5ea40af21f01e583e530764a4de80ec7b4c9410e81f4685ddef7d',scope='Original 26-row CSV preserved byte-for-byte; no new TTK metric or battle samples')
result=dict(status='PASS' if len(jobs)==10 and all(r['status']=='PASS' for r in reports) and csvproof['matchesReviewedBytes'] else 'FAIL',scope='Only read-only audit of old actual evidence. NOT a new Unity, battle, build or native test run.',jobs=reports,combatCsv=csvproof,source=[dict(path=str(source/n),sha256=hashlib.sha256((source/n).read_bytes()).hexdigest()) for n in ('MatrixEvidence.py','Summarize-Matrix.py')])
(a.output/'historical-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(status=result['status'],jobs=len(jobs),cases=sum(r.get('rows',0) for r in reports),failed=[r['name'] for r in reports if r['status']!='PASS'])));raise SystemExit(0 if result['status']=='PASS' else 1)
