"""Archive explicitly named ended B09 attempts via the existing redacting publisher."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--test-root',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--attempt',action='append',required=True,help='Label=relative-owned-run');a=p.parse_args()
if a.target.exists():raise ValueError('Fresh history directory required')
base=a.test_root.resolve(strict=True);records=[]
for spec in a.attempt:
 label,relative=spec.split('=',1);root=(base/relative).resolve(strict=True)
 if not root.is_relative_to(base) or Path(label).name!=label or not (root/'owner.json').exists():raise ValueError('Contained owned synthetic attempt required')
 rows=json.loads((root/'results.json').read_text(encoding='utf-8-sig'));rows=rows if isinstance(rows,list) else [rows]
 target=a.target/label
 subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('Publish-Evidence.py')),'--run',str(root),'--target',str(target)],check=True)
 sources=[]
 for f in sorted((root/'Project/Assets/CombatPrototype').rglob('*.cs')):
  raw=f.read_bytes();rel=Path('AttemptSources')/f.relative_to(root/'Project');rel=rel.with_name(rel.name+'.txt');out=target/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw);sources.append(dict(file=rel.as_posix(),sha256=hashlib.sha256(raw).hexdigest(),scope='End-of-attempt snapshot, never reused project; not a claim of current source equality'))
 (target/'attempt-sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 records.append(dict(label=label,root=str(root),results=[{k:r.get(k) for k in ['name','scope','status','exitCode','timedOut','reason']} for r in rows]))
(a.target/'attempts.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Archived distinct attempts:',len(records))
