using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

[Serializable]
public sealed class SpecialRewardReceipt
{
    public string specialRewardId;
    public string earnedRunId;
    public bool claimed;
}

// These IDs name permanent profile rewards, never a run-local drop or an inventory slot.
public static class RuinsSpecialRewards
{
    public const string Artifact = "c1.special.artifact";
    public const string Guardian = "c1.special.guardian-first";
    public const string Chronicle = "c1.special.chronicle";
    public const string Seal = "c1.special.collector-seal";
    public const string GateKey = "c1.special.gate-key";

    static readonly string[] All = { Artifact, Guardian, Chronicle, Seal, GateKey };

    public static bool Enabled(RunState run) =>
        run != null && run.ruinsR1 && run.region == RuinsLayout.Region && run.contentRevision == RuinsLayout.Content;

    static bool Equipment(string id) => id == Artifact || id == Guardian;
    static string GearId(string id) => id + ".gear";
    static GearType Type(string id) => id == Artifact ? GearType.Scythe : GearType.Greatsword;
    public static string PendingId(string id) => id + ".pending";

    public static string Label(string id)
    {
        switch (id)
        {
            case Artifact: return "回响遗镰";
            case Guardian: return "守护者初誓";
            case Chronicle: return "祭坛残卷";
            case Seal: return "石柱广场纪念印";
            case GateKey: return "符文机关钥";
            default: return "";
        }
    }

    public static string ItemLabel(string gearId)
    {
        if (gearId == GearId(Artifact)) return Label(Artifact);
        return gearId == GearId(Guardian) ? Label(Guardian) : null;
    }

    public static string ForEvent(string entityId)
    {
        switch (entityId)
        {
            case "c1:hidden": return Artifact;
            case "c1:archive": return Chronicle;
            case "c1:plaza-chest": return Seal;
            case "c1:lever": return GateKey;
            default: return null;
        }
    }

    static SpecialRewardReceipt[] Receipts(ProfileState profile) =>
        profile?.specialRewards ?? Array.Empty<SpecialRewardReceipt>();

    public static bool Earned(ProfileState profile, string id) =>
        Receipts(profile).Any(receipt => receipt.specialRewardId == id);

    public static bool IsSpecialPending(string pendingId) =>
        pendingId == PendingId(Artifact) || pendingId == PendingId(Guardian);

    // The caller publishes this mutation with the world event or guardian death in one save.
    internal static bool Earn(ProfileState profile, RunState run, string id)
    {
        if (!Enabled(run) || !All.Contains(id) || Earned(profile, id)) return false;
        bool equipment = Equipment(id);
        var receipt = new SpecialRewardReceipt { specialRewardId = id, earnedRunId = run.runId, claimed = !equipment };
        if (equipment)
        {
            var item = NewWeaponRegistry.Create(Type(id), GearQuality.Purple, profile.profileId + "/" + id);
            item.id = GearId(id);
            var pending = new PendingReward {
                pendingId = PendingId(id), sourceRunId = run.runId, reason = "永久特殊奖励 · " + Label(id),
                equipment = true, item = item
            };
            profile.pending = profile.pending.Concat(new[] { pending }).ToArray();
        }
        profile.specialRewards = Receipts(profile).Concat(new[] { receipt }).ToArray();
        return true;
    }

    // Called inside the existing camp commit, alongside inserting the gear and removing the inbox row.
    internal static void CompleteClaim(ProfileState profile, string pendingId)
    {
        if (!IsSpecialPending(pendingId)) return;
        var receipt = Receipts(profile).Single(row => PendingId(row.specialRewardId) == pendingId);
        if (receipt.claimed) throw new InvalidOperationException("特殊奖励已经领取");
        receipt.claimed = true;
    }

    public static string CollectionLabel(ProfileState profile) => string.Join(" / ",
        Receipts(profile).Where(row => row.claimed).Select(row => Label(row.specialRewardId)));

    internal static void Validate(ProfileState profile)
    {
        var ids = new HashSet<string>(StringComparer.Ordinal);
        foreach (var receipt in Receipts(profile))
        {
            if (receipt == null || !All.Contains(receipt.specialRewardId) ||
                !ids.Add(receipt.specialRewardId) || string.IsNullOrEmpty(receipt.earnedRunId))
                throw new InvalidDataException("遗迹特殊奖励回执不合法");

            string id = receipt.specialRewardId;
            var pending = profile.pending.SingleOrDefault(row => row.pendingId == PendingId(id));
            if (receipt.claimed)
            {
                if (pending != null) throw new InvalidDataException("已领取的特殊奖励仍在待领取区");
                continue;
            }

            if (!Equipment(id) || pending == null || !pending.equipment ||
                pending.sourceRunId != receipt.earnedRunId || pending.item.id != GearId(id) ||
                pending.item.type != Type(id) || pending.item.quality != GearQuality.Purple)
                throw new InvalidDataException("待领取的特殊奖励缺少匹配物品");
        }

        foreach (var pending in profile.pending.Where(row => IsSpecialPending(row.pendingId)))
            if (!ids.Any(id => PendingId(id) == pending.pendingId))
                throw new InvalidDataException("特殊奖励物品缺少永久回执");
    }

    internal static void ValidateRun(ProfileState profile, RunState run)
    {
        if (!run.ruinsR1) return;
        if (!Enabled(run) || run.checkpoint.forest.ruinsStage != 5)
            throw new InvalidDataException("遗迹 R1 奖励规则与区域不匹配");
        foreach (var point in run.checkpoint.events)
        {
            string id = ForEvent(point.entityId);
            if (point.used && id != null && !Earned(profile, id))
                throw new InvalidDataException("遗迹特殊事件缺少永久回执");
        }

        bool dead = run.checkpoint.enemies.Single(enemy => enemy.entityId == "c1:guardian").health <= 0;
        var first = Receipts(profile).SingleOrDefault(row => row.specialRewardId == Guardian);
        if (dead && first == null || !dead && first?.earnedRunId == run.runId)
            throw new InvalidDataException("遗迹守护者生命与首次奖励回执不一致");
    }
}
