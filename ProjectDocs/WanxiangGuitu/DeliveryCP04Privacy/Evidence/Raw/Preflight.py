from pathlib import Path
import json,hashlib
r=Path('I:/WGCombat/CP04PRIVACY-1103-A');found=[];expected=str(r/'DisabledBuild/Release/WanxiangGuitu.exe').replace('\\','/')
for p in (r/'Isolated/Project/Library/Bee').glob('Player*-inputdata.json'):
 j=json.loads(p.read_text(encoding='utf-8-sig'));c=j.get('PlayerBuildProgramLibrary.Data.PlayerBuildConfig',{})
 if c.get('DestinationPath','').replace('\\','/').lower()==expected.lower():found.append({'source':str(p),'sourceSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'destination':c['DestinationPath'],'development':c['Development'],'services':c['Services']})
assert len(found)==1
(r/'bee-disabled.json').write_text(json.dumps(found[0],indent=2));assert not any(found[0]['services'].values()),'Refuse launch: some native service still enabled'
files=[]
for p in sorted((r/'DisabledBuild/Release').rglob('*')):
 if p.is_file():files.append({'path':p.relative_to(r/'DisabledBuild/Release').as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(r/'release-files.json').write_text(json.dumps(files,indent=2));print(found[0]);print('release files',len(files))
