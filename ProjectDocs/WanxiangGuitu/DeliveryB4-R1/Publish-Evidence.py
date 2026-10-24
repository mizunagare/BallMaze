"""Extend the reviewed B4 allowlisted redacting publisher with R1 diagnostics."""
import argparse,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args()
here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB4/Publish-Evidence.py'),'--run',str(a.run),'--target',str(a.target)],check=True)
spec=importlib.util.spec_from_file_location('publisher',here.parent/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
paths=[item.relative_to(a.run).as_posix() for item in sorted((a.run/'Rules').glob('r1-*')) if item.is_file() and item.suffix in ('.csv','.txt','.json','.jsonl')]
paths += [item.relative_to(a.run).as_posix() for item in sorted((a.run/'TerrainScreens').glob('r1-*')) if item.is_file() and item.suffix in ('.csv','.txt','.json','.jsonl')]
paths += [item.relative_to(a.run).as_posix() for item in sorted(a.run.glob('r1-*')) if item.is_file() and item.suffix in ('.csv','.txt','.json','.jsonl')]
paths += [item.relative_to(a.run).as_posix() for item in sorted((a.run/'Rules').glob('score-*')) if item.is_file() and item.suffix in ('.csv','.txt','.json','.jsonl')]
paths += [item.relative_to(a.run).as_posix() for folder in sorted(a.run.glob('Normal-*')) if folder.is_dir() for item in sorted(folder.glob('score-normal-*.json')) if item.is_file()]
if paths:m.publish(a.run,a.target/'R1Diagnostics',paths)
logs=[item.relative_to(a.run).as_posix() for item in sorted((a.run/'TerrainScreens').glob('*.log'))]
if (a.run/'shore.log').is_file():logs.append('shore.log')
if logs:m.publish(a.run,a.target/'R1Logs',logs,archive=True)
images=[]
for folder in ('TerrainScreens','Rules','.'):
 for item in sorted((a.run/folder).glob('r1-*.png')):
  data=item.read_bytes()
  if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid PNG')
  relative=Path('R1Screens')/item.name;(a.target/relative).parent.mkdir(exist_ok=True);(a.target/relative).write_bytes(data)
  width,height=struct.unpack('>II',data[16:24]);images.append(dict(file=relative.as_posix(),width=width,height=height,sha256=hashlib.sha256(data).hexdigest(),scope='Controlled Unity camera/GUI capture; NOT native UI or normal AI'))
(a.target/'r1-screens.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
preflight=a.run/'preflight.json'
if preflight.is_file():
 raw=preflight.read_bytes();data=json.loads(raw.decode('utf-8-sig'))
 safe={key:data.get(key) for key in ('freeBytes','requiredGB','unityExists','pythonExists','installedUnity','projectVersion','sourceHead')}
 safe.update(originalSha256=hashlib.sha256(raw).hexdigest(),policy='Safe preflight fields only; process command lines and source-status contents omitted')
 (a.target/'preflight-safe-summary.json').write_text(json.dumps(safe,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
