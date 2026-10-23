using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class BallMazeDemoBuilder
{
    [MenuItem("Ball Maze/Create Demo Scene")]
    public static void CreateScene()
    {
        if (!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo()) return;
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        new GameObject("Ball Maze Demo", typeof(BallMazeDemo));
        EditorSceneManager.SaveScene(scene, "Assets/BallMazeDemo/BallMazeDemo.unity");
        Selection.activeGameObject = GameObject.Find("Ball Maze Demo");
        Debug.Log("Demo ready. Press Play. WASD / arrows to move; R to restart.");
    }

    public static void CreateSceneBatch()
    {
        CreateScene();
        if (GameObject.Find("Ball Maze Demo") == null)
            throw new System.Exception("Demo scene was not created.");
    }
}
