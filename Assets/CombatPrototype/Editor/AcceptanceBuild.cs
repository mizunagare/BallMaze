using System;
using System.IO;
using System.Security.Cryptography;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
#pragma warning disable 0618 // BuildTargetGroup scripting-define API is obsolete but still functional in 6000.6.5

// Acceptance build tooling for UX-PROGRESSION-03A real Player acceptance.
// Three discrete entry points are used so the driver can orchestrate them
// across separate Unity invocations (toggling the UX_ACCEPTANCE scripting
// define triggers a script recompile, which must not interrupt a build):
//   1. SetAcceptanceDefine  -> persist UX_ACCEPTANCE into Standalone defines
//   2. BuildAcceptance      -> build the Acceptance EXE (marker MUST be present),
//                              then RESET the define back to baseline
//   3. BuildNoDefine        -> build without the define (marker MUST be absent;
//                              proves the #if UX_ACCEPTANCE gating / shipping
//                              exclusion)
//
// The harness marker is hardcoded here (not referenced from the gated class) so
// this Editor script compiles regardless of the current scripting defines.
public static class AcceptanceBuild
{
    // Boot -> Title (GameEntry entry flow) -> ForestRuins (real gameplay scene).
    // The harness authorizes gameplay through the real public entry API, so the
    // Title scene must be in the build. ForestRuins is the genuine combat scene.
    static readonly string[] SCENES = new[] {
        "Assets/CombatPrototype/Boot.unity",
        "Assets/CombatPrototype/Title.unity",
        "Assets/CombatPrototype/ForestRuins.unity"
    };
    const string OUT_ACCEPTANCE = "Builds/WanxiangGuitu.Acceptance/WanxiangGuitu.exe";
    const string OUT_NODEFINE = "Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu.exe";
    const string ACCEPTANCE_DEFINE = "UX_ACCEPTANCE";
    const string MARKER = "UX_ACCEPTANCE_HARNESS_v1";
    const string GROUP = "Standalone";

    static void Guard()
    {
        if (Application.unityVersion != "6000.6.5f1") Debug.LogWarning("Unity version mismatch: " + Application.unityVersion);
    }

    public static void SetAcceptanceDefine()
    {
        Guard();
        string[] _d; PlayerSettings.GetScriptingDefineSymbolsForGroup(BuildTargetGroup.Standalone, out _d);
        var defs = new List<string>(_d);
        if (!defs.Contains(ACCEPTANCE_DEFINE)) defs.Add(ACCEPTANCE_DEFINE);
        PlayerSettings.SetScriptingDefineSymbolsForGroup(BuildTargetGroup.Standalone, defs.ToArray());
        AssetDatabase.SaveAssets();
        Debug.Log("ACCEPTANCE_DEFINE_SET (persisted; recompile will occur on next launch)");
        EditorApplication.Exit(0);
    }

