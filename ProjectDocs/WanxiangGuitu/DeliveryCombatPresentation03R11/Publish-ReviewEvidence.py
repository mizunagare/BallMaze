"""Publish only owned synthetic CP03-R1 evidence. Originals remain untouched."""
import argparse,gzip,hashlib,json,re
from pathlib import Path

def main():
    a=argparse.ArgumentParser();a.add_argument('root',type=Path);a.add_argument('output',type=Path);o=a.parse_args()
    root=o.root.resolve();out=o.output.resolve()
    if not str(root).lower().replace('\\','/').startswith('i:/wgcombat/cp03-r1-') or not (root/'owner.json').is_file():raise ValueError('owned R1 root required')
    out.mkdir(exist_ok=False);manifest=[]
    for f in sorted(root.rglob('*')):
        if not f.is_file():continue
        rel=f.relative_to(root)
        if any(x in ('P','Library','Release','__pycache__') for x in rel.parts):continue
        if f.suffix.lower() not in ('.json','.jsonl','.csv','.md','.txt','.log','.stdout','.stderr','.ps1','.cs','.py'):continue
        raw=f.read_bytes();data=raw;redacted=False
        if f.suffix.lower() in ('.log','.stdout','.stderr','.jsonl'):
            text=raw.decode('utf-8-sig')
            cleaned=re.sub(r'(?i)((?:access[_ ]?token|authorization|client[_ ]?secret)\s*[:=]\s*)(?:Bearer\s+)?(?:"[^"\r\n]*"|[A-Za-z0-9._/+\-=]{8,})',r'\1[REDACTED_CREDENTIAL]',text)
            redacted=text!=cleaned;data=gzip.compress(cleaned.encode('utf-8'),mtime=0);rel=rel.with_name(rel.name+'.gz')
        target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        manifest.append(dict(path=rel.as_posix(),sourceRelative=f.relative_to(root).as_posix(),sourceSHA256=hashlib.sha256(raw).hexdigest(),publishedSHA256=hashlib.sha256(data).hexdigest(),bytes=len(data),credentialValuesRedacted=redacted))
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(len(manifest),'artifacts')
if __name__=='__main__':main()
