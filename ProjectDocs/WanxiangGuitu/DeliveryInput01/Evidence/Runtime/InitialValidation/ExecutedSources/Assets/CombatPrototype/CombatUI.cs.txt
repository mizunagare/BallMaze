using UnityEngine;

// Shared geometry and colors keep the HUD and management panels consistent.
public static class CombatUI
{
    public static readonly Color Surface = CatUI.Surface;
    public static readonly Color Raised = CatUI.Raised;
    public static readonly Color Ink = CatUI.Ink;
    public static readonly Color Muted = CatUI.Muted;
    public static readonly Color Gold = CatUI.Gold;
    public static readonly Color Health = new Color(.78f, .20f, .23f);
    public static readonly Color Experience = new Color(.13f, .66f, .72f);
    public static float Scale => Mathf.Clamp(Mathf.Min(Screen.width / 1280f, Screen.height / 800f), .4f, 2);
    public static float Width => Screen.width / Scale;
    public static float Height => Screen.height / Scale;
    public static Matrix4x4 Begin()
    {
        CombatChineseUI.Apply();
        Matrix4x4 old = GUI.matrix;
        GUI.matrix = Matrix4x4.Scale(new Vector3(Scale, Scale, 1));
        return old;
    }
    public static void Fill(Rect area, Color color)
    {
        var old = GUI.color;
        GUI.color = color;
        GUI.DrawTexture(area, Texture2D.whiteTexture);
        GUI.color = old;
    }
    public static void Panel(Rect area)
    {
        Fill(area, Surface);
        Fill(new Rect(area.x, area.y, area.width, 1), new Color(.32f, .40f, .45f));
    }
    public static void Text(Rect area, string value, int size = 20, Color? color = null, bool bold = false)
    {
        GUI.Label(area, value, new GUIStyle(GUI.skin.label) {
            fontSize = size, fontStyle = bold ? FontStyle.Bold : FontStyle.Normal,
            normal = { textColor = color ?? Ink }, wordWrap = true
        });
    }
    public static bool Button(Rect area, string label, bool enabled = true, bool selected = false)
    {
        bool oldEnabled = GUI.enabled;
        GUI.enabled = oldEnabled && enabled;
        var style = new GUIStyle(GUI.skin.button) { fontSize = 18, fontStyle = selected ? FontStyle.Bold : FontStyle.Normal };
        style.normal.textColor = selected ? Gold : Ink;
        bool clicked = GUI.Button(area, label, style);
        GUI.enabled = oldEnabled;
        return clicked;
    }
    public static void Bar(Rect area, float fraction, Color fill, string label = null)
    {
        Fill(area, Raised);
        Fill(new Rect(area.x, area.y, area.width * Mathf.Clamp01(fraction), area.height), fill);
        if (label != null) GUI.Label(area, label, new GUIStyle(GUI.skin.label) {
            fontSize = 16, alignment = TextAnchor.MiddleCenter, normal = { textColor = Ink }
        });
    }
}
