using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

// The demo builds its level at runtime, so the original scene stays untouched.
public class BallMazeDemo : MonoBehaviour
{
    const float Cell = 2f;
    readonly string[] map = {
        "###########",
        "#S....#..K#",
        "#.##..#.#.#",
        "#..#....#.#",
        "##.#.####.#",
        "#K.#......#",
        "#..###.##.#",
        "#......#..#",
        "#.####.#K.#",
        "#......#.E#",
        "###########"
    };
    readonly List<Transform> keys = new List<Transform>();
    readonly List<Vector3> keyPositions = new List<Vector3>();
    Rigidbody ball;
    Camera view;
    Vector3 spawn, exit;
    Vector2 input;
    int collected;
    float elapsed;
    bool won;
    Material floorMat, wallMat, ballMat, keyMat, exitMat;

    void Awake()
    {
        floorMat = MakeMaterial(new Color(.12f, .2f, .27f));
        wallMat = MakeMaterial(new Color(.28f, .43f, .52f));
        ballMat = MakeMaterial(new Color(.25f, .85f, 1f));
        keyMat = MakeMaterial(new Color(1f, .73f, .12f));
        exitMat = MakeMaterial(new Color(.25f, .9f, .5f));
        Box("Floor", new Vector3(0, -.5f, 0), new Vector3(22, 1, 22), floorMat);
        for (int z = 0; z < map.Length; z++)
        for (int x = 0; x < map[z].Length; x++)
        {
            Vector3 p = new Vector3((x - 5) * Cell, 0, (5 - z) * Cell);
            char tile = map[z][x];
            if (tile == '#') Box("Wall", p + Vector3.up * .6f, new Vector3(2, 1.2f, 2), wallMat);
            if (tile == 'S') spawn = p + Vector3.up * .6f;
            if (tile == 'E') {
                exit = p;
                Box("Exit", p + Vector3.up * .035f, new Vector3(1.7f, .07f, 1.7f), exitMat);
            }
            if (tile == 'K') {
                GameObject key = GameObject.CreatePrimitive(PrimitiveType.Cube);
                key.name = "Golden key";
                key.transform.position = p + Vector3.up * .8f;
                key.transform.localScale = Vector3.one * .55f;
                key.GetComponent<Collider>().enabled = false;
                key.GetComponent<Renderer>().sharedMaterial = keyMat;
                keys.Add(key.transform);
                keyPositions.Add(key.transform.position);
            }
        }
        GameObject player = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        player.name = "Player";
        player.transform.position = spawn;
        player.GetComponent<Renderer>().sharedMaterial = ballMat;
        ball = player.AddComponent<Rigidbody>();
        ball.mass = 1;
        ball.linearDamping = 2f;
        ball.angularDamping = .5f;
        ball.interpolation = RigidbodyInterpolation.Interpolate;
        ball.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
        GameObject cameraObject = new GameObject("Demo Camera", typeof(Camera), typeof(AudioListener));
        view = cameraObject.GetComponent<Camera>();
        view.tag = "MainCamera";
        view.transform.position = new Vector3(0, 27, -16);
        view.transform.LookAt(Vector3.zero);
        view.orthographic = true;
        view.orthographicSize = 14;
        view.backgroundColor = new Color(.035f, .06f, .09f);
        view.clearFlags = CameraClearFlags.SolidColor;
        GameObject lamp = new GameObject("Sun", typeof(Light));
        lamp.transform.rotation = Quaternion.Euler(50, -30, 0);
        Light light = lamp.GetComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 1.5f;
        RenderSettings.ambientLight = new Color(.6f, .65f, .7f);
    }

    Material MakeMaterial(Color color)
    {
        Shader shader = Shader.Find("Universal Render Pipeline/Lit");
        if (shader == null) shader = Shader.Find("Standard");
        return new Material(shader) { color = color };
    }

    void Box(string label, Vector3 position, Vector3 size, Material material)
    {
        GameObject obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
        obj.name = label;
        obj.transform.position = position;
        obj.transform.localScale = size;
        obj.GetComponent<Renderer>().sharedMaterial = material;
    }

