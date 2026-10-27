"""Verify and reconstruct archived raw diagnostics into a new external analysis-only root."""
import argparse,gzip,hashlib,json
from pathlib import Path
def h(raw):return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();repo=Path(__file__).resolve().parents[3];dest=a.output.resolve()
 if dest==repo or repo in dest.parents or 'locallow' in str(dest).lower():raise ValueError('External analysis-only output required')
 a.output.mkdir(parents=True,exist_ok=False);m=json.loads((a.archive/'MANIFEST.json').read_text(encoding='utf-8'));restored=0
 for e in m['entries']:
  source=e['source'].replace('\\','/');relative=Path(source)
  if relative.is_absolute() or '..' in relative.parts:raise ValueError('Invalid manifest path')
  data=(a.archive/e['path']).read_bytes();assert h(data)==e['storedSha256'] and len(data)==e['storedBytes']
  raw=gzip.decompress(data) if e['encoding']=='gzip-lossless' else data;assert h(raw)==e['rawSha256'] and len(raw)==e['rawBytes']
  out=a.output/relative;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);restored+=1
 # Canonical deduplication preserves the exact original synthetic StorageAfter bytes.
 for e in m['deduplicatedStorageAfter']:
  canonical=next(x for x in m['entries'] if x['path']==e['identicalCanonical']);data=(a.archive/canonical['path']).read_bytes();raw=gzip.decompress(data) if canonical['encoding']=='gzip-lossless' else data
  assert h(raw)==e['rawSha256'];out=a.output/Path(e['source'].replace('\\','/'));out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);restored+=1
 print(json.dumps(dict(status='PASS',restored=restored,scope='Exact raw hash reconstruction, not a new Player run or a new performance pass')))
if __name__=='__main__':main()
