using System;using UnityEngine;
// Selection/intents only. Never applies Damage, moves a target, or consumes RNG.
public sealed class TargetAssist:MonoBehaviour {
 public CombatEnemy Selected {get;private set;}public Vector3 IntentPoint {get;private set;}public float Score {get;private set;}public string Reason {get;private set;}="FREE";
 ThirdPersonHero hero;CombatEnemy[] candidates=Array.Empty<CombatEnemy>();float nextScan,pendingSince;CombatEnemy pending;float previousYaw;int observedFrame=-1;bool turning;
 public float screenRadius=.15f,angleLimit=12,retention=1.25f,switchMargin=.12f,switchDelay=.15f;
 void Awake(){hero=GetComponent<ThirdPersonHero>();}
 public void Clear(){Selected=pending=null;Score=0;Reason="FREE";nextScan=0;observedFrame=-1;}
 bool Ready=>hero!=null&&!hero.Health.Dead&&!hero.GameplayPaused&&!hero.Dodge.IsRolling&&AdventureFlow.Find(hero)?.BlockCombat!=true&&Time.timeScale>0&&PlayerInput.Focused&&!PlayerInput.UIBlocked;
 public CombatEnemy Choose(Vector3 muzzle,float reach,bool melee=false){
  if(!Ready){Clear();return null;}var camera=CombatAim.CameraFor(hero);if(camera==null){Clear();return null;}
  if(observedFrame!=Time.frameCount){var orbit=camera.GetComponent<OrbitCamera>();float yaw=orbit.ViewYaw;turning=observedFrame>=0&&Mathf.Abs(Mathf.DeltaAngle(previousYaw,yaw))>Mathf.Max(.5f,80*Time.deltaTime);previousYaw=yaw;observedFrame=Time.frameCount;}
  if(Time.time>=nextScan){candidates=UnityEngine.Object.FindObjectsByType<CombatEnemy>();nextScan=Time.time+.1f;}
  CombatEnemy best=null;Vector3 bestPoint=default,oldPoint=default;float bestScore=float.NegativeInfinity,oldScore=float.NegativeInfinity,bestError=0,oldError=float.PositiveInfinity;
  foreach(var enemy in candidates){if(!Candidate(enemy,camera,muzzle,reach,melee,out var point,out var error,out var angle,out var distance))continue;float score=.45f*(1-error/screenRadius)+.20f*(1-distance/Mathf.Max(.01f,reach))+.20f*(1-angle/angleLimit)+(enemy==Selected&&!turning?.15f:0);
   if(enemy==Selected){oldScore=score;oldPoint=point;oldError=error;}
   if(score>bestScore+.00001f||Mathf.Abs(score-bestScore)<.00001f&&string.CompareOrdinal(Key(enemy),Key(best))<0){best=enemy;bestPoint=point;bestScore=score;bestError=error;}}
  if(best==null){Selected=pending=null;Score=0;Reason="FREE";return null;}
  bool replace=Selected==null||float.IsNegativeInfinity(oldScore)||(turning&&bestError<oldError*.6f);
  if(best!=Selected&&!replace){if(bestScore<oldScore+switchMargin){pending=null;best=Selected;bestPoint=oldPoint;bestScore=oldScore;}else{if(pending!=best){pending=best;pendingSince=Time.time;}if(Time.time-pendingSince<switchDelay){best=Selected;bestPoint=oldPoint;bestScore=oldScore;}else replace=true;}}
  if(best!=Selected)Reason=replace?"ACQUIRE_OR_INTENT_SWITCH":"HYSTERESIS_SWITCH";else Reason="RETAIN";
  Selected=best;IntentPoint=bestPoint;Score=bestScore;return Selected;
 }
 static string Key(CombatEnemy e)=>e==null?"":!string.IsNullOrEmpty(e.entityId)?e.entityId:e.gameObject.scene.handle+":"+e.transform.GetSiblingIndex();
 bool Candidate(CombatEnemy e,Camera camera,Vector3 muzzle,float reach,bool melee,out Vector3 point,out float error,out float angle,out float distance){
  point=default;error=angle=distance=0;if(e==null||!e.isActiveAndEnabled||e.Health==null||e.Health.Dead||e.gameObject.scene!=hero.gameObject.scene)return false;var c=e.GetComponent<CharacterController>();if(c==null||!c.enabled)return false;
  var ray=camera.ViewportPointToRay(new Vector3(.5f,.5f));var center=c.bounds.center;float projection=Vector3.Dot(center-ray.origin,ray.direction);if(projection<=0)return false;point=c.ClosestPoint(ray.GetPoint(projection));var view=camera.WorldToViewportPoint(point);if(view.z<=0||view.x<0||view.x>1||view.y<0||view.y>1)return false;
  error=new Vector2((view.x-.5f)*camera.aspect,view.y-.5f).magnitude;angle=Vector3.Angle(camera.transform.forward,point-camera.transform.position);float retain=e==Selected?retention:1;
  if(error>screenRadius*retain||angle>angleLimit*retain)return false;distance=Vector3.Distance(melee?MeleeGeometry.Center(hero.transform.position):muzzle,point);if(distance>reach)return false;
  if(melee){var horizontal=Vector3.ProjectOnPlane(point-hero.transform.position,Vector3.up);if(Vector3.Dot(hero.transform.forward,horizontal)<0)return false;}
  return CameraSight(ray.origin,point,e)&&Reachable(muzzle,point,e);
 }
 bool CameraSight(Vector3 origin,Vector3 point,CombatEnemy target){var inside=CombatAim.InitialContact(origin,hero);if(inside!=null&&inside.GetComponentInParent<CombatEnemy>()!=target)return false;float closest=float.PositiveInfinity;Collider first=null;foreach(var h in Physics.RaycastAll(origin,(point-origin).normalized,Vector3.Distance(origin,point)+.002f,~0,QueryTriggerInteraction.Ignore))if(CombatAim.Legal(h.collider,hero)&&h.distance<closest){closest=h.distance;first=h.collider;}return first==null||first.GetComponentInParent<CombatEnemy>()==target;}
 bool Reachable(Vector3 origin,Vector3 point,CombatEnemy target){var initial=CombatAim.InitialContact(origin,hero);if(initial!=null)return initial.GetComponentInParent<CombatEnemy>()==target;var d=point-origin;if(d.sqrMagnitude<.000001f)return false;return !CombatAim.Sweep(origin,d.normalized,d.magnitude+.002f,hero,out var hit)||hit.collider.GetComponentInParent<CombatEnemy>()==target;}
 public RangedAimSolution Solve(RangedAimSolution free,float reach){
  if(!CombatAssistOptions.Ranged)return free;if(free.barrelBlocked||!free.valid){Clear();return free;}
  var target=Choose(free.origin,reach);if(target==null)return free;Vector3 d=IntentPoint-free.origin;if(d.sqrMagnitude<.000001f)return free;
  // Preserve CP04-B's near surface / no backwards fire policy without changing CombatAim.
  var c=target.GetComponent<CharacterController>();if(Vector3.Dot(d,free.cameraDirection)<=.001f){Vector3 anchor=hero.transform.position+Vector3.up*1.25f;if(Vector3.Dot(c.bounds.center-free.origin,free.cameraDirection)<=.001f||Vector3.Dot(c.bounds.center-anchor,Vector3.ProjectOnPlane(free.cameraDirection,Vector3.up))<=.001f)return free;}
  if(!Reachable(free.origin,IntentPoint,target))return free;var result=free;result.intentPoint=IntentPoint;result.direction=d.normalized;result.reason="ASSIST_MUZZLE_TO_TARGET";result.fanUp=Vector3.ProjectOnPlane(Vector3.up,result.direction).normalized;if(result.fanUp.sqrMagnitude<.001f)result.fanUp=free.camera.transform.up;
  result.hasContact=false;result.contactCollider=null;result.contactPoint=result.origin+result.direction*reach;var initial=CombatAim.InitialContact(result.origin,hero);if(initial!=null){result.hasContact=true;result.contactCollider=initial;result.contactPoint=CombatAim.OverlapPoint(initial,result.origin);}else if(CombatAim.Sweep(result.origin,result.direction,reach,hero,out var hit)){result.hasContact=true;result.contactCollider=hit.collider;result.contactPoint=hit.point;}
  result.obstructed=result.barrelBlocked||result.contactCollider!=null&&!CombatAim.SameOwner(result.contactCollider,c);result.viewport=result.camera.WorldToViewportPoint(result.contactPoint);return result;
 }
 public Vector3 Facing(Vector3 fallback){if(!CombatAssistOptions.Ranged||Selected==null||!Ready||hero.MoveDirection.sqrMagnitude>.01f)return fallback;var camera=CombatAim.CameraFor(hero);if(camera==null||!Candidate(Selected,camera,hero.GetComponent<AdventureCombat>().MuzzlePosition,60,false,out var point,out _,out _,out _))return fallback;return Vector3.ProjectOnPlane(point-hero.transform.position,Vector3.up);}
 void Update(){var c=hero==null?null:hero.GetComponent<AdventureCombat>();bool ranged=c?.Gear!=null&&(int)c.Gear.Weapon>=2;if(!Ready||(ranged?!CombatAssistOptions.Ranged:!CombatAssistOptions.Melee)||Selected!=null&&(!Selected.isActiveAndEnabled||Selected.Health.Dead))Clear();}
 void OnDisable(){Clear();}void OnApplicationFocus(bool value){if(!value)Clear();}
 void OnGUI(){if(Selected==null||!Ready)return;var combat=hero.GetComponent<AdventureCombat>();if((int)combat.Gear.Weapon<2&&combat.PendingAttackCount==0)return;var camera=CombatAim.CameraFor(hero);if(camera==null)return;var p=camera.WorldToViewportPoint(IntentPoint);if(p.z<=0)return;GUI.Box(new Rect(p.x*Screen.width-10,(1-p.y)*Screen.height-10,20,20),"");CombatUI.Text(new Rect(12,125,600,24),"辅助意图 · "+Selected.DisplayName+" · "+Reason,16);}
}
