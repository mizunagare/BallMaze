"""Publish owned lab evidence, never vendor code/package or build binaries.
Original files stay untouched. Redaction is applied only to published copies.
"""
from pathlib import Path
import json, hashlib, gzip, re, shutil
ROOT=Path('I:/WGCombat/MAPTOOLS-1104-A')
DOC=Path(__file__).resolve().parents[1]
OUT=DOC/'Evidence'/'Validation'
OUT.mkdir(parents=True,exist_ok=True)
manifest=[]
def publish(src,rel):
    raw=src.read_bytes();data=raw;redacted=False;dest=OUT/rel
    if src.suffix.lower() not in ['.png']:
        text=raw.decode('utf-8-sig',errors='strict')
        clean=re.sub(r'(access token:\s*)"[^"]*"',r'\1"[REDACTED]"',text,flags=re.I)
        clean=re.sub(r'LicenseClient-[A-Za-z0-9_.-]+','LicenseClient-[REDACTED]',clean)
        clean=re.sub(r'(-accessToken\s+)[^\s"\\]+',r'\1[REDACTED]',clean,flags=re.I)
        redacted=clean!=text;data=clean.encode('utf-8')
    if src.suffix.lower() in ['.log','.txt'] and src.stat().st_size>50000:
        dest=dest.with_name(dest.name+'.gz');data=gzip.compress(data,mtime=0)
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    manifest.append(dict(source=str(src),published=str(dest.relative_to(OUT)),sourceSHA256=hashlib.sha256(raw).hexdigest(),publishedSHA256=hashlib.sha256(data).hexdigest(),redacted=redacted))
for run in ['Import1','Generate1','Generate2','Generate3','Generate4','EditorPlay1','Build1','Build2','Player1','Player2']:
    for src in sorted((ROOT/run).glob('*')):
        if src.is_file() and src.suffix.lower() in ['.json','.log','.csv','.png','.txt','.sha256','.stdout','.stderr']:
            publish(src,Path(run)/src.name)
for name in ['protected-validation-before.json','protected-validation-after.json','external-change-since-acquisition.json','performance-summary.json']:
    publish(ROOT/name,Path(name))
publish(ROOT/'Inputs/package-provenance.json',Path('package-provenance.json'))
# Owned scenes/prefab/materials only; no MapMagic source, demo art or plugin package.
lab=ROOT/'ValidationProject/Assets/LabGeneratedV2'
for src in sorted(lab.iterdir()):
    if src.is_file():
        dest=DOC/'LabInputs/Assets/LabGeneratedV2'/src.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
for rel in ['Assets/MapLabRuntime.cs.meta','Assets/Editor/MapLabEditor.cs.meta','Packages/manifest.json','Packages/packages-lock.json','ProjectSettings/ProjectVersion.txt']:
    src=ROOT/'ValidationProject'/rel;dest=DOC/'LabInputs'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('published',len(manifest),'evidence artifacts; no vendor package/code')
