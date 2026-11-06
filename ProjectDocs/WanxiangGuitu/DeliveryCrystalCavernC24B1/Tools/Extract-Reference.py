import tarfile,pathlib,re,shutil,json,hashlib
root=pathlib.Path('I:/WGCombat/C24B1-1107-A'); dest=root/'ReferenceProject2'
if dest.exists():raise SystemExit('Fresh destination required')
dest.mkdir()
with tarfile.open(root/'reference-product.tar',encoding='utf-8') as archive:
    archive.extractall(dest,filter='data')
objects=pathlib.Path('H:/unity/WanxiangGuitu/.git/lfs/objects');manifest=[]
for f in sorted(dest.rglob('*')):
    if not f.is_file():continue
    if f.stat().st_size<1024:
        data=f.read_bytes()
        if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
            oid=re.search(rb'oid sha256:(\w+)',data)[1].decode();source=objects/oid[:2]/oid[2:4]/oid
            if not source.exists():raise RuntimeError(f'Missing LFS {f}: {oid}')
            shutil.copyfile(source,f)
    manifest.append(dict(path=f.relative_to(dest).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
(root/'reference-inputs.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(len(manifest))
