"""Produce new FIX delivery metadata; never stage or rewrite original evidence."""
from pathlib import Path
import json,csv,hashlib,shutil,argparse,struct
R=Path.cwd();D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX';E=R/'Evidence/Runs04B2R2FIX'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def rel(p):return p.relative_to(R).as_posix()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def lines(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()] if p.is_file() else []
def bits(x):return '' if x is None else format(struct.unpack('<I',struct.pack('<f',x))[0],'08X') # reconstruct RECORDED Single only

def matrix():
 p=D/'PLAYER_RUN_MATRIX.csv';assert not p.exists();rows=[]
 for manifest in E.rglob('run-manifest.json'):
  if '_roots' in manifest.parts or 'original-root' in manifest.parts:continue
  m=load(manifest);q=m.get('result') or {};ev=manifest.parent;trans=lines(ev/'state-changes.jsonl');ui=next((x for x in trans if x.get('tag')=='UI-Evaluate'),None);commit=next((x for x in trans if x.get('tag')=='UI-Commit'),None);evaluation=q.get('evaluation') or (ui or {}).get('evaluation') or {};req=(ui or {}).get('request') or {};apBefore=(evaluation.get('before') or {}).get('attackPower');apAfter=(evaluation.get('after') or {}).get('attackPower');actual=None
  if commit:actual=json.loads(commit['after']['canonical']['AttackPower'])['attackPower']
  finalUI=manifest.parent.parent.name=='UI-A07';finalFloat=m.get('runId')=='UX04B2R2FIX-FLOAT-FINAL-001';target=req.get('target') or {};note=''
  if 'A01-accessory' in m['runId']:note='Historical FAIL: observer confused worn body0 with container total6; original unchanged'
  if 'board-insufficient' in m['runId'] and m.get('verdict')=='FAIL':note='Historical FAIL before Evaluate: real wheel overshoot, not product capacity verdict'
  if 'A05-illegal' in m['runId']:note='Historical FAIL: operation window crossed unchanged natural 5s autosave; all nine/random same, save bytes differ; original unchanged'
  rows.append({'startUtc':m.get('startUtc',''),'runId':m['runId'],'mode':m.get('mode',''),'batch':manifest.parent.parent.name,'finalUI':finalUI,'finalFloat':finalFloat,'verdict':m.get('verdict',''),'pid':m.get('pid'),'exitCode':m.get('exitCode'),'buildId':m['buildId'],'DLL_SHA256':m.get('dllSHA256',m.get('productDLLSHA256','')),'Driver_SHA256':m.get('driverSHA256',''),'EXE_SHA256':m.get('exeSHA256',''),'checks':q.get('checks',''),'passed':q.get('passed',''),'failed':q.get('failed',''),'candidateGearId':req.get('candidateGearId',evaluation.get('candidateGearId','')),'replacedGearId':req.get('replacedGearId',evaluation.get('replacedGearId','')),'targetX':target.get('x',''),'targetY':target.get('y',''),'rotation':req.get('rotation',''),'role':req.get('role',evaluation.get('role','')),'feasible':evaluation.get('feasible',''),'AP_before':apBefore,'AP_projected':apAfter,'AP_actual_after':actual,'AP_before_bits':bits(apBefore),'AP_projected_bits':bits(apAfter),'AP_actual_after_bits':bits(actual),'deltaAP_recorded':evaluation.get('deltaAttackPower',''),'oldContributionBefore':evaluation.get('oldContribution',''),'oldContributionAfter':evaluation.get('oldContributionAfter',''),'newContributionBefore':evaluation.get('newContributionBefore',''),'newContributionAfter':evaluation.get('newContribution',''),'swapped':evaluation.get('swapped',''),'oldReturnedToBag':evaluation.get('oldReturnedToBag',''),'operationResult':q.get('commitText',''),'failureReason':evaluation.get('reason',q.get('error','')),'allNineEqualEvaluate':(ui or {}).get('allNineEqual',''),'randomEqualEvaluate':(ui or {}).get('randomEqual',''),'saveEqualEvaluate':(ui or {}).get('saveEqual',''),'manifest':rel(manifest),'result':rel(ev/'result.json'),'input':rel(ev/'input-events.jsonl'),'stateChanges':rel(ev/'state-changes.jsonl') if (ev/'state-changes.jsonl').is_file() else '','note':note})
 rows.sort(key=lambda x:x['startUtc']);assert sum(r['finalUI'] for r in rows)==6 and all(r['verdict']=='PASS' for r in rows if r['finalUI'])
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 protection=E/'FINAL-PROTECTION/PROTECTION_SHA256.tsv';dest=D/'PROTECTION_SHA256.tsv';assert not dest.exists();shutil.copyfile(protection,dest)
 print(json.dumps({'actualRunsAllAttempts':len(rows),'finalUIRuns':6,'historicalFailures':sum(r['verdict']=='FAIL' for r in rows),'finalUIchecks':sum(int(r['checks']) for r in rows if r['finalUI'])},indent=2))

def index():
 p=D/'EVIDENCE/INDEX.json';assert not p.exists();need=['REPORT.md','FLOAT_FIX.md','REPLACEMENT_MODEL.md','CAPACITY_VALIDATION.md','ACCEPTANCE.md','PLAYER_RUN_MATRIX.csv','PROTECTION_SHA256.tsv','RISK_REGISTER.md'];assert all((D/x).is_file() for x in need)
 files=[{'path':rel(x),'bytes':x.stat().st_size,'sha256':sha(x)} for root in [D,E] for x in sorted(root.rglob('*')) if x.is_file() and x!=p and '_roots' not in x.parts]
 oldRefs=[R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/SUBMIT_WHITELIST.txt',R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/SUBMIT_WHITELIST.csv',R/'Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/result.json',R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2/EVIDENCE/INDEX.json'];refs=[{'path':rel(x),'sha256':sha(x),'bytes':x.stat().st_size} for x in oldRefs]
 manifests=[]
 for x in sorted(E.rglob('run-manifest.json')):
  if '_roots' in x.parts or 'original-root' in x.parts:continue
  m=load(x);manifests.append({'runId':m['runId'],'mode':m.get('mode'),'pid':m.get('pid'),'exitCode':m.get('exitCode'),'verdict':m.get('verdict'),'buildId':m['buildId'],'manifest':rel(x),'selectedFinal':x.parent.parent.name=='UI-A07' or m['runId']=='UX04B2R2FIX-FLOAT-FINAL-001'})
 obj={'scope':'UX-04-B2-R2-FIX only; old B2/R1/R2 evidence and 961 candidate allowlists unchanged','decision':'PASS_SCOPED_REPAIR_PENDING_OWNER_REVIEW','head':'95caf234256613d4a6e4f89a8ab0dc09c397c6b2','branch':'feature/ux-progression-04-b2','finalProductDLLSHA256':'ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1','finalReplacementDriverSHA256':'0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45','finalUIBuildId':'ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6','finalUIBatch':'Evidence/Runs04B2R2FIX/UI-A07','allAttempts':manifests,'artifacts':files,'immutableHistoricalReferences':refs,'metaPolicy':'Index excludes its own impossible self-hash; originals not edited to include these new files.'};p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'indexedArtifacts':len(files),'allActualRuns':len(manifests),'finalUI':6,'decision':obj['decision']},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['matrix','index']);a=ap.parse_args();matrix() if a.stage=='matrix' else index()
