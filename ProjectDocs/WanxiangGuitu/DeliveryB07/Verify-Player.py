"""Read-only B07 Player recovery assertions on explicit synthetic normal-adventure copies."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--badge',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve()
if not root.is_absolute() or 'locallow' in [s.lower() for s in root.parts]:raise ValueError('Explicit isolated root required')
for f in [a.before,a.after,a.output]:
 if not f.resolve().is_relative_to(root):raise ValueError('Evidence outside isolated root')
here=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('close_checks',here.parent/'DeliveryUI01/Tests/analyze-player-close.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def rows(path):
 envelope,data=m.payload(path);profile=data['profile'];run=data['activeRun'] if data.get('hasActiveRun') else None
 if run is None or run['mode']!=2 or run['checkpoint']['forest'].get('bossVersion')!=1:raise ValueError('B07 forest run not restored')
 if a.badge not in profile['badges']:raise ValueError('Previously earned badge missing')
 checkpoint=run['checkpoint'];loot=list(checkpoint.get('loot') or [])
 for page in checkpoint.get('groundLootPages') or []:
  digest=page['hash']
  if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('Invalid page ref')
  raw=(root/'WanxiangGuitu/ForestRuins/ground-loot'/(digest+'.json')).read_bytes()
  if len(raw)!=page['bytes'] or hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Invalid page integrity')
  items=json.loads(raw)['items']
  if len(items)!=page['count']:raise ValueError('Invalid page count')
  loot+=items
 bosses=sorted([(e['entityId'],e['health'],e['aiState']) for e in checkpoint['enemies'] if e['entityId'].startswith('boss:')])
 if len(bosses)!=2:raise ValueError('Two Boss entities absent')
 state=dict(profile=profile['profileId'],run=run['runId'],region=run['regionInstanceId'],seed=run['seed'],generation=run['generationVersion'],layout=m.digest(checkpoint['forest']),streams=run['randomStreams'],brought=run['broughtRemaining'],earned=run['earnedRemaining'],materials=checkpoint['materials'],potions=[run['broughtPotions'],run['earnedPotions']],gear=m.digest(sorted(checkpoint['gear'],key=lambda i:i['id'])),main=checkpoint['mainWeapon'],reserve=checkpoint['reserveWeapon'],warehouse=m.digest(sorted(profile['warehouse'],key=lambda i:i['id'])),warehouseMaterials=profile['materials'],recipes=profile['unlockedRecipes'],committed=profile['committedRuns'],badges=profile['badges'],regions=profile['regions'],hunts=profile.get('bossHunts'),bosses=bosses,events=sorted((e['entityId'],e['used']) for e in checkpoint['events']),resources=sorted((e['entityId'],e['health']) for e in checkpoint['resources']),ground=m.digest(sorted(loot,key=lambda l:l.get('entityId') or '')))
 return state
result={'scope':'Final non-development Player on actual normal-adventure-derived synthetic checkpoint. Background WM_CLOSE only; NOT native UI or Player combat victory.','before':rows(a.before),'after':rows(a.after)};result['passed']=result['before']==result['after'];a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'badge':a.badge}));raise SystemExit(0 if result['passed'] else 1)
