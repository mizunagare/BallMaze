from pathlib import Path
from PIL import Image
import json,shutil,subprocess,sys
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False);script=Path(__file__).with_name('RenderReceipt.py');rows=[]
def case(name,mutate,status,code):
 p=out/name;p.mkdir()
 for f in ['br-probe.json','runtime.json','Player.desktop-process.json']:shutil.copyfile(source/f,p/f)
 r=json.loads((p/'br-probe.json').read_text(encoding='utf-8-sig'))
 for f in r['captures']:shutil.copyfile(source/f,p/f)
 mutate(p,r);result=subprocess.run([sys.executable,str(script),str(p),str(p/'receipt.json')],capture_output=True,text=True);actual=json.loads((p/'receipt.json').read_text())
 rows.append({'name':name,'scope':'synthetic tool selftest, not real Player evidence','expectedStatus':status,'expectedExit':code,'actualStatus':actual['status'],'actualExit':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'status':'PASS' if actual['status']==status and result.returncode==code else 'FAIL'})
def write(p,r):(p/'br-probe.json').write_text(json.dumps(r),encoding='utf8')
case('valid',lambda p,r:None,'PASS',0)
case('missing-picture',lambda p,r:(p/r['captures'][0]).unlink(),'INCOMPLETE',3)
case('malformed',lambda p,r:(p/'br-probe.json').write_text('{'),'INCOMPLETE',3)
def hidden(p,r):r['renderStates'][0]['visible']=False;write(p,r)
case('hidden',hidden,'FAIL',1)
def no_render(p,r):r['renderStates'][0]['cameraRendered']=0;write(p,r)
case('no-camera-frame',no_render,'FAIL',1)
case('black',lambda p,r:Image.new('RGB',(1280,720)).save(p/r['captures'][0]),'FAIL',1)
case('bad-exit',lambda p,r:(p/'runtime.json').write_text(json.dumps({'exitCode':1,'timedOut':False,'exited':True,'forcedTermination':False})),'FAIL',1)
(out/'selftests.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows,indent=2));sys.exit(any(r['status']!='PASS' for r in rows))
