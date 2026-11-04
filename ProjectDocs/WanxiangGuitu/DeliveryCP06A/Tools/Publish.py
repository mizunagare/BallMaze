from pathlib import Path
import json,hashlib,gzip,re
root=Path('I:/WGCombat/CP06A-1104-A');out=Path(__file__).resolve().parents[1]/'Evidence';out.mkdir(exist_ok=False);manifest=[]
def publish(f,rel):
 raw=f.read_bytes();payload=raw;redacted=False;encoding='binary';transcoded=False
 if f.suffix.lower() in ('.json','.jsonl','.log','.stdout','.stderr','.txt','.ps1','.cs'):
  encoding='utf-8-sig'
  try:text=raw.decode(encoding)
  except UnicodeDecodeError:
   if f.name not in ('hardware.json','window-tool-capability.json'):raise
   encoding='gbk';text=raw.decode(encoding);json.loads(text);transcoded=True
  clean=re.sub(r'(?i)(access[_ ]?token\s*:\s*)"[^"]*"',r'\1"[REDACTED]"',text);clean=re.sub(r'LicenseClient-[\w-]+','LicenseClient-[REDACTED]',clean);clean=re.sub(r'(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s"<>]+','[USERPROFILE]',clean);redacted=clean!=text;payload=clean.encode('utf8') if redacted or transcoded else raw
 if f.suffix.lower() in ('.log','.stdout','.stderr','.jsonl'):payload=gzip.compress(payload,mtime=0);rel=rel.with_name(rel.name+'.gz')
 p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(payload);manifest.append({'path':rel.as_posix(),'sourceRelative':f.relative_to(root).as_posix(),'sourceSHA256':hashlib.sha256(raw).hexdigest(),'publishedSHA256':hashlib.sha256(payload).hexdigest(),'redacted':redacted,'sourceEncoding':encoding,'transcodedUTF8':transcoded})
for folder in root.iterdir():
 if not folder.is_dir() or folder.name=='Project':continue
 for f in folder.rglob('*'):
  if not f.is_file() or 'Release' in f.relative_to(folder).parts or 'PartialEvidence' in f.relative_to(folder).parts:continue
  if f.suffix.lower() in ('.json','.jsonl','.log','.stdout','.stderr','.png','.cs','.txt','.ps1') or '.executed' in f.name:publish(f,f.relative_to(root))
for f in root.glob('*.json'):publish(f,f.relative_to(root))
for name in ('BeforeBuild','TestBuild'):
 for suffix in ('.release.json','.summary.txt','.bee.json'):publish(root/name/'Release'/('WanxiangGuitu.exe'+suffix),Path(name)/('release'+suffix))
build=root/'PureBuild/Release';exe=build/'WanxiangGuitu.exe'
files=[{'path':f.relative_to(build).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in build.rglob('*') if f.is_file()]
(out/'release-files.json').write_text(json.dumps(files,indent=2),encoding='utf8')
for suffix in ('.release.json','.summary.txt','.bee.json'):publish(Path(str(exe)+suffix),Path('PureBuild/release'+suffix))
bee=json.loads(Path(str(exe)+'.bee.json').read_text(encoding='utf8'))['PlayerBuildProgramLibrary.Data.PlayerBuildConfig'];assert bee['Development'] is False and all(bee['Services'][k] is False for k in ['EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting'])
foreign=[f['path'] for f in files if re.search(r'BR2AllocationNative|NativeProbe|CP05BRProbe',f['path'],re.I)];assert not foreign
(out/'release-identity.json').write_text(json.dumps({'executableSHA256':hashlib.sha256(exe.read_bytes()).hexdigest(),'assemblySHA256':hashlib.sha256((build/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll').read_bytes()).hexdigest(),'Development':False,'services':bee['Services'],'forbiddenNativeFiles':foreign},indent=2),encoding='utf8')
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');print(len(manifest),'published artifacts, no original modified')
