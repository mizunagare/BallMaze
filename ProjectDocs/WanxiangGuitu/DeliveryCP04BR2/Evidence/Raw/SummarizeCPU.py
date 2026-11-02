import json,statistics,hashlib
from pathlib import Path
r=Path('I:/WGCombat/CP04BR2-1102-A');out=[]
for run,key in [('Allocation6','scopes'),('MonoPlayer','rows'),('MonoPlayerRepeat','rows')]:
 name='scoped-events.json' if key=='scopes' else 'mono-probe.json';j=json.loads((r/run/name).read_text(encoding='utf8'));groups=[]
 for d in [.35,1.5,6,20]:
  z=[x for x in j[key] if x['kind']=='solve' and abs(x['distance']-d)<.001];t=sorted(x['cpuNs'] for x in z);groups.append({'distance':d,'n':len(t),'medianNs':statistics.median(t),'p95Ns':t[int((len(t)-1)*.95)],'minNs':min(t),'maxNs':max(t)})
 out.append({'run':run,'sourceSHA256':hashlib.sha256((r/run/name).read_bytes()).hexdigest(),'groups':groups,'note':'Instrumented measurement; sampling modes differ; no same-condition speedup claim'})
(r/'cpu-current.json').write_text(json.dumps(out,indent=2));print([(x['run'],[(g['distance'],g['medianNs']/1000) for g in x['groups']]) for x in out])
# Preserve read-only reference measurements with original source identities, not new PASS.
old=Path('I:/WGCombat/CP04BR-1102-A');refs=[]
for name in ['editor-allocation-analysis.json','player-performance-analysis.json','hardware.json']:
 p=old/name;refs.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'data':json.loads(p.read_text(encoding='utf-8-sig'))})
(r/'br-reference-measurements.json').write_text(json.dumps({'scope':'Historical BR measurements for comparison, not rerun results','references':refs},indent=2))
