using System;
using System.Linq;
using UnityEngine;

public enum RuinsBossState { Idle, Tracking, Telegraph, Recovery, Dead }
public enum RuinsBossAttack { StoneArc, RuneVolley, SealPulse }
[Serializable] public sealed class RuinsBossTrace {public string stage,attack;public int phase,frame;public float time,before,after;public Vector3 origin,direction,aim;}
[RequireComponent(typeof(CombatEnemy))]
public sealed class RuinsBossBrain:MonoBehaviour {
 public RuinsBossState State {get;private set;}public RuinsBossAttack Attack {get;private set;}
 public int Phase=>enemy!=null&&enemy.Health.Current<=enemy.Health.maxHealth*.5f?2:1;
 public int Releases {get;private set;}public float Remaining=>Mathf.Max(0,until-Time.time);
 public Vector3 Origin {get;private set;}public Vector3 Direction {get;private set;}public Vector3 Aim {get;private set;}
 public event Action<RuinsBossTrace> Observed;
 CombatEnemy enemy;CharacterController controller;EncounterGuard guard;LineRenderer warning;Material warningMaterial;
 float until,readyAt,vertical;int sequence;bool initialized;
 public static float Windup(RuinsBossAttack a)=>a==RuinsBossAttack.StoneArc?1:a==RuinsBossAttack.RuneVolley?1.25f:1.35f;
 public static float Reach(RuinsBossAttack a)=>a==RuinsBossAttack.StoneArc?3.5f:a==RuinsBossAttack.RuneVolley?18:5;
 public static float Recovery(RuinsBossAttack a)=>a==RuinsBossAttack.StoneArc?1.2f:a==RuinsBossAttack.RuneVolley?.9f:1.5f;
 public void Configure(){enemy=GetComponent<CombatEnemy>();controller=GetComponent<CharacterController>();guard=GetComponent<EncounterGuard>();GetComponent<BossBrain>().enabled=false;
  enemy.name="遗迹守护者 · 回响石像";enemy.Health.maxHealth=320;enemy.Health.ResetHealth();enemy.speed=2.1f;enemy.detectionRange=15;enemy.experienceReward=0;
  controller.enabled=false;controller.radius=.6f;controller.height=2.5f;controller.center=Vector3.up*1.25f;controller.enabled=true;
  var go=new GameObject("守护者真实几何预警");go.transform.SetParent(transform,false);warning=go.AddComponent<LineRenderer>();warning.useWorldSpace=true;warning.widthMultiplier=.12f;warning.loop=false;
  warningMaterial=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=new Color(1,.52f,.12f)};warning.sharedMaterial=warningMaterial;warning.enabled=false;readyAt=Time.time+2;initialized=true;
 }
 void Emit(string stage,float before=0,float after=0){Observed?.Invoke(new RuinsBossTrace{stage=stage,attack=Attack.ToString(),phase=Phase,frame=Time.frameCount,time=Time.time,origin=Origin,direction=Direction,aim=Aim,before=before,after=after});}
 void Update(){if(!initialized)return;if(enemy.Health.Dead){Cancel();State=RuinsBossState.Dead;return;}if(enemy.target==null||enemy.target.Health.Dead){Cancel();return;}if(enemy.target.GameplayPaused||Time.timeScale<=0)return;
  if(State==RuinsBossState.Telegraph){if(Time.time>=until)Release();return;}
  if(State==RuinsBossState.Recovery&&Time.time<until){Move(Vector3.zero);return;}
  if(guard.IdleOrReturn(controller,enemy.speed,ref vertical)){State=RuinsBossState.Idle;return;}
  State=RuinsBossState.Tracking;var d=Vector3.ProjectOnPlane(enemy.target.transform.position-transform.position,Vector3.up);
  if(d.sqrMagnitude>.01f)transform.rotation=Quaternion.RotateTowards(transform.rotation,Quaternion.LookRotation(d),90*Time.deltaTime);
  var next=(RuinsBossAttack)(Phase==1?sequence%2:sequence%3);
  if(Time.time>=readyAt&&d.magnitude<=Reach(next)&&enemy.HasSight()){Begin(next);return;}
  Move(d.magnitude>2.5f?guard.Chase(d.normalized*enemy.speed):Vector3.zero);
 }
 void Move(Vector3 direction){if(controller.isGrounded&&vertical<0)vertical=-2;vertical+=Physics.gravity.y*Time.deltaTime;controller.Move((direction+Vector3.up*vertical)*Time.deltaTime);}
 public bool Begin(RuinsBossAttack a){if(!initialized||!isActiveAndEnabled||enemy.Health.Dead||enemy.target==null||enemy.target.Health.Dead||enemy.target.GameplayPaused||Time.timeScale<=0||State==RuinsBossState.Telegraph||Time.time<readyAt)return false;
  if(a<RuinsBossAttack.StoneArc||a>RuinsBossAttack.SealPulse||a==RuinsBossAttack.SealPulse&&Phase<2)return false;
  float flight=a==RuinsBossAttack.RuneVolley?Vector3.Distance(transform.position,enemy.target.transform.position)/8:0;
  if(!enemy.HasAttackSlot(Time.time+Windup(a)+flight,0))return false;
  Attack=a;Origin=transform.position;Aim=enemy.target.transform.position+Vector3.up;Direction=Vector3.ProjectOnPlane(Aim-Origin,Vector3.up).normalized;if(Direction.sqrMagnitude<.01f)Direction=transform.forward;
  State=RuinsBossState.Telegraph;until=Time.time+Windup(a);ShowWarning();Emit("begin");CombatFeedback.Find(this)?.BossWarning(Origin);return true;
 }
 void ShowWarning(){var pts=new System.Collections.Generic.List<Vector3>();float radius=Reach(Attack);float y=Origin.y+.09f;
  if(Attack==RuinsBossAttack.RuneVolley){for(int i=-1;i<=1;i++){var d=Quaternion.Euler(0,i*12,0)*Direction;pts.Add(Origin+Vector3.up*.15f);pts.Add(Origin+d*radius+Vector3.up*.15f);pts.Add(Origin+Vector3.up*.15f);}}
  else {float angle=Attack==RuinsBossAttack.StoneArc?70:180;if(angle<180)pts.Add(Origin+Vector3.up*.09f);for(int i=0;i<=48;i++){var p=Origin+Quaternion.Euler(0,Mathf.Lerp(-angle,angle,i/48f),0)*Direction*radius;p.y=y;pts.Add(p);}if(angle<180)pts.Add(Origin+Vector3.up*.09f);}
  warning.positionCount=pts.Count;warning.SetPositions(pts.ToArray());warning.enabled=true;
 }
 public bool Release(){if(State!=RuinsBossState.Telegraph||Time.time<until||Time.timeScale<=0||enemy.target.GameplayPaused||enemy.Health.Dead)return false;
  warning.enabled=false;Emit("release");Releases++;float before=enemy.target.Health.Current;
  GetComponent<FantasyActorVisual>()?.Attack(Attack==RuinsBossAttack.RuneVolley);
  if(Attack==RuinsBossAttack.RuneVolley){Vector3 from=Origin+Vector3.up*1.4f;var d=(Aim-from).normalized;for(int i=-1;i<=1;i++)EnemyProjectile.Fire(enemy,from,from+Quaternion.Euler(0,i*12,0)*d,12,8,enemy.projectileMaterial,18);enemy.RememberReleasedThreat(Time.time+Vector3.Distance(from,Aim)/8,0);}
  else{
   float range=Reach(Attack);bool contact=Physics.OverlapSphere(Origin+Vector3.up*.7f,range,~0,QueryTriggerInteraction.Ignore).Any(c=>c.GetComponentInParent<ThirdPersonHero>()==enemy.target);
   var offset=Vector3.ProjectOnPlane(enemy.target.transform.position-Origin,Vector3.up);
   bool geometry=offset.magnitude<=range&&(Attack==RuinsBossAttack.SealPulse||offset.sqrMagnitude<.001f||Vector3.Angle(Direction,offset)<=70);
   if(contact&&geometry&&EnemyProjectile.ClearWorldSegment(Origin+Vector3.up*1.3f,enemy.target.transform.position+Vector3.up)){enemy.target.Health.Damage(Attack==RuinsBossAttack.StoneArc?16:14,enemy.target.transform.position+Vector3.up,Direction);Emit("collision-damage",before,enemy.target.Health.Current);}
   else Emit("physical-miss",before,enemy.target.Health.Current);
   CombatFeedback.Find(this)?.ProjectileImpact(Origin+Direction*1.5f);
  }
  sequence++;State=RuinsBossState.Recovery;until=Time.time+Recovery(Attack);readyAt=until+(Phase==1?.65f:.45f);return true;
 }
 void Cancel(){if(warning!=null)warning.enabled=false;if(State!=RuinsBossState.Dead){State=RuinsBossState.Idle;readyAt=Time.time+1;}Emit("cancel");}
 void OnDisable(){Cancel();} // Released EnemyProjectile owns its remaining physical threat.
 void OnDestroy(){if(warningMaterial!=null)Destroy(warningMaterial);}
 void OnGUI(){if(!initialized||enemy.Health.Dead||enemy.target==null||enemy.target.GameplayPaused||Vector3.Distance(enemy.target.transform.position,transform.position)>22)return;var old=CombatUI.Begin();CombatUI.Panel(new Rect(CombatUI.Width/2-210,130,420,65));CombatUI.Text(new Rect(CombatUI.Width/2-200,136,400,52),$"回响石像 · 阶段{Phase}  {enemy.Health.Current:0}/{enemy.Health.maxHealth:0}\n"+(State==RuinsBossState.Telegraph?new[]{"石刃横扫","符文三连矢","封印震波"}[(int)Attack]+$" · {Remaining:0.0}s":"观察收招窗口"),18,CombatUI.Gold);GUI.matrix=old;}
}
