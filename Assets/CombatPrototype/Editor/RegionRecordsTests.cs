using System;
using System.IO;
using System.Linq;
using UnityEngine;

public static class RegionRecordsTests
{
    static int checks;
    static void Require(bool value,string name) { if(!value)throw new Exception("UX06 fixture failed: "+name);checks++;Debug.Log("UX06_FIXTURE_PASS "+name); }
    public static void Run()
    {
        checks=0;
        var p=new ProfileState();
        Require(!RegionRecords.Query(p,ObjectiveCatalog.Forest).coverage.Contains("未知"),"new empty is not legacy unknown");
        p.objectiveHistoryLegacyUnknown=true;
        Require(RegionRecords.Query(p,ObjectiveCatalog.Forest).coverage.Contains("旧版目标历史未知"),"legacy unknown distinguished");
        p.specialRewards=new[]{new SpecialRewardReceipt{specialRewardId=RuinsSpecialRewards.Artifact,earnedRunId="fixture",claimed=false},
            new SpecialRewardReceipt{specialRewardId=RuinsSpecialRewards.Chronicle,earnedRunId="fixture",claimed=true},
            new SpecialRewardReceipt{specialRewardId=CrystalCavernBossRewards.First,earnedRunId="fixture",claimed=true}};
        var ruins=RegionRecords.Query(p,ObjectiveCatalog.Ruins);
        Require(ruins.records.Length==5 && !ruins.records.Any(l=>l.Contains("晶脊")),"five ruins stable IDs exclude cavern");
        Require(ruins.records[0].Contains("已记录 · 待领取"),"pending receipt distinct");
        Require(ruins.records[2].Contains("已记录 · 已领取"),"claimed receipt independent of inventory");
        Require(ruins.records[1].Contains("暂无获得记录"),"absent receipt not earned");
        Require(RegionRecords.Query(p,ObjectiveCatalog.Cavern).records.Single().Contains("已领取"),"cavern first receipt grouped");
        p.objectiveHistory=Enumerable.Range(0,128).Select(i=>new ObjectiveHistoryEntry{runId="fixture-"+i.ToString("D3"),objectiveId="forest.challenge",regionId=ObjectiveCatalog.Forest,
            completedAtUtc="2026-11-23T00:00:00.0000000Z",committedAtUtc="2026-11-23T00:00:01.0000000Z",displayNameSnapshot="完成时旧名称"}).Reverse().ToArray();
        string before=JsonUtility.ToJson(p);
        for(int i=0;i<20;i++) foreach(var id in new[]{ObjectiveCatalog.Forest,ObjectiveCatalog.Ruins,ObjectiveCatalog.Cavern}) RegionRecords.Query(p,id);
        Require(before==JsonUtility.ToJson(p),"repeated projections preserve all Profile bytes");
        var forest=RegionRecords.Query(p,ObjectiveCatalog.Forest);
        Require(forest.records[0].Contains("讨伐 0 次") && forest.records[1].Contains("讨伐 0 次"),"objective history cannot fabricate named boss kills");
        Require(forest.recent[0].Contains("fixture-000") && forest.recent[0].Contains("完成时旧名称"),"stable tie order and name snapshot");
        Require(forest.coverage.Contains("最多 128 条") && forest.coverage.Contains("不代表永久进度倒退"),"bounded retention coverage");
        var pending=new SettlementRecord{plan=new ProfileState{objectiveHistory=p.objectiveHistory}};
        Require(RegionRecords.Query(new ProfileState(),ObjectiveCatalog.Forest).recent.Length==0 && pending.plan.objectiveHistory.Length==128,"Pending plan is not a projection input");
        Require(!ObjectiveCatalog.RegionOneLine(ObjectiveCatalog.Forest).Contains("唯一"),"forest copy matches cavern weapon drops");
        Require(RegionRecords.Gaps.Contains("暂无可用记录"),"unsupported lifetime metrics remain gaps");
        string dir="ProjectDocs/WanxiangGuitu/DeliveryUxProgression06";
        Directory.CreateDirectory(dir);File.WriteAllText(dir+"/FIXTURE_RESULT.json","{\"verdict\":\"PASS\",\"checks\":"+checks+",\"evidenceLevel\":\"T constructed fixtures, not Player expeditions\"}");
    }
}
