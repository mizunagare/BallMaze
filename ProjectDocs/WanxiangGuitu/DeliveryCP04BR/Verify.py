from pathlib import Path
import json,hashlib,re,gzip,collections
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR');r=Path('I:/WGCombat/CP04BR-1102-A');bad=[];manifest=json.loads((p/'Evidence/Raw/manifest.json').read_text())
for x in manifest:
 f=p/'Evidence/Raw'/x['path']
 if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=x['publishedSHA256']:bad.append('hash '+x['path'])
for f in p.rglob('*.md'):
 for link in re.findall(r'\]\(([^)]+)\)',f.read_text(encoding='utf8')):
  if not link.startswith(('http:','https:','#')) and not (f.parent/link.split('#')[0]).exists():bad.append(str(f.relative_to(p))+': '+link)
counts={}
for name,f in [('Editor',r/'FixedEditorCore/presentation.json'),('Player',r/'FixedPlayers/PlayerCore/presentation.json')]:
 j=json.loads(f.read_text());counts[name]=dict(collections.Counter(x['status'] for x in j['rows']))
 if counts[name]!={'PASS':293}:bad.append(name+' semantic mismatch')
if (r/'user-status-before.txt').read_text(encoding='utf8').strip()!=(r/'user-status-after.txt').read_text(encoding='utf8').strip():bad.append('user status changed')
pro=json.loads((r/'protection-after.json').read_text());assert pro['frozenExact'] and not pro['protected']['mismatches'] and not pro['history']['mismatches']
out={'status':'PASS' if not bad else 'FAIL','scope':'Publication hash/link/count consistency only, not overall acceptance','publishedFiles':len(manifest),'functional':counts,'errors':bad};(r/'consistency.json').write_text(json.dumps(out,indent=2));print(out);raise SystemExit(bool(bad))
