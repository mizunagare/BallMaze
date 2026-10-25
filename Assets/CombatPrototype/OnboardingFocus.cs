using System.Linq;
using UnityEngine;
using UnityEngine.AI;

// Bounded read-only navigation hint. Never moves the hero or interacts with its target.
public sealed class OnboardingFocus:MonoBehaviour {
 public string TargetId {get;private set;}
 public TutorialStage CapturedStage {get;private set;}
 public void Invalidate(){next=0;TargetId=null;Hint="";Reachable=false;Distance=-1;}
 public string Hint {get;private set;}="";
 public Vector3 Position {get;private set;}
 public float Distance {get;private set;}=-1;
 public bool Reachable {get;private set;}
 float next;CombatSession session;
 void Awake(){session=GetComponent<CombatSession>();}
 void Update(){if(Time.unscaledTime>=next){next=Time.unscaledTime+1;Refresh();}}
 static float Segment(Vector3 p,Vector3 a,Vector3 b){p.y=a.y=b.y=0;var d=b-a;return Vector3.Distance(p,a+d*Mathf.Clamp01(Vector3.Dot(p-a,d)/Mathf.Max(.001f,d.sqrMagnitude)));}
 public void Refresh(){TargetId=null;Hint="";Distance=-1;Reachable=false;if(!Onboarding.Active(session))return;var t=Onboarding.State(session);CapturedStage=t.stage;
  if(session.Flow.AtCamp){TargetId=Onboarding.FacilityId(session);Position=session.Camp.FacilityPosition(TargetId);Distance=Vector3.Distance(session.hero.transform.position,Position);Reachable=true;Hint="营地约"+Distance.ToString("0")+"米 · 靠近按E";return;}
  var region=GetComponent<ForestRegionRuntime>();if(session.Flow.ActiveRun?.mode!=AdventureMode.ForestExploration||region==null||!region.Ready)return;
  if(t.stage==TutorialStage.FreeExit){foreach(var exit in session.Flow.ExitConfigs().Where(e=>!e.repairRequired))if(region.TryInteractionApproach(exit,out var point))Consider(exit.id,"免费出口",point,false);}
  else if(t.stage==TutorialStage.Harvest||t.stage==TutorialStage.Pickup||t.stage==TutorialStage.Withdraw||t.stage==TutorialStage.Manufacture){var costs=CraftingCosts.Gear(GearQuality.White);var missing=costs.Where(c=>session.hero.Inventory.Count(c.material)<c.amount).Select(c=>c.material).ToArray();
   foreach(var loot in Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Where(l=>l.gameObject.scene==gameObject.scene&&!l.Collected&&l.Gear==null&&(t.stage==TutorialStage.Harvest?t.resourceLootIds.Contains(l.InteractionId):missing.Length==0||missing.Contains(l.Kind))).OrderBy(l=>(l.transform.position-session.hero.transform.position).sqrMagnitude).Take(12))Consider(loot.InteractionId,PlayerInventory.Label(loot.Kind)+"掉落",loot.transform.position,true);
   if(!Reachable)foreach(var resource in Object.FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(r=>r.gameObject.scene==gameObject.scene&&r.Health>0&&(t.stage==TutorialStage.Harvest||missing.Length==0||missing.Contains(r.kind))).OrderBy(r=>(r.transform.position-session.hero.transform.position).sqrMagnitude).Take(12))Consider(resource.StableId,PlayerInventory.Label(resource.kind)+"节点",resource.transform.position,true);
  }
  if(!Reachable&&(t.stage==TutorialStage.Harvest||t.stage==TutorialStage.Pickup||t.stage==TutorialStage.Withdraw||t.stage==TutorialStage.Manufacture||t.stage==TutorialStage.FreeExit))Hint="附近无安全可达目标 · M查看路线";
 }
 void Consider(string id,string name,Vector3 point,bool avoidElite){if(!NavMesh.SamplePosition(session.hero.transform.position,out var from,3,NavMesh.AllAreas)||!NavMesh.SamplePosition(point,out var to,3,NavMesh.AllAreas))return;var path=new NavMeshPath();if(!NavMesh.CalculatePath(from.position,to.position,NavMesh.AllAreas,path)||path.status!=NavMeshPathStatus.PathComplete||path.corners.Length<1)return;
  float distance=0;for(int i=1;i<path.corners.Length;i++)distance+=Vector3.Distance(path.corners[i-1],path.corners[i]);
  if(avoidElite)foreach(var e in session.enemies.Where(e=>!e.Health.Dead&&(e.archetype==EnemyArchetype.Elite||e.archetype==EnemyArchetype.Boss)))for(int i=1;i<path.corners.Length;i++)if(Segment(e.transform.position,path.corners[i-1],path.corners[i])<12)return;
  if(Reachable&&distance>=Distance)return;TargetId=id;Position=to.position;Distance=distance;Reachable=true;Hint=name+" · 约"+distance.ToString("0")+"米";
 }
}