    public static void BuildAcceptance()
    {
        Guard();
        string[] _ad; PlayerSettings.GetScriptingDefineSymbolsForGroup(BuildTargetGroup.Standalone, out _ad);
        var defs = _ad;
        if (Array.IndexOf(defs, ACCEPTANCE_DEFINE) < 0)
        {
            Debug.LogError("UX_ACCEPTANCE not defined before Acceptance build; run SetAcceptanceDefine first.");
            ResetDefine();
            EditorApplication.Exit(2); return;
        }
        BuildReport rep = BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes = SCENES,
            locationPathName = Path.GetFullPath(OUT_ACCEPTANCE),
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.Development
        });
        int code = 1;
        string sha = null; bool marker = false;
        if (rep.summary.result != BuildResult.Succeeded)
        {
            Debug.LogError("Acceptance build failed: " + rep.summary.totalErrors + " errors, " + rep.summary.totalWarnings + " warnings");
        }
        else
        {
            sha = Sha(OUT_ACCEPTANCE);
            // The marker lives in the managed assembly (code string constants are
            // stored there as UTF-16), NOT in the small native EXE launcher.
            marker = GrepBuildOutput(Path.GetDirectoryName(OUT_ACCEPTANCE), MARKER);
            if (!marker) { Debug.LogError("Acceptance build output missing harness marker -- harness did not compile in"); code = 3; }
            else { WriteManifest(sha, marker, rep.summary.totalWarnings); Debug.Log("ACCEPTANCE_BUILD_PASS exeSha=" + sha + " markerPresent=" + marker); code = 0; }
        }
        // EditorApplication.Exit does NOT unwind try/finally, so the define reset
        // must happen explicitly BEFORE exiting (otherwise UX_ACCEPTANCE leaks
        // into ProjectSettings and poisons the NoDefine build).
        ResetDefine();
        EditorApplication.Exit(code);
    }

    public static void BuildNoDefine()
    {
        Guard();
        string[] _nd; PlayerSettings.GetScriptingDefineSymbolsForGroup(BuildTargetGroup.Standalone, out _nd);
        var defs = _nd;
        if (Array.IndexOf(defs, ACCEPTANCE_DEFINE) >= 0)
        {
            Debug.LogError("UX_ACCEPTANCE still defined before NoDefine build; reset first.");
            EditorApplication.Exit(2); return;
        }
        BuildReport rep = BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes = SCENES,
            locationPathName = Path.GetFullPath(OUT_NODEFINE),
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.Development
        });
        if (rep.summary.result != BuildResult.Succeeded)
        {
            Debug.LogError("NoDefine build failed: " + rep.summary.totalErrors + " errors");
            EditorApplication.Exit(1); return;
        }
        bool marker = GrepBuildOutput(Path.GetDirectoryName(OUT_NODEFINE), MARKER);
        if (marker) { Debug.LogError("NoDefine build output contains harness marker -- shipping exclusion FAILED"); EditorApplication.Exit(3); return; }
        Debug.Log("NODEFINE_BUILD_PASS markerAbsent=" + (!marker));
        EditorApplication.Exit(0);
    }

    static void ResetDefine()
    {
        string[] _o; PlayerSettings.GetScriptingDefineSymbolsForGroup(BuildTargetGroup.Standalone, out _o);
        var original = new List<string>(_o);
        original.Remove(ACCEPTANCE_DEFINE);
        PlayerSettings.SetScriptingDefineSymbolsForGroup(BuildTargetGroup.Standalone, original.ToArray());
        AssetDatabase.SaveAssets();
    }

    // Grep the built output for the marker: the managed assembly first (Mono
    // builds store code strings there as UTF-16), then the EXE launcher.
    static bool GrepBuildOutput(string buildDir, string needle)
    {
        string dll = Path.Combine(buildDir, "WanxiangGuitu_Data", "Managed", "Assembly-CSharp.dll");
        if (File.Exists(dll) && Grep(dll, needle)) return true;
        string exe = Path.Combine(buildDir, "WanxiangGuitu.exe");
        if (File.Exists(exe) && Grep(exe, needle)) return true;
        return false;
    }

    static void WriteManifest(string exeSha, bool marker, int warnings)
    {
        var lines = new List<string>();
        lines.Add("{");
        lines.Add("  \"acceptanceExe\": \"" + Path.GetFullPath(OUT_ACCEPTANCE).Replace("\\", "/") + "\",");
        lines.Add("  \"exeSha256\": \"" + exeSha + "\",");
        lines.Add("  \"unityVersion\": \"" + Application.unityVersion + "\",");
        lines.Add("  \"marker\": \"" + MARKER + "\",");
        lines.Add("  \"markerPresent\": " + (marker ? "true" : "false") + ",");
        lines.Add("  \"buildWarnings\": " + warnings + ",");
        lines.Add("  \"builtAt\": \"" + DateTime.UtcNow.ToString("o") + "\"");
        lines.Add("}");
        Directory.CreateDirectory("Builds");
        File.WriteAllText("Builds/acceptance_manifest.json", string.Join("\n", lines));
    }

    static string Sha(string path)
    {
        using (var s = SHA256.Create()) return BitConverter.ToString(s.ComputeHash(File.ReadAllBytes(path))).Replace("-", "").ToLowerInvariant();
    }
    static bool Grep(string path, string needle)
    {
        try
        {
            byte[] data = File.ReadAllBytes(path);
            if (ContainsBytes(data, System.Text.Encoding.ASCII.GetBytes(needle))) return true;
            if (ContainsBytes(data, System.Text.Encoding.Unicode.GetBytes(needle))) return true;
            if (ContainsBytes(data, System.Text.Encoding.UTF8.GetBytes(needle))) return true;
            return false;
        }
        catch { return false; }
    }
    static bool ContainsBytes(byte[] hay, byte[] needle)
    {
        if (hay == null || needle == null || hay.Length < needle.Length) return false;
        for (int i = 0; i <= hay.Length - needle.Length; i++)
        {
            bool ok = true;
            for (int j = 0; j < needle.Length; j++) if (hay[i + j] != needle[j]) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }
}
