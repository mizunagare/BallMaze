using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
public static class T06BuildCheck
{
 public static void Build(){const string root="C:/Users/guan/Documents/unitytest/T06Validation";Directory.CreateDirectory(root+"/BuildSmoke");const string matPath="Assets/CombatPrototype/Resources/CombatFeedback/AdventureUnlit.mat";if(AssetDatabase.LoadAssetAtPath<UnityEngine.Material>(matPath)==null){var shader=UnityEngine.Shader.Find("Universal Render Pipeline/Unlit");if(shader==null)throw new Exception("Missing required runtime shader");AssetDatabase.CreateAsset(new UnityEngine.Material(shader){name="AdventureUnlit"},matPath);AssetDatabase.SaveAssets();}var report=BuildPipeline.BuildPlayer(new BuildPlayerOptions{scenes=new[]{"Assets/CombatPrototype/ForestRuins.unity"},locationPathName=root+"/BuildSmoke/AdventureTest.exe",target=BuildTarget.StandaloneWindows64,options=BuildOptions.Development});var s=report.summary;File.WriteAllText(root+"/BuildSummary.txt",s.result+"\nerrors="+s.totalErrors+"\nwarnings="+s.totalWarnings+"\nbytes="+s.totalSize+"\nduration="+s.totalTime);if(s.result!=BuildResult.Succeeded)throw new Exception("Local build failed "+s.result);UnityEngine.Debug.Log("T06_WINDOWS_BUILD_PASSED");}
}
