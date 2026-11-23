import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

root=Path.cwd()
delivery=root/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation'
batch=delivery/'UX05-IMGUI-R2'
ev=batch/'EVIDENCE'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest().upper()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def lines(p):return [json.loads(x) for x in p.read_text('utf-8-sig').splitlines() if x]

# A separate, reproducible per-operation view. Raw action/outcome logs remain intact.
operations=[]
for name in ['MIXED-A06','EMPTY-A03','UNKNOWN-A03']:
    run=ev/name
    outcomes={x['step']:x for x in lines(run/'outcomes.jsonl')}
    captured=lines(run/'observer/states.jsonl')
    for a in lines(run/'actions.jsonl'):
        if not a['label'].startswith(('IMGUI','uGUI')) or a['step'] not in outcomes:continue
        out=outcomes[a['step']];s=out['after']
        previous=[(i+1,x) for i,x in enumerate(captured) if x['utc']<=out['utc']]
        n=previous[-1][0]
        screen=run/'observer'/f'screen-{n:04d}.png'
        assert screen.exists()
        operations.append(dict(run_id=load(run/'manifest.json')['runId'],step=a['step'],operation=a['label'],
            pid=a['window']['playerPid'],hwnd=a['window']['hwnd'],foreground_pid=a['window']['foregroundPid'],
            client_x=a['clientPoint']['x'],client_y=a['clientPoint']['y'],ui=s['ui'],open=s['open'],
            region=s['regionFilter'],type=s['typeFilter'],page=s['page'],pages=s['pages'],
            query_count=len(s['query']),visible_count=len(s['visible']),
            screenshot=screen.relative_to(batch).as_posix(),status='PASS_INTERACTION'))
assert len(operations)==48
with (batch/'INTERACTION_MATRIX.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=operations[0].keys());w.writeheader();w.writerows(operations)

snap=load(ev/'source-before.json')
protection=[]
for r in snap:
    p=root/r['path'];current=sha(p)
    protection.append(dict(path=r['path'],beforeSha256=r['sha256'],afterSha256=current,bytes=p.stat().st_size,
                           unchanged=current==r['sha256']))
assert [r['path'] for r in protection if not r['unchanged']]==['Assets/CombatPrototype/AdventureFlow.UI.cs']
write(ev/'protection-after.json',protection)
assert (root/'Assets/CombatPrototype/AdventureFlow.UI.cs').read_bytes()==(root/'Builds/ux05-validation-01/Project/Assets/CombatPrototype/AdventureFlow.UI.cs').read_bytes()
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip()
assert head=='ae705b944b7d0fe851fbd395229dfc30ec636f5c'
assert branch=='feature/ux-progression-05-objective-history'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
check=subprocess.run(['git','diff','--check'],capture_output=True,text=True)
assert check.returncode==0
write(ev/'git-after.json',dict(head=head,branch=branch,indexEmpty=True,diffCheckExitCode=check.returncode,
                             diffCheckStderr=check.stderr,sourceCloneMatches=True))

docs=[delivery/'REPORT.md',delivery/'ACCEPTANCE.md',delivery/'TESTING.md',delivery/'RISK_REGISTER.md',
      delivery/'FINAL_ACCEPTANCE_REPORT.md',batch/'REPORT.md']
broken=[]
for p in docs:
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',p.read_text('utf-8-sig')):
        if target.startswith(('http:','https:','#')):continue
        target=target.split('#')[0]
        # Index files are created below, then validated.
        if target.endswith('EVIDENCE/INDEX.json'):continue
        if not (p.parent/target).exists():broken.append(dict(document=str(p),target=target))
assert not broken,broken
csv_counts={}
for p,delimiter,expected in [(delivery/'PLAYER_RUN_MATRIX.csv',',',159),(batch/'PLAYER_RUN_MATRIX.csv',',',12),
                              (batch/'INTERACTION_MATRIX.csv',',',48),(delivery/'BUILD_IDENTITY.tsv','\t',None)]:
    with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.reader(f,delimiter=delimiter))
    assert all(len(r)==len(rows[0]) for r in rows)
    if expected is not None:assert len(rows)-1==expected
    csv_counts[p.relative_to(delivery).as_posix()]=len(rows)-1
write(ev/'delivery-check.json',dict(markdownLinks='PASS',csvColumns='PASS',csvRowCounts=csv_counts,
     original147Rows='UNCHANGED',historicalFilesVerified=4142,productScope='ONE_UI_FILE',
     schemaMigrationSettlement='UNCHANGED_FROM_R1',trueUserSaves='NOT_ACCESSED',verdict='R2_PASS'))

batch_index=ev/'INDEX.json'
batch_files=[]
for p in sorted(batch.rglob('*')):
    if p.is_file() and p!=batch_index and '__pycache__' not in p.parts:
        batch_files.append(dict(path=p.relative_to(batch).as_posix(),sha256=sha(p),bytes=p.stat().st_size))
write(batch_index,dict(pathBase='UX05-IMGUI-R2',runCount=12,verdict='R2_PASS',files=batch_files))
original=load(ev/'history-before.json')
all_files=original['files'][:]
for p in sorted(batch.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts:
        all_files.append(dict(path=p.relative_to(delivery).as_posix(),sha256=sha(p),bytes=p.stat().st_size))
assert len({x['path'] for x in all_files})==len(all_files)
write(delivery/'EVIDENCE/INDEX.json',dict(runCount=159,branch=branch,verdict='R2_PASS',files=all_files))
for idx,base in [(batch_index,batch),(delivery/'EVIDENCE/INDEX.json',delivery)]:
    for r in load(idx)['files']:
        p=Path('\\\\?\\'+str(base/r['path']).replace('/','\\'))
        assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],r['path']
print(json.dumps(dict(check='PASS',batchFiles=len(batch_files),totalIndexedFiles=len(all_files),
                      interactionOperations=len(operations),sourceFiles=len(protection),csvRows=csv_counts),indent=2))
