"""Read-only CP05 protection and source contract audit; no writes to product inputs."""
from pathlib import Path
import hashlib,json,subprocess,sys
repo=Path(__file__).resolve().parents[4]
root=Path('I:/WGCombat/CP05B-1103-A')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((root/'protected-before.json').read_text(encoding='utf-8-sig'))
allowed={'Assets/CombatPrototype/'+s+'.cs' for s in ('AdventureCombat','OrbitCamera','CameraActorFade')}
changed=[];missing=[];errors=[]
for row in before:
 p=Path(row['path'])
 if not p.is_file():missing.append(str(p));continue
 if sha(p)!=row['sha256']:
  rel=p.relative_to(repo).as_posix() if p.is_relative_to(repo) else None
  changed.append({'path':str(p),'relative':rel,'before':row['sha256'],'after':sha(p)})
  if rel not in allowed:errors.append('Unexpected protected change: '+str(p))
errors+=['Missing: '+p for p in missing]
base='c6473b1832a545a5d348e26220fafa73cca741ac'
def old(path):return subprocess.check_output(['git','show',base+':'+path],cwd=repo).decode('utf8').replace('\r\n','\n')
def body(text,head):
 start=text.index(head);i=text.index('{',start);depth=1;j=i+1
 while depth:
  depth+=(text[j]=='{')-(text[j]=='}');j+=1
 return text[start:j]
path='Assets/CombatPrototype/AdventureCombat.cs';a=old(path);b=(repo/path).read_text(encoding='utf-8-sig')
checks=[]
for head in ('public static class MeleeGeometry','public static float ActionDuration','void AdvanceAttacks()','void Fire(','bool Sight(','public class AdventureProjectile'):
 try:ok=body(a,head)==body(b,head)
 except ValueError:ok=False
 checks.append({'name':head,'pass':ok})
# Exact known adapter/facing changes removed only from Release; all original branches remain.
release=body(b,'void Release(AttackAction a)')
addition='        if(a.type<GearType.Staff){if(CombatAssistOptions.Melee&&a.assistedFacing&&hero.MoveDirection.sqrMagnitude<=.01f)transform.rotation=a.facing;LastMeleeFacing=transform.forward;LastMeleeTrackedDegrees=a.trackedDegrees;}\n'
assert release.count(addition)==1
release=release.replace(addition,'')
assert release.count('aim=SolveRanged(speed*2.5f)')==1
release=release.replace('aim=SolveRanged(speed*2.5f)','aim=CombatAim.Solve(hero,MuzzlePosition,MuzzleSource,speed*2.5f)')
checks.append({'name':'Release original branch body after two exact additions removed','pass':release==body(a,'void Release(AttackAction a)')})
for c in checks:
 if not c['pass']:errors.append('Source contract check: '+c['name'])
aim=repo/'Assets/CombatPrototype/CombatAim.cs'
if sha(aim)!='9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a':errors.append('CombatAim changed')
report={'baseline':base,'protectedCount':len(before),'changed':changed,'missing':missing,'sourceChecks':checks,'CombatAimSHA256':sha(aim),'errors':errors,'status':'FAIL' if errors else 'PASS'}
out=Path(sys.argv[1]);out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))

