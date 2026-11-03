from pathlib import Path
import json,hashlib,sys
r=Path(sys.argv[1]);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();before=json.loads((r/'protected-before.json').read_text(encoding='utf8'));allowed='H:/unity/WanxiangGuitu-CP04/Assets/CombatPrototype/Editor/ReleaseDiagnosticsGuard.cs';changes=[]
for x in before:
 if Path(x['path']).as_posix()==allowed:continue
 if not Path(x['path']).exists() or sha(x['path'])!=x['sha256']:changes.append(x['path'])
rows=[]
for file in ['GuardTests/guard-tests.json','OriginalNegatives/real-negatives.json','R1Negatives/r1-negatives.json','marker-tests.json']:
 j=json.loads((r/file).read_text(encoding='utf-8-sig'));rs=j['rows'] if isinstance(j,dict) else j;rows.append({'file':file,'count':len(rs),'PASS':sum(x['status']=='PASS' for x in rs),'FAIL':sum(x['status']=='FAIL' for x in rs)})
result={'protectedChecked':len(before)-1,'unexpectedChanges':changes,'tests':rows,'aimSHA256':sha('H:/unity/WanxiangGuitu-CP04/Assets/CombatPrototype/CombatAim.cs'),'onlyAuthorizedEditorChange':allowed};(r/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(result);sys.exit(bool(changes) or any(x['FAIL'] for x in rows))
