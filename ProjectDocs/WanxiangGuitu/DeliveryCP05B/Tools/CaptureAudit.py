"""Independent pixel inspection; valid API assertions do not certify visible rendering."""
from pathlib import Path
from PIL import Image,ImageStat
import json,sys
root=Path('I:/WGCombat/CP05B-1103-A');rows=[]
for stage,run in [('B1','Editor2'),('B2','Editor1'),('B2','Player2'),('B3','EditorFinal'),('B3','PlayerFinal')]:
 p=root/stage/run
 for f in p.rglob('*.png'):
  with Image.open(f) as im:
   rgb=im.convert('RGB');ext=rgb.getextrema();black=all(high==0 for low,high in ext)
   rows.append({'stage':stage,'run':run,'file':f.relative_to(p).as_posix(),'allBlack':black,'size':list(im.size),'extrema':ext})
report={'scope':'Pixel audit only; does not diagnose rendering root cause','rows':rows,'summary':{run:{'images':len([r for r in rows if r['stage']+'/'+r['run']==run]),'allBlack':sum(r['allBlack'] for r in rows if r['stage']+'/'+r['run']==run)} for run in sorted(set(r['stage']+'/'+r['run'] for r in rows))},'playerVisibleRendering':'UNRESOLVED','nativeInput':'NOT_RUN','humanExperience':'NOT_RUN'}
Path(sys.argv[1]).write_text(json.dumps(report,indent=2),encoding='utf8');print(json.dumps(report['summary'],indent=2))
