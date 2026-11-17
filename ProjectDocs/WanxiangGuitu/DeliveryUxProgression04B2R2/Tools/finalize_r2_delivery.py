"""Generate only new R2 delivery metadata after the mandatory float stop."""
from pathlib import Path
import json,csv,hashlib
R=Path.cwd();D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2';E=R/'Evidence/Runs04B2R2/SESSION-20261116-R2-01';run=E/'UX04B2R2-FLOAT-001';m=json.loads((run/'run-manifest.json').read_text(encoding='utf-8'));q=m['result']
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def rel(p):return p.relative_to(R).as_posix()
assert m['verdict']=='BIT_DIFFERENCE_STOP' and m['exitCode']==21 and q['ulpDifference']==1
assert q['oldActualBitsHex']=='418B999A' and q['newActualBitsHex']=='418B9999' and q['tracesMatch'] and q['identityMatches']
fields=['runId','scenario','status','buildId','PID','exitCode','DLL_SHA256','EXE_SHA256','Driver_SHA256','oldBits','newBits','ULP','result','manifest','reason']
p=D/'PLAYER_RUN_MATRIX.csv';assert not p.exists()
rows=[{'runId':m['runId'],'scenario':'R03 same-Mono three-item comparison','status':m['verdict'],'buildId':m['buildId'],'PID':m['pid'],'exitCode':m['exitCode'],'DLL_SHA256':m['dllSHA256'],'EXE_SHA256':m['exeSHA256'],'Driver_SHA256':m['driverSHA256'],'oldBits':q['oldActualBitsHex'],'newBits':q['newActualBitsHex'],'ULP':q['ulpDifference'],'result':rel(run/'result.json'),'manifest':rel(run/'run-manifest.json'),'reason':'Actual 1 ULP difference triggers mandatory STOP; not bit-consistency PASS'}]
for name in ['A accessory replacement','B arms replacement','C main-weapon replacement','D insufficient board space','E legal swap','F illegal swap']:
    rows.append({'runId':'','scenario':name,'status':'NOT_RUN_STOP_GATE','reason':'No Run created: stop after actual Mono float difference; R01 not implemented'})
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
index=D/'EVIDENCE/INDEX.json';assert not index.exists();index.parent.mkdir(parents=True,exist_ok=True)
evidence=[{'path':rel(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(E.rglob('*')) if p.is_file() and '_roots' not in p.parts]
delivery=[{'path':rel(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p!=index]
old=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/SUBMIT_WHITELIST.csv'
snapshot=Path('I:/unity/WanxiangGuitu-UX04B2R2-snapshot-20261116-1459')
obj={'scope':'R2 STOP-GATE evidence only; R01 repair and six UI Runs NOT performed','decision':'BIT_DIFFERENCE_STOP_WAIT_FOR_SEPARATE_AUTHORIZATION','actualRunCount':1,'actualRun':{'runId':m['runId'],'PID':m['pid'],'exitCode':m['exitCode'],'buildId':m['buildId'],'verdict':m['verdict'],'result':rel(run/'result.json'),'manifest':rel(run/'run-manifest.json')},'notRunScenarios':[r['scenario'] for r in rows[1:]],'floatResult':{'oldBits':q['oldActualBitsHex'],'newBits':q['newActualBitsHex'],'ULP':q['ulpDifference'],'runtime':q['monoDisplayName'],'unityVersion':q['unityVersion'],'isEditor':q['isEditor']},'frozen961Ledger':{'path':rel(old),'sha256':sha(old),'modified':False},'preR2Snapshot':{'path':str(snapshot),'manifestSHA256':sha(snapshot/'PRECHANGE_R2_SHA256.json')},'evidenceFiles':evidence,'deliveryFiles':delivery,'historyPolicy':'Original B2/R1 files, failures, indexes and 961 allowlist untouched. This index records new artifacts only.'}
index.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'actualRuns':1,'notRunScenarios':6,'evidenceFiles':len(evidence),'deliveryFiles':len(delivery),'decision':obj['decision']},indent=2))
