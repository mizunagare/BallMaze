using UnityEditor;
using UnityEngine;
public static class DevelopmentQuickLoadMenu {
 [MenuItem("Ball Maze/开发工具/切换 F9 快速读档（仅当前试玩）")]
 static void Toggle(){if(!EditorApplication.isPlaying){Debug.Log("进入试玩后才可显式启用开发读档。");return;}var save=Object.FindFirstObjectByType<CombatSaveSystem>();if(save==null)return;save.enableEditorQuickLoad=!save.enableEditorQuickLoad;Debug.LogWarning(save.enableEditorQuickLoad?"开发 F9 读档已启用：仅本次编辑器试玩，可能回滚进度；正式构建始终禁用。":"开发 F9 读档已关闭。");}
}
