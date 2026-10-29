using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public enum BasicSkill { Strength, IronSkin, Vitality, Speed, Frenzy, Reach }

public class HeroProgression : MonoBehaviour
{
    [InspectorName("经验曲线起点基础值")] public int firstLevelExperience = 20;
    [InspectorName("经验曲线线性增长基础值")] public int experienceGrowth = 10;
    public int Level { get; private set; } = 1;
    public int Experience { get; private set; }
    public int RequiredExperience => ProgressionCurve.Required(Level,firstLevelExperience,experienceGrowth);
    public int PendingChoices { get; private set; }
    public bool IsChoosing { get; private set; }
    public int ClosedFrame { get; private set; } = -1;
    public IReadOnlyList<BasicSkill> Offers => offers;
    readonly List<BasicSkill> offers = new List<BasicSkill>();
    readonly Queue<string> rewardSources = new Queue<string>();
    readonly int[] ranks = new int[6];
    ThirdPersonHero hero;
    float initialMaxHealth, previousTimeScale = 1, noticeUntil;
    int lastExperience;
    bool restoredOffers;
    public int[] CaptureRanks() => (int[])ranks.Clone();
    public string[] CaptureRewards() => rewardSources.ToArray();
    public int[] CaptureOffers() { var result = new int[offers.Count]; for (int i = 0; i < result.Length; i++) result[i] = (int)offers[i]; return result; }
    public void RestoreProgress(int level, int experience, int[] savedRanks, string[] rewards, int[] savedOffers)
    {
        Clear(); Level = level; Experience = experience;
        System.Array.Copy(savedRanks, ranks, ranks.Length);
        hero.Health.maxHealth = initialMaxHealth + 25 * ranks[(int)BasicSkill.Vitality];
        foreach (var source in rewards) rewardSources.Enqueue(source);
        PendingChoices = rewards.Length;
        foreach (int skill in savedOffers) offers.Add((BasicSkill)skill);
        restoredOffers = offers.Count == 3;
    }
    public float AttackBonus => Rank(BasicSkill.Strength) * 5;
    public float DefenseBonus => Rank(BasicSkill.IronSkin) * 2;
    public float SpeedMultiplier => 1 + Rank(BasicSkill.Speed) * .1f;
    public float AttackSpeedMultiplier => 1 + Rank(BasicSkill.Frenzy) * .15f;
    public float ReachBonus => Rank(BasicSkill.Reach) * .25f;
    public int Rank(BasicSkill skill) => ranks[(int)skill];
    void Awake() { hero = GetComponent<ThirdPersonHero>(); initialMaxHealth = hero.Health.maxHealth; }
    public static string Name(BasicSkill skill)
    {
        switch (skill) {
            case BasicSkill.Strength: return "强力打击";
            case BasicSkill.IronSkin: return "钢铁皮肤";
            case BasicSkill.Vitality: return "旺盛生命";
            case BasicSkill.Speed: return "疾行";
            case BasicSkill.Frenzy: return "快速挥砍";
            default: return "长臂攻击";
        }
    }
    public static string Description(BasicSkill skill)
    {
        switch (skill) {
            case BasicSkill.Strength: return "攻击力 +5\n可与武器加成叠加";
            case BasicSkill.IronSkin: return "防御力 +2\n可与护甲加成叠加";
            case BasicSkill.Vitality: return "最大生命 +25\n立即恢复 25 点生命";
            case BasicSkill.Speed: return "移动、跑步速度\n增加基础速度的 10%";
            case BasicSkill.Frenzy: return "攻击速度\n增加基础攻速的 15%";
            default: return "近战攻击距离\n增加 0.25 米";
        }
    }
    public void GainExperience(int amount)
    {
        if (amount <= 0 || hero.Health.Dead) return;
        Experience += amount;
        lastExperience = amount;
        noticeUntil = Time.unscaledTime + 3;
        while (Experience >= RequiredExperience) {
            Experience -= RequiredExperience;
            Level++;
            PendingChoices++;
            rewardSources.Enqueue("升级奖励");
        }
    }
    public bool GrantSkillChoice()
    {
        if (hero.Health.Dead) return false;
        PendingChoices++;
        rewardSources.Enqueue("祭坛赐福");
        BeginChoice();
        return true;
    }
    void Update()
    {
        if (hero.Health.Dead || hero.SaveMenuOpen) return;
        if (!IsChoosing && PendingChoices > 0 && !hero.Inventory.IsOpen) BeginChoice();
        if (!IsChoosing || Keyboard.current == null) return;
        var keyboard = Keyboard.current;
        if (keyboard.digit1Key.wasPressedThisFrame) SelectChoice(0);
        else if (keyboard.digit2Key.wasPressedThisFrame) SelectChoice(1);
        else if (keyboard.digit3Key.wasPressedThisFrame) SelectChoice(2);
    }
    public void BeginChoice()
    {
        if (IsChoosing || PendingChoices <= 0 || hero.Inventory.IsOpen || hero.Health.Dead) return;
        var pool = new List<BasicSkill>((BasicSkill[])System.Enum.GetValues(typeof(BasicSkill)));
        if (!restoredOffers) offers.Clear();
        for (int i = 0; !restoredOffers && i < 3; i++) {
            int index = AdventureRandom.Range(0, pool.Count,AdventureRandomStream.Rewards,this);
            offers.Add(pool[index]);
            pool.RemoveAt(index);
        }
        restoredOffers = false;
        if(PlayerHudPresenter.Running&&PlayerHudPresenter.Instance.Detail!="")PlayerHudPresenter.Instance.SetDetails("");
        IsChoosing = true;
        previousTimeScale = Time.timeScale;
        Time.timeScale = 0;
        Cursor.lockState = CursorLockMode.None;
        Cursor.visible = true;
    }
    public bool SelectChoice(int index)
    {
        if (!IsChoosing || index < 0 || index >= offers.Count) return false;
        var skill = offers[index];
        ranks[(int)skill]++;
        if (skill == BasicSkill.Vitality) {
            hero.Health.maxHealth += 25;
            hero.Health.Heal(25);
        }
        PendingChoices--;
        if (rewardSources.Count > 0) rewardSources.Dequeue();
        EndChoice();
        if (PendingChoices > 0) BeginChoice();
        return true;
    }
    void EndChoice()
    {
        if (!IsChoosing) return;
        IsChoosing = false;
        offers.Clear();
        Time.timeScale = previousTimeScale;
        ClosedFrame = Time.frameCount;
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }
    public void Clear()
    {
        EndChoice();
        PendingChoices = Experience = 0;
        restoredOffers = false;
        offers.Clear();
        rewardSources.Clear();
        Level = 1;
        System.Array.Clear(ranks, 0, ranks.Length);
        hero.Health.maxHealth = initialMaxHealth;
        noticeUntil = 0;
    }
    void OnDisable()
    {
        if (!IsChoosing) return;
        Time.timeScale = previousTimeScale;
        IsChoosing = false;
        Cursor.lockState = CursorLockMode.None;
        Cursor.visible = true;
    }
    void OnGUI()
    {
        if (hero.SaveMenuOpen) return;
        CombatChineseUI.Apply();
        Matrix4x4 previous = GUI.matrix;
        float scale = Mathf.Clamp(Mathf.Min(Screen.height / 800f, Screen.width / 1000f), .5f, 2);
        GUI.matrix = Matrix4x4.Scale(new Vector3(scale, scale, 1));
        float width = Screen.width / scale, height = Screen.height / scale;
        var text = new GUIStyle(GUI.skin.label) { fontSize = 20 };
        if (IsChoosing) {
            int oldDepth = GUI.depth;
            GUI.depth = -100;
            float left = width / 2 - 440, top = height / 2 - 190;
            GUI.Box(new Rect(left, top, 880, 380), "");
            GUI.Label(new Rect(left + 30, top + 20, 800, 45), $"{(rewardSources.Count > 0 ? rewardSources.Peek() : "技能奖励")} · 选择一个技能", new GUIStyle(text) { fontSize = 27 });
            GUI.Label(new Rect(left + 30, top + 70, 800, 32), $"游戏已暂停，点击选择或按数字 1 / 2 / 3。待选次数：{PendingChoices}", text);
            for (int i = 0; i < offers.Count; i++) {
                var skill = offers[i];
                float x = left + 25 + i * 280;
                GUI.Box(new Rect(x, top + 125, 270, 225), "");
                GUI.Label(new Rect(x + 15, top + 140, 240, 35), $"{i + 1}. {Name(skill)}", text);
                GUI.Label(new Rect(x + 15, top + 185, 240, 65), Description(skill), new GUIStyle(text) { fontSize = 18 });
                GUI.Label(new Rect(x + 15, top + 258, 240, 30), $"技能等级：{Rank(skill)} → {Rank(skill) + 1}", new GUIStyle(text) { fontSize = 17 });
                if (GUI.Button(new Rect(x + 15, top + 298, 240, 38), "选择此技能")) {
                    SelectChoice(i);
                    break;
                }
            }
            GUI.depth = oldDepth;
        }
        GUI.matrix = previous;
    }
}


