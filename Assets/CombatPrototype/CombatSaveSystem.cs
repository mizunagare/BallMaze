using System.Linq;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.SceneManagement;

public class CombatSaveSystem : MonoBehaviour
{
    [Min(1), InspectorName("自动存档间隔（秒）")] public float autoSaveInterval = 5;
    CombatSession session;
    bool initialized, restoring, blocked, primaryValid, newGameDialog;
    float nextSave, dialogTimeScale;
    CursorLockMode dialogCursor;
    bool dialogCursorVisible;
    string folder;
    public bool IsInitialized => initialized;
    public bool CanCommitWarehouse=>CanCapture;
    public bool ConfirmationOpen => newGameDialog;
    public string SavePath => folder == null ? "" : Path.Combine(folder, "save.json");
    public string BackupPath => SavePath + ".bak";
    public bool HasSave => initialized && (File.Exists(SavePath) || File.Exists(BackupPath));
    public string Status { get; private set; } = "正在准备存档…";
    void Awake() { session = GetComponent<CombatSession>(); }
    IEnumerator Start()
    {
        // Automated validation uses an explicit workspace directory, never a player's real save.
        if (Application.isBatchMode || gameObject.scene.name != "ForestRuins") yield break;
        session.hero.SaveMenuOpen = true;
        yield return null; // All actor, wave and random-event Start methods must finish first.
        session.hero.SaveMenuOpen = false;
        InitializeStorage(Path.Combine(Application.persistentDataPath, "ForestRuins"), true);
    }
    public void InitializeStorage(string directory, bool loadExisting)
    {
        folder = Path.GetFullPath(directory); initialized = true;
        nextSave = Time.unscaledTime + Mathf.Max(1, autoSaveInterval);
        if (loadExisting && HasSave) LoadProgress(true);
        else{if(!session.Flow.LegacyHarness)session.Flow.StartFresh();if(!HasSave)SaveProgress(false);}
    }
    [NonSerialized] public bool enableEditorQuickLoad;
    public bool QuickLoadAllowed => Application.isEditor && enableEditorQuickLoad;
    void Update()
    {
        if (!initialized) return;
        var keyboard = Keyboard.current;
        if (newGameDialog) { if (keyboard != null && keyboard.escapeKey.wasPressedThisFrame) CancelNewGame(); return; }
        if (keyboard != null && keyboard.f5Key.wasPressedThisFrame) SaveProgress(true);
        if (QuickLoadAllowed && keyboard != null && keyboard.f9Key.wasPressedThisFrame) { if(session.Flow.Enabled)session.Flow.ResolveTerminal();LoadProgress(true); }
    }
    void LateUpdate()
    {
        if (!initialized || restoring || newGameDialog || blocked || Time.unscaledTime < nextSave) return;
        SaveProgress(false);
    }
    bool CanCapture => initialized && !restoring && !blocked && !newGameDialog
        && !(session.Flow.Enabled&&!session.Flow.HasResult&&!string.IsNullOrEmpty(session.Flow.Error)) && session != null && session.hero != null
        && session.hero.Health != null && (!session.hero.Health.Dead || session.Flow.Enabled&&session.Flow.HasResult) && session.hero.Inventory != null && session.hero.Progression != null
        && session.Waves != null && session.Events != null && session.enemies != null && session.enemies.Length > 0;
    public bool SaveProgress(bool notify = true)
    {
        if (!CanCapture) {
            if (notify) Notice(blocked ? "存档异常，已停止覆盖；请恢复有效存档后重试。" : "当前无法保存；结局未提交时请在结算页重试。" , true);
            return false;
        }
        nextSave = Time.unscaledTime + Mathf.Max(1, autoSaveInterval);
        try {
            var live = CaptureLegacy(); var data=session.Flow.Enabled?session.Flow.Compose(live):live; if(session.Flow.Enabled)AdventureValidation.Validate(data);else Validate(data,6);
            // Page a detached snapshot: publishing must never mutate the live run or settlement.
            var disk = AdventureData.Clone(data);
            if(session.Flow.Enabled)GroundLootStore.Pack(disk, folder);
            string payload = JsonUtility.ToJson(disk);
            var envelope = new CombatSaveEnvelope { version=session.Flow.Enabled?9:6,revision=data.revision,savedAtUtc = DateTime.UtcNow.ToString("o"), payload = payload, checksum = Checksum(payload) };
            string json = JsonUtility.ToJson(envelope, true);
            Directory.CreateDirectory(folder);
            string temporary = SavePath + ".tmp";
            byte[] bytes = new UTF8Encoding(false).GetBytes(json);
            if(bytes.Length>8*1024*1024)throw new IOException("主存档元数据超过读取预算，原档保留；地面掉落分页未被删除。 ");
            using (var file = new FileStream(temporary, FileMode.Create, FileAccess.Write, FileShare.None)) { file.Write(bytes, 0, bytes.Length); file.Flush(true); }
            if (File.Exists(SavePath)) File.Replace(temporary, SavePath, primaryValid ? BackupPath : null);
            else File.Move(temporary, SavePath);
            primaryValid = true; if(session.Flow.Enabled)session.Flow.Published(data.revision);
            Status = "进度已保存";
            if (notify) Notice("进度已保存；下次进入会自动继续。", false);
            return true;
        }
        catch (Exception e) { Status = "保存失败，已有存档保留"; Debug.LogWarning("存档写入失败：" + e); if (notify) Notice(Status, true); return false; }
    }
    internal CombatSaveData CaptureLegacy()
    {
        // Settle rewards before recording dead actors, preventing duplicated XP/Boss rewards.
        foreach (var enemy in session.enemies) if (enemy.Health.Dead) enemy.DropLootOnce();
        var hero = session.hero; var bag = hero.Inventory; var gear = hero.Equipment; var progression = hero.Progression;
        var data = new CombatSaveData {
            unlockedRecipes=session.Camp.CaptureRecipes(),
            warehouseGear=session.Camp.Items.Select(i=>i.Clone()).ToArray(), warehouseMaterials=(int[])session.Camp.Materials.Clone(),
            wave = session.Wave, level = progression.Level, experience = progression.Experience,
            skills = progression.CaptureRanks(), offers = progression.CaptureOffers(), rewards = progression.CaptureRewards(),
            materials = System.Enum.GetValues(typeof(MaterialKind)).Cast<MaterialKind>().Select(bag.Count).ToArray(),
            gear = hero.GetComponent<AdventureLoadout>().items.ToArray(), mainWeapon = hero.GetComponent<AdventureLoadout>().mainWeapon, reserveWeapon=hero.GetComponent<AdventureLoadout>().reserveWeapon, weaponAttackCooldown=hero.GetComponent<AdventureCombat>().AttackRemaining,weaponSwitchCooldown=hero.GetComponent<AdventureCombat>().SwitchRemaining,
            weaponSkillCooldown = hero.GetComponent<AdventureCombat>().SkillRemaining,
            resources = FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(n=>n.gameObject.scene==gameObject.scene).Select(n=>new SavedResource{id=n.nodeId,entityId=n.StableId,health=n.Health}).ToArray(),
            potions = bag.HealthPotionCount, potionAssigned = bag.PotionOnQuickbar, potionCooldown = bag.PotionCooldownRemaining,
            swordTier = gear.SwordTier, armorTier = gear.ArmorTier, swordEquipped = gear.SwordEquipped, armorEquipped = gear.ArmorEquipped,
            health = hero.Health.Current, heroPosition = session.Camp.InCamp?session.Camp.ReturnPosition:hero.transform.position, heroYaw = session.Camp.InCamp?session.Camp.ReturnYaw:hero.transform.eulerAngles.y,
            cameraYaw = session.Camp.InCamp?session.Camp.ReturnCameraYaw:session.orbit.ViewYaw, cameraPitch = session.Camp.InCamp?session.Camp.ReturnCameraPitch:session.orbit.ViewPitch, dodgeCooldown = hero.Dodge.CooldownRemaining,
            waitingForWave = session.WaitingForNextWave, waveRemaining = session.NextWaveRemaining,
            entitySchema=1,forestWorld=GetComponent<ForestRegionRuntime>()?.Active==true,forest=GetComponent<ForestRegionRuntime>()?.Capture(),
            enemies = new SavedEnemy[session.enemies.Length], events = new SavedWorldEvent[session.Events.Points.Count]
        };
        for (int i = 0; i < data.enemies.Length; i++) {
            var enemy = session.enemies[i];
            data.enemies[i] = new SavedEnemy { entityId=enemy.entityId,aiState=enemy.GetComponent<EncounterGuard>()?.State??0,position = enemy.transform.position, yaw = enemy.transform.eulerAngles.y, health = enemy.Health.Current };
        }
        for (int i = 0; i < data.events.Length; i++) {
            var point = session.Events.Points[i];
            data.events[i] = new SavedWorldEvent { entityId=point.entityId,kind = point.Kind, position = point.transform.position, used = point.Used };
        }
        var loot = new List<SavedLoot>();
        foreach (var item in FindObjectsByType<LootPickup>(FindObjectsSortMode.None))
            if (!item.Collected && item.gameObject.scene == gameObject.scene && item.gameObject.activeSelf)
                loot.Add(new SavedLoot { equipment = item.Gear != null, gear = item.Gear, kind = item.Kind, amount = item.Amount, position = item.SavePosition });
        data.loot = loot.ToArray(); data.randomStateJson=JsonUtility.ToJson(UnityEngine.Random.state);return data;
    }
    public bool LoadProgress(bool notify = true)
    {
        if (!initialized || restoring || newGameDialog) return false;
        CombatSaveData data = null; bool recovered = false;
        try {
            if (File.Exists(SavePath)) { data = Read(SavePath); primaryValid = true; }
        } catch (Exception e) {
            primaryValid = false; Debug.LogWarning("主存档无法读取：" + e.Message);
            if (e is NotSupportedException) { blocked = true; BlockRecovery("存档版本或必要定义不兼容，已保留文件并停止覆盖。请补回定义或恢复有效存档后重试："+e.Message); return false; }
        }
        if (data == null && File.Exists(BackupPath)) {
            try { data = Read(BackupPath); recovered = true; } catch (Exception e) { Debug.LogWarning("备份存档无法读取：" + e.Message); }
        }
        if (data == null) {
            blocked = HasSave;
            if(blocked)BlockRecovery("存档及备份无法读取，已保留文件并暂停游戏。请恢复完整有效存档后点击重试。");else if(notify)Notice("还没有存档，按 F5 保存当前进度。",true);
            return false;
        }
        try {
            if(data.sourceVersion>=7){restoring=true;if(data.sourceVersion==7)AdventureMigration.UpgradeV7(data);session.Flow.Restore(data);blocked=false;Status=recovered?"从完整备份恢复冒险 / 结算":"已恢复完整检查点 / 营地";restoring=false;if(data.sourceVersion<9&&!SaveProgress(false)){blocked=true;session.Flow.MigrationFailed("v9 迁移保存失败，原档已备份，请修复存储后重试。");return false;}return true;}
            string migrationArchive=Path.Combine(folder,"save-v"+data.sourceVersion+"-before-adventure-v7.json");if(!File.Exists(migrationArchive))File.Copy(recovered?BackupPath:SavePath,migrationArchive,false);
            if(data.sourceVersion<4){string origin=recovered?BackupPath:SavePath;string archive=Path.Combine(folder,"save-v"+data.sourceVersion+"-before-containers.json");if(!File.Exists(archive))File.Copy(origin,archive,false);}
            if(data.sourceVersion==4){string origin=recovered?BackupPath:SavePath;string archive=Path.Combine(folder,"save-v4-before-camp.json");if(!File.Exists(archive))File.Copy(origin,archive,false);}
            if(data.sourceVersion==5){string origin=recovered?BackupPath:SavePath;string archive=Path.Combine(folder,"save-v5-before-workbench.json");if(!File.Exists(archive))File.Copy(origin,archive,false);}
            restoring = true; session.Flow.BeginLegacyRestore();
            session.Restart();
            session.Camp.Restore(data.sourceVersion>=5?data.warehouseGear:null,data.sourceVersion>=5?data.warehouseMaterials:null);
            var hero = session.hero;
            hero.Progression.RestoreProgress(data.level, data.experience, data.skills, data.rewards, data.offers);
            hero.Inventory.RestoreInventory(data.materials, data.potions, data.potionAssigned, data.potionCooldown);
            hero.Equipment.RestoreEquipment(data.swordTier, data.armorTier, data.swordEquipped, data.armorEquipped);
            if(data.gear != null) hero.GetComponent<AdventureLoadout>().Restore(data.gear, data.mainWeapon); else hero.GetComponent<AdventureLoadout>().Migrate(data.swordTier,data.armorTier,data.swordEquipped,data.armorEquipped);
            if(data.sourceVersion>=6)session.Camp.RestoreRecipes(data.unlockedRecipes);else session.Camp.MigrateRecipes(hero.GetComponent<AdventureLoadout>().items.Concat(session.Camp.Items));
            hero.GetComponent<AdventureLoadout>().RestoreReserve(data.reserveWeapon);
            hero.GetComponent<AdventureCombat>().RestoreCooldown(data.weaponSkillCooldown,data.weaponAttackCooldown,data.weaponSwitchCooldown);
            if(data.resources!=null) foreach(var state in data.resources){var node=FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).FirstOrDefault(n=>(string.IsNullOrEmpty(state.entityId)?n.nodeId==state.id:n.StableId==state.entityId)&&n.gameObject.scene==gameObject.scene);if(node!=null)node.Restore(state.health);}
            session.RestoreWave(data.wave);
            for (int i = 0; i < data.enemies.Length; i++) session.enemies[i].RestoreState(data.enemies[i]);
            session.Events.RestoreEvents(data.events);
            foreach (var item in data.loot) {
                var instance = item.equipment ? LootPickup.SpawnGear(item.gear,item.position) : LootPickup.Spawn(item.kind, item.amount, item.position);
                SceneManager.MoveGameObjectToScene(instance.gameObject, gameObject.scene);
            }
            hero.RestorePosition(data.heroPosition, data.heroYaw); hero.Health.RestoreHealth(data.health);
            hero.GetComponent<AdventureLoadout>().RestoreReserve(data.reserveWeapon);
            hero.GetComponent<AdventureCombat>().RestoreCooldown(data.weaponSkillCooldown,data.weaponAttackCooldown,data.weaponSwitchCooldown); hero.Dodge.RestoreCooldown(data.dodgeCooldown); session.orbit.RestoreView(data.cameraYaw, data.cameraPitch);
            session.RestoreCountdown(data.waitingForWave, data.waveRemaining);
            Physics.SyncTransforms();
            blocked = false; nextSave = Time.unscaledTime + Mathf.Max(1, autoSaveInterval);
            Status = recovered ? "已从备份恢复进度" : "已继续上次进度";
            if (notify) Notice(Status + $" · 第 {data.wave} 波", false);
            if(!session.Flow.LegacyHarness){session.Flow.AdoptLegacy(data);restoring=false;if(!SaveProgress(false)){blocked=true;session.Flow.MigrationFailed("迁移保存失败，原文件已保留，请修复存储后重试读取。");return false;}}
            if (hero.Progression.PendingChoices > 0) hero.Progression.BeginChoice();
            return true;
        }
        catch (Exception e) { blocked = true; Debug.LogWarning("存档恢复失败：" + e.Message); BlockRecovery("恢复失败，存档文件已保留。暂停游戏与自动覆盖，可修复后重试读取："+e.Message); return false; }
        finally { restoring = false; }
    }

    internal void RestoreWorld(CombatCheckpoint data)
    {
        session.Restart();var hero=session.hero;
        hero.Progression.RestoreProgress(data.level,data.experience,data.skills,data.rewards,data.offers);
        hero.Inventory.RestoreInventory(data.materials,data.potions,data.potionAssigned,data.potionCooldown);
        hero.Equipment.RestoreEquipment(data.swordTier,data.armorTier,data.swordEquipped,data.armorEquipped);
        hero.GetComponent<AdventureLoadout>().Restore(data.gear,data.mainWeapon);hero.GetComponent<AdventureLoadout>().RestoreReserve(data.reserveWeapon);
        if(data.forestWorld){var region=GetComponent<ForestRegionRuntime>()??gameObject.AddComponent<ForestRegionRuntime>();region.Build(data.forest);}else session.RestoreWave(data.wave);
        if(data.resources!=null)foreach(var state in data.resources){var node=FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).FirstOrDefault(n=>(string.IsNullOrEmpty(state.entityId)?n.nodeId==state.id:n.StableId==state.entityId)&&n.gameObject.scene==gameObject.scene);if(node!=null)node.Restore(state.health);}
        for(int i=0;i<data.enemies.Length;i++){var state=data.enemies[i];string id=string.IsNullOrEmpty(state.entityId)?"wave:"+data.wave+":enemy:"+i:state.entityId;var enemy=session.enemies.Single(e=>e.entityId==id);enemy.RestoreState(state);enemy.GetComponent<EncounterGuard>()?.Restore(state.aiState);}session.Events.RestoreEvents(data.events);
        foreach(var item in data.loot){var instance=item.equipment?LootPickup.SpawnGear(item.gear,item.position):LootPickup.Spawn(item.kind,item.amount,item.position);SceneManager.MoveGameObjectToScene(instance.gameObject,gameObject.scene);}
        hero.RestorePosition(data.heroPosition,data.heroYaw);hero.Health.RestoreHealth(data.health);hero.GetComponent<AdventureCombat>().RestoreCooldown(data.weaponSkillCooldown,data.weaponAttackCooldown,data.weaponSwitchCooldown);hero.Dodge.RestoreCooldown(data.dodgeCooldown);session.orbit.RestoreView(data.cameraYaw,data.cameraPitch);session.RestoreCountdown(data.waitingForWave,data.waveRemaining);
        if(!string.IsNullOrEmpty(data.randomStateJson))UnityEngine.Random.state=JsonUtility.FromJson<UnityEngine.Random.State>(data.randomStateJson);Physics.SyncTransforms();
    }
    static string Checksum(string value)
    {
        using (var sha = SHA256.Create()) return BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(value))).Replace("-", "");
    }
    static CombatSaveData Read(string path)
    {
        if (new FileInfo(path).Length > 8 * 1024 * 1024) throw new InvalidDataException("存档过大");
        var envelope = JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(path, Encoding.UTF8));
        if (envelope == null || envelope.version <= 0) throw new InvalidDataException("存档内容不完整");
        if (envelope.version != 1 && envelope.version != 2 && envelope.version != 3 && envelope.version != 4 && envelope.version != 5 && envelope.version != 6 && envelope.version != 7 && envelope.version != 8 && envelope.version != 9) throw new NotSupportedException("未知存档版本");
        if (string.IsNullOrEmpty(envelope.payload) || string.IsNullOrEmpty(envelope.checksum) || envelope.checksum != Checksum(envelope.payload)) throw new InvalidDataException("存档校验未通过");
        var data = JsonUtility.FromJson<CombatSaveData>(envelope.payload);
        if(envelope.version>=9)GroundLootStore.Unpack(data,Path.GetDirectoryName(path));
        if(envelope.version==8){string archive8=Path.Combine(Path.GetDirectoryName(path),"save-v8-before-v9.json");if(!File.Exists(archive8))File.Copy(path,archive8,false);}
        if(envelope.version>=7){if(envelope.version<9)NormalizeStableIds(data.activeRun?.checkpoint);Require(envelope.revision==data.revision);AdventureValidation.Validate(data,envelope.version>=8);if(envelope.version==7){string archive7=Path.Combine(Path.GetDirectoryName(path),"save-v7-before-pve-v8.json");if(!File.Exists(archive7))File.Copy(path,archive7,false);}data.sourceVersion=envelope.version;return data;}
        string archive=Path.Combine(Path.GetDirectoryName(path),"save-v"+envelope.version+"-before-pve-v8.json");if(!File.Exists(archive))File.Copy(path,archive,false);
        AdventureMigration.Normalize(data,envelope.version);
        if(envelope.version >= 2) Require(data != null && data.gear != null && data.resources != null && data.materials != null && data.materials.Length == 6); Validate(data,envelope.version); data.sourceVersion=envelope.version; return data;
    }
    static void Require(bool value) { if (!value) throw new InvalidDataException("存档字段不完整或超出范围"); }
    static bool Finite(float value) => !float.IsNaN(value) && !float.IsInfinity(value);
    static bool Position(Vector3 p) => Finite(p.x) && Finite(p.y) && Finite(p.z) && Mathf.Abs(p.x) <= 51 && Mathf.Abs(p.z) <= 51 && p.y >= -2 && p.y <= 8;
    static void NormalizeStableIds(CombatCheckpoint c){if(c==null)return;c.entitySchema=1;if(c.enemies!=null)for(int i=0;i<c.enemies.Length;i++)if(string.IsNullOrEmpty(c.enemies[i].entityId))c.enemies[i].entityId="wave:"+c.wave+":enemy:"+i;if(c.resources!=null)foreach(var n in c.resources)if(string.IsNullOrEmpty(n.entityId))n.entityId="resource:"+n.id;if(c.events!=null)for(int i=0;i<c.events.Length;i++)if(string.IsNullOrEmpty(c.events[i].entityId))c.events[i].entityId="event:"+i;}
    static bool WorldPosition(CombatCheckpoint c,Vector3 p)=>!c.forestWorld?Position(p):Finite(p.x)&&Finite(p.y)&&Finite(p.z)&&c.forest.WorldBounds.Contains(p);
    internal static void Validate(CombatCheckpoint data,int version=6)
    {
        if(data!=null&&data.forestWorld)data.forest.Validate();
        Require(data != null && data.game == "ForestRuins" && data.wave >= 1 && data.wave <= 100000);
        Require(data.level >= 1 && data.level <= 1000000 && data.experience >= 0 && data.experience <= 100000000);
        Require(data.skills != null && data.skills.Length == 6 && data.materials != null && (data.materials.Length == 3 || data.materials.Length == 6));
        foreach (int rank in data.skills) Require(rank >= 0 && rank <= 1000000);
        foreach (int amount in data.materials) Require(amount >= 0 && amount <= 100000000);
        Require(data.rewards != null && data.rewards.Length <= 10000 && data.offers != null && (data.offers.Length == 0 || data.offers.Length == 3));
        foreach (string reward in data.rewards) Require(reward == "升级奖励" || reward == "祭坛赐福");
        if (data.offers.Length == 3) { Require(data.rewards.Length > 0); Require(data.offers[0] != data.offers[1] && data.offers[1] != data.offers[2] && data.offers[0] != data.offers[2]); }
        foreach (int skill in data.offers) Require(skill >= 0 && skill < 6);
        Require(data.swordTier >= 0 && data.swordTier <= 1000000 && data.armorTier >= 0 && data.armorTier <= 1000000);
        Require((!data.swordEquipped || data.swordTier > 0) && (!data.armorEquipped || data.armorTier > 0));
        Require(data.potions >= 0 && data.potions <= PlayerInventory.MaximumPotions && Finite(data.health) && data.health > 0 && data.health <= 100000000);
        Require(WorldPosition(data,data.heroPosition) && Finite(data.heroYaw) && Finite(data.cameraYaw) && Finite(data.cameraPitch));
        Require(Finite(data.potionCooldown) && data.potionCooldown >= 0 && data.potionCooldown <= 3600 && Finite(data.dodgeCooldown) && data.dodgeCooldown >= 0 && data.dodgeCooldown <= 3600);
        Require(data.enemies != null && (data.forestWorld?data.enemies.Length==data.forest.encounters.Length:data.enemies.Length == CombatWaveDirector.CountForWave(data.wave)));
        var stableIds=data.enemies.Select(e=>e?.entityId).Where(id=>!string.IsNullOrEmpty(id)).ToArray();Require(stableIds.Distinct().Count()==stableIds.Length);if(data.entitySchema>=1)Require(stableIds.Length==data.enemies.Length&&data.events.All(e=>e!=null&&!string.IsNullOrEmpty(e.entityId))&&data.events.Select(e=>e.entityId).Distinct().Count()==data.events.Length&&data.resources.All(n=>n!=null&&!string.IsNullOrEmpty(n.entityId))&&data.resources.Select(n=>n.entityId).Distinct().Count()==data.resources.Length);if(data.forestWorld)Require(stableIds.Length==data.enemies.Length&&data.forest.encounters.All(e=>stableIds.Contains(e.id)));
        bool allDead = true;
        foreach (var enemy in data.enemies) { Require(enemy != null && WorldPosition(data,enemy.position) && Finite(enemy.yaw) && Finite(enemy.health) && enemy.health >= 0 && enemy.health <= 1000000000); if (enemy.health > 0) allDead = false; }
        Require(!data.waitingForWave || allDead);
        Require(Finite(data.waveRemaining) && data.waveRemaining >= 0 && data.waveRemaining <= 86400);
        Require(data.events != null && (data.forestWorld||data.events.Length <= 4) && data.loot != null);
        if(data.forestWorld){Require(data.events.All(e=>e!=null&&!string.IsNullOrEmpty(e.entityId))&&data.events.Select(e=>e.entityId).Distinct().Count()==data.events.Length);Require(data.resources!=null&&data.resources.Length==data.forest.nodes.Length&&data.resources.Select(n=>n.entityId).Distinct().Count()==data.resources.Length&&data.forest.nodes.All(n=>data.resources.Any(r=>r.entityId==n.id)));}
        foreach (var point in data.events) Require(point != null && WorldPosition(data,point.position) && (int)point.kind >= 0 && (int)point.kind <= 1);
        foreach (var loot in data.loot) Require(loot != null && WorldPosition(data,loot.position) && loot.amount > 0 && loot.amount <= 100000000 && (int)loot.kind >= 0 && (int)loot.kind <= 5);
        if(version>=3)ValidateContainers(data);else ValidateAdventure(data);
        if(version>=5)ValidateWarehouse(data);
        if(version>=6){
            Require(data.unlockedRecipes!=null&&data.unlockedRecipes.Length<=1024&&data.unlockedRecipes.Distinct().Count()==data.unlockedRecipes.Length);
            foreach(string id in data.unlockedRecipes){var r=AdventureRecipes.Find(id);if(r==null)throw new NotSupportedException("缺少配方定义："+id);Require(string.IsNullOrEmpty(r.prerequisiteId)||data.unlockedRecipes.Contains(r.prerequisiteId));}
        }
        if(version>=4){Require(Finite(data.weaponAttackCooldown)&&data.weaponAttackCooldown>=0&&data.weaponAttackCooldown<=3600&&Finite(data.weaponSwitchCooldown)&&data.weaponSwitchCooldown>=0&&data.weaponSwitchCooldown<=3600);Require(string.IsNullOrEmpty(data.reserveWeapon)||(data.reserveWeapon!=data.mainWeapon&&data.gear.Any(i=>i.id==data.reserveWeapon&&i.Weapon&&i.InBag)));}
    }
    static void ValidateWarehouse(CombatCheckpoint data)
    {
        Require(data.warehouseGear!=null&&data.warehouseGear.Length<=CampRuntime.Capacity&&data.warehouseMaterials!=null&&data.warehouseMaterials.Length==6);
        foreach(int amount in data.warehouseMaterials)Require(amount>=0&&amount<=CampRuntime.MaterialLimit);
        var ids=new HashSet<string>(data.gear.Select(i=>i.id));foreach(var loot in data.loot)if(loot.equipment)Require(ids.Add(loot.gear.id));
        foreach(var item in data.warehouseGear){ValidateCurrentItem(item);Require(!item.board&&!item.worn&&!item.overflow&&item.x==-1&&item.y==-1&&ids.Add(item.id));}
    }
    static void ValidateGear(GearItem item)
    {
        Require(item!=null && !string.IsNullOrEmpty(item.id) && item.id.Length<=64 && (int)item.type>=0 && (int)item.type<9 && (int)item.quality>=0 && (int)item.quality<5 && item.legacyTier>=0 && item.legacyTier<=1000000);
    }
    static void ValidateAdventure(CombatCheckpoint data)
    {
        Require(Finite(data.weaponSkillCooldown)&&data.weaponSkillCooldown>=0&&data.weaponSkillCooldown<=3600);
        if(data.gear==null)return; // Version-one equipment is migrated after validation.
        Require(data.gear.Length<=AdventureItems.BagWidth*AdventureItems.BagHeight+AdventureItems.BoardWidth*AdventureItems.BoardHeight);
        var ids=new HashSet<string>();
        var cells=new HashSet<string>();
        foreach(var item in data.gear){
            ValidateGear(item);Require(ids.Add(item.id));
            int w=item.board?AdventureItems.BoardWidth:AdventureItems.BagWidth,h=item.board?AdventureItems.BoardHeight:AdventureItems.BagHeight;
            Require(item.x>=0&&item.y>=0&&item.x+item.Size.x<=w&&item.y+item.Size.y<=h);
            for(int y=item.y;y<item.y+item.Size.y;y++)for(int x=item.x;x<item.x+item.Size.x;x++)Require(cells.Add(item.board+":"+x+":"+y));
        }
        Require(string.IsNullOrEmpty(data.mainWeapon)||data.gear.Any(i=>i.id==data.mainWeapon&&i.Weapon&&!i.board));
        foreach(var loot in data.loot)if(loot.equipment){ValidateGear(loot.gear);Require(ids.Add(loot.gear.id));}
        Require(data.resources!=null&&(data.forestWorld||data.resources.Length<=256));var nodes=new HashSet<int>();
        foreach(var node in data.resources)Require(node!=null&&nodes.Add(node.id)&&node.id>=0&&Finite(node.health)&&node.health>=0&&node.health<=10000);
    }    internal static void ValidateCurrentItem(GearItem item)
    {
        Require(item!=null&&!string.IsNullOrEmpty(item.id)&&item.id.Length<=64&&(int)item.type>=0&&(int)item.type<=10&&(int)item.quality>=0&&(int)item.quality<5&&item.dataRevision==1&&item.rotation>=0&&item.rotation<4);
        Require(item.legacyTier>=0&&item.legacyTier<=1000000&&Finite(item.savedAttack)&&item.savedAttack>=0&&item.savedAttack<=1000000000&&Finite(item.savedDefense)&&item.savedDefense>=0&&item.savedDefense<=1000000000);
        Require(item.affixes==null||item.affixes.Length==0||(item.Weapon&&item.affixes.Length<=2&&item.affixes.Distinct().Count()==item.affixes.Length&&item.affixes.All(a=>a>=0&&a<WeaponTraits.Names.Length)));
        var definition=AdventureCatalog.Item(item.definitionId);
        if(definition==null)throw new NotSupportedException("缺少物品定义："+item.definitionId);
        Require((definition.canRotate||item.rotation==0)&&(definition.category==ItemCategory.Equipment||definition.category==ItemCategory.Container)&&definition.type==item.type&&(!item.worn||item.Container)&&!(item.worn&&item.overflow));
        Require(item.widthOverride>=0&&item.widthOverride<=12&&item.heightOverride>=0&&item.heightOverride<=12&&((item.widthOverride==0)==(item.heightOverride==0)));
        if(item.Container){var container=AdventureCatalog.Container(item.definitionId);if(container==null)throw new NotSupportedException("缺少容器模板");Require(container.type==item.type&&container.quality==item.quality&&item.savedAttack==0&&item.savedDefense==0&&!item.board);}
        Require(!item.worn||(!item.board&&item.x==-1&&item.y==-1));
        Require(!item.overflow||(item.x==-1&&item.y==-1));
    }
    internal static void ValidateContainers(CombatCheckpoint data)
    {
        Require(Finite(data.weaponSkillCooldown)&&data.weaponSkillCooldown>=0&&data.weaponSkillCooldown<=3600&&data.gear!=null&&data.gear.Length>=2&&data.gear.Length<=1024);
        var ids=new HashSet<string>();var cells=new HashSet<string>();
        foreach(var item in data.gear){ValidateCurrentItem(item);Require(ids.Add(item.id));}
        var rigs=data.gear.Where(i=>i.worn&&i.type==GearType.ChestRig).ToArray();var bags=data.gear.Where(i=>i.worn&&i.type==GearType.Backpack).ToArray();Require(rigs.Length==1&&bags.Length==1);
        var rig=AdventureCatalog.Container(rigs[0].definitionId);var bag=AdventureCatalog.Container(bags[0].definitionId);
        foreach(var item in data.gear){
            if(item.worn||item.overflow)continue;var container=item.board?rig:bag;
            Require(item.x>=0&&item.y>=0);
            foreach(var p in item.Cells(item.rotation)){int x=p.x+item.x,y=p.y+item.y;Require(container.Allows(x,y)&&cells.Add(item.board+":"+x+":"+y));}
        }
        Require(string.IsNullOrEmpty(data.mainWeapon)||data.gear.Any(i=>i.id==data.mainWeapon&&i.Weapon&&i.InBag));
        foreach(var loot in data.loot)if(loot.equipment){ValidateCurrentItem(loot.gear);Require(!loot.gear.worn&&!loot.gear.overflow&&!loot.gear.board&&ids.Add(loot.gear.id));}
        Require(data.resources!=null&&(data.forestWorld||data.resources.Length<=256));var nodes=new HashSet<int>();
        foreach(var node in data.resources)Require(node!=null&&nodes.Add(node.id)&&node.id>=0&&Finite(node.health)&&node.health>=0&&node.health<=10000);
    }    void Notice(string message, bool error) { Status = message; if (session != null && session.hero != null && session.hero.Inventory != null) session.hero.Inventory.NotifyMessage(message); }
    void BlockRecovery(string message){Notice(message,true);if(!session.Flow.LegacyHarness)session.Flow.MigrationFailed(message);}
    public void RequestNewGame()
    {
        if(session.Flow.Enabled){if(session.Flow.AtCamp)session.Flow.OpenPreparation();else session.Flow.OpenAbandon();return;}
        if (!initialized || newGameDialog) return;
        newGameDialog = true; dialogTimeScale = Time.timeScale; dialogCursor = Cursor.lockState; dialogCursorVisible = Cursor.visible;
        session.hero.SaveMenuOpen = true; Time.timeScale = 0; Cursor.lockState = CursorLockMode.None; Cursor.visible = true;
    }
    public void CancelNewGame()
    {
        if (!newGameDialog) return;
        newGameDialog = false; session.hero.SaveMenuOpen = false; Time.timeScale = dialogTimeScale; Cursor.lockState = dialogCursor; Cursor.visible = dialogCursorVisible;
    }
    public bool ConfirmNewGame()
    {
        if(session.Flow.Enabled)return session.Flow.ConfirmAbandon();
        if (!newGameDialog) return false;
        if(blocked){Notice("存档异常，无法确认永久仓库内容；请先恢复有效存档。",true);return false;}
        try {
            string previous = File.Exists(SavePath) ? SavePath : File.Exists(BackupPath) ? BackupPath : null;
            if (previous != null) File.Copy(previous, Path.Combine(folder, "previous-run.json"), true);
            CancelNewGame(); blocked = false; session.Restart(); return SaveProgress(true);
        } catch (Exception e) { Notice("无法备份旧进度，未开始新游戏：" + e.Message, true); return false; }
    }
    void OnGUI()
    {
        if (!newGameDialog) return;
        int depth = GUI.depth; GUI.depth = -200; var matrix = CombatUI.Begin();
        float width = CombatUI.Width, height = CombatUI.Height;
        CombatUI.Fill(new Rect(0, 0, width, height), new Color(0, 0, 0, .75f));
        float x = width / 2 - 290, y = height / 2 - 120;
        CombatUI.Panel(new Rect(x, y, 580, 240));
        CombatUI.Text(new Rect(x + 28, y + 22, 530, 40), "重新开局？", 28, CombatUI.Gold, true);
        CombatUI.Text(new Rect(x + 28, y + 78, 520, 68), "将从第 1 波、等级 1 开始，随身材料与装备归零，永久仓库与配方保留。\n旧存档会保留一份备份，再保存新进度。", 19);
        if (CombatUI.Button(new Rect(x + 28, y + 170, 240, 42), "取消，继续当前游戏")) CancelNewGame();
        if (CombatUI.Button(new Rect(x + 302, y + 170, 250, 42), "确认重新开局")) ConfirmNewGame();
        GUI.matrix = matrix; GUI.depth = depth;
    }
    void OnApplicationPause(bool paused) { if (paused && initialized) SaveProgress(false); }
    void OnApplicationFocus(bool focused) { if (!focused && initialized) SaveProgress(false); }
    public void SaveBeforeExit() { if (initialized) { if(session.Flow.Enabled)session.Flow.ResolveTerminal(); if (newGameDialog) CancelNewGame(); SaveProgress(false); } }
    void OnApplicationQuit() { SaveBeforeExit(); }
}
