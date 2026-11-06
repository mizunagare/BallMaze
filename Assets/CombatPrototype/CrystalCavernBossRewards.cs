using System;
using System.Linq;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class CrystalCavernBossRewards
{
    public const string First = "c24.special.crystal-warden-first";
    public static bool Enabled(RunState run) => run!=null && run.region==CrystalCavernLayout.Region &&
        run.contentRevision==CrystalCavernLayout.Content24 && run.generationVersion==CrystalCavernLayout.Generation24 &&
        CrystalCavernLayout.HasBoss(run.checkpoint?.forest);
    public static void Drop(CombatEnemy enemy)
    {
        var session=UnityEngine.Object.FindObjectsByType<CombatSession>(FindObjectsSortMode.None)
            .Single(s=>s.gameObject.scene==enemy.gameObject.scene);
        var run=session.Flow.ActiveRun;
        if(!Enabled(run)||!CrystalCavernBossRules.Exact(run.checkpoint.forest,enemy)||!enemy.Health.Dead)
            throw new InvalidOperationException("晶脊守望者死亡来源不匹配");
        string identity=CrystalCavernLayout.Content24+"/"+run.runId+"/"+run.regionInstanceId+"/"+run.seed+"/"+enemy.entityId;
        uint Number(string suffix)=>Convert.ToUInt32(RuinsExploration.Hash(identity+suffix).Substring(0,8),16);
        var position=enemy.transform.position;
        int quality=(int)(Number("/quality")%100);
        var type=new[]{GearType.TwinBlades,GearType.Greatsword,GearType.Scythe}[Number("/type")%3];
        var gear=NewWeaponRegistry.Create(type,quality<50?GearQuality.White:quality<90?GearQuality.Green:GearQuality.Purple,identity+"/gear");
        // Freeze gameplay before publishing any member. CaptureLegacy retries this same
        // deterministic batch if construction failed; stable IDs prevent partial duplicates.
        session.Flow.QueueRuinsBossCheckpoint();
        LootPickup Existing(string suffix) => UnityEngine.Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None)
            .SingleOrDefault(p=>p.gameObject.scene==enemy.gameObject.scene&&p.InteractionId=="c24:"+RuinsExploration.Hash(identity+suffix).Substring(0,32));
        void Place(LootPickup loot,string suffix)
        {
            loot.RestoreInteractionId("c24:"+RuinsExploration.Hash(identity+suffix).Substring(0,32));
            SceneManager.MoveGameObjectToScene(loot.gameObject,enemy.gameObject.scene);
        }
        if(Existing("/ore")==null)
            Place(LootPickup.Spawn(MaterialKind.Ore,2+(int)(Number("/ore")%3),position+Vector3.up*.6f+Vector3.left),"/ore");
        if(Existing("/crystal")==null)
            Place(LootPickup.Spawn(MaterialKind.CrystalShard,3+(int)(Number("/crystal")%3),position+Vector3.up*.6f+Vector3.right),"/crystal");
        if(Existing("/gear")==null)
            Place(LootPickup.SpawnGear(gear,position+Vector3.up+Vector3.back),"/gear");
        bool firstEarnedThisDeath=RuinsSpecialRewards.Earn(session.Flow.Profile,run,First);
        session.Flow.QueueRuinsBossCheckpoint();
        session.Flow.QueueCavernBossNotice(firstEarnedThisDeath);
    }
}
