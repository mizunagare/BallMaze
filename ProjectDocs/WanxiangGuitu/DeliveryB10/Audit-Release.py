"""Extend existing ended-run release audit. No game or save mutation."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--baseline',required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB09/Audit-Release.py'),'--project',str(a.project),'--run',str(a.run),'--target',str(a.target),'--baseline',a.baseline],check=True)
raw=(a.run/'Build/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll').read_bytes()
runtime={s:s.encode() in raw for s in ['BootEntry','CatWorldArt','CatActorVisual','CatInventoryPresenter','CatUI','CatWorldScenery','CatIconLayout']}
excluded={s:s.encode() in raw for s in ['B10ControlledPlayer','B10VisualMover','B10Rules','B10Cats','B10ArtSpec','CatWorldBake','SetNextSeedForValidation']}
result=dict(status='PASS' if all(runtime.values()) and not any(excluded.values()) else 'FAIL',scope='Static shipping metadata; controlled validation Player deliberately has a driver, this release must not',runtime=runtime,testNamesPresent=excluded,sha256=hashlib.sha256(raw).hexdigest())
(a.target/'release-cat-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
resources=[]
for f in sorted((a.project/'Assets/CombatPrototype/Resources/CatWorld').rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(a.project);b=(a.run/'Project'/rel).read_bytes();resources.append(dict(path=rel.as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),inputSha256=hashlib.sha256(b).hexdigest(),equal=f.read_bytes()==b))
(a.target/'cat-resource-input-check.json').write_text(json.dumps(dict(status='PASS' if all(x['equal'] for x in resources) else 'FAIL',files=resources),indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(release=result['status'],resources=len(resources),allEqual=all(x['equal'] for x in resources))))
raise SystemExit(0 if result['status']=='PASS' and all(x['equal'] for x in resources) else 1)
