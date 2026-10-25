"""Compare synthetic B08 Player launch/exit snapshots; no UI/combat claim."""
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
def load(path):return json.loads(json.loads(path.read_text(encoding='utf-8-sig'))['payload'])
b,c=load(a.before),load(a.after)
def identity(v):
 r=v['activeRun'];f=v['profile'];w=r['checkpoint']
 return dict(profile=f['profileId'],hasTutorial=f['hasTutorial'],tutorial=f['tutorial'],run=r['runId'],region=r['regionInstanceId'],seed=r['seed'],streams=r['randomStreams'],layout=w['forest'],brought=r['broughtRemaining'],earned=r['earnedRemaining'],gear=sorted(g['id'] for g in w['gear']),warehouse=sorted(g['id'] for g in f['warehouse']),materials=f['materials'],recipes=f['unlockedRecipes'],badges=f['badges'])
same=identity(b)==identity(c);t=c['profile']['tutorial'];ok=same and c['profile']['hasTutorial'] and t['stage']==12 and not t['enabled'] and c['activeRun']['mode']==2 and c['activeRun']['runId']!=t['firstRunId'] and t['firstRunId'] in c['profile']['committedRuns']
if a.output.exists():raise ValueError('Fresh output required')
a.output.write_text(json.dumps(dict(status='PASS' if ok else 'FAIL',scope='Final nondevelopment Player startup/exit and restore of actual normal tutorial successor; not native UI',sameIdentityAndTutorial=same,stage=t['stage'],enabled=t['enabled'],run=c['activeRun']['runId'],profile=c['profile']['profileId'],beforeRevision=b['revision'],afterRevision=c['revision']),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
raise SystemExit(0 if ok else 1)
