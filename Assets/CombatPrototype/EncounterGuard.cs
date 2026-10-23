using System.Linq;
using UnityEngine;
using UnityEngine.AI;
public class EncounterGuard:MonoBehaviour {
 public string encounterId,poi;public Vector3 home;public int State {get;private set;}
 ForestRegionRuntime region;CombatEnemy enemy;NavMeshPath path;float nextPath,lastHealth;Vector3 destination;int corner;
 public void Configure(ForestRegionRuntime owner,ForestEncounter descriptor){region=owner;enemy=GetComponent<CombatEnemy>();encounterId=descriptor.id;poi=descriptor.poi;home=descriptor.home;lastHealth=enemy.Health.Current;path=new NavMeshPath();}
 public void Restore(int state){State=Mathf.Clamp(state,0,2);nextPath=0;lastHealth=enemy.Health.Current;}
 public bool IdleOrReturn(CharacterController controller,float speed,ref float vertical){
  if(region==null||!region.Active)return false;
  float player=Vector3.Distance(enemy.target.transform.position,transform.position);
  if(State==0&&(player<enemy.detectionRange||enemy.Health.Current<lastHealth))Alert();lastHealth=enemy.Health.Current;
  if(State==1&&(Vector3.Distance(home,transform.position)>24||Vector3.Distance(home,enemy.target.transform.position)>31)){State=2;nextPath=0;}
  if(State==1)return false;
  Vector3 move=Vector3.zero;if(State==2){if(Vector3.Distance(home,transform.position)<1.2f){State=0;lastHealth=enemy.Health.Current;}else move=Direction(home)*speed;}
  if(controller.isGrounded&&vertical<0)vertical=-2;vertical+=Physics.gravity.y*Time.deltaTime;controller.Move((move+Vector3.up*vertical)*Time.deltaTime);return true;
 }
 void Alert(){State=1;foreach(var g in FindObjectsByType<EncounterGuard>(FindObjectsSortMode.None).Where(g=>g.region==region))if(g.poi==poi&&g.State==0&&!g.GetComponent<CombatEnemy>().Health.Dead)g.State=1;}
 public Vector3 Navigate(Vector3 movement){if(movement.sqrMagnitude<.01f)return movement;return Direction(transform.position+movement.normalized*2)*movement.magnitude;}
 public Vector3 Chase(Vector3 movement){if(movement.sqrMagnitude<.01f)return movement;Vector3 target=Vector3.Dot(movement,enemy.target.transform.position-transform.position)>0?enemy.target.transform.position:transform.position+movement.normalized*3;return Direction(target)*movement.magnitude;}
 Vector3 Direction(Vector3 target){if(Time.time>=nextPath||Vector3.Distance(target,destination)>3){destination=target;nextPath=Time.time+.35f;corner=1;path.ClearCorners();if(!NavMesh.SamplePosition(transform.position,out var a,3,NavMesh.AllAreas)||!NavMesh.SamplePosition(target,out var b,3,NavMesh.AllAreas)||!NavMesh.CalculatePath(a.position,b.position,NavMesh.AllAreas,path)||path.status!=NavMeshPathStatus.PathComplete)return Vector3.zero;}
  if(path.status!=NavMeshPathStatus.PathComplete||path.corners.Length<2)return Vector3.zero;while(corner<path.corners.Length-1&&Vector3.ProjectOnPlane(path.corners[corner]-transform.position,Vector3.up).magnitude<.65f)corner++;return Vector3.ProjectOnPlane(path.corners[corner]-transform.position,Vector3.up).normalized;
 }
}
