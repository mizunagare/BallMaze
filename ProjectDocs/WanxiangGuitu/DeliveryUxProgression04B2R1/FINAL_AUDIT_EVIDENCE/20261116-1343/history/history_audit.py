import json,hashlib,csv,re,subprocess,collections,urllib.parse
from pathlib import Path
ROOT=Path.cwd(); OUT=ROOT/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/history'
inputs=json.loads((OUT/'discovered_inputs.json').read_text('utf-8'))
cache={}; checks=[]; inventories=[]; links=[]; runs=[]; relations=[]
def norm(p):
 p=str(p).replace('\\','/'); prefix=str(ROOT).replace('\\','/')+'/'
 return p[len(prefix):] if p.lower().startswith(prefix.lower()) else p
def meta(p):
 p=norm(p)
 if p not in cache:
  q=ROOT/p
  if not q.is_file(): cache[p]={'path':p,'exists':q.exists(),'isFile':False,'sha256':None,'bytes':None}
  else:
   h=hashlib.sha256()
   with q.open('rb') as f:
    for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
   cache[p]={'path':p,'exists':True,'isFile':True,'sha256':h.hexdigest(),'bytes':q.stat().st_size}
 return cache[p]
def check(p,h=None,b=None,source='',kind='reference'):
 m=meta(p); status='MISSING' if not m['exists'] else ('DIRECTORY' if not m['isFile'] else ('HASH_MISMATCH' if h and m['sha256']!=h.lower() else ('SIZE_MISMATCH' if b is not None and m['bytes']!=b else 'MATCH' if h else 'EXISTS_NO_EXPECTED_HASH')))
 checks.append(dict(m,expectedSHA256=h,expectedBytes=b,source=source,kind=kind,status=status));return checks[-1]
def load(p):return json.loads((ROOT/p).read_text('utf-8-sig'))
def walk(o,src,base=None,trail=''):
 if isinstance(o,dict):
  if isinstance(o.get('path'),str) and re.fullmatch('[a-fA-F0-9]{64}',str(o.get('sha256',''))):check(o['path'] if o['path'].startswith(('Evidence/','Assets/','ProjectDocs/')) or Path(o['path']).is_absolute() else str((base or Path(src).parent)/o['path']),o['sha256'],o.get('bytes'),src,'json-path-sha')
  if 'supersededBy' in o: relations.append({'source':src,'location':trail,'supersededBy':o['supersededBy']})
  if isinstance(o.get('files'),dict):
   for n,d in o['files'].items():
    if isinstance(d,dict) and 'sha256' in d:check(str((base or Path(src).parent)/n),d['sha256'],d.get('bytes'),src,'manifest-file-sha')
  for k,v in o.items():
   if k!='files' or isinstance(v,list):walk(v,src,base,trail+'/'+k)
 elif isinstance(o,list):
  for i,v in enumerate(o):walk(v,src,base,trail+'/'+str(i))
