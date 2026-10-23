using System;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
public class ForestRegionRuntime:MonoBehaviour {
 public ForestLayout Layout {get;private set;}public bool Active=>root!=null&&root.activeSelf;
 GameObject root;readonly List<GameObject> hidden=new List<GameObject>();readonly List<Material> materials=new List<Material>();NavMeshDataInstance nav;NavMeshData navData;
 CombatSession S=>GetComponent<CombatSession>();
 public bool Ready {get;private set;}
 [NonSerialized] public Action<string> ValidationHook;
 [NonSerialized] public Func<int,ForestLayout> LayoutFactory;
 public bool MatchesActors(CombatEnemy[] actors)=>Ready&&Layout!=null&&actors!=null&&actors.Length==Layout.encounters.Length&&actors.All(a=>a!=null&&!string.IsNullOrEmpty(a.entityId))&&actors.Select(a=>a.entityId).Distinct().Count()==actors.Length&&Layout.encounters.All(e=>actors.Any(a=>a.entityId==e.id));
 public void GeneratePlayable(int seed){
  for(int attempt=0;attempt<3;attempt++){try{var layout=LayoutFactory==null?ForestLayout.Generate(unchecked(seed+attempt)):LayoutFactory(unchecked(seed+attempt));layout.requestedSeed=seed;layout.generationAttempt=attempt;Build(layout,true);return;}catch(Exception e){Debug.LogWarning("森林生成重试 "+attempt+"："+e.Message);}}
  var safe=ForestLayout.Generate(1);safe.requestedSeed=seed;safe.fallback=true;safe.generationAttempt=3;Build(safe,true);Debug.LogWarning("森林采用备用布局 seed=1，请求="+seed);
 }
 public void Build(ForestLayout layout,bool newGeneration=false){Ready=false;ValidationHook?.Invoke("before-build");layout.Validate();Clear();Layout=AdventureData.Clone(layout);layout=Layout;root=new GameObject("ForestRuins 森林布局测试");UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(root,gameObject.scene);
  var templates=FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(n=>n.gameObject.scene==gameObject.scene).GroupBy(n=>n.kind).ToDictionary(g=>g.Key,g=>g.First());
  foreach(var node in templates.Values.SelectMany(t=>FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(n=>n.kind==t.kind&&n.gameObject.scene==gameObject.scene)).Distinct()){hidden.Add(node.gameObject);node.gameObject.SetActive(false);}
  foreach(var e in FindObjectsByType<CombatEnemy>(FindObjectsSortMode.None).Where(e=>e.gameObject.scene==gameObject.scene)){hidden.Add(e.gameObject);e.gameObject.SetActive(false);}
  Part("森林地面",new Vector3(layout.boundsCenter.x,-.5f,layout.boundsCenter.z),new Vector3(layout.boundsSize.x,1,layout.boundsSize.z),new Color(.18f,.29f,.19f));
  Part("西边界",new Vector3(-94,1,242),new Vector3(1,3,186),Color.gray);Part("东边界",new Vector3(94,1,242),new Vector3(1,3,186),Color.gray);Part("南边界",new Vector3(0,1,150),new Vector3(188,3,1),Color.gray);Part("北边界",new Vector3(0,1,334),new Vector3(188,3,1),Color.gray);
  foreach(var r in layout.routes){var a=layout.points.First(p=>p.id==r.from).position;var b=layout.points.First(p=>p.id==r.to).position;var obj=Part("小径",(a+b)/2+Vector3.up*.012f,new Vector3(5,.02f,Vector3.Distance(a,b)),new Color(.38f,.34f,.24f),false);obj.transform.rotation=Quaternion.LookRotation(b-a);}
  foreach(var p in layout.points){var marker=Part(p.label,p.position+Vector3.up*.03f,new Vector3(13,.04f,13),p.risk==3?new Color(.35f,.18f,.2f):new Color(.3f,.36f,.24f),false);}
  foreach(var rock in layout.rocks){Part("林中岩石",rock+Vector3.up,new Vector3(2.4f,2,2.4f),new Color(.28f,.32f,.31f));var trunk=Part("树干",rock+Vector3.right*2.5f+Vector3.up*2,new Vector3(.6f,4,.6f),new Color(.28f,.18f,.1f));Part("低多边形树冠",trunk.transform.position+Vector3.up*2.5f,new Vector3(3.7f,3.7f,3.7f),new Color(.16f,.36f,.22f),false);}
  foreach(var n in layout.nodes){AdventureResource node;if(templates.TryGetValue((MaterialKind)(n.kind+3),out var template)){node=Instantiate(template,root.transform);node.gameObject.SetActive(true);node.transform.position=n.position;}else{var obj=Part("采集节点",n.position+Vector3.up,new Vector3(1,2,1),Color.gray);node=obj.AddComponent<AdventureResource>();node.kind=(MaterialKind)(n.kind+3);}node.entityId=n.id;node.nodeId=10000+Array.IndexOf(layout.nodes,n);node.Restore(node.maxHealth);}
  S.Events.RestoreEvents(layout.points.Where(p=>p.id!="poi:0").SelectMany(p=>new[]{new SavedWorldEvent{entityId=p.id+":chest",kind=WorldEventKind.Treasure,position=p.position+Vector3.right*3},new SavedWorldEvent{entityId=p.id+":altar",kind=WorldEventKind.Altar,position=p.position+Vector3.back*3}}).ToArray());
  foreach(var exit in layout.exits){var point=new GameObject(exit.label);point.transform.SetParent(root.transform);point.AddComponent<ExtractionPoint>().Configure(exit,true);var basePart=Part(exit.label,exit.position+Vector3.up*.1f,new Vector3(2,.2f,2),Color.cyan,false);var beacon=Part("撤离光柱",exit.position+Vector3.up*1.5f,new Vector3(.25f,3,.25f),Color.cyan,false);basePart.transform.SetParent(point.transform,true);beacon.transform.SetParent(point.transform,true);}
  Physics.SyncTransforms();ValidationHook?.Invoke("before-nav");BuildNavigation(newGeneration);ValidationHook?.Invoke("after-nav");
  S.enemies=layout.encounters.Select(d=>{var e=S.Waves.CreateEncounter(root.transform,d.id,d.home,(EnemyArchetype)d.type);var guard=e.gameObject.AddComponent<EncounterGuard>();guard.Configure(this,d);return e;}).ToArray();Physics.SyncTransforms();Ready=true;
 }
 GameObject Part(string label,Vector3 p,Vector3 scale,Color color,bool collision=true){var obj=GameObject.CreatePrimitive(PrimitiveType.Cube);obj.name=label;obj.transform.SetParent(root.transform);obj.transform.position=p;obj.transform.localScale=scale;if(!collision){obj.GetComponent<Collider>().enabled=false;}var mat=new Material(Shader.Find("Universal Render Pipeline/Lit")){color=color};materials.Add(mat);obj.GetComponent<Renderer>().sharedMaterial=mat;return obj;}
 void BuildNavigation(bool newGeneration){var sources=new List<NavMeshBuildSource>();foreach(var c in root.GetComponentsInChildren<Collider>()){if(!c.enabled||c.isTrigger)continue;var b=c.bounds;sources.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Box,transform=Matrix4x4.TRS(b.center,Quaternion.identity,Vector3.one),size=b.size,area=0});}
  // Event collision is included even though its existing owner is outside the forest root.
  foreach(var c in S.Events.Points.SelectMany(p=>p.GetComponentsInChildren<Collider>())){if(!c.enabled||c.isTrigger)continue;var b=c.bounds;sources.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Box,transform=Matrix4x4.TRS(b.center,Quaternion.identity,Vector3.one),size=b.size,area=0});}
  if(NavMesh.GetSettingsCount()==0)throw new InvalidOperationException("缺少导航代理配置");var settings=NavMesh.GetSettingsByIndex(0);settings.agentRadius=.65f;settings.agentHeight=2.5f;settings.agentClimb=.35f;navData=NavMeshBuilder.BuildNavMeshData(settings,sources,new Bounds(Layout.boundsCenter,Layout.boundsSize),Vector3.zero,Quaternion.identity);if(navData==null)throw new InvalidOperationException("森林导航生成失败");nav=NavMesh.AddNavMeshData(navData);
  foreach(var poi in Layout.points)if(!PathComplete(Layout.entry,poi.position))throw new InvalidOperationException("兴趣点无可通行导航："+poi.label);
  foreach(var exit in Layout.exits)if(!TryInteractionApproach(exit,out _))throw new InvalidOperationException("出口互动范围不可达："+exit.id);
  foreach(var encounter in Layout.encounters){
   if(newGeneration){if(!TryGround(encounter.home,6,out var candidate)||!PathComplete(Layout.entry,candidate))throw new InvalidOperationException("敌人出生点无安全候选："+encounter.id);encounter.home=candidate+Vector3.up*.1f;}
   if(!TryGround(encounter.home,1.25f,out var home)||Vector3.ProjectOnPlane(home-encounter.home,Vector3.up).magnitude>.75f||!PathComplete(Layout.entry,home))throw new InvalidOperationException("敌人出生点不可达："+encounter.id);
  }
 }
 public bool TryGround(Vector3 p,float range,out Vector3 grounded){grounded=p;bool ok=NavMesh.SamplePosition(p,out var hit,range,NavMesh.AllAreas);if(ok)grounded=hit.position;return ok;}
 public bool TryInteractionApproach(ExtractionConfig exit,out Vector3 approach){
  for(int ring=0;ring<3;ring++)for(int i=0;i<16;i++){float angle=i*Mathf.PI/8;float radius=ring==0?0:exit.range*(ring==1?.45f:.8f);Vector3 candidate=exit.position+new Vector3(Mathf.Cos(angle)*radius,0,Mathf.Sin(angle)*radius);
   if(TryGround(candidate,1.5f,out approach)&&Vector3.Distance(approach+Vector3.up*.1f,exit.position)<exit.range-.15f&&PathComplete(Layout.entry,approach))return true;
  }approach=default;return false;
 }
 public ForestLayout Capture(){if(!Active)return null;var copy=AdventureData.Clone(Layout);copy.exits=FindObjectsByType<ExtractionPoint>(FindObjectsSortMode.None).Where(p=>p.forest&&p.gameObject.scene==gameObject.scene).Select(p=>p.Capture()).OrderBy(p=>p.id).ToArray();return copy;}
 public bool PathComplete(Vector3 from,Vector3 to){var path=new NavMeshPath();return NavMesh.SamplePosition(from,out var a,3,NavMesh.AllAreas)&&NavMesh.SamplePosition(to,out var b,3,NavMesh.AllAreas)&&NavMesh.CalculatePath(a.position,b.position,NavMesh.AllAreas,path)&&path.status==NavMeshPathStatus.PathComplete;}
 public void Clear(){Ready=false;if(root!=null){root.SetActive(false);Destroy(root);root=null;}if(nav.valid)nav.Remove();if(navData!=null)Destroy(navData);foreach(var g in hidden)if(g!=null)g.SetActive(true);hidden.Clear();foreach(var m in materials)if(m!=null)Destroy(m);materials.Clear();Layout=null;}
 void OnDestroy(){Clear();}
 void OnGUI(){if(!Active||S.Flow.BlockCombat||S.hero.Inventory.IsOpen||S.hero.Progression.IsChoosing)return;CombatChineseUI.Apply();GUI.Box(new Rect(15,175,265,255),"森林布局测试 · 路线\n林间入口 → 伐木林地 / 碎岩矿脉\n林地 → 遗迹营地 → 归途祭坛\n矿脉 → 精英哨站 → 湖岸物资点\n遗迹与哨站间可横向绕行\n蓝色装置：靠近按 H 撤离\n普通遭遇可绕开，无清场要求");float y=370;foreach(var p in Layout.points.OrderBy(p=>Vector3.Distance(p.position,S.hero.transform.position)).Take(3)){GUI.Label(new Rect(30,y,250,25),p.label+"  "+Vector3.Distance(p.position,S.hero.transform.position).ToString("0")+"米");y+=25;}}
}
