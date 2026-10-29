"""Layer actual current assertions, finite observations, process receipts and immutable failures."""
import pathlib,json,csv,collections,sys
root=pathlib.Path(sys.argv[1]);out=root/'SummaryFinal';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
specs=[('new-negative-recheck','TrackedReplay/RulesBaseline/baseline-checks.json','rows'),('curve-lifecycle-v9','TrackedCompatibility/rules-run.json','rows'),('new-process-v9','TrackedCompatibility/rules-resume.json','rows'),('UX02-graphics','UX02GraphicsRetry/ux02.json','checks'),('weapon-timing','Final/CombatTiming/combat01.json','checks'),('full-recovery','Final/RecoveryMatrix/matrix.json','rows'),('area-projectile','Final/RangedArea/area.json','checks'),('input','Final/Input/input01-rules.json','checks')]
rows=[]
for group,rel,key in specs:
 d=read(root/rel)
 for i,r in enumerate(d[key]):
  if isinstance(r,str):r=dict(name=r,status=d['status'])
  rows.append(dict(group=group,index=i,name=r.get('name',r.get('check','')),status=r['status'],detail=r.get('detail',''),evidence=rel))
with (root/'Final/MeleeContracts/contracts.csv').open(encoding='utf-8-sig',newline='') as f:
 for i,r in enumerate(csv.DictReader(f)):rows.append(dict(group='weapon-quality',index=i,name=f"weapon {r['weapon']} quality {r['quality']}",status=r['status'],detail=json.dumps(r),evidence='Final/MeleeContracts/contracts.csv'))
with (out/'assertions.csv').open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
history=[]
for p in root.rglob('results.json'):
 if 'P' in p.relative_to(root).parts or 'DeferredUserInputs' in p.relative_to(root).parts:continue
 data=read(p)
 for r in data if isinstance(data,list) else [data]:
  if isinstance(r,dict) and 'exitCode' in r:history.append(dict(path=p.relative_to(root).as_posix(),**r))
builds=[]
for rel in ['Final/Build','TrackedFinal/Build']:
 d=read(root/rel/'build-report-messages.json');builds.append(dict(folder=rel,**{k:v for k,v in d.items() if k!='messages'}))
 with (root/rel/'warnings.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['index','step','type','text']);w.writeheader();w.writerows(dict(index=i,**m) for i,m in enumerate(d['messages']) if m['type'] in ('Warning','Error'))
summary=dict(overall='UNRESOLVED',scope='420 enumerable current assertions exclude finite battle rows and marker-only suites; history includes expected pre-fix negatives and tool failure. No All-green, native or human claim.',currentAssertionCounts=dict(collections.Counter(r['status'] for r in rows)),groups={g:dict(collections.Counter(r['status'] for r in rows if r['group']==g)) for g in sorted({r['group'] for r in rows})},paired=read(out/'paired-check.json'),markerSuites=[dict(folder='Final/Boss-'+m,**read(root/('Final/Boss-'+m)/'results.json')) for m in ['Run','Resume','PendingResume','CommittedResume']]+[dict(folder='Final/'+m,**read(root/('Final/'+m)/'results.json')) for m in ['BossEconomy','RandomStreams']],normalAI={phase:[read(root/phase/'Normal-Gather'/('process-result-'+m+'.json')) for m in ['Normal','Resume','FinalResume']] for phase in ['Final','TrackedFinal']},builds=builds,protection=read(root/'protection-check.json')['status'],sourceBinding=read(root/'source-bindings.json')['status'],historyExecutionCounts=dict(collections.Counter(r['status'] for r in history)),historyExecutions=history,notRun=['Native keyboard/mouse U16','Independent human playtest','Final difficulty/balance approval','Performance benchmark'],unresolved=['UI01 D3D12 UNKNOWN','Editor cyan frame','Editor.Search','JobTempAlloc','old C15','old UX04 GPU fatal','old UX04 AI phase31 stall','engine internals of unsupported no-graphics render-request crash; launcher corrected, no product root-cause claim'])
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'assertions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(summary['currentAssertionCounts'],summary['historyExecutionCounts'],summary['overall'])
if any(r['status']!='PASS' for r in rows) or summary['sourceBinding']!='PASS' or summary['protection']!='PASS':raise SystemExit(1)
