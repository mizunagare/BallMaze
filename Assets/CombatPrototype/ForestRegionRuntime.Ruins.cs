using System;using System.Linq;using System.Collections.Generic;using UnityEngine;using UnityEngine.AI;
public partial class ForestRegionRuntime {
 readonly List<NavMeshBuildSource> ruinsFloors=new List<NavMeshBuildSource>();
 readonly List<Collider> ruinsHiddenCollision=new List<Collider>();
 RuinsAssets ruinsAssets;Material ruinsStone,ruinsGold,ruinsDark;
 public void RebuildRuinsNavigation(){
  if(!RuinsLayout.Is(Layout)||root==null)return;var sources=new List<NavMeshBuildSource>(ruinsFloors);
  foreach(var c in root.GetComponentsInChildren<Collider>()){
   if(!c.enabled||c.isTrigger||c is MeshCollider||c is TerrainCollider||c.GetComponentInParent<CombatEnemy>()!=null||c.GetComponentInParent<LootPickup>()!=null)continue;
   sources.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Box,transform=Matrix4x4.TRS(c.bounds.center,Quaternion.identity,Vector3.one),size=c.bounds.size,area=1});
  }
  var settings=NavMesh.GetSettingsByIndex(0);settings.agentRadius=.65f;settings.agentHeight=2.5f;settings.agentClimb=.4f;settings.agentSlope=35;
  var next=NavMeshBuilder.BuildNavMeshData(settings,sources,Layout.WorldBounds,Vector3.zero,Quaternion.identity);if(next==null)throw new InvalidOperationException("遗迹导航构建失败");if(nav.valid)nav.Remove();if(navData!=null)Destroy(navData);navData=next;nav=NavMesh.AddNavMeshData(navData);InvalidateRoutes();
 }
 void BuildRuins(ForestLayout layout){
  layout.Validate();Clear();Layout=AdventureData.Clone(layout);Ready=false;ruinsFloors.Clear();ruinsAssets=RuinsAssets.Load();
  // Only the old scene's static environment is suspended; user asset files are never edited.
  foreach(var c in FindObjectsByType<Collider>(FindObjectsSortMode.None).Where(c=>c.gameObject.scene==gameObject.scene&&c.enabled&&!c.isTrigger&&c.GetComponentInParent<ThirdPersonHero>()==null&&c.GetComponentInParent<CombatEnemy>()==null&&c.GetComponentInParent<LootPickup>()==null)){ruinsHiddenCollision.Add(c);c.enabled=false;}
  root=new GameObject("C1 远古遗迹 · 保存地形与自有模块");UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(root,gameObject.scene);
  var natural=Instantiate(ruinsAssets.terrain,root.transform);natural.name="MapMagic editor-baked TerrainData (no runtime generator)";
  var terrain=natural.GetComponentsInChildren<Terrain>().OrderBy(t=>t.transform.position.z).ThenBy(t=>t.transform.position.x).ToArray();if(terrain.Length!=4)throw new InvalidOperationException("遗迹保存地形块缺失");terrain[0].SetNeighbors(null,terrain[2],terrain[1],null);terrain[1].SetNeighbors(terrain[0],terrain[3],null,null);terrain[2].SetNeighbors(null,null,terrain[3],terrain[0]);terrain[3].SetNeighbors(terrain[2],null,null,terrain[1]);
  foreach(var e in FindObjectsByType<CombatEnemy>(FindObjectsSortMode.None).Where(x=>x.gameObject.scene==gameObject.scene)){hidden.Add(e.gameObject);e.gameObject.SetActive(false);}
  foreach(var n in FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(x=>x.gameObject.scene==gameObject.scene)){hidden.Add(n.gameObject);n.gameObject.SetActive(false);}
  ruinsStone=RuinsMat(new Color(.34f,.40f,.37f));ruinsGold=RuinsMat(new Color(.72f,.56f,.29f));ruinsDark=RuinsMat(new Color(.18f,.23f,.26f));
  RuinsFloor("入口风化石台",-9,9,164,190,0,0);RuinsFloor("石柱广场",-17,17,190,214,0,0);RuinsFloor("机关走廊",-5,5,214,236,0,0);
  Wall("入口西残垣",-9,177,.8f,26,0);Wall("入口东残垣",9,177,.8f,26,0);CrossWall("入口后封石",0,164,18,0);
  Wall("广场西墙",-17,202,.8f,24,0);Wall("广场东墙",17,202,.8f,24,0);CrossWall("广场南左",-13,190,8,0);CrossWall("广场南右",13,190,8,0);CrossWall("门廊左",-11,214,12,0);CrossWall("门廊右",11,214,12,0);
  Wall("走廊西墙",-5.5f,225,1,22,0);Wall("走廊东墙",5.5f,225,1,22,0);
  for(int z=196;z<=210;z+=14)for(int side=-1;side<=1;side+=2)Column(new Vector3(side*12,0,z),4.7f);
  Place(RuinsModule.Arch,"入口拱门",new Vector3(0,2,188),new Vector3(12,4,1.2f));Place(RuinsModule.Arch,"机关门廊",new Vector3(0,2.3f,218),new Vector3(10.8f,4.6f,1));
  GameObject seal=null;
  if(Layout.ruinsStage==5){
   RuinsFloor("下行通道",-4,4,236,244,0,-3);RuinsFloor("地下祭坛",-24,6,244,264,-3,-3);RuinsFloor("隐秘藏室",-34,-24,248,260,-3,-3);RuinsFloor("上行石桥",-4,4,264,274,-3,0);RuinsFloor("守护者大厅",-18,32,274,304,0,0);
   Wall("下阶西壁",-5.5f,240,1,8,-3);Wall("下阶东壁",5.5f,240,1,8,-3);Wall("祭坛东壁",6,254,1,20,-3);Wall("祭坛西南",-24,246,1,4,-3);Wall("祭坛西北",-24,260,1,8,-3);CrossWall("祭坛南壁",-15,244,18,-3);CrossWall("祭坛北壁",-15,264,18,-3);Wall("密室外壁",-34,254,1,12,-3);CrossWall("密室南壁",-29,248,10,-3);CrossWall("密室北壁",-29,260,10,-3);
   Wall("桥西护栏",-4.5f,269,.6f,10,-3);Wall("桥东护栏",4.5f,269,.6f,10,-3);Wall("大厅西墙",-18,289,1,30,0);Wall("大厅东墙",32,289,1,30,0);CrossWall("大厅北墙",7,304,50,0);CrossWall("大厅南左",-11,274,14,0);CrossWall("大厅南右",18,274,28,0);
   Place(RuinsModule.Roof,"地下顶盖",new Vector3(-14,2.3f,254),new Vector3(21,.6f,20));
   Place(RuinsModule.Altar,"猫族祭坛",new Vector3(-17,-2.7f,255),new Vector3(3,.6f,3));Place(RuinsModule.Rune,"碑文符石",new Vector3(-17,-1.1f,255),Vector3.one*.55f);
   for(int z=280;z<=298;z+=18)for(int x=-12;x<=26;x+=38)Column(new Vector3(x,0,z),5.8f);Column(new Vector3(-20,-3,249),3.8f);Column(new Vector3(-20,-3,261),3.8f);
   foreach(var pos in new[]{new Vector3(-8,0,280),new Vector3(22,0,280)}){var prefab=Resources.Load<GameObject>("CatWorld/Actors/Warden");if(prefab==null)throw new InvalidOperationException("现有猫族雕像资源缺失");var statue=Instantiate(prefab,root.transform);statue.name="石化猫族守护像";statue.transform.position=pos;statue.transform.localScale=Vector3.one*1.15f;foreach(var c in statue.GetComponentsInChildren<Collider>())c.enabled=false;foreach(var r in statue.GetComponentsInChildren<Renderer>())r.sharedMaterial=ruinsStone;var body=statue.AddComponent<BoxCollider>();body.center=Vector3.up*1.4f;body.size=new Vector3(2,2.8f,2);}
   seal=Place(RuinsModule.Door,"藏室封石",new Vector3(-24,-1.2f,254),new Vector3(.9f,3.6f,8));
  }else CrossWall("前三地区原型终点",0,236,10,0);
  var events=RuinsLayout.Events(Layout.ruinsStage);var saved=S.Flow.ActiveRun?.checkpoint?.events;foreach(var e in events)e.used=RuinsLayout.Used(saved,e.entityId);S.Events.RestoreEvents(events);
  foreach(var exit in Layout.exits){var g=new GameObject(exit.label);g.transform.SetParent(root.transform);g.AddComponent<ExtractionPoint>().Configure(exit,true);Place(RuinsModule.Altar,exit.label+"归途纹章",exit.position-Vector3.up*.05f,new Vector3(2,.1f,2),false).transform.SetParent(g.transform,true);}
  var exploration=GetComponent<RuinsExploration>()??gameObject.AddComponent<RuinsExploration>();exploration.Configure(this,Place(RuinsModule.Door,"符文石门",new Vector3(0,1.8f,220),new Vector3(10,3.6f,.9f)),seal);
  Physics.SyncTransforms();RebuildRuinsNavigation();
  S.enemies=Layout.encounters.Select(e=>{var actor=S.Waves.CreateEncounter(root.transform,e.id,e.home,(EnemyArchetype)e.type);actor.gameObject.AddComponent<EncounterGuard>().Configure(this,e);if(e.id=="c1:guardian")actor.gameObject.AddComponent<RuinsBossBrain>().Configure();else actor.name=e.type==2?"遗迹精英 · 石甲卫":"遗迹守卫";return actor;}).ToArray();Physics.SyncTransforms();
  if(!PathComplete(Layout.entry,Layout.points[1].position)||!TryInteractionApproach(Layout.exits[0],out _))throw new InvalidOperationException("遗迹安全入口或免费出口不可达");Ready=true;InvalidateRoutes();
 }
 void RestoreRuinsCollision(){foreach(var c in ruinsHiddenCollision)if(c!=null)c.enabled=true;ruinsHiddenCollision.Clear();ruinsAssets=null;}
 Material RuinsMat(Color c){var m=new Material(Shader.Find("Universal Render Pipeline/Lit")){color=c};m.SetFloat("_Smoothness",.12f);materials.Add(m);return m;}
 GameObject Place(RuinsModule type,string name,Vector3 p,Vector3 scale,bool collide=true){var g=Instantiate(ruinsAssets.Module(type),root.transform);g.name=name;g.transform.position=p;g.transform.localScale=scale;if(!collide)foreach(var c in g.GetComponentsInChildren<Collider>())c.enabled=false;return g;}
 void Wall(string name,float x,float z,float width,float length,float floor){int pieces=Mathf.CeilToInt(length/3);for(int n=0;n<pieces;n++)Place(RuinsModule.Block,name+" "+n,new Vector3(x,floor+1.8f,z-length/2+(n+.5f)*length/pieces),new Vector3(width,3.6f,length/pieces));}
 void CrossWall(string name,float x,float z,float width,float floor){int pieces=Mathf.CeilToInt(width/3);for(int n=0;n<pieces;n++)Place(RuinsModule.Block,name+" "+n,new Vector3(x-width/2+(n+.5f)*width/pieces,floor+1.8f,z),new Vector3(width/pieces,3.6f,.8f));}
 void Column(Vector3 p,float h){Place(RuinsModule.Column,"猫族十棱石柱",p+Vector3.up*h/2,new Vector3(2,h,2));}
 void RuinsFloor(string name,float x0,float x1,float z0,float z1,float y0,float y1){var mesh=new Mesh{name=name};mesh.vertices=new[]{new Vector3(x0,y0,z0),new Vector3(x0,y1,z1),new Vector3(x1,y1,z1),new Vector3(x1,y0,z0)};mesh.triangles=new[]{0,1,2,0,2,3};mesh.uv=new[]{new Vector2(x0,z0)/4,new Vector2(x0,z1)/4,new Vector2(x1,z1)/4,new Vector2(x1,z0)/4};mesh.RecalculateNormals();terrainMeshes.Add(mesh);var g=new GameObject(name,typeof(MeshFilter),typeof(MeshRenderer),typeof(MeshCollider));g.transform.SetParent(root.transform,false);g.GetComponent<MeshFilter>().sharedMesh=mesh;g.GetComponent<MeshCollider>().sharedMesh=mesh;g.GetComponent<MeshRenderer>().sharedMaterial=ruinsStone;ruinsFloors.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Mesh,sourceObject=mesh,transform=Matrix4x4.identity,area=0});}
}
