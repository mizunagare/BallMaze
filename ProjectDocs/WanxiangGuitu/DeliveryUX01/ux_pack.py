"""UX01 preparation only. No player launch, input injection, game-state fabrication or human PASS oracle."""
import argparse,csv,hashlib,json,shutil,subprocess
from pathlib import Path,PureWindowsPath
from datetime import datetime,timezone

BASE='2caa2bb91c518078ea16c4230614eb2eb26034d9'
EXE='001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a'
ASSEMBLY='5da33f6ca959637f9dc46b7c92d4778da0fbc864129244d3805a67937573e65b'
TASKS=['标题进入或继续','装备与出征','移动转向和目标','指定武器普攻与技能','闪避与命中受击反馈','采集与背包','继续探索或合法撤离','回营仓库制造再次出征','改键提示实际操作及重启']
KEYS={'Forward':'W','Back':'S','Left':'A','Right':'D','Sprint':'LeftShift','Dodge':'Space','Attack':'MouseLeft','Skill':'F','SwitchWeapon':'V','Potion':'Q','Interact':'E','Exit':'H','Inventory':'Tab','Items':'B','Character':'C','Abandon':'R','Route':'M','Help':'F1','Rotate':'R'}
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def safe(p):
 p=Path(p)
 if not p.is_absolute() or any(x.lower()=='locallow' for x in p.parts):raise ValueError('Explicit external path outside real player LocalLow required')
 for x in [p,*p.parents]:
  if x.exists() and (x.is_symlink() or getattr(x,'is_junction',lambda:False)()):raise ValueError('Reparse path rejected')
 return p.resolve()
def files(p):
 rows=[]
 for x in sorted(p.rglob('*')):
  if x.is_symlink() or getattr(x,'is_junction',lambda:False)():raise ValueError('Reparse member refused: '+str(x))
  if x.is_file():rows.append(x)
 return rows
def inventory(p):return [dict(path=x.relative_to(p).as_posix(),bytes=x.stat().st_size,sha256=sha(x)) for x in files(p)]
def verify_tree(p,rows):
 if {x['path'] for x in rows}!={x.relative_to(p).as_posix() for x in files(p)}:raise ValueError('Tree membership differs: '+str(p))
 for x in rows:
  if sha(p/x['path']).lower()!=x['sha256'].lower():raise ValueError('Hash mismatch: '+x['path'])
def csv_template(p,fields,rows=()):
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def prepare(a):
 repo=safe(a.repo);root=safe(a.root);release=safe(a.release);fixture=safe(a.fixture)
 if root.exists() or root==repo or repo in root.parents:raise ValueError('Fresh external preparation root required')
 if subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()!=BASE:raise ValueError('Repository baseline advanced; do not reset')
 provenance=repo/'ProjectDocs/WanxiangGuitu/DeliveryCombat01R1/Evidence/Run-1028-112303'
 verify_tree(release,load(provenance/'Inputs/full-release-hashes.json'))
 if sha(release/'WanxiangGuitu.exe')!=EXE or sha(release/'WanxiangGuitu_Data/Managed/Assembly-CSharp.dll')!=ASSEMBLY:raise ValueError('Acceptance/unknown build refused')
 expected=load(provenance/'Inputs/source-files.json')
 if any(sha(repo/x['path']).upper()!=x['sha256'].upper() for x in expected):raise ValueError('Product or user overlay differs; inspect and re-authorize, never overwrite')
 env=load(fixture/'ForestRuins/save.json');payload=json.loads(env['payload'])
 if env['version']!=9 or hashlib.sha256(env['payload'].encode()).hexdigest().upper()!=env['checksum'].upper():raise ValueError('Invalid synthetic fixture')
 if payload['profile']['profileId']!='376aa5d5a11c4aa183824fac16c12383' or payload['activeRun']['runId']!='82032de5ba5e483ea8ef08629d51b2bf' or env['revision']!=6:raise ValueError('Only specifically reviewed synthetic exit fixture allowed; no real save ingestion')
 # Bind the ENTIRE save collection, including backups/journals/pages, to published runtime evidence.
 published=load(next((provenance/'Attempts').glob('113617-*/storage-after.json')))
 approved=[]
 for x in published:
  parts=PureWindowsPath(x['path']).parts
  if parts and parts[0]=='WanxiangGuitu':approved.append(dict(path=PureWindowsPath(*parts[1:]).as_posix(),bytes=x['bytes'],sha256=x['sha256']))
 verify_tree(fixture,approved)
 source_rows=[]
 for name in ['Assets','Packages','ProjectSettings']:
  source_rows += [dict(path=x.relative_to(repo).as_posix(),sha256=sha(x),bytes=x.stat().st_size) for x in files(repo/name)]
 changed=subprocess.check_output(['git','ls-files','--modified','--others','--exclude-standard'],cwd=repo,text=True).splitlines()
 protected=[dict(path=x,sha256=sha(repo/x)) for x in changed if (repo/x).is_file() and not x.startswith('ProjectDocs/') and x!='.gitattributes']
 root.mkdir(parents=True);write(root/'owner.json',dict(kind='UX01 preparation only',root=str(root),source=str(repo),repositoryBaseline=BASE,utc=now(),humanStatus='NOT_RUN'))
 shutil.copytree(release,root/'Release');shutil.copytree(fixture,root/'Golden/WanxiangGuitu')
 neutral=dict(version=1,width=1280,height=720,fullScreen=False,volume=1,sensitivity=.12,uiScale=1,bindingVersion=1,inputBindings=None)
 write(root/'Configuration/preferences.json',neutral)
 write(root/'release-files.json',inventory(root/'Release'));write(root/'fixture-files.json',inventory(root/'Golden/WanxiangGuitu'));write(root/'source-files.json',source_rows);write(root/'protected-inputs.json',protected)
 write(root/'version-lock.json',dict(repositoryBaseline=BASE,productBuildRecordedHead='d37b9ba98deea109fa67900314a2f6864b24c98a',productSourceReviewedCommit='be448f56cb629022047c5de35ca3bfb03eac7604',buildInput='COMBAT01 R2 working product changes plus existing user scene/settings overlays; 1152 exact hashes, not pure Git scene',variant='Release BuildOptions.None; no runtime driver',exeSha256=EXE,assemblySha256=ASSEMBLY,unity='6000.6.5f1',packages=dict(URP='17.6.0',InputSystem='1.20.0',uGUI='2.6.0'),graphics=dict(api='D3D11',width=1280,height=720,fullScreen=False,uiScale=1,qualityExpected='PC, Standalone index1 from frozen QualitySettings; operator must confirm actual conditions'),bindings=KEYS,fixture=dict(version=9,revision=env['revision'],profileId=payload['profile']['profileId'],runId=payload['activeRun']['runId'],seed=payload['activeRun']['seed'],source='Reviewed runtime acceptance-produced synthetic collection; NOT human evidence'),humanStatus='NOT_RUN',nativeU16='NOT_RUN'))
 return dict(status='PASS',scope='Package preparation/hash checks only',root=str(root),releaseFiles=len(files(root/'Release')),fixtureFiles=len(files(root/'Golden/WanxiangGuitu')),humanStatus='NOT_RUN')
