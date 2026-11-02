from pathlib import Path
import json,hashlib
r=Path('I:/WGCombat/CP04BR2-1102-A');rows=[]
for project,target in [('Fixed','MonoBuild'),('Control','ConnectControlBuild')]:
 expected=f'I:/WGCombat/CP04BR2-1102-A/{target}/Release/WanxiangGuitu.exe'
 for p in (r/project/'Project/Library/Bee').glob('Player*-inputdata.json'):
  j=json.loads(p.read_text(encoding='utf-8-sig'));config=j.get('PlayerBuildProgramLibrary.Data.PlayerBuildConfig',{})
  if config.get('DestinationPath','').replace('\\','/').lower()!=expected.lower():continue
  rows.append({'role':target,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'destination':config['DestinationPath'],'development':config.get('Development'),'services':config['Services']})
assert len(rows)==2
(r/'bee-services-current.json').write_text(json.dumps(rows,indent=2));(r/'bee-cache-inventory-note.json').write_text(json.dumps({'scope':'Correction of evidence selection, not product correction','file':'bee-services-snapshots.json','issue':'The initial broad glob includes inherited cache entries and labels them by container project; it is NOT a per-run build receipt. Do not use its role labels as run identity.','authoritative':'bee-services-current.json selects exact PlayerBuildConfig.DestinationPath matching this run output; source SHA retained.'},indent=2));print(rows)
