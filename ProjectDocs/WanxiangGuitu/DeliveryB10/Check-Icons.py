"""Inspect actual PNG alpha; does not edit images or infer human readability."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--icons',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-count',type=int,default=47);a=p.parse_args();rows=[]
limits={'portrait':.4,'hero':.3,'potion':.35,'sword':.15}
for f in sorted(a.icons.glob('*.png')):
 im=Image.open(f).convert('RGBA');alpha=im.getchannel('A');bbox=alpha.point(lambda x:255 if x>8 else 0).getbbox();total=sum(1 for x in alpha.get_flattened_data() if x>8);area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1]) if bbox else 0;coverage=total/area if area else 0
 rows.append(dict(key=f.stem,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),width=im.width,height=im.height,alphaBounds=bbox,opaquePixels=total,coverage=coverage,minimumCoverage=limits.get(f.stem),status='PASS' if im.size==(256,256) and area and coverage>=limits.get(f.stem,0) else 'FAIL'))
result=dict(status='PASS' if len(rows)==a.expected_count and all(r['status']=='PASS' for r in rows) else 'FAIL',scope='PNG format/nonempty/selected solid-shape alpha coverage only; not human recognition or native UI',icons=rows)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8');print(json.dumps(dict(status=result['status'],count=len(rows),failed=[r['key'] for r in rows if r['status']=='FAIL'])));raise SystemExit(0 if result['status']=='PASS' else 1)