    void Update()
    {
        Keyboard keyboard = Keyboard.current;
        if (keyboard != null && keyboard.rKey.wasPressedThisFrame) Restart();
        input = Vector2.zero;
        if (keyboard != null && !won) {
            input.x = (keyboard.dKey.isPressed || keyboard.rightArrowKey.isPressed ? 1 : 0)
                    - (keyboard.aKey.isPressed || keyboard.leftArrowKey.isPressed ? 1 : 0);
            input.y = (keyboard.wKey.isPressed || keyboard.upArrowKey.isPressed ? 1 : 0)
                    - (keyboard.sKey.isPressed || keyboard.downArrowKey.isPressed ? 1 : 0);
            input = Vector2.ClampMagnitude(input, 1);
        }
        if (won) return;
        elapsed += Time.deltaTime;
        for (int i = 0; i < keys.Count; i++) {
            if (!keys[i].gameObject.activeSelf) continue;
            keys[i].Rotate(30 * Time.deltaTime, 75 * Time.deltaTime, 0);
            if (Vector3.Distance(ball.position, keys[i].position) < 1f) {
                keys[i].gameObject.SetActive(false);
                collected++;
            }
        }
        if (collected == keys.Count && Vector3.Distance(ball.position, exit + Vector3.up * .5f) < .9f) {
            won = true;
            ball.linearVelocity = Vector3.zero;
            ball.angularVelocity = Vector3.zero;
        }
        if (ball.position.y < -3) Restart();
    }

    void FixedUpdate()
    {
        if (!won) ball.AddForce(new Vector3(input.x, 0, input.y) * 16f, ForceMode.Acceleration);
        Vector3 velocity = ball.linearVelocity;
        Vector3 horizontal = Vector3.ClampMagnitude(new Vector3(velocity.x, 0, velocity.z), 5f);
        ball.linearVelocity = new Vector3(horizontal.x, velocity.y, horizontal.z);
    }

    void Restart()
    {
        ball.position = spawn;
        ball.rotation = Quaternion.identity;
        ball.linearVelocity = Vector3.zero;
        ball.angularVelocity = Vector3.zero;
        input = Vector2.zero;
        collected = 0;
        elapsed = 0;
        won = false;
        for (int i = 0; i < keys.Count; i++) {
            keys[i].position = keyPositions[i];
            keys[i].gameObject.SetActive(true);
        }
    }

    void OnGUI()
    {
        CombatChineseUI.Apply();
        float scale = Mathf.Clamp(Screen.height / 720f, .7f, 2f);
        GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1));
        GUIStyle text = new GUIStyle(GUI.skin.label) { fontSize = 20 };
        GUI.Box(new Rect(16, 16, 390, 138), "");
        GUI.Label(new Rect(30, 25, 370, 32), "小球迷宫", new GUIStyle(text) { fontSize = 26 });
        GUI.Label(new Rect(30, 65, 370, 30), $"钥匙： {collected}/{keys.Count}     用时： {elapsed:0.0}s", text);
        GUI.Label(new Rect(30, 99, 370, 30), "WASD / 方向键：移动    R：重开", new GUIStyle(text) { fontSize = 17 });
        if (won) {
            float center = Screen.width / scale / 2;
            GUI.Box(new Rect(center - 200, 200, 400, 145), "");
            GUI.Label(new Rect(center - 175, 220, 350, 40), $"通关成功！  {elapsed:0.0} 秒", text);
            if (GUI.Button(new Rect(center - 90, 280, 180, 40), "再玩一次")) Restart();
        }
        else if (collected == keys.Count)
            GUI.Label(new Rect(30, 162, 500, 35), "钥匙已集齐！请前往绿色出口。", text);
    }

    void OnDestroy()
    {
        Destroy(floorMat); Destroy(wallMat); Destroy(ballMat); Destroy(keyMat); Destroy(exitMat);
    }
}

