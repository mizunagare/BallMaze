from pathlib import Path
import json,hashlib,gzip,re,sys
root=Path(sys.argv[1]);out=Path(__file__).resolve().parents[1]/'Evidence';append='--append' in sys.argv
out.mkdir(exist_ok=append)
manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8')) if append else []
existing={x['sourceRelative']:x for x in manifest}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def publish(f,rel):
 raw=f.read_bytes();payload=raw;redacted=False;encoding='binary'
 previous=existing.get(f.relative_to(root).as_posix())
 if previous:
  assert hashlib.sha256(raw).hexdigest()==previous['sourceSHA256'], 'Existing raw evidence changed: '+str(f)
  assert digest(out/previous['path'])==previous['publishedSHA256'], 'Published bytes changed'
  return
 if f.suffix.lower() in ('.json','.jsonl','.log','.stdout','.stderr','.txt','.ps1','.cs','.csv','.cpp'):
  encoding='utf-8-sig'
  try:text=raw.decode(encoding)
  except UnicodeDecodeError:
   if f.name!='hardware.json':raise
   encoding='gbk';text=raw.decode(encoding);json.loads(text)
  clean=re.sub(r'(?i)(access[_ ]?token\s*:\s*)"[^"]*"',r'\1"[REDACTED]"',text)
  clean=re.sub(r'LicenseClient-[\w-]+','LicenseClient-[REDACTED]',clean)
  clean=re.sub(r'(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s"<>]+','[USERPROFILE]',clean)
  redacted=clean!=text
  if redacted or encoding!='utf-8-sig':payload=clean.encode('utf8')
 if f.suffix.lower() in ('.log','.stdout','.stderr','.jsonl'):
  payload=gzip.compress(payload,mtime=0);rel=rel.with_name(rel.name+'.gz')
 p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(payload)
 manifest.append(dict(path=rel.as_posix(),sourceRelative=f.relative_to(root).as_posix(),sourceSHA256=hashlib.sha256(raw).hexdigest(),publishedSHA256=hashlib.sha256(payload).hexdigest(),redacted=redacted,sourceEncoding=encoding))
for folder in root.iterdir():
 if not folder.is_dir() or folder.name=='Project':continue
 for f in folder.rglob('*'):
  if not f.is_file() or 'Release' in f.relative_to(folder).parts:continue
  if f.suffix.lower() in ('.json','.jsonl','.log','.stdout','.stderr','.png','.cs','.txt','.ps1','.csv','.cpp'):publish(f,f.relative_to(root))
for f in root.iterdir():
 if f.is_file() and f.suffix.lower() in ('.json','.jsonl','.txt','.ps1'):publish(f,f.relative_to(root))
builds=[]
for folder in root.iterdir():
 b=folder/'Release';exe=b/'WanxiangGuitu.exe'
 if not exe.exists():continue
 files=[dict(path=f.relative_to(b).as_posix(),bytes=f.stat().st_size,sha256=digest(f)) for f in b.rglob('*') if f.is_file()]
 (out/folder.name).mkdir(exist_ok=True)
 (out/folder.name/'release-files.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
 for suffix in ('.release.json','.summary.txt','.bee.json'):publish(Path(str(exe)+suffix),Path(folder.name)/('release'+suffix))
 builds.append(dict(name=folder.name,executableSHA256=digest(exe),assemblySHA256=digest(b/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll')))
pure=root/'LatestPureBuild4/Release';bee=json.loads(Path(str(pure/'WanxiangGuitu.exe')+'.bee.json').read_text(encoding='utf-8-sig'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig']
assert bee['Development'] is False and all(bee['Services'].get(k) is False for k in ['EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting'])
assert not any(re.search(r'BR2AllocationNative|NativeProbe|CP05BRProbe',f.name,re.I) for f in pure.rglob('*') if f.is_file())
(out/'build-identities.json').write_text(json.dumps(builds,indent=2),encoding='utf-8')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(out/'.gitattributes').write_text('* -text\n',encoding='utf-8')
print(len(manifest),'published artifacts;',len(builds),'build manifests; originals unmodified')
