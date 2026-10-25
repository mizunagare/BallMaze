"""Narrow regression for the observed solid-cyan frame; not a general visual-quality oracle."""
import argparse,json
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--image',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise ValueError('Keep previous checks; fresh output required')
im=Image.open(a.image).convert('RGB');pixels=getattr(im,'get_flattened_data',im.getdata)();fraction=sum(r<15 and g>245 and b>245 for r,g,b in pixels)/(im.width*im.height)
result=dict(status='FAIL' if fraction>.4 else 'PASS',image=str(a.image),solidCyanFraction=fraction,threshold=.4,scope='Observed cyan occlusion regression only; not native UI or human understanding')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(result))
raise SystemExit(1 if result['status']=='FAIL' else 0)
