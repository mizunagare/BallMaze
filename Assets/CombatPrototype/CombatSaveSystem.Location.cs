using UnityEngine;

public partial class CombatSaveSystem
{
    bool locationPrompt;
    SaveLocationResult locationResult;

    public void InitializeDefaultStorage()
    {
        try
        {
            string root = GameEntry.TestRoot;
            InitializeLocatedStorage(GameEntry.V9Source(root), GameEntry.V10Directory(root));
        }
        catch (System.Exception e)
        {
            ShowLocationFailure(e.Message);
        }
    }

    public void InitializeLocatedStorage(string legacy, string current)
    {
        // Direct editor validation never migrates. The title's explicit action is the sole import route.
        var existing = SaveCatalog.Inspect(current);
        if (existing.canContinue && existing.version == SaveSchemaMigration.Version ||
            existing.status == SaveAvailability.Missing && !SaveCatalog.Inspect(legacy).canContinue)
        {
            locationPrompt = false;
            InitializeStorage(current, existing.canContinue);
            return;
        }
        ShowLocationFailure("请回到标题的读取存档页面检查现行 v10 集合或明确迁入 v9 原档。");
    }

    void ShowLocationFailure(string message)
    {
        locationResult = new SaveLocationResult { status = SaveLocationStatus.Blocked, message = message };
        locationPrompt = true;
        session.Flow.MigrationFailed(message);
    }

    void DrawLocationPrompt()
    {
        var matrix = CombatUI.Begin();
        int depth = GUI.depth;
        GUI.depth = -220;
        float x = CombatUI.Width/2-510, y = CombatUI.Height/2-230;
        CombatUI.Panel(new Rect(x,y,1020,460));
        CombatUI.Text(new Rect(x+25,y+20,970,45),"万象归途 · 存档定位与恢复",28,CombatUI.Gold,true);
        CombatUI.Text(new Rect(x+25,y+85,970,260),locationResult.message,19);
        if(CombatUI.Button(new Rect(x+25,y+370,285,45),"重新检查（不迁移）")) InitializeDefaultStorage();
        if(CombatUI.Button(new Rect(x+710,y+370,285,45),"退出，保持现状")) Application.Quit();
        GUI.depth=depth;
        GUI.matrix=matrix;
    }
}
