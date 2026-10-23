using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

[InitializeOnLoad]
public static class EditableMazeBuilder
{
    const string Root = "Assets/EditableMaze";
    const string ScenePath = Root + "/BallMazeEditable.unity";
    static EditableMazeBuilder() { EditorApplication.delayCall += FirstImport; }

    static void FirstImport()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode || EditorApplication.isCompiling) {
            EditorApplication.delayCall += FirstImport;
            return;
        }
        if (!File.Exists(ScenePath)) Create();
    }

    [MenuItem("Ball Maze/Open Editable Scene")]
    public static void Open()
    {
        if (!File.Exists(ScenePath)) Create();
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene(ScenePath);
    }

    public static void Create()
    {
        // Never overwrite a level the user has already edited.
        if (File.Exists(ScenePath)) { Validate(); return; }
        Directory.CreateDirectory(Root + "/Materials");
        Directory.CreateDirectory(Root + "/Prefabs");
        AssetDatabase.Refresh();
        Scene previous = SceneManager.GetActiveScene();
        bool replaceEmpty = Application.isBatchMode || (string.IsNullOrEmpty(previous.path) && !previous.isDirty);
        if (!replaceEmpty && string.IsNullOrEmpty(previous.path)) { Debug.LogWarning("Save your current scene first, then use Ball Maze > Open Editable Scene."); return; }
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, replaceEmpty ? NewSceneMode.Single : NewSceneMode.Additive);
        try {
            SceneManager.SetActiveScene(scene);
            var floor = Material("Floor", new Color(.12f, .2f, .27f));
            var wall = Material("Wall", new Color(.28f, .43f, .52f));
            var gold = Material("Key", new Color(1, .73f, .12f));
            var blue = Material("Player", new Color(.25f, .85f, 1));
            var green = Material("Exit", new Color(.25f, .9f, .5f));
            Transform walls = new GameObject("Walls - move or duplicate children").transform;
            Transform keys = new GameObject("Keys - duplicate to add collectibles").transform;
            Make("Floor", PrimitiveType.Cube, new Vector3(22, 1, 22), floor).transform.position = new Vector3(0, -.5f, 0);
            GameObject wallSource = Make("Wall", PrimitiveType.Cube, new Vector3(2, 1.2f, 2), wall);
            GameObject wallPrefab = SavePrefab(wallSource);
            GameObject keySource = Make("Key", PrimitiveType.Cube, Vector3.one * .55f, gold);
            keySource.GetComponent<BoxCollider>().isTrigger = true;
            keySource.AddComponent<MazeKey>();
            GameObject keyPrefab = SavePrefab(keySource);
            GameObject exitSource = Make("Exit", PrimitiveType.Cube, new Vector3(1.7f, .08f, 1.7f), green);
            exitSource.GetComponent<BoxCollider>().isTrigger = true;
            exitSource.GetComponent<BoxCollider>().size = new Vector3(1, 18, 1);
            exitSource.GetComponent<BoxCollider>().center = new Vector3(0, 8, 0);
            exitSource.AddComponent<MazeExit>();
            GameObject exitPrefab = SavePrefab(exitSource);
            string[] map = { "###########", "#S....#..K#", "#.##..#.#.#", "#..#....#.#", "##.#.####.#", "#K.#......#", "#..###.##.#", "#......#..#", "#.####.#K.#", "#......#.E#", "###########" };
            Vector3 spawn = Vector3.zero;
            for (int z = 0; z < 11; z++) for (int x = 0; x < 11; x++) {
                Vector3 p = new Vector3((x - 5) * 2, 0, (5 - z) * 2);
                if (map[z][x] == '#') Place(wallPrefab, p + Vector3.up * .6f, walls);
                if (map[z][x] == 'K') Place(keyPrefab, p + Vector3.up * .8f, keys);
                if (map[z][x] == 'E') Place(exitPrefab, p + Vector3.up * .04f, null);
                if (map[z][x] == 'S') spawn = p + Vector3.up * .6f;
            }
            MazeGame game = new GameObject("GameManager").AddComponent<MazeGame>();
            GameObject playerSource = Make("Player", PrimitiveType.Sphere, Vector3.one, blue);
            Rigidbody rb = playerSource.AddComponent<Rigidbody>();
            rb.linearDamping = 2;
            rb.angularDamping = .5f;
            rb.interpolation = RigidbodyInterpolation.Interpolate;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
            playerSource.AddComponent<MazePlayer>();
            var player = Place(SavePrefab(playerSource), spawn, null).GetComponent<MazePlayer>();
            player.game = game;
            game.player = player;
            PrefabUtility.RecordPrefabInstancePropertyModifications(player);
            Camera camera = new GameObject("Main Camera", typeof(Camera), typeof(AudioListener)).GetComponent<Camera>();
            camera.tag = "MainCamera";
            camera.transform.position = new Vector3(0, 27, -16);
            camera.transform.LookAt(Vector3.zero);
            camera.orthographic = true;
            camera.orthographicSize = 14;
            camera.clearFlags = CameraClearFlags.SolidColor;
            camera.backgroundColor = new Color(.035f, .06f, .09f);
            Light sun = new GameObject("Sun").AddComponent<Light>();
            sun.type = LightType.Directional;
            sun.intensity = 1.5f;
            sun.transform.rotation = Quaternion.Euler(50, -30, 0);
            RenderSettings.ambientLight = new Color(.6f, .65f, .7f);
            EditorSceneManager.SaveScene(scene, ScenePath);
            AssetDatabase.SaveAssets();
            ValidateScene(scene);
            Debug.Log("EDITABLE_MAZE_VALIDATED: Scene saved; 3 keys, player/manager references, trigger colliders and prefab instances verified.");
        }
        finally {
            if (!replaceEmpty && previous.IsValid()) SceneManager.SetActiveScene(previous);
            if (!replaceEmpty) EditorSceneManager.CloseScene(scene, true);
        }
    }

    static Material Material(string name, Color color)
    {
        string path = Root + "/Materials/" + name + ".mat";
        var existing = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (existing != null) return existing;
        var material = new Material(Shader.Find("Universal Render Pipeline/Lit")) { color = color };
        AssetDatabase.CreateAsset(material, path);
        return material;
    }
    static GameObject Make(string name, PrimitiveType shape, Vector3 size, Material material)
    {
        var obj = GameObject.CreatePrimitive(shape);
        obj.name = name;
        obj.transform.localScale = size;
        obj.GetComponent<Renderer>().sharedMaterial = material;
        return obj;
    }
    static GameObject SavePrefab(GameObject source)
    {
        var prefab = PrefabUtility.SaveAsPrefabAsset(source, Root + "/Prefabs/" + source.name + ".prefab");
        UnityEngine.Object.DestroyImmediate(source);
        return prefab;
    }
    static GameObject Place(GameObject prefab, Vector3 p, Transform parent)
    {
        var obj = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
        obj.transform.SetParent(parent);
        obj.transform.position = p;
        return obj;
    }
    public static void Validate()
    {
        Scene scene = SceneManager.GetSceneByPath(ScenePath);
        bool opened = !scene.isLoaded;
        if (opened) scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Additive);
        try { ValidateScene(scene); Debug.Log("EDITABLE_MAZE_VALIDATED: saved scene passed checks."); }
        finally { if (opened) EditorSceneManager.CloseScene(scene, true); }
    }
    static void ValidateScene(Scene scene)
    {
        MazeGame game = null;
        int count = 0, exits = 0, prefabCount = 0;
        foreach (var root in scene.GetRootGameObjects()) {
            foreach (var manager in root.GetComponentsInChildren<MazeGame>()) game = manager;
            foreach (var key in root.GetComponentsInChildren<MazeKey>()) {
                if (!key.GetComponent<Collider>().isTrigger) throw new Exception("Key trigger missing");
                count++;
            }
            exits += root.GetComponentsInChildren<MazeExit>().Length;
            foreach (var t in root.GetComponentsInChildren<Transform>())
                if (PrefabUtility.IsAnyPrefabInstanceRoot(t.gameObject)) prefabCount++;
            if (root.GetComponent<BallMazeDemo>() != null) throw new Exception("Runtime generator found");
        }
        if (game == null || game.player == null || game.player.game != game || count != 3 || exits != 1 || prefabCount < 60)
            throw new Exception("Editable maze validation failed");
    }
}


