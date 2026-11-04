from pathlib import Path
import json,hashlib,sys
root=Path(sys.argv[1]);repo=Path(__file__).resolve().parents[4]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
summary=read(root/'FinalAnalysis/summary.json');checks=[]
process_folders={'ResumeEditorData2':'ResumeEditor2','BossData1':'BossEditor1','LegacyFormalData4':'LegacyFormalFinal4','UpgradeEditorData1':'UpgradeEditor1'}
process_folders.update({f'Channel{x}Data2':f'Channel{x}Editor2' for x in ['Control','Normal','Ground','Picked']})
for trial in summary['trials']:
 folder=root/process_folders.get(trial['name'],trial['name']);receipts=list(folder.glob('*.exit.json'))
 if len(receipts)!=1:raise RuntimeError('ambiguous/missing exit '+str(folder))
 d=read(receipts[0]);ok=d.get('exitCode')==0 and d.get('forcedTermination') is False and bool(d.get('hostPid'))
 checks.append(dict(name=trial['name'],status='PASS' if ok else 'FAIL',processEvidence=str(receipts[0].relative_to(root)),sha256=sha(receipts[0]),actual=d))
inputs=read(root/'latest-source-inputs.json');actual=[]
for item in inputs['files']:
 p=repo/item['path'];h=sha(p);actual.append(dict(path=item['path'],source=item['sha256'],current=h,identical=h==item['sha256']))
checks.append(dict(name='source-freeze-still-identical',status='PASS' if all(x['identical'] for x in actual) else 'FAIL',files=len(actual)))
pure=root/'LatestPureBuild4/Release';bee=read(Path(str(pure/'WanxiangGuitu.exe')+'.bee.json'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
services=['EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting']
checks.append(dict(name='actual-bee-release',status='PASS' if bee['Development'] is False and all(bee['Services'].get(k) is False for k in services) else 'FAIL',services=bee['Services']))
data=dict(status='PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL',checks=checks,sourceFiles=actual)
(root/'delivery-consistency.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
print(data['status'],len(checks),'checks',len(actual),'product input files');sys.exit(data['status']!='PASS')
