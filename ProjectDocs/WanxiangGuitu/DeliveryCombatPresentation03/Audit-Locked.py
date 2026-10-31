"""Exact presentation-only contract audit; fails closed. No broad line stripping."""
from pathlib import Path
import subprocess,hashlib,json,sys,math
BASE='c7efb644f38387f7588f4bd58fe5697e4ecdd9c4'
LOCKED=('CombatAim','CombatHealth','CombatEnemy','BossBrain','ForestBossBrain','ForestBossRules','ArmorMitigation','AdventureRandom','CombatSaveSystem','CombatSaveData','CatActorVisual','CombatSoundBank','OrbitCamera')
class AuditError(ValueError): pass

def need(ok,message):
    if not ok: raise AuditError(message)
def norm(b): return b.decode('utf-8-sig').replace('\r\n','\n')
def original(repo,p): return norm(subprocess.check_output(['git','-C',str(repo),'show',BASE+':'+p]))

def adventure(old,current):
    changes=[
      ('BeginAttack','        GetComponent<FantasyActorVisual>()?.AttackTimed((int)type>=2,duration);','        GetComponent<FantasyActorVisual>()?.AttackTimed((int)type>=2,duration,skill);'),
      ('BeginAttack','        CombatFeedback.Find(this)?.AttackStarted(hero);','        CombatFeedback.Find(this)?.AttackStarted(hero,type,skill);'),
      ('Release','        if((int)a.type>=2)feedback?.RangedRelease(hero);else feedback?.Swing(hero,a.type==GearType.Spear);','        if((int)a.type>=2)feedback?.RangedRelease(hero,a.type);else feedback?.MeleeRelease(hero);'),
      ('Melee','        AdventurePulse.SpawnMelee(transform,radius,dot,a.type==GearType.Spear?width:float.PositiveInfinity,new Color(.9f,.7f,.25f));','        AdventurePulse.SpawnMelee(transform,radius,dot,a.type==GearType.Spear?width:float.PositiveInfinity,new Color(.9f,.7f,.25f));\n        CombatFeedback.Find(this)?.MeleeTrace(hero,a.type,radius,dot,a.type==GearType.Spear?width:float.PositiveInfinity);')]
    expected=old;report=[]
    for method,before,after in changes:
        need(expected.splitlines().count(before)==1,'baseline anchor count '+method+': '+before)
        need(expected.count(before+'\n')==1,'baseline exact line '+method)
        expected=expected.replace(before+'\n',after+'\n',1)
        report.append(dict(method=method,before=before,after=after,expectedOccurrences=1))
    need(current==expected,'AdventureCombat differs outside the four exact anchored presentation edits')
    need(current.count('?.MeleeTrace(')==1,'exactly one MeleeTrace call required')
    for item in report: item['finalLine']=current[:current.index(item['after'])].count('\n')+1
    return report

def sampling(old,current):
    start='    void LateUpdate()';end='    void OnDestroy() { if (weaponTint != null) Destroy(weaponTint); if (shieldTint != null) Destroy(shieldTint); }'
    for text in (old,current):
        need(text.splitlines().count(start)==1 and text.splitlines().count(end)==1,'sampling method markers must each be unique')
        need(text.index(start)<text.index(end),'sampling method order')
    a=old[old.index(start):old.index(end)];b=current[current.index(start):current.index(end)]
    need(a==b,'animation sampling region changed')
    return dict(sha256=hashlib.sha256(b.encode()).hexdigest(),firstLine=current[:current.index(start)].count('\n')+1,bytes=len(b.encode()))

def spawns(path):
    result={}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        x=json.loads(line)
        if x.get('stage')!='spawn': continue
        key=(x.get('attack'),x.get('shot'))
        need(all(type(v) is int and v>0 for v in key),'invalid attack/shot identity')
        need(key not in result,'duplicate spawn identity '+str(key))
        for name in ('from','aim'):
            v=x.get(name);need(isinstance(v,dict) and set(v)=={'x','y','z'},'invalid xyz '+name)
            need(all(type(v[k]) in (int,float) and math.isfinite(v[k]) for k in ('x','y','z')),'nonfinite vector')
        result[key]=x
    return result

def paired(a,b):
    need(len(a)==24,'baseline must contain exactly 24 real paired spawns')
    need(set(a)<=set(b),'missing final spawn identity')
    need(set(b)-set(a)=={(59,1)},'only separately documented pause-arrow (59,1) may be additional')
    rows=[]
    for key in sorted(a):
        # Explicit xyz ordering: JSON dictionary insertion order is not geometry.
        for name in ('from','aim'):
            need(a[key][name]==b[key][name],'actual '+name+' changed at '+str(key))
        rows.append(dict(attack=key[0],shot=key[1],origin=a[key]['from'],direction=a[key]['aim'],originDelta=0,directionDelta=0))
    return rows

def audit(repo,root):
    p='Assets/CombatPrototype/AdventureCombat.cs';changes=adventure(original(repo,p),norm((repo/p).read_bytes()))
    rows=[]
    for n in LOCKED:
        p='Assets/CombatPrototype/'+n+'.cs';raw=(repo/p).read_bytes();need(norm(raw)==original(repo,p),'locked source changed: '+p)
        rows.append(dict(path=p,sha256=hashlib.sha256(raw).hexdigest(),baselineCanonicalEqual=True))
    p='Assets/CombatPrototype/FantasyActorVisual.cs';sample=sampling(original(repo,p),norm((repo/p).read_bytes()))
    paired_rows=paired(spawns(root/'Before2/events.jsonl'),spawns(root/'Final2/events.jsonl'))
    return dict(status='PASS',baseline=BASE,allowedEdits=changes,lockedSources=rows,animationSampling=sample,pairedActualSpawnCount=len(paired_rows),pairedActualSpawns=paired_rows,additionalFinalSpawns=[[59,1]])

def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('repo',type=Path);p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True);o=p.parse_args()
    need(not o.output.exists(),'refuse to overwrite audit evidence')
    try: result=audit(o.repo,o.root);code=0
    except (AuditError,OSError,ValueError,subprocess.CalledProcessError) as e: result=dict(status='FAIL',reason=str(e));code=1
    o.output.write_text(json.dumps(result,indent=2),encoding='utf-8');print(result['status']);return code
if __name__=='__main__': raise SystemExit(main())
