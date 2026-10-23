using System;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class CombatPrototypeBuilder
{
    const string Root = "Assets/CombatPrototype";
    const string ScenePath = Root + "/CombatPlayground.unity";
    [MenuItem("Ball Maze/打开战斗试玩（默认场景）")]
    public static void Open()
    {
        FantasySceneMenu.Open();
    }
    public static void Build()
    {
        if (File.Exists(ScenePath)) { Validate(); return; }
        Directory.CreateDirectory(Root + "/Materials");
        Directory.CreateDirectory(Root + "/Prefabs");
        AssetDatabase.Refresh();
        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var ground = Mat("Ground", new Color(.19f, .28f, .22f));
        var stone = Mat("Stone", new Color(.34f, .4f, .43f));
        var blue = Mat("Hero", new Color(.12f, .6f, .95f));
        var green = Mat("Goblin", new Color(.4f, .72f, .18f));
        var metal = Mat("Sword", new Color(.8f, .88f, .95f));
        var gold = Mat("Gold", new Color(1, .68f, .15f));
        var red = Mat("AttackWarning", new Color(1, .15f, .08f));
        var dark = Mat("Dark", new Color(.05f, .08f, .1f));
        Shape("Ground", PrimitiveType.Cube, new Vector3(0, -.5f, 0), new Vector3(40, 1, 40), ground);
        Transform environment = new GameObject("Environment - edit obstacles here").transform;
        Shape("North boundary", PrimitiveType.Cube, new Vector3(0, 1, 20), new Vector3(41, 2, 1), stone, environment);
        Shape("South boundary", PrimitiveType.Cube, new Vector3(0, 1, -20), new Vector3(41, 2, 1), stone, environment);
        Shape("West boundary", PrimitiveType.Cube, new Vector3(-20, 1, 0), new Vector3(1, 2, 40), stone, environment);
        Shape("East boundary", PrimitiveType.Cube, new Vector3(20, 1, 0), new Vector3(1, 2, 40), stone, environment);
        foreach (var p in new[] { new Vector3(-11, 1.5f, -7), new Vector3(11, 1.5f, -7), new Vector3(-11, 1.5f, 8), new Vector3(11, 1.5f, 8) })
            Shape("Stone pillar", PrimitiveType.Cube, p, new Vector3(2, 3, 2), stone, environment);
        for (int i = -3; i <= 3; i++)
            Shape("Path stone", PrimitiveType.Cube, new Vector3(0, .025f, i * 2.7f), new Vector3(2.4f, .05f, 1.8f), stone, environment, false);

        var playerObject = Actor("Hero", blue);
        var hero = playerObject.AddComponent<ThirdPersonHero>();
        Transform pivot = new GameObject("Sword pivot").transform;
        pivot.SetParent(playerObject.transform, false);
        pivot.localPosition = new Vector3(.48f, 1.1f, .1f);
        Shape("Sword blade", PrimitiveType.Cube, new Vector3(0, 0, .6f), new Vector3(.13f, .13f, 1.2f), metal, pivot, false);
        Shape("Sword guard", PrimitiveType.Cube, new Vector3(0, 0, .12f), new Vector3(.45f, .15f, .12f), gold, pivot, false);
        hero.weaponPivot = pivot;
        Face(playerObject.transform, dark);
        var heroPrefab = PrefabUtility.SaveAsPrefabAsset(playerObject, Root + "/Prefabs/Hero.prefab");
        UnityEngine.Object.DestroyImmediate(playerObject);
        hero = ((GameObject)PrefabUtility.InstantiatePrefab(heroPrefab)).GetComponent<ThirdPersonHero>();
        hero.transform.position = new Vector3(0, .1f, -7);
        var camera = new GameObject("Main Camera", typeof(Camera), typeof(AudioListener)).GetComponent<Camera>();
        camera.tag = "MainCamera";
        camera.fieldOfView = 65;
        camera.nearClipPlane = .05f;
        camera.farClipPlane = 150;
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(.22f, .32f, .42f);
        camera.transform.position = new Vector3(0, 4.4f, -12.3f);
        camera.transform.rotation = Quaternion.Euler(28, 0, 0);
        var orbit = camera.gameObject.AddComponent<OrbitCamera>();
        orbit.target = hero.transform;
        hero.cameraTransform = camera.transform;
        PrefabUtility.RecordPrefabInstancePropertyModifications(hero);

        var enemyObject = Actor("Goblin", green);
        enemyObject.GetComponent<CombatHealth>().maxHealth = 60;
        var enemySource = enemyObject.AddComponent<CombatEnemy>();
        var ring = Shape("Red attack warning", PrimitiveType.Cylinder, new Vector3(0, .035f, 0), new Vector3(3.4f, .025f, 3.4f), red, enemyObject.transform, false);
        enemySource.warningRing = ring.transform;
        ring.SetActive(false);
        Face(enemyObject.transform, dark);
        var enemyPrefab = PrefabUtility.SaveAsPrefabAsset(enemyObject, Root + "/Prefabs/Goblin.prefab");
        UnityEngine.Object.DestroyImmediate(enemyObject);
        var enemies = new CombatEnemy[3];
        Vector3[] positions = { new Vector3(0, .1f, 1), new Vector3(-6, .1f, 7), new Vector3(6, .1f, 10) };
        Transform camp = new GameObject("Enemies - Goblin instances").transform;
        for (int i = 0; i < enemies.Length; i++) {
            enemies[i] = ((GameObject)PrefabUtility.InstantiatePrefab(enemyPrefab)).GetComponent<CombatEnemy>();
            enemies[i].name = "Goblin " + (i + 1);
            enemies[i].transform.SetParent(camp);
            enemies[i].transform.position = positions[i];
            enemies[i].target = hero;
            PrefabUtility.RecordPrefabInstancePropertyModifications(enemies[i]);
        }
        var session = new GameObject("Combat Session").AddComponent<CombatSession>();
        session.hero = hero;
        session.enemies = enemies;
        session.orbit = orbit;
        var sun = new GameObject("Sun").AddComponent<Light>();
        sun.type = LightType.Directional;
        sun.intensity = 1.6f;
        sun.transform.rotation = Quaternion.Euler(50, -35, 0);
        RenderSettings.ambientLight = new Color(.65f, .68f, .72f);
        EditorSceneManager.SaveScene(scene, ScenePath);
        AssetDatabase.SaveAssets();
        ValidateScene(scene);
        CheckCombat(session);
        Debug.Log("COMBAT_VALIDATED: editable scene, prefab references, frontal melee damage, rear miss, death and restart passed.");
    }
    static GameObject Actor(string name, Material material)
    {
        var root = new GameObject(name);
        var controller = root.AddComponent<CharacterController>();
        controller.height = 2;
        controller.radius = .4f;
        controller.center = Vector3.up;
        controller.stepOffset = .3f;
        controller.minMoveDistance = 0;
        root.AddComponent<CombatHealth>();
        Shape("Body", PrimitiveType.Capsule, Vector3.up, new Vector3(.8f, 1, .8f), material, root.transform, false);
        return root;
    }
    static void Face(Transform parent, Material material)
    {
        Shape("Eyes", PrimitiveType.Cube, new Vector3(0, 1.65f, .37f), new Vector3(.5f, .12f, .08f), material, parent, false);
    }
    static GameObject Shape(string name, PrimitiveType type, Vector3 position, Vector3 scale, Material material, Transform parent = null, bool collision = true)
    {
        var obj = GameObject.CreatePrimitive(type);
        obj.name = name;
        obj.transform.SetParent(parent, false);
        obj.transform.localPosition = position;
        obj.transform.localScale = scale;
        obj.GetComponent<Renderer>().sharedMaterial = material;
        if (!collision) UnityEngine.Object.DestroyImmediate(obj.GetComponent<Collider>());
        return obj;
    }
    static Material Mat(string name, Color color)
    {
        var existing = AssetDatabase.LoadAssetAtPath<Material>(Root + "/Materials/" + name + ".mat");
        if (existing != null) return existing;
        var material = new Material(Shader.Find("Universal Render Pipeline/Lit")) { color = color };
        AssetDatabase.CreateAsset(material, Root + "/Materials/" + name + ".mat");
        return material;
    }
    public static void Validate()
    {
        var scene = EditorSceneManager.OpenScene(ScenePath);
        ValidateScene(scene);
        CombatSession session = null;
        foreach (var root in scene.GetRootGameObjects()) if (root.TryGetComponent<CombatSession>(out var value)) session = value;
        CheckCombat(session);
        Debug.Log("COMBAT_VALIDATED: saved scene and combat checks passed.");
    }
    static void ValidateScene(Scene scene)
    {
        CombatSession session = null;
        foreach (var root in scene.GetRootGameObjects()) if (root.TryGetComponent<CombatSession>(out var value)) session = value;
        if (session == null || session.hero == null || session.orbit == null || session.enemies.Length != 3)
            throw new Exception("Missing combat scene references");
        if (session.hero.cameraTransform != session.orbit.transform || session.orbit.target != session.hero.transform)
            throw new Exception("Invalid camera target");
        foreach (var enemy in session.enemies)
            if (enemy.target != session.hero || enemy.warningRing == null || !PrefabUtility.IsPartOfPrefabInstance(enemy))
                throw new Exception("Invalid enemy references");
    }
    static void AwakeComponent(MonoBehaviour component)
    {
        component.GetType().GetMethod("Awake", BindingFlags.Instance | BindingFlags.NonPublic)?.Invoke(component, null);
    }
    static void CheckCombat(CombatSession session)
    {
        var hero = session.hero;
        AwakeComponent(hero.GetComponent<CombatHealth>());
        AwakeComponent(hero);
        foreach (var enemy in session.enemies) { AwakeComponent(enemy.GetComponent<CombatHealth>()); AwakeComponent(enemy); }
        var first = session.enemies[0];
        // Test a real overlap + facing + line-of-sight hit against the saved scene's colliders.
        first.GetComponent<CharacterController>().enabled = false;
        first.transform.position = hero.transform.position + hero.transform.forward * 1.25f;
        first.GetComponent<CharacterController>().enabled = true;
        Physics.SyncTransforms();
        hero.Attack();
        if (!Mathf.Approximately(first.Health.Current, first.Health.maxHealth - hero.attackDamage)) throw new Exception("Frontal melee test failed");
        hero.Health.Damage(12);
        if (hero.Health.Current != 88) throw new Exception("Hero damage test failed");
        first.Health.Damage(999);
        first.Health.Damage(999);
        if (!first.Health.Dead || first.Health.Current != 0) throw new Exception("Enemy death test failed");
        session.Restart();
        if (hero.Health.Current != 100 || first.Health.Dead) throw new Exception("Restart test failed");
        first.GetComponent<CharacterController>().enabled = false;
        first.transform.position = hero.transform.position - hero.transform.forward * 1.25f;
        first.GetComponent<CharacterController>().enabled = true;
        Physics.SyncTransforms();
        hero.Attack();
        if (first.Health.Current != first.Health.maxHealth) throw new Exception("Rear miss test failed");
        session.Restart();
        // Tests modify only the in-memory scene after saving, never the authored asset.
    }
}

