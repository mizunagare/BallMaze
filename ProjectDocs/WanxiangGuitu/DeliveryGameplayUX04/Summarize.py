"""Keep current assertion totals separate from immutable failed attempts."""
import pathlib,json,csv,collections,sys
root=pathlib.Path(sys.argv[1]);out=root/'Summary';out.mkdir(exist_ok=True)
specs=[('target','Shared07/matrix-target.json','rows'),('matrix','Shared07/matrix-run.json','rows'),('camp-resume','Shared07/matrix-resume.json','rows'),('run-craft-resume','Shared07/matrix-runcraftresume.json','rows'),('scroll','Scroll08/scroll.json','rows'),('timing-domain','TimingDomain-Store/combat01.json','checks'),('real-ui-callback','Final3/UI/result.json','rows'),('UX02','Final2/UX02Regression/ux02.json','checks'),('ranged','Final2/RangedArea/area.json','checks'),('recovery','Final2/RecoveryMatrix/matrix.json','rows'),('input','Final2/Input/input01-rules.json','checks')]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
rows=[]
for group,path,key in specs:
 data=read(root/path)
 for i,r in enumerate(data[key]):
  if isinstance(r,str):r=dict(name=r,status=data['status'])
  rows.append(dict(group=group,index=i,name=r.get('name',r.get('check','')),status=r['status'],detail=r.get('detail',''),evidence=path))
with (root/'Final2/MeleeContracts/contracts.csv').open(encoding='utf-8-sig',newline='') as f:
 for i,r in enumerate(csv.DictReader(f)):rows.append(dict(group='quality-contracts',index=i,name=f"weapon {r['weapon']} quality {r['quality']}",status=r['status'],detail=json.dumps(r),evidence='Final2/MeleeContracts/contracts.csv'))
with (out/'assertions.csv').open('w',encoding='utf-8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
history=[]
for path in root.rglob('results.json'):
 if 'P' in path.relative_to(root).parts:continue
 data=read(path)
 for r in data if isinstance(data,list) else [data]:
  if isinstance(r,dict) and 'exitCode' in r:history.append(dict(path=path.relative_to(root).as_posix(),**r))
summary=dict(overall='UNRESOLVED',finalAssertionCounts=dict(collections.Counter(r['status'] for r in rows)),groups={g:dict(collections.Counter(r['status'] for r in rows if r['group']==g)) for g,_,_ in specs}|{'quality-contracts':dict(collections.Counter(r['status'] for r in rows if r['group']=='quality-contracts'))},normalAI=[read(root/f'Final3/Normal-Gather/process-result-{m}.json') for m in ['Normal','Resume','FinalResume']],build={k:v for k,v in read(root/'Final3/Build/build-report-messages.json').items() if k!='messages'},notRun=['Native U16/keyboard-mouse acceptance','Independent human playtest','Performance measurement','Final release Player native UI operations in this batch'],unresolved=['Historical UI01 UNKNOWN/cyan/Search/JobTempAlloc/C15 retained','Original normal-AI continuation stopped at phase31, cause unconfirmed','Editor D3D12 unrecoverable GPU error, exit -1073740771; later domain pass does not close it'],historyExecutionCounts=dict(collections.Counter(r['status'] for r in history)),historyExecutions=history)
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'assertions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(summary['finalAssertionCounts'],summary['overall'])

timeline=[r for r in rows if r['group'] in ('target','matrix','camp-resume','run-craft-resume') and any(k in r['name'] for k in ('target','craft','tutorial','payment','profile','checkpoint'))]
(out/'goal-timeline.json').write_text(json.dumps(dict(scope='Actual assertion order, not a fabricated per-event time trace; timestamps were not captured per assertion',steps=timeline),ensure_ascii=False,indent=2),encoding='utf-8')
matrix=read(root/'Shared07/matrix-run.json')['matrix']
with (out/'range-matrix.csv').open('w',encoding='utf-8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(matrix[0]));writer.writeheader();writer.writerows([{k:json.dumps(v) if isinstance(v,dict) else v for k,v in r.items()} for r in matrix])
