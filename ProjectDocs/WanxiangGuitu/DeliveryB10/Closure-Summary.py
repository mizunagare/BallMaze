"""Summarize one ended All; never treats coordinator zero as acceptance."""
import argparse,collections,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--input-commit',required=True);a=p.parse_args()
rows=json.loads((a.run/'results.json').read_text('utf-8-sig'))
if not any(r['name']=='report.finalized' and r['status']=='PASS' for r in rows):raise ValueError('Ended All required')
if a.output.exists():raise ValueError('Fresh result receipt required')
def expected(r):return r['scope']=='harness-negative' and ((r['name']=='probe.nonzero' and r['exitCode']==7 and not r['timedOut']) or (r['name']=='probe.timeout' and r['timedOut']))
failures=[r for r in rows if r['status']=='FAIL'];unexpected=[r for r in failures if not expected(r)]
normal=[dict(name=r['name'],status=r['status'],exitCode=r['exitCode'],timedOut=r['timedOut']) for r in rows if r['name'].startswith('normal-ai.')]
title=[dict(name=r['name'],status=r['status'],exitCode=r['exitCode']) for r in rows if r['name'].startswith('B09-TitleVerify.')]
child_reports=list((a.run/'ControlledPlayer').glob('*/results.json'));direct=a.run/'ControlledPlayer/results.json';child_reports+=([direct] if direct.is_file() else []);children=[]
for f in child_reports:
 rs=json.loads(f.read_text('utf-8-sig'));children.append(dict(root=str(f.parent),counts=dict(collections.Counter(r['status'] for r in rs)),failures=[r for r in rs if r['status']=='FAIL']))
requiredCoverage=dict(normal21='PASS' if len(normal)==21 and all(r['status']=='PASS' for r in normal) else 'NOT_RUN',title8='PASS' if len(title)==8 and all(r['status']=='PASS' for r in title) else 'NOT_RUN',controlledPlayer='PASS' if len(children)==1 and not children[0]['failures'] and children[0]['counts'].get('PASS')==15 else 'NOT_RUN')
summary=(a.run/'Build/Release/BuildSummary.txt').read_text('utf-8-sig');build=dict(line.split('=',1) for line in summary.splitlines() if '=' in line)
files=[]
for rel in ['Build/Release/WanxiangGuitu.exe','Build/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll']:
 f=a.run/rel;files.append(dict(path=rel,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
performance=[]
for f in (a.run/'ControlledPlayer').rglob('b10-performance.json'):
 if 'Project' in f.relative_to(a.run).parts:continue
 performance.append(dict(path=f.relative_to(a.run).as_posix(),measurements=json.loads(f.read_text('utf-8-sig'))))
gate_path=a.run/'b10-runtime-log-gate.json';gate=json.loads(gate_path.read_text('utf-8-sig')) if gate_path.is_file() else {'status':'NOT_RUN','logs':[],'findings':[]}
result=dict(runtimeLogGate=dict(status=gate['status'],logs=len(gate['logs']),findings=len(gate['findings'])),inputCommit=a.input_commit,run=str(a.run),mainCounts=dict(collections.Counter(r['status'] for r in rows)),expectedProbeFailures=[r['name'] for r in failures if expected(r)],unexpectedFailures=unexpected,requiredCoverage=requiredCoverage,normalAI=normal,formalTitle=title,controlledPlayer=children,build=build,buildHashes=files,performance=performance,scope='No inherited results; child step counts separate, never added to main counts. AI uses Editor test devices, not native Windows UI. Performance includes driver/capture and inactive-desktop overhead.',overall='FAIL' if unexpected or any(c['failures'] for c in children) else 'UNRESOLVED',nativeUI='NOT_RUN',humanReadability='NOT_RUN')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(counts=result['mainCounts'],expected=len(result['expectedProbeFailures']),unexpected=len(unexpected),normalStages=len(normal),titleCases=len(title),childReports=len(children),overall=result['overall'])))
raise SystemExit(1 if unexpected or any(c['failures'] for c in children) else 0)
