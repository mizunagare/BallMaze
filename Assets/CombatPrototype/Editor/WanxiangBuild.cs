using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Profile;
public static class WanxiangBuild {
 [MenuItem("万象归途/构建/Windows 正式版")]
 public static void Windows(){Build(Path.GetFullPath("Builds/WanxiangGuitu/"+DateTime.UtcNow.ToString("yyyyMMdd-HHmmss-ffff")+"/WanxiangGuitu.exe"));}
 public static void ValidateBuild(){try{string root=Environment.GetEnvironmentVariable("UNITY_TEST_ROOT")??throw new Exception("Explicit local results directory required");Build(Path.Combine(root,"Release","WanxiangGuitu.exe"));EditorApplication.Exit(0);}catch(Exception e){UnityEngine.Debug.LogException(e);EditorApplication.Exit(1);}}
 static void Build(string output){
  var p=AssetDatabase.LoadAssetAtPath<BuildProfile>(ReleaseDiagnosticsGuard.ProfilePath);if(p==null)throw new Exception("Release profile missing");
  BuildProfile.SetActiveBuildProfile(p);ReleaseDiagnosticsGuard.ValidateProfile();ReleaseDiagnosticsGuard.NativeGate();Directory.CreateDirectory(Path.GetDirectoryName(output));
  var report=BuildPipeline.BuildPlayer(new BuildPlayerWithProfileOptions{buildProfile=p,locationPathName=output,options=BuildOptions.None});
  File.WriteAllText(output+".summary.txt","result="+report.summary.result+"\nerrors="+report.summary.totalErrors+"\nwarnings="+report.summary.totalWarnings+"\noptions="+report.summary.options);
  ReleaseDiagnosticsGuard.Publish(report);UnityEngine.Debug.Log("WANXIANG_RELEASE_BUILD_PASS "+output);
 }
}
