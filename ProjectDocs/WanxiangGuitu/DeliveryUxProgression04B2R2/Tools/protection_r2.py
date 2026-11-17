"""Post-stop protection verification only. Does not run Player or alter old files."""
from pathlib import Path
import hashlib,json,csv,subprocess
R=Path.cwd(); D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2'; S=Path('I:/unity/WanxiangGuitu-UX04B2R2-snapshot-20261116-1459'); E=R/'Evidence/Runs04B2R2/SESSION-20261116-R2-01'
def xp(p):return Path(chr(92)*2+'?'+chr(92)+str(p.absolute()))
def info(p):
    p=xp(p)
    if not p.is_file():return ('MISSING',None)
    with p.open('rb') as f:return (hashlib.file_digest(f,'sha256').hexdigest(),p.stat().st_size)
base=json.loads((S/'PRECHANGE_R2_SHA256.json').read_text(encoding='utf-8')); rows=[]; errors=[]
for b in base['files']:
    current=info(R/b['path']);snapshot=info(S/'workspace'/b['path']);good=current==(b['sha256'],b['bytes']) and snapshot==(b['sha256'],b['bytes'])
    rows.append({'path':b['path'],'preR2SHA256':b['sha256'],'preR2Bytes':b['bytes'],'currentSHA256':current[0],'currentBytes':current[1],'snapshotSHA256':snapshot[0],'snapshotBytes':snapshot[1],'result':'UNCHANGED' if good else 'MISMATCH'})
    if not good:errors.append(rows[-1])
p=D/'PROTECTION_SHA256.tsv';assert not p.exists()
with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0],delimiter='\t');w.writeheader();w.writerows(rows)
frozen=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/SUBMIT_WHITELIST.csv';fr=list(csv.DictReader(frozen.open(encoding='utf-8-sig')))
frozen_changed=[x['path'] for x in fr if not (R/x['path']).is_file() or (x['sha256']!='SELF_REFERENTIAL_META' and info(R/x['path'])[0]!=x['sha256'])]
g=lambda *a:subprocess.run(['git',*a],capture_output=True,text=True)
summary={'preR2FileCount':len(rows),'allOriginalFilesByteIdentical':not errors,'snapshotMatches':not errors,'changedOrMissing':errors,'frozenPaths':len(fr),'frozenPayloadChanged':frozen_changed,'head':g('rev-parse','HEAD').stdout.strip(),'branch':g('branch','--show-current').stdout.strip(),'staged':g('diff','--cached','--name-status').stdout.strip(),'diffCheckExitCode':g('diff','--check').returncode,'productSourceEditsDuringR2':[],'result':'PASS' if not errors and not frozen_changed else 'FAIL'}
assert not (E/'protection-result.json').exists();(E/'protection-result.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(summary['result']!='PASS')
