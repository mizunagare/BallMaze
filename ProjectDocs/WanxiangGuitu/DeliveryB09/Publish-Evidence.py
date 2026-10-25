"""B09 allowlisted extension of existing evidence publication, never saves/builds."""
import argparse, hashlib, importlib.util, json, struct, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB08/Publish-Evidence.py'),'--run',str(a.run),'--target',str(a.target)],check=True)
spec=importlib.util.spec_from_file_location('pub',here.parent/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
paths=[];images=[];logs=[]
for folder in [a.run,a.run/'Rules']+sorted(a.run.glob('Normal-*'))+sorted(a.run.glob('B09-*')):
 if not folder.is_dir():continue
 for f in sorted(folder.iterdir()):
  if not f.is_file():continue
  if f.suffix=='.log' and (f.name.startswith('B09') or folder.name.startswith('B09-')):logs.append(f.relative_to(a.run).as_posix())
  if (f.name.startswith('b09-') and f.suffix in {'.txt','.csv','.json'}) or f.name=='entry-audit.jsonl' or (folder.name.startswith('B09-Title') and f.name in {'close.json','process.json','player.command.json','player.exit.json','player.desktop-process.json','save-before.json'}):paths.append(f.relative_to(a.run).as_posix())
  if f.suffix=='.png' and (f.name.startswith('b09-') or f.name=='title-player.png'):
   raw=f.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';rel=Path('B09Screens')/folder.name/f.name;out=a.target/rel
   if out.exists():raise ValueError('Fresh evidence output required')
   out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);w,h=struct.unpack('>II',raw[16:24]);images.append(dict(file=rel.as_posix(),width=w,height=h,sha256=hashlib.sha256(raw).hexdigest(),scope='Actual final Player observational title capture' if f.name=='title-player.png' else 'Actual controlled renderer, NOT native UI or human gameplay'))
if paths:m.publish(a.run,a.target/'B09Diagnostics',paths)
if logs:m.publish(a.run,a.target/'B09Logs',logs,archive=True)
(a.target/'b09-screens.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
