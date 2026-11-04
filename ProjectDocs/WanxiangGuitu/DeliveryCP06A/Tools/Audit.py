from pathlib import Path
import subprocess,json,hashlib,sys
repo=Path(__file__).resolve().parents[4];base='397d53fe87ce5b6c490c86c63d59015de26a46af';root=Path(sys.argv[1]);output=Path(sys.argv[2]);errors=[]
def old(path):return subprocess.check_output(['git','show',base+':'+path],cwd=repo).decode('utf-8-sig').replace('\r\n','\n')
path='Assets/CombatPrototype/AdventureCombat.cs';expected=old(path)
patches=[('public class AdventureCombat :','public partial class AdventureCombat :'),('public int PendingAttackCount {get{int count=0;','public int PendingAttackCount {get{int count=Expanded!=null&&Expanded.Busy?1:0;'),('    public void CancelPending() {','    public void CancelPending() {\n        Expanded?.CancelSequence();'),('    public float SkillDuration=>7+','    public float SkillDuration=>Expanded!=null&&Expanded.Selected>0?Expanded.Definition.cooldown:7+'),('public string SkillName => new[]','public string SkillName => Expanded!=null&&Expanded.Selected>0?Expanded.Definition.name:new[]'),('        get {\n            int q=Gear.Main','        get {\n            if(Expanded!=null&&Expanded.Selected>0)return Expanded.Definition.description;\n            int q=Gear.Main'),('Gear=gameObject.AddComponent<AdventureLoadout>(); }','Gear=gameObject.AddComponent<AdventureLoadout>(); Expanded=GetComponent<WeaponSkillExpansion>();if(Expanded==null)Expanded=gameObject.AddComponent<WeaponSkillExpansion>(); }'),('    public bool Strike()\n    {','    public bool Strike()\n    {\n        if(Expanded!=null&&Expanded.Busy)return false;'),('    public bool UseSkill()\n    {','    public bool UseSkill()\n    {\n        if(Expanded!=null&&Expanded.Selected>0)return Expanded.TryCast();'),('public void ResetCombat(){CancelPending();','public void ResetCombat(){SkillPiercingProjectile.Clear(hero);SkillImpactField.Clear(hero);CancelPending();')]
for a,b in patches:
 if expected.count(a)!=1:errors.append('Patch location/count '+a)
 else:expected=expected.replace(a,b)
actual=(repo/path).read_text(encoding='utf-8-sig')
if actual!=expected:errors.append('Shared file differs outside ten exact additions; legacy release/geometry/projectile/values must remain exact')
changed=[]
for row in json.loads((root/'protected-before.json').read_text()):
 f=Path(row['path']);h=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else 'MISSING'
 if h!=row['sha256']:
  changed.append(dict(path=str(f),before=row['sha256'],after=h))
  if f!=repo/path:errors.append('Protected file changed '+str(f))
for f in (repo/'ProjectDocs/WanxiangGuitu/DeliveryCP06A/Tests').glob('*.cs.txt'):
 for forbidden in ['.Damage(','.RestoreHealth(','.ResetHealth(','.RestoreInventory(']:
  if forbidden in f.read_text(encoding='utf8'):errors.append('Injected business result in '+str(f)+': '+forbidden)
result=dict(status='FAIL' if errors else 'PASS',baseline=base,protectedCount=len(json.loads((root/'protected-before.json').read_text())),exactSharedPatches=len(patches),changed=changed,errors=errors);output.write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result));sys.exit(bool(errors))
