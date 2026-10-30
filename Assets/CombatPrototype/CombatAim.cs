using System;
using System.Linq;
using UnityEngine;

[Serializable] public struct RangedAimSolution {
 public const int ContractVersion=1;
 public int version,frame;public bool valid,barrelBlocked,obstructed,hasContact;
 public string reason,muzzleSource;public Vector3 cameraOrigin,cameraDirection,intentPoint,rawMuzzle,origin,direction,fanUp,contactPoint,viewport;
 public Camera camera;public Collider cameraCollider,contactCollider;
}

// Read-only physics queries. It never chooses a nearest enemy, consumes RNG or applies damage.
public static class CombatAim {
 public const float ProjectileRadius=.16f,RayLimit=80;
 public static bool Finite(Vector3 v)=>!float.IsNaN(v.x)&&!float.IsInfinity(v.x)&&!float.IsNaN(v.y)&&!float.IsInfinity(v.y)&&!float.IsNaN(v.z)&&!float.IsInfinity(v.z);
 public static Camera CameraFor(ThirdPersonHero hero){
  if(hero==null||hero.cameraTransform==null)return null;var camera=hero.cameraTransform.GetComponent<Camera>();var orbit=hero.cameraTransform.GetComponent<OrbitCamera>();
  return camera!=null&&camera.isActiveAndEnabled&&camera.gameObject.scene==hero.gameObject.scene&&orbit!=null&&orbit.target==hero.transform?camera:null;
 }
 public static bool Legal(Collider c,ThirdPersonHero hero)=>c!=null&&c.enabled&&c.gameObject.activeInHierarchy&&!c.isTrigger&&c.gameObject.scene==hero.gameObject.scene&&c.GetComponentInParent<ThirdPersonHero>()!=hero;
 static int Priority(Collider c)=>c.GetComponentInParent<CombatEnemy>()!=null||c.GetComponentInParent<AdventureResource>()!=null?1:0;
 public static bool SameOwner(Collider a,Collider b){if(a==null||b==null)return false;if(a==b)return true;var resource=a.GetComponentInParent<AdventureResource>();if(resource!=null)return resource==b.GetComponentInParent<AdventureResource>();var enemy=a.GetComponentInParent<CombatEnemy>();return enemy!=null&&enemy==b.GetComponentInParent<CombatEnemy>();}
 // Non-convex terrain has no supported ClosestPoint API in the pinned engine.
 // This point is used only AFTER an actual overlap query confirmed solid contact.
 public static Vector3 OverlapPoint(Collider c,Vector3 p)=>c is TerrainCollider||c is MeshCollider m&&!m.convex?p:c.ClosestPoint(p);
 public static Collider InitialContact(Vector3 origin,ThirdPersonHero hero){
  return Physics.OverlapSphere(origin,ProjectileRadius,~0,QueryTriggerInteraction.Ignore).Where(c=>Legal(c,hero))
   .OrderBy(c=>(OverlapPoint(c,origin)-origin).sqrMagnitude).ThenBy(Priority).FirstOrDefault();
 }
 public static bool Sweep(Vector3 origin,Vector3 direction,float distance,ThirdPersonHero hero,out RaycastHit hit){
  foreach(var candidate in Physics.SphereCastAll(origin,ProjectileRadius,direction,Mathf.Max(0,distance),~0,QueryTriggerInteraction.Ignore).OrderBy(h=>h.distance).ThenBy(h=>Priority(h.collider)))
   if(Legal(candidate.collider,hero)){hit=candidate;return true;}hit=default;return false;
 }
 public static RangedAimSolution Solve(ThirdPersonHero hero,Vector3 muzzle,string source,float flightDistance){
  var result=new RangedAimSolution{version=RangedAimSolution.ContractVersion,frame=Time.frameCount,reason="NO_OWN_ACTIVE_CAMERA",rawMuzzle=muzzle,muzzleSource=source};var camera=CameraFor(hero);
  if(camera==null||!Finite(muzzle))return result;var ray=camera.ViewportPointToRay(new Vector3(.5f,.5f));
  if(!Finite(ray.origin)||!Finite(ray.direction)||ray.direction.sqrMagnitude<.001f){result.reason="INVALID_CAMERA_RAY";return result;}
  result.camera=camera;result.cameraOrigin=ray.origin;result.cameraDirection=ray.direction.normalized;result.intentPoint=ray.GetPoint(RayLimit);
  foreach(var hit in Physics.RaycastAll(ray,RayLimit,~0,QueryTriggerInteraction.Ignore).OrderBy(h=>h.distance).ThenBy(h=>Priority(h.collider)))
   if(Legal(hit.collider,hero)){result.intentPoint=hit.point;result.cameraCollider=hit.collider;break;}
  Vector3 anchor=hero.transform.position+Vector3.up*1.25f;result.origin=muzzle;
  var inside=InitialContact(anchor,hero);var barrel=muzzle-anchor;
  if(inside!=null){result.origin=anchor;result.barrelBlocked=true;}
  else if(barrel.sqrMagnitude>.000001f&&Sweep(anchor,barrel.normalized,barrel.magnitude,hero,out var block)){
   result.origin=anchor+barrel.normalized*Mathf.Max(0,block.distance-.002f);result.barrelBlocked=true;
  }
  Vector3 direction=result.intentPoint-result.origin;
  // A surface between the camera and the body must never turn the projectile backwards.
  if(direction.sqrMagnitude<.000001f||Vector3.Dot(direction,result.cameraDirection)<=.001f){direction=result.cameraDirection;result.intentPoint=result.origin+direction*RayLimit;result.cameraCollider=null;result.reason="CAMERA_SURFACE_BEHIND_MUZZLE";}
  else result.reason="CAMERA_TO_MUZZLE";
  result.direction=direction.normalized;result.fanUp=Vector3.ProjectOnPlane(Vector3.up,result.direction).normalized;
  if(result.fanUp.sqrMagnitude<.001f)result.fanUp=camera.transform.up;
  float distance=Mathf.Min(RayLimit,Mathf.Max(.001f,flightDistance));result.contactPoint=result.origin+result.direction*distance;
  inside=InitialContact(result.origin,hero);
  if(inside!=null){result.contactCollider=inside;result.contactPoint=OverlapPoint(inside,result.origin);result.hasContact=true;}
  else if(Sweep(result.origin,result.direction,distance,hero,out var collision)){result.contactCollider=collision.collider;result.contactPoint=collision.point;result.hasContact=true;}
  result.obstructed=result.barrelBlocked||result.contactCollider!=null&&!SameOwner(result.contactCollider,result.cameraCollider);
  result.viewport=camera.WorldToViewportPoint(result.contactPoint);result.valid=Finite(result.origin)&&Finite(result.direction)&&Finite(result.contactPoint)&&result.direction.sqrMagnitude>.99f;return result;
 }
}
