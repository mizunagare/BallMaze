from pathlib import Path
import json,csv,collections,hashlib,sys
r=Path(sys.argv[1]);selected=['RulesFull10','FullEditorFinal1','FullPlayer1','ResumeEditor1','ResumePlayer1','FrontierResumeEditor1','FrontierResumePlayer1','EliteEditor3','ElitePlayer2','BossEditor2','BossPlayer1','DeathEditor3','DeathPlayer2','FaultEditor2','FaultPlayer1','BossResumeEditor1','BossResumePlayer1','CampPrepareEditor1','CampPreparePlayer1']
for weapon in ['Sword','Spear','Staff','Bow','Twin','Great','Scythe']:
 n=3 if weapon in ['Twin','Great','Scythe'] else 2
 selected += [f'WeaponEditor{weapon}{n}',f'WeaponPlayer{weapon}{n}']
final='--final' in sys.argv
if final:selected+=['AssistEditor1','AssistPlayer1']
def load(p):return json.loads(p.read_text('utf-8-sig'))
def result(folder):
 p=folder/'process.json';process=load(p) if p.exists() else {};f=next((folder/n for n in ['probe.json','rules.json'] if (folder/n).exists()),None);data=load(f) if f else {};rows=data.get('rows',[]);counts=collections.Counter(x.get('status','MISSING') for x in rows)
 invalid=not rows or any(x not in ['PASS','FAIL','NOT_RUN','UNRESOLVED'] for x in counts)
 status='INCOMPLETE' if invalid or process.get('exited') is not True or process.get('timedOut') is not False or process.get('exitCode') is None else 'FAIL' if counts['FAIL'] or process['exitCode']!=0 else 'BLOCKED' if counts['UNRESOLVED'] else 'INCOMPLETE' if counts['NOT_RUN'] else 'PASS'
 return dict(case=folder.name,layer=data.get('layer','Editor rules'),mode=data.get('mode','rules'),process=process,status=status,counts=dict(counts),failures=[dict(index=i,**x) for i,x in enumerate(rows) if x.get('status')!='PASS'],receipt=f.name if f else None)
current=[result(r/n) for n in selected];hist=[result(f) for f in sorted(r.iterdir()) if f.is_dir() and any((f/n).exists() for n in ['probe.json','rules.json']) and f.name not in selected];totals=collections.defaultdict(collections.Counter)
for x in current:totals[x['layer']].update(x['counts'])
identities=[]
for name in selected:
 folder=r/name;save=folder/'WanxiangGuitu/ForestRuins/save.json'
 if not save.exists():continue
 env=load(save);payload=env['payload'];assert hashlib.sha256(payload.encode('utf-8')).hexdigest().upper()==env['checksum'].upper(), 'Actual save checksum '+name
 body=json.loads(payload);run=body.get('activeRun');e=load(folder/'expected.json') if (folder/'expected.json').exists() else None
 identities.append(dict(case=name,saveSHA256=hashlib.sha256(save.read_bytes()).hexdigest(),profileId=body.get('profile',{}).get('profileId'),runId=run.get('runId') if run else None,seed=run.get('seed') if run else None,region=run.get('region') if run else None,regionInstanceId=run.get('regionInstanceId') if run else None,content=run.get('contentRevision') if run else None,generationVersion=run.get('generationVersion') if run else None,expectedSavedRun=e.get('run') if e else None,note='Final snapshot may be next Run after successful settlement; expected.json binds the restored original Run.'))
summary=dict(scope='Current frozen-product actual runs, selected latest valid fixture cases. Repeated assertions/steps are not independent gameplay features; old FAIL retained below.',current=current,currentByLayer={k:dict(v) for k,v in totals.items()},history=hist,allCurrentPass=all(x['status']=='PASS' for x in current),caseInputs=identities)
(r/('validation-summary-final.json' if final else 'validation-summary.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2),'utf-8');print('current',len(current),dict(summary['currentByLayer']));print('failed current',[x['case'] for x in current if x['status']!='PASS'])
with (r/('warning-index-final.csv' if final else 'warning-index.csv')).open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f);w.writerow(['source','line','text'])
 for folder in sorted(r.iterdir()):
  if not folder.is_dir():continue
  for name in ['Unity.log','Player.log']:
   path=folder/name
   if not path.exists():continue
   for i,line in enumerate(path.read_text('utf-8-sig',errors='replace').splitlines(),1):
    if any(k in line.lower() for k in ['warning','jobtempalloc','error cs','argumentoutofrangeexception','searchdatabase']):w.writerow([path.relative_to(r).as_posix(),i,line])
assert summary['allCurrentPass'],'Current acceptance is not all PASS'
