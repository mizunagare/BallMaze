using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

// UX-PROGRESSION-01 P1-03 · structured presentation of the EXISTING route score.
// No new weight, no re-sort, no extra draw: the order is literally
// RouteScoring.Ranked(...) and every number printed here already exists on
// RouteEvaluation.
public static class RouteCards
{
    public static string Reason(string code) => code == "NO_PATH" ? "无通行路径"
        : code == "NO_USABLE_EXIT" ? "没有可用撤离出口"
        : code == "TARGET_MISMATCH" ? "与当前目标不匹配"
        : code == "NO_TREASURE_REMAINING" ? "没有剩余宝箱"
        : code == "NO_ENCOUNTER_REMAINING" ? "没有剩余遭遇"
        : code == "NO_REMAINING_YIELD" ? "没有可预期收益"
        : code == "MISSING_REPAIR_MATERIALS" ? "修复材料不足"
        : code == "NO_EXIT_PATH" ? "出口不可达"
        : code == "NO_INTERACTION_APPROACH" ? "无法靠近交互点"
        : "条件不满足";

    public static string RiskLabel(RouteEvaluation e) => e.risk.pathElites > 0 ? "高"
        : e.risk.destinationEnemies > 0 ? "中" : "低";

    public static string ExitLabel(RouteEvaluation e)
    {
        if (e.exits == null || e.exits.Length == 0) return "—";
        var exit = e.exits.FirstOrDefault(x => x.id == e.chosenExit) ?? e.exits.FirstOrDefault(x => x.usable);
        if (exit == null) return "无可用出口";
        string tail = exit.availability == "FREE" ? "免费" : exit.availability == "REPAIRED" ? "已修" : "需修";
        return exit.label + "(" + tail + ")";
    }

    public static RouteEvaluation[] Top(CombatSession s, int count = 3) =>
        RouteScoring.Ranked(RouteScoring.Evaluate(s)).Take(count).ToArray();

    public static string[] Top3Ids(CombatSession s) => Top(s).Select(e => e.poiId).ToArray();
    public static string[] RankedIds(CombatSession s) => RouteScoring.Ranked(RouteScoring.Evaluate(s)).Select(e => e.poiId).ToArray();

    public static string[] Cards(CombatSession s)
    {
        var top = Top(s);
        var lines = new List<string>();
        string[] marks = { "①", "②", "③" };
        for (int i = 0; i < top.Length; i++)
        {
            var e = top[i];
            lines.Add(marks[i] + " " + e.label + " · 匹配 " + e.targetMatch.ToString("0.00") +
                      " · 风险 " + RiskLabel(e) + " · 撤离 " + ExitLabel(e) +
                      " · 评分 " + e.totalScore.ToString("0.00") + (i == 0 ? "   ← 推荐" : ""));
        }
        return lines.ToArray();
    }

    // Only what the existing evaluation already flagged, localised.
    public static string[] Excluded(CombatSession s)
    {
        var all = RouteScoring.Evaluate(s).Where(e => !e.eligible).OrderBy(e => e.poiId, StringComparer.Ordinal);
        return all.Select(e => e.label + " · " + string.Join("/", (e.exclusionReasons ?? new string[0]).Select(Reason))).ToArray();
    }

    // Full block for the existing 路线 detail page. Header shows the same objective
    // card the HUD shows so the two never disagree.
    public static string Page(CombatSession s)
    {
        var run = s.Flow?.ActiveRun;
        var progress = run != null && ObjectiveCatalog.IsRegion(run.region)
            ? ObjectiveEvaluator.Evaluate(ObjectiveEvaluator.Live(s)) : null;
        var text = new List<string>();
        text.Add("[本局目标] " + (progress == null ? "未选择目标" : progress.line1 + " · " + progress.line2));
        var cards = Cards(s);
        text.Add("[路线 Top3] 顺序与 RouteScoring.Ranked 一致，未新增权重");
        text.AddRange(cards.Length == 0 ? new[] { "当前没有满足条件的路线；可查看下方地点详情或直接去免费出口。" } : cards);
        var excluded = Excluded(s);
        if (excluded.Length > 0) text.Add("[不可用] " + string.Join("；", excluded));
        return string.Join("\n", text);
    }
}
