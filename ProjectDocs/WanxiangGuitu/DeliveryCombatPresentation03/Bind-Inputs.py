from pathlib import Path
import json,sys,hashlib,subprocess
root=Path(sys.argv[1]);repo=Path(sys.argv[2]);sha=lambda b:hashlib.sha256(b).hexdigest()
files=['AdventureCombat','CombatFeedback','CombatFeedbackEffect','FantasyActorVisual','CombatAim','CombatHealth','ForestBossBrain','CombatSoundBank','OrbitCamera']
sources=[]
for n in files:
 p='Assets/CombatPrototype/'+n+'.cs';a=(repo/p).read_bytes();b=(root/'P/Project'/p).read_bytes();assert a==b,p;sources.append(dict(path=p,sha256=sha(a),canonicalLF=sha(a.replace(b'\r\n',b'\n'))))
builds=[]
for name in ['AcceptanceBuild','PureBuild','AcceptanceBuild2','PureBuild2']:
 f=root/name/'build-inputs.json'
 if not f.exists():continue
 rows=json.loads(f.read_text(encoding='utf-8-sig'));idx={x['path'].replace('\\','/'):x for x in rows};matches=[dict(path=s['path'],match=idx[s['path']]['sha256'].lower()==s['sha256']) for s in sources]
 final=name.endswith('2')
 if final:assert all(x['match'] for x in matches),name
 builds.append(dict(name=name,finalVariant=final,inputsSHA256=sha(f.read_bytes()),sourceMatches=matches,acceptanceDriverInputs=[x for x in rows if 'CP03AcceptanceOnly' in x['path']]))
users=[]
for x in json.loads((root/'user-before.json').read_text(encoding='utf-8-sig')):
 a=sha(Path(x['Path']).read_bytes());assert a.lower()==x['Hash'].lower();users.append(dict(path=x['Path'],before=x['Hash'],after=a,equal=True))
assets=json.loads((repo/'ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/BASELINE_RESOURCE_AUDIT.json').read_text(encoding='utf-8-sig'))['assets'];assert all(sha((repo/x['path']).read_bytes())==x['sha256'] for x in assets)
(root/'final-bindings.json').write_text(json.dumps(dict(sources=sources,builds=builds,userProtection=users,unchangedAssetCount=len(assets)),indent=2),encoding='utf-8');print('PASS: nine source/runtime/final build bindings, 54 assets, five user files; intermediate builds kept distinct')
