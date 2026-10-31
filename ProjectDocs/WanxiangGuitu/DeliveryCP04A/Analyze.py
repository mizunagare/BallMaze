"""Readonly geometry/event analysis. Never applies Damage or alters Unity inputs."""
import argparse,collections,csv,hashlib,json,math
from pathlib import Path
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
lines=lambda p:[json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def xyz(v):return [v[k] for k in ('x','y','z')]
def sub(a,b):return [x-y for x,y in zip(xyz(a),xyz(b))]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.root;a.output.mkdir(exist_ok=False)
hist=lines(r/'Historical/aim-diagnosis.jsonl');events=lines(r/'Historical/events.jsonl');history=[]
for x in hist:
 e=[y for y in events if y['attack']==x['attack'] and y['shot']==x['shot']];contact=next((y for y in e if y['stage'] in ('sweep-contact','initial-overlap','initial-overlap-solid')),None)
 history.append(dict(target=x['target'],cameraPosition=x['cameraPosition'],rayOrigin=x['cameraOrigin'],rayDirection=x['cameraDirection'],muzzle=x['rawMuzzle'],spawnOrigin=x['origin'],spawnDirection=x['direction'],surface=x['rawCameraSurface'],surfaceProjection=x['surfaceForwardFromOrigin'],computedProjection=dot(sub(x['rawCameraSurface'],x['origin']),xyz(x['cameraDirection'])),firstCollision=contact,actualDamage=[y for y in events if y['stage']=='Damage' and y['entity']==x['target']],flightEvents=sum(y['stage']=='flight' for y in e),reason=x['reason']))
q=load(r/'Matrix/diagnosis.json');cases=[]
for c in q['cases']:
 shots=[s for s in q['shots'] if s['caseId']==c['id']];trace=[t for t in q['trace'] if t['caseId']==c['id']];damage=[d for d in q['damage'] if d['caseId']==c['id']]
 collision=next((t for t in trace if t['stage'] in ('sweep-contact','initial-overlap','initial-overlap-solid')),None)
 cases.append(dict(**c,reasons=sorted(set(s['reason'] for s in shots)),firstCollision=collision,damageEvents=len(damage),observedApplied=sum(d['applied'] for d in damage),flightEvents=sum(t['stage']=='flight' for t in trace),projectileSpeeds=sorted(set(s['speed'] for s in shots)),projections=[s['surfaceProjection'] for s in shots],cameraPositions=[s['cameraPosition'] for s in shots],muzzles=[s['muzzle'] for s in shots],directions=[s['direction'] for s in shots]))
result=dict(scope='Readonly observation; zero loss is a measured outcome, not a repaired PASS',historical=history,caseCount=len(cases),accepted=sum(c['accepted'] for c in cases),withDamage=sum(c['hpLoss']>0 for c in cases),zeroDamage=sum(c['hpLoss']==0 for c in cases),remainingProjectiles=sum(c['remainingProjectiles'] for c in cases),cases=cases)
(a.output/'analysis.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
with (a.output/'matrix.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['id','camera','distance','skill','occlusion','accepted','spawns','hpLoss','damageEvents','flightEvents','reasons','remainingProjectiles']);w.writeheader();w.writerows({k:x[k] for k in w.fieldnames} for x in cases)
checks=[]
def check(n,v):checks.append(dict(name=n,status='PASS' if v else 'FAIL'))
check('38 controlled cases completed',len(cases)==38 and all(c['accepted'] and c['spawns']>0 and c['remainingProjectiles']==0 for c in cases))
check('two historical zero Damage retained',len(history)==2 and all(not c['actualDamage'] and c['reason']=='CAMERA_SURFACE_BEHIND_MUZZLE' and c['surfaceProjection']<0 and c['firstCollision'] is None for c in history))
paired=load(r/'paired-24.json');check('24 original spawns exact',paired['count']==24 and all(x['originEqual'] and x['directionEqual'] for x in paired['rows']))
for mode,name in [('Historical','CP03Editor.Run'),('Matrix','CP04Editor.Run')]:
 runner=load(r/mode/'results.json');runner=runner if isinstance(runner,list) else [runner];native=load(r/mode/(name+'.exit.json'));cmd=load(r/mode/(name+'.command.json'));desktop=load(r/mode/(name+'.desktop-process.json'));stage=next(x for x in runner if x['name']==name)
 check(mode+' actual exit and host association',stage['exitCode']==native['exitCode']==0 and stage['status']=='PASS' and stage['timedOut'] is False and native['forcedTermination'] is False and native['hostPid']==cmd['hostPid'] and Path(cmd['exe']).resolve()==Path(desktop['exe']).resolve()==Path(stage['command'][0]).resolve() and cmd['arguments']==stage['command'][1:])
check('real damage sums consistent',all(abs(c['hpLoss']-c['observedApplied'])<.001 for c in cases))
(a.output/'verification.json').write_text(json.dumps(dict(counts=dict(collections.Counter(c['status'] for c in checks)),rows=checks),indent=2),encoding='utf-8');print(json.dumps({k:result[k] for k in ['caseCount','accepted','withDamage','zeroDamage','remainingProjectiles']}));print(json.dumps(checks));raise SystemExit(1 if any(c['status']=='FAIL' for c in checks) else 0)
