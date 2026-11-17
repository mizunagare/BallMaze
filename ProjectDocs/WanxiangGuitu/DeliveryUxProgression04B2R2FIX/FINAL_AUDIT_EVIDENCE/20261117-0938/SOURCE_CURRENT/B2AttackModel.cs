using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

// UX-04-B2 / B2-01: SINGLE authoritative, read-only attack-power calculation.
//
// D-02 approved an EQUIVALENT refactor. AdventureLoadout.Attack / Defense now
// delegate to the pure functions below, so there is exactly ONE calculation
// chain shared by the live properties, the comparison preview and the golden
// matrix. No coefficient, no stacking rule (D-24) and no equipment attribute
// was changed: the expressions are byte-for-byte the pre-B2 expressions.
//
// The model NEVER mutates AdventureLoadout.items, never writes a save, and
// never touches the random stream. Previews work on Clone()d snapshots only.

public enum B2EquipRole
{
    None,            // read-only snapshot of the current state
    Main,            // simulate candidate as main weapon
    Reserve,         // simulate candidate as reserve weapon (contributes 0)
    Board,           // simulate candidate placed on the equipment board
    Overflow,        // candidate in migration overflow (contributes 0)
    Worn,            // candidate worn as a container (contributes 0, changes bonus)
    ContainerRig,    // candidate worn as chest rig
    ContainerBag     // candidate worn as backpack
}

[Serializable]
public struct B2AttackSnapshot
{
    public float baseDamage;
    public float progressionBonus;
    public float loadoutAttack;
    public float loadoutDefense;
    public float attackPower;
    public float basicPower;
    public float mainContribution;
    public float reserveContribution;
    public float accessoryContribution;
    public float armsContribution;
    public float boardContribution;
    public float containerBonus;
    public GearType weaponType;
    public int activeCount;
}

[Serializable]
public struct B2AttackEvaluation
{
    public B2AttackSnapshot before;
    public B2AttackSnapshot after;
    public float deltaAttackPower;
    public float deltaBasicPower;
    public float deltaLoadoutAttack;
    public float itemAttack;
    public float itemDefense;
    public B2EquipRole role;
    public bool feasible;
    public string reason;
    [NonSerialized] public string candidateGearId, replacedGearId;
    [NonSerialized] public float oldContribution, newContribution, oldContributionAfter, newContributionBefore;
    [NonSerialized] public int capacityBefore, capacityAfter;
    [NonSerialized] public bool swapped, oldReturnedToBag;
    [NonSerialized] public string projectedMainId, projectedReserveId;
    [NonSerialized] List<GearItem> projectedItems;
    // Defensive clones: callers cannot mutate either the real state or the stored projection.
    public IReadOnlyList<GearItem> ProjectedItems => projectedItems == null ? null : projectedItems.Select(i => i.Clone()).ToList().AsReadOnly();
    internal void SetProjection(IReadOnlyList<GearItem> list, string mainId, string reserveId)
    {
        projectedItems = list.Select(i => i.Clone()).ToList();
        projectedMainId = mainId; projectedReserveId = reserveId;
    }
}

public static class B2AttackModel
{
    // Verbatim equivalent of the pre-B2 AdventureLoadout.Main getter:
    //   items.Find(i => i.id == mainWeapon && i.InBag && i.Weapon)
    public static GearItem FindMain(IReadOnlyList<GearItem> list, string mainId)
    {
        if (list == null || string.IsNullOrEmpty(mainId)) return null;
        for (int n = 0; n < list.Count; n++)
        {
            var i = list[n];
            if (i != null && i.id == mainId && i.InBag && i.Weapon) return i;
        }
        return null;
    }

    // Verbatim equivalent of the pre-B2 Unique + Active chain:
    //   Unique  = items.GroupBy(i => i.id).Select(g => g.First())
    //   Active  = Unique.Where(i => !i.overflow && !i.worn && (i.board || i == Main))
    // GroupBy preserves first-occurrence order, and GearItem does not overload
    // ==, so ReferenceEquals reproduces the original identity comparison exactly.
    public static IEnumerable<GearItem> Active(IReadOnlyList<GearItem> list, string mainId)
    {
        var main = FindMain(list, mainId);
        var seen = new HashSet<string>();
        var result = new List<GearItem>();
        for (int n = 0; n < list.Count; n++)
        {
            var i = list[n];
            if (i == null || !seen.Add(i.id ?? "")) continue;
            if (i.overflow || i.worn) continue;
            if (i.board || ReferenceEquals(i, main)) result.Add(i);
        }
        return result;
    }

