using System;using System.IO;using System.Linq;using System.Collections.Generic;using System.Security.Cryptography;
using UnityEngine;using UnityEngine.AI;using MapMagic.Core;using MapMagic.Nodes;using MapMagic.Nodes.MatrixGenerators;using Den.Tools;
public class MT02WorldState:MonoBehaviour
{
 public int seed=424242,resolution=257;public Terrain[] terrains;public NavMeshData navigation;
 public string identity="MT02-world-v1",expectedHash,placementHash;public GameObject waterBlocker;
 public Vector3 enemyStartA=new Vector3(8,2,32),enemyGoalA=new Vector3(118,2,32),enemyStartB=new Vector3(20,2,100),enemyGoalB=new Vector3(106,4,110);
 public static MapMagicObject Generator(int seed,int resolution,Material material,Vector3 offset)
 {
  var go=new GameObject("Actual MM2 four-tile source");go.SetActive(false);go.transform.position=offset;var mm=go.AddComponent<MapMagicObject>();
  mm.graph=ScriptableObject.CreateInstance<Graph>();mm.graph.random=new Noise(seed,32768);var noise=(Noise200)MapMagic.Nodes.Generator.Create(typeof(Noise200));noise.seed=7;noise.size=50;noise.intensity=.25f;noise.detail=.35f;
  var height=(HeightOutput200)MapMagic.Nodes.Generator.Create(typeof(HeightOutput200));mm.graph.Add(noise);mm.graph.Add(height);mm.graph.Link(height,noise);
  mm.tileSize=new Vector2D(64,64);mm.tileResolution=(MapMagicObject.Resolution)resolution;mm.globals.height=32;mm.globals.heightMainApply=HeightOutput200.ApplyType.SetHeights;mm.terrainSettings.material=material;
  mm.draftsInEditor=false;mm.draftsInPlaymode=false;mm.tiles.allowMove=false;mm.tiles.generateLimited=false;mm.tiles.generateInfinite=false;mm.tiles.genAroundMainCam=false;
  go.SetActive(true);for(int z=0;z<2;z++)for(int x=0;x<2;x++)mm.tiles.Pin(new Coord(x,z),false,mm);return mm;
 }
 public static bool Ready(MapMagicObject mm)=>mm.tiles.All().Count()==4&&mm.tiles.All().All(t=>t.main!=null&&t.main.applyReady)&&!mm.IsGenerating();
 public static Terrain[] Ordered(MapMagicObject mm)=>Enumerable.Range(0,4).Select(i=>mm.tiles[new Coord(i%2,i/2)].main.terrain).ToArray();
 public static string Hash(Terrain[] tiles){using(var sha=SHA256.Create()){using(var ms=new MemoryStream()){foreach(var t in tiles){var a=t.terrainData.GetHeights(0,0,t.terrainData.heightmapResolution,t.terrainData.heightmapResolution);var b=new byte[a.Length*4];Buffer.BlockCopy(a,0,b,0,b.Length);ms.Write(b,0,b.Length);}return BitConverter.ToString(sha.ComputeHash(ms.ToArray())).Replace("-","").ToLowerInvariant();}}}
 public static float Seam(Terrain[] t){float max=0;int n=t[0].terrainData.heightmapResolution;for(int i=0;i<n;i++){for(int row=0;row<2;row++)max=Mathf.Max(max,Mathf.Abs(t[row*2].terrainData.GetHeight(n-1,i)-t[row*2+1].terrainData.GetHeight(0,i)));for(int col=0;col<2;col++)max=Mathf.Max(max,Mathf.Abs(t[col].terrainData.GetHeight(i,n-1)-t[col+2].terrainData.GetHeight(i,0)));}return max;}
 public static void Link(Terrain[] t){t[0].SetNeighbors(null,t[2],t[1],null);t[1].SetNeighbors(t[0],t[3],null,null);t[2].SetNeighbors(null,null,t[3],t[0]);t[3].SetNeighbors(t[2],null,null,t[1]);}
 // Authored post-process, NOT a paid Objects/Splines/Biomes node.
 public static void Shape(Terrain[] tiles)
 {
  for(int index=0;index<tiles.Length;index++){
   var td=tiles[index].terrainData;int n=td.heightmapResolution;var a=td.GetHeights(0,0,n,n);
   for(int z=0;z<n;z++)for(int x=0;x<n;x++){
    float wx=(index%2)*64+x*64f/(n-1),wz=(index/2)*64+z*64f/(n-1);float h=a[z,x]*32;
    h+=9*Mathf.Exp(-Mathf.Pow((wx-100)/9,2)-Mathf.Pow((wz-75)/36,2));
    float lake=Vector2.Distance(new Vector2(wx,wz),new Vector2(60,85));h=Mathf.Lerp(h,.4f,1-Mathf.SmoothStep(0,1,Mathf.InverseLerp(11,17,lake)));
    h=Mathf.Lerp(h,2,Mathf.Exp(-Mathf.Pow((wz-32)/5,4)));
    float pad=Mathf.Max(Mathf.Abs(wx-26)/28,Mathf.Abs(wz-105)/14);h=Mathf.Lerp(h,2,1-Mathf.SmoothStep(0,1,Mathf.InverseLerp(.82f,1,pad)));
    a[z,x]=Mathf.Clamp01(h/32);
   }td.SetHeights(0,0,a);tiles[index].Flush();
  }Link(tiles);
 }
 public static void Release(MapMagicObject mm,bool immediate)
 {
  if(mm==null)return;var data=mm.tiles.All().Where(t=>t.main?.terrain!=null).Select(t=>t.main.terrain.terrainData).ToArray();foreach(var t in mm.tiles.All())t.Stop();var graph=mm.graph;
  if(immediate){UnityEngine.Object.DestroyImmediate(mm.gameObject);foreach(var d in data)UnityEngine.Object.DestroyImmediate(d);UnityEngine.Object.DestroyImmediate(graph);}
  else{UnityEngine.Object.Destroy(mm.gameObject);foreach(var d in data)UnityEngine.Object.Destroy(d);UnityEngine.Object.Destroy(graph);}
 }
 public static string Placements(GameObject root){var text=string.Join("\n",root.GetComponentsInChildren<Transform>().OrderBy(t=>PathOf(t,root.transform),StringComparer.Ordinal).Select(t=>PathOf(t,root.transform)+"|"+t.position.x.ToString("R",System.Globalization.CultureInfo.InvariantCulture)+","+t.position.y.ToString("R",System.Globalization.CultureInfo.InvariantCulture)+","+t.position.z.ToString("R",System.Globalization.CultureInfo.InvariantCulture)+"|"+t.rotation.ToString("F5")+"|"+t.localScale.ToString("F5")));using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(System.Text.Encoding.UTF8.GetBytes(text))).Replace("-","").ToLowerInvariant();}
 static string PathOf(Transform t,Transform root){if(t==root)return t.name;return PathOf(t.parent,root)+"/"+t.name+"#"+t.GetSiblingIndex();}
}
