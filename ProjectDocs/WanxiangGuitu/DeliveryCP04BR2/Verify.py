from pathlib import Path
import json,hashlib,re,subprocess,importlib.util
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR2');r=Path('I:/WGCombat/CP04BR2-1102-A');errors=[];manifest=json.loads((p/'Evidence/Raw/manifest.json').read_text());check=[]
for x in manifest:
 f=p/'Evidence/Raw'/x['path'];h=hashlib.sha256(f.read_bytes()).hexdigest()
 if h!=x['publishedSHA256']:errors.append('hash '+x['path'])
for f in p.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf-8-sig')):
  if not link.startswith(('http:','https:','#')) and not (f.parent/link.split('#')[0]).exists():errors.append('link '+str(f.relative_to(p))+' '+link)
spec=importlib.util.spec_from_file_location('verifyEvidence',p/'ValidateEvidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if not m.editor(json.loads((r/'Allocation6/scoped-events.json').read_text())):errors.append('editor calibration')
for run in ['MonoPlayer','MonoPlayerRepeat']:
 if not m.player(json.loads((r/run/'mono-probe.json').read_text())):errors.append(run+' calibration')
 cmd=json.loads((r/run/'BR2MonoPlayer.command.json').read_text(encoding='utf-8-sig'));ex=json.loads((r/run/'BR2MonoPlayer.exit.json').read_text(encoding='utf-8-sig'))
 if cmd['hostPid']!=ex['hostPid'] or ex['exitCode']!=0:errors.append(run+' actual process evidence')
pro=json.loads((r/'protection-and-il.json').read_text())
if not pro['sourceFrozen'] or not pro['normalizedAimILSame'] or pro['pureTestTypes'] or not pro['noEditorRefs'] or any(pro[x]['changed'] for x in ['productAndUser','cp04bHistory','brHistory']):errors.append('protection')
for x in json.loads((r/'bee-services-current.json').read_text()):
 if not x['destination'].replace('\\','/').startswith('I:/WGCombat/CP04BR2-1102-A/'+x['role']+'/Release/') or x['development'] is not False:errors.append('Bee identity')
identity=json.loads((r/'native-identity.json').read_text())
if not identity['matching']:errors.append('PDB identity')
out={'status':'PASS' if not errors else 'FAIL','scope':'Delivery integrity and tool-evidence validation, NOT overall game/performance acceptance','rawArtifacts':len(manifest),'manifestSHA256':hashlib.sha256((p/'Evidence/Raw/manifest.json').read_bytes()).hexdigest(),'errors':errors};(p/'Evidence/DELIVERY_VERIFY.json').write_text(json.dumps(out,indent=2));print(out);raise SystemExit(bool(errors))
