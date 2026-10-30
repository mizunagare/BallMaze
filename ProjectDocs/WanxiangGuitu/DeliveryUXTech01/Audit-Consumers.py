from pathlib import Path
import re,json,hashlib,sys
repo=Path(sys.argv[1]);out=Path(sys.argv[2]);rows=[]
for p in sorted((repo/'Assets/CombatPrototype').rglob('*.cs')):
 if 'Editor' in p.parts:continue
 for line,text in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
  actions=re.findall(r'PlayerInput\.(Down|Held|Key|Cap)\(PlayerAction\.(\w+)\)',text)
  raw=bool(re.search(r'wasPressedThisFrame|EventType\.(KeyDown|MouseDown)|Mouse\.current\.delta|Keyboard\.current|Mouse\.current',text))
  if actions or raw or re.search(r'PlayerInput\.(Barrier|Focus|UIBlocked|DeviceEpoch)',text):
   rows.append(dict(path=p.relative_to(repo).as_posix(),line=line,actions=[dict(api=a,action=b) for a,b in actions],rawInputOrDeviceRead=raw,text=text))
result=dict(scope='Current runtime source only; includes display and raw pointer/reserved controls. A read is not automatically a bypass; DESIGN classifies actual consumers.',files=len(set(r['path'] for r in rows)),entries=rows)
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('runtime input/label files:',result['files'])
