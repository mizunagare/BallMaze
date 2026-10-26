using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

[InitializeOnLoad]
public static class FantasySceneMenu
{
    public const string DefaultScene = "Assets/CombatPrototype/ForestRuins.unity";
    const string StartupKey = "CombatPrototype.ForestRuinsOpenedThisSession";
    static FantasySceneMenu()
    {
        EditorApplication.delayCall += ConfigurePlayEntry;
        EditorApplication.playModeStateChanged += state=>{if(state==PlayModeStateChange.ExitingEditMode)ConfigurePlayEntry();};
        // Domain reloads during editing and Play Mode must not reopen scenes.
        if (!Application.isBatchMode) EditorApplication.delayCall += OpenOnStartup;
    }
    static void ConfigurePlayEntry(){var boot=AssetDatabase.LoadAssetAtPath<SceneAsset>(GameEntry.BootPath);if(boot!=null)EditorSceneManager.playModeStartScene=GameEntry.EditorValidationEntry?null:boot;}
    static void OpenOnStartup()
    {
        if (SessionState.GetBool(StartupKey, false)) return;
        if (EditorApplication.isCompiling || EditorApplication.isUpdating) {
            EditorApplication.delayCall += OpenOnStartup;
            return;
        }
        SessionState.SetBool(StartupKey, true);
        if (EditorApplication.isPlayingOrWillChangePlaymode) return;
        if (!ConfigureDefaults()) return;
        // Protect edits recovered by Unity, or made before this script was installed.
        for (int i = 0; i < SceneManager.sceneCount; i++) if (SceneManager.GetSceneAt(i).isDirty) return;
        if (SceneManager.sceneCount == 1 && SceneManager.GetActiveScene().path == GameEntry.BootPath) return;
        EditorSceneManager.OpenScene(GameEntry.BootPath, OpenSceneMode.Single);
    }
    public static bool ConfigureDefaults()
    {
        if (AssetDatabase.LoadAssetAtPath<SceneAsset>(DefaultScene) == null) {
            Debug.LogWarning("默认场景 ForestRuins 尚未导入，保留当前场景设置。");
            return false;
        }
        var scenes = new List<EditorBuildSettingsScene> { new EditorBuildSettingsScene(GameEntry.BootPath,true),new EditorBuildSettingsScene(GameEntry.TitlePath, true),new EditorBuildSettingsScene(DefaultScene, true) };
        foreach (var scene in EditorBuildSettings.scenes) if (scene.path != DefaultScene && scene.path != GameEntry.TitlePath && scene.path != GameEntry.BootPath) scenes.Add(scene);
        EditorBuildSettings.scenes = scenes.ToArray();
        return true;
    }
    [MenuItem("万象归途/打开森林遗迹场景")]
    public static void Open()
    {
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene(DefaultScene);
    }
    [MenuItem("万象归途/打开正式开始入口")]
    public static void OpenEntry(){if(EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())EditorSceneManager.OpenScene(GameEntry.BootPath);}
}
