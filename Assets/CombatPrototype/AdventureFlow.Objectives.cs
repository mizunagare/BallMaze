using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

// UX-PROGRESSION-01 P1 · settlement snapshot for the objective card and the
// "next three things" block. Everything here is derived once, before the world is
// unloaded, and is never persisted: it is presentation only (D-01 = pure record,
// no reward, no receipt, no new save field).
public partial class AdventureFlow
{
    [NonSerialized] public ObjectiveProgress LastObjective = new ObjectiveProgress();
    [NonSerialized] public ObjectiveSnapshot LastSnapshot;
    [NonSerialized] public string[] NextSteps = new string[0];
    public bool HasObjectiveSnapshot => NextSteps != null && NextSteps.Length > 0;

    void CaptureObjectives(AdventureOutcome outcome)
    {
        var snap = ObjectiveEvaluator.Live(session);
        snap.settledSuccess = AdventureRules.Success(outcome);
        LastSnapshot = snap;
        LastObjective = ObjectiveEvaluator.Evaluate(snap, snap.settledSuccess);
        NextSteps = BuildNextSteps(snap, LastObjective);
    }

    string[] BuildNextSteps(ObjectiveSnapshot snap, ObjectiveProgress p)
    {
        var lines = new List<string>(3);
        // 1) crafting gap, straight from the existing target tracker
        var target = Profile?.craftingTarget;
        if (CraftingTargets.Valid(target))
        {
            var needs = CraftingTargets.Needs(session).Where(n => n.Missing > 0).ToArray();
            lines.Add(needs.Length == 0
                ? "缺口：材料已齐 · " + CraftingTargets.Name(target) + "（回营在工作台制作）"
                : "缺口：" + string.Join(" ", needs.Take(2).Select(n => PlayerInventory.Label(n.kind) + " 缺" + n.Missing)) +
                  " · " + CraftingTargets.Name(target));
        }
        else lines.Add("缺口：未设置制造目标 · 去制作页挑一件，路线页会按缺口排序");

        // 2) what this run left unfinished, measured from the same snapshot
        int unopened = Math.Max(0, snap.treasureTotal - snap.treasureUsed);
        int living = Math.Max(0, snap.enemyTotal - snap.enemiesDead);
        string aim = string.IsNullOrEmpty(p.cardId) ? "本局无目标卡" : p.title + " " + p.line2;
        lines.Add("未竟：" + aim + " · 未开宝箱 " + unopened + "/" + snap.treasureTotal + " · 剩余敌人 " + living);

        // 3) deterministic next-run suggestion (no RNG, no new scoring)
        lines.Add("下一步：" + Suggest(snap, p));
        return lines.ToArray();
    }

    static string Suggest(ObjectiveSnapshot snap, ObjectiveProgress p)
    {
        if (string.IsNullOrEmpty(snap.cardId)) return "森林 · 满载而归";
        // Conditions met but the extraction failed (death / abandon): the objective is
        // still unachieved, so "switch to another goal" would contradict the badge right
        // above it. Only the extraction itself is missing, and it is one attempt away.
        if (p.conditionsMet && !p.achieved)
            return "再来一次 " + p.regionLabel + " · " + p.title + "（条件已满足，只差成功撤离）";
        if (!p.conditionsMet)
        {
            int deficit = Math.Max(0, p.primaryRequired - p.primaryCurrent);
            // A single blocking unit is worth one more attempt; otherwise rotate.
            bool near = (p.primaryLabel == "宝箱" && deficit <= 1) || (p.primaryLabel != "宝箱" && deficit <= 4);
            if (near) return "再来一次 " + p.regionLabel + " · " + p.title + "（差 " + deficit + "）";
        }
        var card = ObjectiveCatalog.For(snap.region, snap.goal);
        if (card == null) return "森林 · 满载而归";
        var nextGoal = (ExpeditionGoal)(((int)snap.goal + 1) % 3);
        var next = ObjectiveCatalog.For(snap.region, nextGoal);
        if (next != null) return p.regionLabel + " · " + next.title + "（换一种目标）";
        var region = snap.region == ObjectiveCatalog.Forest ? ObjectiveCatalog.Cavern
            : snap.region == ObjectiveCatalog.Cavern ? ObjectiveCatalog.Ruins : ObjectiveCatalog.Forest;
        var fallback = ObjectiveCatalog.Of(region).FirstOrDefault();
        return fallback == null ? "森林 · 满载而归" : ObjectiveCatalog.RegionLabel(region) + " · " + fallback.title;
    }

    public string ObjectiveBadge => LastObjective == null || string.IsNullOrEmpty(LastObjective.cardId)
        ? "目标：未记录（世界已卸载，本页仅显示结算）"
        : LastObjective.achieved ? "目标达成 · " + LastObjective.line1
        : LastObjective.conditionsMet ? "目标条件已满足但未成功撤离 · " + LastObjective.line1
        : "目标未达成 · " + LastObjective.line1 + " " + LastObjective.line2;
}
