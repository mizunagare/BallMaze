using System.Collections.Generic;using System.Linq;using UnityEngine;

// Rigid original cat meshes follow the existing sampled KayKit bone hierarchy.
// Animations remain on FantasyActorVisual; this component never drives damage/time/RNG.
[DefaultExecutionOrder(22000)]
public sealed class CatActorVisual:MonoBehaviour {
 FantasyActorVisual actor;GameObject prior;string kind;readonly List<GameObject> parts=new List<GameObject>();readonly List<Renderer> originals=new List<Renderer>();
 public string Kind=>kind;public int PartCount=>parts.Count;public bool Ready=>prior!=null&&parts.Count>0;
 public static uint Stable(string value){unchecked{uint h=2166136261;foreach(char c in value??""){h^=c;h*=16777619;}return h;}}
 public static string EnemyKind(CombatEnemy enemy){var boss=enemy.GetComponent<ForestBossBrain>();if(boss!=null)return boss.Kind==ForestBossKind.Warden?"Warden":"Tide";if(enemy.archetype==EnemyArchetype.Boss)return "Warden";uint n=Stable(enemy.entityId);if(enemy.archetype==EnemyArchetype.Elite)return n%2==0?"Hunter":"Lynx";if(enemy.archetype==EnemyArchetype.Ranged)return n%3==0?"WoodSpirit":"Scout";return n%4==0?"Mushroom":"Bandit";}
 public static string DisplayName(CombatEnemy enemy){switch(EnemyKind(enemy)){case "Warden":return "古林狞猫守卫";case "Tide":return "湖心潮灵猫";case "Hunter":return "豹猫猎手";case "Lynx":return "猞猁精英";case "WoodSpirit":return "林间猫灵";case "Scout":return "山猫斥候";case "Mushroom":return "猫爪蘑菇灵";default:return "野猫盗匪";}}
 void Awake(){actor=GetComponent<FantasyActorVisual>();}
 void LateUpdate(){if(actor==null||actor.model==null)return;var enemy=GetComponent<CombatEnemy>();string next=actor.isHero?"Hero":enemy!=null?EnemyKind(enemy):"Bandit";if(prior!=actor.model||next!=kind)Bind(next);}
 void Clear(){foreach(var p in parts)if(p!=null){p.SetActive(false);Destroy(p);}parts.Clear();foreach(var r in originals)if(r!=null)r.enabled=true;originals.Clear();}
 void Bind(string next){Clear();prior=actor.model;kind=next;var prefab=Resources.Load<GameObject>("CatWorld/Actors/"+kind);if(prefab==null){Debug.LogError("Missing B10 cat prefab: "+kind);return;}
  // Retain old renderers as disabled bone carriers so legacy saves/prefabs and bound animations remain intact.
  var bones=prior.GetComponentsInChildren<Transform>(true).Where(t=>t.name.StartsWith("@") == false).GroupBy(t=>t.name).ToDictionary(g=>g.Key,g=>g.First());
  foreach(var r in prior.GetComponentsInChildren<Renderer>(true)){if(r is SkinnedMeshRenderer||r.name.StartsWith("Knight_")||r.name.StartsWith("Skeleton_")){originals.Add(r);r.enabled=false;}}
  foreach(var r in GetComponentsInChildren<Renderer>(true))if(r.name=="角卫枝冠"||r.name=="潮灵水冠"){originals.Add(r);r.enabled=false;}
  var model=Instantiate(prefab,prior.transform,false);model.name="B10 猫族外观 · "+kind;
  foreach(Transform group in model.transform.Cast<Transform>().ToArray()){if(group.name.StartsWith("@")&&bones.TryGetValue(group.name.Substring(1),out var bone))group.SetParent(bone,true);parts.Add(group.gameObject);}Destroy(model);
  GetComponent<CombatHealth>()?.RefreshVisuals();
 }
 void OnDestroy(){Clear();}
}
