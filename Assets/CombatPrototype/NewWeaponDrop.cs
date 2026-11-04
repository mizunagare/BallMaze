using UnityEngine;
// Supplemental new-content roll. Never draws from Rewards/Placement/Events or Unity.Random.
public static class NewWeaponDrop {
 public static bool KnownRevision(string value)=>NewWeaponDropRules.Read(value,out _);
 public static string Revision(string old)=>NewWeaponDropRules.Stamp(old);
 public static GearItem Preview(RunState run,string entityId,EnemyArchetype archetype){if(run==null||run.mode!=AdventureMode.ForestExploration||!NewWeaponDropRules.Read(run.contentRevision,out int count)||string.IsNullOrEmpty(entityId)||archetype==EnemyArchetype.Boss)return null;string key="NW1/"+run.runId+"/"+run.regionInstanceId+"/"+run.seed.ToString(System.Globalization.CultureInfo.InvariantCulture)+"/"+entityId;double chance=NewWeaponRegistry.Number(key+"/chance")/4294967296.0;if(chance>=NewWeaponDropRules.Chance(archetype))return null;var type=(GearType)(11+NewWeaponDropRules.Choose(NewWeaponRegistry.Number(key+"/type"),count));double q=NewWeaponRegistry.Number(key+"/quality")/4294967296.0;var quality=NewWeaponDropRules.Quality(q);return NewWeaponRegistry.Create(type,quality,key);}
 public static void AfterDeath(CombatEnemy enemy){if(enemy==null||enemy.target==null||enemy.GetComponent<ForestBossBrain>()!=null)return;var flow=AdventureFlow.Find(enemy.target);var item=Preview(flow?.ActiveRun,enemy.entityId,enemy.archetype);if(item==null)return;var pickup=LootPickup.SpawnGear(item,enemy.transform.position+Vector3.up*.55f+Vector3.back*.4f);UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(pickup.gameObject,enemy.gameObject.scene);}
}
