"""Read-only protection check against the complete pre-run product input manifest."""
import argparse,hashlib,json,subprocess
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--root',type=Path,required=True);a=p.parse_args();before=json.loads((a.root/'ReadOnlyAudit/source-files.json').read_text(encoding='utf-8-sig'));changed=[]
 for e in before:
  f=a.source/e['path'];actual=hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None
  if actual!=e['sha256']:changed.append(dict(path=e['path'],before=e['sha256'],after=actual))
 old={e['path'] for e in before};now={f.relative_to(a.source).as_posix() for folder in ['Assets','Packages','ProjectSettings'] for f in (a.source/folder).rglob('*') if f.is_file()};added=sorted(now-old)
 out=dict(status='PASS' if not changed and not added else 'FAIL',checked=len(before),changed=changed,added=added,head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.source,text=True).strip(),statusText=subprocess.check_output(['git','status','--porcelain'],cwd=a.source,text=True),scope='All pre-run Assets/Packages/ProjectSettings bytes unchanged, including user overlay; no source bodies copied to Git evidence')
 (a.root/'source-protection.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(dict(status=out['status'],checked=len(before),changed=len(changed),added=len(added))))
 if out['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
