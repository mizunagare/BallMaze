"""Verify immutable evidence and index bytes (or LFS oid), not merely filenames."""
import pathlib,sys,subprocess,json,hashlib,re
repo=pathlib.Path(sys.argv[1]);base='ProjectDocs/WanxiangGuitu/DeliveryBalanceAI01/';out=repo/base/'Evidence'
entries=json.loads((out/'manifest.json').read_text(encoding='utf-8'));bad=[];lfs=0
p=subprocess.Popen(['git','-C',str(repo),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for row in entries:
 rel=base+'Evidence/'+row['path'];data=(repo/rel).read_bytes()
 if hashlib.sha256(data).hexdigest()!=row['sha256']:bad.append([rel,'working hash'])
 p.stdin.write((':'+rel+'\n').encode('utf-8'));p.stdin.flush();header=p.stdout.readline().decode().strip().split()
 if len(header)!=3:bad.append([rel,'not staged']);continue
 raw=p.stdout.read(int(header[2]));p.stdout.read(1)
 if raw.startswith(b'version https://git-lfs.github.com/spec/v1'):
  oid=re.search(rb'oid sha256:([a-f0-9]{64})',raw);lfs+=1
  if not oid or oid[1].decode()!=row['sha256']:bad.append([rel,'LFS oid'])
 elif hashlib.sha256(raw).hexdigest()!=row['sha256']:bad.append([rel,'index bytes'])
p.stdin.close();p.wait()
staged=subprocess.check_output(['git','-C',str(repo),'diff','--cached','--name-only','-z']).decode().split('\0')
bad.extend([[x,'outside BALANCE-AI-01/plan'] for x in staged if x and not x.startswith(base) and x!='ProjectDocs/WanxiangGuitu/DEVELOPMENT_PLAN.md'])
result={'status':'FAIL' if bad else 'PASS','manifestFiles':len(entries),'lfsFiles':lfs,'failures':bad,'scope':'Exact owned evidence + staged index/LFS oid; no user data staged'}
(out/'publication-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
if bad:raise SystemExit(1)
