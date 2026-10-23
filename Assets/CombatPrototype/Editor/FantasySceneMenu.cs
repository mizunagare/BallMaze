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
        // Domain reloads during editing and Play Mode must not reopen scenes.
        if (!Application.isBatchMode) EditorApplication.delayCall += OpenOnStartup;
    }
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
        if (SceneManager.sceneCount == 1 && SceneManager.GetActiveScene().path == DefaultScene) return;
        EditorSceneManager.OpenScene(DefaultScene, OpenSceneMode.Single);
    }
    public static bool ConfigureDefaults()
    {
        if (AssetDatabase.LoadAssetAtPath<SceneAsset>(DefaultScene) == null) {
            Debug.LogWarning("默认场景 ForestRuins 尚未导入，保留当前场景设置。");
            return false;
        }
        var scenes = new List<EditorBuildSettingsScene> { new EditorBuildSettingsScene(DefaultScene, true) };
        foreach (var scene in EditorBuildSettings.scenes) if (scene.path != DefaultScene) scenes.Add(scene);
        EditorBuildSettings.scenes = scenes.ToArray();
        return true;
    }
    [MenuItem("Ball Maze/打开森林遗迹场景")]
    public static void Open()
    {
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene(DefaultScene);
    }
}
