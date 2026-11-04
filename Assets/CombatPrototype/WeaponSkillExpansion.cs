using System;using System.Collections.Generic;using UnityEngine;
// New skill definitions do not alter legacy release code, traits or save schema.
public sealed class WeaponSkillDefinition {
 public readonly string id,name,description;public readonly GearType weapon;public readonly float cooldown,startup,gap,power,reach,dot,width,charge;public readonly int pulses;public readonly string mechanism;
 public WeaponSkillDefinition(string id,GearType w,string name,string mechanism,float cd,float startup,int count,float gap,float power,float reach,float dot,float width,float charge,string description){this.id=id;weapon=w;this.name=name;this.mechanism=mechanism;cooldown=cd;this.startup=startup;pulses=count;this.gap=gap;this.power=power;this.reach=reach;this.dot=dot;this.width=width;this.charge=charge;this.description=description;}
}
public static class WeaponSkillCatalog {
 public static readonly WeaponSkillDefinition[] All={
 new WeaponSkillDefinition("sword.triple",GearType.Sword,"三拍连斩","combo",8,.22f,3,.22f,.65f,2.5f,.4f,99,0,"三拍前向斩击；每段65%，可被翻滚/暂停取消后续段"),
 new WeaponSkillDefinition("sword.circle",GearType.Sword,"回旋剑阵","sustain",11,.32f,3,.48f,.55f,3.1f,-1,99,0,"周身三次55%近战脉冲；持续覆盖，恢复结束才可普攻"),
 new WeaponSkillDefinition("spear.charge",GearType.Spear,"蓄势穿刺","charge-thrust",9,.24f,1,0,1.2f,4.2f,.96f,.42f,.85f,"按住技能蓄势，松开突刺；最高1.85倍蓄势系数，不穿墙"),
 new WeaponSkillDefinition("spear.sweep",GearType.Spear,"扫锋拒敌","split-sweep",10,.27f,2,.30f,.8f,3.2f,.72f,2,0,"先左后右两道扇扫，各80%；不同于远距窄刺"),
 new WeaponSkillDefinition("staff.field",GearType.Staff,"余烬符阵","impact-field",10,.34f,1,0,.65f,3,-1,99,0,"火球真实接触后留下固定符阵，三次40%区域脉冲；墙体遮挡"),
 new WeaponSkillDefinition("staff.echo",GearType.Staff,"回响连珠","retarget-burst",9,.3f,3,.32f,.55f,0,0,0,0,"三枚55%直击弹，每次从当前真实杖首重新校验目标及遮挡"),
 new WeaponSkillDefinition("bow.burst",GearType.Bow,"追点连射","retarget-arrows",9,.25f,3,.22f,.55f,0,0,0,0,"三次独立箭，各55%，分时重瞄；不是原同时扇形箭雨"),
 new WeaponSkillDefinition("bow.pierce",GearType.Bow,"蓄势贯矢","charge-pierce",11,.3f,1,0,1.15f,0,0,0,1f,"按住蓄势，最多贯穿三个真实目标；实心场景立即阻挡")};
 public static WeaponSkillDefinition Get(GearType w,int slot)=>slot>=1&&slot<=2&&(int)w<4?All[(int)w*2+slot-1]:null;
}
[DefaultExecutionOrder(150)]
public sealed class WeaponSkillExpansion:MonoBehaviour {
 public struct Observation{public string skill,stage;public long attack;public int pulse;public Vector3 origin,direction;public Component target;public float before,after,time;}
 public event Action<Observation> Observed;
 public int Selected{get;private set;}public bool Busy=>active!=null;public WeaponSkillDefinition Definition=>WeaponSkillCatalog.Get(combat.Gear.Weapon,Selected);
 public string Phase{get;private set;}="Idle";public float ChargeFraction=>active==null||active.def.charge<=0?0:Mathf.Clamp01((Time.time-active.started)/active.def.charge);
 AdventureCombat combat;ThirdPersonHero hero;Cast active;
 sealed class Cast{public WeaponSkillDefinition def;public GearItem source;public long id;public float power,started,next,finish,visualAt,scale=1;public int pulse;public bool charged,prepared;public Quaternion facing;public object tracking;}
 sealed class PendingField{public Cast cast;public float expires;}
 readonly Dictionary<long,PendingField> fields=new Dictionary<long,PendingField>();readonly List<long> expired=new List<long>();
 void Awake(){combat=GetComponent<AdventureCombat>();hero=GetComponent<ThirdPersonHero>();if(GetComponent<WeaponSkillPanel>()==null)gameObject.AddComponent<WeaponSkillPanel>();}
 void OnEnable(){AdventureProjectile.Observed+=Projectile;}
 public bool Select(int slot){if(NewWeaponRegistry.Is(combat.Gear.Weapon))return combat.NewWeapons.Select(slot);if(slot<0||slot>2||combat==null)return false;CancelSequence();Selected=slot;PlayerInput.Barrier();return true;}
 public bool TryCast(){var def=Definition;if(def==null||combat.Gear.Main==null||Busy||!combat.ExpandedReady||def.weapon>=GearType.Staff&&CombatAim.CameraFor(hero)==null)return false;combat.PrepareExpanded(def.cooldown);active=new Cast{def=def,source=combat.Gear.Main?.Clone(),id=combat.ReserveExpandedAttack(),power=hero.AttackPower,started=Time.time,next=Time.time+def.startup,facing=transform.rotation};active.tracking=combat.CreateExpandedTracking(active.id,active.source,def.reach,active.next);Phase="Startup";Emit(active,"start");if(def.charge<=0)Animate(active);else CombatFeedback.Find(this)?.AttackStarted(hero,def.weapon,true);return true;}
 void Animate(Cast c){c.prepared=true;Emit(c,"windup");GetComponent<FantasyActorVisual>()?.AttackTimed(c.def.weapon>=GearType.Staff,Mathf.Max(.18f,c.def.startup+.22f),c.def.weapon==GearType.Sword&&c.def.mechanism=="sustain");CombatFeedback.Find(this)?.AttackStarted(hero,c.def.weapon,true);}
 void LateUpdate(){
  expired.Clear();foreach(var pair in fields)if(Time.time>=pair.Value.expires)expired.Add(pair.Key);foreach(long key in expired)fields.Remove(key);
  if(active==null)return;if(!combat.ExpandedContextReady||combat.Gear.Weapon!=active.def.weapon||combat.Gear.Main?.id!=active.source?.id){CancelSequence();return;}
  var c=active;if(c.pulse==0)c.facing=combat.TrackExpandedFacing(c.tracking);float elapsed=Time.time-c.started;
  if(c.def.charge>0&&!c.charged){Phase="Charging";if(Time.time>=c.visualAt){c.visualAt=Time.time+.15f;AdventurePulse.SpawnImpact(combat.MuzzlePosition,.18f+ChargeFraction*.12f,new Color(.5f,.8f,1),gameObject.scene,hero);}if(elapsed<c.def.startup||PlayerInput.Held(PlayerAction.Skill)&&elapsed<c.def.charge)return;c.scale=1+.85f*Mathf.Clamp01(elapsed/c.def.charge);c.charged=true;c.next=Time.time+c.def.startup;Animate(c);Emit(c,"charge-locked");}
  if(c.pulse<c.def.pulses&&!c.prepared&&Time.time>=c.next-c.def.startup)Animate(c);
  if(c.pulse<c.def.pulses&&Time.time>=c.next){Phase="Release";Release(c);if(active!=c)return;c.pulse++;c.prepared=false;c.next=Time.time+c.def.gap;if(c.pulse==c.def.pulses)c.finish=Time.time+.22f;}
  if(c.pulse==c.def.pulses){Phase="Recovery";if(Time.time>=c.finish){Emit(c,"complete");CombatFeedback.Find(this)?.CancelStartup(hero);active=null;Phase="Idle";}}
 }
 void Release(Cast c){
  if(c.def.weapon<GearType.Staff){float yaw=c.def.mechanism=="split-sweep"?(c.pulse==0?-32:32):0;var original=transform.rotation;try{transform.rotation=c.facing*Quaternion.Euler(0,yaw,0);CombatFeedback.Find(this)?.MeleeRelease(hero);Emit(c,"release",transform.position,transform.forward);combat.ExpandedMelee(c.id,c.source,c.def.reach,c.power*c.def.power*c.scale,c.def.dot,c.def.width);}finally{if(this!=null)transform.rotation=original;}}
  else{var aim=combat.ExpandedAim(c.def.weapon==GearType.Bow?57.5f:40);if(!aim.valid){Emit(c,"aim-rejected");return;}CombatFeedback.Find(this)?.RangedRelease(hero,c.def.weapon);Emit(c,"release",aim.origin,aim.direction);if(c.def.mechanism=="charge-pierce")SkillPiercingProjectile.Spawn(hero,this,c.def.id,c.id,c.source,aim,c.power*c.def.power*c.scale);else{if(c.def.mechanism=="impact-field")fields[c.id]=new PendingField{cast=c,expires=Time.time+3};AdventureProjectile.Spawn(hero,aim.origin,aim.direction,c.power*c.def.power,0,c.def.weapon==GearType.Bow?23:16,c.source,true,c.id,c.pulse+1,aim);}}
 }
 void Projectile(AdventureProjectile.Observation e){if(hero==null||e.projectile.gameObject.scene!=hero.gameObject.scene)return;if(!fields.TryGetValue(e.projectile.AttackId,out var field))return;if(e.stage=="resolved"||e.stage=="resolved-blocked-origin"){fields.Remove(e.projectile.AttackId);if(e.stage=="resolved"&&hero!=null&&!hero.Health.Dead){var c=field.cast;SkillImpactField.Spawn(hero,this,c.def.id,c.id,c.source,e.from-e.projectile.Direction*.2f,c.power*.4f,c.def.reach);Emit(c,"field-created",e.from,e.projectile.Direction);}}}
 public void Contact(string id,long attack,string stage,Component target,Vector3 p,Vector3 dir,float before,float after){Observed?.Invoke(new Observation{skill=id,attack=attack,stage=stage,target=target,origin=p,direction=dir,before=before,after=after,time=Time.time});}
 void Emit(Cast c,string stage,Vector3 p=default,Vector3 dir=default){Observed?.Invoke(new Observation{skill=c.def.id,attack=c.id,stage=stage,pulse=c.pulse,origin=p,direction=dir,time=Time.time});}
 public void CancelSequence(){if(active==null)return;Emit(active,"cancel");active=null;Phase="Cancelled";GetComponent<FantasyActorVisual>()?.CancelAttack();CombatFeedback.Find(this)?.CancelStartup(hero);}
 void OnApplicationFocus(bool focused){if(!focused)CancelSequence();}
 void OnDisable(){CancelSequence();AdventureProjectile.Observed-=Projectile;fields.Clear();SkillPiercingProjectile.Clear(hero);SkillImpactField.Clear(hero);}
}
public partial class AdventureCombat {
 public WeaponSkillExpansion Expanded{get;private set;}
 internal bool ExpandedContextReady=>Ready&&!PlayerInput.Suspended;
 internal bool ExpandedReady=>ExpandedContextReady&&actions.Count==0&&Time.time>=skillAt;
 internal void PrepareExpanded(float cooldown){skillAt=Time.time+cooldown;if((int)Gear.Weapon>=2)FaceCamera();}
 internal long ReserveExpandedAttack(){LastAttackId=++nextAttackId;return nextAttackId;}
 internal object CreateExpandedTracking(long id,GearItem source,float reach,float releaseAt)=>new AttackAction{id=id,source=source,type=source.type,beganAt=Time.time,releaseAt=releaseAt,range=reach,reach=reach-SpearReach};
 internal Quaternion TrackExpandedFacing(object state){TrackMelee((AttackAction)state);return transform.rotation;}
 internal RangedAimSolution ExpandedAim(float distance){FaceCamera();return SolveRanged(distance);}
 internal void ExpandedMelee(long id,GearItem source,float radius,float damage,float dot,float width){var a=new AttackAction{id=id,source=source,type=source.type,skill=true};Melee(a,radius,damage,dot,width);}
}
