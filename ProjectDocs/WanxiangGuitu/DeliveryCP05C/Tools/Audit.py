from pathlib import Path
import json,hashlib,subprocess,sys
repo=Path(__file__).resolve().parents[4];baseline='7fc4f5dc3043bcbb69f63c2ebf267359741ccbbe'
def old(name):return subprocess.check_output(['git','show',baseline+':Assets/CombatPrototype/'+name],cwd=repo).decode('utf-8-sig').replace('\r\n','\n')
def method(text,head):
 start=text.index(head);i=text.index('{',start);j=i+1;depth=1
 while depth:depth+=(text[j]=='{')-(text[j]=='}');j+=1
 return start,j,text[i+1:j-1]
def source_checks(after):
 errors=[]
 try:
  a=old('AdventureRandom.cs');anchor='        var flows=UnityEngine.Object.FindObjectsByType<AdventureFlow>(FindObjectsSortMode.None)';assert a.count(anchor)==1
  if after['AdventureRandom.cs']!=a.replace(anchor,'        var training=TrainingLootContext.For(owner);if(training!=null)return training.Streams;\n'+anchor):errors.append('Random routing differs outside exact scene-context insertion')
  a=old('AdventureItems.cs');b=after['AdventureItems.cs'];oa,oz,ob=method(a,'public static GearItem Roll(');na,nz,nb=method(b,'public static GearItem Roll(');_,tz,tb=method(b,'public static GearItem RollTraining(');_,hz,hb=method(b,'static GearItem RollQuality(');split=ob.index('        GearQuality q =');prefix=ob[:split]
  if nb!=prefix+'        return RollQuality(r,luck,treasure,boss,owner);\n    ':errors.append('Formal Roll draw/luck order changed')
  if hb.strip()!=ob[split:].strip():errors.append('Shared quality/type/New body changed')
  if tb.strip()!='return RollQuality(AdventureRandom.Value(owner:owner),0,false,false,owner);':errors.append('Training policy not explicit zero luck')
  if a[:oa]!=b[:na] or a[oz:]!=b[hz:]:errors.append('Unrelated item code changed')
  a=old('CombatEnemy.cs');b=after['CombatEnemy.cs'];oa,oz,ob=method(a,'public void DropLootOnce()');na,nz,nb=method(b,'public void DropLootOnce()');ca,cz,cb=method(b,'void DropLootCore(')
  wrapper='\n        if (health == null || !health.Dead || lootDropped) return;\n        var training=TrainingLootContext.ForDeath(this);\n        DropLootCore(training);\n        if(training!=null)training.CompleteDeath();\n    '
  if nb!=wrapper:errors.append('Death guard/wrapper changed')
  guard='        if (health == null || !health.Dead || lootDropped) return;\n';assert ob.count(guard)==1
  original='AdventureItems.Roll(Object.FindFirstObjectByType<CombatSession>().Wave,owner:this)';replacement='training!=null?training.RollEquipment(this):'+original;assert cb.count(replacement)==1
  if cb.replace(replacement,original)!=ob.replace(guard,''):errors.append('Formal drop body/probability/XP/material order changed')
  if a[:oa]!=b[:na] or a[oz:]!=b[cz:]:errors.append('Unrelated enemy/AI code changed')
 except (ValueError,AssertionError,IndexError) as e:errors.append('Invalid source structure '+str(e))
 return errors
if __name__=='__main__':
 files=['AdventureRandom.cs','AdventureItems.cs','CombatEnemy.cs'];after={n:(repo/'Assets/CombatPrototype'/n).read_text(encoding='utf-8-sig') for n in files};errors=source_checks(after);root=Path('I:/WGCombat/CP05C-1104-A');before=json.loads((root/'protected-before.json').read_text(encoding='utf8'));allowed={'Assets/CombatPrototype/'+n for n in files+['CP05Training.cs']};changed=[]
 for r in before:
  p=Path(r['path']);h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'MISSING'
  if h!=r['sha256']:
   rel=p.relative_to(repo).as_posix() if p.is_relative_to(repo) else '';changed.append({'path':str(p),'relative':rel,'before':r['sha256'],'after':h})
   if rel not in allowed:errors.append('Unexpected protected change '+str(p))
 tests='\n'.join(f.read_text(encoding='utf-8-sig') for f in (repo/'ProjectDocs/WanxiangGuitu/DeliveryCP05C/Tests').glob('*.cs.txt'))
 for forbidden in ['.Damage(','.ResetHealth(','.RestoreHealth(','.RestoreInventory(','.RestoreProgress(']:
  if forbidden in tests:errors.append('Injected state API in tests '+forbidden)
 result={'status':'FAIL' if errors else 'PASS','baseline':baseline,'protectedFiles':len(before),'changed':changed,'errors':errors,'scope':'Exact formal body/order contracts + user/frozen hashes; runtime paired evidence is separate'};Path(sys.argv[1]).write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2));sys.exit(bool(errors))
