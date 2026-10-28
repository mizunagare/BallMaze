"""Read-only summary of fixed UX02 attempts; never changes saves or historical results."""
import argparse,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=a.root
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def checks(name,file='ux02.json'):
 rows=read(r/name/file)['checks'];return dict(attempt=name,checks=len(rows),PASS=sum(x['status']=='PASS' for x in rows),FAIL=sum(x['status']=='FAIL' for x in rows),scope=read(r/name/file).get('scope'))
build=read(r/'FinalBuildR4/build-report-messages.json');exe=r/'FinalBuildR4/Release/WanxiangGuitu.exe';dll=r/'FinalBuildR4/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'
hashof=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
normal=[read(r/'AffectedFinal/Normal-Gather'/('process-result-'+m+'.json')) for m in ['Normal','Resume','FinalResume']]
result=dict(startSha='da118c245a04f32909ce4c83b45e239ce2e0d2df',finalRules=checks('FinalRulesR4'),finalCatalog=checks('FinalExtrasRunR4'),finalNewProcess=checks('FinalExtrasResumeR4'),combat=checks('CombatBatchFinal','combat01.json'),negativeBefore=[checks('Before'),checks('Before2')],affectedFramework=read(r/'AffectedFinal/results.json'),normalAI=normal,build=dict(result=build['result'],options=build['options'],errors=build['errors'],warnings=build['warnings'],seconds=build['seconds'],exeSha256=hashof(exe),assemblySha256=hashof(dll),runtimeDriverAbsent=all(t not in dll.read_bytes() for t in [b'PlayerAcceptanceDriver',b'UX02Checks',b'UnityEditor'])),nativeUI='NOT_RUN',independentHuman='NOT_RUN',longStress='NOT_RUN',fullPerformance='NOT_RUN',historicalUnresolved=['C15','D3D12 UNKNOWN','Editor cyan frame','Editor.Search','JobTempAlloc','old extra Editor startup'],note='Independent layers; no summed global assertion pass rate. Old failures retained.')
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:result[k] for k in ['finalRules','finalCatalog','finalNewProcess','build']},ensure_ascii=False))
if any(result[k]['FAIL'] for k in ['finalRules','finalCatalog','finalNewProcess','combat']) or build['errors'] or build['result']!='Succeeded' or any(x['exitCode']!=0 or x['timedOut'] for x in normal):raise SystemExit(1)
