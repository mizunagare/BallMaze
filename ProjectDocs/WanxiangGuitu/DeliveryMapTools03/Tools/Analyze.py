"""Read-only analysis of explicitly named independent Unity runs. No product imports."""
from pathlib import Path
import collections, csv, hashlib, json, re, statistics

ROOT = Path('I:/WGCombat/MAPTOOLS03-A')
DOC = Path(__file__).resolve().parents[1]
RUNS = ['Audit2', 'Memory1', 'Memory2', 'Audit3', 'EditorPlay1']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

summary = {}
for name in RUNS:
    root = ROOT / name
    result, process = load(root/'results.json'), load(root/'process.json')
    rows = result['rows']
    names = [r['name'] for r in rows]
    assert names and len(names) == len(set(names)), name
    assert all(r['status'] in ['PASS','FAIL','NOT_RUN','UNRESOLVED'] for r in rows)
    assert process['exited'] and not process['timedOut'] and process['exitCode'] == 0
    assert not any(r['status'] == 'FAIL' for r in rows)
    data = [json.loads(s) for s in (root/'memory.jsonl').read_text().splitlines()]
    warm = [s for s in data if s['phase']=='warm-unloaded']
    measured = [s for s in data if s['phase']=='measured-unloaded']
    assert len(warm)==2 and [s['cycle'] for s in measured]==list(range(6))
    def counts(s):
        return {t['type']:t['count'] for t in s['types']}
    # Editor resource inventory includes persistent assets/open editor objects, not just live scene objects.
    # Runtime's independently recorded cycle-unload checks remain mandatory in both layers.
    assert all(next(r for r in rows if r['name']==f'cycle-unload-{i}')['status']=='PASS' for i in range(6))
    if not name.startswith('Editor'):
        assert all(counts(s)['TerrainData']==counts(s)['Collider']==counts(s)['NavMeshData']==0 for s in measured)
    fields = ['engineAllocated','reserved','monoUsed','monoHeap','workingSet','privateBytes']
    mem = {k:dict(first=measured[0][k],last=measured[-1][k],min=min(s[k] for s in measured),max=max(s[k] for s in measured)) for k in fields}
    kinds = {}
    for kind in measured[0]['types']:
        group=[next(x for x in s['types'] if x['type']==kind['type']) for s in measured]
        kinds[kind['type']] = dict(counts=[x['count'] for x in group],nativeBytes=[x['nativeBytes'] for x in group],identitiesStable=all(x['objects']==group[0]['objects'] for x in group))
    times = [float(s.split(',')[1]) for s in (root/'cycle-times.csv').read_text().splitlines() if int(s.split(',')[0])>=0]
    gpu = (root/'gpu-status.txt').read_text() if result['mode']=='audit' else 'NOT_RUN: intentionally separate memory-only protocol'
    summary[name] = dict(layer='Editor controlled Play Mode' if name.startswith('Editor') else 'nondevelopment independent Player',counts=dict(collections.Counter(r['status'] for r in rows)),process=process,development=result['development'],gpu=result['gpu'],memory=mem,objects=kinds,cycleSeconds=dict(n=len(times),mean=statistics.mean(times),min=min(times),max=max(times)),gc=load(root/'gc-calibration.json'),gpuCalibration=gpu)
    assert result['development'] is False or name.startswith('Editor')
    with (root/'unloaded-summary.csv').open('w', newline='') as f:
        w=csv.writer(f);w.writerow(['cycle']+fields+[x['type'] for x in measured[0]['types']])
        for s in measured:w.writerow([s['cycle']]+[s[k] for k in fields]+list(counts(s).values()))
(ROOT/'runtime-summary.json').write_text(json.dumps(summary,indent=2))

# Preserve all source logs locally. Publish stack facts separately from native hex payloads.
jobs={}
for name in ['BuildEmpty1','BuildTerrain1','BuildAudit1','BuildEmpty2','BuildTerrain2','BuildAudit2','BuildAudit3','EditorPlay1']:
    p=ROOT/name/'Unity.log';lines=p.read_text(errors='replace').splitlines()
    allocations=[]
    for i,s in enumerate(lines):
        if s.startswith('Allocation of '):
            stack=[]
            for t in lines[i+1:]:
                if not t.startswith('0x'):break
                stack.append(t)
            allocations.append(dict(line=i+1,allocation=s,stack=stack))
    jobs[name]=dict(sourceSHA256=sha(p),warningLines=[i+1 for i,s in enumerate(lines) if 'remaining Allocations on the JobTempAlloc' in s],allocations=allocations,compileVariantAllocations=sum(any('ShaderCompilation::CompileVariantJob' in t for t in a['stack']) for a in allocations),preBuild=load(ROOT/name/'pre-build.json') if (ROOT/name/'pre-build.json').exists() else None)
(ROOT/'job-stacks.json').write_text(json.dumps(jobs,indent=2))

from PIL import Image, ImageChops, ImageStat
seams=[]
for stage in ['baseline','rebind-sync','lod-control','pixel-normal-control','no-shadow-control','matte-source-control']:
    for v in range(3):
        p=ROOT/'Audit3'/f'{stage}-v{v}.png';a=Image.open(p).convert('RGB');b=Image.open(ROOT/'Audit3'/f'baseline-v{v}.png').convert('RGB')
        assert a.size==b.size==(1280,720)
        difference=ImageChops.difference(a,b);h=difference.histogram()
        seams.append(dict(stage=stage,view=v,sha256=sha(p),identicalToBaseline=a.tobytes()==b.tobytes(),meanAbsoluteRGBDifference=statistics.mean(ImageStat.Stat(difference).mean)))
(ROOT/'image-comparison.json').write_text(json.dumps(seams,indent=2))

builds={}
for name in ['BuildEmpty1','BuildTerrain1','BuildAudit1','BuildEmpty2','BuildTerrain2','BuildAudit2','BuildAudit3']:
    p=ROOT/name/'Player';files=[]
    for rel in ['MT03.exe','UnityPlayer.dll','MT03_Data/Managed/Assembly-CSharp.dll']:
        f=p/rel;files.append(dict(path=str(f),bytes=f.stat().st_size,sha256=sha(f)))
    builds[name]=dict(build=load(ROOT/name/'build.json'),process=load(ROOT/name/'process.json'),validSceneProfile=name.endswith('2') or name=='BuildAudit3',files=files)
(ROOT/'build-summary.json').write_text(json.dumps(builds,indent=2))
print(json.dumps({n:s['counts'] for n,s in summary.items()},indent=2))
print('JobTempAlloc detailed allocations:',{n:len(s['allocations']) for n,s in jobs.items()})
