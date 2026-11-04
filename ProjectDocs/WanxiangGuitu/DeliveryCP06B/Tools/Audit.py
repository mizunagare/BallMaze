from pathlib import Path
import sys,json,hashlib,subprocess
repo=Path(__file__).resolve().parents[4];root=Path(sys.argv[1]);out=Path(sys.argv[2]);base='e1f13446601e4324a67c472eecd3419a6c317e65';checks=[]
def check(n,b,detail):checks.append(dict(name=n,status='PASS' if b else 'FAIL',detail=detail))
def old(f):return subprocess.check_output(['git','show',base+':'+f],cwd=repo).decode('utf-8-sig').replace('\r\n','\n')
def now(f):return (repo/f).read_text(encoding='utf-8-sig').replace('\r\n','\n')
allowed={'AdventureCombat.cs','AdventureFlow.cs','AdventureItems.cs','AdventureValidation.cs','CombatEnemy.cs','CombatHealth.cs','CombatSaveSystem.cs','FantasyActorVisual.cs','PlayerHudPresenter.cs','WeaponSkillExpansion.cs','WeaponSkillPanel.cs','WeaponTraits.cs','CombatFeedback.cs','CombatSoundBank.cs','CatDropVisual.cs'}
protected=json.loads((root/'protected-before.json').read_text(encoding='utf-8-sig'));changed=[]
for row in protected:
 f=Path(row['path']);value=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else 'MISSING'
 if value!=row['sha256']:changed.append(dict(path=str(f),before=row['sha256'],after=value,authorized=f.parent==repo/'Assets/CombatPrototype' and f.name in allowed))
check('original-user-and-locked-inputs',all(x['authorized'] for x in changed),{'protected':len(protected),'changed':changed})
for name in ['CombatAim.cs','TargetAssist.cs','OrbitCamera.cs','CameraActorFade.cs','AdventureRandom.cs','CP05Training.cs','TrainingLootContext.cs','AdventureState.cs','AdventureFlow.Supplies.cs']:
 f='Assets/CombatPrototype/'+name;check('locked-'+name,old(f)==now(f),'Full normalized text equality; SHA of raw source recorded in input manifest')
f='Assets/CombatPrototype/CombatSoundBank.cs';s=old(f);patches=[('new AudioClip[7]','new AudioClip[10]'),('.65f, .5f };','.65f, .5f, .13f, .45f, .32f };'),('else value = (.65f','else if(cue>=7){float hz=cue==7?1200:cue==8?90:330;value=(Mathf.Sin(2*Mathf.PI*hz*t)*.3f+low*.65f+high*(cue==7?.3f:.08f))*Mathf.Sin(Mathf.PI*u)*Mathf.Exp(-2*u); }\n                else value = (.65f')]
# Exact branch text below retains the first seven sound generators and seeds.
patches[2]=(patches[2][0],patches[2][1].replace('*Mathf.Exp(-2*u); }','*Mathf.Exp(-2*u);}'))
for a,b in patches:
 check('sound-patch-location-'+a,s.count(a)==1,'exact one replacement');s=s.replace(a,b)
check('legacy-seven-sounds',s==now(f),'Only append three clip types; first seven remain exact')
for f in (repo/'ProjectDocs/WanxiangGuitu/DeliveryCP06B/Tests').glob('NW*.cs.txt'):
 if f.name=='NWMigration.cs.txt':continue
 s=f.read_text(encoding='utf-8');bad=[k for k in ['.Damage(','.ResetHealth(','.RestoreHealth(','.maxHealth =','.damage ='] if k in s];check('no-fake-hit-'+f.name,not bad,bad)
profile='Assets/BuildProfiles/WindowsRelease.asset';check('privacy-profile',old(profile)==now(profile),'fixed existing release profile unchanged')
status='FAIL' if any(c['status']=='FAIL' for c in checks) else 'PASS';out.write_text(json.dumps(dict(status=status,baseline=base,checks=checks),indent=2,ensure_ascii=False),encoding='utf-8');print(status,len(checks));sys.exit(status=='FAIL')
