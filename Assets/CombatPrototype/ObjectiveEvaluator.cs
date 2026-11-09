using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.SceneManagement;

// UX-PROGRESSION-01 P1 · read-only objective evaluation.
//
// Frozen semantics (see DESIGN.md §3.1 / DECISIONS.md D-08):
//   GrossEarned      = everything picked up during THIS run (never carried in)
//   EarnedRemaining  = what is still held from this run (drops when spent)
//   CarriedIn        = broughtRemaining, always excluded from progress
//   Spent            = consumed this run (exit repair / potions / engraving)
//
// The product has no persisted gross signal and P1 may not add save fields, so
// gross is reconstructed as max(runtimeGross, EarnedRemaining):
//   * runtimeGross is an in-memory monotonic counter fed by AdventureFlow.GainMaterial.
//   * EarnedRemaining is the persisted fallback that survives a process restart.
// Both are <= the true gross, so the projection can never over-report (a false
// "achieved" is impossible); it can only under-report after a restart of a run in
// which materials were spent. `Exact` states which case applies.
public static class ObjectiveLedger
{
    static string runId;
    static readonly int[] gross = new int[6];
    static readonly int[] spent = new int[6];
    static int gains;
    public static string RunId => runId;
    public static int Gains => gains;
    public static bool Matches(string id) => !string.IsNullOrEmpty(id) && id == runId;
    public static void BeginRun(string id)
    {
        if (id == runId) return;
        runId = id; gains = 0;
        Array.Clear(gross, 0, gross.Length); Array.Clear(spent, 0, spent.Length);
    }
    public static void Clear() { runId = null; gains = 0; Array.Clear(gross, 0, gross.Length); Array.Clear(spent, 0, spent.Length); }
    public static void Gain(int kind, int amount) { if (kind >= 0 && kind < 6 && amount > 0) { gross[kind] += amount; gains++; } }
    public static void Spend(int kind, int amount) { if (kind >= 0 && kind < 6 && amount > 0) spent[kind] += amount; }
    public static int Gross(int kind) => kind >= 0 && kind < 6 ? gross[kind] : 0;
    public static int Spent(int kind) => kind >= 0 && kind < 6 ? spent[kind] : 0;
}

public struct ObjectiveSnapshot
{
    public string cardId, region;
    public ExpeditionGoal goal;
    public int[] gross, net, carried;
    public int treasureUsed, treasureTotal;
    public int eliteOrBossDead, enemyTotal, enemiesDead;
    public int veinsDead, veinTotal;
    public int chainDone;
    public bool lever, door, archive, hiddenChest, chamberChest, farShoreChest;
    public int guardianDead, wardenDead;
    public bool exact, fromSave;
    // Optional live-only hint used for the HUD "next step" line.
    public string nextLabel;
    public float nextDistance;
    public bool settledSuccess;
}

public sealed class ObjectiveProgress
{
    public string cardId = "", title = "", regionLabel = "", oneLine = "";
    public string line1 = "", line2 = "", line3 = "";
    public bool conditionsMet, achieved, settledSuccess, exact, fromSave;
    public int primaryCurrent, primaryRequired;
    public string primaryLabel = "", blockedReason = "";
    public int[] current = new int[0], required = new int[0];
    public override string ToString() => cardId + " " + line1 + " | " + line2 + " | " + line3 + " | met=" + conditionsMet + " achieved=" + achieved;
}

