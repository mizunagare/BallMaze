using System;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

public static class ObjectiveHistoryProbeBuild
{
    public static void Run()
    {
        string output=Environment.GetEnvironmentVariable("UX05_PROBE_OUTPUT");
        if (string.IsNullOrEmpty(output) || !System.IO.Path.IsPathRooted(output))
            throw new InvalidOperationException("Explicit isolated output is required");
        var result=BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes=new[] {GameEntry.BootPath,GameEntry.TitlePath,GameEntry.ForestPath},
            locationPathName=output,
            target=BuildTarget.StandaloneWindows64,
            options=BuildOptions.Development,
            extraScriptingDefines=new[] {"UX05_ENTRY_PROBE","UX_ACCEPTANCE","UX05_V10_OBJECTIVE_PROBE"}
        });
        Debug.Log("UX05_ACCEPTANCE_BUILD " + result.summary.result);
        EditorApplication.Exit(result.summary.result==BuildResult.Succeeded?0:1);
    }
}


