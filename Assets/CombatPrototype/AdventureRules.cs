using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
// Pure planning: no scene writes, RNG, inventory mutation, or file access.
public static class AdventureRules
{
    public static void Spend(int[] brought,int[] earned,int kind,int count)
    {
        if(kind<0||kind>=6||count<=0||brought[kind]+earned[kind]<count)throw new InvalidOperationException("材料来源账目不足");
        int fromEarned=Math.Min(earned[kind],count);earned[kind]-=fromEarned;brought[kind]-=count-fromEarned;
    }
    public static bool Success(AdventureOutcome outcome)=>outcome==AdventureOutcome.Extracted||outcome==AdventureOutcome.TestChallengeComplete;
    public static SettlementRecord Plan(ProfileState original,RunState run,CombatCheckpoint world,AdventureOutcome outcome)
    {
        if(original.committedRuns.Contains(run.runId))throw new InvalidOperationException("本次冒险已结算");
        bool success=Success(outcome);var profile=AdventureData.Clone(original);var record=new SettlementRecord{runId=run.runId,settlementId=run.runId+":terminal",outcome=outcome,legacyProtection=run.legacyProtected};
        var entries=new HashSet<string>(run.entryGear.Select(i=>i.id));var owned=world.gear.ToDictionary(i=>i.id);
        var returned=run.entryGear.Select(originalItem=>{
            GearItem item=success&&owned.ContainsKey(originalItem.id)?owned[originalItem.id].Clone():originalItem.Clone();
            item.x=originalItem.x;item.y=originalItem.y;item.rotation=originalItem.rotation;item.board=originalItem.board;item.worn=originalItem.worn;item.overflow=originalItem.overflow;return item;
        }).ToArray();
        var earned=world.gear.Where(i=>!entries.Contains(i.id)).Select(i=>i.Clone()).ToArray();
        record.returnedGear=returned.Select(i=>i.Clone()).ToArray();record.keptGear=success?earned:new GearItem[0];record.lostGear=success?new GearItem[0]:earned;
        record.returnedMaterials=(int[])run.broughtRemaining.Clone();record.keptMaterials=success?(int[])run.earnedRemaining.Clone():new int[6];record.lostMaterials=success?new int[6]:(int[])run.earnedRemaining.Clone();
        record.returnedPotions=success?world.potions:run.broughtPotions;record.lostPotions=success?0:run.earnedPotions;record.lostLevel=Math.Max(0,world.level-1);record.clearedSkills=(int[])world.skills.Clone();
        var warehouse=profile.warehouse.ToList();var pending=profile.pending.ToList();
        foreach(var item in record.keptGear){var copy=item.Clone();copy.x=copy.y=-1;copy.worn=copy.board=copy.overflow=false;
            if(warehouse.Count<CampRuntime.Capacity)warehouse.Add(copy);else pending.Add(new PendingReward{pendingId=record.settlementId+":"+copy.id,sourceRunId=run.runId,reason="结算装备溢出",equipment=true,item=copy});}
        for(int k=0;k<6;k++){int amount=record.keptMaterials[k],room=CampRuntime.MaterialLimit-profile.materials[k],deposit=Math.Min(room,amount);profile.materials[k]+=deposit;if(amount>deposit)pending.Add(new PendingReward{pendingId=record.settlementId+":material:"+k,sourceRunId=run.runId,reason="结算材料溢出",material=(MaterialKind)k,amount=amount-deposit});}
        if(success){var recipes=new HashSet<string>(profile.unlockedRecipes);foreach(string id in run.pendingRecipeProofs){var definition=AdventureRecipes.Find(id);while(definition!=null){recipes.Add(definition.recipeId);definition=AdventureRecipes.Find(definition.prerequisiteId);}}record.permanentUnlocks=recipes.Except(profile.unlockedRecipes).ToArray();profile.unlockedRecipes=recipes.OrderBy(i=>i).ToArray();}
        profile.warehouse=warehouse.ToArray();profile.pending=pending.ToArray();profile.committedRuns=profile.committedRuns.Concat(new[]{run.runId}).ToArray();
        var camp=AdventureData.Clone(world);camp.gear=returned;camp.materials=(int[])run.broughtRemaining.Clone();camp.potions=record.returnedPotions;camp.potionCooldown=camp.dodgeCooldown=camp.weaponSkillCooldown=camp.weaponAttackCooldown=camp.weaponSwitchCooldown=0;
        camp.level=1;camp.experience=0;camp.skills=new int[6];camp.offers=new int[0];camp.rewards=new string[0];camp.health=100;camp.heroPosition=new Vector3(0,.1f,-7);camp.heroYaw=0;camp.cameraYaw=0;camp.cameraPitch=28;
        camp.wave=1;camp.enemies=new SavedEnemy[0];camp.events=new SavedWorldEvent[0];camp.loot=new SavedLoot[0];camp.resources=new SavedResource[0];camp.waitingForWave=false;camp.waveRemaining=0;camp.randomStateJson="";
        camp.mainWeapon=returned.Any(i=>i.id==world.mainWeapon&&i.Weapon&&i.InBag)?world.mainWeapon:run.entryMain;camp.reserveWeapon=returned.Any(i=>i.id==world.reserveWeapon&&i.Weapon&&i.InBag)?world.reserveWeapon:run.entryReserve;
        if(!returned.Any(i=>i.id==camp.mainWeapon&&i.Weapon&&i.InBag))camp.mainWeapon=returned.FirstOrDefault(i=>i.Weapon&&i.InBag)?.id;
        if(!returned.Any(i=>i.id==camp.reserveWeapon&&i.Weapon&&i.InBag)||camp.mainWeapon==camp.reserveWeapon)camp.reserveWeapon=null;
        profile.hasCamp=true;profile.camp=camp;record.plan=profile;return record;
    }
}
