"""Publish bounded research evidence; originals remain at ROOT. No vendor packages/source."""
from pathlib import Path
import json, hashlib, gzip, re, shutil

ROOT=Path('I:/WGCombat/MAPTOOLS03-A')
DOC=Path(__file__).resolve().parents[1]
OUT=DOC/'Evidence'
manifest=[]

def emit(src, rel):
    raw=src.read_bytes();data=raw;changes=[];dest=OUT/rel
    if src.suffix.lower()!='.png':
        text=raw.decode('utf-8-sig',errors='strict')
        clean=re.sub(r'(access token:\s*)"[^"]*"',r'\1"[REDACTED]"',text,flags=re.I)
        clean=re.sub(r'LicenseClient-[A-Za-z0-9_.-]+','LicenseClient-[REDACTED]',clean)
        if clean!=text:changes.append('licensing token/client identifier redacted')
        # Diagnostic engine heap byte dumps are not needed to identify allocation stacks.
        # Keep every warning, allocation record, stack frame and line order; originals never edited.
        pattern=r'(?m)^(?:[0-9a-fA-F]{2} ){8,}.*$'
        clean,n=re.subn(pattern,'[NATIVE HEAP HEX PAYLOAD OMITTED; original retained locally]',clean)
        if n:changes.append(f'{n} native heap hex payload lines omitted, stack frames retained')
        data=clean.encode('utf-8')
    if src.suffix.lower() in ['.log','.csv','.jsonl'] and len(data)>50000:
        dest=dest.with_name(dest.name+'.gz');data=gzip.compress(data,mtime=0)
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    manifest.append(dict(source=str(src),published=str(dest.relative_to(OUT)),sourceSHA256=hashlib.sha256(raw).hexdigest(),publishedSHA256=hashlib.sha256(data).hexdigest(),transformations=changes))

runs=['Prepare1','Prepare2','BuildEmpty1','BuildTerrain1','BuildAudit1','Audit1','BuildEmpty2','BuildTerrain2','BuildAudit2','Audit2','Memory1','Memory2','BuildAudit3','Audit3','EditorPlay1','VersionResearch']
for run in runs:
    for src in sorted((ROOT/run).rglob('*')):
        if not src.is_file() or 'Player' in src.relative_to(ROOT/run).parts:continue
        if src.suffix.lower() in ['.json','.jsonl','.log','.csv','.png','.txt','.cs','.stdout','.stderr']:emit(src,Path(run)/src.relative_to(ROOT/run))
for src in sorted(ROOT.iterdir()):
    if src.is_file() and src.suffix in ['.json','.log']:emit(src,Path(src.name))

# Only our new fixture and metadata are redistributed. Earlier fixture is already in doc02.
lab=Path('I:/WGCombat/MAPTOOLS02-A/Project')
for src in sorted((lab/'Assets/MT03Generated').iterdir()):
    if src.is_file():
        dest=DOC/'LabInputs/Assets/MT03Generated'/src.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
for rel in ['Assets/MT03Runtime.cs.meta','Assets/MT03Calibration.shader.meta','Assets/Editor/MT03Editor.cs.meta','Packages/manifest.json','Packages/packages-lock.json','ProjectSettings/ProjectVersion.txt']:
    dest=DOC/'LabInputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(lab/rel,dest)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Published',len(manifest),'artifacts; vendor package/code and Player binaries excluded.')
