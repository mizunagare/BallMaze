using System.Collections.Generic;using System.Linq;using UnityEngine;

// Renderer-only forest refinement. Existing colliders/nav, coordinates and saved layouts stay authoritative.
[DefaultExecutionOrder(23000)]
public sealed class CatWorldScenery:MonoBehaviour {
 CombatSession s;GameObject previous,root;readonly Dictionary<Renderer,bool> hidden=new Dictionary<Renderer,bool>();
 void Awake(){s=GetComponent<CombatSession>();}
 void LateUpdate(){var region=s?.GetComponent<ForestRegionRuntime>();var current=region?.PresentationRoot;if(current==previous)return;Clear();previous=current;if(current==null)return;root=new GameObject("猫族森林 · 仅表现");root.transform.SetParent(current.transform,false);
  foreach(var r in current.GetComponentsInChildren<Renderer>().ToArray()){if(r.transform.IsChildOf(root.transform))continue;if(r.name=="低多边形树冠"){hidden[r]=r.enabled;r.enabled=false;var p=r.transform.position;for(int i=0;i<3;i++){var g=CatWorldArt.Part(root.transform,"树冠体块","Sphere",Vector3.zero,new Vector3(3.2f,2.65f,3.2f),"Leaf");g.transform.position=p+new Vector3((i-1)*.7f,i==1?.6f:0,i==2?.45f:0);}}
   else if(r.name=="林中岩石"){hidden[r]=r.enabled;r.enabled=false;var g=CatWorldArt.Part(root.transform,"岩体（原碰撞保留）","Box",Vector3.zero,r.bounds.size,"Stone");g.transform.position=r.bounds.center;}
   else if(r.name=="树干")r.sharedMaterial=CatWorldArt.Mat("Wood");
   else if(r.name.Contains("水面"))r.sharedMaterial=CatWorldArt.Mat("Water");
  }
  foreach(var p in region.Layout.points.Where(p=>p.siteKind==ForestSiteKind.Ruins)){for(int i=0;i<3;i++){var at=p.position+new Vector3(-5+i*4,0,5);if(region.Layout.revision>=5)at.y=region.Layout.terrain.Height(region.Layout,at);var g=CatWorldArt.Part(root.transform,"遗迹猫耳石刻（无碰撞）","Ear",Vector3.zero,new Vector3(.5f,.45f,.3f),"Stone");g.transform.position=at+Vector3.up*.3f;}}
  foreach(var exit in current.GetComponentsInChildren<ExtractionPoint>()){var marker=CatWorldArt.Part(root.transform,"猫族归途路牌","Box",Vector3.zero,new Vector3(.75f,.4f,.09f),"Leaf");marker.transform.position=exit.transform.position+new Vector3(1.1f,1.6f,.5f);for(int side=-1;side<=1;side+=2){var ear=CatWorldArt.Part(root.transform,"归途猫耳","Ear",Vector3.zero,new Vector3(.18f,.24f,.08f),"Cream");ear.transform.position=marker.transform.position+new Vector3(side*.25f,.18f,0);}}
 }
 void Clear(){foreach(var p in hidden)if(p.Key!=null)p.Key.enabled=p.Value;hidden.Clear();if(root!=null){root.SetActive(false);Destroy(root);}root=null;}
 void OnDestroy(){Clear();}
}
