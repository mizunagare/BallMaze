from pathlib import Path
import json,hashlib,re,subprocess,sys
repo=Path(sys.argv[1]);base=repo/'ProjectDocs/WanxiangGuitu/DeliveryGameplayUX02';sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((base/'Evidence/manifest.json').read_text(encoding='utf-8-sig'))
for x in manifest:assert sha((base/'Evidence'/x['path']).read_bytes())==x['sha256'],x['path']
for p in base.glob('*.md'):
 for rel in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
  if '://' not in rel:assert (p.parent/rel.split('#')[0]).exists(),(p.name,rel)
for rel in re.findall(r'\]\(([^)]+)\)',(base/'Evidence/INDEX.md').read_text(encoding='utf-8-sig')):assert (base/'Evidence'/rel).exists(),rel
names=subprocess.check_output(['git','-C',str(repo),'diff','--cached','--name-only'],text=True).splitlines()
allowed={'Assets/CombatPrototype/'+x+'.cs' for x in ('CombatFeedback',)}
assert all(x in allowed or x.startswith('ProjectDocs/WanxiangGuitu/DeliveryGameplayUX02/') for x in names)
j=json.loads((base/'Evidence/final-bindings.json').read_text(encoding='utf-8-sig'))
for x in j['sources']:
 staged=subprocess.check_output(['git','-C',str(repo),'show',':'+x['path']]);assert sha(staged.replace(b'\r\n',b'\n'))==x['canonicalLF'],x['path']
for x in j['userProtection']:assert sha(Path(x['path']).read_bytes()).lower()==x['before'].lower(),x['path']
for x in names:
 assert not x.endswith(('.exe','.dll')),x
print('PASS:',len(manifest),'published hashes; links; staged source/build bindings; five protected files; scope')