public static class ObjectiveEvaluator
{
    // Reads live world + run state. Never writes, never samples RNG.
    public static ObjectiveSnapshot Live(CombatSession s)
    {
        var snap = new ObjectiveSnapshot();
        if (s == null || s.Flow == null || s.Flow.ActiveRun == null) return snap;
        var run = s.Flow.ActiveRun;
        snap.region = run.region; snap.goal = run.goal;
        snap.cardId = ObjectiveCatalog.For(run.region, run.goal)?.id ?? "";
        snap.gross = new int[6]; snap.net = new int[6]; snap.carried = new int[6];
        bool ledger = ObjectiveLedger.Matches(run.runId);
        snap.exact = ledger && ObjectiveLedger.Gains > 0;
        for (int k = 0; k < 6; k++)
        {
            int net = run.earnedRemaining != null && k < run.earnedRemaining.Length ? run.earnedRemaining[k] : 0;
            int carried = run.broughtRemaining != null && k < run.broughtRemaining.Length ? run.broughtRemaining[k] : 0;
            snap.net[k] = net; snap.carried[k] = carried;
            snap.gross[k] = Math.Max(net, ledger ? ObjectiveLedger.Gross(k) : 0);
        }
        var events = s.Events != null ? s.Events.Points : null;
        if (events != null)
        {
            for (int i = 0; i < events.Count; i++)
            {
                var e = events[i]; if (e == null) continue;
                bool used = e.Used;
                if (e.Kind == WorldEventKind.Treasure)
                {
                    snap.treasureTotal++;
                    if (used) snap.treasureUsed++;
                }
                if (!used) continue;
                switch (e.entityId)
                {
                    case "c1:lever": snap.lever = true; break;
                    case "c1:door": snap.door = true; break;
                    case "c1:archive": snap.archive = true; break;
                    case "c1:hidden": snap.hiddenChest = true; break;
                    case "c22:chamber:chest": snap.chamberChest = true; break;
                    case "c23:far-shore:chest": snap.farShoreChest = true; break;
                }
            }
        }
        snap.chainDone = (snap.lever ? 1 : 0) + (snap.door ? 1 : 0) + (snap.archive ? 1 : 0) + (snap.hiddenChest ? 1 : 0);
        var live = s.enemies;
        if (live != null)
        {
            for (int i = 0; i < live.Length; i++)
            {
                var e = live[i]; if (e == null || e.Health == null) continue;
                snap.enemyTotal++;
                if (!e.Health.Dead) continue;
                snap.enemiesDead++;
                if (e.archetype == EnemyArchetype.Elite || e.archetype == EnemyArchetype.Boss) snap.eliteOrBossDead++;
                if (e.entityId == ObjectiveCatalog.RuinsGuardian) snap.guardianDead = 1;
                if (e.entityId == ObjectiveCatalog.CavernWarden) snap.wardenDead = 1;
            }
        }
        var nodes = UnityEngine.Object.FindObjectsByType<AdventureResource>(FindObjectsSortMode.None)
            .Where(n => n != null && n.gameObject.scene == s.gameObject.scene).ToArray();
        for (int i = 0; i < nodes.Length; i++)
        {
            snap.veinTotal++;
            if (nodes[i].Health <= 0) snap.veinsDead++;
        }
        FillNextHint(s, run, ref snap, nodes);
        return snap;
    }

    // Builds the same numbers from a persisted checkpoint only. Used after a
    // process restart and by the settlement snapshot when no live scene exists.
    public static ObjectiveSnapshot Saved(RunState run)
    {
        var snap = new ObjectiveSnapshot { fromSave = true };
        if (run == null) return snap;
        snap.region = run.region; snap.goal = run.goal;
        snap.cardId = ObjectiveCatalog.For(run.region, run.goal)?.id ?? "";
        snap.gross = new int[6]; snap.net = new int[6]; snap.carried = new int[6];
        for (int k = 0; k < 6; k++)
        {
            int net = run.earnedRemaining != null && k < run.earnedRemaining.Length ? run.earnedRemaining[k] : 0;
            int carried = run.broughtRemaining != null && k < run.broughtRemaining.Length ? run.broughtRemaining[k] : 0;
            snap.net[k] = net; snap.carried[k] = carried;
            // Conservative: only the persisted net survives a restart.
            snap.gross[k] = net;
        }
        var cp = run.checkpoint;
        if (cp == null) return snap;
        if (cp.events != null)
            for (int i = 0; i < cp.events.Length; i++)
            {
                var e = cp.events[i]; if (e == null) continue;
                if (e.kind == WorldEventKind.Treasure) { snap.treasureTotal++; if (e.used) snap.treasureUsed++; }
                if (!e.used) continue;
                switch (e.entityId)
                {
                    case "c1:lever": snap.lever = true; break;
                    case "c1:door": snap.door = true; break;
                    case "c1:archive": snap.archive = true; break;
                    case "c1:hidden": snap.hiddenChest = true; break;
                    case "c22:chamber:chest": snap.chamberChest = true; break;
                    case "c23:far-shore:chest": snap.farShoreChest = true; break;
                }
            }
        snap.chainDone = (snap.lever ? 1 : 0) + (snap.door ? 1 : 0) + (snap.archive ? 1 : 0) + (snap.hiddenChest ? 1 : 0);
        var layout = cp.forest;
        var types = new Dictionary<string, int>();
        if (layout != null && layout.encounters != null)
            foreach (var e in layout.encounters) if (e != null && !string.IsNullOrEmpty(e.id)) types[e.id] = e.type;
        if (layout != null && layout.nodes != null) snap.veinTotal = layout.nodes.Length;
        if (cp.resources != null)
            for (int i = 0; i < cp.resources.Length; i++)
                if (cp.resources[i] != null && cp.resources[i].health <= 0) snap.veinsDead++;
        if (cp.enemies != null)
            for (int i = 0; i < cp.enemies.Length; i++)
            {
                var e = cp.enemies[i]; if (e == null) continue;
                snap.enemyTotal++;
                if (e.health > 0) continue;
                snap.enemiesDead++;
                if (types.TryGetValue(e.entityId ?? "", out int type) && (type == (int)EnemyArchetype.Elite || type == (int)EnemyArchetype.Boss)) snap.eliteOrBossDead++;
                if (e.entityId == ObjectiveCatalog.RuinsGuardian) snap.guardianDead = 1;
                if (e.entityId == ObjectiveCatalog.CavernWarden) snap.wardenDead = 1;
            }
        return snap;
    }

