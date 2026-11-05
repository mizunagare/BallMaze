import hashlib
import json
from pathlib import Path
import sys

root, original, raw_r5, published_r5, protected = map(Path, sys.argv[1:])
def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def digest(path):
    with path.open('rb') as file:
        return hashlib.file_digest(file, 'sha256').hexdigest()

frozen = load(original/'Audit/build-file-hashes.json')
expected = {
    'WanxiangGuitu_Data/Managed/C1R6RenderProbe.dll',
    'WanxiangGuitu_Data/RuntimeInitializeOnLoads.json',
    'WanxiangGuitu_Data/ScriptingAssemblies.json',
}
releases = {}
for arm in 'AB':
    build = f'Project{arm}-Build'
    baseline = frozen[build]
    cases = {'original':original/build/'Release',
             'pureBootCopy':root/f'Pure{arm}/Release',
             'render':root/f'Render{arm}/Release',
             'diagnostic':root/f'Diagnostic{arm}/Release'}
    compare={}
    for label, path in cases.items():
        actual = {p.relative_to(path).as_posix():digest(p) for p in path.rglob('*') if p.is_file()}
        delta = sorted(k for k in actual.keys()|baseline.keys() if actual.get(k)!=baseline.get(k))
        assert set(delta)==(set() if label in ('original','pureBootCopy') else expected), (label,delta)
        compare[label] = dict(files=len(actual), difference=delta, differenceHashes={k:actual[k] for k in delta})
    config=load(cases['original']/'WanxiangGuitu.exe.bee.json')['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
    service={k:config['Services'][k] for k in ('EnableUnityConnect','EnableCrashReporting','EnableInsights',
                                                 'EnableAnalytics','EnablePerformanceReporting')}
    assert config['Development'] is False and all(v is False for v in service.values())
    releases[arm]=dict(**compare, bee=service, development=config['Development'])
history = load(published_r5/'manifest.json')
broken = [e['path'] for e in history if digest(raw_r5/e['sourceRelative'])!=e['sourceSHA256'] or
          digest(published_r5/e['path'])!=e['publishedSHA256']]
files=load(protected)
user_broken=[x['path'] for x in files if not Path(x['path']).is_file() or digest(Path(x['path']))!=x['sha256']]
images=sum(e['sourceRelative'].startswith('Frames-') and e['path'].endswith('.png') for e in history)
assert images==42
(root/'protection.json').write_text(json.dumps(dict(releases=releases,r5Entries=len(history),r5FramePNGs=images,
    r5Mismatches=broken,userFiles=len(files),userMismatches=user_broken),indent=2),encoding='utf-8')
assert not broken and not user_broken
print('A/B original hashes match, 42 historical frames and',len(files),'protected paths unchanged.')
