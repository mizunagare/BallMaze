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
        float sum = 0f;
        foreach (var i in Active(list, mainId)) sum += i.Attack;
        return sum + (rig != null ? rig.attackBonus : 0f) + (bag != null ? bag.attackBonus : 0f);
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

    // Simulate an equipment replacement on a CLONED list. Nothing here writes
    // back to gear.items, mainWeapon, reserveWeapon, any save, or any coefficient.
    public static B2AttackEvaluation Preview(AdventureLoadout gear, ThirdPersonHero hero,
                                             GearItem candidate, B2EquipRole role)
    {
        var ev = new B2AttackEvaluation();
        ev.role = role;
        ev.feasible = true;
        ev.reason = "";
        ev.itemAttack = candidate != null ? candidate.Attack : 0f;
        ev.itemDefense = candidate != null ? candidate.Defense : 0f;
        if (gear == null || hero == null) { ev.feasible = false; ev.reason = "缺少装备或角色"; return ev; }

        var real = gear.items;
        var rig0 = gear.Rig;
        var bag0 = gear.Bag;
        ev.before = Snapshot(real, gear.mainWeapon, gear.reserveWeapon, rig0, bag0, hero);

        if (candidate == null || role == B2EquipRole.None)
        {
            ev.after = ev.before;
        }
        else
        {
            var copy = real.Select(i => i.Clone()).ToList();
            var c = candidate.Clone();
            copy.RemoveAll(i => i.id == c.id);
            string mainId = gear.mainWeapon;
            string reserveId = gear.reserveWeapon;

            switch (role)
            {
                case B2EquipRole.Main:
                    if (!c.Weapon) { ev.feasible = false; ev.reason = "候选不是武器，不能设为主武器"; break; }
                    c.board = false; c.worn = false; c.overflow = false;
                    if (c.id == reserveId) reserveId = mainId;   // mirrors SelectMain
                    mainId = c.id;
                    break;
                case B2EquipRole.Reserve:
                    if (!c.Weapon || c.id == mainId) { ev.feasible = false; ev.reason = "候选不能设为备用武器"; break; }
                    c.board = false; c.worn = false; c.overflow = false;
                    reserveId = c.id;                              // Active unchanged -> delta 0
                    break;
                case B2EquipRole.Board:
                    if (c.Container || (gear.Carried(candidate))) { ev.feasible = false; ev.reason = "容器或携带中的武器不能放入装备盘"; break; }
                    c.board = true; c.worn = false; c.overflow = false;
                    break;
                case B2EquipRole.Overflow:
                    c.board = false; c.worn = false; c.overflow = true; c.x = c.y = -1;
                    break;
                case B2EquipRole.Worn:
                case B2EquipRole.ContainerRig:
                case B2EquipRole.ContainerBag:
                    if (!c.Container) { ev.feasible = false; ev.reason = "候选不是容器，不能穿戴"; break; }
                    c.worn = true; c.board = false; c.overflow = false; c.x = c.y = -1;
                    break;
            }
            if (!ev.feasible) { ev.after = ev.before; return ev; }
            copy.Add(c);
            var rig1 = AdventureLoadout.ContainersFor(copy, true);
            var bag1 = AdventureLoadout.ContainersFor(copy, false);
            ev.after = Snapshot(copy, mainId, reserveId, rig1, bag1, hero);
        }

        ev.deltaLoadoutAttack = ev.after.loadoutAttack - ev.before.loadoutAttack;
        ev.deltaAttackPower = ev.after.attackPower - ev.before.attackPower;
        ev.deltaBasicPower = ev.after.basicPower - ev.before.basicPower;
        return ev;
    }
}
