from pathlib import Path
import json,hashlib,subprocess,sys
r=Path(sys.argv[1]);out=Path(sys.argv[2]);baseline='31950f7bbd1f7946157632a52f1efd3854780340';root=Path('I:/WGCombat/C1-1105-A')
def digest(b):return hashlib.sha256(b).hexdigest()
protected=json.loads((root/'protected-before.json').read_text('utf-8-sig'));changes=[]
for i in protected:
 p=Path(i['path']);h=digest(p.read_bytes()) if p.is_file() else None
 if h!=i['sha256']:changes.append(dict(path=str(p),before=i['sha256'],actual=h))
core=['CombatAim.cs','TargetAssist.cs','OrbitCamera.cs','CameraActorFade.cs','AdventureCombat.cs','WeaponSkillCatalog.cs','NewWeaponRegistry.cs','NewWeaponDrop.cs','ReleaseDiagnosticsGuard.cs','ForestLayout.cs','ForestRegionRuntime.cs','EnemyProjectile.cs','WeaponSkillExpansion.cs','NewWeaponCombat.cs','ArmorMitigation.cs'];rows=[]
for name in core:
 for p in (r/'Assets').rglob(name):
  rel=p.relative_to(r).as_posix();b=subprocess.check_output(['git','-C',str(r),'show',baseline+':'+rel]);w=p.read_bytes();rows.append(dict(path=rel,baselineGitSHA256=digest(b),workingSHA256=digest(w),canonicalIdentical=b.replace(b'\r\n',b'\n')==w.replace(b'\r\n',b'\n'),note='Git text checkout LF/CRLF only, retain both raw hashes'))
vendor=json.loads(Path('I:/WGCombat/MAPTOOLS03-A/protection.json').read_text('utf-8-sig'));v=[]
for i in vendor['vendorFiles']:
 p=Path('I:/WGCombat/MAPTOOLS02-A/Project')/i['path'];h=digest(p.read_bytes()) if p.is_file() else None
 v.append(dict(path=i['path'],originalSHA256=i['originalSHA256'],actualSHA256=h,same=h==i['originalSHA256']))
for row in rows:
 match=next((x for x in protected if x['path'].replace('\\','/').endswith('WanxiangGuitu-CP04/'+row['path'])),None)
 row['protectedWindowsBaselineSHA256']=match['sha256'] if match else None
 row['rawWindowsIdentical']=match is not None and row['workingSHA256']==match['sha256']
files=[]
for folder in ['Assets','Packages','ProjectSettings']:
 for p in sorted((r/folder).rglob('*')):
  if p.is_file():files.append(dict(path=p.relative_to(r).as_posix(),sha256=digest(p.read_bytes()),bytes=p.stat().st_size))
ref=subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip();diff=subprocess.check_output(['git','-C',str(r),'diff','--name-only',baseline,'--','Assets','Packages','ProjectSettings'],text=True).splitlines()
result=dict(commit=ref,baseline=baseline,protectedCount=len(protected),protectedChanges=changes,frozenCore=rows,vendorCount=len(v),vendorChanges=[x for x in v if not x['same']],changedProductPaths=diff,productInputs=files,status='PASS' if not changes and all(x['canonicalIdentical'] for x in rows) and all(x['same'] for x in v) else 'FAIL')
assert not out.exists(),'Fresh audit output required';out.write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8');print(result['status'],len(files),'product inputs;',len(protected),'protected;',len(v),'vendor')
assert result['status']=='PASS'
