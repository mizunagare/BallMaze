using System;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
public partial class ForestRegionRuntime {
 readonly List<NavMeshBuildSource> ruinsFloors=new List<NavMeshBuildSource>();
 Material ruinsStone,ruinsGold,ruinsDark;
 public void RebuildRuinsNavigation(){
  if(!RuinsLayout.Is(Layout)||root==null)return;
  var sources=new List<NavMeshBuildSource>(ruinsFloors);
  foreach(var c in root.GetComponentsInChildren<Collider>()){
   if(!c.enabled||c.isTrigger||c is MeshCollider||c.GetComponentInParent<CombatEnemy>()!=null||c.GetComponentInParent<LootPickup>()!=null)continue;
   sources.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Box,transform=Matrix4x4.TRS(c.bounds.center,Quaternion.identity,Vector3.one),size=c.bounds.size,area=1});
  }
  var settings=NavMesh.GetSettingsByIndex(0);settings.agentRadius=.65f;settings.agentHeight=2.5f;settings.agentClimb=.4f;settings.agentSlope=35;
  var next=NavMeshBuilder.BuildNavMeshData(settings,sources,Layout.WorldBounds,Vector3.zero,Quaternion.identity);
  if(next==null)throw new InvalidOperationException("遗迹导航构建失败");
  if(nav.valid)nav.Remove();if(navData!=null)Destroy(navData);navData=next;nav=NavMesh.AddNavMeshData(navData);InvalidateRoutes();
 }
 void BuildRuins(ForestLayout layout){
  layout.Validate();Clear();Layout=AdventureData.Clone(layout);Ready=false;ruinsFloors.Clear();
  root=new GameObject("C1 远古遗迹 · 五区实例");UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(root,gameObject.scene);
  foreach(var e in FindObjectsByType<CombatEnemy>(FindObjectsSortMode.None).Where(x=>x.gameObject.scene==gameObject.scene)){hidden.Add(e.gameObject);e.gameObject.SetActive(false);}
  foreach(var n in FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(x=>x.gameObject.scene==gameObject.scene)){hidden.Add(n.gameObject);n.gameObject.SetActive(false);}
  ruinsStone=RuinsMaterial(new Color(.34f,.38f,.40f));ruinsGold=RuinsMaterial(new Color(.72f,.56f,.29f));ruinsDark=RuinsMaterial(new Color(.18f,.23f,.26f));
  RuinsFloor("入口风化石台",-9,9,164,190,0,0);RuinsFloor("石柱广场马赛克",-17,17,190,214,0,0);
  RuinsFloor("机关走廊",-5,5,214,236,0,0);RuinsFloor("下行石阶缓坡",-4,4,236,244,0,-3);
  RuinsFloor("地下祭坛地坪",-24,6,244,264,-3,-3);RuinsFloor("隐秘藏室",-34,-24,248,260,-3,-3);
  RuinsFloor("上行断桥修存段",-4,4,264,274,-3,0);RuinsFloor("守护者大厅",-18,32,274,304,0,0);
  // Real perimeter and room walls. Door gaps, ramps and alcoves stay open.
  Wall("入口西墙",-9,177,.8f,26,0);Wall("入口东墙",9,177,.8f,26,0);CrossWall("入口残垣",0,164,18,0);
  Wall("广场西墙",-17,202,.8f,24,0);Wall("广场东墙",17,202,.8f,24,0);
  CrossWall("广场南左",-13,190,8,0);CrossWall("广场南右",13,190,8,0);CrossWall("门廊左",-11,214,12,0);CrossWall("门廊右",11,214,12,0);
  Wall("走廊西侧",-5.5f,229,1,30,0);Wall("走廊东侧",5.5f,229,1,30,0);
  Wall("祭坛东壁",6,254,1,20,-3);Wall("祭坛西壁南",-24,246,1,4,-3);Wall("祭坛西壁北",-24,260,1,8,-3);
  CrossWall("祭坛南壁",-15,244,18,-3);CrossWall("祭坛北壁",-15,264,18,-3);
  Wall("密室外壁",-34,254,1,12,-3);CrossWall("密室南壁",-29,248,10,-3);CrossWall("密室北壁",-29,260,10,-3);
  Wall("桥西护栏",-4.5f,269,.6f,10,-3);Wall("桥东护栏",4.5f,269,.6f,10,-3);
  Wall("大厅西墙",-18,289,1,30,0);Wall("大厅东墙",32,289,1,30,0);CrossWall("大厅北墙",7,304,50,0);CrossWall("大厅南左",-11,274,14,0);CrossWall("大厅南右",18,274,28,0);
  for(int z=196;z<=210;z+=14)for(int side=-1;side<=1;side+=2)Column(new Vector3(side*12,0,z),4.7f);
  for(int z=280;z<=298;z+=18)for(int x=-12;x<=26;x+=38)Column(new Vector3(x,0,z),5.8f);
  Column(new Vector3(-20,-3,249),3.8f);Column(new Vector3(-20,-3,261),3.8f);
  RuinsShape("地下穹顶",PrimitiveType.Cube,new Vector3(-14,2.3f,254),new Vector3(21,.6f,20),ruinsDark);
  for(int i=0;i<8;i++)RuinsShape("下降踏面边缘",PrimitiveType.Cube,new Vector3(0,-i*.375f,236+i),new Vector3(7.6f,.06f,.14f),ruinsGold,false);
  RuinsShape("祭坛八角基座",PrimitiveType.Cylinder,new Vector3(-17,-2.7f,255),new Vector3(3,.3f,3),ruinsStone);
  RuinsShape("悬浮符文",PrimitiveType.Cube,new Vector3(-17,-1.1f,255),Vector3.one*.55f,ruinsGold,false).transform.rotation=Quaternion.Euler(30,45,25);
  // Reuse project-owned cat statue art, not a new external model or animation pack.
  foreach(var pos in new[]{new Vector3(-8,0,280),new Vector3(22,0,280)}){
   var prefab=Resources.Load<GameObject>("CatWorld/Actors/Warden");if(prefab!=null){var statue=Instantiate(prefab,root.transform);statue.name="石化猫族守护像";statue.transform.position=pos;statue.transform.localScale=Vector3.one*1.15f;foreach(var c in statue.GetComponentsInChildren<Collider>())c.enabled=false;foreach(var r in statue.GetComponentsInChildren<Renderer>())r.sharedMaterial=ruinsStone;var body=statue.AddComponent<BoxCollider>();body.center=Vector3.up*1.4f;body.size=new Vector3(2,2.8f,2);}
  }
  // Broken side bridge is visibly impassable, with solid guard/abutment rather than an invisible floor.
  RuinsShape("断桥残段",PrimitiveType.Cube,new Vector3(-13,.2f,182),new Vector3(5,.4f,5),ruinsStone);
  RuinsShape("断桥折断桥面",PrimitiveType.Cube,new Vector3(-15,.4f,185),new Vector3(3,.5f,2),ruinsStone).transform.rotation=Quaternion.Euler(0,20,12);
  foreach(var p in Layout.points){var mark=RuinsShape(p.label+" · 纹章",PrimitiveType.Cylinder,p.position+Vector3.up*.035f,new Vector3(3,.025f,3),ruinsGold,false);}
  var saved=S.Flow.ActiveRun?.checkpoint?.events;var events=RuinsLayout.Events();
  foreach(var e in events)e.used=RuinsLayout.Used(saved,e.entityId);S.Events.RestoreEvents(events);foreach(var point in S.Events.Points)if(point.entityId=="c1:door")point.interactionRange=4;
  foreach(var exit in Layout.exits){var g=new GameObject(exit.label);g.transform.SetParent(root.transform);g.AddComponent<ExtractionPoint>().Configure(exit,true);var ring=RuinsShape(exit.label+"石环",PrimitiveType.Cylinder,exit.position,new Vector3(2,.08f,2),ruinsGold,false);ring.transform.SetParent(g.transform,true);}
  var exploration=GetComponent<RuinsExploration>()??gameObject.AddComponent<RuinsExploration>();exploration.Configure(this,
   RuinsShape("符文石门",PrimitiveType.Cube,new Vector3(0,1.8f,220),new Vector3(10,3.6f,.9f),ruinsDark),
   RuinsShape("藏室封石",PrimitiveType.Cube,new Vector3(-24,-1.2f,254),new Vector3(.9f,3.6f,8),ruinsStone));
  Physics.SyncTransforms();RebuildRuinsNavigation();
  S.enemies=Layout.encounters.Select(e=>{var actor=S.Waves.CreateEncounter(root.transform,e.id,e.home,(EnemyArchetype)e.type);actor.gameObject.AddComponent<EncounterGuard>().Configure(this,e);if(e.id=="c1:guardian")actor.gameObject.AddComponent<RuinsBossBrain>().Configure();else actor.name=e.type==2?"遗迹精英 · 石甲卫":"遗迹守卫";return actor;}).ToArray();
  Physics.SyncTransforms();if(!PathComplete(Layout.entry,Layout.points[1].position)||!TryInteractionApproach(Layout.exits[0],out _))throw new InvalidOperationException("遗迹安全入口或免费出口不可达");Ready=true;InvalidateRoutes();
 }
 Material RuinsMaterial(Color c){var m=new Material(Shader.Find("Universal Render Pipeline/Lit")){color=c};m.SetFloat("_Smoothness",.16f);materials.Add(m);return m;}
 GameObject RuinsShape(string name,PrimitiveType shape,Vector3 p,Vector3 scale,Material mat,bool collide=true){var g=GameObject.CreatePrimitive(shape);g.name=name;g.transform.SetParent(root.transform);g.transform.position=p;g.transform.localScale=scale;g.GetComponent<Renderer>().sharedMaterial=mat;g.GetComponent<Collider>().enabled=collide;return g;}
 void Wall(string name,float x,float z,float width,float length,float floor){RuinsShape(name,PrimitiveType.Cube,new Vector3(x,floor+1.8f,z),new Vector3(width,3.6f,length),ruinsStone);}
 void CrossWall(string name,float x,float z,float width,float floor){RuinsShape(name,PrimitiveType.Cube,new Vector3(x,floor+1.8f,z),new Vector3(width,3.6f,.8f),ruinsStone);}
 void Column(Vector3 p,float h){RuinsShape("八角柱座",PrimitiveType.Cylinder,p+Vector3.up*.2f,new Vector3(2,.2f,2),ruinsDark);RuinsShape("古代石柱",PrimitiveType.Cylinder,p+Vector3.up*(h/2),new Vector3(1.2f,h/2,1.2f),ruinsStone);RuinsShape("柱顶环饰",PrimitiveType.Cylinder,p+Vector3.up*(h-.2f),new Vector3(1.8f,.2f,1.8f),ruinsGold);}
 void RuinsFloor(string name,float x0,float x1,float z0,float z1,float y0,float y1){
  var mesh=new Mesh{name=name};mesh.vertices=new[]{new Vector3(x0,y0,z0),new Vector3(x0,y1,z1),new Vector3(x1,y1,z1),new Vector3(x1,y0,z0)};mesh.triangles=new[]{0,1,2,0,2,3};mesh.uv=new[]{Vector2.zero,Vector2.up,Vector2.one,Vector2.right};mesh.RecalculateNormals();terrainMeshes.Add(mesh);
  var g=new GameObject(name,typeof(MeshFilter),typeof(MeshRenderer),typeof(MeshCollider));g.transform.SetParent(root.transform,false);g.GetComponent<MeshFilter>().sharedMesh=mesh;g.GetComponent<MeshCollider>().sharedMesh=mesh;g.GetComponent<MeshRenderer>().sharedMaterial=ruinsStone;
  ruinsFloors.Add(new NavMeshBuildSource{shape=NavMeshBuildSourceShape.Mesh,sourceObject=mesh,transform=Matrix4x4.identity,area=0});
 }
}
