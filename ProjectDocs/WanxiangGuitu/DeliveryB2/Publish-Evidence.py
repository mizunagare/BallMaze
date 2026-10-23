"""Publish explicit B2 diagnostics using the existing redacting publisher. No saves/dumps/builds."""
import argparse, hashlib, importlib.util, json, struct
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--run',type=Path,required=True)
parser.add_argument('--target',type=Path,required=True)
parser.add_argument('--visual',action='store_true')
a=parser.parse_args()
if a.target.exists():parser.error("New evidence directory required; preserve prior runs")
helper=Path(__file__).resolve().parent.parent/'DeliveryUI01/Automation/publish-evidence.py'
spec=importlib.util.spec_from_file_location('reviewed_publisher',helper)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
paths=[]
for name in ('owner.json','results.json','results.csv','counts.json','REPORT.md','test-plan.json','build-manifest.json','preserved-processes.json','b2-visual-result.txt','b2-visual.jsonl','visual.log'):
    if (a.run/name).is_file():paths.append(name)
for pattern in ('*.command.json','*.exit.json','*.desktop-process.json','*.stderr'):
    paths.extend(p.relative_to(a.run).as_posix() for p in a.run.glob(pattern))
for name in ('b2-results.txt','ui01-results.txt'):
    if (a.run/'Rules'/name).is_file():paths.append('Rules/'+name)
for name in ('normal-results.txt','normal-ai.csv','metadata.txt','expected-normal.txt','b2-target-expected.txt','process-result-Normal.json','process-result-Resume.json','storage-audit.jsonl','Normal.log','Resume.log'):
    if (a.run/'Normal'/name).is_file():paths.append('Normal/'+name)
module.publish(a.run,a.target,sorted(set(paths)))
logs=sorted(p.relative_to(a.run).as_posix() for folder in ('Rules','Build','ControlledScreens') for p in (a.run/folder).glob('*.log'))
if logs:module.publish(a.run,a.target/'Logs',logs,archive=True)
images=[]
for p in sorted(a.run.glob('b2-*.png') if a.visual else (a.run/'Normal').glob('*.png')):
    data=p.read_bytes()
    if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid PNG')
    relative=Path('Screens')/p.name
    (a.target/relative).parent.mkdir(parents=True,exist_ok=True)
    (a.target/relative).write_bytes(data)
    width,height=struct.unpack('>II',data[16:24])
    images.append(dict(file=relative.as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),width=width,height=height,scope='controlled UI' if a.visual else 'scripted normal AI; not native UI'))
# Keep a hash inventory of the old 92 captures, without duplicating that large archive.
legacy=[dict(file=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted((a.run/'ControlledScreens').glob('*.png'))]
(a.target/'screens.json').write_text(json.dumps(dict(published=images,controlledUiInventory=legacy),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
