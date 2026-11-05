using System;using System.IO;using System.Linq;using System.Text.RegularExpressions;using UnityEditor;using UnityEditor.SceneManagement;using UnityEditor.Build.Profile;using UnityEngine;using UnityEngine.SceneManagement;using Unity.Collections;using Unity.Collections.LowLevel.Unsafe;
public static class MT03Editor
{
 public const string Root="Assets/MT03Generated";const string WorldSource="Assets/MT02GeneratedV2/MT02World.unity";
 public static void Prepare()
 {
  Directory.CreateDirectory(MT03Runtime.Output);Directory.CreateDirectory(Root);PlayerSettings.enableFrameTimingStats=true;PlayerSettings.runInBackground=true;NativeLeakDetection.Mode=NativeLeakDetectionMode.EnabledWithStackTrace;
  if(!File.Exists(Root+"/MT03World.unity"))AssetDatabase.CopyAsset(WorldSource,Root+"/MT03World.unity");
  if(!File.Exists(Root+"/MT03Boot.unity")){EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);var controller=new GameObject("MT03 independent diagnostics").AddComponent<MT03Runtime>();controller.calibrationShader=Shader.Find("Hidden/MT03GpuCalibration");var camera=new GameObject("FixedCamera").AddComponent<Camera>();camera.tag="MainCamera";camera.farClipPlane=900;camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=new Color(.4f,.6f,.75f);camera.transform.position=new Vector3(140,100,-32);camera.transform.LookAt(new Vector3(64,3,64));var light=new GameObject("FixedSun").AddComponent<Light>();light.type=LightType.Directional;light.intensity=1.2f;light.shadows=LightShadows.Soft;light.transform.rotation=Quaternion.Euler(48,-35,0);RenderSettings.ambientLight=new Color(.35f,.4f,.5f);EditorSceneManager.SaveScene(SceneManager.GetActiveScene(),Root+"/MT03Boot.unity");}
  if(!File.Exists(Root+"/MT03Empty.unity")){EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);var camera=new GameObject("Empty control camera").AddComponent<Camera>();camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=Color.gray;EditorSceneManager.SaveScene(SceneManager.GetActiveScene(),Root+"/MT03Empty.unity");}
  if(!File.Exists(Root+"/MT03TerrainOnly.unity")){EditorSceneManager.OpenScene(Root+"/MT03World.unity");foreach(var go in SceneManager.GetActiveScene().GetRootGameObjects())if(go.GetComponent<Terrain>()==null)UnityEngine.Object.DestroyImmediate(go);EditorSceneManager.SaveScene(SceneManager.GetActiveScene(),Root+"/MT03TerrainOnly.unity");}
  AssetDatabase.SaveAssets();File.WriteAllText(MT03Runtime.Output+"/prepare.json","{\"frameTimingEnabled\":"+PlayerSettings.enableFrameTimingStats.ToString().ToLowerInvariant()+",\"vendorModified\":false,\"productModified\":false}");EditorApplication.Exit(0);
 }
 static BuildProfile Profile(string name,string[] scenes)
 {
  string path=Root+"/"+name+".asset";if(!File.Exists(path)){string s=File.ReadAllText("Assets/MT02GeneratedV2/LabRelease.asset");string list="  m_Scenes:\n";foreach(string scene in scenes)list+="  - m_enabled: 1\n    m_path: "+scene+"\n    m_guid: "+AssetDatabase.AssetPathToGUID(scene)+"\n";s=Regex.Replace(s,"  m_Scenes:\\n.*?(?=  m_HasScriptingDefines:)",list,RegexOptions.Singleline);File.WriteAllText(path,s);AssetDatabase.ImportAsset(path);}
  return AssetDatabase.LoadAssetAtPath<BuildProfile>(path);
 }
 public static void BuildEmpty(){Build("Empty",new[]{Root+"/MT03Empty.unity"});}
 public static void BuildTerrain(){Build("Terrain",new[]{Root+"/MT03TerrainOnly.unity"});}
 public static void BuildAudit(){Build("Audit",new[]{Root+"/MT03Boot.unity",Root+"/MT03World.unity"});}
 static void Build(string name,string[] scenes)
 {
  Directory.CreateDirectory(MT03Runtime.Output);NativeLeakDetection.Mode=NativeLeakDetectionMode.EnabledWithStackTrace;var profile=Profile(name,scenes);BuildProfile.SetActiveBuildProfile(profile);
  File.WriteAllText(MT03Runtime.Output+"/pre-build.json","{\"case\":\""+name+"\",\"frameTimingEnabled\":"+PlayerSettings.enableFrameTimingStats.ToString().ToLowerInvariant()+",\"liveMapMagicObjects\":"+UnityEngine.Object.FindObjectsByType<MapMagic.Core.MapMagicObject>().Length+"}");
  var report=BuildPipeline.BuildPlayer(new BuildPlayerWithProfileOptions{buildProfile=profile,locationPathName=MT03Runtime.Output+"/Player/MT03.exe",options=BuildOptions.None});File.WriteAllLines(MT03Runtime.Output+"/build-messages.txt",report.steps.SelectMany(s=>s.messages).Select(m=>m.type+": "+m.content));File.WriteAllText(MT03Runtime.Output+"/build.json","{\"case\":\""+name+"\",\"result\":\""+report.summary.result+"\",\"errors\":"+report.summary.totalErrors+",\"warnings\":"+report.summary.totalWarnings+",\"platform\":\""+report.summary.platform+"\",\"seconds\":"+report.summary.totalTime.TotalSeconds.ToString(System.Globalization.CultureInfo.InvariantCulture)+"}");EditorApplication.Exit(report.summary.totalErrors==0&&report.summary.result==UnityEditor.Build.Reporting.BuildResult.Succeeded?0:1);
 }
}
