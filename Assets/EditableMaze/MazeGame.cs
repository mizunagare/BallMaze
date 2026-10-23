using System.Linq;
using UnityEngine;
using UnityEngine.InputSystem;

public class MazeGame : MonoBehaviour
{
    public MazePlayer player;
    MazeKey[] keys;
    int collected;
    float elapsed;
    public bool Won { get; private set; }
    public int TotalKeys => keys == null ? 0 : keys.Length;

    void Start()
    {
        // Count scene instances automatically, including duplicated key prefabs.
        keys = FindObjectsByType<MazeKey>(FindObjectsInactive.Include, FindObjectsSortMode.None)
            .Where(key => key.gameObject.scene == gameObject.scene).ToArray();
    }
    void Update()
    {
        if (Keyboard.current != null && Keyboard.current.rKey.wasPressedThisFrame) Restart();
        if (!Won) elapsed += Time.deltaTime;
    }
    public void Collect() { collected++; }
    public void TryWin()
    {
        if (Won || keys == null || collected != keys.Length) return;
        Won = true;
        player.Stop();
    }
    public void Restart()
    {
        if (keys == null) return;
        Won = false;
        collected = 0;
        elapsed = 0;
        player.ResetPlayer();
        foreach (var key in keys) if (key != null) key.ResetKey();
    }
    void OnGUI()
    {
        CombatChineseUI.Apply();
        Matrix4x4 previous = GUI.matrix;
        float scale = Mathf.Clamp(Screen.height / 720f, .7f, 2f);
        GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1));
        var text = new GUIStyle(GUI.skin.label) { fontSize = 20 };
        GUI.Box(new Rect(16, 16, 410, 140), "");
        GUI.Label(new Rect(30, 25, 380, 35), "小球迷宫", new GUIStyle(text) { fontSize = 26 });
        GUI.Label(new Rect(30, 65, 380, 30), $"钥匙： {collected}/{TotalKeys}    用时： {elapsed:0.0}s", text);
        GUI.Label(new Rect(30, 105, 380, 30), "WASD / 方向键：移动    R：重开", new GUIStyle(text) { fontSize = 17 });
        if (Won) {
            float center = Screen.width / scale / 2;
            GUI.Box(new Rect(center - 200, 200, 400, 145), "");
            GUI.Label(new Rect(center - 175, 220, 350, 35), $"通关成功！ {elapsed:0.0} 秒", text);
            if (GUI.Button(new Rect(center - 90, 280, 180, 40), "再玩一次")) Restart();
        }
        else if (collected == TotalKeys)
            GUI.Label(new Rect(30, 165, 550, 35), "钥匙已集齐！请前往绿色出口。", text);
        GUI.matrix = previous;
    }
}

