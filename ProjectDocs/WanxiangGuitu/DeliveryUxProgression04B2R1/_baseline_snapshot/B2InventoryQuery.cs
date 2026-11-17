using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using UnityEngine;

// UX-04-B2 / B2-02 + B2-05: ONE semantic filter contract shared by IMGUI and
// uGUI. There is deliberately NO per-UI integer filter meaning: both views read
// the same B2FilterState and call the same B2InventoryQuery.Apply().
//
// Source display uses ONLY GearItem.origin and GearItem.originRunId. No region
// or new source field is introduced. Sorting/filtering are pure read-only
// projections -- they never mutate, merge, stack or delete an item.

public enum B2Category { All, Weapon, Accessory, Arms, Armor, Container, Other }
public enum B2ItemStatus { All, Main, Reserve, Worn, Board, Unused, Overflow, Warehouse }
public enum B2SortKey { None, AttackDesc, AttackAsc, QualityDesc, QualityAsc, TypeAsc, NameAsc }

[Serializable]
public sealed class B2FilterSpec
{
    public B2Category category = B2Category.All;
    public int qualityMask;              // bits 0..4 = White..Red; 0 = all
    public B2ItemStatus status = B2ItemStatus.All;
    public B2SortKey sort = B2SortKey.None;
    public bool favoritesOnly;
    public string text = "";

    public string Key => (int)category + "|" + qualityMask + "|" + (int)status + "|" +
                         (int)sort + "|" + (favoritesOnly ? 1 : 0) + "|" + (text ?? "");
}

// Shared semantic tab table. Both UI paths render these exact labels and map
// each index through the SAME SpecForTab function (no divergent int semantics).
public static class B2FilterTabs
{
    public static readonly string[] Labels =
    {
        "全部", "武器", "饰品", "护臂", "品质", "状态", "排序", "收藏"
    };

    public static string CategoryLabel(B2Category c)
    {
        switch (c)
        {
            case B2Category.Weapon: return "武器";
            case B2Category.Accessory: return "饰品";
            case B2Category.Arms: return "护臂";
            case B2Category.Armor: return "防具";
            case B2Category.Container: return "容器";
            case B2Category.Other: return "其他";
            default: return "全部";
        }
    }
    public static string StatusLabel(B2ItemStatus s)
    {
        switch (s)
        {
            case B2ItemStatus.Main: return "主武器";
            case B2ItemStatus.Reserve: return "备用武器";
            case B2ItemStatus.Worn: return "已穿戴";
            case B2ItemStatus.Board: return "装备盘";
            case B2ItemStatus.Unused: return "未使用";
            case B2ItemStatus.Overflow: return "迁移暂存";
            case B2ItemStatus.Warehouse: return "仓库";
            default: return "全部状态";
        }
    }
    public static string SortLabel(B2SortKey s)
    {
        switch (s)
        {
            case B2SortKey.AttackDesc: return "攻击↓";
            case B2SortKey.AttackAsc: return "攻击↑";
            case B2SortKey.QualityDesc: return "品质↓";
            case B2SortKey.QualityAsc: return "品质↑";
            case B2SortKey.TypeAsc: return "类型";
            case B2SortKey.NameAsc: return "名称";
            default: return "默认顺序";
        }
    }
}

public static class B2FilterState
{
    static B2FilterSpec current = new B2FilterSpec();
    public static B2FilterSpec Current => current;
    public static int Tab { get; private set; }

