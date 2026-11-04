from pathlib import Path
import json,hashlib,gzip,re,shutil,csv,statistics
ROOT=Path('I:/WGCombat/MAPTOOLS02-A')
DOC=Path(__file__).resolve().parents[1]
OUT=DOC/'Evidence';OUT.mkdir(parents=True,exist_ok=True)
manifest=[]
def emit(src,rel):
    raw=src.read_bytes();data=raw;cleaned=False;dest=OUT/rel
    if src.suffix.lower()!='.png':
        text=raw.decode('utf-8-sig',errors='strict')
        clean=re.sub(r'(access token:\s*)"[^"]*"',r'\1"[REDACTED]"',text,flags=re.I)
        clean=re.sub(r'LicenseClient-[A-Za-z0-9_.-]+','LicenseClient-[REDACTED]',clean)
        cleaned=clean!=text;data=clean.encode('utf-8')
    if src.suffix.lower() in ['.log','.csv','.jsonl'] and len(data)>50000:
        dest=dest.with_name(dest.name+'.gz');data=gzip.compress(data,mtime=0)
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    manifest.append(dict(source=str(src),published=str(dest.relative_to(OUT)),sourceSHA256=hashlib.sha256(raw).hexdigest(),publishedSHA256=hashlib.sha256(data).hexdigest(),redacted=cleaned))
for run in ['Generate1','Generate2','EditorPlay1','EditorPlay2','EditorPlay3','Build1','Version1','Build2','PlayerWrite1','PlayerRead1','PlayerWrite2','PlayerRead2','Refine1','EditorPlay4','EditorPlay5','EditorPlay6','Build3','PlayerWrite3','PlayerRead3']:
    for src in sorted((ROOT/run).rglob('*')):
        if not src.is_file() or 'Player' in src.relative_to(ROOT/run).parts:continue
        if src.suffix.lower() in ['.json','.jsonl','.log','.csv','.png','.txt','.cs','.stdout','.stderr']:emit(src,Path(run)/src.relative_to(ROOT/run))
for name in ['owner.json','protected-before.json','protected-after.json','package.json','package-audit.json','source-protection.json','performance-summary.json','generation-summary.json','asset-manifest.json','driver-consistency.json']:
    src=ROOT/name
    if src.exists():emit(src,Path(name))
# Owned output only. Never include MapMagic package/source/Demo art or Player binaries.
lab=ROOT/'Project/Assets/MT02GeneratedV2'
for src in sorted(lab.iterdir()):
    if src.is_file():
        dst=DOC/'LabInputs/Assets/MT02GeneratedV2'/src.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
for rel in ['Assets/MT02WorldState.cs.meta','Assets/MT02Runtime.cs.meta','Assets/Editor/MT02Editor.cs.meta','Packages/manifest.json','Packages/packages-lock.json','ProjectSettings/ProjectVersion.txt']:
    dst=DOC/'LabInputs'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'Project'/rel,dst)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('published',len(manifest),'raw artifacts; vendor package/code/binaries excluded')
