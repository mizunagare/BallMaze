"""Bind pure build inputs, observed sources and preserved user files; read only."""
import pathlib,json,hashlib,sys,subprocess
repo=pathlib.Path(sys.argv[1]);root=pathlib.Path(sys.argv[2]);base='ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(b):return b.replace(b'\r\n',b'\n')
rows=[];bad=[]
inputs={r['path'].replace('\\','/'):r for r in read(root/'PureBuild/build-inputs.json')}
for name in ['CombatEnemy','EnemyProjectile','ForestBossBrain','BossBrain']:
 rel=f'Assets/CombatPrototype/{name}.cs';data=(repo/rel).read_bytes();build=inputs[rel]
 clone=(root/'F/Project'/rel).read_bytes();old=subprocess.check_output(['git','-C',str(repo),'show','49aadd5088453b606029ab558e0e1a2262dc6e7a:'+rel])
 observed=[]
 for folder in ['BeforeInstrumentation','AfterInstrumentation','FinalInstrumentation']:
  p=root/folder/f'{name}.raw.cs'
  if p.exists():observed.append(dict(stage=folder,rawSHA256=sha(p.read_bytes()),canonicalLF=sha(norm(p.read_bytes()))))
 okay=sha(data)==build['sha256'].lower() and data==clone
 rows.append(dict(path=rel,status='PASS' if okay else 'FAIL',baselineCanonicalLF=sha(norm(old)),finalRawSHA256=sha(data),finalCanonicalLF=sha(norm(data)),pureBuildInputSHA256=build['sha256'],observationOriginals=observed))
 if not okay:bad.append(rel)
protected=[]
for r in read(root/'user-before.json'):
 p=pathlib.Path(r['Path']);actual=sha(p.read_bytes()) if p.is_file() else 'MISSING';okay=actual==r['Hash'].lower();protected.append(dict(path=str(p),beforeSHA256=r['Hash'],afterSHA256=actual,status='PASS' if okay else 'FAIL'))
 if not okay:bad.append(str(p))
locks=read(root/'locked-contracts.json')
for r in locks:
 okay=sha((repo/r['path']).read_bytes())==r['sha256'].lower() and r['unchanged']
 if not okay:bad.append(r['path'])
result=dict(status='FAIL' if bad else 'PASS',baselineProduct='49aadd5088453b606029ab558e0e1a2262dc6e7a',taskOnlyFastForward='efaf541fc6c3b6d66c9f0a0ca0e3353e176ca30c',productSources=rows,userFiles=protected,lockedContracts=locks,failures=bad,scope='raw build/source equality; canonical-LF source binding for Git line endings. User scene/settings excluded from all builds; clones use baseline Git variants. New hashes do not claim independent review or native Player execution.')
(root/'input-binding.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(status=result['status'],productSources=len(rows),userFiles=len(protected),lockedContracts=len(locks),failures=bad),ensure_ascii=False))
if bad:raise SystemExit(1)
