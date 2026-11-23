using System;
using System.IO;

public partial class CombatSaveSystem
{
    [NonSerialized] public Action<string> EntryValidationHook;
    FileStream storageLease;
    string storageGeneration;

    bool CheckEntry()
    {
        if (!GameEntry.LaunchRejected && GameEntry.GameSceneAuthorized) return true;
        initialized = false;
        blocked = true;
        Status = GameEntry.LaunchRejected ? GameEntry.Error : "请先从开始界面选择旅途。";
        if (session != null && session.hero != null) session.hero.SaveMenuOpen = true;
        return false;
    }

    bool BindCollection(string directory)
    {
        directory = Path.GetFullPath(directory);
        if (!UnityEngine.Application.isEditor && directory != GameEntry.V10Directory(GameEntry.TestRoot))
            throw new IOException("新版必须使用独立 v10 存档根");
        if (storageLease != null) return folder == directory;
        storageLease = SaveSchemaMigration.Acquire(directory);
        folder = directory;
        storageGeneration = SaveSchemaMigration.Generation(folder);
        return true;
    }

    void AssertGeneration()
    {
        if (storageLease == null || storageGeneration != SaveSchemaMigration.Generation(folder))
            throw new IOException("存档世代已变化，写入暂停");
    }

    public void SuspendEntry()
    {
        initialized = false;
        blocked = true;
        storageLease?.Dispose();
        storageLease = null;
    }

    void OnDestroy() => SuspendEntry();

    public bool InitializeFromEntry(string current, bool create, string fingerprint)
    {
        if (!CheckEntry()) return false;
        try
        {
            if (!BindCollection(current)) throw new IOException("存档根已绑定");
            if (SaveCatalog.Fingerprint(current) != fingerprint)
                throw new IOException("读取前存档发生变化，请返回列表刷新");
            initialized = true;
            blocked = false;
            if (create)
            {
                string noLegacy = current + ".newgame-unused-" + Guid.NewGuid().ToString("N");
                bool done = NewProfileTransaction.Create(current, noLegacy, fingerprint, stage =>
                {
                    folder = stage;
                    primaryValid = false;
                    storageGeneration = SaveSchemaMigration.Generation(folder);
                    session.Camp.Restore(new GearItem[0], new int[6]);
                    session.Camp.RestoreRecipes(new string[0]);
                    session.Flow.StartFresh();
                    return SaveProgress(false);
                }, EntryValidationHook, out string error);
                folder = current;
                if (!done) throw new IOException(error);
            }
            storageGeneration = SaveSchemaMigration.Generation(folder);
            bool ok = LoadProgress(false);
            nextSave = UnityEngine.Time.unscaledTime + autoSaveInterval;
            if (!ok) SuspendEntry();
            return ok;
        }
        catch (Exception e)
        {
            SuspendEntry();
            Status = "档案未打开，原集合保留：" + e.Message;
            return false;
        }
    }
}
