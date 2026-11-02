import json,hashlib,statistics,collections
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A');out={}
for v in ['Fixed','Baseline']:
 p=r/(v+'Players')/'PlayerProbe/probe.json'
 if not p.exists():out[v]={'status':'NOT_RUN','reason':'No completed probe receipt; missing-script warnings; normal-close interruption retained, not a PASS'};continue
 j=json.loads(p.read_text());rows=j['scopes'];cal={k:[(x['threadDelta'],x['samples'],x['gcUnit']) for x in rows if x['kind']==k] for k in ['zero','positive-65536','release-reference']};groups=[]
 for d in [.35,1.5,6,20]:
  z=[x['cpuNs'] for x in rows if x['kind']=='solve' and abs(x['distance']-d)<.001];groups.append({'distance':d,'n':len(z),'cpuNsMedian':statistics.median(z),'cpuNsMin':min(z),'cpuNsMax':max(z)})
 frames=[x['mainThreadNs'] for x in j['concurrent'] if x['mainThreadNs']>0]
 out[v]={'cpuStatus':'PASS','gcBytesStatus':'NOT_RUN','queryCountStatus':'NOT_RUN','reason':'Thread byte API fails positive calibration; GC.Alloc values have time units, no per-scope byte metadata in nondevelopment Player. Physics Queries fails known query calibration.','calibration':cal,'groups':groups,'peakActiveProjectiles':j['peak'],'spawnCount':j['spawnCount'],'concurrentFrames':len(j['concurrent']),'mainThreadMedianNs':statistics.median(frames) if frames else None,'damage':j['damage'],'eventCounts':dict(collections.Counter(x['stage'] for x in j['events']))}
(r/'player-performance-analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
for layer,p in [('Player',r/'FixedPlayers/PlayerCore/presentation.json'),('Editor',r/'FixedEditorCore/presentation.json')]:
 if p.exists():
  j=json.loads(p.read_text());print(layer,dict(collections.Counter(x['status'] for x in j['rows'])))
