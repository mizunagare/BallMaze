using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Profile;
using UnityEditor.Build.Reporting;
using UnityEditorInternal;
using UnityEngine;

// Build-copy-only instrumentation. Never runs in a Player or writes the development tree.
public sealed class RegionRecordsBuildGuard : IPreprocessBuildWithReport, IPostprocessBuildWithReport
{
    static readonly string[] Paths={"ProjectSettings/EditorBuildSettings.asset","ProjectSettings/GraphicsSettings.asset",
        "ProjectSettings/ProjectSettings.asset","ProjectSettings/UnityConnectSettings.asset",
        "Assets/Settings/PC_RPAsset.asset","Assets/Settings/UniversalRenderPipelineGlobalSettings.asset"};
    static string Evidence=>Environment.GetEnvironmentVariable("UX06_BUILD_EVIDENCE");
    public int callbackOrder=>int.MaxValue-1;
    public static void Prepare()
    {
        if(Environment.GetEnvironmentVariable("UX06_SCRATCH")!="1" || string.IsNullOrEmpty(Evidence) ||
            Path.GetFullPath(Application.dataPath).Replace('\\','/').StartsWith("I:/unity/",StringComparison.OrdinalIgnoreCase))
            throw new BuildFailedException("UX06 requires explicitly isolated writable build copy");
        Directory.CreateDirectory(Evidence);
        Snapshot("IMPORTED");
        var profile=AssetDatabase.LoadAssetAtPath<BuildProfile>(ReleaseDiagnosticsGuard.ProfilePath);
        BuildProfile.SetActiveBuildProfile(profile);
        var type=AppDomain.CurrentDomain.GetAssemblies().Select(a=>a.GetType("UnityEngine.Connect.UnityConnectSettings")).First(t=>t!=null);
        var property=type.GetProperty("enabled",BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic);
        property.SetValue(null,false);
        AssetDatabase.SaveAssets();
        ReleaseDiagnosticsGuard.ValidateProfile();ReleaseDiagnosticsGuard.NativeGate();
        Snapshot("APPROVED_EFFECTIVE");
        // Compare the two imported URP objects with the approved raw baseline,
        // deserialized by this exact Unity version. OnAfterDeserialize clears the
        // runtime-only list; build-time lists are generated from editor settings.
        foreach(string path in Paths.Where(p=>p.StartsWith("Assets/",StringComparison.Ordinal)))
        {
            var original=InternalEditorUtility.LoadSerializedFileAndForget(Path.Combine("UX06Baseline",path));
            var actual=AssetDatabase.LoadMainAssetAtPath(path);
            if(original.Length!=1 || actual==null)throw new BuildFailedException("Cannot compare baseline "+path);
            string baseline=EditorJsonUtility.ToJson(original[0],true), imported=EditorJsonUtility.ToJson(actual,true);
            File.WriteAllText(Path.Combine(Evidence,Path.GetFileName(path)+".baseline-effective.json"),baseline);
            File.WriteAllText(Path.Combine(Evidence,Path.GetFileName(path)+".imported-effective.json"),imported);
            if(baseline!=imported)throw new BuildFailedException("URP effective settings differ from baseline: "+path);
            UnityEngine.Object.DestroyImmediate(original[0]);
        }
    }
    static void Snapshot(string phase)
    {
        string directory=Path.Combine(Evidence,phase);Directory.CreateDirectory(directory);
        foreach(string path in Paths)
        {
            string target=Path.Combine(directory,path);Directory.CreateDirectory(Path.GetDirectoryName(target));
            File.Copy(path,target,false);
        }
    }
    public void OnPreprocessBuild(BuildReport report)
    {
        if(string.IsNullOrEmpty(Evidence))return;
        ReleaseDiagnosticsGuard.NativeGate();Snapshot("PACKAGING");
    }
    public void OnPostprocessBuild(BuildReport report)
    {
        if(string.IsNullOrEmpty(Evidence))return;
        ReleaseDiagnosticsGuard.NativeGate();Snapshot("POSTPROCESS");
    }
    public static void Finish(BuildReport report)
    {
        ReleaseDiagnosticsGuard.NativeGate();Snapshot("FINISHED");
        string output=Path.GetFullPath(report.summary.outputPath).Replace('\\','/');
        var candidates=Directory.GetFiles("Library/Bee","Player*-inputdata.json")
            .Where(p=>File.ReadAllText(p).Contains(output)).ToArray();
        if(candidates.Length!=1)throw new BuildFailedException("Ambiguous actual Bee input");
        string bee=File.ReadAllText(candidates[0]);
        File.WriteAllText(Path.Combine(Evidence,"ACTUAL_BEE_INPUT.json"),bee);
        string services=ReleaseDiagnosticsGuard.Object(ReleaseDiagnosticsGuard.Object(bee,"PlayerBuildProgramLibrary.Data.PlayerBuildConfig"),"Services");
        foreach(string field in new[]{"EnableUnityConnect","EnablePerformanceReporting","EnableAnalytics","EnableCrashReporting","EnableInsights"})
        {
            var m=System.Text.RegularExpressions.Regex.Matches(services,"\""+field+"\"\\s*:\\s*(false|true)(?=\\s*[,}])");
            if(m.Count!=1||m[0].Groups[1].Value!="false")throw new BuildFailedException("Enabled service in actual packaging: "+field);
        }
        if((report.summary.options&BuildOptions.Development)==0)ReleaseDiagnosticsGuard.Publish(report);
    }
}
