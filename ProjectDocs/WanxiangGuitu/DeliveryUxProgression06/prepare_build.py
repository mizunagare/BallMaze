"""Freeze a new input version and copy it into the idle disposable build project."""
import pathlib,json,hashlib,shutil,sys,zipfile,subprocess
DEV=pathlib.Path('I:/unity/WanxiangGuitu-UX06')
DELIVERY=DEV/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression06'
PROJECT=pathlib.Path('I:/UX06_BUILD_20261124/Project')
record=sys.argv[1]
out=DELIVERY/record
out.mkdir(exist_ok=False)
rows=json.loads((DELIVERY/'SETTINGS_GATE/SETTINGS_DRIFT_6FILES.json').read_text(encoding='utf-8'))
for row in rows:
    assert hashlib.sha256((DEV/row['path']).read_bytes()).hexdigest()==row['baselineSha256']
manifest=[]
with zipfile.ZipFile(out/'FROZEN_SOURCES.zip','x',zipfile.ZIP_DEFLATED) as archive:
    for folder in ['Assets','Packages','ProjectSettings']:
        for source in sorted((DEV/folder).rglob('*')):
            if not source.is_file():continue
            relative=source.relative_to(DEV)
            content=source.read_bytes()
            entry={'path':relative.as_posix(),'size':len(content),'sha256':hashlib.sha256(content).hexdigest()}
            manifest.append(entry)
            if source.suffix=='.cs' or folder in ['Packages','ProjectSettings']:
                archive.writestr(relative.as_posix(),content)
            target=PROJECT/relative
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
            assert target.read_bytes()==content
(out/'FROZEN_INPUT_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'record':record,'files':len(manifest),'copiedAndByteVerified':True}),flush=True)
