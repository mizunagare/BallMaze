using UnityEngine;
using System.Linq;

// Presentation only: no colliders, time scaling, damage decisions or random calls.
public sealed class EnemyAttackSignal:MonoBehaviour {
 LineRenderer line;Material material;
 void Awake(){line=GetComponent<LineRenderer>();if(line!=null){if(line.sharedMaterial!=null){material=new Material(line.sharedMaterial);line.sharedMaterial=material;}line.enabled=false;}}
 public void Show(Vector3 origin,Vector3 direction,float range,float halfAngle,bool ranged,Vector3 aim){
  if(line==null)line=gameObject.AddComponent<LineRenderer>();if(material==null){material=new Material(Shader.Find("Universal Render Pipeline/Unlit"));line.sharedMaterial=material;}line.useWorldSpace=true;line.startWidth=line.endWidth=.07f;
  material.color=ranged?new Color(1,.64f,.16f):new Color(1,.3f,.12f);line.enabled=true;
  if(ranged){line.positionCount=2;line.SetPosition(0,origin+Vector3.up*1.25f+direction*.7f);line.SetPosition(1,aim);return;}
  line.positionCount=43;line.SetPosition(0,Ground(origin));line.SetPosition(42,Ground(origin));
  for(int i=0;i<41;i++)line.SetPosition(i+1,Ground(origin+Quaternion.Euler(0,Mathf.Lerp(-halfAngle,halfAngle,i/40f),0)*direction*range));
 }
 static Vector3 Ground(Vector3 p){foreach(var hit in Physics.RaycastAll(p+Vector3.up*5,Vector3.down,10,~0,QueryTriggerInteraction.Ignore).OrderBy(h=>h.distance)){if(hit.collider.GetComponentInParent<CombatEnemy>()!=null||hit.collider.GetComponentInParent<ThirdPersonHero>()!=null)continue;return hit.point+Vector3.up*.08f;}return p+Vector3.up*.08f;}
 public void Hide(){if(line!=null)line.enabled=false;}
 void OnDisable(){Hide();}void OnDestroy(){if(material!=null)Destroy(material);}
}
