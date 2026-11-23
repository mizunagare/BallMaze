import pathlib,hashlib,json,csv,subprocess,collections,zipfile,tarfile,re,datetime,os,struct,zlib
R=pathlib.Path.cwd();D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation';O=D/'EVIDENCE/R2'
def sha(b):return hashlib.sha256(b).hexdigest().upper()
rows=list(csv.DictReader((D/'FINAL_RUN_RECONCILIATION.csv').open(encoding='utf-8-sig')))
target=[x for x in rows if x['driver_artifact_status']=='HISTORICAL_HASH_ONLY']; hashes=set(x['driver_sha256'] for x in target)
assert len(target)==114 and len(hashes)==18
matches={h:[] for h in hashes};errors=[];inventory=[];stats=collections.Counter()
def consider(b,where,kind):
 h=sha(b);stats[kind]+=1
 if h in matches:matches[h].append({'location':where,'kind':kind,'size':len(b),'sha256':h});p=O/'recovered'/h;p.parent.mkdir(exist_ok=True);p.write_bytes(b)
def git(args):
 c=subprocess.run(['git']+args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);return c
fsck=git(['fsck','--full','--no-reflogs','--unreachable']);(O/'git-fsck.txt').write_bytes(fsck.stdout+fsck.stderr)
obj=git(['cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)']);(O/'git-object-inventory.txt').write_bytes(obj.stdout)
blobs=[]
for line in obj.stdout.decode().splitlines():
 oid,t,n=line.split();stats['git_objects_total']+=1
 if t=='blob' and int(n)<=8*1024*1024:blobs.append(oid)
p=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for oid in blobs:
 p.stdin.write((oid+'\n').encode());p.stdin.flush();head=p.stdout.readline().split();n=int(head[2]);b=p.stdout.read(n);assert p.stdout.read(1)==b'\n';consider(b,'git:'+oid,'git_blob')
p.stdin.close();p.wait()
print('git search',dict(stats),flush=True)
# Read repository-owned files only; never walk user LocalLow, home or real save roots.
skip={'.git','Library','Temp','obj','node_modules','.vs','.idea','UserSettings','Packages'}
exts={'.ps1','.psm1','.cs','.py','.js','.cjs','.mjs','.txt','.log','.rsp','.json','.jsonl','.md','.csv','.tsv','.bak','.backup','.old','.orig','.tmp','.zip','.7z','.tar','.gz','.pdb','.dll','.exe'}
archives=[]
for base,dirs,files in os.walk(R):
 dirs[:]=[x for x in dirs if x not in skip and (pathlib.Path(base)/x).resolve()!=O.resolve()]
 for name in files:
  f=pathlib.Path(base)/name;rel=f.relative_to(R).as_posix();ext=f.suffix.lower()
  if ext not in exts and not any(s in name.lower() for s in ['driver','backup','archive','harness','tool']):continue
  try:
   n=f.stat().st_size
   if ext in {'.zip','.7z','.tar','.gz'}:archives.append(f);continue
   if n>64*1024*1024:stats['size_skipped']+=1;continue
   b=f.read_bytes();consider(b,rel,'file')
   if ext=='.pdb':
    inventory.append({'path':rel,'size':n,'sha256':sha(b),'kind':'PDB','format':'portable' if b.startswith(b'BSJB') else 'native_or_other','driver_hash_mentions':[h for h in hashes if h.encode() in b or h.lower().encode() in b],'launcher_name_mentions':list(set(re.findall(rb'[A-Za-z0-9_.-]+\.ps1',b)))[:50]})
   elif ext=='.rsp' or ('build' in rel.lower() and ext=='.log') or ('driver' in name.lower() and ext in {'.json','.log'}):
    inventory.append({'path':rel,'size':n,'sha256':sha(b),'kind':'compile_parameters_or_log','driver_hash_mentions':[h for h in hashes if h.encode() in b or h.lower().encode() in b]})
  except Exception as e:errors.append({'path':rel,'error':str(e)})
print('repository search',dict(stats),'archives',len(archives),flush=True)
for f in archives:
 rel=f.relative_to(R).as_posix()
 try:
  if zipfile.is_zipfile(f):
   with zipfile.ZipFile(f) as z:
    for i in z.infolist():
     if i.is_dir() or i.file_size>16*1024*1024:continue
     if pathlib.Path(i.filename).suffix.lower() in exts or any(s in i.filename.lower() for s in ['driver','backup','tool']):consider(z.read(i),rel+'!'+i.filename,'archive_member')
   inventory.append({'path':rel,'kind':'archive','status':'ZIP_READ'})
  elif tarfile.is_tarfile(f):
   with tarfile.open(f) as t:
    for i in t:
     if i.isfile() and i.size<=16*1024*1024:consider(t.extractfile(i).read(),rel+'!'+i.name,'archive_member')
   inventory.append({'path':rel,'kind':'archive','status':'TAR_READ'})
  else:inventory.append({'path':rel,'kind':'archive','status':'UNSUPPORTED_OR_NON_ARCHIVE'})
 except Exception as e:errors.append({'path':rel,'error':str(e)})
def serial(x):return x.decode(errors='replace') if isinstance(x,bytes) else str(x)
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'repository-owned Git objects reachable+unreachable and working files excluding Library/Temp/obj/node_modules/.vs/.idea/UserSettings/Packages and this new R2 evidence','targetRows':len(target),'uniqueDriverHashes':len(hashes),'r1PassRows':sum(x['group']=='r1new79' and x['recorded_class']=='PASS' for x in target),'stats':dict(stats),'fsckExitCode':fsck.returncode,'matches':matches,'inventory':inventory,'errors':errors,'unreachableObjectCount':sum('unreachable ' in x for x in (fsck.stdout+fsck.stderr).decode(errors='replace').splitlines())}
(O/'driver-search.json').write_text(json.dumps(report,ensure_ascii=True,indent=2,default=serial))
print(json.dumps({'stats':dict(stats),'matchedHashes':sum(bool(v) for v in matches.values()),'errors':len(errors),'r1PassRows':report['r1PassRows']}),flush=True)
