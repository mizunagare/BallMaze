import pathlib,json,hashlib,subprocess,csv
R=pathlib.Path('I:/unity/WanxiangGuitu-UX06');O=pathlib.Path('I:/unity/WanxiangGuitu')
D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression06'
B=json.loads((D/'BASELINE.json').read_text(encoding='utf-8'))
def git(root,*args):return subprocess.check_output(['git','--no-optional-locks','-c','core.longpaths=true',*args],cwd=root).decode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for path,value in B['product'].items():
    if not path.endswith('.cs'):continue
    current=sha(R/path);expected=path in ['Assets/CombatPrototype/AdventureFlow.UI.cs','Assets/CombatPrototype/ObjectiveCatalog.cs']
    rows.append([path,value['sha256'],current,'AUTHORIZED_UI_CHANGE' if expected else 'UNCHANGED'])
    if not expected:assert current==value['sha256'],path
for path,value in B['settingsPackages'].items():
    current=sha(R/path);assert current==value['sha256'],path
    rows.append([path,value['sha256'],current,'UNCHANGED_AFTER_AUTHORIZED_RECOVERY' if path.startswith('ProjectSettings/') else 'UNCHANGED'])
for value in json.loads((D/'SETTINGS_GATE/SETTINGS_DRIFT_6FILES.json').read_text()):
    assert sha(R/value['path'])==value['baselineSha256']
    rows.append([value['path'],value['baselineSha256'],sha(R/value['path']),'RESTORED_UNDER_OWNER_AUTHORIZATION'])
for receipt in ['REUSED_UI_FIXTURE_RECEIPT.json','REUSED_UNKNOWN_FIXTURE_RECEIPT.json']:
    rec=json.loads((D/receipt).read_text());source=pathlib.Path(rec['source'])
    assert all(sha(source/x['path'])==x['sha256'] for x in rec['files'])
old_index=pathlib.Path(git(O,'rev-parse','--git-path','index').strip())
status={'originalHead':git(O,'rev-parse','HEAD').strip(),'originalBranch':git(O,'branch','--show-current').strip(),
        'originalIndexUnchanged':sha(old_index)==B['originalIndexSha256'],
        'originalStatusUnchanged':git(O,'status','--porcelain=v1','--untracked-files=all')==B['originalStatus'],
        'originalAgENTSUnchanged':sha(O/'AGENTS.md')==B['originalAgENTS'],
        'ux06Head':git(R,'rev-parse','HEAD').strip(),'ux06Branch':git(R,'branch','--show-current').strip(),
        'staged':git(R,'diff','--cached','--name-only').splitlines(),
        'trackedChanges':git(R,'diff','--name-only').splitlines(),'realSaves':'not accessed; explicit isolated roots audited per Run'}
assert status['originalIndexUnchanged'] and status['originalStatusUnchanged'] and status['originalAgENTSUnchanged']
assert not status['staged'] and status['ux06Head']=='1c3fb90bf5902c147fda35252dc59e3b3a5f8872'
assert status['trackedChanges']==['Assets/CombatPrototype/AdventureFlow.UI.cs','Assets/CombatPrototype/ObjectiveCatalog.cs']
(D/'FINAL_PROTECTION.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
with (D/'PROTECTION_SHA256.tsv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.writer(f,delimiter='\t');writer.writerow(['Path','BaselineSha256','CurrentSha256','Status']);writer.writerows(rows)
print(json.dumps({'status':'PASS','protectedRows':len(rows),**status},ensure_ascii=False))
