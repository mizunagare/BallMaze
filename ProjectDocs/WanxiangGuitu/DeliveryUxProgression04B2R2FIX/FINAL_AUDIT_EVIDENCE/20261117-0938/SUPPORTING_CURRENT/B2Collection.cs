using System;
using System.Collections.Generic;
using System.Linq;

// UX-04-B2 / B2-04: SESSION-ONLY favourites.
//
// R1-01 (UX-04-B2-R1): the favourite set is keyed ONLY by the equipment's
// unique identity (GearItem.id, a GUID string). It is a single process-wide
// set and is NEVER bound to a container: an item may live in the bag, on the
// equipment board, in overflow, worn, or in the permanent warehouse, and its
// favourite state follows it by id across all of those locations.
//
// This is an ordinary in-process HashSet<string>. It is NOT a GearItem field,
// NOT part of CombatSaveData / CombatCheckpoint / ProfileState, NOT serialized
// by JsonUtility, and NOT written to any save. A process restart naturally
// yields an empty set -- that is the required "clear on restart" behaviour.
//
// Scope of protection (deliberately narrow):
//   * favourite items cannot be QUICK-dismantled (single server-side gate)
//   * favourite items cannot be silently dropped by a batch organisation
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

    // R1-01 (#7/#8): called ONLY from the successful-dismantle path of
    // AdventureLoadout.Salvage. A favourite can never be dismantled by the
    // product gate, so this is a defensive cleanup: if a favourite id somehow
    // still referenced the now-destroyed equipment, drop it. Every failure
    // branch of Salvage returns before this call, so a refused dismantle NEVER
    // clears a favourite id.
    public static bool NotifyGearDestroyed(string id) => Remove(id);

    // R1-01 (#10): safe reconciliation. Removes ONLY favourite ids whose
    // equipment no longer exists in ANY live container. `allLiveIds` MUST be
    // the UNION of the loadout ids and the warehouse ids; passing a single
    // container here would be incorrect (that was the C-01 defect). Live
    // favourites in either container are always preserved. Idempotent.
    public static int PruneStale(IEnumerable<string> allLiveIds)
    {
        if (ids.Count == 0) return 0;
        var live = new HashSet<string>(allLiveIds ?? Array.Empty<string>(), StringComparer.Ordinal);
        var stale = ids.Where(id => !live.Contains(id)).ToArray();
        foreach (var id in stale) ids.Remove(id);
        return stale.Length;
    }

    // R1-01 (#3/#4/#6/#9): SCOPED batch-organisation guard. `beforeIds` and
    // `afterIds` are the id sets of the ONE container being reorganised
    // (SortBag -> bag only; SortWarehouse -> warehouse only). A favourite is
    // relevant to this operation ONLY if it was present in that container's
    // BEFORE set; such an id must survive into the AFTER set. Favourites that
    // live in a DIFFERENT container are not in `beforeIds` and therefore never
    // cause a false rejection. Sorting never removes ids and never clears a
    // favourite, so the usual result is simply "all in-scope ids preserved".
    public static bool BatchPreservesFavourites(IEnumerable<string> beforeIds,
                                                IEnumerable<string> afterIds)
    {
        if (ids.Count == 0) return true;
        var before = new HashSet<string>(beforeIds ?? Array.Empty<string>(), StringComparer.Ordinal);
        var after = new HashSet<string>(afterIds ?? Array.Empty<string>(), StringComparer.Ordinal);
        foreach (var id in ids)
            if (before.Contains(id) && !after.Contains(id)) return false;
        return true;
    }
}
