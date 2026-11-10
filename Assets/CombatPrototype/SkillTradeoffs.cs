using System;
using System.Collections.Generic;
using System.Linq;

// UX-PROGRESSION-01 P1-05 · skill trade-off table.
// Every number is read from the shipped definition (WeaponSkillCatalog) or copied
// from the corresponding motor constant in NewWeaponCombat / GreatswordCombat /
// ScytheCombat. No value is invented and nothing here changes gameplay.
public sealed class SkillRow
{
    public readonly string weapon, name, id;
    public readonly float cooldown, startup, reach, charge;
    public readonly int segments;
    public SkillRow(string weapon, string name, string id, float cooldown, float startup, int segments, float reach, float charge)
    { this.weapon = weapon; this.name = name; this.id = id; this.cooldown = cooldown; this.startup = startup; this.segments = segments; this.reach = reach; this.charge = charge; }
    public string Cooldown => cooldown > 0 ? cooldown.ToString("0.#") + "s" : "—";
    public string Startup => startup > 0 ? startup.ToString("0.##") + "s" : "—";
    public string Segments => segments > 0 ? segments + "段" : "—";
    public string Reach => reach > 0 ? reach.ToString("0.#") + "m" : "—";
    public string Charge => charge > 0 ? charge.ToString("0.##") + "s" : "—";
    public string Compact => name + " " + Cooldown + "/" + Startup + "/" + Segments + "/" + Reach + "/" + Charge;
}

public static class SkillTradeoffs
{
    static string WeaponName(GearType type) => type == GearType.Sword ? "长剑" : type == GearType.Spear ? "长枪"
        : type == GearType.Staff ? "法杖" : type == GearType.Bow ? "弓" : type == GearType.TwinBlades ? "双刃"
        : type == GearType.Greatsword ? "巨剑" : type == GearType.Scythe ? "镰刀" : type.ToString();

    // 8 catalog skills (2 per legacy weapon) + 6 new-weapon skills = 14.
    public static readonly SkillRow[] Rows = Build();
    static SkillRow[] Build()
    {
        var rows = new List<SkillRow>();
        foreach (var d in WeaponSkillCatalog.All)
            rows.Add(new SkillRow(WeaponName(d.weapon), d.name, d.id, d.cooldown, d.startup, d.pulses, d.reach, d.charge));
        // New weapons: duration/startup/reach/count taken from the motors.
        // twin: NewWeaponCombat.TwinBladeMotor (cd 7/8, startup .14/.28, 6/2 hits, reach 1.4)
        // greatsword: GreatswordCombat (cd 9/10, startup .65/.60, reach 3.1 sector / 8 ground wave)
        // scythe: ScytheCombat (cd 8/11, startup .3/.4, 3 arcs / 4.5 pull)
        rows.Add(new SkillRow("双刃", NewWeaponCombat.NameFor(GearType.TwinBlades, 0), "twin.volley", 7, .14f, 6, 1.4f, 0));
        rows.Add(new SkillRow("双刃", NewWeaponCombat.NameFor(GearType.TwinBlades, 1), "twin.counter", 8, .28f, 2, 1.4f, 0));
        rows.Add(new SkillRow("巨剑", NewWeaponCombat.NameFor(GearType.Greatsword, 0), "greatsword.cleave", 9, .65f, 1, 3.1f, 0));
        rows.Add(new SkillRow("巨剑", NewWeaponCombat.NameFor(GearType.Greatsword, 1), "greatsword.wave", 10, .60f, 1, 8f, 0));
        rows.Add(new SkillRow("镰刀", NewWeaponCombat.NameFor(GearType.Scythe, 0), "scythe.reap", 8, .3f, 3, 3.4f, 0));
        rows.Add(new SkillRow("镰刀", NewWeaponCombat.NameFor(GearType.Scythe, 1), "scythe.pull", 11, .4f, 1, 4.5f, 0));
        return rows.ToArray();
    }

    public const string Header = "[技能取舍] 14 项 · 顺序：名称 冷却/前摇/段数/范围/蓄力（— 表示该技能没有这个参数）";
    public const string Foot = "数值全部来自现有定义；蓄力仅长枪·蓄势穿刺与弓·蓄势贯矢存在。新武器冷却受聚能词缀 +1s 影响（现有实现）。";

    public static SkillRow[] For(GearType type) => Rows.Where(r => r.weapon == WeaponName(type)).ToArray();
    public static string Line(GearType type) => WeaponName(type) + " · " + string.Join(" · ", For(type).Select(r => r.Compact));

    public static string Table()
    {
        var lines = new List<string> { Header };
        foreach (var g in ObjectiveCatalog.WeaponOrder) lines.Add(Line(g));
        lines.Add("[独占机制] 旋风横扫·扫锋拒敌·陨火留场·扇形箭雨·裂地冲击波·灵魂牵引为独占收益；多段与蓄力属节奏，不折算成等效倍率");
        lines.Add("[有效距离带] 长剑≤1.8m · 长枪2-4.2m · 法杖6-35m · 弓8-57.5m · 双刃≤1.4m · 巨剑1.5-8m · 镰刀1.2-5.6m（回响范围内×1.25）");
        lines.Add("[T3 专属指标] 双刃反击·灵魂牵引数值冻结：仅以专属事件验收，不折算 η、不纳入 T1/T2 通过率");
        lines.Add(Foot);
        return string.Join("\n", lines);
    }
}
