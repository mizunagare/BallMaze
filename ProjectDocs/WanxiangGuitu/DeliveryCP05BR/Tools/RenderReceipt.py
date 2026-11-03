from pathlib import Path
from PIL import Image
import json,sys,hashlib
def evaluate(folder):
 p=Path(folder);errors=[];images=[]
 try:
  r=json.loads((p/'br-probe.json').read_text(encoding='utf-8-sig'));process=json.loads((p/'runtime.json').read_text(encoding='utf-8-sig'));host=json.loads((p/'Player.desktop-process.json').read_text(encoding='utf-8-sig'))
  if process.get('exitCode')!=0 or process.get('timedOut') is not False or process.get('exited') is not True or process.get('forcedTermination') is not False:errors.append('No successful observed process exit')
  states=r['renderStates'];files=r['captures']
  if len(states)!=7 or len(files)!=7 or len(set(files))!=7:errors.append('Missing/duplicate render evidence')
  for state in states:
   if not state['visible'] or state['minimized'] or not state['cameraEnabled'] or state['cameraRendered']<=0 or state['targetTexture']!='BACKBUFFER' or state['cullingMask']==0 or state['screenWidth']!=1280 or state['screenHeight']!=720:errors.append('No valid visible camera/backbuffer state')
  for name in files:
   f=(p/name).resolve()
   if f.parent!=p.resolve():raise ValueError('Capture path outside run')
   with Image.open(f) as im:
    rgb=im.convert('RGB');black=all(v[1]==0 for v in rgb.getextrema());colors=rgb.getcolors(16);constant=colors is not None and len(colors)<16
    if im.size!=(1280,720) or black or constant:errors.append('Invalid visual frame '+name)
    images.append({'path':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'allBlack':black,'constant':constant})
  return {'status':'FAIL' if errors else 'PASS','scope':'Actual instrumented nondevelopment Player camera frames and own window state; NOT pure-package/native-input/human acceptance','errors':errors,'images':images,'inputDesktopActive':host['inputDesktopActive'],'showMode':host['showMode'],'physicalInput':'NOT_RUN','humanExperience':'NOT_RUN'}
 except (OSError,ValueError,KeyError,TypeError) as e:return {'status':'INCOMPLETE','errors':[str(e)],'scope':'Required render evidence missing or malformed'}
if __name__=='__main__':
 r=evaluate(sys.argv[1]);out=Path(sys.argv[2]);assert not out.exists(),'Fresh report path required';out.write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps({'status':r['status'],'errors':r['errors']},indent=2));sys.exit({'PASS':0,'FAIL':1,'INCOMPLETE':3}[r['status']])
