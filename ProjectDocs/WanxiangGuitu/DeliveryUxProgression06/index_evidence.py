import pathlib,json,hashlib,datetime
D=pathlib.Path(__file__).resolve().parent;R=D.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for x in json.loads((D/'SETTINGS_GATE/SETTINGS_DRIFT_6FILES.json').read_text()):
    p=R/x['path'];baseline=D/'SETTINGS_GATE/BASELINE'/x['path']
    assert p.read_bytes()==baseline.read_bytes()
    rows.append({'path':x['path'],'beforeRecoverySize':x['currentSize'],'beforeRecoverySha256':x['currentSha256'],
                 'baselineSize':baseline.stat().st_size,'baselineSha256':sha(baseline),'restoredSize':p.stat().st_size,
                 'restoredSha256':sha(p),'exactBytesEqual':True})
recovery=D/'RECOVERY_20261124/RESTORATION_POSTVERIFICATION.json'
if recovery.exists():
    previous=json.loads(recovery.read_text())
    assert previous['status']=='PASS' and previous['rows']==rows,'Archived recovery verification drift'
else:recovery.write_text(json.dumps({'status':'PASS','verifiedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'statement':'Unity did modify these six files; original exact bytes were restored under owner authorization. The earlier receipt rows and NOT_APPLIED proposedAction are the archived pre-recovery input, not the current state.',
    'rows':rows},indent=2))
screens=[]
for name,caption in [('ui-22765.png','uGUI 遗迹永久回执/五项与领取状态'),('ui-65887.png','IMGUI 同一遗迹回执页面'),('ui-68710.png','IMGUI 最近目标名称快照'),('ui-71100.png','IMGUI 复访方向')]:
    p=D/'EVIDENCE/UX06-UI-REAL-A03-20261124/probe'/name
    assert p.exists();screens.append({'path':p.relative_to(D).as_posix(),'caption':caption,'bytes':p.stat().st_size,'sha256':sha(p)})
(D/'SCREENSHOTS.json').write_text(json.dumps(screens,ensure_ascii=False,indent=2),encoding='utf-8')
entries=[]
index=D/'EVIDENCE/INDEX.json'
for p in sorted(D.rglob('*')):
    if not p.is_file() or p==index or '__pycache__' in p.parts:continue
    entries.append({'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
out={'batch':'UX06','conclusion':'CONDITIONAL_PASS','generatedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'note':'Current batch index; prior gate index preserved as INDEX_AT_SETTINGS_GATE.json. Raw failed runs/builds unchanged. Index self-excluded; external build artifacts bound through BUILD_IDENTITY.tsv and RESULT.json.',
     'fileCount':len(entries),'totalBytes':sum(x['bytes'] for x in entries),'files':entries}
index.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
for x in entries:
    p=D/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],x['path']
print(json.dumps({'status':'PASS','indexedFiles':len(entries),'totalBytes':out['totalBytes'],'indexSha256':sha(index)}))
