from pathlib import Path
import json,hashlib,re,sys
repo=Path(sys.argv[1]);out=Path(sys.argv[2]);rows=[]
for p in sorted((repo/'Assets').rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(repo).as_posix()
 if p.suffix.lower() in {'.anim','.wav','.ogg','.mp3'} or any(t in rel for t in ('Resources/CombatFeedback/','Resources/CatWorld/Actors/')) and p.suffix in {'.prefab','.mat','.asset','.shader'}:
  b=p.read_bytes();text=b.decode('utf-8-sig',errors='replace') if p.suffix in {'.anim','.prefab','.mat','.shader'} else ''
  rows.append(dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),name=re.findall(r'^\s*m_Name: (.*)',text,re.M)[:1],animationEvents=re.findall(r'^\s*m_Events: (.*)',text,re.M)[:1]))
calls=[]
for p in (repo/'Assets/CombatPrototype').rglob('*.cs'):
 if 'Editor' in p.parts:continue
 for n,t in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
  if re.search(r'CombatFeedback|AttackTimed|\.Hurt\(|\.Recoil\(|BossWarningGeometry|\.Damage\(|\.Shake\(',t):calls.append(dict(path=p.relative_to(repo).as_posix(),line=n,source=t))
out.write_text(json.dumps(dict(assets=rows,calls=calls,note='Static inventory; clip runtime availability checked separately. Audio bank generated at runtime; no recording asset invented.'),ensure_ascii=False,indent=2),encoding='utf-8');print(len(rows),'assets;',len(calls),'event call sites')
