"""Copy completed isolated runs without overwriting any prior evidence.
Does not copy Player binaries, Unity project caches, or external vendor sources.
Full immutable shipping manifest is kept separately; raw packages remain local.
"""
import hashlib, json, pathlib, shutil
ROOT = pathlib.Path('I:/WGCombat/C24-1106-A')
DEST = pathlib.Path(__file__).resolve().parents[1] / 'Evidence' / 'Runs'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
manifest=[]
for directory in sorted(ROOT.iterdir()):
    if not directory.is_dir(): continue
    if not (directory/'process.json').exists() and not (directory/'pure-runtime.json').exists() and not directory.name.endswith('Audit1'): continue
    for src in sorted(directory.rglob('*')):
        if not src.is_file() or 'Release' in src.relative_to(directory).parts: continue
        rel=src.relative_to(ROOT); dst=DEST/rel; digest=sha(src)
        if dst.exists():
            if sha(dst)!=digest: raise RuntimeError(f'Existing evidence differs: {dst}')
        else:
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        manifest.append(dict(source=str(src),archive=str(rel).replace('\\','/'),bytes=src.stat().st_size,sha256=digest))
    for src in sorted((directory/'Release').glob('*.exe.*')):
        rel=pathlib.Path(directory.name)/'BuildReceipts'/src.name;dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True)
        if dst.exists() and sha(src)!=sha(dst):raise RuntimeError(str(dst))
        if not dst.exists():shutil.copy2(src,dst)
        manifest.append(dict(source=str(src),archive=rel.as_posix(),bytes=src.stat().st_size,sha256=sha(src)))
for src in sorted(ROOT.glob('player-driver-compile-*.log')):
    dst=DEST/'Compilation'/src.name;dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists() and sha(src)!=sha(dst): raise RuntimeError(str(dst))
    if not dst.exists():shutil.copy2(src,dst)
    manifest.append(dict(source=str(src),archive='Compilation/'+src.name,bytes=src.stat().st_size,sha256=sha(src)))
for src in sorted(ROOT.glob('*/Driver.executed.cs.txt')):
    rel=pathlib.Path('ExecutedDrivers')/src.parent.name/src.name;dst=DEST/rel;dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists() and sha(src)!=sha(dst): raise RuntimeError(str(dst))
    if not dst.exists():shutil.copy2(src,dst)
    manifest.append(dict(source=str(src),archive=rel.as_posix(),bytes=src.stat().st_size,sha256=sha(src)))
out=DEST.parent/'archive-origin.json'
if out.exists(): raise RuntimeError('Use a new archive manifest name; preserve original')
out.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(dict(files=len(manifest),bytes=sum(x['bytes'] for x in manifest))))
