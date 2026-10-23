using UnityEditor;
using UnityEngine;

// The Editor's Stop button and closing the Editor also preserve the current play session.
[InitializeOnLoad]
public static class CombatSaveEditorLifecycle
{
    static CombatSaveEditorLifecycle()
    {
        EditorApplication.playModeStateChanged += state => { if (state == PlayModeStateChange.ExitingPlayMode) PersistAll(); };
        EditorApplication.quitting += PersistAll;
        AssemblyReloadEvents.beforeAssemblyReload += PersistAll;
    }
    static void PersistAll()
    {
        foreach (var saves in Object.FindObjectsByType<CombatSaveSystem>(FindObjectsInactive.Include, FindObjectsSortMode.None))
            if (saves.IsInitialized) saves.SaveBeforeExit();
    }
}
