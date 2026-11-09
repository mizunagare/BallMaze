using System;
using System.Collections.Generic;
using System.Linq;
// UX-PROGRESSION-01 P1: objective contract and player-facing identity copy.
// Pure data only: no Unity calls, no scene access, no RNG, no writes. Every
// threshold below is derived from content that already exists in the build;
// see ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1/OBJECTIVE_CARD_MATRIX.csv
// for the per-card source proof. Nothing here grants a reward or a receipt.
public enum ObjectiveConditionKind { GrossMaterial, TreasureOpened, EliteOrBossKilled, NamedEnemyDead, VeinDestroyed, ChainStep, NamedChest }

public sealed class ObjectiveCondition
{
    public readonly ObjectiveConditionKind kind;
    public readonly string label;
    public readonly int required;
    public readonly int[] materials;
    public readonly string entityId;
    public readonly string[] chain;
    ObjectiveCondition(ObjectiveConditionKind k, string label, int required, int[] materials, string entityId, string[] chain)
    { kind = k; this.label = label; this.required = required; this.materials = materials; this.entityId = entityId; this.chain = chain; }
    public static ObjectiveCondition Material(string label, int required, params MaterialKind[] kinds) =>
        new ObjectiveCondition(ObjectiveConditionKind.GrossMaterial, label, required, kinds == null || kinds.Length == 0 ? null : kinds.Select(k => (int)k).ToArray(), null, null);
    public static ObjectiveCondition Count(ObjectiveConditionKind kind, string label, int required) =>
        new ObjectiveCondition(kind, label, required, null, null, null);
    public static ObjectiveCondition Enemy(string label, int required, string entityId) =>
        new ObjectiveCondition(ObjectiveConditionKind.NamedEnemyDead, label, required, null, entityId, null);
    public static ObjectiveCondition Chest(string label, string entityId) =>
        new ObjectiveCondition(ObjectiveConditionKind.NamedChest, label, 1, null, entityId, null);
    public static ObjectiveCondition Steps(string label, params string[] ids) =>
        new ObjectiveCondition(ObjectiveConditionKind.ChainStep, label, ids.Length, null, null, ids);
}

public sealed class ObjectiveCard
{
    public readonly string id, region, title, oneLine, nextHint;
    public readonly ExpeditionGoal goal;
    public readonly ObjectiveCondition[] conditions;
    public ObjectiveCard(string id, string region, ExpeditionGoal goal, string title, string oneLine, string nextHint, params ObjectiveCondition[] conditions)
    { this.id = id; this.region = region; this.goal = goal; this.title = title; this.oneLine = oneLine; this.nextHint = nextHint; this.conditions = conditions; }
}

public static class ObjectiveCatalog
{
    public const string Forest = "ForestRuins", Ruins = "AncientRuins", Cavern = "CrystalCavern";
    // Chain ids are the existing ruins interaction chain (RuinsLayout.Events / RuinsExploration.CanUse).
    public static readonly string[] RuinsChain = { "c1:lever", "c1:door", "c1:archive", "c1:hidden" };
    public const string RuinsGuardian = "c1:guardian";
    public const string CavernChamberChest = "c22:chamber:chest";
    public const string CavernFarChest = "c23:far-shore:chest";
    public const string CavernWarden = "c24:boss:crystal-warden";

    public static readonly ObjectiveCard[] All =
    {
        new ObjectiveCard("forest.gather", Forest, ExpeditionGoal.Gather, "满载而归",
            "带走 12 单位本局新采集的材料，成功撤离才算达成", "采集矿点或开箱补足材料",
            ObjectiveCondition.Material("材料", 12)),
        new ObjectiveCard("forest.treasure", Forest, ExpeditionGoal.Treasure, "扫箱",
            "开启森林三处宝箱，成功撤离才算达成", "前往最近未开宝箱",
            ObjectiveCondition.Count(ObjectiveConditionKind.TreasureOpened, "宝箱", 3)),
        new ObjectiveCard("forest.challenge", Forest, ExpeditionGoal.Challenge, "拔点",
            "击败一名精英或首领，成功撤离才算达成", "前往最近的精英或首领",
            ObjectiveCondition.Count(ObjectiveConditionKind.EliteOrBossKilled, "强敌", 1)),

        new ObjectiveCard("ruins.gather", Ruins, ExpeditionGoal.Gather, "清点",
            "遗迹没有矿脉：材料只来自宝箱与敌人", "开箱或击败守卫补足材料",
            ObjectiveCondition.Count(ObjectiveConditionKind.TreasureOpened, "宝箱", 2),
            ObjectiveCondition.Material("材料", 6)),
        new ObjectiveCard("ruins.treasure", Ruins, ExpeditionGoal.Treasure, "解封",
            "机关→石门→碑文→密室宝箱，顺序由现有交互决定", "按机关提示推进下一步",
            ObjectiveCondition.Steps("机关", RuinsChain)),
        new ObjectiveCard("ruins.challenge", Ruins, ExpeditionGoal.Challenge, "守誓",
            "击败遗迹守护者，成功撤离才算达成", "前往守护者大厅",
            ObjectiveCondition.Enemy("守护者", 1, RuinsGuardian)),

        new ObjectiveCard("cavern.gather", Cavern, ExpeditionGoal.Gather, "掘脉",
            "破坏三处矿脉，并带回 10 单位矿石与晶石", "沿青色晶纹深入矿脉",
            ObjectiveCondition.Count(ObjectiveConditionKind.VeinDestroyed, "矿脉", 3),
            ObjectiveCondition.Material("矿晶", 10, MaterialKind.Ore, MaterialKind.CrystalShard)),
        new ObjectiveCard("cavern.treasure", Cavern, ExpeditionGoal.Treasure, "双箱",
            "矿室箱与对岸箱各一处，需先开启对应机关", "先开矿室或回程桥机关",
            ObjectiveCondition.Chest("矿室宝箱", CavernChamberChest),
            ObjectiveCondition.Chest("对岸宝箱", CavernFarChest)),
        new ObjectiveCard("cavern.challenge", Cavern, ExpeditionGoal.Challenge, "试锋",
            "击败晶脊守望者，成功撤离才算达成", "前往东岸挑战守望者",
            ObjectiveCondition.Enemy("守望者", 1, CavernWarden)),
    };

