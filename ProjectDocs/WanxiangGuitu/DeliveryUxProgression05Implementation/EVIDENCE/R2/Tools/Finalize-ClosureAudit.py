import pathlib,json,csv,hashlib,subprocess,re,collections,datetime
R=pathlib.Path.cwd();D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation';O=D/'EVIDENCE/R2'
def lp(p):return pathlib.Path(chr(92)*2+'?'+chr(92)+str(p.resolve()))
def h(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
before=load(O/'preflight.json')
allowed={str((D/'FINAL_AUDIT.md').relative_to(R)).replace(chr(92),'/'),str((D/'FINAL_RISK_REGISTER.md').relative_to(R)).replace(chr(92),'/')}
changed=[];missing=[]
for row in before['files']:
    p=R/row['path']
    if not lp(p).is_file():missing.append(row['path']);continue
    if h(p)!=row['sha256'] or lp(p).stat().st_size!=row['size']:changed.append(row['path'])
assert not missing and set(changed)==allowed,(missing,changed)
assert h(pathlib.Path(before['indexPath']))==before['indexSha256']
for name,expected in [('UX05-IMGUI-R2/EVIDENCE/history-before.json',4142),('EVIDENCE/INDEX.json',5404)]:
    idx=load(D/name);assert len(idx['files'])==expected
    for row in idx['files']:
        assert h(D/row['path'])==row['sha256'].upper(),row['path']
        assert lp(D/row['path']).stat().st_size==row['bytes']
historical=list(csv.DictReader((D/'PLAYER_RUN_MATRIX.csv').open(encoding='utf-8-sig')))
reconciled=list(csv.DictReader((D/'FINAL_RUN_RECONCILIATION.csv').open(encoding='utf-8-sig')))
assert len(historical)==159 and len(reconciled)==159
assert {v['run_id']:v['status'] for v in historical}=={v['run_id']:v['recorded_class'] for v in reconciled}
link_errors=[]
for name in ['R2_FINAL_CLOSURE.md','FINAL_AUDIT.md','FINAL_RISK_REGISTER.md']:
    p=D/name
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
        if target.startswith(('http:','https:','#')):continue
        if target=='EVIDENCE/R2/INDEX.json':continue # generated below, then verified
        if not lp(p.parent/target.split('#')[0]).exists():link_errors.append([name,target])
assert not link_errors,link_errors
for name,n in [('DRIVER_ARCHIVE_RECOVERY.csv',114),('NODEFINE_RELEASE_RUN_MATRIX.csv',6)]:
    raw=list(csv.reader((D/name).open(encoding='utf-8-sig')));assert len(raw)==n+1 and all(len(v)==len(raw[0]) for v in raw)
new=load(O/'run-verification.json');assert new['statuses']=={'PASS':4,'INSTRUMENT_INTERRUPTED':2}
assert len({v['run_id'] for v in new['rows']})==6
for kind in ['nodefine','release']:
    storage=O/(kind+'-storage')
    for line in (storage/'storage-audit.jsonl').read_text().splitlines():
        record=json.loads(line)
        assert pathlib.Path(record['path']).resolve().is_relative_to(storage.resolve()),record
checks={}
for args in [['branch','--show-current'],['rev-parse','HEAD'],['diff','--cached','--name-only'],['diff','--check'],['status','--porcelain=v1'],['ls-remote','--heads','origin','feature/ux-progression-05-objective-history','feature/ux-progression-04-b2','main']]:
    c=subprocess.run(['git']+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    checks['git '+' '.join(args)]={'exitCode':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
assert checks['git rev-parse HEAD']['stdout'].strip()==before['head']
assert checks['git branch --show-current']['stdout'].strip()==before['branch']
assert checks['git diff --cached --name-only']['stdout']==''
assert checks['git diff --check']['exitCode']==0
protection={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'beforeFileCount':len(before['files']),'changedExistingFiles':changed,'missingExistingFiles':missing,'productSourceChangesThisRound':0,'schemaChangesThisRound':0,'projectSettingsChangesThisRound':0,'packagesChangesThisRound':0,'historical4142Mismatches':0,'existing5404IndexMismatches':0,'historical159ClassesUnchanged':True,'historicalClassificationCounts':dict(collections.Counter(v['status'] for v in historical)),'indexSha256Before':before['indexSha256'],'indexSha256After':h(pathlib.Path(before['indexPath'])),'linkErrors':link_errors,'csvChecks':'PASS','newRunStatuses':new['statuses'],'git':checks,'trueUserSaves':'not accessed; storage logs confined to two new evidence roots, not OS-wide retrospective tracing'}
(O/'protection-final.json').write_text(json.dumps(protection,ensure_ascii=True,indent=2))
files=[]
for p in O.rglob('*'):
    if p.is_file() and p.name!='INDEX.json':files.append({'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,'sha256':h(p)})
for name in ['R2_FINAL_CLOSURE.md','DRIVER_ARCHIVE_RECOVERY.csv','NODEFINE_RELEASE_RUN_MATRIX.csv','FINAL_AUDIT.md','FINAL_RISK_REGISTER.md']:
    p=D/name;files.append({'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,'sha256':h(p)})
index={'closure':'UX-05-R2-FINAL-CLOSURE','verdict':'CONDITIONAL_PASS','F01':'CLOSED_FINAL_PURE_RUNTIME','F02':'OPEN_114_RUNS_18_DRIVER_SOURCE_HASHES_31_R1_PASS','historicalRunCount':159,'historicalClassificationsChanged':False,'newRunCount':6,'newRunClassifications':new['statuses'],'files':sorted(files,key=lambda x:x['path'])}
(O/'INDEX.json').write_text(json.dumps(index,ensure_ascii=True,indent=2))
assert lp(O/'INDEX.json').is_file()
for row in index['files']:assert h(D/row['path'])==row['sha256']
print(json.dumps({'verdict':index['verdict'],'newRuns':index['newRunClassifications'],'historicalFilesUnchanged':4142,'oldIndexItemsUnchanged':5404,'existingFileChanges':changed,'productChanges':0,'indexUnchanged':True,'closureIndexItems':len(files),'csvLinks':'PASS','gitDiffCheck':0}))
