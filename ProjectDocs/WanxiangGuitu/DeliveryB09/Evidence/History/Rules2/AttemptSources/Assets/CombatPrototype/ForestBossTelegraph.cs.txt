using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

// No colliders, timers, RNG or combat mutation. Child ownership prevents scene-rebuild remnants.
public sealed class ForestBossTelegraph:MonoBehaviour {
 public Vector3[] Boundary {get;private set;}=new Vector3[0];
 public Vector3[] RayStarts {get;private set;}=new Vector3[0];
 public Vector3[] RayEnds {get;private set;}=new Vector3[0];
 public bool Visible=>gameObject.activeSelf;
 readonly List<LineRenderer> lines=new List<LineRenderer>();Material material;Mesh mesh;MeshRenderer fill;
 public void Show(ForestBossAttack attack,Vector3 origin,Vector3 direction,Vector3 locked,Vector3 source,Vector3 aim){
  gameObject.SetActive(true);if(material==null){material=new Material(Resources.Load<Material>("CombatFeedback/BossWarning"));material.name="首领预警（场景独占）";}
  transform.SetPositionAndRotation(Vector3.zero,Quaternion.identity);
  foreach(var line in lines)line.gameObject.SetActive(false);
  Color color=attack>=ForestBossAttack.WaterFan?new Color(.05f,.85f,1,1):new Color(1,.42f,.05f,1);
  Boundary=BossWarningGeometry.Boundary(attack,origin,direction,locked);RayStarts=RayEnds=new Vector3[0];
  if(BossWarningGeometry.IsFan(attack)){
   if(fill!=null)fill.enabled=false;RayStarts=new Vector3[5];RayEnds=new Vector3[5];
   for(int i=0;i<5;i++){RayStarts[i]=source;var v=BossWarningGeometry.FanDirection(source,aim,i);float distance=ForestBossRules.Definition(attack).range;
    foreach(var hit in Physics.SphereCastAll(source,EnemyProjectile.CollisionRadius,v,distance,~0,QueryTriggerInteraction.Ignore))if(hit.collider.GetComponentInParent<CombatEnemy>()==null&&hit.collider.GetComponentInParent<ThirdPersonHero>()==null)distance=Mathf.Min(distance,hit.distance);
    RayEnds[i]=source+v*distance;var band=color;band.a=.18f;
    Line(i*2,new[]{source,RayEnds[i]},false,band,EnemyProjectile.CollisionRadius*2);
    Line(i*2+1,new[]{source,RayEnds[i]},false,color,.045f);
   }
   Ring(10,source,.65f,color);return;
  }
  var projected=new Vector3[Boundary.Length];for(int i=0;i<projected.Length;i++)projected[i]=Ground(Boundary[i]);
  Line(0,projected,true,color,.11f);
  // Convex shapes: center fan subdivided radially so slopes cannot bury the fill.
  var center=attack==ForestBossAttack.AntlerCharge?origin+direction*ForestBossRules.Definition(attack).range*.5f:locked;
  if(attack==ForestBossAttack.ShoreBite)center=origin+direction*ForestBossRules.Definition(attack).radius*.4f;
  var vertices=new List<Vector3>();var triangles=new List<int>();
  for(int i=0;i<Boundary.Length;i++)for(int ring=0;ring<6;ring++){
   var a=Boundary[i];var b=Boundary[(i+1)%Boundary.Length];float t=ring/6f,u=(ring+1)/6f;
   int k=vertices.Count;vertices.Add(Ground(Vector3.Lerp(center,a,t)));vertices.Add(Ground(Vector3.Lerp(center,a,u)));vertices.Add(Ground(Vector3.Lerp(center,b,u)));vertices.Add(Ground(Vector3.Lerp(center,b,t)));triangles.AddRange(new[]{k,k+1,k+2,k,k+2,k+3});
  }
  if(fill==null){var g=new GameObject("地形贴合危险面");g.transform.SetParent(transform,false);fill=g.AddComponent<MeshRenderer>();fill.shadowCastingMode=ShadowCastingMode.Off;fill.receiveShadows=false;g.AddComponent<MeshFilter>();}
  if(mesh!=null)Destroy(mesh);mesh=new Mesh{name="只读危险区域"};mesh.SetVertices(vertices);mesh.SetTriangles(triangles,0);var colors=new Color[vertices.Count];for(int i=0;i<colors.Length;i++)colors[i]=Color.white;mesh.colors=colors;mesh.RecalculateBounds();fill.GetComponent<MeshFilter>().sharedMesh=mesh;fill.sharedMaterial=material;var block=new MaterialPropertyBlock();block.SetColor("_BaseColor",new Color(color.r,color.g,color.b,.13f));fill.SetPropertyBlock(block);fill.enabled=true;
  Ring(1,Ground(locked),.25f,color);
 }
 void Ring(int index,Vector3 center,float radius,Color color){var p=new Vector3[40];for(int j=0;j<p.Length;j++){float t=j*Mathf.PI*2/p.Length;p[j]=center+new Vector3(Mathf.Sin(t),0,Mathf.Cos(t))*radius;}Line(index,p,true,color,.08f);}
 void Line(int index,Vector3[] positions,bool loop,Color color,float width){while(lines.Count<=index){var g=new GameObject("危险边界");g.transform.SetParent(transform,false);var line=g.AddComponent<LineRenderer>();line.useWorldSpace=true;line.shadowCastingMode=ShadowCastingMode.Off;line.receiveShadows=false;line.numCapVertices=4;lines.Add(line);}var l=lines[index];l.gameObject.SetActive(true);l.sharedMaterial=material;l.startColor=l.endColor=color;l.widthMultiplier=width;l.loop=loop;l.positionCount=positions.Length;l.SetPositions(positions);}
 static Vector3 Ground(Vector3 point){foreach(var h in Physics.RaycastAll(point+Vector3.up*40,Vector3.down,80,~0,QueryTriggerInteraction.Ignore)){if(h.collider.GetComponentInParent<CombatEnemy>()!=null||h.collider.GetComponentInParent<ThirdPersonHero>()!=null)continue;if(h.point.y<=point.y+5)return h.point+Vector3.up*.06f;}return point+Vector3.up*.06f;}
 public void Hide(){gameObject.SetActive(false);}
 void OnDestroy(){if(mesh!=null)Destroy(mesh);if(material!=null)Destroy(material);}
}
