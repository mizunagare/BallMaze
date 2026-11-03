"""Read-only evidence validation; measured costs do not imply a performance budget PASS."""
from pathlib import Path
import json,statistics,math,sys,collections
from PIL import Image
def analyse(folder,stress=False):
 p=Path(folder);r=json.loads((p/'br-probe.json').read_text(encoding='utf-8-sig'));errors=[];rows=r['samples'];phases=r['phases'];cal=[s for s in rows if s['phase']=='calibration']
 if r['nativeInit']!=1 or not r['calibrationValid'] or r.get('error'):errors.append('Invalid calibration/init/runtime')
 for kind in ('zero','positive-65536','release-reference'):
  selected=[s for s in cal if s['kind']==kind]
  if len(selected)!=8 or any(s['invalid'] or (s['bytes']<65536 or not s['events'] if kind=='positive-65536' else s['bytes']!=0) for s in selected):errors.append('Invalid '+kind)
 if len({s['marker'] for s in rows})!=len(rows) or any(s['invalid'] for s in rows):errors.append('Duplicate markers or invalid allocation events')
 names=['free','shoulder-only','shoulder-ranged','all-assists','two-moving','ten-moving-projectiles']
 if [s['name'] for s in phases]!=names:errors.append('Missing/reordered phases')
 for phase in phases:
  dense=phase['name']==names[-1]
  if (dense and stress and (phase['windowFrames']<240 or phase['duration']<4)) or (not(dense and stress) and phase['windowFrames']!=(240 if dense else 60)):errors.append('Incomplete interval count/duration '+phase['name'])
 for index,name in enumerate(names):
  expected={'camera-reflection-inclusive':16,'fade-refresh':16,'raw-raycastall-control':16,'raw-spherecastall-control':16,'update-to-endframe-main-thread-interval':phases[index]['windowFrames'] if index==5 and stress and len(phases)>index else 240 if index==5 else 60}
  if index>=2:expected['target-choose']=16
  actual=dict(collections.Counter(x['kind'] for x in rows if x['phase']==name))
  if actual!=expected:errors.append('Missing/extra method samples '+name)
 if any(s['bytes']<0 or not math.isfinite(s['cpuNs']) or s['cpuNs']<0 for s in rows):errors.append('Invalid numeric sample')
 groups=collections.defaultdict(list)
 for s in rows:groups[s['phase']+'/'+s['kind']].append(s)
 result=[]
 def desc(v):
  q=sorted(v);return {'n':len(v),'mean':statistics.mean(v),'median':statistics.median(v),'min':min(v),'max':max(v),'p95':q[max(0,math.ceil(len(q)*.95)-1)]}
 for k,v in groups.items():result.append({'key':k,'bytes':desc([x['bytes'] for x in v]),'cpuNs':desc([x['cpuNs'] for x in v])})
 images=[]
 for f in sorted(p.glob('*.png')):
  with Image.open(f) as im:images.append({'path':f.name,'size':list(im.size),'allBlack':all(x[1]==0 for x in im.convert('RGB').getextrema())})
 raw=p/'unity-profiler.json';prof=None
 if raw.exists():
  u=json.loads(raw.read_text(encoding='utf-8-sig'));maprows={x['marker']:x for x in rows};unknown=[x['marker'] for x in u['rows'] if x['marker'] not in maprows];duplicates=len({x['marker'] for x in u['rows']})!=len(u['rows']);expected=[x for x in rows if x['kind']!='update-to-endframe-main-thread-interval'];missing=sorted(set(x['marker'] for x in expected)-set(x['marker'] for x in u['rows']));different=[x['marker'] for x in u['rows'] if x['marker'] in maprows and sum(x['allocations'])!=maprows[x['marker']]['bytes']]
  prof={'scope':'Independent Unity native CPU/GC metadata; no frame interval equivalence claim','samples':len(u['rows']),'expectedQueryScopes':len(expected),'missing':missing,'unknown':unknown,'duplicates':duplicates,'allocationMismatch':different,'errors':u['errors'],'status':'PASS' if not(missing or unknown or duplicates or different or u['errors']) else 'UNRESOLVED'}
 motion=[]
 for phase in phases:
  distances=[math.sqrt((a['x']-b['x'])**2+(a['z']-b['z'])**2) for a,b in zip(phase['enemyBefore'],phase['enemyAfter'])]
  motion.append({'phase':phase['name'],'horizontalDisplacements':distances,'movedCount':sum(d>.05 for d in distances)})
 moving=next((m for m in motion if m['phase']=='two-moving'),None);dense=next((p for p in phases if p['name']=='ten-moving-projectiles'),None)
 coverage=[]
 if moving is None or moving['movedCount']!=2:coverage.append('Two actors did not both move horizontally >0.05m')
 if stress and (dense is None or dense['enemies']!=10 or dense['spawns']<4 or dense['collisions']<1 or not dense['completedAlive']):coverage.append('Dense/live/continuous real-projectile workload incomplete')
 report={'measurementValidity':'FAIL' if errors else 'PASS','workloadCoverage':'FAIL' if coverage else 'PASS','workloadErrors':coverage,'motion':motion,'errors':errors,'sampleCount':len(rows),'calibrationSamples':len(cal),'phases':phases,'statistics':result,'images':images,'unityProfilerCrossCheck':prof,'performanceBudget':'NOT_RUN','nativeInput':'NOT_RUN','humanExperience':'NOT_RUN','incompleteLiveWorkloads':[x['name'] for x in phases if not x['completedAlive']]}
 return report
if __name__=='__main__':
 result=analyse(sys.argv[1],stress='--stress' in sys.argv);Path(sys.argv[2]).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:result[k] for k in ['measurementValidity','sampleCount','errors','incompleteLiveWorkloads','unityProfilerCrossCheck']},indent=2));sys.exit(result['measurementValidity']!='PASS')
