"""Postprocess an ended directed run. Same artifacts; no execution or save access.
The older All auditor requires report.finalized, which directed runs do not emit.
We verify the directed runner's actual sealed process ledger instead of forging that row.
"""
import argparse,hashlib,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
root=a.run.resolve(strict=True);source=a.project.resolve(strict=True)
if not a.run.is_absolute() or a.output.exists() or read(root/'owner.json').get('kind')!='B4 directed checks using existing orchestration' or read(root/'preserved-processes.json')!=[]:raise ValueError('Ended directed owner and fresh output required')
steps=read(root/'results.json');build=[r for r in steps if r['name']=='WanxiangBuild.ValidateBuild']
if len(build)!=1 or build[0]['status']!='PASS' or build[0]['exitCode']!=0 or build[0]['timedOut']:raise ValueError('Actual successful build receipt required')
release=root/'Rules/Release';raw=(release/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll').read_bytes()
runtime={n:n.encode() in raw for n in ('CombatHealth','HealthObservation','HealthObservationKind','TotalDamageTaken','ForestBossBrain','AdventureFlow','TitleMenu','Onboarding')}
editor={n:n.encode() in raw for n in ('S2R1Fight','S2R1Observation','S2R1Recovery','S2R1BoundaryRules','Stage2Rules','Stage2Builds','WGNormalAICheck','SetNextSeedForValidation')}
files=[]
for f in sorted((source/'Assets/CombatPrototype').rglob('*.cs')):
 if 'Editor' in f.relative_to(source).parts:continue
 rel=f.relative_to(source);other=root/'Project'/rel;files.append(dict(path=rel.as_posix(),sourceSha256=sha(f),inputSha256=sha(other),equal=f.read_bytes()==other.read_bytes()))
dependencies=[]
for name in ('Packages/manifest.json','Packages/packages-lock.json','ProjectSettings/ProjectVersion.txt'):
 f=source/name;other=root/'Project'/name;dependencies.append(dict(path=name,sourceSha256=sha(f),inputSha256=sha(other),equal=f.read_bytes()==other.read_bytes()))
protected=[]
for item in read(Path(__file__).with_name('START_BASELINE.json'))['protected']:
 f=source/item['path'];other=root/'Project'/item['path'];protected.append(dict(**item,currentSha256=sha(f),isolatedSha256=sha(other),unchanged=sha(f)==item['sha256'],isolatedRawEqual=f.read_bytes()==other.read_bytes()))
diagnostics=[];warnings=[]
for f in sorted((root/'Rules').glob('*.log')):
 lines=f.read_text(encoding='utf-8-sig',errors='replace').splitlines()
 for i,line in enumerate(lines):
  context='\n'.join(lines[max(0,i-6):i+20])
  if re.match(r'^[\w.]*Exception:',line):
   kind='Editor.Search UNRESOLVED' if 'UnityEditor.Search.' in context else 'EXPECTED S2R1 observer fault' if 'S2R1_EXPECTED_OBSERVER_FAULT' in context else 'EXPECTED injected B07 save fault' if 'B07_EXPECTED_COMMIT_FAIL' in context else 'UNCLASSIFIED'
   diagnostics.append(dict(log=f.relative_to(root).as_posix(),line=i+1,error=line,classification=kind,context=context))
  if f.name=='WanxiangBuild.ValidateBuild.log' and re.search(r'warning|JobTempAlloc|remaining Allocations',line,re.I):warnings.append(dict(line=i+1,text=line))
summary=(release/'BuildSummary.txt').read_text(encoding='utf-8-sig');metadata=all(runtime.values()) and not any(editor.values())
result=dict(status='PASS' if metadata and all(x['equal'] for x in files+dependencies) and all(x['unchanged'] for x in protected) else 'FAIL',scope='Source/input/protected-byte and shipping metadata audit only. Not native gameplay, clean shutdown, performance or complete engine-error classification.',releaseMetadata=dict(runtime=runtime,excludedNamesPresent=editor),buildStep=build[0],buildSummary=summary,artifacts=[dict(path=f.relative_to(root).as_posix(),sha256=sha(f),bytes=f.stat().st_size) for f in (release/'WanxiangGuitu.exe',release/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll')],productInputs=files,dependencyInputs=dependencies,protected=protected,diagnostics=diagnostics,buildWarningMarkerLines=warnings,allSteps=dict(PASS=sum(r['status']=='PASS' for r in steps),FAIL=sum(r['status']=='FAIL' for r in steps),NOT_RUN=sum(r['status']=='NOT_RUN' for r in steps)),notes=['The earlier All-specific auditor rejection is retained, not converted to PASS.','JobTempAlloc diagnostics have no verified causal stack; UNRESOLVED, not a clean-close claim.','88 BuildReport warnings and marker-line counts have different scopes. Full log is retained.'])
a.output.mkdir(parents=True);(a.output/'release-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(status=result['status'],productInputs=len(files),runtimeMetadata=metadata,exceptions=len(diagnostics),unclassified=sum(x['classification']=='UNCLASSIFIED' for x in diagnostics))));raise SystemExit(0 if result['status']=='PASS' else 1)