    static void FillNextHint(CombatSession s, RunState run, ref ObjectiveSnapshot snap, AdventureResource[] nodes)
    {
        var layout = s.GetComponent<ForestRegionRuntime>()?.Layout;
        var hero = s.hero; if (hero == null) return;
        Vector3 from = hero.transform.position;
        float best = float.MaxValue; string label = null;
        System.Action<Vector3, string> consider = (p, l) =>
        {
            float d = Vector3.Distance(from, p); if (d < best) { best = d; label = l; }
        };
        var card = ObjectiveCatalog.For(run.region, run.goal);
        if (card == null || layout == null) return;
        if (run.goal == ExpeditionGoal.Gather)
        {
            foreach (var n in nodes) if (n.Health > 0) consider(n.transform.position, NearestLabel(layout, n.transform.position, "采集点"));
            if (run.region == ObjectiveCatalog.Ruins) label = null;
        }
        else if (run.goal == ExpeditionGoal.Treasure)
        {
            if (s.Events != null) foreach (var e in s.Events.Points) if (e != null && !e.Used && e.Kind == WorldEventKind.Treasure) consider(e.transform.position, e.Title);
        }
        else
        {
            foreach (var e in s.enemies)
            {
                if (e == null || e.Health == null || e.Health.Dead) continue;
                if (run.region == ObjectiveCatalog.Ruins && e.entityId != ObjectiveCatalog.RuinsGuardian) continue;
                if (run.region == ObjectiveCatalog.Cavern && e.entityId != ObjectiveCatalog.CavernWarden) continue;
                if (run.region == ObjectiveCatalog.Forest && e.archetype != EnemyArchetype.Elite && e.archetype != EnemyArchetype.Boss) continue;
                string tag = e.archetype == EnemyArchetype.Boss ? "首领" : "精英";
                consider(e.transform.position, NearestLabel(layout, e.transform.position, tag) + " · " + tag);
            }
        }
        if (label != null) { snap.nextLabel = label; snap.nextDistance = best; }
    }

    static string NearestLabel(ForestLayout layout, Vector3 position, string fallback)
    {
        if (layout == null || layout.points == null || layout.points.Length == 0) return fallback;
        var p = layout.points.OrderBy(x => (x.position - position).sqrMagnitude).First();
        return p.label;
    }

    public static ObjectiveProgress Evaluate(ObjectiveSnapshot snap) => Evaluate(snap, false);

