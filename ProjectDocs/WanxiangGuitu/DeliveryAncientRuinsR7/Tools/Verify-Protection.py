import hashlib
import json
from pathlib import Path
import sys

run, original = map(Path, sys.argv[1:3])
historical_args = sys.argv[3:]
assert len(historical_args)==7
def load(path):
    return json.loads(path.read_text('utf-8-sig'))
def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

baseline = load(original/'Audit/build-file-hashes.json')
allowed = {'WanxiangGuitu_Data/Managed/C1R7RenderProbe.dll',
           'WanxiangGuitu_Data/RuntimeInitializeOnLoads.json',
           'WanxiangGuitu_Data/ScriptingAssemblies.json'}
result={}
for arm in 'AB':
    build=f'Project{arm}-Build'
    original_release=original/build/'Release'
    references=baseline[build]
    result[arm]={}
    for scope,path in (('original',original_release),('pureCopy',run/f'Pure{arm}/Release'),
                       ('observedCopy',run/f'Render{arm}/Release')):
        actual={p.relative_to(path).as_posix():digest(p) for p in path.rglob('*') if p.is_file()}
        differences=sorted(k for k in references.keys()|actual.keys() if references.get(k)!=actual.get(k))
        assert set(differences)==(allowed if scope=='observedCopy' else set()), (arm,scope,differences)
        result[arm][scope]=dict(path=str(path),files=len(actual),differences={k:actual[k] for k in differences})
    config=load(original_release/'WanxiangGuitu.exe.bee.json')['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
    services={k:config['Services'][k] for k in ('EnableUnityConnect','EnableCrashReporting','EnableInsights',
                                              'EnableAnalytics','EnablePerformanceReporting')}
    assert config['Development'] is False and all(v is False for v in services.values())
    pure=load(run/f'PureBoot{arm}-final/pure-runtime.json')
    assert pure['titleReady'] and pure['titleOnly'] and pure['actualProcessExited'] and pure['unchangedSyntheticFiles'] and pure['exitCode']==0
    result[arm].update(development=config['Development'],services=services,pureRun=pure)
history={}
for number,i in zip((4,5,6),(0,2,4)):
    raw,published=map(Path,historical_args[i:i+2])
    manifest=load(published/'manifest.json')
    mismatches=[e['path'] for e in manifest if digest(raw/e['sourceRelative'])!=e['sourceSHA256'] or
                 digest(published/e['path'])!=e['publishedSHA256']]
    assert not mismatches,(number,mismatches)
    history[f'R{number}']=dict(entries=len(manifest),mismatches=mismatches)
files=load(Path(historical_args[6]))
changed=[x['path'] for x in files if not Path(x['path']).is_file() or digest(Path(x['path']))!=x['sha256']]
assert not changed,changed
(run/'Audit'/'protection.json').write_text(json.dumps(dict(releases=result,historical=history,
     protectedUserPaths=len(files),protectedMismatches=changed),indent=2),encoding='utf-8')
print(history,'user paths',len(files),'unchanged')
