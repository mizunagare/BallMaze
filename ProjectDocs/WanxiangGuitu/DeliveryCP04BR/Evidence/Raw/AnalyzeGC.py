import json,statistics,hashlib
from pathlib import Path
r=Path('I:/WGCombat/CP04BR-1102-A');out={}
for v in ['Baseline','Fixed']:
 p=r/(v+'Scoped')/'scoped-events.json';j=json.loads(p.read_text(encoding='utf8'));raw={x['marker']:x for x in j['raw']};rows=[]
 for s in j['scopes']:
  a=raw.get(s['marker']);rows.append(dict(**s,bytes=sum(x['bytes'] for x in a['allocations']) if a else None,rawFrame=a['frame'] if a else None,rawCpuMs=a['cpuMs'] if a else None))
 cal={k:[x['bytes'] for x in rows if x['kind']==k] for k in ['zero','positive-65536','release-reference']}
 valid=len(raw)==len(j['raw'])==len(rows)==152 and not j['errors'] and cal['zero']==[0]*8 and cal['release-reference']==[0]*8 and all(x>=65536 for x in cal['positive-65536'])
 groups=[]
 for d in [.35,1.5,6,20]:
  z=[x for x in rows if x['kind']=='solve' and abs(x['distance']-d)<.001];b=[x['bytes'] for x in z];c=sorted(x['cpuNs'] for x in z)
  groups.append(dict(distance=d,n=len(z),bytesMin=min(b),bytesMedian=statistics.median(b),bytesMax=max(b),cpuNsMedian=statistics.median(c),cpuNsP95=c[int((len(c)-1)*.95)],reasons=sorted(set(x['reason'] for x in z))))
 out[v]={'sourceSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'calibrationValid':valid,'calibration':cal,'groups':groups,'aimILSHA':j['aimILSHA'],'assemblySHA':j['assemblySHA'],'scope':j['scope']}
 (r/(v+'-solve-allocations.json')).write_text(json.dumps(rows,indent=2))
(r/'editor-allocation-analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
