"""Bind current product sources to every actual build input, retain failures separately."""
from pathlib import Path
import json,hashlib,sys
root=Path(sys.argv[1]);repo=Path(sys.argv[2]);sha=lambda b:hashlib.sha256(b).hexdigest()
files=['Assets/CombatPrototype/'+n+'.cs' for n in ('CombatFeedback','AdventureCombat','CombatHealth','ForestBossBrain','FantasyActorVisual','CombatFeedbackEffect','OrbitCamera')]
rows=[]
for path in files:
 a=(repo/path).read_bytes();b=(root/'P/Project'/path).read_bytes()
 rows.append(dict(path=path,repositorySHA256=sha(a),runtimeCopySHA256=sha(b),equal=a==b,canonicalLF=sha(a.replace(b'\r\n',b'\n'))))
builds=[]
for name in ('AcceptanceBuild','PureBuild'):
 p=root/name/'build-inputs.json'
 if not p.exists():continue
 inp=json.loads(p.read_text(encoding='utf-8-sig'));m={x['path'].replace('\\','/'):x for x in inp}
 builds.append(dict(name=name,inputsSHA256=sha(p.read_bytes()),sourceMatches=[dict(path=r['path'],match=m.get(r['path'],{}).get('sha256','').lower()==r['runtimeCopySHA256']) for r in rows],runtimeDriverInputs=[x for x in inp if 'GUXAcceptanceOnly' in x['path']]))
users=[]
for x in json.loads((root/'user-before.json').read_text(encoding='utf-8-sig')):
 p=Path(x['Path']);users.append(dict(path=str(p),before=x['Hash'],after=sha(p.read_bytes()),equal=x['Hash'].lower()==sha(p.read_bytes())))
r=dict(sources=rows,builds=builds,userProtection=users)
(root/'final-bindings.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
assert all(x['equal'] for x in rows+users)
assert all(x['match'] for b in builds for x in b['sourceMatches'])
print('PASS source/build/user binding; builds',len(builds),'user files',len(users))