    public static void Reset() { current = new B2FilterSpec(); Tab = 0; }
    public static void SetTab(int tab)
    {
        Tab = Mathf.Clamp(tab, 0, B2FilterTabs.Labels.Length - 1);
        current = SpecForTab(Tab);
    }
    // The SINGLE authoritative index -> semantic mapping, used by both UIs.
    public static B2FilterSpec SpecForTab(int tab)
    {
        var s = new B2FilterSpec();
        switch (tab)
        {
            case 1: s.category = B2Category.Weapon; break;
            case 2: s.category = B2Category.Accessory; break;
            case 3: s.category = B2Category.Arms; break;
            case 4: s.qualityMask = 1 << (int)GearQuality.Gold; break;   // 品质: 金/红重点
            case 5: s.status = B2ItemStatus.Unused; break;
            case 6: s.sort = B2SortKey.AttackDesc; break;
            case 7: s.favoritesOnly = true; break;
            default: break;
        }
        return s;
    }
    public static void SetCategory(B2Category c) { current.category = c; }
    public static void SetQuality(int mask) { current.qualityMask = mask; }
    public static void SetStatus(B2ItemStatus s) { current.status = s; }
    public static void SetSort(B2SortKey s) { current.sort = s; }
    public static void SetFavoritesOnly(bool v) { current.favoritesOnly = v; }
    public static void SetText(string t) { current.text = t ?? ""; }
    public static void CycleQuality()
    {
        int[] cycle = { 0, 1 << 0, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 3 | 1 << 4 };
        int at = Array.IndexOf(cycle, current.qualityMask);
        current.qualityMask = cycle[(at + 1 + cycle.Length) % cycle.Length];
    }
    public static void CycleStatus()
    {
        current.status = (B2ItemStatus)(((int)current.status + 1) % Enum.GetValues(typeof(B2ItemStatus)).Length);
    }
    public static void CycleSort()
    {
        current.sort = (B2SortKey)(((int)current.sort + 1) % Enum.GetValues(typeof(B2SortKey)).Length);
    }
    public static string Describe()
    {
        string q = current.qualityMask == 0 ? "五品质" : "品质掩码" + current.qualityMask;
        return B2FilterTabs.CategoryLabel(current.category) + " · " + q + " · " +
               B2FilterTabs.StatusLabel(current.status) + " · " + B2FilterTabs.SortLabel(current.sort) +
               (current.favoritesOnly ? " · 仅收藏" : "");
    }
}

public static class B2InventoryQuery
{
    public static B2Category CategoryOf(GearItem i)
    {
        if (i == null) return B2Category.Other;
        if (i.Container) return B2Category.Container;
        if (i.Weapon) return B2Category.Weapon;
        if (i.type == GearType.Accessory) return B2Category.Accessory;
        if (i.type == GearType.Arms) return B2Category.Arms;
        if (i.type == GearType.Armor || i.type == GearType.Trousers || i.type == GearType.Boots) return B2Category.Armor;
        return B2Category.Other;
    }

    public static B2ItemStatus StatusOf(GearItem i, AdventureLoadout gear, bool warehouse)
    {
        if (warehouse) return B2ItemStatus.Warehouse;
        if (i == null) return B2ItemStatus.All;
        if (i.worn) return B2ItemStatus.Worn;
        if (i.overflow) return B2ItemStatus.Overflow;
        if (i.board) return B2ItemStatus.Board;
        if (gear != null && i.id == gear.mainWeapon) return B2ItemStatus.Main;
        if (gear != null && i.id == gear.reserveWeapon) return B2ItemStatus.Reserve;
        return B2ItemStatus.Unused;
    }

    public static bool Matches(GearItem i, B2FilterSpec s, AdventureLoadout gear, bool warehouse)
    {
        if (i == null || s == null) return false;
        if (s.category != B2Category.All && CategoryOf(i) != s.category) return false;
        if (s.qualityMask != 0 && (s.qualityMask & (1 << (int)i.quality)) == 0) return false;
        if (s.status != B2ItemStatus.All && StatusOf(i, gear, warehouse) != s.status) return false;
        if (s.favoritesOnly && !B2Collection.IsFavorite(i.id)) return false;
        if (!string.IsNullOrEmpty(s.text) &&
            (i.Name ?? "").IndexOf(s.text, StringComparison.OrdinalIgnoreCase) < 0) return false;
        return true;
    }

