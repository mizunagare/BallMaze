"""Derived GIF recordings from full raw API Player frames, never native/human evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False)
pairs=[('camera','CameraOriginal','CameraShoulder'),('staff','Staff-basic-d6-free','Staff-basic-d6-assist'),('bow','Bow-basic-d6-free','Bow-basic-d6-assist'),('sword','Sword-basic-free-facing','Sword-basic-assisted-facing'),('spear','Spear-basic-free-facing','Spear-basic-assisted-facing')]
manifest=[]
for name,left,right in pairs:
 def load(label):
  p=root/('clip-'+label);files=sorted(p.glob('*.png'));times=[json.loads(s)['realtime'] for s in (p/'frames.jsonl').read_text().splitlines()];assert len(files)==len(times)>1
  return files,[t-times[0] for t in times]
 lf,lt=load(left);rf,rt=load(right);duration=max(lt[-1],rt[-1]);frames=[]
 for i in range(max(2,int(duration*8)+1)):
  t=i/8;canvas=Image.new('RGB',(960,298),(20,25,28));draw=ImageDraw.Draw(canvas);draw.text((8,5),'CONTROLLED EDITOR API | '+left+' / '+right,fill='white')
  for x,fs,ts in ((0,lf,lt),(480,rf,rt)):
   k=min(range(len(ts)),key=lambda j:abs(ts[j]-t));im=Image.open(fs[k]);im.thumbnail((480,270));canvas.paste(im,(x,28))
  frames.append(canvas)
 dest=out/(name+'.gif');frames[0].save(dest,save_all=True,append_images=frames[1:],duration=125,loop=0)
 with Image.open(dest) as check:assert check.n_frames>1
 manifest.append({'file':dest.name,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':str(root),'left':left,'right':right,'sourceFrames':[len(lf),len(rf)],'derivedFps':8,'audio':False,'nativeInput':False,'humanPlaytest':False,'note':'Full-frame resize; sequences independently start at their first capture. Unequal tail held; not synchronized damage timing measurement.'})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(json.dumps(manifest,indent=2))

