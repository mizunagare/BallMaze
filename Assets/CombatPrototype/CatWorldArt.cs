using System.Collections.Generic;
using UnityEngine;

// Original B10 geometry recipes. No colliders, RNG, inventory, damage or save writes.
// The Editor baker persists these meshes/materials/prefabs; production loads those assets.
public static class CatWorldArt {
 public static readonly string[] Actors={"Hero","Bandit","Scout","Mushroom","WoodSpirit","Hunter","Lynx","Warden","Tide","Keeper","Smith","Guide","Departure","Supplies"};
 public static readonly string[] Materials={"Fur","Cream","Red","Cloth","Leather","Canvas","Steel","Wood","Leaf","Stone","Water","Amber","White","Orange","Pink","Dark","Crystal"};
 public static readonly Color[] Colors={new Color(.085f,.12f,.16f),new Color(.81f,.81f,.68f),new Color(.7f,.17f,.13f),new Color(.28f,.39f,.27f),new Color(.2f,.12f,.08f),new Color(.63f,.43f,.22f),new Color(.57f,.64f,.69f),new Color(.38f,.23f,.12f),new Color(.3f,.43f,.19f),new Color(.44f,.49f,.52f),new Color(.13f,.58f,.72f),new Color(1,.64f,.16f),new Color(.86f,.87f,.78f),new Color(.75f,.36f,.13f),new Color(.58f,.29f,.29f),new Color(.045f,.055f,.065f),new Color(.26f,.82f,.87f)};
 static readonly Dictionary<string,Material> mats=new Dictionary<string,Material>();static readonly Dictionary<string,Mesh> meshes=new Dictionary<string,Mesh>();
 public static Material Mat(string name){if(mats.TryGetValue(name,out var m)&&m!=null)return m;m=Resources.Load<Material>("CatWorld/Materials/"+name);if(m==null){int n=System.Array.IndexOf(Materials,name);m=new Material(Shader.Find("Universal Render Pipeline/Lit")){name=name,color=Colors[Mathf.Max(0,n)]};m.SetFloat("_Metallic",name=="Steel"?.72f:0);m.SetFloat("_Smoothness",name=="Steel"?.38f:name=="Leather"?.22f:name=="Water"?.65f:.08f);}mats[name]=m;return m;}
 public static Mesh Mesh(string name){if(meshes.TryGetValue(name,out var m)&&m!=null)return m;m=Resources.Load<Mesh>("CatWorld/Meshes/"+name);if(m==null)m=Geometry(name);meshes[name]=m;return m;}
 public static Mesh Geometry(string name){
  if(name=="Cylinder"){var vertices=new List<Vector3>();var normals=new List<Vector3>();var triangles=new List<int>();for(int i=0;i<24;i++){float a=i*Mathf.PI*2/24,b=(i+1)*Mathf.PI*2/24;var n=new Vector3(Mathf.Cos(a),0,Mathf.Sin(a));var m=new Vector3(Mathf.Cos(b),0,Mathf.Sin(b));int k=vertices.Count;vertices.AddRange(new[]{n*.5f-Vector3.up*.5f,n*.5f+Vector3.up*.5f,m*.5f-Vector3.up*.5f,m*.5f+Vector3.up*.5f});normals.AddRange(new[]{n,n,m,m});triangles.AddRange(new[]{k,k+1,k+2,k+1,k+3,k+2});foreach(int side in new[]{-1,1}){k=vertices.Count;vertices.AddRange(new[]{Vector3.up*.5f*side,n*.5f+Vector3.up*.5f*side,m*.5f+Vector3.up*.5f*side});normals.AddRange(new[]{Vector3.up*side,Vector3.up*side,Vector3.up*side});triangles.AddRange(side==1?new[]{k,k+2,k+1}:new[]{k,k+1,k+2});}}var cylinder=new Mesh{name=name};cylinder.SetVertices(vertices);cylinder.SetNormals(normals);cylinder.SetTriangles(triangles,0);cylinder.RecalculateBounds();return cylinder;}
  if(name=="Gem"){var points=new[]{new Vector3(0,.7f,0),new Vector3(0,-.5f,0),new Vector3(-.4f,0,-.3f),new Vector3(.4f,0,-.3f),new Vector3(.4f,0,.3f),new Vector3(-.4f,0,.3f)};var vertices=new List<Vector3>();for(int i=0;i<4;i++)foreach(int tip in new[]{0,1}){var a=points[tip];var b=points[2+i];var c=points[2+(i+1)%4];if(Vector3.Dot(Vector3.Cross(b-a,c-a),(a+b+c)/3)<0){var t=b;b=c;c=t;}vertices.AddRange(new[]{a,b,c});}var jewel=new Mesh{name=name};jewel.SetVertices(vertices);jewel.SetTriangles(System.Linq.Enumerable.ToArray(System.Linq.Enumerable.Range(0,vertices.Count)),0);jewel.RecalculateNormals();jewel.RecalculateBounds();return jewel;}
  if(name=="Ear"){var m=new Mesh{name=name};m.vertices=new[]{new Vector3(-.5f,0,-.23f),new Vector3(.5f,0,-.23f),new Vector3(0,1,-.08f),new Vector3(-.5f,0,.23f),new Vector3(.5f,0,.23f),new Vector3(0,1,.08f)};m.triangles=new[]{0,2,1,3,4,5,0,3,5,0,5,2,1,2,5,1,5,4,0,1,4,0,4,3};m.RecalculateNormals();m.RecalculateBounds();return m;}
  var verts=new List<Vector3>();var norms=new List<Vector3>();var tri=new List<int>();
  const int u=24,v=16;
  if(name=="Sphere"){for(int y=0;y<=v;y++){float a=Mathf.PI*y/v;for(int x=0;x<=u;x++){float b=2*Mathf.PI*x/u;var n=new Vector3(Mathf.Sin(a)*Mathf.Cos(b),Mathf.Cos(a),Mathf.Sin(a)*Mathf.Sin(b));verts.Add(n*.5f);norms.Add(n);if(x<u&&y<v){int i=y*(u+1)+x;tri.AddRange(new[]{i,i+1,i+u+1,i+1,i+u+2,i+u+1});}}}}
  else { // Rounded box with explicit broad bevel normals, shared by clothing and props.
   const int q=6;var axes=new[]{Vector3.right,Vector3.left,Vector3.up,Vector3.down,Vector3.forward,Vector3.back};foreach(var axis in axes){var a=Vector3.Cross(axis,Mathf.Abs(axis.y)>.5f?Vector3.forward:Vector3.up);var b=Vector3.Cross(axis,a);int start=verts.Count;for(int y=0;y<=q;y++)for(int x=0;x<=q;x++){var p=axis*.5f+a*(x/(float)q-.5f)+b*(y/(float)q-.5f);var core=new Vector3(Mathf.Clamp(p.x,-.36f,.36f),Mathf.Clamp(p.y,-.36f,.36f),Mathf.Clamp(p.z,-.36f,.36f));var n=(p-core).normalized;verts.Add(core+n*.14f);norms.Add(n);if(x<q&&y<q){int i=start+y*(q+1)+x;tri.AddRange(new[]{i,i+1,i+q+1,i+1,i+q+2,i+q+1});}}}
  }
  var mesh=new Mesh{name=name};mesh.SetVertices(verts);mesh.SetNormals(norms);mesh.SetTriangles(tri,0);mesh.RecalculateBounds();return mesh;
 }
 public static GameObject Part(Transform root,string name,string shape,Vector3 p,Vector3 size,string material,Vector3 euler=default){var g=new GameObject(name,typeof(MeshFilter),typeof(MeshRenderer));g.layer=2;g.transform.SetParent(root,false);g.transform.localPosition=p;g.transform.localScale=size;g.transform.localRotation=Quaternion.Euler(euler);g.GetComponent<MeshFilter>().sharedMesh=Mesh(shape);g.GetComponent<Renderer>().sharedMaterial=Mat(material);return g;}
 static Transform Group(Transform root,string bone){var g=new GameObject("@"+bone);g.transform.SetParent(root,false);return g.transform;}
 static void Segment(Transform t,string n,Vector3 a,Vector3 b,float width,string mat){var g=Part(t,n,"Sphere",(a+b)*.5f,new Vector3(width,Vector3.Distance(a,b)+width*.4f,width),mat);g.transform.localRotation=Quaternion.FromToRotation(Vector3.up,b-a);}
 public static GameObject Actor(string kind){
  var root=new GameObject("猫族 · "+kind);root.layer=2;bool warden=kind=="Warden",tide=kind=="Tide",hero=kind=="Hero",wood=kind=="WoodSpirit",mush=kind=="Mushroom",elite=kind=="Hunter"||kind=="Lynx";
  string fur=hero?"Fur":tide?"Water":wood?"Wood":kind=="Guide"||kind=="Departure"?"White":kind=="Keeper"||kind=="Smith"?"Orange":elite?"Canvas":"Stone";
  string cloth=hero?"Cloth":warden||wood?"Leaf":tide?"Water":kind=="Scout"?"Canvas":kind=="Guide"?"Water":"Leather";
  var head=Group(root.transform,"head");var chest=Group(root.transform,"chest");var hips=Group(root.transform,"hips");
  Part(head,"猫头","Sphere",new Vector3(0,1.86f,.03f),new Vector3(.87f,.73f,.69f),fur);
  for(int s=-1;s<=1;s+=2){Part(head,"猫耳","Ear",new Vector3(s*.3f,2.08f,.015f),new Vector3(.38f,.43f,.25f),fur,new Vector3(0,0,s*-12));Part(head,"耳内浅色","Ear",new Vector3(s*.3f,2.12f,.145f),new Vector3(.22f,.27f,.045f),warden?"Wood":"Pink",new Vector3(0,0,s*-12));Part(head,"眼眶","Sphere",new Vector3(s*.185f,1.88f,.337f),new Vector3(.19f,.22f,.04f),"Amber");Part(head,"竖瞳","Sphere",new Vector3(s*.185f,1.88f,.363f),new Vector3(.055f,.15f,.023f),"Dark");Part(head,"浅色口鼻","Sphere",new Vector3(s*.09f,1.68f,.33f),new Vector3(.23f,.16f,.14f),"Cream");}
  Part(head,"鼻尖","Ear",new Vector3(0,1.73f,.42f),new Vector3(.105f,.075f,.055f),"Dark",new Vector3(0,0,180));
  Part(chest,"旅行上衣","Box",new Vector3(0,1.12f,0),new Vector3(.58f,.74f,.39f),cloth);
  Part(chest,"肩部浅护甲","Box",new Vector3(0,1.42f,.03f),new Vector3(.64f,.17f,.43f),hero?"Steel":elite?"Steel":cloth);
  Part(chest,"领巾","Box",new Vector3(0,1.55f,.025f),new Vector3(.6f,.16f,.44f),hero?"Red":tide?"Crystal":"Canvas");
  Part(chest,"围巾垂角","Box",new Vector3(-.19f,1.28f,-.3f),new Vector3(.24f,.5f,.075f),hero?"Red":"Canvas",new Vector3(-12,0,-12));
  Part(chest,"帆布背包","Box",new Vector3(0,1.15f,-.32f),new Vector3(.48f,.57f,.26f),"Canvas");Part(chest,"包盖","Box",new Vector3(0,1.41f,-.37f),new Vector3(.5f,.16f,.23f),"Leather");Part(chest,"归途布签","Box",new Vector3(0,1.15f,-.46f),new Vector3(.17f,.24f,.018f),"Cream");
  Part(hips,"腰带","Box",new Vector3(0,.82f,0),new Vector3(.58f,.12f,.42f),"Leather");Part(hips,"裤装","Box",new Vector3(0,.67f,0),new Vector3(.5f,.29f,.37f),"Cloth");
  var tail=Group(root.transform,"hips");for(int i=0;i<5;i++){float a=i*.45f;Part(tail,"尾巴节"+i,"Sphere",new Vector3(.1f+Mathf.Sin(a)*.39f,.69f+i*.045f,-.24f-i*.13f),new Vector3(.17f,.18f,.26f),fur,new Vector3(0,15,0));}
  for(int s=-1;s<=1;s+=2){string side=s<0?".l":".r";var arm=Group(root.transform,"upperarm"+side);var hand=Group(root.transform,"hand"+side);var leg=Group(root.transform,"upperleg"+side);var foot=Group(root.transform,"foot"+side);
   Segment(arm,"袖子",new Vector3(s*.36f,1.38f,0),new Vector3(s*.44f,1.05f,.01f),.25f,cloth);Part(hand,"猫爪手套","Sphere",new Vector3(s*.48f,.91f,.03f),new Vector3(.26f,.3f,.25f),hero?"Leather":fur);Segment(leg,"裤腿",new Vector3(s*.15f,.63f,0),new Vector3(s*.16f,.32f,.01f),.23f,"Cloth");Part(foot,"厚底靴","Box",new Vector3(s*.17f,.19f,.09f),new Vector3(.3f,.35f,.45f),"Leather");}
  if(mush){Part(head,"猫爪菇帽","Sphere",new Vector3(0,2.12f,0),new Vector3(1.32f,.56f,1.1f),"Red");for(int n=0;n<5;n++){float a=n*2.3f;Part(head,"菇帽浅斑","Sphere",new Vector3(Mathf.Cos(a)*.44f,2.32f,Mathf.Sin(a)*.34f),new Vector3(.17f,.05f,.17f),"Cream");}}
  if(warden||wood){for(int s=-1;s<=1;s+=2){Segment(head,"枝角主干",new Vector3(s*.32f,2.03f,-.07f),new Vector3(s*.61f,2.73f,-.05f),.17f,"Wood");Segment(head,"枝角分叉",new Vector3(s*.48f,2.4f,-.05f),new Vector3(s*.87f,2.56f,-.02f),.12f,"Wood");}Part(chest,"古林胸甲","Box",new Vector3(0,1.13f,.27f),new Vector3(.55f,.6f,.14f),"Wood");Part(chest,"林心晶核","Sphere",new Vector3(0,1.19f,.37f),new Vector3(.23f,.29f,.08f),"Crystal");}
  if(elite){for(int s=-1;s<=1;s+=2){Part(head,"猞猁耳簇","Ear",new Vector3(s*.33f,2.42f,.015f),new Vector3(.13f,.2f,.09f),"Dark");Part(chest,"精英肩甲","Box",new Vector3(s*.35f,1.42f,.02f),new Vector3(.27f,.22f,.49f),"Steel");}}
  if(tide){for(int s=-1;s<=1;s+=2)Part(head,"潮灵耳鳍","Ear",new Vector3(s*.36f,1.98f,-.1f),new Vector3(.47f,.65f,.17f),"Crystal",new Vector3(0,0,s*-27));Part(chest,"潮印","Sphere",new Vector3(0,1.16f,.28f),new Vector3(.27f,.38f,.09f),"Crystal");}
  if(kind=="Keeper")Part(chest,"仓库账本","Box",new Vector3(.12f,1.03f,.34f),new Vector3(.37f,.45f,.08f),"Cream");
  if(kind=="Smith"){Part(chest,"工匠围裙","Box",new Vector3(0,1,.24f),new Vector3(.45f,.65f,.04f),"Canvas");Part(chest,"锤柄","Box",new Vector3(.36f,.99f,.22f),new Vector3(.08f,.5f,.08f),"Wood");Part(chest,"锤头","Box",new Vector3(.36f,1.21f,.22f),new Vector3(.35f,.19f,.18f),"Steel");}
  if(kind=="Guide"||kind=="Departure")Part(chest,"路线记录板","Box",new Vector3(0,1.03f,.33f),new Vector3(.5f,.4f,.06f),"Cream");
  return root;
 }
}
