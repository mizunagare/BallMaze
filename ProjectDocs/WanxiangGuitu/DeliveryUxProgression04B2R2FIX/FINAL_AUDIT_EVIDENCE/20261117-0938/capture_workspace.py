"""Read-only current Git/source capture; writes ONLY this new audit folder."""
from pathlib import Path
import subprocess,json,hashlib,difflib
R=Path.cwd();A=Path(__file__).resolve().parent
S=Path('I:/unity/WanxiangGuitu-UX04B2R2FIX-snapshot-20261116-1536/workspace')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def git(*args):
 p=subprocess.run(['git',*args],capture_output=True);assert p.returncode==0,(args,p.stderr.decode(errors='replace'));return p.stdout

def put(name,data):
 p=A/name;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data if isinstance(data,bytes) else data.encode('utf-8'))
head=git('rev-parse','HEAD').decode().strip();branch=git('branch','--show-current').decode().strip();staged=git('diff','--cached','--name-status');assert not staged.strip();assert head=='95caf234256613d4a6e4f89a8ab0dc09c397c6b2' and branch=='feature/ux-progression-04-b2'
for name,args in {'GIT_STATUS.txt':['status','--short','--untracked-files=all'],'GIT_STATUS_PORCELAIN_V2.txt':['status','--porcelain=v2','--untracked-files=all'],'GIT_DIFF_HEAD.patch':['diff','--binary','--full-index','HEAD','--'],'GIT_CACHED_DIFF.patch':['diff','--cached','--binary','--full-index'],'GIT_TRACKED_LS_FILES.txt':['ls-files'],'GIT_UNTRACKED_LS_FILES.txt':['ls-files','--others','--exclude-standard']}.items():put(name,git(*args))
paths=[Path('Assets/CombatPrototype')/n for n in ['AdventureLoadout.cs','B2AttackModel.cs','CatInventoryPresenter.cs','ContainerInventoryView.cs']];src=[]
for p in paths:
 data=p.read_bytes();old=(S/p).read_bytes();put('SOURCE_CURRENT/'+p.name,data);put('SOURCE_FIX_BEFORE/'+p.name,old)
 diff=''.join(difflib.unified_diff(old.decode('utf-8-sig').splitlines(True),data.decode('utf-8-sig').splitlines(True),fromfile='FIX-before/'+p.as_posix(),tofile='CURRENT/'+p.as_posix()));put('DIFF_FIX_BEFORE/'+p.name+'.diff',diff)
 previous=subprocess.run(['git','show','HEAD:'+p.as_posix()],capture_output=True)
 if previous.returncode==0:put('SOURCE_HEAD/'+p.name,previous.stdout);base=previous.stdout.decode('utf-8-sig').splitlines(True);label='HEAD/'+p.as_posix()
 else:base=[];label='/dev/null'
 put('DIFF_HEAD/'+p.name+'.diff',''.join(difflib.unified_diff(base,data.decode('utf-8-sig').splitlines(True),fromfile=label,tofile=p.as_posix())))
 src.append({'path':p.as_posix(),'currentSHA256':sha(p),'currentBytes':len(data),'fixBeforeSHA256':sha(S/p),'trackedAtHead':previous.returncode==0,'headSHA256':hashlib.sha256(previous.stdout).hexdigest() if previous.returncode==0 else None})
for n in ['B2Collection.cs','B2Collection.cs.meta','B2InventoryQuery.cs','B2InventoryQuery.cs.meta','B2AttackModel.cs.meta','CampInventoryView.cs','CampRuntime.cs']:
 p=Path('Assets/CombatPrototype')/n;put('SUPPORTING_CURRENT/'+n,p.read_bytes())
idx=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/INDEX.json';j=json.loads(idx.read_text(encoding='utf-8'));bad=[]
for x in j['artifacts']+j['immutableHistoricalReferences']:
 p=R/x['path']
 if not p.is_file() or sha(p)!=x['sha256'] or p.stat().st_size!=x['bytes']:bad.append(x['path'])
put('ENTRY_STATE.json',json.dumps({'head':head,'branch':branch,'stagedEmpty':not staged.strip(),'sourceFiles':src,'frozenIndexSHA256':sha(idx),'indexedPayloads':len(j['artifacts']),'oldIndexActualHashErrors':bad,'scope':'Current source copies and full HEAD diff; untracked B2 source explicitly diffed from /dev/null. New audit outputs are not retroactively added to old901 index.'},ensure_ascii=False,indent=2));assert not bad,bad
print(json.dumps({'head':head,'branch':branch,'currentSourceCopies':4,'old901ActualHashErrors':bad,'untrackedB2Captured':True},indent=2))
