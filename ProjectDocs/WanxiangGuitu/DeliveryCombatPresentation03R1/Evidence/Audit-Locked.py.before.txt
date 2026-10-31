from pathlib import Path
import subprocess,hashlib,json,sys,math,csv
repo=Path(sys.argv[1]);root=Path(sys.argv[2]);base='c7efb644f38387f7588f4bd58fe5697e4ecdd9c4'
def original(p):return subprocess.check_output(['git','-C',str(repo),'show',base+':'+p])
def norm(b):return b.decode('utf-8-sig').replace('\r\n','\n').strip()
p='Assets/CombatPrototype/AdventureCombat.cs';current=norm((repo/p).read_bytes());old=norm(original(p))
for a,b in [('AttackTimed((int)type>=2,duration,skill)','AttackTimed((int)type>=2,duration)'),('AttackStarted(hero,type,skill)','AttackStarted(hero)'),('if((int)a.type>=2)feedback?.RangedRelease(hero,a.type);else feedback?.MeleeRelease(hero);','if((int)a.type>=2)feedback?.RangedRelease(hero);else feedback?.Swing(hero,a.type==GearType.Spear);')]:
 assert current.count(a)==1,a;current=current.replace(a,b)
current='\n'.join(x for x in current.splitlines() if 'CombatFeedback.Find(this)?.MeleeTrace(' not in x)
assert current==old,'Nonpresentation change in AdventureCombat'
locked=['CombatAim','CombatHealth','CombatEnemy','BossBrain','ForestBossBrain','ForestBossRules','ArmorMitigation','AdventureRandom','CombatSaveSystem','CombatSaveData','CatActorVisual','CombatSoundBank','OrbitCamera']
rows=[]
for n in locked:
 p='Assets/CombatPrototype/'+n+'.cs';b=(repo/p).read_bytes();o=original(p);assert norm(b)==norm(o),p;rows.append(dict(path=p,sha256=hashlib.sha256(b).hexdigest(),baselineCanonicalEqual=True))
# Ranged animation sampling code remains byte-for-byte except sword skill selection and cancellation feedback.
p='Assets/CombatPrototype/FantasyActorVisual.cs';c=norm((repo/p).read_bytes());o=norm(original(p));start=c.index('    void LateUpdate()');end=c.index('    void OnDestroy()');a=o.index('    void LateUpdate()');b=o.index('    void OnDestroy()');assert c[start:end]==o[a:b],'sampling clock changed'
def spawns(folder):return {(x['attack'],x['shot']):x for x in (json.loads(l) for l in (root/folder/'events.jsonl').read_text(encoding='utf-8-sig').splitlines()) if x['stage']=='spawn'}
a,b=spawns('Before2'),spawns('Final2');assert a.keys()<=b.keys();extra=[list(k) for k in b.keys()-a.keys()];origin=max(math.dist(list(a[k]['from'].values()),list(b[k]['from'].values())) for k in a);direction=max(math.dist(list(a[k]['aim'].values()),list(b[k]['aim'].values())) for k in a);assert origin==direction==0,'actual muzzle/aim changed'
(root/'locked-contract.json').write_text(json.dumps(dict(status='PASS',baseline=base,adventureCombatOnlyPresentationCalls=True,animationSamplingLoopUnchanged=True,lockedSources=rows,pairedActualSpawnCount=len(a),maxOriginDelta=origin,maxDirectionDelta=direction,additionalFinalSpawns=extra,note='Controlled paired events; zero deltas are measured, not substituted for missing performance data.'),indent=2),encoding='utf-8')
print('PASS: exact business code after stripping four presentation call changes; 13 locked sources; sampled loop unchanged;',len(a),'paired real spawns identical')
