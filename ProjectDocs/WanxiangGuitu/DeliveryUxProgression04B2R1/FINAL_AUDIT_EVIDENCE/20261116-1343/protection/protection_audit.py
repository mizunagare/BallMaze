"""FINAL independent read-only file audit. Writes only new audit attachments."""
from pathlib import Path
import csv,json,hashlib,subprocess,difflib
ROOT=Path.cwd(); AUD=ROOT/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343'; OUT=AUD/'protection'; OUT.mkdir(parents=True,exist_ok=True)
DEL=ROOT/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1'
SNAP=Path('I:/unity/WanxiangGuitu-UX04B2R1-snapshot-20261116-1108')
def xp(p): return Path(chr(92)*2+'?'+chr(92)+str(p.absolute()))
def sha(p):
    with xp(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def info(p):
    return {'sha256':sha(p),'bytes':xp(p).stat().st_size} if xp(p).is_file() else {'sha256':'MISSING','bytes':None}
def emit(p,obj):
    if p.exists(): raise RuntimeError('Refuse overwrite '+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
# Capture every pre-existing product/document/evidence file, excluding this NEW audit namespace.
entry=[]
for folder in ['Assets','Packages','ProjectSettings','UserSettings','ProjectDocs','Evidence']:
    for p in sorted((ROOT/folder).rglob('*')):
        if not p.is_file() or AUD in p.parents or p==DEL/'FINAL_AUDIT.md':continue
        entry.append({'path':p.relative_to(ROOT).as_posix(),**info(p)})
emit(OUT/'READONLY_ENTRY_SHA256.json',entry)
base=json.loads((SNAP/'PRECHANGE_SHA256.json').read_text(encoding='utf-8'))
tsv=list(csv.DictReader((DEL/'PROTECTION_SHA256.tsv').open(encoding='utf-8-sig'),delimiter='	'))
reported={x['file']:x for x in tsv}; allowed={'Assets/CombatPrototype/AdventureLoadout.cs','Assets/CombatPrototype/CatInventoryPresenter.cs','Assets/CombatPrototype/ContainerInventoryView.cs','ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/IntDriverR1.cs','ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/run_r1_player.py'}
rows=[]; faults=[]; changed=[]
for b in base['files']:
    rel=b['path']; current=info(ROOT/rel); saved=info(SNAP/'workspace'/rel); r=reported.get(rel,{})
    same=current['sha256']==b['sha256']; auth=rel in allowed
    errors=[]
    if saved['sha256']!=b['sha256'] or saved['bytes']!=b['bytes']:errors.append('snapshot_input_mismatch')
    if r.get('prechange_sha256')!=b['sha256']:errors.append('reported_baseline_mismatch')
    if r.get('current_sha256')!=current['sha256']:errors.append('reported_current_mismatch')
    if current['sha256']=='MISSING':errors.append('missing_current')
    if same and current['bytes']!=b['bytes']:errors.append('same_hash_size_mismatch')
    if not same:
        changed.append(rel)
        if not auth:errors.append('unauthorized_change')
    expected='UNCHANGED' if same else 'AUTHORIZED_R1_EDIT'
    if r.get('status')!=expected:errors.append('reported_status_mismatch')
    row={'path':rel,'baseline_sha256':b['sha256'],'baseline_bytes':b['bytes'],'snapshot_sha256':saved['sha256'],'snapshot_bytes':saved['bytes'],'current_sha256':current['sha256'],'current_bytes':current['bytes'],'authorized':auth,'same':same,'result':'PASS' if not errors else 'FAIL','errors':','.join(errors)}
    rows.append(row)
    if errors:faults.append(row)
with (OUT/'PROTECTION_RECALCULATED.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0],delimiter='	');w.writeheader();w.writerows(rows)
# Three independent temporal points: original B2, complete 11:07 R1 handover, and current.
old=json.loads((DEL/'_baseline_snapshot/snapshot.json').read_text(encoding='utf-8')); temporal=[]
for b in old['files']:
    rel=b['path']; saved=info(ROOT/b['backup']); before=info(SNAP/'workspace'/rel); now=info(ROOT/rel)
    if saved['sha256']!=b['sha256'] or saved['bytes']!=b['bytes']:faults.append({'path':b['backup'],'errors':'original_B2_snapshot_mismatch'})
    temporal.append({'path':rel,'B2_snapshot':saved,'R1_handover_snapshot':before,'current':now,'changed_B2_to_R1':saved['sha256']!=now['sha256'],'changed_handover_to_current':before['sha256']!=now['sha256']})
    original=(ROOT/b['backup']).read_text(encoding='utf-8-sig').splitlines(True); final=(ROOT/rel).read_text(encoding='utf-8-sig').splitlines(True)
    (OUT/(Path(rel).name+'.B2-to-final.diff')).write_text(''.join(difflib.unified_diff(original,final,fromfile='B2/'+rel,tofile='current/'+rel)),encoding='utf-8')
emit(OUT/'SOURCE_TEMPORAL_CLASSIFICATION.json',temporal)
churn=[]
for rel in ['Assets/Resources.meta','Assets/Settings/PC_RPAsset.asset','ProjectSettings/GraphicsSettings.asset','ProjectSettings/ProjectSettings.asset','ProjectSettings/URPProjectSettings.asset']:
    proc=subprocess.run(['git','show','HEAD:'+rel],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    head=hashlib.sha256(proc.stdout).hexdigest() if proc.returncode==0 else 'UNTRACKED_AT_HEAD'
    churn.append({'path':rel,'head':head,'current':info(ROOT/rel),'handover':info(SNAP/'workspace'/rel),'same_as_handover':info(ROOT/rel)==info(SNAP/'workspace'/rel)})
emit(OUT/'UNITY_CHURN_CLASSIFICATION.json',churn)
summary={'baseline_count':len(base['files']),'tsv_count':len(tsv),'unique_tsv_count':len(reported),'exact_path_set':set(reported)=={b['path'] for b in base['files']},'audit_entry_files':len(entry),'changed':changed,'exact_five_authorized_changes':set(changed)==allowed,'errors':faults,'result':'PASS' if not faults and len(tsv)==len(base['files']) and set(changed)==allowed else 'FAIL'}
emit(OUT/'summary.json',summary); print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(summary['result']!='PASS')
