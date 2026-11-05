from pathlib import Path
import sys,json,hashlib,gzip,re
root=Path(sys.argv[1]);out=Path(__file__).resolve().parents[1]/'Evidence'
out.mkdir(exist_ok=True)
old=json.loads((out/'manifest.json').read_text('utf-8')) if (out/'manifest.json').exists() else []
known={x['sourceRelative']:x for x in old};manifest=list(old);skipped=[]
def sha(b):return hashlib.sha256(b).hexdigest()
for f in sorted(root.rglob('*')):
 if not f.is_file():continue
 rel=f.relative_to(root)
 if rel.parts[0] in {'LabBefore','PureExcluded','RetiredDriver','pycache'}:continue
 raw=f.read_bytes();rh=sha(raw)
 if rel.parts[0]=='PriorUnfinished' and 'Assets' in rel.parts:continue
 if any(x in rel.parts for x in ['bin','obj','Release','Project','Library']):
  if 'Release' in rel.parts:skipped.append(dict(path=rel.as_posix(),bytes=len(raw),sha256=rh))
  continue
 if f.suffix.lower() not in ['.json','.jsonl','.log','.stdout','.stderr','.png','.cs','.txt','.ps1','.csv','.skip','.cpp','.bak','.csproj']:continue
 key=rel.as_posix()
 if key in known:
  assert known[key]['sourceSHA256']==rh, 'Old raw evidence changed: '+key
  assert sha((out/known[key]['path']).read_bytes())==known[key]['publishedSHA256']
  continue
 payload=raw;redacted=False
 if f.suffix.lower()!='.png':
  try:text=raw.decode('utf-8-sig')
  except UnicodeDecodeError:continue
  clean=re.sub(r'LicenseClient-[\w-]+','LicenseClient-[REDACTED]',text)
  clean=re.sub(r'(?i)(access[_ ]?token\s*:\s*)"[^"]*"',r'\1"[REDACTED]"',clean)
  clean=re.sub(r'(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s"<>]+','[USERPROFILE]',clean)
  # Native heap bytes are not needed to explain warnings and may contain memory contents.
  clean=re.sub(r'(?m)^.*(?:0x[0-9A-Fa-f]+:|[0-9A-Fa-f]{16}:)(?:\s+[0-9A-Fa-f]{2}){8,}.*$', '[NATIVE_HEAP_BYTES_REDACTED]',clean)
  redacted=clean!=text
  if redacted:payload=clean.encode('utf-8')
 if f.suffix.lower() in ['.jsonl','.log','.stdout','.stderr','.bak'] or 'WanxiangGuitu' in rel.parts or 'SeedPackage' in rel.parts:
  payload=gzip.compress(payload,mtime=0);rel=rel.with_name(rel.name+'.gz')
 target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists(), 'Refuse overwrite '+str(target);target.write_bytes(payload)
 manifest.append(dict(path=rel.as_posix(),sourceRelative=key,sourceSHA256=rh,publishedSHA256=sha(payload),sourceBytes=len(raw),redacted=redacted))
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf-8')
(out/'build-files.json').write_text(json.dumps(skipped,indent=2),'utf-8')
(out/'.gitattributes').write_text('* -text\n','utf-8')
print(len(manifest),'published; raw originals unchanged')
