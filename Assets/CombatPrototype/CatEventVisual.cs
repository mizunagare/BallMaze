using UnityEngine;
// Preserve the original event object, lid transform, collider and consumed flag.
public sealed class CatEventVisual:MonoBehaviour {
 bool done;
 void LateUpdate(){if(done)return;var point=GetComponent<WorldEventPoint>();if(point==null||point.VisualLid==null&&point.Kind==WorldEventKind.Treasure)return;done=true;foreach(var r in GetComponentsInChildren<Renderer>()){r.sharedMaterial=CatWorldArt.Mat(point.Kind==WorldEventKind.Treasure?"Wood":"Stone");var mesh=r.GetComponent<MeshFilter>();if(mesh!=null&&r.GetComponent<BoxCollider>()!=null)mesh.sharedMesh=CatWorldArt.Mesh("Box");}
  var parent=point.Kind==WorldEventKind.Treasure?point.VisualLid:transform;for(int side=-1;side<=1;side+=2)CatWorldArt.Part(parent,"猫族遗迹耳纹","Ear",new Vector3(side*.22f,.45f,.25f),new Vector3(.19f,.28f,.1f),point.Kind==WorldEventKind.Treasure?"Canvas":"Crystal");
 }
}
