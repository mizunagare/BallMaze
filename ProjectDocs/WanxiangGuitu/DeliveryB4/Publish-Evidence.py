"""B4 allowlisted publication; reuse the existing redaction/manifest publisher.

Never publish saves, dumps, binaries or Library. Settlement summaries omit plans.
"""
import argparse, hashlib, importlib.util, json, struct, subprocess, sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--target', type=Path, required=True)
a = p.parse_args()
here = Path(__file__).resolve().parent
if a.target.exists():
    p.error('Fresh evidence target required; previous attempts must survive')
subprocess.run([sys.executable, '-B', str(here.parent/'DeliveryB3/Publish-Evidence.py'),
                '--run', str(a.run), '--target', str(a.target)], check=True)
spec = importlib.util.spec_from_file_location('reviewed_publisher', here.parent/'DeliveryUI01/Automation/publish-evidence.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
paths = []
for name in ('b4-topology.csv', 'b4-topology.txt', 'b4-physical.csv', 'b4-physical.txt',
             'b4-state-results.txt', 'b4-pickup.txt'):
    if (a.run/'Rules'/name).is_file():
        paths.append('Rules/'+name)
for folder in sorted(a.run.glob('Normal-*')):
    for name in ('metadata.txt', 'normal-results.txt', 'normal-ai.csv', 'storage-audit.jsonl',
                 'Normal.log', 'Resume.log', 'FinalResume.log', 'b4-expected.json',
                 'b4-checkpoint-1.json', 'b4-checkpoint-2.json',
                 'process-result-Normal.json', 'process-result-Resume.json', 'process-result-FinalResume.json'):
        if (folder/name).is_file():
            paths.append((folder/name).relative_to(a.run).as_posix())
    for item in sorted(folder.glob('ExecutedDrivers-*/*')):
        # Exact executed drivers are test sources, not product saves.
        if item.is_file() and item.suffix in ('.txt', '.json'):
            paths.append(item.relative_to(a.run).as_posix())
for folder_name in ('Default-1', 'Default-2', 'D3D11-1', 'D3D11-2', 'Default-dump'):
    folder = a.run/folder_name
    for pattern in ('process-*.json', 'timeline-*.json', 'analysis-*.json', 'ui-*.json',
                    'close-*.json', 'player-*.log', 'player-*.command.json', 'player-*.exit.json',
                    'player-*.desktop-process.json', 'player-*.stderr', 'storage-audit.jsonl'):
        paths.extend(item.relative_to(a.run).as_posix() for item in folder.glob(pattern) if item.is_file())
if paths:
    m.publish(a.run, a.target/'B4Diagnostics', sorted(set(paths)))

images = []
for name in ('after-1280x720-100-route.png', 'after-1920x1080-100-route.png',
             'after-1280x720-100-empty.png', 'after-1920x1080-100-empty.png'):
    item=a.run/'ControlledScreens'/name
    if not item.is_file(): continue
    data=item.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n': raise ValueError('Invalid screenshot')
    relative=Path('Screens/Controlled')/name
    (a.target/relative).parent.mkdir(parents=True,exist_ok=True)
    (a.target/relative).write_bytes(data)
    width,height=struct.unpack('>II',data[16:24])
    images.append(dict(file=relative.as_posix(),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
                       width=width,height=height,scope='Controlled UI capture; NOT native UI'))
for folder in sorted(a.run.glob('Normal-*')):
    for item in sorted(folder.glob('*.png')):
        data = item.read_bytes()
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('Invalid screenshot: '+str(item))
        relative = Path('Screens')/folder.name/item.name
        (a.target/relative).parent.mkdir(parents=True, exist_ok=True)
        (a.target/relative).write_bytes(data)
        width, height = struct.unpack('>II', data[16:24])
        images.append(dict(file=relative.as_posix(), sha256=hashlib.sha256(data).hexdigest(),
                           bytes=len(data), width=width, height=height,
                           scope='Normal NPC AI with domain bot; NOT native UI'))
    item = folder/'b4-first-settlement.json'
    if item.is_file():
        record = json.loads(item.read_text(encoding='utf-8-sig'))
        summary = {key: value for key, value in record.items() if not key.lower().startswith('plan')}
        summary['originalSha256'] = hashlib.sha256(item.read_bytes()).hexdigest()
        summary['publicationNote'] = 'Synthetic settlement evidence; commit plans deliberately omitted'
        output = a.target/'SettlementSummaries'/(folder.name+'.json')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(a.target/'b4-screens.json').write_text(json.dumps(images, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
drivers = [dict(path=item.relative_to(a.run).as_posix(), sha256=hashlib.sha256(item.read_bytes()).hexdigest())
           for item in sorted(a.run.glob('Normal-*/ExecutedDrivers-*/*')) if item.is_file()]
(a.target/'executed-drivers.json').write_text(json.dumps(drivers,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=a.run/'Build/Release/BuildSummary.txt'
if summary.is_file():
    (a.target/'build-summary.json').write_text(json.dumps(dict(source='Build/Release/BuildSummary.txt',
        originalSha256=hashlib.sha256(summary.read_bytes()).hexdigest(),
        summary=summary.read_text(encoding='utf-8-sig')),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
