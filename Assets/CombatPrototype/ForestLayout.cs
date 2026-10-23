using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
[Serializable] public class ForestPoi { public string id,label;public Vector3 position;public int risk; }
[Serializable] public class ForestNode { public string id;public Vector3 position;public int kind; }
[Serializable] public class ForestEncounter {public string id,poi;public Vector3 home;public int type;}
[Serializable] public class ForestRoute {public string from,to;}
[Serializable] public class ExtractionConfig {public string id,label;public Vector3 position;public float range=3,duration=5;}
[Serializable] public class ForestLayout {
 public Vector3 boundsCenter=new Vector3(0,3,242),boundsSize=new Vector3(190,16,186); public Bounds WorldBounds=>new Bounds(boundsCenter,boundsSize);
 public int requestedSeed;public bool fallback;public int generationAttempt;public int seed,revision=1;public Vector3 entry;public ForestPoi[] points;public ForestNode[] nodes;public ForestEncounter[] encounters;public ForestRoute[] routes;public ExtractionConfig[] exits;public Vector3[] rocks;
 public static ForestLayout Generate(int seed){
  var rng=new System.Random(seed);var layout=new ForestLayout{seed=seed,entry=new Vector3(0,.1f,172)};
  Vector3[] centers={new Vector3(0,0,172),new Vector3(-45,0,205),new Vector3(45,0,205),new Vector3(-42,0,260),new Vector3(38,0,260),new Vector3(-35,0,307),new Vector3(43,0,307)};
  string[] labels={"林间入口","伐木林地","碎岩矿脉","遗迹营地","精英哨站","归途祭坛","湖岸物资点"};
  layout.points=centers.Select((c,i)=>new ForestPoi{id="poi:"+i,label=labels[i],risk=i==4?3:i==3?2:1,position=c+(i==0?Vector3.zero:new Vector3(rng.Next(-6,7),0,rng.Next(-6,7)))}).ToArray();
  int[][] links={new[]{0,1},new[]{0,2},new[]{1,3},new[]{2,4},new[]{3,4},new[]{3,5},new[]{4,6},new[]{5,6}};
  layout.routes=links.Select(a=>new ForestRoute{from="poi:"+a[0],to="poi:"+a[1]}).ToArray();
  var nodes=new List<ForestNode>();for(int i=0;i<42;i++){int poi=i<18?1:i<34?2:6;var c=layout.points[poi].position;double angle=rng.NextDouble()*Math.PI*2;float radius=4+(float)rng.NextDouble()*8;nodes.Add(new ForestNode{id="node:"+i,kind=i<18?0:i<30?1:2,position=c+new Vector3((float)Math.Cos(angle)*radius,0,(float)Math.Sin(angle)*radius)});}layout.nodes=nodes.ToArray();
  int[] sites={1,2,3,3,3,4,4,4,6,6,5};layout.encounters=sites.Select((n,i)=>new ForestEncounter{id="enemy:"+i,poi="poi:"+n,home=layout.points[n].position+new Vector3((i%3-1)*3,.1f,4+(i%2)*3),type=n==4?2:i%3==0?1:0}).ToArray();
  layout.exits=new[]{new ExtractionConfig{id="exit:entry",label="入口撤离装置",position=layout.entry+Vector3.back*3},new ExtractionConfig{id="exit:altar",label="归途祭坛",position=layout.points[5].position+Vector3.left*5}};
  var rocks=new List<Vector3>();for(int i=0;i<100;i++){var pos=new Vector3(rng.Next(-85,86),0,rng.Next(160,326));if(layout.points.Any(p=>Vector3.Distance(p.position,pos)<17)||layout.routes.Any(e=>DistanceToSegment(pos,layout.points.First(p=>p.id==e.from).position,layout.points.First(p=>p.id==e.to).position)<6))continue;rocks.Add(pos);}layout.rocks=rocks.ToArray();return layout;
 }
 public static float DistanceToSegment(Vector3 p,Vector3 a,Vector3 b){var d=b-a;return Vector3.Distance(p,a+d*Mathf.Clamp01(Vector3.Dot(p-a,d)/d.sqrMagnitude));}
 public void Validate(){if(revision!=1||points==null||nodes==null||encounters==null||routes==null||exits==null||rocks==null||points.Length<2||exits.Length<1)throw new System.IO.InvalidDataException("森林布局不完整");
  var ids=new HashSet<string>();foreach(var p in points){Check(p.position);if(string.IsNullOrEmpty(p.id)||!ids.Add(p.id))throw new System.IO.InvalidDataException("兴趣点重复");}foreach(var r in routes)if(!ids.Contains(r.from)||!ids.Contains(r.to)||r.from==r.to)throw new System.IO.InvalidDataException("路线无端点");
  foreach(var n in nodes){Check(n.position);if(n.kind<0||n.kind>2||!ids.Add(n.id))throw new System.IO.InvalidDataException("资源标识损坏");}foreach(var e in encounters){Check(e.home);if(e.type<0||e.type>2||!ids.Add(e.id)||!points.Any(p=>p.id==e.poi))throw new System.IO.InvalidDataException("遭遇标识损坏");}foreach(var e in exits){Check(e.position);if(!ids.Add(e.id)||e.range<1||e.range>20||e.duration<.1f||e.duration>3600)throw new System.IO.InvalidDataException("撤离配置损坏");}foreach(var r in rocks)Check(r);Check(entry);
  var reachable=new HashSet<string>{points[0].id};for(int i=0;i<points.Length;i++)foreach(var r in routes){if(reachable.Contains(r.from))reachable.Add(r.to);if(reachable.Contains(r.to))reachable.Add(r.from);}if(reachable.Count!=points.Length)throw new System.IO.InvalidDataException("森林路线不连通");
 }
 void Check(Vector3 p){if(float.IsNaN(p.x)||float.IsInfinity(p.x)||float.IsNaN(p.y)||float.IsInfinity(p.y)||float.IsNaN(p.z)||float.IsInfinity(p.z)||!WorldBounds.Contains(p))throw new System.IO.InvalidDataException("森林实体越界");}
}
