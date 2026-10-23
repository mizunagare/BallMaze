using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
public static class AdventureValidation
{
    static void Need(bool b){if(!b)throw new System.IO.InvalidDataException("冒险存档边界或来源账目不合法");}
    static void Counts(int[] a){Need(a!=null&&a.Length==6&&a.All(v=>v>=0&&v<=CampRuntime.MaterialLimit));}
    static void Recipes(string[] a){Need(a!=null&&a.Length<=1024&&a.Distinct().Count()==a.Length);foreach(string id in a){var r=AdventureRecipes.Find(id);if(r==null)throw new NotSupportedException("缺少配方定义："+id);Need(string.IsNullOrEmpty(r.prerequisiteId)||a.Contains(r.prerequisiteId));}}
    static HashSet<string> Profile(ProfileState p)
    {
        Need(p!=null&&!string.IsNullOrEmpty(p.profileId)&&p.warehouse!=null&&p.warehouse.Length<=200&&p.pending!=null&&p.pending.Length<=4096);Counts(p.materials);Recipes(p.unlockedRecipes);
        Need(p.committedRuns!=null&&p.committedRuns.Length<=100000&&p.committedRuns.All(id=>!string.IsNullOrEmpty(id))&&p.committedRuns.Distinct().Count()==p.committedRuns.Length&&p.badges!=null&&p.regions!=null);
        var ids=new HashSet<string>();foreach(var i in p.warehouse){CombatSaveSystem.ValidateCurrentItem(i);Need(!i.worn&&!i.board&&!i.overflow&&i.x==-1&&i.y==-1&&ids.Add(i.id));}
        var pendingIds=new HashSet<string>();foreach(var pending in p.pending){Need(pending!=null&&!string.IsNullOrEmpty(pending.pendingId)&&pendingIds.Add(pending.pendingId)&&!string.IsNullOrEmpty(pending.reason));if(pending.equipment){Loose(pending.item);Need(ids.Add(pending.item.id));}else Need((int)pending.material>=0&&(int)pending.material<6&&pending.amount>0&&pending.amount<=CampRuntime.MaterialLimit);}
        if(p.hasCamp){Need(p.camp!=null);Inventory(p.camp);foreach(var i in p.camp.gear)Need(ids.Add(i.id));}
        return ids;
    }
    static void Loose(GearItem i){Need(i!=null&&!string.IsNullOrEmpty(i.id)&&i.id.Length<=64&&(int)i.type>=0&&(int)i.type<=10&&(int)i.quality>=0&&(int)i.quality<=4&&i.dataRevision==1&&!float.IsNaN(i.savedAttack)&&!float.IsInfinity(i.savedAttack)&&!float.IsNaN(i.savedDefense)&&!float.IsInfinity(i.savedDefense));}
    static void Inventory(CombatCheckpoint c)
    {
        Counts(c.materials);Need(c.gear!=null&&c.gear.Length>=2&&c.gear.Length<=1024&&c.potions>=0&&c.potions<=99);CombatSaveSystem.ValidateContainers(c);
    }
    public static void Validate(CombatSaveData data,bool current=true)
    {
        Need(data!=null&&data.revision>0);var ids=Profile(data.profile);
        var run=data.hasActiveRun?data.activeRun:null;var record=data.hasSettlement?data.settlement:null;
        if(run!=null){
            Need(!data.profile.hasCamp&&!string.IsNullOrEmpty(run.runId)&&!data.profile.committedRuns.Contains(run.runId)&&(int)run.mode>=0&&(int)run.mode<=2&&(int)run.phase>=0&&(int)run.phase<=2&&run.region=="ForestRuins"&&run.targetWave>=5&&run.targetWave<=100000&&run.checkpoint!=null);
            if(current){Need(!string.IsNullOrEmpty(run.regionInstanceId)&&(run.contentRevision=="B05-1"||run.contentRevision=="B06-1"||run.contentRevision=="B06-A1"||run.contentRevision=="B06-B1"||run.contentRevision=="B06-B2")&&(int)run.goal>=0&&(int)run.goal<=2&&run.supplySlots>=1&&run.materialStack>=1&&run.potionStack>=1);Need(AdventureFlow.SupplyCount(run.checkpoint.materials,run.checkpoint.potions,run.materialStack,run.potionStack)<=run.supplySlots);foreach(var i in run.checkpoint.gear){bool entry=run.entryGear.Any(e=>e.id==i.id);Need(i.originRunId==run.runId&&i.origin==(entry?(run.legacyProtected?ItemOrigin.LegacyProtected:ItemOrigin.DeploymentProtected):ItemOrigin.RunLoot));}}
            Need((run.mode==AdventureMode.ForestExploration)==run.checkpoint.forestWorld);if(run.checkpoint.forestWorld&&run.phase==RunPhase.Extracting)Need(run.checkpoint.forest.exits.Any(e=>e.id==run.exitId));
            if(run.checkpoint.forestWorld)foreach(var exit in run.checkpoint.forest.exits)if(exit.repaired)Need(exit.repairReceipt==run.runId+":"+run.regionInstanceId+":"+exit.id);
            Counts(run.broughtRemaining);Counts(run.earnedRemaining);Need(run.entryGear!=null&&run.entryGear.Length<=1024&&run.entryGear.Select(i=>i.id).Distinct().Count()==run.entryGear.Length&&run.pendingRecipeProofs!=null);
            foreach(var entry in run.entryGear){CombatSaveSystem.ValidateCurrentItem(entry);Need(!ids.Contains(entry.id));}
            var c=AdventureData.Clone(run.checkpoint);if(run.phase==RunPhase.OutcomePending&&c.health==0)c.health=1;CombatSaveSystem.Validate(c,4);
            foreach(var i in run.checkpoint.gear)Need(ids.Add(i.id));foreach(var loot in run.checkpoint.loot)if(loot.equipment)Need(ids.Add(loot.gear.id));
            for(int k=0;k<6;k++)Need(run.broughtRemaining[k]+run.earnedRemaining[k]==run.checkpoint.materials[k]);
            Need(run.broughtPotions>=0&&run.earnedPotions>=0&&run.broughtPotions+run.earnedPotions==run.checkpoint.potions&&run.extractionRemaining>=0&&run.extractionRemaining<=3600);
        }else Need(data.profile.hasCamp&&data.profile.camp!=null);
        if(record!=null){
            Need(record.settlementId==record.runId+":terminal"&&(int)record.outcome>=0&&(int)record.outcome<=3&&(int)record.status>=0&&(int)record.status<=1&&record.plan!=null);Profile(record.plan);Need(record.plan.committedRuns.Contains(record.runId));
            if(record.status==SettlementStatus.Pending)Need(run!=null&&run.runId==record.runId&&run.phase==RunPhase.OutcomePending&&!data.profile.committedRuns.Contains(record.runId)&&!record.acknowledged);
            else Need(data.profile.committedRuns.Contains(record.runId)&&run==null);
            Counts(record.returnedMaterials);Counts(record.keptMaterials);Counts(record.lostMaterials);
        }
        if(run!=null&&run.phase==RunPhase.OutcomePending)Need(record!=null&&record.status==SettlementStatus.Pending);
    }
}