    public static bool IsRegion(string region) => region == Forest || region == Ruins || region == Cavern;
    public static ObjectiveCard Find(string id) => All.FirstOrDefault(c => c.id == id);
    public static ObjectiveCard For(string region, ExpeditionGoal goal) =>
        All.FirstOrDefault(c => c.region == region && c.goal == goal);
    public static ObjectiveCard[] Of(string region) => All.Where(c => c.region == region).ToArray();
    public static string Label(ExpeditionGoal goal) => goal == ExpeditionGoal.Gather ? "采集" : goal == ExpeditionGoal.Treasure ? "寻宝" : "讨伐";
    public static string RegionLabel(string region) => region == Ruins ? "遗迹" : region == Cavern ? "洞窟" : region == Forest ? "森林" : "未知";

    // Region identity: one line, three axis stars, recommended objective. Stars are
    // design expression over existing content density, never a numeric bonus.
    public static string RegionOneLine(string region) =>
        region == Ruins ? "一条机关链，尽头是收藏：没有矿脉，靠机关、宝箱与守护者" :
        region == Cavern ? "高价值矿脉 + 空间机关 + 可选强敌：矿晶最密" :
        region == Forest ? "广袤的资源沙盘，路线自己选：唯一的新武器掉落来源" : "";
    public static string[] RegionAxes(string region) => region == Ruins ? new[] { "资源 ☆（0 矿脉）", "挑战 ★★★（机关链+守护者）", "收藏 ★★★（5 件永久藏品）" }
        : region == Cavern ? new[] { "资源 ★★（4 矿脉，矿晶专精）", "挑战 ★★★（能量区+精英+守望者）", "收藏 ★★（首次击杀+机关）" }
        : region == Forest ? new[] { "资源 ★★★（42 矿点，6 类材料）", "挑战 ★★（11 遭遇+2 可选首领）", "收藏 ★（2 首领徽章）" }
        : new string[0];
    public static string RegionRecommended(string region) =>
        region == Ruins ? "推荐目标：解封（机关链是这里唯一独有的体验）" :
        region == Cavern ? "推荐目标：掘脉 或 试锋（看装备；两者都不需要清场）" :
        region == Forest ? "推荐目标：扫箱 或 满载而归（材料缺口优先采集）" : "";
    // D-13: recommendation text only. No gate, no difficulty tier, no stat change.
    public static string RegionPrepare(string region) =>
        region == Ruins ? "推荐准备：紫装以上 + 近战与远程各一（只提示，不设门槛）" :
        region == Cavern ? "推荐准备：金装以上 + 药水（守望者为可选挑战，可全程绕行）" :
        region == Forest ? "推荐准备：任意白装即可，42 个矿点足够补材料" : "";

    // Seven weapon role cards: derived from existing parameters only.
    public static string WeaponRole(GearType type) => type == GearType.Sword ? "稳定连段 / 低门槛"
        : type == GearType.Spear ? "距离控制 / 蓄力穿刺" : type == GearType.Staff ? "区域封锁 / 延迟爆发"
        : type == GearType.Bow ? "远程贯穿 / 蓄力狙击" : type == GearType.TwinBlades ? "高频多段 / 反击窗口"
        : type == GearType.Greatsword ? "蓄力破防 / 地面冲击" : type == GearType.Scythe ? "群体收割 / 限速牵引" : "未配置";
    public static string WeaponReason(GearType type) => type == GearType.Sword ? "三拍连斩 3×65%，回旋剑阵 3 脉冲 — 出手稳定"
        : type == GearType.Spear ? "蓄势穿刺 1.2 倍+蓄力，扫锋拒敌双向扇扫"
        : type == GearType.Staff ? "余烬符阵接触后留场 3 脉冲，回响连珠三段重瞄"
        : type == GearType.Bow ? "蓄势贯矢最多贯穿 3 目标，追点连射三段重瞄"
        : type == GearType.TwinBlades ? "六段 40% 交替碰撞，真实闪避成功才强化反击"
        : type == GearType.Greatsword ? "蓄力下劈破防，裂地冲击沿地面前进"
        : type == GearType.Scythe ? "三段弧形收割，4.5 米限速牵引（Boss 免疫）" : "";
    public static GearType[] WeaponOrder => new[] { GearType.Sword, GearType.Spear, GearType.Staff, GearType.Bow, GearType.TwinBlades, GearType.Greatsword, GearType.Scythe };
}
