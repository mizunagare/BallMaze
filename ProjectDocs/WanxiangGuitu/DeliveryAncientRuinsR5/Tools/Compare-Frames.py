import hashlib
import json
from pathlib import Path
import sys
from PIL import Image, ImageChops, ImageDraw

root = Path(sys.argv[1])
attempt = sys.argv[2] if len(sys.argv) > 2 else "1"
out = root / ("RenderComparison" + attempt)
out.mkdir(exist_ok=True)
views = ("title","camp","entry","plaza","corridor","altar","guardian")
overview = Image.new("RGB", (960, 210 * len(views)), "#222222")
draw = ImageDraw.Draw(overview)
rows = []
for i, view in enumerate(views):
    mode = "camp" if view in ("title","camp") else "ruins"
    folders = [root / f"Frames-{label}-{mode}-{attempt}" for label in "AB"]
    paths = [folder / (view+".png") for folder in folders]
    a,b = [Image.open(path).convert("RGB") for path in paths]
    assert a.size == b.size == (1280,720)
    delta = ImageChops.difference(a,b)
    red,green,blue=delta.split()
    max_channel=ImageChops.lighter(ImageChops.lighter(red,green),blue)
    hist=max_channel.histogram()
    pixels=a.width*a.height
    avg=sum(j*count for band in delta.split() for j,count in enumerate(band.histogram()))/(pixels*3)
    if hist[0]!=pixels:
        delta.point(lambda v: min(v*8,255)).save(out/(view+"-diff-x8.png"))
    metas=[(folder/(view+".tsv")).read_text(encoding="utf-8-sig").splitlines() for folder in folders]
    meta_equal=metas[0]==metas[1]
    rows.append(dict(view=view,resolution=a.size, imageSHA256=[hashlib.sha256(path.read_bytes()).hexdigest() for path in paths],
                     imagesNonUniform=[any(lo!=hi for lo,hi in im.getextrema()) for im in (a,b)],
                     changedPixels=pixels-hist[0], pixelsAboveOne=sum(hist[2:]), maxChannelError=max(k for k,v in enumerate(hist) if v),
                     channelMeanAbsoluteError=avg, deltaBounds=max_channel.getbbox(),metadataOrderedEqual=meta_equal,
                     onlyA=sorted(set(metas[0])-set(metas[1]))[:16],onlyB=sorted(set(metas[1])-set(metas[0]))[:16]))
    for j, im in enumerate((a,b)):
        overview.paste(im.resize((320,180)), (320*j, i*210+24))
    overview.paste(delta.point(lambda v:min(v*8,255)).resize((320,180)),(640,i*210+24))
    draw.text((8,i*210+5),f"{view} | A, B, diff x8 | {pixels-hist[0]} pixels",fill="white")
overview.save(out/"montage.png")
(out/"pixel-metrics.json").write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding="utf-8")
for row in rows:
    print(row["view"], row["changedPixels"], row["pixelsAboveOne"], row["maxChannelError"], row["metadataOrderedEqual"],row["imagesNonUniform"])
