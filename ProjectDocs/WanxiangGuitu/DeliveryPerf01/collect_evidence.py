"""Closed-run only, lossless evidence copier. Does not upload binaries or user overlay bodies."""
import argparse,gzip,hashlib,json,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();r=a.root
 assert json.loads((r/'owner.json').read_text(encoding='utf-8-sig'))['kind']=='PERF-01 isolated measurements'
 assert (r/'recovery-complete.json').exists(),'Do not archive a live recovery'
 a.output.mkdir(parents=True,exist_ok=False);entries=[];excluded=[]
 def copy(f,rel):
  if not f.is_file():return
  out=a.output/rel;out.parent.mkdir(parents=True,exist_ok=True);size=f.stat().st_size;sourcehash=sha(f)
  # No filtering, rows or bytes are removed. Decompression is exactly source SHA256.
  compressed=(f.suffix.lower() in ('.csv','.log','.stdout') and size>32768)
  if compressed:
   out=out.with_name(out.name+'.gz')
   with f.open('rb') as src,out.open('wb') as dst:
    with gzip.GzipFile(filename='',mode='wb',fileobj=dst,mtime=0) as z:shutil.copyfileobj(src,z)
  else:shutil.copyfile(f,out)
  entries.append(dict(source=str(f.relative_to(r)),path=str(out.relative_to(a.output)).replace('\\','/'),rawBytes=size,rawSha256=sourcehash,encoding='gzip-lossless' if compressed else 'original',storedBytes=out.stat().st_size,storedSha256=sha(out)))
 for f in r.iterdir():
  if f.is_file():copy(f,Path(f.name))
 for folder in ('ReadOnlyAudit','WarningAudit','BuildProof','ToolVersions','AnalysisFinal','Runtime/System','Runtime/Cases','Runtime/WorkerSource'):
  p=r/folder
  if p.exists():
   for f in p.rglob('*'):
    if f.is_file():copy(f,f.relative_to(r))
 # Every original attempt command, host audit, actual exit, complete log and final synthetic save.
 # Large StorageAfter frames/screenshots duplicate Cases: retain an exact identity manifest,
 # and map identical bytes to canonical evidence. Nonidentical files are copied, never discarded.
 for d in (r/'Runtime/Attempts').iterdir():
  if not d.is_dir():continue
  for f in d.rglob('*'):
   if not f.is_file():continue
   if 'StorageAfter' in f.relative_to(d).parts:
    h=sha(f);match=next((x for x in entries if x['rawSha256']==h and x['rawBytes']==f.stat().st_size),None)
    if match:
     excluded.append(dict(source=str(f.relative_to(r)),rawBytes=f.stat().st_size,rawSha256=h,identicalCanonical=match['path']));continue
   copy(f,f.relative_to(r))
 for top in ('R','Runtime/T'):
  for b in (r/top).iterdir():
   if not b.is_dir():continue
   for f in b.iterdir():
    if f.is_file():copy(f,f.relative_to(r))
   if (b/'Results').exists():
    for f in (b/'Results').iterdir():
     if f.is_file():copy(f,f.relative_to(r))
   # Exact injected test-only source copies, but no original Assets/ProjectSettings bodies.
   for folder in ('InjectedSource','SourceCopies','ExecutedTools'):
    p=b/folder
    if p.exists():
     for f in p.rglob('*'):
      if f.is_file():copy(f,f.relative_to(r))
 (a.output/'MANIFEST.json').write_text(json.dumps(dict(toolSha256=sha(Path(__file__)),root=str(r),entries=entries,deduplicatedStorageAfter=excluded,excludedBodies=['Project','Library','Release binaries','user scene/settings/Recovery bodies'],note='gzip is lossless; duplicate StorageAfter bytes resolve via exact SHA256 to a canonical archived file'),ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(dict(files=len(entries),deduplicated=len(excluded),rawBytes=sum(x['rawBytes'] for x in entries),storedBytes=sum(x['storedBytes'] for x in entries))))
if __name__=='__main__':main()
