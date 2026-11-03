from pathlib import Path
import json,hashlib,gzip,re,sys
stage=sys.argv[1];r=Path('I:/WGCombat/CP05B-1103-A')/stage;out=Path('ProjectDocs/WanxiangGuitu/DeliveryCP05B/Evidence')/stage;out.mkdir(parents=True,exist_ok=False);rows=[]
def publish(f,rel):
 data=f.read_bytes();payload=data;red=False
 if f.suffix.lower() in ['.json','.jsonl','.log','.stdout','.stderr','.txt']:
  text=data.decode('utf-8-sig');clean=re.sub(r'(?i)(access[_ ]?token\s*:\s*)"[^"]*"',r'\1"[REDACTED]"',text);clean=re.sub(r'LicenseClient-[\w-]+','LicenseClient-[REDACTED]',clean);clean=re.sub(r'(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s"<>]+','[USERPROFILE]',clean);red=clean!=text;payload=clean.encode('utf8') if red else data
 if f.suffix.lower() in ['.log','.stdout','.stderr','.jsonl']:payload=gzip.compress(payload,mtime=0);rel=rel.with_name(rel.name+'.gz')
 p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(payload);rows.append({'path':rel.as_posix(),'originalRelative':str(f.relative_to(r)),'sourceSHA256':hashlib.sha256(data).hexdigest(),'publishedSHA256':hashlib.sha256(payload).hexdigest(),'redacted':red})
for folder in r.iterdir():
 if not folder.is_dir() or folder.name in ['Project','Project2']:continue
 for f in folder.glob('*'):
  if f.is_file() and f.suffix.lower() in ['.json','.jsonl','.log','.stdout','.stderr','.png']:publish(f,f.relative_to(r))
 for clip in folder.glob('clip-*'):
  for f in clip.glob('*'):
   if f.is_file() and f.suffix in ['.png','.jsonl']:publish(f,f.relative_to(r))
build=sys.argv[2];exe=r/build/'Release/WanxiangGuitu.exe';files=[{'path':f.relative_to(exe.parent).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in exe.parent.rglob('*') if f.is_file()];(out/'release-files.json').write_text(json.dumps(files,indent=2),encoding='utf8');publish(Path(str(exe)+'.release.json'),Path('release-marker.json'));publish(Path(str(exe)+'.summary.txt'),Path('build-summary.txt'));c=json.loads(Path(str(exe)+'.bee.json').read_text(encoding='utf8'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig'];assert c['Development'] is False
assert all(c['Services'][k] is False for k in ['EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting']);(out/'bee.json').write_text(json.dumps(c,indent=2),encoding='utf8');(out/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(stage,len(rows),'raw artifacts')
