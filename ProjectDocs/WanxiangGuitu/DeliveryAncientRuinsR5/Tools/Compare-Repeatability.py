import itertools
import json
from pathlib import Path
import sys
from PIL import Image, ImageChops

root=Path(sys.argv[1])
cases=("A2","A3","B2","B3")
views=("title","camp","entry","plaza","corridor","altar","guardian")
out=root/"Audit"
out.mkdir(exist_ok=True)

def stats(a,b):
    diff=ImageChops.difference(a,b)
    r,g,bl=diff.split()
    hist=ImageChops.lighter(ImageChops.lighter(r,g),bl).histogram()
    return dict(changedPixels=sum(hist[1:]), pixelsAboveOne=sum(hist[2:]),
                maxChannel=max(i for i,c in enumerate(hist) if c),
                mae=sum(i*c for band in diff.split() for i,c in enumerate(band.histogram()))/(a.width*a.height*3))

rows=[]
for view in views:
    mode="camp" if view in ("title","camp") else "ruins"
    paths={case:root/f"Frames-{case[0]}-{mode}-{case[1]}" for case in cases}
    frames={case:Image.open(folder/(view+".png")).convert("RGB") for case,folder in paths.items()}
    metadata={case:(folder/(view+".tsv")).read_text(encoding="utf-8-sig").splitlines() for case,folder in paths.items()}
    assert all(im.size==(1280,720) and any(x!=y for x,y in im.getextrema()) for im in frames.values())
    pairs={a+"/"+b:stats(frames[a],frames[b]) for a,b in itertools.combinations(cases,2)}
    control=[m["mae"] for pair,m in pairs.items() if pair[0]==pair[3]]
    cross=[m["mae"] for pair,m in pairs.items() if pair[0]!=pair[3]]
    row=dict(view=view,pairs=pairs,allMetadataEqual=all(m==metadata["A2"] for m in metadata.values()),
             withinBuildMAE=control,crossBuildMAE=cross,crossEntirelyAboveControls=min(cross)>max(control),
             strictPixelsEqualAcrossAll=all(p["changedPixels"]==0 for p in pairs.values()))
    rows.append(row)
    print(view,"control",*[round(v,7) for v in control],"cross",*[round(v,7) for v in cross],row["allMetadataEqual"])
(out/"repeatability.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
