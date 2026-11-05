using System;using System.IO;using System.Linq;using System.Collections;using System.Collections.Generic;
using UnityEngine;using UnityEngine.SceneManagement;using UnityEngine.AI;using UnityEngine.Profiling;using UnityEngine.Rendering;using Unity.Profiling;using Unity.Profiling.LowLevel.Unsafe;using Unity.Collections;using Unity.Jobs;
public class MT03Runtime:MonoBehaviour
{
 public Shader calibrationShader;
 public static string Output=>Environment.GetEnvironmentVariable("MT03_OUTPUT")??throw new Exception("Explicit independent output required");
 [Serializable]public class Row{public string name,status,detail;}
 [Serializable]class Result{public string mode,unity,gpu;public bool development;public Row[] rows;}
 [Serializable]class Kind{public string type;public int count;public long nativeBytes;public string[] objects;}
 [Serializable]class Snapshot{public string phase;public int cycle;public long engineAllocated,reserved,monoUsed,monoHeap,workingSet,privateBytes;public Kind[] types;}
 static List<Row> rows=new List<Row>();static int errors;bool ending;static byte[] sink;List<Material> clonedMaterials=new List<Material>();
 static void Check(string n,bool good,string d){rows.Add(new Row{name=n,status=good?"PASS":"FAIL",detail=d});}
 static void Note(string n,string status,string d){rows.Add(new Row{name=n,status=status,detail=d});}
 static void Exit(int code){
  #if UNITY_EDITOR
  UnityEditor.EditorApplication.Exit(code);
  #else
  Application.Quit(code);
  #endif
 }
 void Update(){if(!ending&&errors>0){ending=true;Finish("aborted");}}
 static string Arg(string key,string fallback){var a=Environment.GetCommandLineArgs();for(int i=0;i<a.Length-1;i++)if(a[i]==key)return a[i+1];return fallback;}
 void Finish(string mode){Check("unhandled-errors",errors==0,"count="+errors);File.WriteAllText(Output+"/results.json",JsonUtility.ToJson(new Result{mode=mode,unity=Application.unityVersion,gpu=SystemInfo.graphicsDeviceName,development=Debug.isDebugBuild,rows=rows.ToArray()},true));Exit(rows.Any(r=>r.status=="FAIL")?1:0);}
 static void SnapshotMemory(string phase,int cycle)
 {
  var types=new[]{typeof(TerrainData),typeof(Collider),typeof(NavMeshData),typeof(GameObject),typeof(Material),typeof(Texture),typeof(Mesh)};var list=new List<Kind>();
  foreach(var type in types){var objects=Resources.FindObjectsOfTypeAll(type);list.Add(new Kind{type=type.Name,count=objects.Length,nativeBytes=objects.Sum(o=>Profiler.GetRuntimeMemorySizeLong(o)),objects=type==typeof(GameObject)||type==typeof(Collider)?Array.Empty<string>():objects.Select(o=>o.GetInstanceID()+"|"+o.name+"|"+o.hideFlags).OrderBy(x=>x,StringComparer.Ordinal).ToArray()});}
  using(var process=System.Diagnostics.Process.GetCurrentProcess()){File.AppendAllText(Output+"/memory.jsonl",JsonUtility.ToJson(new Snapshot{phase=phase,cycle=cycle,engineAllocated=Profiler.GetTotalAllocatedMemoryLong(),reserved=Profiler.GetTotalReservedMemoryLong(),monoUsed=Profiler.GetMonoUsedSizeLong(),monoHeap=Profiler.GetMonoHeapSizeLong(),workingSet=process.WorkingSet64,privateBytes=process.PrivateMemorySize64,types=list.ToArray()})+"\n");}
 }
 IEnumerator Start()
 {
  Directory.CreateDirectory(Output);DontDestroyOnLoad(gameObject);Application.logMessageReceivedThreaded+=(m,s,t)=>{if(t==LogType.Error||t==LogType.Exception||t==LogType.Assert)System.Threading.Interlocked.Increment(ref errors);};string mode=Arg("-mt03-mode","audit");
  yield return CalibrateGC();
  if(mode=="audit"){
   yield return SceneManager.LoadSceneAsync("MT03World",LoadSceneMode.Additive);var world=UnityEngine.Object.FindAnyObjectByType<MT02WorldState>();Check("saved-world-load",world!=null,"Same MT02 world-v2 geometry");
   if(world==null){ending=true;Finish(mode);yield break;}
   yield return SeamAudit(world);yield return GpuCalibration();world=null;yield return SceneManager.UnloadSceneAsync("MT03World");yield return Resources.UnloadUnusedAssets();
  }
  // Two complete warmups, then six identical measured cycles; each process repeats independently.
  for(int i=-2;i<6;i++){yield return Cycle(i);yield return null;yield return Resources.UnloadUnusedAssets();GC.Collect();for(int frame=0;frame<30;frame++)yield return null;SnapshotMemory(i<0?"warm-unloaded":"measured-unloaded",i);}
  // Positive retention control verifies that object inventory detects a known strong reference.
  int before=Resources.FindObjectsOfTypeAll<TerrainData>().Length;var held=new TerrainData{heightmapResolution=257,name="MT03 deliberate retention control"};SnapshotMemory("retention-control-held",6);Check("retention-positive-control",Resources.FindObjectsOfTypeAll<TerrainData>().Length==before+1,"Known owned TerrainData reference detected");Destroy(held);held=null;yield return null;yield return Resources.UnloadUnusedAssets();GC.Collect();SnapshotMemory("retention-control-released",6);Check("retention-control-release",Resources.FindObjectsOfTypeAll<TerrainData>().Length==before,"Controlled reference released, not a plugin leak");
  ending=true;Finish(mode);
 }
 IEnumerator Cycle(int index)
 {
  SnapshotMemory("before-load",index);double start=Time.realtimeSinceStartupAsDouble;yield return SceneManager.LoadSceneAsync("MT03World",LoadSceneMode.Additive);var world=UnityEngine.Object.FindAnyObjectByType<MT02WorldState>();if(world==null){Check("cycle-load-"+index,false,"No world");yield break;}var lease=NavMesh.AddNavMeshData(world.navigation);SnapshotMemory("loaded",index);
  var mm=MT02WorldState.Generator(world.seed,257,world.terrains[0].materialTemplate,new Vector3(300,0,0));double deadline=Time.realtimeSinceStartupAsDouble+90;while(!MT02WorldState.Ready(mm)&&Time.realtimeSinceStartupAsDouble<deadline)yield return null;
  bool ready=MT02WorldState.Ready(mm);Check("cycle-generated-"+index,ready,"257,4 tiles");if(ready){var generated=MT02WorldState.Ordered(mm);MT02WorldState.Shape(generated);Check("cycle-content-"+index,MT02WorldState.Hash(generated)==world.expectedHash,"Real MM2 generation + same authored shape");}
  SnapshotMemory("generated",index);MT02WorldState.Release(mm,false);mm=null;lease.Remove();world=null;yield return null;yield return SceneManager.UnloadSceneAsync("MT03World");yield return Resources.UnloadUnusedAssets();GC.Collect();
  Check("cycle-unload-"+index,!SceneManager.GetSceneByName("MT03World").isLoaded&&UnityEngine.Object.FindObjectsByType<Terrain>().Length==0,"No active terrain; actual unload");
  // Owned TempJob control always completes/disposes before the cycle ends.
  var array=new NativeArray<int>(1024,Allocator.TempJob);var job=new ClearJob{values=array}.Schedule();job.Complete();array.Dispose();Check("owned-job-complete-dispose-"+index,!array.IsCreated,"No intentional leak");
  File.AppendAllText(Output+"/cycle-times.csv",index+","+(Time.realtimeSinceStartupAsDouble-start)+"\n");
 }
 struct ClearJob:IJob{public NativeArray<int> values;public void Execute(){for(int i=0;i<values.Length;i++)values[i]=i;}}
 IEnumerator CalibrateGC()
 {
  var handles=new List<ProfilerRecorderHandle>();ProfilerRecorderHandle.GetAvailable(handles);File.WriteAllLines(Output+"/available-counters.txt",handles.Select(h=>ProfilerRecorderHandle.GetDescription(h)).Where(d=>d.Name.Contains("GC")||d.Name.Contains("Alloc")||d.Name.Contains("GPU")).Select(d=>d.Name+"|"+d.UnitType));
  long[] positive=new long[3],zero=new long[3];GC.GetAllocatedBytesForCurrentThread();for(int i=0;i<3;i++){long begin=GC.GetAllocatedBytesForCurrentThread();sink=new byte[65536];positive[i]=GC.GetAllocatedBytesForCurrentThread()-begin;begin=GC.GetAllocatedBytesForCurrentThread();zero[i]=GC.GetAllocatedBytesForCurrentThread()-begin;}
  var recorder=ProfilerRecorder.StartNew(ProfilerCategory.Memory,"GC.Alloc",256);recorder.Reset();sink=new byte[65536];yield return null;var samples=new List<ProfilerRecorderSample>();if(recorder.Valid)recorder.CopyTo(samples);bool eventPositive=recorder.Valid&&samples.Sum(s=>s.Value)>=65536;File.WriteAllText(Output+"/gc-calibration.json","{\"positive\":["+string.Join(",",positive)+"],\"zero\":["+string.Join(",",zero)+"],\"eventValid\":"+recorder.Valid.ToString().ToLowerInvariant()+",\"eventPositiveBytes\":"+samples.Sum(s=>s.Value)+"}");recorder.Dispose();
  bool valid=positive.All(x=>x>=65536)&&zero.All(x=>x==0);Note("thread-gc-calibration",valid?"PASS":"NOT_RUN","Positive/zero current-thread control; never infer worker allocations");Note("gc-event-calibration","NOT_RUN",eventPositive?"Positive event observed, but isolated zero-event control not established":"GC.Alloc unavailable or positive control not observed");
 }
 IEnumerator SeamAudit(MT02WorldState world)
 {
  string hash=MT02WorldState.Hash(world.terrains);var camera=Camera.main;var views=new[]{new Vector3(140,100,-32),new Vector3(75,15,53),new Vector3(64,8,42)};var targets=new[]{new Vector3(64,3,64),new Vector3(64,3,64),new Vector3(64,3,76)};var stages=new[]{"baseline","rebind-sync","lod-control","pixel-normal-control","no-shadow-control"};
  var originalError=world.terrains.Select(t=>t.heightmapPixelError).ToArray();var originalInstancing=world.terrains.Select(t=>t.drawInstanced).ToArray();var originalMaterials=world.terrains.Select(t=>t.materialTemplate).ToArray();var light=UnityEngine.Object.FindAnyObjectByType<Light>();var shadows=light.shadows;
  for(int s=0;s<stages.Length;s++){
   if(s==1){MT02WorldState.Link(world.terrains);foreach(var t in world.terrains){t.terrainData.SyncHeightmap();t.Flush();}}
   if(s==2)foreach(var t in world.terrains){t.heightmapPixelError=1;t.drawInstanced=false;}
   if(s==3)foreach(var t in world.terrains){t.drawInstanced=true;var material=new Material(t.materialTemplate);material.SetFloat("_EnableInstancedPerPixelNormal",1);material.EnableKeyword("_TERRAIN_INSTANCED_PERPIXEL_NORMAL");t.materialTemplate=material;clonedMaterials.Add(material);}
   if(s==4)light.shadows=LightShadows.None;
   for(int view=0;view<views.Length;view++){camera.transform.position=views[view];camera.transform.LookAt(targets[view]);for(int f=0;f<20;f++)yield return null;yield return Picture(stages[s]+"-v"+view);}
   float normalAngle=0;for(int i=0;i<=64;i++){float z=i/64f;for(int row=0;row<2;row++)normalAngle=Mathf.Max(normalAngle,Vector3.Angle(world.terrains[row*2].terrainData.GetInterpolatedNormal(1,z),world.terrains[row*2+1].terrainData.GetInterpolatedNormal(0,z)));}
   File.AppendAllText(Output+"/seam-state.jsonl","{\"stage\":\""+stages[s]+"\",\"heightHash\":\""+MT02WorldState.Hash(world.terrains)+"\",\"maxHeightSeam\":"+MT02WorldState.Seam(world.terrains)+",\"maxDataNormalAngle\":"+normalAngle+",\"pixelError\":"+world.terrains[0].heightmapPixelError+",\"instancing\":"+world.terrains[0].drawInstanced.ToString().ToLowerInvariant()+",\"material\":\""+world.terrains[0].materialTemplate.shader.name+"\",\"tileScale\":8}");File.AppendAllText(Output+"/seam-state.jsonl","\n");Check("same-height-"+stages[s],MT02WorldState.Hash(world.terrains)==hash,"No geometry edits, post effects or concealment");
  }
  // Controls are diagnostic only; restore original scene before memory cycles.
  for(int i=0;i<4;i++){world.terrains[i].heightmapPixelError=originalError[i];world.terrains[i].drawInstanced=originalInstancing[i];world.terrains[i].materialTemplate=originalMaterials[i];}light.shadows=shadows;foreach(var material in clonedMaterials)Destroy(material);clonedMaterials.Clear();
 }
 IEnumerator Picture(string name){yield return new WaitForEndOfFrame();string p=Output+"/"+name+".png";ScreenCapture.CaptureScreenshot(p);double end=Time.realtimeSinceStartupAsDouble+5;while(!File.Exists(p)&&Time.realtimeSinceStartupAsDouble<end)yield return new WaitForSecondsRealtime(.05f);Check("image-"+name,File.Exists(p),"Actual Player frame; fixed scene/camera/light except explicitly named diagnostic control");}
 IEnumerator GpuCalibration()
 {
  var material=new Material(calibrationShader);RenderTexture a=new RenderTexture(512,512,0),b=new RenderTexture(512,512,0);a.Create();b.Create();var timings=new FrameTiming[1];var means=new List<double>();
  for(int phase=0;phase<3;phase++){var values=new List<double>();for(int i=0;i<100;i++){if(phase==1){material.SetFloat("_Seed",i*.01f);for(int pass=0;pass<4;pass++){Graphics.Blit(a,b,material);var swap=a;a=b;b=swap;}}FrameTimingManager.CaptureFrameTimings();yield return null;uint n=FrameTimingManager.GetLatestTimings(1,timings);double gpu=n>0?timings[0].gpuFrameTime:0;File.AppendAllText(Output+"/gpu-calibration.csv",phase+","+i+","+n+","+gpu+"\n");if(i>=20&&n>0&&gpu>0)values.Add(gpu);}means.Add(values.Count>=30?values.Average():double.NaN);}
  bool valid=FrameTimingManager.IsFeatureEnabled()&&FrameTimingManager.GetGpuTimerFrequency()>0&&means.All(x=>!double.IsNaN(x))&&means[1]>means[0]*1.2&&means[2]<means[1]*.85;File.WriteAllText(Output+"/gpu-status.txt","enabled="+FrameTimingManager.IsFeatureEnabled()+" frequency="+FrameTimingManager.GetGpuTimerFrequency()+" meansMs="+string.Join(",",means)+" calibrated="+valid);Note("gpu-controlled-load-calibration",valid?"PASS":"NOT_RUN","Baseline/owned bounded GPU workload/recovery; no performance budget verdict");a.Release();b.Release();Destroy(a);Destroy(b);Destroy(material);
 }
}
