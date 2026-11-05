from collections import Counter
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
from PIL import Image, ImageDraw

root=Path(sys.argv[1])
out=root/'Audit'
out.mkdir(exist_ok=True)
views=('title','camp','entry','plaza','corridor','altar','guardian')
states=('native','off','on','off-repeat')
expected_psos=dict(graphicsStateCollectionInstanceId=0,collectionStartupAction=0,traceSavePath='TracedCollection',
                   traceSendToEditor=1,additionalWarmupCollectionCount=0,warmupAsync=1,enableCacheMissTracing=0,
                   warmupProgressivelyLimit=-1,cacheMissCollectionPath='CacheMissCollection')

def folder(arm, view, run):
    return root/f'Frames-{arm}-{"camp" if view in ("title","camp") else "ruins"}-gpu-{run}'
def load(path):
    return json.loads(path.read_text('utf-8-sig'))
def image(path):
    with Image.open(path) as frame:
        assert frame.size==(1280,720)
        return np.asarray(frame.convert('RGB'))
def delta(a,b):
    x=np.abs(a.astype(np.int16)-b)
    return dict(mae=float(x.mean()),changed=int(np.any(x!=0,axis=-1).sum()),
                over2=int(np.any(x>2,axis=-1).sum()),max=int(x.max()))
def normalized_stages(value):
    return '|'.join(f'{stage}:{data["sha256"]}' for stage,data in sorted(value.items()))

compiled=root/'packaged-shaders.json'
packaged=load(compiled)['A'] if compiled.exists() else []
packages={}
for obj in packaged:
    for segment in obj['segments']:
        for value in segment['bytecodes']:
            packages.setdefault(value['sha256'],set()).add(
                (obj['file'],obj['pathID'],obj['name'] or '',segment['platform']))
pairs={}
all_used=set()
for index,view in enumerate(views):
    captures={}
    for arm in 'AB':
        for run in (1,2):
            key=f'{arm}{run}'
            folder_path=folder(arm,view,run)
            receipt=load(folder_path/'player-process.json')
            assert receipt['exited'] and receipt['exitCode']==0 and receipt['gpuCatalog'] and not receipt['forcedTermination']
            events=[json.loads(line) for line in (folder_path/'gpu.jsonl').read_text('utf-8').splitlines()]
            errors=[e for e in events if e.get('type')=='error' or e.get('kind')=='read-error']
            graphics,=[e for e in events if e.get('kind')=='graphics-register-startup']
            assert graphics['pid']==receipt['pid'] and graphics['values']==expected_psos
            assert not any(e.get('kind','').startswith('graphics-startup-') for e in events)
            gpu={e['label']:e for e in events if e.get('kind')=='gpu-window'}
            cat,=[e for e in events if e.get('kind')=='catalog']
            variants={x['id']:x for x in cat['entries']}
            rows={}
            renderer={}
            for line in (folder_path/'camera-path.tsv').read_text('utf-8-sig').splitlines():
                label,frame,post,kind,mode,asset,main,additional=line.split('\t')
                renderer[label]=dict(frame=int(frame),post=post,renderer=kind,mode=mode,asset=asset,shadows=[main,additional])
            frames={}
            for state in states:
                label=f'{view}-{state}'
                row=gpu[label]
                assert row['submissions']>0 and row['calls']
                drawn={}
                missing={}
                for call,count in row['calls'].items():
                    typ,n=call.split(':')
                    n=int(n)
                    if not n:
                        missing[typ]=count
                        continue
                    stages=variants[n]['stages']
                    all_used.update(x['sha256'] for x in stages.values())
                    stage_key=normalized_stages(stages)
                    drawn.setdefault(stage_key,{})[typ]=count
                rows[state]=dict(submissions=row['submissions'],drawn=drawn,unknown=missing,camera=renderer[label])
                frames[state]=image(folder_path/f'{label}.png')
            captures[key]=dict(errors=errors, unresolvedCatalog=cat['unresolved'],
                               rows=rows,hashes={s:hashlib.sha256((folder_path/f'{view}-{s}.png').read_bytes()).hexdigest()
                                               for s in states},
                               effect={s:delta(frames['on'],frames[s]) for s in ('off','off-repeat')},
                               repeat=delta(frames['off'],frames['off-repeat']))
    comparisons={}
    for state in states:
        first=captures['A1']['rows'][state]
        comparisons[state]=dict(allDrawnSetsEqual=all(set(c['rows'][state]['drawn'])==set(first['drawn'])
                                                      for c in captures.values()),stageTuples=len(first['drawn']),
                                allCamerasEqual=len({tuple(v for k,v in c['rows'][state]['camera'].items()
                                                           if k not in ('frame','shadows')) for c in captures.values()})==1,
                                unknown=sum(sum(c['rows'][state]['unknown'].values()) for c in captures.values()))
    first=captures['A1']['rows']
    added=sorted(set(first['on']['drawn'])-set(first['off']['drawn']))
    pairs[view]=dict(captures=captures,comparisons=comparisons,onOnlyStageTuples=added)
    print(view,comparisons,{k:(round(v['effect']['off']['mae'],3),round(v['repeat']['mae'],3))
                              for k,v in captures.items()},flush=True)
result=dict(views=pairs, usedUniqueStageBytecodes=len(all_used),
            packagedIntersection={h:sorted(packages[h]) for h in sorted(all_used & set(packages))},
            observedWithoutExactPackagedMap=sorted(all_used-set(packages)),
            packagedUnobserved=sorted(set(packages)-all_used))
(out/'gpu-and-post.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
montage=Image.new('RGB',(1200,216*len(views)),'#162023')
pen=ImageDraw.Draw(montage)
for i,view in enumerate(views):
    for col,(arm,state) in enumerate((('A','off'),('A','on'),('B','off'),('B','on'))):
        path=folder(arm,view,1)/f'{view}-{state}.png'
        with Image.open(path) as shot:
            montage.paste(shot.resize((294,165),Image.Resampling.LANCZOS),(col*300+3,i*216+22))
        pen.text((col*300+4,i*216+3),f'{view} | {arm} {state}',fill='#eeeeee')
montage.save(out/'post-contact-sheet.png')
