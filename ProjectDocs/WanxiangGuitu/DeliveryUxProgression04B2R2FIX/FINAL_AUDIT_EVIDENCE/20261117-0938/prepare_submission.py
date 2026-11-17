"""Create new literal candidate list and review bundle; never stage, mutate originals, build or run Unity."""
from pathlib import Path
import json,hashlib,subprocess,csv,shutil,zipfile,sys
R=Path.cwd();D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX';A=Path(__file__).resolve().parent;OLD=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/SUBMIT_WHITELIST.txt';TXT=D/'SUBMIT_WHITELIST.txt';CSV=D/'SUBMIT_WHITELIST.csv';REPORT=D/'FINAL_AUDIT.md'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def rel(p):return p.relative_to(R).as_posix()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,text):assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def git(*args,stdin=None):
 p=subprocess.run(['git',*args],input=stdin,capture_output=True);assert p.returncode==0,(args,p.stderr);return p.stdout

def prepare():
 snap=Path('I:/unity/WanxiangGuitu-UX04B2R2FIX-FinalAudit-snapshot-20261117-0940');oldSnap=Path('I:/unity/WanxiangGuitu-UX04B2R2FIX-snapshot-20261116-1536')
 for source,name in [(snap/'ROBOCOPY.log','WORKSPACE_SNAPSHOT_ROBOCOPY.log'),(snap/'SNAPSHOT_SCOPE.txt','WORKSPACE_SNAPSHOT_SCOPE.txt'),(oldSnap/'PRECHANGE_FIX_SHA256.json','PRECHANGE_FIX_SHA256.original.json')]:
  assert not (A/name).exists();shutil.copyfile(source,A/name)
 put(A/'AUDIT_DIAGNOSTICS.md','# Audit diagnostics (not Player Run verdicts)\n\n- Original 25 Player records still have exactly four FAIL; none changed.\n- First PDB parser diagnostic assumed every Document existed on disk and retained COMPILER_PDB_SOURCE_CHECKSUMS.json FAIL for one Unity generated virtual document. PDB_SOURCE_AUDIT.json independently validates its original embedded text; 153 project sources and one generator source verified. No source/PDB/DLL was repaired.\n- First read-only oracle wrapper supplied relative paths; evaluator required absolute paths and exited before writing any output. Only new wrapper corrected to resolve paths; fresh 18,306 checks then pass. Original Oracle never rewritten.\n- No Unity compilation/Player launch in this final audit.\n')
 old={x.strip() for x in OLD.read_text(encoding='utf-8-sig').splitlines() if x.strip() and not x.startswith('#')};assert len(old)==961
 idx=load(D/'EVIDENCE/INDEX.json');fixed={x['path'] for x in idx['artifacts']};r2={rel(p) for root in [R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2',R/'Evidence/Runs04B2R2'] for p in root.rglob('*') if p.is_file() and '_roots' not in p.parts and '__pycache__' not in p.parts}
 audit={rel(p) for p in A.rglob('*') if p.is_file() and '__pycache__' not in p.parts};reserved={rel(TXT),rel(CSV),rel(REPORT),rel(A/'FINAL_INTEGRITY.json'),rel(A/'SUBMISSION_SCOPE.json')};paths=sorted(old|fixed|r2|audit|reserved|{rel(D/'EVIDENCE/INDEX.json')})
 assert all(not x.startswith(('Builds/','Library/','Temp/','Packages/','ProjectSettings/')) and x!='Assets/Resources.meta' and '/_roots/' not in x and not x.endswith(('.zip','.pyc')) for x in paths)
 sources=[x for x in paths if x.startswith('Assets/')];assert len(sources)==11 and all(x.startswith('Assets/CombatPrototype/') for x in sources)
 obj={'scope':'Accumulated B2/R1/R2/R2FIX candidate only, NOT authorization to stage/commit. Old961 original unchanged.','legacy961':len(old),'fixedIndexed':len(fixed),'R2AdditionalOutsidePriorSets':len(r2-old-fixed),'candidateCount':len(paths),'paths':paths,'productPaths':sources,'transportExcluded':[rel(D/'FINAL_AUDIT_PACKAGE.zip'),rel(D/'FINAL_AUDIT_PACKAGE_SHA256.txt')],'excludePolicy':['all unrelated worktree content','Builds Library Temp caches','Assets/Resources.meta','ProjectSettings Packages scenes prefabs','runtime _roots live copy (canonical original-root evidence retained)','transport ZIP and its sidecar (derived duplicate)'],'selfHashPolicy':'TXT includes itself and CSV as literal paths. CSV hashes every candidate except CSV itself; its own digest is in bundle manifest/ZIP. No impossible self-hash placeholders or invented zeros.'}
 put(A/'SUBMISSION_SCOPE.json',json.dumps(obj,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in obj.items() if k!='paths'},ensure_ascii=False,indent=2))
def freeze():
 s=load(A/'SUBMISSION_SCOPE.json');paths=s['paths'];assert REPORT.is_file()
 put(TXT,'# UX-04-B2-R2-FIX final literal candidate whitelist; NOT staging/commit/push authorization.\n# Old 961 list is immutable; new union is intentionally separate.\n# Exactly '+str(len(paths))+' literal paths; no directory globs. Exclusions and scope are in FINAL_AUDIT.md.\n'+'\n'.join(paths)+'\n')
 entry=load(A/'ENTRY_STATE.json');idx=load(D/'EVIDENCE/INDEX.json');bad=[]
 for x in idx['artifacts']+idx['immutableHistoricalReferences']:
  p=R/x['path']
  if not p.is_file() or sha(p)!=x['sha256'] or p.stat().st_size!=x['bytes']:bad.append(x['path'])
 for x in entry['sourceFiles']:
  if sha(R/x['path'])!=x['currentSHA256']:bad.append(x['path'])
 assert not bad,bad;staged=git('diff','--cached','--name-status').decode().strip();assert not staged
 assert git('rev-parse','HEAD').decode().strip()==entry['head'];assert git('branch','--show-current').decode().strip()==entry['branch'];assert sha(D/'EVIDENCE/INDEX.json')==entry['frozenIndexSHA256']
 put(A/'FINAL_INTEGRITY.json',json.dumps({'result':'PASS_READONLY_CLOSURE','old901AndHistoricalReferenceDrift':bad,'fourProductSourceDrift':[],'head':entry['head'],'branch':entry['branch'],'stagedEmpty':True,'candidateCount':len(paths),'originalsUntouched':True,'old901IndexNotRewritten':True,'noBuildNoPlayerNoStage':True},indent=2))
 tracked=set(git('ls-files','-z').decode('utf-8').split('\0'));ig=subprocess.run(['git','check-ignore','--stdin','-z'],input=('\0'.join(paths)+'\0').encode(),capture_output=True);assert ig.returncode in (0,1);ignored=set(ig.stdout.decode().split('\0'));rows=[]
 for x in paths:
  if x==rel(CSV):continue
  p=R/x;assert p.is_file(),x;category='PRODUCT' if x.startswith('Assets/') else 'AUDIT' if '/FINAL_AUDIT_EVIDENCE/' in x or x in (rel(REPORT),rel(TXT)) else 'HISTORICAL_OR_DELIVERY'
  rows.append({'path':x,'bytes':p.stat().st_size,'sha256':sha(p),'gitKind':'TRACKED_MODIFIED' if x in tracked else 'IGNORED_UNTRACKED' if x in ignored else 'UNTRACKED','category':category})
 assert not CSV.exists()
 with CSV.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print(json.dumps({'candidateCount':len(paths),'hashedCSVRows':len(rows),'selfCSVExcludedFromOwnHash':True,'tracked':sum(r['gitKind']=='TRACKED_MODIFIED' for r in rows),'ignoredUntracked':sum(r['gitKind']=='IGNORED_UNTRACKED' for r in rows)},indent=2))
def bundle():
 s=load(A/'SUBMISSION_SCOPE.json');paths=s['paths'];candidate={x:R/x for x in paths};pdb=load(A/'PDB_SOURCE_AUDIT.json');context={rel(Path(x['path'])):Path(x['path']) for x in pdb['documents'] if Path(x['path']).is_file()};members={**context,**candidate};entries=[];out=D/'FINAL_AUDIT_PACKAGE.zip';assert not out.exists()
 with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,p in sorted(members.items()):
   digest=sha(p);z.write(p,name);entries.append({'path':name,'bytes':p.stat().st_size,'sha256':digest,'candidate':name in candidate})
  z.writestr('BUNDLE_MANIFEST.json',json.dumps({'scope':'Review bundle, not a staged tree. Includes exact candidate files plus compiler-source context. No Builds/Library/full Player shell. Source code is current original byte content; generated text extracted separately in audit.','candidateCount':len(candidate),'members':entries,'manifestSelfHash':'Excluded, intentionally no self-reference'},ensure_ascii=False,indent=2))
 with zipfile.ZipFile(out) as z:
  assert len(z.namelist())==len(set(z.namelist()))==len(entries)+1
  for row in entries:
   raw=z.read(row['path']);assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 put(D/'FINAL_AUDIT_PACKAGE_SHA256.txt',sha(out)+'  FINAL_AUDIT_PACKAGE.zip\n')
 print(json.dumps({'zip':rel(out),'bytes':out.stat().st_size,'sha256':sha(out),'candidatePaths':len(candidate),'bundleMaterialMembers':len(entries),'allZipMembersRehashed':True},indent=2))
{'prepare':prepare,'freeze':freeze,'bundle':bundle}[sys.argv[1]]()
