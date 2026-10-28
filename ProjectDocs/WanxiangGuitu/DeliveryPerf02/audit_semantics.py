"""Exactly three readonly categories, preserving all 91 warnings as OPEN."""
import argparse,json,hashlib,re,collections
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();f=a.source/'ProjectDocs/WanxiangGuitu/DeliveryPerf01/Evidence/Run-1027-224456/WarningAudit/warnings.json';audit=json.loads(f.read_text(encoding='utf-8'));rows=[]
 for w in audit['warnings']:
  group='ObjectsByType-and-sort' if w['code']=='CS0618' and ('FindObjectsByType' in w['api'] or w['api']=='FindObjectsSortMode') else 'First-identity' if 'FindFirstObjectByType' in w['api'] else 'CS0414-lifecycle' if w['code']=='CS0414' else None
  if not group:continue
  b=(a.source/w['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==w['sourceSha256'];lines=b.decode('utf-8-sig').splitlines();n=w['line'];row=dict(id=w['id'],group=group,file=w['file'],line=n,column=w['column'],api=w['api'],sourceSha256=w['sourceSha256'],context=lines[max(0,n-4):n+4],originalRisk=w['risk'],state='OPEN / read-only semantics, no equivalence proof or migration')
  if group=='CS0414-lifecycle':
   name=w['api'].split('.')[-1];row['allWordReferences']=[dict(line=i+1,text=l.strip()) for i,l in enumerate(lines) if re.search(r'\b'+re.escape(name)+r'\b',l)]
  rows.append(row)
 assert len(rows)==89;out=dict(status='PASS',scope='Exactly 3 categories, 89 associated diagnostics; two scene diagnostics not reworked; all 91 remain OPEN',groups=dict(collections.Counter(x['group'] for x in rows)),rows=rows);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(out['groups'])
if __name__=='__main__':main()
