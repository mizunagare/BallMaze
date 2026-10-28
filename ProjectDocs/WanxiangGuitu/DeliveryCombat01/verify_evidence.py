"""Verify published bytes and compressed raw logs without the original machine/run directory."""
import argparse,gzip,hashlib,json
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('evidence',type=Path);a=p.parse_args();root=a.evidence
 manifest=json.loads((root/'manifest.json').read_text());checked=0
 for x in manifest:
  file=root/x['path'];b=file.read_bytes();assert sha(b)==x['publishedSha256'],str(file)
  raw=gzip.decompress(b) if file.name.endswith('.log.gz') else b
  assert sha(raw)==x['sourceSha256'],str(file)+' raw hash';checked+=1
 analysis=json.loads((root/'analysis.json').read_text())
 assert len(analysis['changes'])==4
 assert all(x['before'].upper()==x['after'].upper() for x in analysis['protectedInputs'])
 assert analysis['finalControlledCounts']==dict(PASS=188,FAIL=0)
 fixed=[x for x in analysis['comparison'] if x['before']=='FAIL'];assert len(fixed)==33
 assert all(x['after']=='PASS' for x in fixed)
 assert all(x['matchesCurrentProductInputs'] for x in analysis['buildProof'])
 print(json.dumps(dict(status='PASS',publishedFiles=checked,protectedInputs=len(analysis['protectedInputs']),oldFailConditionsNowPassing=len(fixed),productChanges=len(analysis['changes']))))
if __name__=='__main__':main()
