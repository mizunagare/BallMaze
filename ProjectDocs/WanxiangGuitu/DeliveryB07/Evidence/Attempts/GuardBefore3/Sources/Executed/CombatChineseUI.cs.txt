using UnityEngine;

public static class CombatChineseUI
{
    static Font font;
    public static void Apply()
    {
        if (font == null) font = Font.CreateDynamicFontFromOSFont(new[] { "Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS" }, 18);
        if (font != null) GUI.skin.font = font;
    }
}