    public static ObjectiveProgress Evaluate(ObjectiveSnapshot snap, bool settledSuccess)
    {
        var card = ObjectiveCatalog.Find(snap.cardId);
        var p = new ObjectiveProgress { cardId = snap.cardId, exact = snap.exact, fromSave = snap.fromSave };
        if (card == null)
        {
            p.title = "未选择目标"; p.regionLabel = ObjectiveCatalog.RegionLabel(snap.region);
            p.line1 = p.title + " · " + p.regionLabel; p.line2 = "—";
            p.line3 = "营地选择出征目标"; p.blockedReason = "NO_CARD";
            return p;
        }
        p.title = card.title; p.regionLabel = ObjectiveCatalog.RegionLabel(card.region); p.oneLine = card.oneLine;
        p.line1 = card.title + " · " + p.regionLabel;
        p.current = new int[card.conditions.Length]; p.required = new int[card.conditions.Length];
        bool met = true; int firstUnmet = -1;
        for (int i = 0; i < card.conditions.Length; i++)
        {
            var c = card.conditions[i];
            int cur = 0;
            switch (c.kind)
            {
                case ObjectiveConditionKind.GrossMaterial:
                    if (c.materials == null) cur = snap.gross == null ? 0 : snap.gross.Sum();
                    else foreach (int m in c.materials) cur += snap.gross != null && m < snap.gross.Length ? snap.gross[m] : 0;
                    break;
                case ObjectiveConditionKind.TreasureOpened: cur = snap.treasureUsed; break;
                case ObjectiveConditionKind.EliteOrBossKilled: cur = snap.eliteOrBossDead; break;
                case ObjectiveConditionKind.VeinDestroyed: cur = snap.veinsDead; break;
                case ObjectiveConditionKind.ChainStep: cur = snap.chainDone; break;
                case ObjectiveConditionKind.NamedEnemyDead:
                    cur = c.entityId == ObjectiveCatalog.RuinsGuardian ? snap.guardianDead
                        : c.entityId == ObjectiveCatalog.CavernWarden ? snap.wardenDead : 0;
                    break;
                case ObjectiveConditionKind.NamedChest:
                    cur = c.entityId == ObjectiveCatalog.CavernChamberChest ? (snap.chamberChest ? 1 : 0)
                        : c.entityId == ObjectiveCatalog.CavernFarChest ? (snap.farShoreChest ? 1 : 0) : 0;
                    break;
            }
            p.current[i] = cur; p.required[i] = c.required;
            if (cur < c.required) { met = false; if (firstUnmet < 0) firstUnmet = i; }
        }
        p.conditionsMet = met;
        p.achieved = met && settledSuccess;
        p.settledSuccess = settledSuccess;
        if (firstUnmet >= 0)
        {
            var c = card.conditions[firstUnmet];
            p.primaryLabel = c.label; p.primaryCurrent = p.current[firstUnmet]; p.primaryRequired = c.required;
            // L2 stays inside the 12-character budget by showing one blocking condition.
            p.line2 = c.label + " " + p.primaryCurrent + "/" + c.required;
            p.blockedReason = "差 " + (c.required - p.primaryCurrent) + " " + c.label;
        }
        else
        {
            // Met: L2 switches to "已达成 · 待撤离", so keep the numeric mirror on the
            // FIRST condition instead of leaving a stale pre-achievement value.
            var first = card.conditions[0];
            p.primaryLabel = first.label;
            p.primaryCurrent = p.current[0];
            p.primaryRequired = p.required[0];
            p.line2 = "已达成 · 待撤离";
            p.blockedReason = "";
        }
        p.line3 = NextStep(card, snap, firstUnmet);
        return p;
    }

    static string NextStep(ObjectiveCard card, ObjectiveSnapshot snap, int firstUnmet)
    {
        if (firstUnmet < 0) return "可从任意可用出口撤离";
        var c = card.conditions[firstUnmet];
        if (c.kind == ObjectiveConditionKind.ChainStep)
        {
            var todo = new[] { "转动符文机关", "开启遗迹门", "解读碑文", "开启隐藏宝箱" };
            int i = Mathf.Clamp(snap.chainDone, 0, 3);
            return "下一步：" + todo[i];
        }
        if (c.kind == ObjectiveConditionKind.NamedChest)
        {
            if (c.entityId == ObjectiveCatalog.CavernChamberChest)
                return snap.lever ? "矿室已开，深入取箱" : "先开矿室晶纹机关";
            return snap.farShoreChest ? "对岸箱已开" : "先开回程桥机关，再到对岸";
        }
        if (!string.IsNullOrEmpty(snap.nextLabel))
            return "最近：" + snap.nextLabel + " · 直线约 " + snap.nextDistance.ToString("0") + " 米";
        return card.nextHint;
    }
}