    // Pre-B2: Active.Sum(i => i.Attack) + (Rig?.attackBonus ?? 0) + (Bag?.attackBonus ?? 0)
    public static float ComputeAttack(IReadOnlyList<GearItem> list, string mainId,
                                      ContainerDefinition rig, ContainerDefinition bag)
    {
        return Active(list, mainId).Sum(i => i.Attack)
             + (rig != null ? rig.attackBonus : 0f)
             + (bag != null ? bag.attackBonus : 0f);
    }

    // Pre-B2: Active.Where(i => i.board).Sum(i => i.Defense) + rig/bag defenseBonus
    public static float ComputeDefense(IReadOnlyList<GearItem> list, string mainId,
                                       ContainerDefinition rig, ContainerDefinition bag)
    {
        float sum = 0f;
        foreach (var i in Active(list, mainId)) if (i.board) sum += i.Defense;
        return sum + (rig != null ? rig.defenseBonus : 0f) + (bag != null ? bag.defenseBonus : 0f);
    }

    // Final AttackPower chain (ThirdPersonHero.cs:22 / HeroEquipment.cs:15):
    //   attackDamage + AdventureLoadout.Attack + Progression.AttackBonus
    // BasicPower chain (AdventureCombat.cs:84):
    //   AttackPower * (MainWeapon == Spear ? SpearPower : 1)
    public static B2AttackSnapshot Snapshot(IReadOnlyList<GearItem> list, string mainId,
                                            string reserveId, ContainerDefinition rig,
                                            ContainerDefinition bag, ThirdPersonHero hero)
    {
        var s = new B2AttackSnapshot();
        s.baseDamage = hero != null ? hero.attackDamage : 25f;
        s.progressionBonus = hero != null && hero.Progression != null ? hero.Progression.AttackBonus : 0f;
        s.loadoutAttack = ComputeAttack(list, mainId, rig, bag);
        s.loadoutDefense = ComputeDefense(list, mainId, rig, bag);
        s.attackPower = s.baseDamage + s.loadoutAttack + s.progressionBonus;
        var main = FindMain(list, mainId);
        s.weaponType = main != null ? main.type : GearType.Sword;
        s.basicPower = s.attackPower * (s.weaponType == GearType.Spear ? AdventureCombat.SpearPower : 1f);
        s.containerBonus = (rig != null ? rig.attackBonus : 0f) + (bag != null ? bag.attackBonus : 0f);

        // Contributions are derived from the REAL Active set, never from a
        // simple candidate.Attack - current.Attack subtraction.
        var active = Active(list, mainId).ToArray();
        foreach (var i in active)
        {
            if (ReferenceEquals(i, main)) s.mainContribution += i.Attack;
            if (!string.IsNullOrEmpty(reserveId) && i.id == reserveId) s.reserveContribution += i.Attack;
            if (i.type == GearType.Accessory) s.accessoryContribution += i.Attack;
            if (i.type == GearType.Arms) s.armsContribution += i.Attack;
            if (i.board) s.boardContribution += i.Attack;
        }
        s.activeCount = active.Length;
        return s;
    }

    // UX04B2R2FIX: legacy name is now an Add query; it never guesses a replaced id.
    public static B2AttackEvaluation Preview(AdventureLoadout gear, ThirdPersonHero hero,
                                             GearItem candidate, B2EquipRole role)
    {
        if (gear == null) return new B2AttackEvaluation { reason = "缺少装备" };
        var position = candidate != null ? new Vector2Int(candidate.x, candidate.y) : default;
        int rotation = candidate != null ? candidate.rotation : 0;
        if (candidate != null && role == B2EquipRole.Board && gear.items != null && gear.items.All(i => i != null))
            gear.FindPreviewAddPosition(candidate.id, out position, out rotation);
        return Evaluate(gear, hero, candidate != null ? candidate.id : null, null, position, role, rotation, false);
    }

