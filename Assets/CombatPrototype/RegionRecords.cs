using System;
using System.Linq;

// A detached presentation of a published Profile. No writes, inventory inference or RNG.
public sealed class RegionRecordView
{
    public readonly string regionId, title, coverage;
    public readonly string[] records, recent, revisit;
    public RegionRecordView(string id, string[] records, string[] recent, string[] revisit, string coverage)
    { regionId=id; title=ObjectiveCatalog.RegionLabel(id); this.records=records; this.recent=recent; this.revisit=revisit; this.coverage=coverage; }
}

public static class RegionRecords
{
    static readonly string[] RuinsIds = { RuinsSpecialRewards.Artifact, RuinsSpecialRewards.Guardian,
        RuinsSpecialRewards.Chronicle, RuinsSpecialRewards.Seal, RuinsSpecialRewards.GateKey };
    public const string Gaps = "探索总次数 / 成功撤离总次数 / 终身最高纪录：暂无可用记录";
    public const string Retention = "最近保留的目标记录 · 全地区合计最多 128 条；更早记录可能已裁剪，不代表永久进度倒退。";

    public static ObjectiveHistoryEntry[] RetainedHistory(ProfileState published,string region=null)
    {
        if(published==null)throw new ArgumentNullException(nameof(published));
        return (published.objectiveHistory??Array.Empty<ObjectiveHistoryEntry>())
            .Where(e=>region==null || e.regionId==region)
            .OrderByDescending(e=>e.completedAtUtc,StringComparer.Ordinal)
            .ThenByDescending(e=>e.committedAtUtc,StringComparer.Ordinal)
            .ThenBy(e=>e.runId,StringComparer.Ordinal).ThenBy(e=>e.SettlementId,StringComparer.Ordinal)
            .ThenBy(e=>e.objectiveId,StringComparer.Ordinal).ToArray();
    }
    public static RegionRecordView Query(ProfileState published, string region)
    {
        if (published==null || !ObjectiveCatalog.IsRegion(region)) throw new ArgumentException("地区档案来源不可用");
        var history=RetainedHistory(published,region);
        string[] records;
        if(region==ObjectiveCatalog.Forest)
        {
            records=new[]{ForestBossKind.Warden,ForestBossKind.Tide}.Select(k=>
            {
                var row=ForestBossRules.Find(published,k);
                bool badge=(published.badges??Array.Empty<string>()).Contains(ForestBossRules.Id(k));
                return ForestBossRules.Name(k)+"：已记录讨伐 "+(row?.kills??0)+" 次 · 纪念徽章"+(badge?"已记录":"暂无记录");
            }).Concat(new[]{"双首领纪念："+((published.badges??Array.Empty<string>()).Contains("forest:dual-hunt")?"已记录":"暂无记录"),
                "拔点也可由精英达成，目标记录不等于指定首领击杀次数。"}).ToArray();
        }
        else records=(region==ObjectiveCatalog.Ruins?RuinsIds:new[]{CrystalCavernBossRewards.First})
            .Select(id=>RewardLine(published,id)).ToArray();
        string direction=region==ObjectiveCatalog.Forest?"可复访森林宝箱、材料矿点与两名可选首领；纪念仅为记录。":
            region==ObjectiveCatalog.Ruins?"可沿机关、石门、碑文到密室，或挑战守护者；待领取装备仍在营地原领取入口。":
            "可采集矿晶、开启矿室与回程桥机关，或挑战晶脊守望者；守望者已有双刃、大剑、镰刀掉落。";
        return new RegionRecordView(region,records,
            history.Take(3).Select(e=>e.displayNameSnapshot+" · "+e.completedAtUtc+" · Run "+e.runId).ToArray(),
            new[]{direction}.Concat(ObjectiveCatalog.Of(region).Select(c=>c.title+"："+c.oneLine)).ToArray(),
            Retention+(published.objectiveHistoryLegacyUnknown?" 旧版目标历史未知，不能视为未完成。":"")+
            (history.Length==0?" 当前没有保留的该地区目标记录。":" 当前保留该地区 "+history.Length+" 条。"));
    }

    static string RewardLine(ProfileState profile,string id)
    {
        var receipt=(profile.specialRewards??Array.Empty<SpecialRewardReceipt>()).SingleOrDefault(r=>r.specialRewardId==id);
        return RuinsSpecialRewards.Label(id)+"："+(receipt==null?"暂无获得记录":
            receipt.claimed?"已记录 · 已领取":"已记录 · 待领取（营地领取入口）");
    }
}
