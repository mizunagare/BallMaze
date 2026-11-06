import hashlib
import json
from pathlib import Path
import re
import sys

repo, root, original, protected = map(Path,sys.argv[1:])
out=root/'Audit'
out.mkdir(exist_ok=True)
def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()
def files(directory):
    return {p.relative_to(directory).as_posix():sha(p) for p in directory.rglob('*') if p.is_file()}
def put(name,obj):
    (out/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding='utf-8')
c1=load(original/'Audit/build-file-hashes.json')
for arm in 'AB':
    label=f'Project{arm}-Build'
    assert files(original/label/'Release')==c1[label],label
manifest=load(protected)
changed=[x['path'] for x in manifest if not Path(x['path']).is_file() or sha(Path(x['path']))!=x['sha256']]
assert not changed,changed
release=root/'PureBuild2/Release'
pure=files(release)
observed=files(root/'ObservedFinal/Release')
delta=sorted(k for k in pure.keys()|observed.keys() if pure.get(k)!=observed.get(k))
assert set(delta)=={'WanxiangGuitu_Data/RuntimeInitializeOnLoads.json','WanxiangGuitu_Data/ScriptingAssemblies.json',
                    'WanxiangGuitu_Data/Managed/CavernValidationDriver.dll'},delta
assert not any('CavernValidationDriver' in k for k in pure)
for name in ('RuntimeInitializeOnLoads.json','ScriptingAssemblies.json'):
    assert 'CavernValidation' not in (release/'WanxiangGuitu_Data'/name).read_text()
exe=release/'WanxiangGuitu.exe'
config=load(Path(str(exe)+'.bee.json'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
keys=('EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting')
services={k:config['Services'][k] for k in keys}
assert config['Development'] is False and all(v is False for v in services.values())
assert load(root/'PureBuild2/editor-actual-exit.json')['exitCode']==0
boot=load(root/'PureBootFinal/pure-runtime.json')
assert boot['titleReady'] and boot['titleOnly'] and boot['exitCode']==0 and boot['unchangedSyntheticFiles']
put('release-audit.json',dict(development=config['Development'],services=services,pureDriverAbsent=True,pureBoot=boot,
   protectedFiles=len(manifest),changed=changed,oldPackageFileCounts={k:len(v) for k,v in c1.items()},
   fileCount=len(pure),exeSHA256=sha(exe),managedSHA256=sha(release/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll'),
   observationDifferences={k:observed[k] for k in delta}))
put('release-manifest.json',pure)
inputs={}; build_inputs={}
for k in ('Assets','Packages','ProjectSettings'):
    inputs.update({k+'/'+p:s for p,s in files(repo/k).items()})
    build_inputs.update({k+'/'+p:s for p,s in files(root/'Project'/k).items()})
mismatches={k:dict(worktree=inputs.get(k),isolated=build_inputs.get(k)) for k in sorted(inputs.keys()|build_inputs.keys())
            if inputs.get(k)!=build_inputs.get(k)}
put('build-input-differences.json',mismatches)
put('product-inputs.json',inputs)
log=(root/'PureBuild2/Unity.log').read_text('utf-8-sig',errors='replace')
warnings=[x for x in log.splitlines() if re.search(r'\bwarning\b',x,re.I)]
(out/'warnings.txt').write_text('\n'.join(warnings)+'\n',encoding='utf-8')
lit=[]
for chunk in re.split(r'(?=^Compiling shader ")',log,flags=re.M):
    if chunk.startswith('Compiling shader "Universal Render Pipeline/Lit"'):
        lit.extend(x for x in chunk.splitlines() if 'Pass ForwardLit' in x or 'After scriptable stripping' in x or x.startswith('Compiling shader'))
(out/'lit-build.txt').write_text('\n'.join(lit)+'\n',encoding='utf-8')
print('Pure files',len(pure),'protected',len(manifest),'input differences',len(mismatches),'Lit evidence lines',len(lit))
