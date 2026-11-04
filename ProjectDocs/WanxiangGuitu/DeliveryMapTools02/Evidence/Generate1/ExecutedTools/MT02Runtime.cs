using System;using System.IO;using System.Linq;using System.Collections;using System.Collections.Generic;using UnityEngine;using UnityEngine.AI;using UnityEngine.SceneManagement;using UnityEngine.Profiling;using Unity.Profiling;
public class MT02Runtime:MonoBehaviour
{
 public static string Output=>Environment.GetEnvironmentVariable("MT02_OUTPUT")??throw new Exception("Explicit isolated output required");
 [Serializable]public class Row{public string name,status,detail;}
 [Serializable]public class Result{public string layer,unity,gpu,mode;public bool development;public Row[] rows;}
 [Serializable]public class Checkpoint{public string runId,identity,heightHash,placementHash;public int seed,resolution;public Vector3 navigationPosition;}
 [Serializable]public class MemorySample{public string phase;public long allocated,reserved,mono;public int terrains,agents;}
 static List<Row> rows=new List<Row>();static int errors;static byte[] sink;
 public static void Check(string name,bool pass,string detail){rows.Add(new Row{name=name,status=pass?"PASS":"FAIL",detail=detail});}
 public static void Note(string name,string status,string detail){rows.Add(new Row{name=name,status=status,detail=detail});}
 public static void CaptureErrors(){Application.logMessageReceivedThreaded+=(m,s,t)=>{if(t==LogType.Error||t==LogType.Exception||t==LogType.Assert)System.Threading.Interlocked.Increment(ref errors);};}
 public static void Save(string name,string layer,string mode=""){Check("unhandled-errors",errors==0,"count="+errors);File.WriteAllText(Output+"/"+name,JsonUtility.ToJson(new Result{layer=layer,unity=Application.unityVersion,gpu=SystemInfo.graphicsDeviceName,development=Debug.isDebugBuild,mode=mode,rows=rows.ToArray()},true));}
 public static bool Failed=>rows.Any(r=>r.status=="FAIL");
 public static void Memory(string phase){File.AppendAllText(Output+"/memory.jsonl",JsonUtility.ToJson(new MemorySample{phase=phase,allocated=Profiler.GetTotalAllocatedMemoryLong(),reserved=Profiler.GetTotalReservedMemoryLong(),mono=Profiler.GetMonoUsedSizeLong(),terrains=UnityEngine.Object.FindObjectsByType<Terrain>(FindObjectsSortMode.None).Length,agents=UnityEngine.Object.FindObjectsByType<NavMeshAgent>(FindObjectsSortMode.None).Length})+"\n");}
 static string Arg(string key,string fallback){var args=Environment.GetCommandLineArgs();for(int i=0;i<args.Length-1;i++)if(args[i]==key)return args[i+1];return fallback;}
 IEnumerator Start()
 {
  DontDestroyOnLoad(gameObject);Directory.CreateDirectory(Output);CaptureErrors();string mode=Arg("-mt02-mode",Environment.GetEnvironmentVariable("MT02_MODE")??"write");string checkpoint=Arg("-mt02-checkpoint","I:/WGCombat/MAPTOOLS02-A/Synthetic/checkpoint.json");
  Checkpoint prior=null;if(mode=="read"){if(File.Exists(checkpoint))prior=JsonUtility.FromJson<Checkpoint>(File.ReadAllText(checkpoint));Check("checkpoint-present",prior!=null,"Synthetic lab metadata only, not game v9");}
  Memory("boot-before-load");double loadStart=Time.realtimeSinceStartupAsDouble;yield return SceneManager.LoadSceneAsync("MT02World",LoadSceneMode.Additive);var world=UnityEngine.Object.FindFirstObjectByType<MT02WorldState>();Check("direct-saved-scene-load",world!=null,"ms="+((Time.realtimeSinceStartupAsDouble-loadStart)*1000));if(world==null)yield break;
  var lease=NavMesh.AddNavMeshData(world.navigation);Memory("world-loaded");string height=MT02WorldState.Hash(world.terrains);Check("four-saved-tiles",world.terrains.Length==4,height);Check("saved-content-hash",height==world.expectedHash,"expected="+world.expectedHash);
  Check("saved-seams",MT02WorldState.Seam(world.terrains)<=.01f,"max meters="+MT02WorldState.Seam(world.terrains));
  var props=GameObject.Find("Authored placements");string placements=MT02WorldState.Placements(props);Check("prefab-placement-identity",placements==world.placementHash,placements);
  if(prior!=null){Check("same-run-and-map-identity",prior.identity==world.identity&&prior.seed==world.seed&&prior.resolution==world.resolution,prior.runId);Check("cross-process-heights",prior.heightHash==height,height);Check("cross-process-placements",prior.placementHash==placements,placements);}
  Physics.SyncTransforms();int terrainHits=0;for(int z=1;z<=4;z++)for(int x=1;x<=4;x++){if(Physics.Raycast(new Vector3(x*28,50,z*25),Vector3.down,out var hit,100)&&hit.collider is TerrainCollider)terrainHits++;}Check("terrain-collider-probes",terrainHits>=14,"hits="+terrainHits+"; lake/module may be first collision");
  Check("lake-physical-block",Physics.Raycast(new Vector3(60,10,85),Vector3.down,out var lake,20)&&lake.collider.gameObject==world.waterBlocker,"First collision="+(lake.collider?lake.collider.name:"none"));
  Check("lake-nav-exclusion",!NavMesh.SamplePosition(new Vector3(60,1,85),out var wet,3,NavMesh.AllAreas),"Deep water not navigable");
  Check("roof-real-collider",Physics.Raycast(new Vector3(20,3,105),Vector3.up,out var roof,10)&&roof.collider.name.Contains("Roof"),roof.collider?roof.collider.name:"none");
  Check("wall-occlusion",Physics.Raycast(new Vector3(20,3,105),Vector3.left,out var wall,12)&&wall.collider.name.Contains("Wall"),wall.collider?wall.collider.name:"none");
  var agents=new List<NavMeshAgent>();yield return Travel("enemy-road-across-seam",prior!=null?prior.navigationPosition:world.enemyStartA,world.enemyGoalA,agents);yield return Travel("enemy-lake-bypass",world.enemyStartB,world.enemyGoalB,agents);
  if(mode=="write"&&agents.Count>0){Directory.CreateDirectory(Path.GetDirectoryName(checkpoint));var cp=new Checkpoint{runId=Guid.NewGuid().ToString("N"),identity=world.identity,heightHash=height,placementHash=placements,seed=world.seed,resolution=world.resolution,navigationPosition=agents[0].transform.position};File.WriteAllText(checkpoint,JsonUtility.ToJson(cp,true));File.Copy(checkpoint,Output+"/checkpoint-written.json");}
  if(prior!=null&&agents.Count>0)Check("saved-navigation-position-restored",Vector3.Distance(prior.navigationPosition,world.enemyGoalA)<2,"Restored actual previous destination, then normal nav request");
  var camera=Camera.main;var views=new[]{new Vector3(140,100,-32),new Vector3(88,30,48),new Vector3(20,3.4f,95)};var look=new[]{new Vector3(64,3,64),new Vector3(61,1.5f,84),new Vector3(20,3.4f,106)};var names=new[]{"four-tiles","lake-ridge-road","closed-ruin"};
  for(int i=0;i<views.Length;i++){camera.transform.position=views[i];camera.transform.LookAt(look[i]);yield return new WaitForEndOfFrame();ScreenCapture.CaptureScreenshot(Output+"/"+names[i]+".png");for(int j=0;j<5;j++)yield return null;Check("screen-"+names[i],File.Exists(Output+"/"+names[i]+".png"),"Automated actual frame, not native/human");}
  long heightVertices=world.terrains.Sum(t=>(long)t.terrainData.heightmapResolution*t.terrainData.heightmapResolution);int colliders=UnityEngine.Object.FindObjectsByType<Collider>(FindObjectsSortMode.None).Length;File.WriteAllText(Output+"/scene-counts.json","{\"terrainTiles\":4,\"heightGridVertices\":"+heightVertices+",\"colliders\":"+colliders+",\"agents\":"+agents.Count+",\"note\":\"Height grid vertices are not GPU LOD triangle counts\"}");
  foreach(var a in agents)a.SetDestination(world.enemyStartA);yield return SamplePerformance();Memory("before-runtime-generation");
  var mm=MT02WorldState.Generator(world.seed,world.resolution,world.terrains[0].materialTemplate,new Vector3(300,0,0));double generationStart=Time.realtimeSinceStartupAsDouble,deadline=generationStart+90;while(!MT02WorldState.Ready(mm)&&Time.realtimeSinceStartupAsDouble<deadline)yield return null;
  bool ready=MT02WorldState.Ready(mm);Check("runtime-four-tile-generation",ready,"elapsedMs="+((Time.realtimeSinceStartupAsDouble-generationStart)*1000));if(ready){var generated=MT02WorldState.Ordered(mm);MT02WorldState.Shape(generated);Check("runtime-regenerated-height-hash",MT02WorldState.Hash(generated)==world.expectedHash,MT02WorldState.Hash(generated));}MT02WorldState.Release(mm,false);yield return null;
  foreach(var a in agents)Destroy(a.gameObject);agents.Clear();lease.Remove();world=null;props=null;Memory("before-world-unload");yield return SceneManager.UnloadSceneAsync("MT02World");yield return Resources.UnloadUnusedAssets();GC.Collect();for(int i=0;i<10;i++)yield return null;Memory("after-world-unload");Check("scene-unloaded",!SceneManager.GetSceneByName("MT02World").isLoaded,"Actual SceneManager unload");Check("no-terrain-agent-residue",UnityEngine.Object.FindObjectsByType<Terrain>(FindObjectsSortMode.None).Length==0&&UnityEngine.Object.FindObjectsByType<NavMeshAgent>(FindObjectsSortMode.None).Length==0,"No active old terrain/agent");
  yield return SceneManager.LoadSceneAsync("MT02World",LoadSceneMode.Additive);world=UnityEngine.Object.FindFirstObjectByType<MT02WorldState>();Check("reload-same-content",world!=null&&MT02WorldState.Hash(world.terrains)==height,"Fresh instance same baked content");world=null;yield return SceneManager.UnloadSceneAsync("MT02World");yield return Resources.UnloadUnusedAssets();GC.Collect();Memory("after-second-unload");
  Save("runtime.json",Application.isEditor?"Editor controlled Play Mode":"nondevelopment isolated plugin Player",mode);yield return null;
  #if UNITY_EDITOR
  UnityEditor.EditorApplication.Exit(Failed?1:0);
  #else
  Application.Quit(Failed?1:0);
  #endif
 }
 IEnumerator Travel(string name,Vector3 from,Vector3 to,List<NavMeshAgent> agents)
 {
  bool a=NavMesh.SamplePosition(from,out var start,8,NavMesh.AllAreas),b=NavMesh.SamplePosition(to,out var end,8,NavMesh.AllAreas);var path=new NavMeshPath();bool good=a&&b&&NavMesh.CalculatePath(start.position,end.position,NavMesh.AllAreas,path)&&path.status==NavMeshPathStatus.PathComplete;Check(name+"-path",good,"corners="+path.corners.Length);if(!good)yield break;
  var go=new GameObject(name);var visual=GameObject.CreatePrimitive(PrimitiveType.Capsule);visual.transform.SetParent(go.transform,false);visual.transform.localScale=new Vector3(1.3f,1.25f,1.3f);visual.transform.localPosition=Vector3.up*1.25f;Destroy(visual.GetComponent<Collider>());var agent=go.AddComponent<NavMeshAgent>();agent.radius=.65f;agent.height=2.5f;agent.speed=10;bool warped=agent.Warp(start.position);Check(name+"-warp",warped&&Vector3.Distance(agent.transform.position,start.position)<.05f,"Actual NavMeshAgent.Warp before path");agent.SetDestination(end.position);agents.Add(agent);double deadline=Time.realtimeSinceStartupAsDouble+35;
  var trace=new List<string>();while((agent.pathPending||Vector3.Distance(agent.transform.position,end.position)>1)&&Time.realtimeSinceStartupAsDouble<deadline){var p=agent.transform.position;trace.Add(Time.realtimeSinceStartupAsDouble+","+p.x+","+p.y+","+p.z);yield return null;}File.WriteAllLines(Output+"/"+name+".csv",trace);Check(name+"-actual-movement",Vector3.Distance(agent.transform.position,end.position)<=1,"distance="+Vector3.Distance(agent.transform.position,end.position));
 }
 IEnumerator SamplePerformance()
 {
  var main=ProfilerRecorder.StartNew(ProfilerCategory.Internal,"Main Thread",180);var draw=ProfilerRecorder.StartNew(ProfilerCategory.Render,"Draw Calls Count",180);
  long[] positive=new long[3],zero=new long[3];GC.GetAllocatedBytesForCurrentThread();for(int i=0;i<3;i++){long begin=GC.GetAllocatedBytesForCurrentThread();sink=new byte[65536];positive[i]=GC.GetAllocatedBytesForCurrentThread()-begin;begin=GC.GetAllocatedBytesForCurrentThread();zero[i]=GC.GetAllocatedBytesForCurrentThread()-begin;}
  bool calibrated=positive.All(x=>x>=65536&&x<131072)&&zero.All(x=>x==0);File.WriteAllText(Output+"/gc-calibration.json","{\"positive\":["+string.Join(",",positive)+"],\"zero\":["+string.Join(",",zero)+"],\"valid\":"+calibrated.ToString().ToLowerInvariant()+"}");Note("gc-allocation",calibrated?"PASS":"NOT_RUN",calibrated?"Current-thread counter calibrated; worker allocations not covered":"Positive/zero calibration failed; no zero-allocation claim");
  var timings=new FrameTiming[1];var gpu=new List<string>();for(int i=0;i<180;i++){FrameTimingManager.CaptureFrameTimings();yield return null;uint count=FrameTimingManager.GetLatestTimings(1,timings);gpu.Add(i+","+count+","+(count>0?timings[0].gpuFrameTime:0));}
  WriteRecorder("main-thread",main);WriteRecorder("draw-calls",draw);main.Dispose();draw.Dispose();File.WriteAllLines(Output+"/gpu-raw.csv",gpu);Note("gpu-frame-time","NOT_RUN","Raw FrameTiming retained; no calibrated independent timing control");
 }
 static void WriteRecorder(string name,ProfilerRecorder recorder){var samples=new List<ProfilerRecorderSample>();if(recorder.Valid)recorder.CopyTo(samples);File.WriteAllLines(Output+"/"+name+".csv",new[]{"value,count"}.Concat(samples.Select(s=>s.Value+","+s.Count)));Note(name,samples.Count>0&&samples.Any(s=>s.Value>0)?"PASS":"NOT_RUN","Raw profiler samples="+samples.Count+"; no budget threshold");}
}
