using System;
using System.Linq;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;
public sealed class RuinsExploration:MonoBehaviour {
 ForestRegionRuntime region;GameObject door,seal;CombatSession S=>GetComponent<CombatSession>();
 public bool Active=>region!=null&&region.Active&&RuinsLayout.Is(region.Layout);
 public bool DoorOpen=>Used("c1:door");public bool SecretOpen=>Used("c1:archive");
 public string Objective=>!Used("c1:lever")?"远古遗迹 · 广场机关\n入口可免费撤离":!DoorOpen?"远古遗迹 · 开启石门\n先查看互动提示":!SecretOpen?"地下祭坛 · 解读碑文\n守护者为可选挑战":"密室已显现\n可寻宝、挑战或撤离";
 public static RuinsExploration For(Component c){if(c==null)return null;return FindObjectsByType<RuinsExploration>(FindObjectsSortMode.None).FirstOrDefault(r=>r.gameObject.scene==c.gameObject.scene&&r.Active);}
 public void Configure(ForestRegionRuntime owner,GameObject gate,GameObject hidden){region=owner;door=gate;seal=hidden;ApplyState(false);}
 public void Detach(){region=null;door=seal=null;}
 bool Used(string id)=>S.Events.Points.Any(p=>p.entityId==id&&p.Used);
 public bool CanUse(WorldEventPoint p){if(!Active||p==null||!p.entityId.StartsWith("c1:")||S.Flow.Frozen)return false;if(p.entityId=="c1:door")return Used("c1:lever");if(p.entityId=="c1:hidden")return SecretOpen&&!p.Used;return !p.Used;}
 public static string Title(WorldEventPoint p){if(For(p)==null)return null;switch(p.entityId){case "c1:lever":return p.Used?"机关已激活":"转动符文机关";case "c1:door":return p.Used?"关闭遗迹门":"开启遗迹门（先激活机关）";case "c1:archive":return p.Used?"碑文已解读 · 密室显现":"解读猫族碑文";case "c1:hidden":return p.Used?"隐藏箱已开启":"开启隐藏宝箱";default:return p.Used?"遗迹宝箱已开启":"开启遗迹宝箱";}}
 void ApplyState(bool navigation){if(door!=null)door.SetActive(!DoorOpen);if(seal!=null)seal.SetActive(!SecretOpen);Physics.SyncTransforms();if(navigation)region.RebuildRuinsNavigation();}
 public bool Interact(WorldEventPoint point,ThirdPersonHero hero){
  if(!CanUse(point)||hero!=S.hero)return false;
  if(point.entityId=="c1:door"&&DoorOpen){foreach(var c in Physics.OverlapBox(new Vector3(0,1.8f,220),new Vector3(5,1.8f,.55f)))if(c.GetComponentInParent<ThirdPersonHero>()!=null||c.GetComponentInParent<CombatEnemy>()!=null){hero.Inventory.NotifyMessage("门口有角色，暂不能关闭。");return false;}}
  bool prior=point.Used;long revision=S.Flow.Revision;var spawned=new List<LootPickup>();
  point.RestoreUsed(point.entityId=="c1:door"?!prior:true);
  try{
   if(point.Kind==WorldEventKind.Treasure)Chest(point,spawned);
   else if(point.entityId=="c1:archive")Spawn(point.entityId,MaterialKind.CrystalShard,2,point.transform.position+Vector3.right*1.3f,spawned);
   ApplyState(true);
   if(!S.Saves.SaveProgress(false)){
    var disk=CombatSaveSystem.InspectReadOnly(S.Saves.SavePath);
    bool published=disk.revision==revision+1&&disk.activeRun?.runId==S.Flow.ActiveRun.runId&&disk.activeRun.checkpoint.events.Any(e=>e.entityId==point.entityId&&e.used==point.Used)&&spawned.All(l=>disk.activeRun.checkpoint.loot.Any(x=>x.entityId==l.InteractionId));
    if(published)S.Saves.ConfirmPublishedSave();
    else if(disk.revision==revision&&disk.activeRun?.runId==S.Flow.ActiveRun.runId&&disk.activeRun.checkpoint.events.Any(e=>e.entityId==point.entityId&&e.used==prior)){Rollback(point,prior,spawned);hero.Inventory.NotifyMessage("交互未保存，状态已还原，请重试。");return false;}
    else throw new InvalidOperationException("遗迹交互保存结果不确定");
   }
   hero.Inventory.NotifyMessage(point.Kind==WorldEventKind.Treasure?"遗迹战利品已落地并保存；靠近按 "+PlayerInput.Key(PlayerAction.Interact)+" 拾取。":Title(point));return true;
  }catch(Exception e){S.Flow.MigrationFailed("遗迹交互结果待核对，请读取完整存档："+e.Message);return false;}
 }
 void Rollback(WorldEventPoint p,bool prior,List<LootPickup> spawned){foreach(var l in spawned){l.gameObject.SetActive(false);Destroy(l.gameObject);}p.RestoreUsed(prior);ApplyState(true);}
 string Identity(string id)=>RuinsLayout.Content+"/"+S.Flow.ActiveRun.runId+"/"+S.Flow.ActiveRun.regionInstanceId+"/"+S.Flow.ActiveRun.seed+"/"+id;
 public static string Hash(string s){using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(s))).Replace("-","").ToLowerInvariant();}
 public void Spawn(string id,MaterialKind kind,int amount,Vector3 p,List<LootPickup> list=null){var loot=LootPickup.Spawn(kind,amount,p+Vector3.up*.6f);loot.RestoreInteractionId("c1:"+Hash(Identity(id)+"/"+kind).Substring(0,32));UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(loot.gameObject,gameObject.scene);list?.Add(loot);}
 void Gear(string id,Vector3 p,GearQuality quality,List<LootPickup> list=null){string identity=Identity(id)+"/gear";int n=Convert.ToInt32(Hash(identity).Substring(0,4),16)%3;var type=new[]{GearType.TwinBlades,GearType.Greatsword,GearType.Scythe}[n];var loot=LootPickup.SpawnGear(NewWeaponRegistry.Create(type,quality,identity),p+Vector3.up);loot.RestoreInteractionId("c1:"+Hash(identity).Substring(0,32));UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(loot.gameObject,gameObject.scene);list?.Add(loot);}
 void Chest(WorldEventPoint p,List<LootPickup> list){bool hidden=p.entityId=="c1:hidden";int roll=Convert.ToInt32(Hash(Identity(p.entityId)).Substring(0,4),16);Spawn(p.entityId,MaterialKind.Ore,hidden?3:1+roll%3,p.transform.position+Vector3.right*1.3f,list);Spawn(p.entityId,MaterialKind.CrystalShard,hidden?2:1,p.transform.position+Vector3.left*1.3f,list);if(hidden||roll%100<25)Gear(p.entityId,p.transform.position+Vector3.back*1.3f,hidden?GearQuality.Green:GearQuality.White,list);}
 public void DropEnemy(CombatEnemy enemy){
  if(!Active||enemy==null||!enemy.Health.Dead||!region.Layout.encounters.Any(e=>e.id==enemy.entityId))throw new InvalidOperationException("遗迹死亡来源不匹配");
  bool boss=enemy.entityId=="c1:guardian",elite=enemy.archetype==EnemyArchetype.Elite;
  Spawn(enemy.entityId,MaterialKind.MonsterHide,boss?4:elite?2:1,enemy.transform.position+Vector3.left);
  if(elite||boss)Spawn(enemy.entityId,MaterialKind.CrystalShard,boss?3:1,enemy.transform.position+Vector3.right);
  if(boss){Spawn(enemy.entityId,MaterialKind.BossCore,1,enemy.transform.position+Vector3.forward);Gear(enemy.entityId,enemy.transform.position+Vector3.back,GearQuality.Purple);}
  // Existing periodic/terminal saves capture dead actor and ground items together.
  // No old reward stream, XP offers, badges or direct inventory credit here.
 }
 public static void ExpectedChest(WorldEventPoint p,float[] amounts,out float gear){bool hidden=p.entityId=="c1:hidden";amounts[(int)MaterialKind.Ore]+=hidden?3:2;amounts[(int)MaterialKind.CrystalShard]+=hidden?2:1;gear=hidden?1:.25f;}
 public static void ExpectedEnemy(CombatEnemy e,float[] amounts,out float gear){bool boss=e.entityId=="c1:guardian",elite=e.archetype==EnemyArchetype.Elite;amounts[(int)MaterialKind.MonsterHide]+=boss?4:elite?2:1;if(elite||boss)amounts[(int)MaterialKind.CrystalShard]+=boss?3:1;if(boss)amounts[(int)MaterialKind.BossCore]++;gear=boss?1:0;}
}