    public static B2AttackEvaluation Evaluate(AdventureLoadout gear, ThirdPersonHero hero,
        string candidateId, string replacedId, Vector2Int position, B2EquipRole role, int rotation, bool replace)
    {
        var ev = new B2AttackEvaluation { role = role, candidateGearId = candidateId,
            replacedGearId = replacedId, reason = "", feasible = false };
        if (gear == null) { ev.reason = "缺少装备"; return ev; }
        if (gear.items == null || gear.items.Any(i => i == null || string.IsNullOrEmpty(i.id)) ||
            gear.items.Select(i => i.id).Distinct().Count() != gear.items.Count)
        { ev.reason = "装备身份重复或无效，操作已取消。"; return ev; }
        ev.before = Snapshot(gear.items, gear.mainWeapon, gear.reserveWeapon, gear.Rig, gear.Bag, hero);
        ev.after = ev.before;
        var candidate = gear.items.FirstOrDefault(i => i != null && i.id == candidateId);
        var previous = gear.items.FirstOrDefault(i => i != null && i.id == replacedId);
        ev.itemAttack = candidate != null ? candidate.Attack : 0f;
        ev.itemDefense = candidate != null ? candidate.Defense : 0f;
        ev.oldContribution = Contribution(gear.items, gear.mainWeapon, replacedId);
        ev.newContributionBefore = Contribution(gear.items, gear.mainWeapon, candidateId);
        ev.oldContributionAfter = ev.oldContribution;
        ev.newContribution = ev.newContributionBefore;
        bool boardCapacity = role == B2EquipRole.Board || role == B2EquipRole.ContainerRig ||
            role == B2EquipRole.Worn && candidate != null && candidate.type == GearType.ChestRig;
        ev.capacityBefore = ContainersCapacity(gear.items, boardCapacity);
        ev.capacityAfter = ev.capacityBefore;
        if (!gear.ProjectEquipment(candidateId, replacedId, position, role, rotation, replace,
            out var projected, out var mainId, out var reserveId, out var swapped, out var reason))
        {
            ev.reason = reason;
            ev.SetProjection(gear.items, gear.mainWeapon, gear.reserveWeapon);
            return ev;
        }
        ev.feasible = true;
        ev.reason = reason;
        ev.swapped = swapped;
        ev.oldReturnedToBag = previous != null && projected.Any(i => i.id == replacedId && i.InBag);
        ev.after = Snapshot(projected, mainId, reserveId, AdventureLoadout.ContainersFor(projected, true),
            AdventureLoadout.ContainersFor(projected, false), hero);
        ev.capacityAfter = ContainersCapacity(projected, boardCapacity);
        ev.oldContributionAfter = Contribution(projected, mainId, replacedId);
        ev.newContribution = Contribution(projected, mainId, candidateId);
        ev.deltaLoadoutAttack = ev.after.loadoutAttack - ev.before.loadoutAttack;
        ev.deltaAttackPower = ev.after.attackPower - ev.before.attackPower;
        ev.deltaBasicPower = ev.after.basicPower - ev.before.basicPower;
        ev.SetProjection(projected, mainId, reserveId);
        return ev;
    }

    static int ContainersCapacity(IReadOnlyList<GearItem> list, bool board)
    {
        var container = AdventureLoadout.ContainersFor(list, board);
        return container != null ? container.Capacity : 0;
    }

    // Per-item contribution uses the same Snapshot/Active chain, including worn bonuses.
    static float Contribution(IReadOnlyList<GearItem> list, string mainId, string id)
    {
        if (string.IsNullOrEmpty(id)) return 0f;
        var item = list.FirstOrDefault(i => i != null && i.id == id);
        if (item == null) return 0f;
        var rig = item.worn && item.type == GearType.ChestRig ? AdventureCatalog.Container(item.definitionId) : null;
        var bag = item.worn && item.type == GearType.Backpack ? AdventureCatalog.Container(item.definitionId) : null;
        var active = Active(list, mainId).Where(i => i.id == id).ToArray();
        return Snapshot(active, mainId, null, rig, bag, null).loadoutAttack;
    }
}