def session(a):
 root=safe(a.root);o=load(root/'owner.json')
 if o['kind']!='UX01 preparation only':raise ValueError('Owned preparation required')
 if not a.session or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in a.session):raise ValueError('Safe unique session ID required')
 target=root/'Sessions'/a.session
 if target.exists():raise ValueError('Session exists; do not overwrite trials')
 verify_tree(root/'Release',load(root/'release-files.json'));verify_tree(root/'Golden/WanxiangGuitu',load(root/'fixture-files.json'))
 target.mkdir(parents=True);(target/'Storage').mkdir();(target/'Evidence').mkdir()
 if a.fixture=='continue':shutil.copytree(root/'Golden/WanxiangGuitu',target/'Storage/WanxiangGuitu')
 pref=target/'Storage/WanxiangGuitu/preferences.json'
 if pref.exists():raise ValueError('Unexpected fixture preferences; preserve and inspect')
 pref.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/'Configuration/preferences.json',pref)
 write(target/'session.json',dict(sessionId=a.session,packageRoot=str(root),storageRoot=str(target/'Storage'),weapon=a.weapon,fixture=a.fixture,participantId=None,observerId=None,priorExposure=None,independenceDeclared=False,consent=None,status='NOT_RUN',nativeUI='NOT_RUN',humanComprehension='NOT_RUN',observationSource=None,utc=now()))
 tasks=TASKS if a.fixture=='fresh' else ['从标题继续并辨认原有进度','核对随身装备物资与当前目标（不作为新手首遇）','改键后正常退出并重启继续同一局']
 csv_template(target/'tasks.csv',['taskId','objective','statusClaim','startUtc','endUtc','firstInput','attempts','repeats','assistance','interruption','participantUnderstanding','evidence','observerNotes'],[dict(taskId=f'T{i:02}',objective=n,statusClaim='NOT_RUN') for i,n in enumerate(tasks,1)])
 csv_template(target/'events.csv',['utc','taskId','eventType','actor','observedInput','observedFeedback','observedDamage','quote','evidence'])
 csv_template(target/'inventory.csv',['utc','taskId','profileId','runId','domain','itemOrMaterial','before','after','operation','sourceId','settlementState','evidence'])
 (target/'issues.md').write_text('# 缺陷记录（空白）\n\n每项填写：编号、分类、影响、步骤、首次失败、实际/预期、版本、证据、观察者提示、重试关联。不得删失败。\n',encoding='utf-8')
 write(target/'initial-storage-hashes.json',inventory(target/'Storage'))
 return dict(status='PASS',scope='Empty unassigned session prepared; no play performed',session=str(target),humanStatus='NOT_RUN')
def summarize(a):
 p=safe(a.session);s=load(p/'session.json');rows=list(csv.DictReader((p/'tasks.csv').open(encoding='utf-8-sig')));claimed=[x for x in rows if x['statusClaim'] not in ['', 'NOT_RUN']]
 return dict(scope='Record inventory, not a human acceptance oracle',sessionId=s['sessionId'],taskRecords=len(rows),nonEmptyClaims=len(claimed),evidenceReviewRequired=True,humanStatus='NOT_RUN' if not claimed else 'AWAITING_INDEPENDENT_REVIEW',nativeStatus='NOT_RUN' if not claimed else 'AWAITING_INDEPENDENT_REVIEW',automaticHumanPass=False)
def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True)
 q=sub.add_parser('prepare');q.add_argument('--repo',required=True);q.add_argument('--root',required=True);q.add_argument('--release',required=True);q.add_argument('--fixture',required=True)
 q=sub.add_parser('session');q.add_argument('--root',required=True);q.add_argument('--session',required=True);q.add_argument('--weapon',choices=['Sword','Spear','Staff','Bow'],required=True);q.add_argument('--fixture',choices=['fresh','continue'],required=True)
 q=sub.add_parser('summarize');q.add_argument('--session',required=True)
 a=p.parse_args();print(json.dumps(dict(prepare=prepare,session=session,summarize=summarize)[a.mode](a),ensure_ascii=False))
if __name__=='__main__':main()
