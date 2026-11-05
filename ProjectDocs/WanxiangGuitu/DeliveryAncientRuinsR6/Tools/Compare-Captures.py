"""Compare independent Windows Player launches. Local masks are never applied to the full-frame result."""
from collections import Counter
from itertools import combinations, product
import hashlib
import json
import re
from pathlib import Path
import sys

import numpy as np
from PIL import Image

root = Path(sys.argv[1])
out = root / (sys.argv[2] if len(sys.argv)>2 else 'Comparison')
out.mkdir(exist_ok=True)
size = (1280, 720)
views = ('title','camp','entry','plaza','corridor','altar','guardian')

def folder(arm, view, sample):
    mode = 'camp' if view in ('title','camp') else 'ruins'
    return root / f'Frames-{arm}-{mode}-{sample}'

def read(path):
    with Image.open(path) as image:
        assert image.size == size, path
        array = np.asarray(image.convert('RGB'))
    assert np.ptp(array) > 10, path
    return array

def sample(arm, view, label):
    base = folder(arm, view, label)
    p = json.loads((base/'process.json').read_text('utf-8-sig'))
    assert p['exited'] and p['exitCode'] == 0 and not p['forcedTermination'] and not p['timedOut']
    assert (base/'render-complete.txt').is_file()
    return base

def masks(bases, view):
    areas = {k:np.zeros((size[1],size[0]),dtype=bool) for k in ('ui','dynamic')}
    names = {k:Counter() for k in areas}
    for base in bases:
        text = (base/f'{view}.regions.tsv').read_text('utf-8-sig')
        for kind,name,region in re.findall(r'^(ui|dynamic)\t(.*?)\t(-?\d+,-?\d+,-?\d+,-?\d+)$',text,re.M|re.S):
            x0,y0,x1,y1 = map(int,region.split(','))
            x0,x1 = [min(size[0],max(0,x)) for x in (x0,x1)]
            y0,y1 = [min(size[1],max(0,y)) for y in (y0,y1)]
            if x0 >= x1 or y0 >= y1:
                continue
            areas[kind][y0:y1,x0:x1] = True
            names[kind][name] += 1
    areas['dynamic'] &= ~areas['ui']
    areas['static'] = ~(areas['ui']|areas['dynamic'])
    return areas,names

def span(x):
    return {k:float(v) for k,v in zip(('min','median','p95','max'),np.quantile(x,[0,.5,.95,1]))}

def score(difference, mask=None):
    vals = difference if mask is None else difference[mask]
    if not vals.size:
        return None
    return dict(changed=int(np.any(vals!=0,axis=-1).sum()), overOne=int(np.any(vals>1,axis=-1).sum()),
                max=int(vals.max()), mae=float(vals.mean()))

result = []
for view in views:
    bases = {k:[sample(k,view,f'{i:02d}') for i in range(1,11)] for k in 'AB'}
    arrays = {k:np.stack([read(p/f'{view}.png') for p in v]) for k,v in bases.items()}
    clocks, state = {}, {}
    for arm, samples in bases.items():
        clocks[arm] = []
        state[arm] = []
        for base in samples:
            keys,vals = [r.split('\t') for r in (base/f'{view}.clock.tsv').read_text('utf-8-sig').splitlines()]
            row = dict(zip(keys, vals))
            assert int(row['frame'])>0 and row['phase']=='WaitForEndOfFrame'
            clocks[arm].append(row)
            meta = base/f'{view}.tsv'
            state[arm].append(hashlib.sha256(meta.read_bytes()).hexdigest())
    for values in ({c[k] for arm in clocks.values() for c in arm} for k in ('gameTime','timeScale','captureStep')):
        assert len(values)==1, (view,values)
    assert len(set(state['A']+state['B']))==1, (view,state)
    areas,names = masks(sum(bases.values(),[]),view)
    controls={}
    for effect in ('renderShadows','renderPostProcessing'):
        signals=[]
        for arm, number in product('AB',(1,2)):
            p=folder(arm,view,f'isolated-{number}')
            if not (p/'interventions.tsv').exists() or not (p/f'{view}-{effect}-off.png').exists():
                continue
            condition = [line.split('\t') for line in (p/'interventions.tsv').read_text('utf-8-sig').splitlines()]
            valid = [row for row in condition if row[:2] == [view,effect] and row[2] in ('1','2','3','4','True')
                     and row[3] in ('0','False')]
            if len(valid) != 1:
                continue
            sample(arm,view,f'isolated-{number}')
            baseline=read(p/f'{view}.png')
            changed=read(p/f'{view}-{effect}-off.png')
            signals.append(np.abs(baseline.astype(np.int16)-changed.astype(np.int16)).max(axis=2))
        if not signals:
            controls[effect] = dict(captures=0, status='NOT_RUN')
            continue
        # All four intervention pairs must independently shift a pixel by >2.
        regions=np.stack(signals)
        area=(regions>2).all(axis=0)
        controls[effect]=dict(captures=len(signals),individualPixels=[int((v>2).sum()) for v in signals],
                              commonPixels=int(area.sum()))
        areas[effect]=area
    pairs={}
    for key in ('AA','BB','AB'):
        sequence = combinations(range(10),2) if key[0]==key[1] else product(range(10),repeat=2)
        rows=[]
        for i,j in sequence:
            a,b=arrays[key[0]][i],arrays[key[1]][j]
            difference=np.abs(a.astype(np.int16)-b)
            rows.append(dict(left=i+1,right=j+1,full=score(difference),
                             **{k:score(difference,mask) for k,mask in areas.items()}))
        pairs[key]=rows
    metrics={}
    for key,rows in pairs.items():
        metrics[key]={k:{m:span([r[k][m] for r in rows]) for m in ('mae','changed','overOne')}
                      for k in ('full',*areas) if rows[0][k] is not None}
    lo_a,lo_b=(arrays[a].min(axis=0).astype(np.int16) for a in 'AB')
    hi_a,hi_b=(arrays[a].max(axis=0).astype(np.int16) for a in 'AB')
    channel_gap=np.maximum(lo_a-hi_b,lo_b-hi_a)
    robust=(channel_gap>2).any(axis=2)
    median_delta=np.abs(np.median(arrays['A'],axis=0)-np.median(arrays['B'],axis=0))
    Image.fromarray(np.clip(median_delta*8,0,255).astype(np.uint8)).save(out/f'{view}-median-delta-x8.png')
    Image.fromarray(np.uint8(robust)*255).save(out/f'{view}-consistent-gap.png')
    region_debug=np.zeros((size[1],size[0],3),dtype=np.uint8)
    region_debug[areas['static']]=(62,100,62)
    region_debug[areas['dynamic']]=(215,95,55)
    region_debug[areas['ui']]=(90,137,226)
    Image.fromarray(region_debug).save(out/f'{view}-regions.png')
    ys,xs=np.where(robust)
    row=dict(view=view, clocks=clocks, metadata=state, summary=metrics, allPairs=pairs,
             regionPixels={k:int(v.sum()) for k,v in areas.items()}, regionLabels=names,
             controlledEffects=controls,
             consistentGapPixels=int(robust.sum()),
             consistentGapBounds=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if len(xs) else None,
             consistentGapByRegion={k:int((robust&v).sum()) for k,v in areas.items()})
    result.append(row)
    print(view, {k:metrics[k]['full']['mae'] for k in pairs},row['consistentGapPixels'],controls,flush=True)

(out/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'summary.json').write_text(json.dumps([{k:v for k,v in row.items() if k not in ('allPairs','regionLabels')}
                                          for row in result],ensure_ascii=False,indent=2),encoding='utf-8')
