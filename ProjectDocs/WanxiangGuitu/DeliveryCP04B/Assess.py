"""Read-only CP04B assessment. Process exit is never the gameplay verdict."""
import argparse,collections,csv,hashlib,json,subprocess,statistics
from pathlib import Path
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
lines=lambda p:[json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('repo',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.root;o=a.output;o.mkdir(exist_ok=False);checks=[];sources=[];case_rows=[]
def C(n,v,d=''):checks.append(dict(name=n,status='PASS' if v else 'FAIL',detail=d))
def player(s):
 paths=[x.parent for x in r.rglob('CP04BPlayer'+s+'.command.json') if 'RunnerControl' not in x.parts];assert len(paths)==1,(s,paths);return paths[0]
paths={'EditorHistorical':r/'AfterHistorical','PlayerHistorical':player('Historical'),'EditorMatrix':r/'AfterMatrix','PlayerMatrix':player('Matrix'),'EditorWall':r/'AfterWall','PlayerWall':player('Wall'),'EditorBoundary':r/'AfterBoundary','PlayerBoundary':player('Boundary'),'EditorLifecycle':r/'AfterLifecycle','PlayerLifecycle':player('Lifecycle'),'EditorDeath':r/'AfterDeath','PlayerDeath':player('Death'),'PlayerPerf':player('Perf')}
(o/'run-paths.json').write_text(json.dumps({k:str(v.relative_to(r)) for k,v in paths.items()},indent=2),encoding='utf-8')
# Actual runner/native/command/desktop association for every completed output, even intermediate attempts.
for f in sorted(r.rglob('results.json')):
 if any(x in f.parts for x in ['Reference','P']):continue
 rows=load(f);rows=rows if isinstance(rows,list) else [rows]
 for row in rows:
  if not isinstance(row,dict) or not isinstance(row.get('command'),list):continue
  prefix=f.parent/row['name'];cmdpath=Path(str(prefix)+'.command.json');nativepath=Path(str(prefix)+'.exit.json');desktopPath=Path(str(prefix)+'.desktop-process.json')
  try:
   cmd=load(cmdpath);native=load(nativepath);desktop=load(desktopPath);valid=row['status']=='PASS' and type(row['exitCode']) is int and row['exitCode']==native['exitCode']==0 and row['timedOut'] is False and native['forcedTermination'] is False and type(native['hostPid']) is int and native['hostPid']==cmd['hostPid'] and Path(cmd['exe']).resolve()==Path(row['command'][0]).resolve()==Path(desktop['exe']).resolve() and cmd['arguments']==row['command'][1:] and Path(row['log']).resolve()==prefix.resolve() and desktop['inputDesktopActive'] is False
  except (OSError,KeyError,TypeError):valid=False
  C('process '+str(f.parent.relative_to(r))+' '+row['name'],valid)
  sources.append(dict(run=str(f.parent.relative_to(r)),name=row['name'],status=row['status'],exitCode=row['exitCode'],timedOut=row['timedOut'],files=[dict(path=str(p.relative_to(r)),sha256=digest(p)) for p in [f,cmdpath,nativepath,desktopPath] if p.is_file()]))
for layer in ['Editor','Player']:
 d=paths[layer+'Historical'];q=load(d/'presentation.json');C(layer+' four weapons 293 real assertions',dict(collections.Counter(x['status'] for x in q['rows']))==dict(PASS=293) and len(q['rows'])==293)
 ev=lines(d/'events.jsonl')
 for case,attack in [('w2-s0-near',11),('w2-s1-near',14)]:
  contacts=[x for x in ev if x['attack']==attack and x['shot']==1 and x['stage'] in ('sweep-contact','initial-overlap') and x['entity']==case];damage=[x for x in ev if x['stage']=='Damage' and x['entity']==case];C(layer+' historical real Collision/Damage '+case,len(contacts)==1 and len(damage)==1 and damage[0]['applied']==(33 if attack==11 else 60))
 old={(x['attack'],x['shot']):x for x in lines(Path('I:/WGCombat/CP03-1031-A/Before2/events.jsonl')) if x['stage']=='spawn'};new={(x['attack'],x['shot']):x for x in ev if x['stage']=='spawn'};pair=[]
 for key,x in old.items():
  y=new.get(key);pair.append(dict(attack=key[0],shot=key[1],originEqual=y is not None and x['from']==y['from'],directionEqual=y is not None and x['aim']==y['aim'],beforeOrigin=x['from'],afterOrigin=y['from'] if y else None,beforeDirection=x['aim'],afterDirection=y['aim'] if y else None))
 C(layer+' original24 origin unchanged / exactly two authorized directions',len(pair)==24 and all(x['originEqual'] for x in pair) and [(x['attack'],x['shot']) for x in pair if not x['directionEqual']]==[(11,1),(14,1)])
 (o/(layer+'-paired24.json')).write_text(json.dumps(pair,indent=2),encoding='utf-8')
 before={c['id']:c for c in load(r/'BeforeMatrix/diagnosis.json')['cases']}
 for group,count in [('Matrix',38),('Wall',2),('Boundary',6)]:
  q=load(paths[layer+group]/'diagnosis.json');C(layer+' '+group+' count',len(q['cases'])==count)
  for c in q['cases']:
   shots=[s for s in q['shots'] if s['caseId']==c['id']];ts=[t for t in q['trace'] if t['caseId']==c['id']];ds=[d for d in q['damage'] if d['caseId']==c['id']];hit=next((t for t in ts if t['stage'] in ('initial-overlap','initial-overlap-solid','sweep-contact')),None)
   if group=='Matrix':expected=(60 if c['skill'] else 33) if c['distance']==1.5 and c['camera'] in ('historical-right','left') else before[c['id']]['hpLoss']
   elif group=='Wall':expected=0
   else:expected=(60 if c['skill'] else 33) if c['occlusion']=='multi-collider' else 0
   selected=True;prediction=True
   for s in shots:
    legal=[v for v in s['rayHits'] if v['legal']];selected=selected and s['cameraCollider']==(legal[0]['name'] if legal else '')
    identity=(s['predictedContact'].get('owner') or s['predictedContact'].get('name')) if s['hasContact'] else None
    actual=(hit.get('owner') or hit.get('collider')) if hit else None;prediction=prediction and identity==actual
    if c['distance']<0:prediction=prediction and sum(s['direction'][k]*s['rayDirection'][k] for k in ('x','y','z'))>.999
   ok=c['accepted'] and c['spawns']==1 and c['remainingProjectiles']==0 and abs(c['hpLoss']-expected)<.001 and abs(sum(x['applied'] for x in ds)-c['hpLoss'])<.001 and len(ds)<2 and selected and prediction
   C(layer+' '+group+' '+c['id'],ok,'expectedLoss='+str(expected)+' actualLoss='+str(c['hpLoss'])+' selected='+str(selected)+' prediction='+str(prediction))
   case_rows.append(dict(layer=layer,group=group,id=c['id'],status='PASS' if ok else 'FAIL',hpLoss=c['hpLoss'],expected=expected,firstCollision=hit,reasons=[s['reason'] for s in shots]))
 for group in ['Lifecycle','Death']:
  q=load(paths[layer+group]/'lifecycle.json')
  for row in q['rows']:C(layer+' '+group+' '+row['name'],row['status']=='PASS')
for name in ['acceptance','pure']:
 q=load(r/(name+'-metadata.json'));C(name+' PE metadata and release exclusion',q['status']=='PASS' and not q['bad'])
for folder in ['AcceptanceBuildShippingInput','PureBuildShippingInput']:
 q=load(r/folder/'build.json');C(folder+' nondevelopment build',q['result']=='Succeeded' and q['errors']==0 and q['options']=='None')
# Protect all original files except the one explicitly authorized product path in this branch.
allowed='Assets/CombatPrototype/CombatAim.cs';before=load(r/'protected-before.json');diff=[]
for x in before:
 f=Path(x['root'])/x['path'];changed=not f.is_file() or digest(f)!=x['sha256'];permitted=Path(x['root']).resolve()==a.repo.resolve() and x['path']==allowed
 if changed:diff.append(dict(**x,authorized=permitted,afterSHA256=digest(f) if f.is_file() else None))
C('2329 protected inputs only authorized Aim changed',len(before)==2329 and len(diff)==1 and diff[0]['authorized'])
C('user worktree status unchanged',subprocess.check_output(['git','-C','H:/unity/WanxiangGuitu','status','--porcelain'])==(r/'user-status-before.txt').read_bytes())
productDiff=subprocess.check_output(['git','-C',str(a.repo),'diff','72db192a527bd256e2ba18cd7ab334d8334051da','--name-only','--','Assets','Packages','ProjectSettings']).decode().splitlines();C('only CombatAim product diff',productDiff==[allowed])
(o/'protection.json').write_text(json.dumps(dict(count=len(before),changes=diff,productDiff=productDiff),indent=2),encoding='utf-8')
control=r/'RunnerControl'
C('runner routing control remains flat',all((control/('Player'+k)/'diagnosis.json').is_file() for k in ['Wall','Boundary']))
for group,count in [('Wall',2),('Boundary',6)]:
 q=load(control/('Player'+group)/'diagnosis.json');ok=len(q['cases'])==count
 for c in q['cases']:
  expected=(60 if c['skill'] else 33) if c['occlusion']=='multi-collider' else 0
  damage=[d for d in q['damage'] if d['caseId']==c['id']]
  ok=ok and c['accepted'] and c['spawns']==1 and c['remainingProjectiles']==0 and c['hpLoss']==expected and sum(x['applied'] for x in damage)==expected
 C('repaired runner '+group+' semantic control',ok)
C('measured query clone exact transformations',all(x['exactTransform'] for x in load(r/'counter-clone-audit.json')))
binding=load(r/'product-input-binding.json')
checks.append(dict(name='isolated post-build input byte equivalence',status='UNRESOLVED' if binding['mismatch'] else 'PASS',detail='Five isolated Unity-written config differences retained; no claim of original byte-equivalent build inputs: '+','.join(x['path'] for x in binding['mismatch'])))
checks.append(dict(name='per-Solve allocation bytes',status='NOT_RUN',detail='Known 65536-byte allocation returns zero via thread API; raw zero is invalid measurement, never zero-allocation PASS'))
checks.append(dict(name='native input',status='NOT_RUN',detail='Controlled API tests only'))
checks.append(dict(name='independent human experience',status='NOT_RUN',detail='No human playtest'))
runnerFailures=[]
for f in r.rglob('results.json'):
 if any(x in f.parts for x in ['Reference','P']):continue
 data=load(f);data=data if isinstance(data,list) else [data]
 runnerFailures += [dict(path=str(f),row=x) for x in data if x.get('status')=='FAIL']
C('all runner note failures propagate',not runnerFailures,str(runnerFailures))
fixtureChecks=[]
for f in r.rglob('fixture-copy.json'):
 if 'Reference' in f.parts:continue
 x=load(f);fixtureChecks.append(x['sourceSHA256'].lower()==x['copiedSHA256'].lower()==digest(Path(x['source'])))
C('nine verbatim synthetic fixtures and original unchanged',len(fixtureChecks)==9 and all(fixtureChecks))
summary=dict(overallStatus='FAIL' if any(x['status']=='FAIL' for x in checks) else 'BLOCKED' if any(x['status']=='UNRESOLVED' for x in checks) else 'INCOMPLETE' if any(x['status']=='NOT_RUN' for x in checks) else 'PASS',counts=dict(collections.Counter(x['status'] for x in checks)),checks=checks,cases=case_rows,processes=sources,limitations=dict(perSolveGC='NOT_RUN: calibrated thread allocation API returns zero for known allocation; raw retained',nativeInput='NOT_RUN',human='NOT_RUN',independentReview='PENDING',historicalEngine='UNRESOLVED'))
(o/'assessment.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
with (o/'checks.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,['name','status','detail']);w.writeheader();w.writerows(checks)
print(json.dumps(summary['counts']));print([x for x in checks if x['status']=='FAIL']);raise SystemExit({'PASS':0,'FAIL':1,'BLOCKED':2,'INCOMPLETE':3}[summary['overallStatus']])