for p in inputs:
 if '/FINAL_AUDIT_EVIDENCE/' in p:continue
 inventories.append(meta(p))
 if p.endswith('INDEX.json'):
  o=load(p)
  if '04B2/EVIDENCE' in p:
   for d in o['buildReceipts'].values():check(d['path'],d['sha256'],d.get('bytes'),p,'B2-index-receipt')
   for r in o['runs']:walk(r,p,Path(r['evidenceDir']))
  else:walk(o,p)
 elif p.endswith('run-manifest.json'):
  o=load(p);walk(o,p,Path(p).parent);runs.append({'manifest':p,**{k:o.get(k) for k in ['runId','verdict','exitCode','completeFlag','driverDllSHA256','dllSHA256','buildId']}})
 elif p.endswith('.json'):
  walk(load(p),p,Path(p).parent)
  if p.endswith('_baseline_snapshot/snapshot.json'):
   for entry in load(p)['files']:check(entry['backup'],entry['sha256'],entry['bytes'],p,'historical-snapshot-backup')
 if p.endswith('.md'):
  text=(ROOT/p).read_text('utf-8-sig')
  for match in re.finditer(r'\]\(<?([^)>]+)>?\)',text):
   v=urllib.parse.unquote(match.group(1)).split('#')[0]
   if not v or v.startswith(('http:','https:','mailto:')):continue
   q=norm(v) if re.match(r'^[A-Za-z]:',v) else norm(str(Path(p).parent/v))
   links.append({'source':p,'target':v,'resolved':q,'exists':(ROOT/q).exists()});meta(q)
 if p.endswith(('.csv','.tsv')):
  delim='\t' if p.endswith('.tsv') else ','
  with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:
   for i,row in enumerate(csv.DictReader(f,delimiter=delim),2):
    for key,v in row.items():
     if not v:continue
     if v.startswith(('Assets/','ProjectDocs/','Evidence/','Packages/','ProjectSettings/')):
      h=row.get('current_sha256') if key=='file' else None
      if not h and any(token in v for token in [' + ',' / ','*','...']):
       checks.append({'path':v,'source':p+':'+str(i),'kind':'csv-design-expression','status':'DESIGN_EXPRESSION_NOT_LITERAL_PATH','exists':None,'sha256':None})
      else:check(v,h,source=p+':'+str(i),kind='protection-current' if h else 'csv-path')
# Independently cross-check matrix run identity against actual manifest, never trust counts.
identity=[]
for p in inputs:
 if not p.endswith('PLAYER_RUN_MATRIX.csv'):continue
 for row in csv.DictReader((ROOT/p).open(encoding='utf-8-sig',newline='')):
  mp=row.get('manifest') or row.get('runManifest')
  if not mp:continue
  o=load(mp);dif={k:{'csv':v,'manifest':o.get(k)} for k,v in row.items() if k in o and isinstance(o[k],(str,int)) and str(o[k])!=v}
  identity.append({'csv':p,'runId':row['runId'],'manifest':mp,'differences':dif})
# Historical archived binary lookup: only discovered archival DLLs, plus receipt's actual live target.
archives=[meta(p) for p in inputs if p.endswith('.dll')]
receipts=[]
for p in inputs:
 if not ('injection' in p and p.endswith('.json')):continue
 o=load(p);h=o.get('driverDllSHA256'); live=meta(o['driverDll']) if o.get('driverDll') else None
 source=o.get('executedSource');sm=check(source,o.get('executedSourceSHA256'),source=p,kind='executed-driver-source') if source else None
 matches=[m for m in archives if m['sha256']==h]
 receipts.append({'receipt':meta(p),'driverSHA256':h,'archivedBinaryMatches':matches,'liveBinary':live,'liveMatchesReceipt':bool(live and live['sha256']==h),'executedSource':sm,'status':'ARCHIVE_AVAILABLE' if matches else 'LIVE_ONLY_NOT_ARCHIVED' if live and live['sha256']==h else 'HISTORICAL_BINARY_UNAVAILABLE'})
manual=[]
for p in inputs:
 if '/manual-' not in p:continue
 o=load(p)
 for item in o.get('observations',[]):
  if item.get('path'):check(str(Path(p).parent/item['path']),item.get('sha256'),source=p,kind='manual-screenshot')
 manual.append({'path':p,'record':o})
