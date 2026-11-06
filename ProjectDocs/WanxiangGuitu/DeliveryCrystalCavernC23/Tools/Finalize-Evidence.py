"""Read-only final audit; writes new delivery evidence, never test originals."""
import json, hashlib, subprocess, zipfile, re
from pathlib import Path

root=Path('I:/WGCombat/C23-1106-A')
repo=Path('H:/unity/WanxiangGuitu-Cavern-C23')
delivery=repo/'ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC23'
ev=delivery/'Evidence'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def write(name,data):
    p=ev/name
    if p.exists(): raise RuntimeError('Preserve existing '+str(p))
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

allruns=read(ev/'runs.json')
final={}
for layer in ('Editor','Player'):
    matrix=[json.loads(x) for x in (root/f'matrix-{layer}-Verified.jsonl').read_text(encoding='utf-8-sig').splitlines()]
    assert len(matrix)==14 and all(r['exitCode']==0 for r in matrix),layer
    names=[Path(r['output']).name for r in matrix]
    extras=['NavFailure','HazardFinal','DeathFinal']
    if layer=='Player': extras+=['ContinuousAudited','ContinuousWarehouse','RoutesAudited']
    names += [layer+n for n in extras]
    assert len(names)==len(set(names))
    selected={name:allruns[name] for name in names}
    assert all(r['semantic']=='PASS' for r in selected.values()),selected
    final[layer]={'runs':selected,'assertions':{s:sum(r[s] for r in selected.values()) for s in ('PASS','FAIL','NOT_RUN','UNRESOLVED')}}
final['pure']=read(root/'PureBoot6/pure-runtime.json')
assert final['pure']['actualProcessExited'] and final['pure']['exitCode']==0 and final['pure']['titleReady'] and final['pure']['unchangedSyntheticFiles']
final['history']={k:v for k,v in allruns.items() if v['FAIL']}
final['limitations']={'nativeInput':'NOT_RUN','humanExperience':'NOT_RUN','finalBalance':'NOT_RUN','calibratedGC':'NOT_RUN','calibratedGPU':'NOT_RUN','performanceBudget':'NOT_RUN','historicalSemanticEquivalence':'UNRESOLVED','historicalJobTempAlloc':'UNRESOLVED'}
write('final-results.json',final)

baseline=read(ev/'baseline-inputs.json')
allowed={'Assets/CombatPrototype/'+f for f in ['AdventureFlow.cs','CrystalCavernLayout.cs','CrystalCavernRegion.cs','WorldEventPoint.cs','SaveCatalog.cs','PlayerHudPresenter.cs','Editor/CrystalCavernAuthoring.cs']}
changes=[]
for item in baseline:
    p=repo/item['path']; actual=sha(p) if p.exists() else None
    if actual!=item['sha256'].upper(): changes.append({'path':item['path'],'before':item['sha256'],'after':actual})
assert {x['path'] for x in changes}==allowed,changes
users=[]
for item in read(ev/'user-files-before.json'):
    actual=sha(Path(item['path']))
    assert actual==item['sha256'].upper(),item['path']
    users.append(dict(item,after=actual,unchanged=True))
manifest=[]
for directory in ('Assets','Packages','ProjectSettings'):
    for p in sorted((repo/directory).rglob('*')):
        if p.is_file(): manifest.append({'path':p.relative_to(repo).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
write('final-inputs.json',manifest)
write('final-protection.json',{'baselineInputs':len(baseline),'changedExisting':changes,'userFiles':users,'allOtherBaselineInputsUnchanged':True,'gitDiffCheck':subprocess.run(['git','diff','--check'],cwd=repo,capture_output=True,text=True).returncode})

assets=[dict(m,assetId='C23:'+Path(m['path']).relative_to('Assets/Resources/CrystalCavernC23').as_posix(),source='Self-authored editor tooling, project-owned meshes/materials; no third-party additions',state='INTEGRATED') for m in manifest if m['path'].startswith('Assets/Resources/CrystalCavernC23/') and not m['path'].endswith('.meta')]
write('asset-catalog.json',assets)

logs=[]
archive=ev/'Logs.zip'
if archive.exists(): raise RuntimeError('Logs.zip exists')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.glob('*/*.log')):
        if p.parent.name in ('Project','EditorProject'): continue
        z.write(p,p.relative_to(root).as_posix())
        logs.append({'path':str(p),'entry':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    for p in sorted(root.glob('player-driver-compile-*.log')):
        z.write(p,p.name);logs.append({'path':str(p),'entry':p.name,'sha256':sha(p),'bytes':p.stat().st_size})
write('log-archive.json',{'archiveSHA256':sha(archive),'files':logs})
warnings=[]
for n,line in enumerate((root/'PureBuild6/Unity.log').read_text(encoding='utf-8-sig',errors='replace').splitlines(),1):
    if re.search(r'warning|JobTempAlloc',line,re.I): warnings.append({'line':n,'text':line})
write('build-warning-index.json',{'buildReportWarnings':105,'matchedLogLines':warnings,'note':'Index only; full raw log archived. Matching line count is not BuildReport warning count.'})

performance={}
for layer in ('Editor','Player'):
    folder=root/f'{layer}InnerVerified'
    samples=[x.split('\t') for x in (folder/'continuous.tsv').read_text().splitlines()[1:] if x]
    times=[float(x[1]) for x in samples]
    performance[layer]={'scene':read(folder/'scene-counts.json'),'traceDurationSeconds':times[-1]-times[0],'traceSamples':len(times),'scope':'0.1s sampled normal AI route, NOT CPU frame profiler; serialization/filesystem overhead included','GC':'NOT_RUN','GPU':'NOT_RUN','budget':'NOT_RUN'}
write('runtime-measurements.json',performance)
print(json.dumps({k:{'runs':len(v['runs']),'assertions':v['assertions']} for k,v in final.items() if k in ('Editor','Player')},ensure_ascii=False))
