using System.Collections.Generic;
using UnityEngine;

// Read-only geometry. Combat and presentation share the same frozen aim and definitions.
public static class BossWarningGeometry {
 public const float ShoreDot=.2f;
 public static bool IsFan(ForestBossAttack a)=>a==ForestBossAttack.SeedVolley||a==ForestBossAttack.WaterFan;
 public static Vector3 FanDirection(Vector3 source,Vector3 aim,int index)=>Quaternion.Euler(0,(index-2)*13,0)*(aim-source).normalized;
 public static bool Contains(ForestBossAttack a,Vector3 target,Vector3 origin,Vector3 direction,Vector3 locked){
  var d=ForestBossRules.Definition(a);
  if(a==ForestBossAttack.AntlerCharge)return ForestBossRules.InCharge(target,origin,origin+direction*d.range,d.radius);
  if(IsFan(a))return false; // Projectile sphere casts, not an instantaneous ground fan.
  var offset=Vector3.ProjectOnPlane(target-origin,Vector3.up);
  return ForestBossRules.InCircle(target,locked,d.radius)&&(a!=ForestBossAttack.ShoreBite||Vector3.Dot(direction,offset.normalized)>ShoreDot);
 }
 public static Vector3[] Boundary(ForestBossAttack a,Vector3 origin,Vector3 direction,Vector3 locked){
  var d=ForestBossRules.Definition(a);var points=new List<Vector3>();
  if(IsFan(a))return points.ToArray();
  if(a==ForestBossAttack.AntlerCharge){var right=Vector3.Cross(Vector3.up,direction);for(int i=0;i<=32;i++){float t=i*Mathf.PI/32;points.Add(origin+direction*d.range+(direction*Mathf.Sin(t)+right*Mathf.Cos(t))*d.radius);}for(int i=0;i<=32;i++){float t=i*Mathf.PI/32;points.Add(origin+(-direction*Mathf.Sin(t)-right*Mathf.Cos(t))*d.radius);}}
  else if(a==ForestBossAttack.ShoreBite){float angle=Mathf.Acos(ShoreDot)*Mathf.Rad2Deg;points.Add(origin);for(int i=0;i<=48;i++)points.Add(origin+Quaternion.Euler(0,Mathf.Lerp(-angle,angle,i/48f),0)*direction*d.radius);}
  else for(int i=0;i<96;i++){float t=i*Mathf.PI*2/96;points.Add(locked+new Vector3(Mathf.Sin(t),0,Mathf.Cos(t))*d.radius);}
  return points.ToArray();
 }
 public static string Cue(ForestBossAttack a){switch(a){case ForestBossAttack.RootSlam:return "震击 · 离圈";case ForestBossAttack.AntlerCharge:return "冲锋 · 横移";case ForestBossAttack.SeedVolley:return "荆种 · 避线";case ForestBossAttack.WaterFan:return "潮矢 · 避线";case ForestBossAttack.TidalMark:return "潮印 · 离圈";default:return "噬浪 · 绕侧";}}
}
