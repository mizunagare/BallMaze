using System;
using System.Collections;
using System.IO;
using System.Linq;
using UnityEngine;

public sealed partial class C1Probe
{
    string SpecialSignature() => string.Join("|", (s.Flow.Profile.specialRewards ?? Array.Empty<SpecialRewardReceipt>())
        .OrderBy(r => r.specialRewardId).Select(r => JsonUtility.ToJson(r)));

    IEnumerator ReturnRoute()
    {
        string[] ids = { RuinsSpecialRewards.Artifact, RuinsSpecialRewards.Chronicle, RuinsSpecialRewards.Seal, RuinsSpecialRewards.GateKey };
        Check("four-physical-events-award-permanent-identities", ids.All(id => RuinsSpecialRewards.Earned(s.Flow.Profile, id)));
        Check("artifact-is-distinct-from-ordinary-ground-loot", s.Flow.Profile.pending.Any(p => p.pendingId == RuinsSpecialRewards.PendingId(RuinsSpecialRewards.Artifact)) &&
            !LootSignature().Contains(RuinsSpecialRewards.Artifact));
        var layout = s.GetComponent<ForestRegionRuntime>().Layout;
        for (int i = 4; i >= 0; i--)
            yield return Go(layout.points[i].position);
        Check("actual-return-through-five-areas", Vector3.Distance(s.hero.transform.position, layout.points[0].position) < .8f);
    }

    IEnumerator RewardResume(bool guardian)
    {
        var expected = JsonUtility.FromJson<Expected>(File.ReadAllText(Root + "/expected.json"));
        string id = guardian ? RuinsSpecialRewards.Guardian : RuinsSpecialRewards.Artifact;
        string pendingId = RuinsSpecialRewards.PendingId(id);
        FreezeOthers();
        Check("fresh-process-same-run-special-and-loot", s.Flow.ActiveRun.ruinsR1 && s.Flow.ActiveRun.runId == expected.run &&
            SpecialSignature() == expected.special && LootSignature() == expected.loot &&
            JsonUtility.ToJson(s.Flow.ActiveRun.randomStreams) == expected.streams);
        if (guardian)
        {
            var boss = s.enemies.Single(e => e.entityId == "c1:guardian");
            Check("fresh-process-guardian-already-dead", boss.Health.Dead);
            boss.DropLootOnce();
            Check("repeated-death-no-new-ordinary-or-special", SpecialSignature() == expected.special && LootSignature() == expected.loot);
        }
        for (int i = 0; i < 2; i++)
        {
            Check("product-reload-" + i, s.Saves.LoadProgress(false));
            yield return null;
            FreezeOthers();
            Check("reload-no-new-special-or-ordinary-" + i, SpecialSignature() == expected.special && LootSignature() == expected.loot);
        }
        var exit = s.GetComponent<ForestRegionRuntime>().Layout.exits[guardian ? 1 : 0];
        yield return Go(exit.position);
        Check("actual-extract-start", s.Flow.BeginExtraction(exit.id));
        s.Flow.CancelExtraction("controlled cancel");
        Check("actual-extract-restart", s.Flow.BeginExtraction(exit.id));
        yield return Wait(() => s.Flow.HasResult, 12);
        Check("actual-extract-pending", s.Flow.HasResult && s.Flow.Settlement.outcome == AdventureOutcome.Extracted);
        Check("actual-commit", s.Flow.CommitSettlement());
        string saved = JsonUtility.ToJson(s.Flow.Profile);
        Check("same-commit-idempotent", s.Flow.CommitSettlement() && saved == JsonUtility.ToJson(s.Flow.Profile));
        Check("actual-ack", s.Flow.AcknowledgeSettlement() && s.Flow.AtCamp);
        yield return null;

        Check("special-pending-cannot-be-discarded", !s.Flow.DiscardPending(pendingId) && s.Flow.Profile.pending.Any(p => p.pendingId == pendingId));
        s.hero.Inventory.SetOpen(true);
        bool claimed;
        try
        {
            s.Saves.WriteValidationHook = phase => { if (phase == "before-publish") throw new IOException("C1R1_EXPECTED_CLAIM_BEFORE_PUBLISH"); };
            claimed = s.Flow.ClaimPending(pendingId, true);
        }
        finally { s.Saves.WriteValidationHook = null; }
        Check("claim-failure-rolls-back-receipt-warehouse-pending", !claimed &&
            !s.Flow.Profile.specialRewards.Single(r => r.specialRewardId == id).claimed &&
            !s.Camp.Items.Any(i => i.id == id + ".gear") && s.Flow.Profile.pending.Any(p => p.pendingId == pendingId));
        try
        {
            s.Saves.WriteValidationHook = phase => { if (phase == "after-publish") throw new IOException("C1R1_EXPECTED_CLAIM_AFTER_PUBLISH"); };
            claimed = s.Flow.ClaimPending(pendingId, true);
        }
        finally { s.Saves.WriteValidationHook = null; }
        Check("claim-confirmed-after-publish", claimed && !s.Flow.Profile.pending.Any(p => p.pendingId == pendingId) &&
            s.Camp.Items.Count(i => i.id == id + ".gear") == 1);
        Check("claim-cannot-repeat", !s.Flow.ClaimPending(pendingId, true));
        Check("claim-reload", s.Saves.LoadProgress(false));
        yield return null;
        Check("claim-durable-with-warehouse-item", s.Flow.Profile.specialRewards.Single(r => r.specialRewardId == id).claimed &&
            s.Camp.Items.Count(i => i.id == id + ".gear") == 1);
        yield return Depart();
        FreezeOthers();
        Check("fresh-run-keeps-permanent-receipt", s.Flow.ActiveRun.runId != expected.run && RuinsSpecialRewards.Earned(s.Flow.Profile, id));
        yield return Interact("c1:plaza-chest");
        Check("fresh-run-ordinary-chest-drops", LootSignature().Length > 0);
        string ordinary = LootSignature();
        Check("same-chest-retry-no-drops", !Point("c1:plaza-chest").Interact(s.hero) && ordinary == LootSignature());
        if (!guardian)
        {
            yield return Interact("c1:lever");
            yield return Interact("c1:door");
            yield return Interact("c1:archive");
            yield return Interact("c1:hidden");
            Check("new-run-artifact-is-not-reissued", !s.Flow.Profile.pending.Any(p => p.pendingId == pendingId) &&
                s.Flow.Profile.specialRewards.Count(r => r.specialRewardId == id) == 1);
        }
        s.Flow.OpenAbandon();
        Check("actual-abandon", s.Flow.ConfirmAbandon());
        yield return Wait(() => s.Flow.HasResult, 8);
        Check("abandon-settlement-preserves-permanent-reward", s.Flow.HasResult && s.Flow.CommitSettlement() &&
            s.Flow.Profile.specialRewards.Any(r => r.specialRewardId == id && r.claimed));
    }
}
