"""B07 adds allowlisted battle diagnostics to the existing redacting publisher.
No profile/save envelopes, ground-loot pages, dump files or build binaries are published.
"""
import argparse,hashlib,importlib.util,json,struct,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB4-R1/Publish-Evidence.py'),'--run',str(a.run),'--target',str(a.target)],check=True)
spec=importlib.util.spec_from_file_location('publisher',here.parent/'DeliveryUI01/Automation/publish-evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
paths=[]
for name in ['probe.log','combat.log','baseline-source.json','coordinator-failure.json','lock-proof.json','post-timeout-diagnostics.json','post-timeout-close.json','post-timeout-tool.json','test-input-amendment.json']:
 if (a.run/name).is_file():paths.append(name)
for item in sorted(a.run.glob('b07-*.txt')):
 if item.name in ['b07-combat.txt','b07-economy.txt','b07-liveness.txt']:paths.append(item.name)
for item in sorted(a.run.glob('b07-*.csv')):paths.append(item.name)

for name in ['b07-rules.txt','b07-nav.csv','b07-combat.txt','b07-hits.csv','b07-economy.txt','b07-liveness.txt','b07-liveness.csv','b07-interrupts.csv','b07-interrupts.txt']:
 if (a.run/'Rules'/name).is_file():paths.append('Rules/'+name)
for folder in sorted(a.run.glob('Normal-*')):
 for pattern in ['boss-combat.csv','boss-world.csv','attack-actions.csv']:
  for item in sorted(folder.glob(pattern)):paths.append(item.relative_to(a.run).as_posix())
for folder in sorted(a.run.glob('B07-*')):
 if folder.is_dir():
  for pattern in ['process-*.json','timeline-*.json','analysis-*.json','ui-*.json','close-*.json','player-*.log','player-*.command.json','player-*.exit.json','player-*.desktop-process.json','storage-audit.jsonl','b07-*.json']:
   paths += [item.relative_to(a.run).as_posix() for item in folder.glob(pattern) if item.is_file()]
if paths:m.publish(a.run,a.target/'B07Diagnostics',paths)
logs=[item.relative_to(a.run).as_posix() for item in sorted((a.run/'Rules').glob('B07*.log'))]
if logs:m.publish(a.run,a.target/'B07Logs',logs,archive=True)
images=[]
for item in sorted(list((a.run/'Rules').glob('b07-*.png'))+list(a.run.glob('b07-*.png'))):
 data=item.read_bytes()
 if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid PNG: '+str(item))
 rel=Path('B07Screens')/item.name;(a.target/rel).parent.mkdir(parents=True,exist_ok=True);(a.target/rel).write_bytes(data);w,h=struct.unpack('>II',data[16:24]);images.append(dict(file=rel.as_posix(),width=w,height=h,sha256=hashlib.sha256(data).hexdigest(),scope='Controlled live Unity combat hitbox/iframe capture; NOT normal AI or native input'))
(a.target/'b07-screens.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Preserve exact executed test sources separately from redacted runtime diagnostics.
# These are repository-owned synthetic drivers; no player save or credential data.
drivers=[]
for item in sorted(a.run.glob('Normal-*/ExecutedDrivers-*/*.cs')):
 rel=Path('Sources/ExecutedDrivers')/item.relative_to(a.run);rel=rel.with_name(rel.name+'.txt');out=a.target/rel;out.parent.mkdir(parents=True,exist_ok=True);raw=item.read_bytes();out.write_bytes(raw);drivers.append(dict(file=rel.as_posix(),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
(a.target/'b07-executed-driver-sources.json').write_text(json.dumps(drivers,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
