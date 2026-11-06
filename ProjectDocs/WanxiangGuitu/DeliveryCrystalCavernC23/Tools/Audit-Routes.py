import json,re,math
from pathlib import Path
root=Path('I:/WGCombat/C23-1106-A')
out=Path(__file__).resolve().parents[1]/'Evidence/route-measurements.json'
assert not out.exists()
result={}
for name in ['EditorRoutesVerified','PlayerRoutesAudited','EditorInnerVerified','PlayerInnerVerified']:
    folder=root/name
    actors={}
    for line in (folder/'ai.tsv').read_text().splitlines():
        cols=line.split('\t')
        position=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',cols[5])]
        assert len(position)==3
        actors.setdefault(cols[2],[]).append(position)
    data={}
    for key,points in actors.items():
        # Deep-water rectangle excludes the bridge and northern/southern shores.
        invalid=[p for p in points if 48.5<p[0]<69.5 and ((399.5<p[2]<407) or (413<p[2]<426.5))]
        assert not invalid,(name,key,invalid)
        data[key]={'samples':len(points),'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)],'deepWaterSamples':len(invalid)}
    paths={}
    if (folder/'paths.tsv').exists():
        for line in (folder/'paths.tsv').read_text().splitlines():
            cols=line.split('\t');assert cols[3]=='PathComplete'
            corners=[[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',s)] for s in cols[4].split(';')]
            length=sum(math.dist(a,b) for a,b in zip(corners,corners[1:]))
            paths[cols[0]]=paths.get(cols[0],0)+length
    result[name]={'actorSamples':data,'navPathLengthByRecordedLegMeters':paths,'limitation':'Sampled actual AI positions, not proof for every possible agent route. Path length is NavMesh corners, not straight graph distance.'}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v['navPathLengthByRecordedLegMeters'] for k,v in result.items()}))
