using UnityEngine;

// Visual proxies for existing camp facilities, not a new trade/reward system.
public sealed class CatCampVisual:MonoBehaviour {
 GameObject prior,decor;CombatSession s;
 void Awake(){s=GetComponent<CombatSession>();}
 void LateUpdate(){if(s==null||s.Camp==null||s.Camp.PresentationRoot==null)return;var camp=s.Camp.PresentationRoot;if(prior==camp)return;prior=camp;foreach(var renderer in camp.GetComponentsInChildren<MeshRenderer>())if(renderer.name.Contains("树冠")){renderer.GetComponent<MeshFilter>().sharedMesh=CatWorldArt.Mesh("Sphere");renderer.sharedMaterial=CatWorldArt.Mat("Leaf");}if(decor!=null)Destroy(decor);decor=new GameObject("猫族营地功能角色");decor.transform.SetParent(camp.transform,false);
  Spawn("Keeper","仓库管理员",CampRuntime.FacilityOffsets[1]+new Vector3(-1.1f,0,0),170);
  Spawn("Smith","工匠",CampRuntime.FacilityOffsets[2]+new Vector3(0,0,1),170);
  Spawn("Guide","向导猫 · 帮助与教程",new Vector3(-5,0,0),115);
  Spawn("Departure","出征顾问",CampRuntime.FacilityOffsets[3]+new Vector3(1.3f,0,-1),150);
  Spawn("Supplies","物资管理员（共用仓库）",CampRuntime.FacilityOffsets[1]+new Vector3(1.2f,0,0),220);
  CatWorldArt.Part(decor.transform,"营地旗杆","Box",new Vector3(-5,1.45f,3),new Vector3(.1f,2.9f,.1f),"Wood");CatWorldArt.Part(decor.transform,"归途猫耳旗","Box",new Vector3(-4.5f,2.4f,3),new Vector3(1,.6f,.07f),"Red");
  for(int n=0;n<3;n++){CatWorldArt.Part(decor.transform,"物资木箱","Box",new Vector3(5+n%2*.7f,.3f+n/2*.6f,4),new Vector3(.7f,.6f,.6f),"Wood");}
 }
 void Spawn(string kind,string label,Vector3 p,float yaw){var prefab=Resources.Load<GameObject>("CatWorld/Actors/"+kind);if(prefab==null)return;var g=Instantiate(prefab,decor.transform,false);g.name=label;g.transform.localPosition=p;g.transform.localRotation=Quaternion.Euler(0,yaw,0);g.transform.localScale=Vector3.one*(kind=="Keeper"?.72f:kind=="Smith"?.7f:kind=="Guide"?.64f:.66f);}
}
