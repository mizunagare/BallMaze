"""Extend the reviewed publisher with R1 diagnostics, never player save payloads."""
import argparse, hashlib, importlib.util, json, struct, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB07/Publish-Evidence.py'),'--run',str(a.run),'--target',str(a.target)],check=True)
spec=importlib.util.spec_from_file_location('publisher',here.parent/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
paths=[item.relative_to(a.run).as_posix() for folder in (a.run,a.run/'Rules') for item in sorted(folder.glob('b07r1-*')) if item.suffix in ('.csv','.txt','.json')]
if paths:m.publish(a.run,a.target/'Readability',paths)
if (a.run/'driver.cs.txt').is_file():m.publish(a.run,a.target/'ReadabilitySource',['driver.cs.txt'])
logs=[item.relative_to(a.run).as_posix() for item in sorted((a.run/'Rules').glob('B07Readability*.log'))]
if logs:m.publish(a.run,a.target/'ReadabilityLogs',logs,archive=True)
images=[]
for folder in (a.run,a.run/'Rules'):
 for item in sorted(folder.glob('b07r1-*.png')):
  data=item.read_bytes()
  if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid PNG')
  rel=Path('ReadabilityScreens')/item.name;out=a.target/rel;out.parent.mkdir(exist_ok=True);out.write_bytes(data);w,h=struct.unpack('>II',data[16:24]);images.append(dict(file=rel.as_posix(),width=w,height=h,sha256=hashlib.sha256(data).hexdigest(),scope='Controlled actual Unity renderer/orbit camera; NPC disabled; NOT normal AI or native UI'))
(a.target/'readability-screens.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
