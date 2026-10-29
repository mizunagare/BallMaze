"""Finite acceptance summary from this run's real artifacts, never inherited PASS."""
import pathlib,json,sys,collections
r=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((r/p).read_text(encoding='utf-8-sig'))
before=read('Before06/matrix.json')['rows'];after=read('After04/matrix.json')['rows'];migration=read('Migration03/migration.json')['rows']
def group(rows):return dict(collections.Counter(x['status'] for x in rows))
attempts=[]
for name in ['Before01','Before02','Before03','Before04','Before05','Before06','After01','After02','After03','After04','Migration01','Migration02','Migration03']:
 p=r/name
 if not p.exists():continue
 item={'id':name,'historical':name not in ['After04','Migration03'],'evidence':name}
 if (p/'matrix.json').exists():item['rows']=group(read(name+'/matrix.json')['rows'])
 if (p/'migration.json').exists():item['cases']=len(read(name+'/migration.json')['rows'])
 if (p/'results.json').exists():item['processResults']=read(name+'/results.json')
 item['exception']=(p/'exception.txt').exists() or (p/'migration-exception.txt').exists()
 attempts.append(item)
attempts.append({'id':'Migration-setup','status':'FAIL','layer':'tool setup','processLaunched':False,'processExitCode':None,'wrapperExitCode':1,'detail':'Output directory precreated for fixtures; existing runner refuses reuse. Preserved; changed fixture lookup, fresh Migration01 used.'})
good=lambda prefix:all(x['status']=='PASS' for x in after if x['id'].startswith(prefix)) and any(x['id'].startswith(prefix) for x in after)
checks=[]
def add(i,ok,evidence,layer='controlled Editor'):checks.append(dict(id=i,status='PASS' if ok else 'FAIL',layer=layer,evidence=evidence))
for i,prefix in [('T01','T-published'),('T02','T02-retry'),('T03','T-plan'),('T04','T-quantities'),('T05','T-identity'),('T06','T-missing'),('T07','T08/10-first-parse'),('T08','T08/10-first-committed'),('T09','T09-second-committed'),('T10','T08/10-first-pending'),('T11','T11-'),('T12','T12-pending')]:
 relevant={'T04':['T-outcome','T-quantities','T-checkpoint','T-source'],'T05':['T-revision','T-profile','T-identity'],'T06':['T-missing','T-corrupt'],'T09':['T09-second-committed','T09-second-pending','T09-second-parse']}.get(i,[prefix])
 add(i,all(good(p) for p in relevant),'After04/matrix.json')
add('MigrationGate',len(migration)==8 and all(all(x[k] for k in ['read','migrated','gateReleased','failureHeld','retryRecovered']) for x in migration),'Migration03/migration.json')
sequence=[json.loads(x) for x in (r/'verified-sequence.jsonl').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
add('FiveProcess',len(sequence)==5 and all(x['exitCode']==0 for x in sequence),'Bindings/verified-sequence.jsonl','independent Editor processes')
def process(phase):
 rows=read(phase+'/results.json');rows=[rows] if isinstance(rows,dict) else rows;return bool(rows) and all(x['status']=='PASS' and not x.get('timedOut',False) for x in rows)
add('RuntimeEntities',process('RuntimeAudit'),'VerifiedShared/runtime-audit.txt')
add('Entry',process('EntryRun'),'EntryRun-Store/entry-checks.txt')
add('Catalog',all(process('Catalog-'+m) for m in ['Run','Resume','Interrupt','Recover']),'Catalog-*/results.json','independent Editor processes')
reg=read('Regression/results.json')
for ident,name in [('Input','Input01Rules.Run'),('Observation','S2R1ObservationProbe.Run'),('Boss','B07Combat.Run')]:add(ident,any(x['name']==name and x['status']=='PASS' and x.get('exitCode')==0 and not x.get('timedOut') for x in reg),'Regression/results.json')
ai=[x for x in reg if x['name'].startswith('AI.')];add('NormalAI',len(ai)==3 and all(x['status']=='PASS' and x.get('exitCode')==0 and not x.get('timedOut') for x in ai),'Regression/Normal-Gather','Editor normal AI, not human')
b=read('Build/build-report-messages.json');add('NonDevelopmentBuild',b['result']=='Succeeded' and b['errors']==0 and b['options']=='None','Build/build-report-messages.json','non-development Windows build only')
add('ReleaseBoundary',read('Build/release-inspection.json')['status']=='PASS','Build/release-inspection.json','read-only PE, not Player run')
add('Protection',read('protection-check.json')['unchanged'],'Bindings/protection-check.json','file hashes')
deferred=[{'id':x,'status':'NOT_RUN'} for x in ['DedicatedAcceptancePlayer','ReleasePlayerRuntime','NativeU16','IndependentHuman','PerformanceBudget','AllTerminalAckPermutations']]+[{'id':x,'status':'UNRESOLVED'} for x in ['D3D12_UNKNOWN','EditorCyanFrame','EditorSearch','JobTempAlloc','OldC15RootCause']]
data={'scope':'R1 limited acceptance, not independent review or full game release','attempts':attempts,'findings':[{'id':x,'state':'FIXED','review':'AWAITING_FIXED_SHA_REVIEW'} for x in ['RL01-RV-01','RL01-RV-02']],'current_acceptance':checks,'current_counts':group(checks),'deferred':deferred,'deferred_counts':group(deferred),'before06_rows':group(before),'after04_rows':group(after),'migration03_cases':len(migration),'build':{k:b[k] for k in ['result','errors','warnings','seconds','options']}}
(out/'status.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
import csv
with (out/'acceptance.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['id','status','layer','evidence']);w.writeheader();w.writerows(checks)
print(data['current_counts'],data['deferred_counts'],data['before06_rows'],data['after04_rows'])
if any(x['status']=='FAIL' for x in checks):raise SystemExit('Current limited acceptance contains FAIL; original status preserved')
