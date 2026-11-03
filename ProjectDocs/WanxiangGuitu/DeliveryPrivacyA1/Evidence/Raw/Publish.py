from pathlib import Path
import os,json,gzip,hashlib,re
r=Path('I:/WGCombat/PRIVACYA1-1103-A');out=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryPrivacyA1/Evidence/Raw');out.mkdir(exist_ok=False);rows=[]
for parent,dirs,files in os.walk(r):
 dirs[:]=[d for d in dirs if d not in ['Project','Project2','CleanProject','Library','Release','bin','obj','__pycache__']]
 for name in sorted(files):
  p=Path(parent)/name;rel=p.relative_to(r);ext=p.suffix.lower()
  if name.lower() in ['save.json','settings.json'] or ext not in ['.json','.jsonl','.txt','.log','.stdout','.stderr','.py','.ps1','.cs','.md']:continue
  raw=p.read_bytes();text=raw.decode('utf-8-sig');clean=text
  clean=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret|machine[_ ]?id|user[_ ]?id)\s*[:=]\s*)(?:Bearer\s+)?(?:"[^"\r\n]*"|[A-Za-z0-9._/+\-=]{8,})',r'\1[REDACTED]',clean)
  clean=re.sub(r'(?i)[A-Z]:[\\/]Users[\\/][^\\/\s"<>]+',r'[USERPROFILE]',clean)
  clean=re.sub(r'LicenseClient-[A-Za-z0-9_-]+','LicenseClient-[REDACTED]',clean)
  clean=re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[EMAIL_REDACTED]',clean)
  red=clean!=text;data=clean.encode('utf8') if red else raw
  if ext in ['.log','.stdout','.stderr','.jsonl']:data=gzip.compress(data,mtime=0);rel=rel.with_name(rel.name+'.gz')
  target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);rows.append({'path':rel.as_posix(),'sourceRelative':p.relative_to(r).as_posix(),'sourceSHA256':hashlib.sha256(raw).hexdigest(),'publishedSHA256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'redacted':red})
(out/'manifest.json').write_text(json.dumps(rows,indent=2));print(len(rows),'artifacts',sum(x['bytes'] for x in rows),'bytes')