    // Pure projection: returns a NEW list, never mutates the source collection.
    public static List<GearItem> Apply(IEnumerable<GearItem> src, B2FilterSpec s,
                                       AdventureLoadout gear, bool warehouse)
    {
        var list = new List<GearItem>();
        foreach (var i in src) if (Matches(i, s, gear, warehouse)) list.Add(i);
        switch (s == null ? B2SortKey.None : s.sort)
        {
            case B2SortKey.AttackDesc: list = list.OrderByDescending(i => i.Attack).ThenBy(i => i.id, StringComparer.Ordinal).ToList(); break;
            case B2SortKey.AttackAsc: list = list.OrderBy(i => i.Attack).ThenBy(i => i.id, StringComparer.Ordinal).ToList(); break;
            case B2SortKey.QualityDesc: list = list.OrderByDescending(i => (int)i.quality).ThenBy(i => i.id, StringComparer.Ordinal).ToList(); break;
            case B2SortKey.QualityAsc: list = list.OrderBy(i => (int)i.quality).ThenBy(i => i.id, StringComparer.Ordinal).ToList(); break;
            case B2SortKey.TypeAsc: list = list.OrderBy(i => (int)i.type).ThenBy(i => i.id, StringComparer.Ordinal).ToList(); break;
            case B2SortKey.NameAsc: list = list.OrderBy(i => i.Name, StringComparer.Ordinal).ToList(); break;
        }
        return list;
    }

    // B2-02: source display uses ONLY origin + originRunId. No new field.
    public static string SourceLabel(GearItem i)
    {
        if (i == null) return "";
        string head;
        switch (i.origin)
        {
            case ItemOrigin.DeploymentProtected: head = "入场保护"; break;
            case ItemOrigin.LegacyProtected: head = "旧档保护"; break;
            case ItemOrigin.RunLoot: head = "本局战利品"; break;
            default: head = "来源未标注"; break;
        }
        string run = string.IsNullOrEmpty(i.originRunId) ? "" : " · " +
            i.originRunId.Substring(0, Math.Min(8, i.originRunId.Length));
        return head + run;
    }

    // B2-04: duplicate hint key. Identity/position/origin are deliberately
    // excluded. Hint ONLY -- never merges, stacks or deletes anything.
    public static string DuplicateKey(GearItem i)
    {
        if (i == null) return "";
        string aff = i.affixes == null ? "" : string.Join(",", i.affixes.OrderBy(a => a).Select(a => a.ToString(CultureInfo.InvariantCulture)));
        return string.Join("|", new[] {
            ((int)i.type).ToString(CultureInfo.InvariantCulture),
            ((int)i.quality).ToString(CultureInfo.InvariantCulture),
            i.definitionId ?? "",
            i.savedAttack.ToString("R", CultureInfo.InvariantCulture),
            i.savedDefense.ToString("R", CultureInfo.InvariantCulture),
            aff,
            i.widthOverride.ToString(CultureInfo.InvariantCulture),
            i.heightOverride.ToString(CultureInfo.InvariantCulture) });
    }

    public static Dictionary<string, int> DuplicateHints(IEnumerable<GearItem> src)
    {
        var counts = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var i in src)
        {
            if (i == null) continue;
            string k = DuplicateKey(i);
            int n; counts.TryGetValue(k, out n); counts[k] = n + 1;
        }
        return counts;
    }

    // B2-05: one shared capacity line for BOTH UI paths.
    public static string CapacityLine(AdventureLoadout gear, CampRuntime camp)
    {
        int bag = gear != null && gear.Bag != null ? gear.Bag.Capacity : 0;
        int board = gear != null && gear.Rig != null ? gear.Rig.Capacity : 0;
        int wh = camp != null ? camp.Items.Count : 0;
        return "背包 " + bag + " 格 · 装备盘 " + board + " 格 · 永久仓库 " + wh + "/" + CampRuntime.Capacity + " 件";
    }
}
