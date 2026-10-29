using System;using System.IO;using System.Collections.Generic;using UnityEngine;
// Isolated measurement assembly only. The injector and exact source hashes are archived.
public static class BAL01Trace {
 public static int Starts,Releases,DamageEvents,Dodges,XP;public static float Loss;public static string Folder;
 static long sequence;static Dictionary<CombatEnemy,long> keys=new Dictionary<CombatEnemy,long>();static Dictionary<EnemyProjectile,long> shots=new Dictionary<EnemyProjectile,long>();static HashSet<long> released=new HashSet<long>(),hit=new HashSet<long>();
 [Serializable]class Event{public string kind,entity;public long attack;public int frame,xp,levelBefore,levelAfter,remainder;public float time,before,after;public bool invulnerable;}
 static void Write(Event e){if(Folder==null)return;e.frame=Time.frameCount;e.time=Time.time;File.AppendAllText(Folder+"/events.jsonl",JsonUtility.ToJson(e)+"\n");}
 public static void Reset(string folder){Folder=folder;Directory.CreateDirectory(folder);Starts=Releases=DamageEvents=Dodges=XP=0;Loss=0;keys.Clear();shots.Clear();released.Clear();hit.Clear();sequence=0;}
 public static void Begin(CombatEnemy e){keys[e]=++sequence;Starts++;Write(new Event{kind="telegraph",entity=e.entityId,attack=sequence});}
 static long Key(CombatEnemy e){if(!keys.ContainsKey(e))Begin(e);return keys[e];}
 public static void Release(CombatEnemy e){long k=Key(e);released.Add(k);Releases++;Write(new Event{kind="release",entity=e.entityId,attack=k});}
 public static void Shot(EnemyProjectile p,CombatEnemy e){shots[p]=Key(e);Write(new Event{kind="projectile",entity=e.entityId,attack=Key(e)});}
 public static void Direct(CombatEnemy e,ThirdPersonHero h,float damage,Vector3 point,Vector3 direction){Apply(Key(e),e.entityId,h,damage,point,direction);}
 public static void Projectile(EnemyProjectile p,ThirdPersonHero h,float damage,Vector3 point,Vector3 direction){Apply(shots.ContainsKey(p)?shots[p]:0,"projectile",h,damage,point,direction);}
 static void Apply(long k,string id,ThirdPersonHero h,float damage,Vector3 point,Vector3 direction){float before=h.Health.Current;bool inv=h.Dodge.IsInvulnerable;h.Health.Damage(damage,point,direction);float applied=before-h.Health.Current;if(applied>0){hit.Add(k);DamageEvents++;Loss+=applied;}else if(inv)Dodges++;Write(new Event{kind="contact",entity=id,attack=k,before=before,after=h.Health.Current,invulnerable=inv});}
 public static void Award(CombatEnemy e,int amount){bool accepted=!e.target.Health.Dead&&amount>0;int level=e.target.Progression.Level;e.target.Progression.GainExperience(amount);int credited=accepted?amount:0;XP+=credited;Write(new Event{kind="xp",entity=e.entityId,xp=credited,levelBefore=level,levelAfter=e.target.Progression.Level,remainder=e.target.Progression.Experience});}
 public static int HitActions{get{int n=0;foreach(var k in hit)if(released.Contains(k))n++;return n;}}
}
