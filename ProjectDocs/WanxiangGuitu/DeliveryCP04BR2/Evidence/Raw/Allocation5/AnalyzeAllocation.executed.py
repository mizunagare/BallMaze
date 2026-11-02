import json,collections,statistics
from pathlib import Path
r=Path('I:/WGCombat/CP04BR2-1102-A');j=json.loads((r/'Allocation5/scoped-events.json').read_text());raw={x['marker']:x for x in j['raw']};byKind=collections.defaultdict(list);stacks=collections.Counter();owners=collections.Counter();nativeArrays=0
for s in j['scopes']:
 a=raw[s['marker']]['allocations'];byKind[s['kind']].append(sum(x['bytes'] for x in a))
 if s['kind']=='solve' and abs(s['distance']-1.5)<.001:
  for x in a:
   frames=[y.split(' | ')[0] for y in x['stack'] if y.split(' | ')[0]];top=frames[0] if frames else 'UNRESOLVED';stacks[top]+=x['bytes'];owner=next((y for y in frames if '::CombatAim.' in y),'UNRESOLVED');owners[owner]+=x['bytes'];nativeArrays+=x['bytes'] if top.startswith('UnityEngine.PhysicsModule.dll!') else 0
out={'sourceRun':'Allocation5','scopes':len(j['scopes']),'raw':len(raw),'calibrationValid':len(raw)==len(j['scopes'])==224 and byKind['zero']==[0]*8 and byKind['positive-65536']==[65568]*8 and byKind['release-reference']==[0]*8 and not j['errors'],'groups':{k:{'n':len(v),'min':min(v),'median':statistics.median(v),'max':max(v)} for k,v in byKind.items()},'nearAllocationTopFrameBPerSolve':{k:v/32 for k,v in stacks.items()},'nearAllocationOwnerBPerSolve':{k:v/32 for k,v in owners.items()},'nearPhysicsReturnedArraysBPerSolve':nativeArrays/32,'nearOtherManagedBPerSolve':4460-nativeArrays/32}
m=json.loads((r/'MonoPlayer/mono-probe.json').read_text());out['player']={'calibrationValid':m['calibrationValid'],'nativeInit':m['nativeInit'],'status':m['status'],'groups':{}}
for d in [.35,1.5,6,20]:
 z=[x for x in m['rows'] if x['kind']=='solve' and abs(x['distance']-d)<.001];out['player']['groups'][str(d)]={'n':len(z),'bytesMedian':statistics.median(x['rawBytes'] for x in z),'cpuNsMedian':statistics.median(x['cpuNs'] for x in z)}
(r/'allocation-analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='nearAllocationTopFrameBPerSolve'},indent=2))
