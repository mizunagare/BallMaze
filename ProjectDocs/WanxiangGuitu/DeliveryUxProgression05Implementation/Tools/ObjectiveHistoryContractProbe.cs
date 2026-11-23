#if UX05_HISTORY_CONTRACT_PROBE
using System;
using System.IO;
using System.Linq;
using UnityEngine;

internal static class ObjectiveHistoryContractProbe
{
    [Serializable] sealed class Result
    {
        public string status, error;
        public bool capacity, frozenTime, replay, wire, invalidTime, retiredMapping;
    }

    internal static void RunIfRequested()
    {
        var args = Environment.GetCommandLineArgs();
        if (Array.IndexOf(args, "-ux05-contract-probe") < 0) return;
        var root = ValidationStorage.Root(args, true);
        var result = new Result {status="FAIL"};
        try
        {
            var parent = new ProfileState
            {
                objectiveHistory=Enumerable.Range(0,128).Select(i=>Row("old-"+i)).ToArray(),
                committedRuns=Enumerable.Range(0,128).Select(i=>"old-"+i).ToArray()
            };
            var next = Row("new-129");
            next.committedAtUtc = null;
            var pending = new SettlementRecord
            {
                runId=next.runId,settlementId=next.SettlementId, outcome=AdventureOutcome.Extracted,
                plan=AdventureData.Clone(parent)
            };
            pending.plan.committedRuns=parent.committedRuns.Concat(new[]{next.runId}).ToArray();
            AdventureRules.FreezeHistoryCandidate(parent,pending,next);
            result.capacity=parent.objectiveHistory.Length==128 &&
                parent.objectiveHistory[0].runId=="old-0" && pending.plan.objectiveHistory.Length==128 &&
                pending.plan.objectiveHistory[0].runId=="old-1" &&
                pending.plan.objectiveHistory[127].runId==next.runId &&
                pending.plan.committedRuns.Contains("old-0") && pending.plan.committedRuns.Length==129;
            var restored=AdventureData.Clone(pending);
            var duringRetry=Row(next.runId);
            duringRetry.committedAtUtc=null;
            AdventureRules.FreezeHistoryCandidate(parent,restored,duringRetry);
            result.frozenTime=ObjectiveHistoryEntry.ValidTime(next.committedAtUtc) &&
                restored.plan.objectiveHistory[127].committedAtUtc==next.committedAtUtc &&
                duringRetry.committedAtUtc==null;
            try
            {
                AdventureRules.Plan(restored.plan,new RunState {runId="old-0"},null,AdventureOutcome.Extracted);
            }
            catch (InvalidOperationException){result.replay=true;}

            var data=new CombatSaveData { profile=restored.plan };
            string json=JsonUtility.ToJson(data);
            SaveSchemaMigration.VerifyHistoryWire(json,data);
            bool rejected=false;
            try { SaveSchemaMigration.VerifyHistoryWire(json.Replace("\"displayNameSnapshot\"","\"forgedSnapshot\""),data); }
            catch (InvalidDataException) {rejected=true;}
            result.wire=rejected && data.profile.objectiveHistory[127].displayNameSnapshot=="固定名称";
            result.invalidTime=!ObjectiveHistoryEntry.ValidTime(null) &&
                !ObjectiveHistoryEntry.ValidTime("2026-11-19T09:03:00.0000000+00:00") &&
                !ObjectiveHistoryEntry.ValidTime("2026-02-30T09:03:00.0000000Z");
            result.retiredMapping=ObjectiveCatalog.HistoricalCompletionType("ruins.challenge")=="ChallengeBoss" &&
                ObjectiveCatalog.HistoricalCompletionType("forest.challenge")=="Challenge" &&
                ObjectiveCatalog.HistoricalCompletionType("other.unknown")==null;
            if (result.capacity && result.frozenTime && result.replay && result.wire &&
                result.invalidTime && result.retiredMapping) result.status="PASS";
        }
        catch (Exception e){result.error=e.ToString();}
        File.WriteAllText(Path.Combine(root,"contract-result.json"),JsonUtility.ToJson(result,true));
        Application.Quit(result.status=="PASS"?0:1);
    }

    static ObjectiveHistoryEntry Row(string id) => new ObjectiveHistoryEntry
    {
        runId=id,objectiveId="forest.gather",regionId="ForestRuins",displayNameSnapshot="固定名称",
        completedAtUtc="2026-11-19T09:00:00.0000000Z",committedAtUtc="2026-11-19T09:01:00.0000000Z"
    };
}
#endif

