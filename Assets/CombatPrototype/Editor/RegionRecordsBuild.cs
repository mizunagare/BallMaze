using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

public static class RegionRecordsBuild
{
    public static void Run()
    {
        RegionRecordsBuildGuard.Prepare();
        RegionRecordsTests.Run();
        string output=Environment.GetEnvironmentVariable("UX06_OUTPUT");
        if(string.IsNullOrEmpty(output)||!Path.IsPathRooted(output)) throw new Exception("Explicit output required");
        bool acceptance=Environment.GetEnvironmentVariable("UX06_ACCEPTANCE")=="1";
        var report=BuildPipeline.BuildPlayer(new BuildPlayerOptions {
            scenes=new[]{GameEntry.BootPath,GameEntry.TitlePath,GameEntry.ForestPath},
            locationPathName=output,target=BuildTarget.StandaloneWindows64,
            options=acceptance?BuildOptions.Development:BuildOptions.None,
            extraScriptingDefines=acceptance?new[]{"UX06_ACCEPTANCE"}:Array.Empty<string>() });
        Debug.Log("UX06_BUILD "+report.summary.result+" warnings="+report.summary.totalWarnings+" errors="+report.summary.totalErrors);
        RegionRecordsBuildGuard.Finish(report);
        EditorApplication.Exit(report.summary.result==BuildResult.Succeeded?0:1);
    }
}