recompute=[{'path':p,'sha256':meta(p)['sha256'],'summary':load(p)} for p in inputs if '/recompute-' in p and p.endswith('summary.json')]
# Read-only git diagnostics, expected non-zero for unset config/check-ignore absent matches are recorded, not hidden.
def git(args,stdin=None):
 r=subprocess.run(['git',*args],input=stdin,text=True,encoding='utf-8',errors='replace',capture_output=True)
 return {'args':args,'exitCode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
formal=sorted(p for p in inputs if p.startswith('ProjectDocs/') and '/FINAL_AUDIT_EVIDENCE/' not in p)
evidence=sorted({c['path'] for c in checks if c['path'].startswith('Evidence/') and c.get('exists') and c['kind']!='protection-current'}|{p for p in inputs if p.startswith('Evidence/')})
evidence=[p for p in evidence if not any(x in p for x in ['/_roots/','/runs/']) and (p.startswith('Evidence/Runs04B2/UX04-B2-') or p.startswith('Evidence/Runs04B2/_build/') or p.startswith('Evidence/Runs04B2R1/SESSION-20261116-1115/') or p.startswith('Evidence/Runs04B2R1/_build/'))]
ignore=git(['check-ignore','-v','--stdin'], '\n'.join(formal+evidence)+'\n')
gitfacts=[git(['config','--get','core.sparseCheckout']),git(['config','--get','core.sparseCheckoutCone']),git(['rev-parse','--git-path','info/sparse-checkout']),git(['ls-files','-v','--',*formal]),ignore]
# Suggested precise candidate lists, not a final whitelist. Exclude runtime roots, all Builds/Library and unrelated historical trees.
failruns=[r for r in runs if r['verdict']!='PLAYER_RUN_COMPLETED' or r['exitCode']!=0]
failprefixes={str(Path(r['manifest']).parent).replace('\\','/')+'/' for r in failruns}
required_failures=sorted({p for p in evidence if any(p.startswith(pre) for pre in failprefixes)}|{p for p in inputs if '/recompute-A01' in p or '/manual-A02' in p})
# Explain legacy digest convention without treating normalization as byte equivalence.
for c in checks:
 if c['status']=='HASH_MISMATCH':
  b=(ROOT/c['path']).read_bytes(); expected=c['expectedSHA256']
  variants={'LF':b.replace(b'\r\n',b'\n'),'CRLF':b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'),'UTF8_BOM_REMOVED':b.removeprefix(b'\xef\xbb\xbf')}
  c['matchingRepresentationVariants']=[name for name,value in variants.items() if hashlib.sha256(value).hexdigest()==expected]
b2index=load('ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/EVIDENCE/INDEX.json')
b2details={'declaredEvidenceFiles':b2index['totalEvidenceFiles'],'actualListedRunFiles':sum(len(r['files']) for r in b2index['runs']),'receiptFiles':len(b2index['buildReceipts']),'finalRuns':[r['runId'] for r in b2index['runs']],'indexSHA256':meta('ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/EVIDENCE/INDEX.json')['sha256']}
result={'B2IndexDetail':b2details,'method':'read-only path/byte/SHA-256 checks; no replay/build; current state cannot prove previous byte identity without prior trusted digest','fileInventory':inventories,'pathHashChecks':checks,'missingOrMismatch':[c for c in checks if c['status'] in ['MISSING','HASH_MISMATCH','SIZE_MISMATCH']],'markdownLinks':links,'brokenMarkdownLinks':[x for x in links if not x['exists']],'runs':runs,'nonPassRuns':failruns,'supersededBy':relations,'matrixIdentityChecks':identity,'driverReceipts':receipts,'manualReviews':manual,'recomputeHistory':recompute,'gitFacts':gitfacts,'candidateFormalFiles_NOT_FINAL_WHITELIST':formal,'candidateEvidenceFiles_NOT_FINAL_WHITELIST':evidence,'mustPreserveFailureFiles':required_failures,'allResolvedFiles':sorted(cache.values(),key=lambda x:x['path'])}
(OUT/'HISTORY_PATH_HASH_MISSING.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
summary={'inventory':len(inventories),'checks':len(checks),'statuses':dict(collections.Counter(x['status'] for x in checks)),'brokenMarkdown':result['brokenMarkdownLinks'],'nonPassRuns':failruns,'supersededBy':relations,'driverReceipts':[{k:r[k] for k in ['driverSHA256','status','liveMatchesReceipt']}|{'receipt':r['receipt']['path']} for r in receipts],'recompute':[{k:r['summary'].get(k) for k in ['verdict','failed','passed']}|{'path':r['path']} for r in recompute],'identityMismatches':[i for i in identity if i['differences']],'candidateFormal':len(formal),'candidateEvidence':len(evidence),'mustPreserveFailures':len(required_failures),'gitFacts':gitfacts[:3]+[ignore]}
(OUT/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(summary,ensure_ascii=False,indent=2))
