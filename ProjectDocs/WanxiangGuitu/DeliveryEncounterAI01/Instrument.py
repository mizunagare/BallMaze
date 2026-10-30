import pathlib,json,hashlib,sys
repo=pathlib.Path(sys.argv[1]);project=pathlib.Path(sys.argv[2]).resolve();out=pathlib.Path(sys.argv[3]).resolve()
if not str(project).lower().replace('\\','/').startswith('i:/wgcombat/eai01-') or not str(out).lower().replace('\\','/').startswith('i:/wgcombat/eai01-'):raise SystemExit('owned BAL01 clone required')
out.mkdir(parents=True,exist_ok=False);records=[]
for name in ['CombatEnemy','EnemyProjectile','ForestBossBrain']:
 p=project/f'Assets/CombatPrototype/{name}.cs';raw=p.read_bytes();text=raw.decode('utf-8-sig')
 if 'BAL01Trace' in text:raise SystemExit('already instrumented; restore product source first')
 (out/f'{name}.raw.cs').write_bytes(raw)
 if name=='CombatEnemy':
  text=text.replace('if(!HasAttackSlot(scheduled+flight))return;', 'if(!HasAttackSlot(scheduled+flight)){BAL01Trace.Deny(this);return;}')
  text=text.replace('lockedAim = target.transform.position + Vector3.up;','BAL01Trace.Begin(this);lockedAim = target.transform.position + Vector3.up;')
  text=text.replace('GetComponent<FantasyActorVisual>()?.Attack(archetype == EnemyArchetype.Ranged);','BAL01Trace.Release(this);GetComponent<FantasyActorVisual>()?.Attack(archetype == EnemyArchetype.Ranged);')
  text=text.replace('target.Health.Damage(damage, target.transform.position + Vector3.up, target.transform.position - transform.position);','BAL01Trace.Direct(this,target,damage,target.transform.position+Vector3.up,target.transform.position-transform.position);')
  text=text.replace('target.Progression.GainExperience(experienceReward);','BAL01Trace.Award(this,experienceReward);')
 elif name=='EnemyProjectile':
  text=text.replace('return shot;','BAL01Trace.Shot(shot,owner);return shot;')
  text=text.replace('hero.Health.Damage(Damage, hit.point, Velocity);','BAL01Trace.Projectile(this,hero,Damage,hit.point,Velocity);')
 else:
  text=text.replace('State=ForestBossState.Telegraph;hit=false;', 'State=ForestBossState.Telegraph;hit=false;BAL01Trace.Begin(enemy);')
  text=text.replace('HideHint();Releases++;','BAL01Trace.Release(enemy);HideHint();Releases++;')
  text=text.replace('enemy.target.Health.Damage(d.damage,enemy.target.transform.position+Vector3.up,direction);','BAL01Trace.Direct(enemy,enemy.target,d.damage,enemy.target.transform.position+Vector3.up,direction);')
  text=text.replace('enemy.target.Health.Damage(def.damage,enemy.target.transform.position+Vector3.up,direction);','BAL01Trace.Direct(enemy,enemy.target,def.damage,enemy.target.transform.position+Vector3.up,direction);')
 data=text.encode('utf-8');p.write_bytes(data);(out/f'{name}.observed.cs').write_bytes(data);records.append(dict(path=name,originalSHA256=hashlib.sha256(raw).hexdigest(),observedSHA256=hashlib.sha256(data).hexdigest()))
trace=(repo/'ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Instrumentation/BAL01Trace.cs.txt').read_bytes();(project/'Assets/CombatPrototype/BAL01Trace.cs').write_bytes(trace)
(out/'manifest.json').write_text(json.dumps(dict(scope='Isolated-only passive observation wrappers. Same original Damage/GainExperience call exactly once; no reward or state injection. Not shipping source.',files=records,traceSHA256=hashlib.sha256(trace).hexdigest()),indent=2),encoding='utf-8')
