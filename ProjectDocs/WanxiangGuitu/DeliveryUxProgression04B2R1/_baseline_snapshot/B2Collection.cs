using System;
using System.Collections.Generic;

// UX-04-B2 / B2-04: SESSION-ONLY favourites.
//
// This is an ordinary in-process HashSet<string>. It is NOT a GearItem field,
// NOT part of CombatSaveData / CombatCheckpoint / ProfileState, NOT serialized
// by JsonUtility, and NOT written to any save. A process restart naturally
// yields an empty set -- that is the required "clear on restart" behaviour.
//
// Scope of protection (deliberately narrow):
//   * favourite items cannot be QUICK-dismantled (single server-side gate)
//   * favourite items cannot be silently dropped by batch organisation
//   * normal deposit / withdraw / equip / move remain fully allowed
//   * the player can always un-favourite explicitly
// No durability, repair, upgrade, star or currency is introduced.

public static class B2Collection
{
    static readonly HashSet<string> ids = new HashSet<string>(StringComparer.Ordinal);
    // Process-scoped token: proves the set is re-created on each process start.
    public static readonly string SessionToken = Guid.NewGuid().ToString("N").Substring(0, 12);

    public static int Count => ids.Count;
    public static bool IsFavorite(string id) => !string.IsNullOrEmpty(id) && ids.Contains(id);

    public static bool Toggle(string id)
    {
        if (string.IsNullOrEmpty(id)) return false;
        if (ids.Remove(id)) return false;
        ids.Add(id);
        return true;
    }
    public static bool Add(string id)
    {
        if (string.IsNullOrEmpty(id)) return false;
        return ids.Add(id);
    }
    public static bool Remove(string id)
    {
        if (string.IsNullOrEmpty(id)) return false;
        return ids.Remove(id);
    }
    public static void Clear() => ids.Clear();
    public static string[] Snapshot()
    {
        var a = new string[ids.Count];
        ids.CopyTo(a);
        Array.Sort(a, StringComparer.Ordinal);
        return a;
    }

    // Single authoritative gate for quick dismantle. Used by BOTH UI paths and
    // by AdventureLoadout.Salvage so no UI-only trick can bypass it.
    public static bool CanQuickDismantle(GearItem item)
        => item != null && !IsFavorite(item.id) && AdventureLoadout.SalvageAllowed(item);

    // Batch organisation must never lose a favourite. Callers pass the ids
    // present BEFORE and AFTER the operation; any missing favourite aborts it.
    public static bool BatchPreservesFavourites(IEnumerable<string> afterIds)
    {
        if (ids.Count == 0) return true;
        var after = new HashSet<string>(afterIds ?? new string[0], StringComparer.Ordinal);
        foreach (var id in ids) if (!after.Contains(id)) return false;
        return true;
    }
}
