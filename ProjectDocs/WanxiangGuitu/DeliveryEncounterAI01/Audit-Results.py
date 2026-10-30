"""Read-only audit; process exit, domain receipts and health observations stay separate."""
import pathlib,json,csv,collections,sys
root=pathlib.Path(sys.argv[1]);repo=pathlib.Path(sys.argv[2]);base=repo/'ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def array(x):return x if isinstance(x,list) else [x]
structured=[]
for rel in ['FinalRepro/repro.json','EncaiGuard-Run/guard.json','BAL02Rules-Run/rules.json','BAL02Math-Run/math.json','Aim01Rules-Run/rules.json','UX04CombatTiming-Run/combat01.json','Combat03Area-Run/area.json','LegacySaveStore/recovery-save.json','LegacyLoadStore/recovery-load.json']:
 j=read(root/rel);r=j.get('rows',j.get('checks',[]));structured.append(dict(path=rel,total=len(r),statuses=dict(collections.Counter(x['status'] for x in r))))
groups={}
for name,paths in {'matrix':['FinalBeforeMatrix/process-results.json','FinalMatrix/process-results.json'],'regression':['regression-processes.json','regression-continuation-processes.json'],'normalAndBuild':['normal-build-processes.json']}.items():
 values=[r for p in paths for r in array(read(root/p))];groups[name]=dict(total=len(values),statuses=dict(collections.Counter(r['status'] for r in values)),allActualExitZero=all(r.get('exitCode')==0 for r in values))
loss=collections.defaultdict(float)
for r in csv.DictReader((base/'HIT_EVENTS.csv').open(encoding='utf-8-sig')):loss[(r['phase'],r['sample'])]+=float(r['loss'])
checks=[]
for r in csv.DictReader((base/'ENCOUNTER_MATRIX.csv').open(encoding='utf-8-sig')):
 delta=abs(float(r['damage'])-loss[(r['phase'],r['sample'])]);checks.append(dict(phase=r['phase'],sample=r['sample'],healthCounter=float(r['damage']),tracedAppliedHP=loss[(r['phase'],r['sample'])],absoluteError=delta,status='PASS' if delta<=.01 else 'FAIL'))
fail=[r for r in checks if r['status']=='FAIL'];semanticFail=sum(r['statuses'].get('FAIL',0) for r in structured)
okay=not fail and not semanticFail and all(r['allActualExitZero'] and r['statuses']=={'PASS':r['total']} for r in groups.values()) and read(root/'input-binding.json')['status']=='PASS' and read(root/'PureBuild/release-inspection.json')['status']=='PASS'
result=dict(automatedScopeStatus='PASS' if okay else 'FAIL',independentReview='NOT_RUN',structured=structured,structuredTotal=sum(r['total'] for r in structured),processes=groups,healthReconciliation=dict(total=len(checks),failures=len(fail),maxAbsoluteError=max(r['absoluteError'] for r in checks),tolerance=.01,detail=checks),historicalFailuresPreserved=True,limitations=['Native U16/manual play and final balance NOT_RUN','Current pure release Player execution NOT_RUN','Natural dual-boss pressure NOT_RUN','Full performance, all Nav failures/jitter and all cancellation combinations NOT_RUN','D3D12 UNKNOWN/C15/cyan frame/Search historical roots UNRESOLVED','Initial regression orchestration interrupted safely; retained separately; continuations only cover unrun stages','EOF blank-line formatting warnings retained; diff-check is not PASS'])
(root/'result-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['automatedScopeStatus'],structuredTotal=result['structuredTotal'],processes=groups,traceFailures=len(fail),maxHealthError=result['healthReconciliation']['maxAbsoluteError']),ensure_ascii=False))
if not okay:raise SystemExit(1)
