"""Hash product sources, isolated build inputs and executed test drivers; no save reads."""
import argparse, hashlib, json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--project',type=Path,required=True)
p.add_argument('--run',type=Path,required=True)
p.add_argument('--target',type=Path,required=True)
a=p.parse_args()
a.target.mkdir(parents=True,exist_ok=True)
def digest(path, normalize=False):
    b=path.read_bytes()
    return hashlib.sha256(b.replace(b'\r\n',b'\n') if normalize else b).hexdigest()
sources=[]
for path in sorted((a.project/'Assets/CombatPrototype').rglob('*.cs')):
    relative=path.relative_to(a.project)
    copy=a.run/'Project'/relative
    sources.append(dict(path=relative.as_posix(),sourceRawSha256=digest(path),
                        normalizedSha256=digest(path,True),copySha256=digest(copy,True),
                        equal=digest(path,True)==digest(copy,True)))
if not sources or not all(item['equal'] for item in sources):
    raise ValueError('Product source and isolated input mismatch')
inputs=[]
for folder in ('Assets','Packages','ProjectSettings'):
    for path in sorted((a.project/folder).rglob('*')):
        if not path.is_file(): continue
        relative=path.relative_to(a.project)
        copy=a.run/'Project'/relative
        inputs.append(dict(path=relative.as_posix(),sourceSha256=digest(path),
                           copySha256=digest(copy) if copy.is_file() else None,
                           equal=copy.is_file() and digest(path)==digest(copy)))
drivers=[]
driverPaths=list(a.run.glob('Normal-*/ExecutedDrivers-*/*'))+list(a.run.glob('Stage2Matrix/*/ExecutedDrivers-*/*'))
for path in sorted(driverPaths):
    if path.is_file():
        drivers.append(dict(path=path.relative_to(a.run).as_posix(),sha256=digest(path),
                            normalizedSha256=digest(path,True)))
result=dict(policy='Product .cs compared after CRLF normalization. Build inputs compared as raw bytes. User ProjectSettings copied for validation but not committed. Test drivers separately hashed; no saves read.',
            sources=sources,buildInputs=inputs,executedDrivers=drivers)
(a.target/'source-build-provenance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(productSources=len(sources),productEqual=all(x['equal'] for x in sources),
                      buildInputs=len(inputs),inputDifferences=[x['path'] for x in inputs if not x['equal']],
                      executedDrivers=len(drivers))))
