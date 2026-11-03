from pathlib import Path
import json,hashlib,subprocess,sys
root=Path('I:/WGCombat/CP05BR-1103-A');repo=Path(__file__).resolve().parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((root/'protected-before.json').read_text(encoding='utf-8-sig'));errors=[]
for r in before:
 p=Path(r['path'])
 if not p.is_file() or sha(p)!=r['sha256']:errors.append(str(p))
baseline='b27bda440201937a01a3add69311d3f982789194';historical=subprocess.check_output(['git','diff',baseline,'--name-only','--','ProjectDocs/WanxiangGuitu/DeliveryCP05B'],cwd=repo).decode().strip()
if historical:errors.append('Historical CP05B changed: '+historical)
names=['CombatAim.cs','AdventureCombat.cs','OrbitCamera.cs','CameraActorFade.cs','TargetAssist.cs','CombatAssistOptions.cs','CP05Training.cs','Editor/CP05Build.cs','Resources/CP05Training/Hero.prefab','Resources/CP05Training/Enemy.prefab'];parity=[]
for n in names:
 source=repo/'Assets/CombatPrototype'/n;copy=root/'Project/Assets/CombatPrototype'/n;row={'path':'Assets/CombatPrototype/'+n,'sourceSHA256':sha(source),'isolatedInputSHA256':sha(copy)};parity.append(row)
 if row['sourceSHA256']!=row['isolatedInputSHA256']:errors.append('Runtime input changed '+n)
native=Path('I:/WGCombat/CP04BR2-1102-A/Native/BR2AllocationNative.dll')
r={'status':'FAIL' if errors else 'PASS','baseline':baseline,'protectedFiles':len(before),'changed':errors,'historicalDiff':historical,'productSourceToInput':parity,'nativeProfilerSHA256':sha(native),'scope':'Original product/user files unchanged. Unity serialized writeback in disposable build copy is separately listed, not source changes.'}
derived=[]
for folder in ('Assets/Settings','ProjectSettings','Packages'):
 for p in (repo/folder).rglob('*'):
  q=root/'Project'/p.relative_to(repo)
  if p.is_file() and q.is_file() and sha(p)!=sha(q):derived.append({'path':p.relative_to(repo).as_posix(),'source':sha(p),'isolatedAfter':sha(q)})
r['isolatedSerializedDifferences']=derived
Path(sys.argv[1]).write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2));sys.exit(bool(errors))
