using System;
using System.Linq;
using UnityEngine;
public partial class AdventureFlow
{
    public static int SupplyCount(int[] materials,int potions,int materialStack=99,int potionStack=5){long used=(potions+(long)potionStack-1)/Math.Max(1,potionStack);foreach(int n in materials)used+=(n+(long)materialStack-1)/Math.Max(1,materialStack);return (int)Math.Min(int.MaxValue,used);}
    public int SupplyUsed()=>SupplyCount(Enumerable.Range(0,6).Select(i=>session.hero.Inventory.Count((MaterialKind)i)).ToArray(),session.hero.Inventory.HealthPotionCount,ActiveRun?.materialStack??materialStack,ActiveRun?.potionStack??potionStack);
    public int SupplyLimit=>ActiveRun?.supplySlots??Math.Max(1,supplySlots);
    public static void UpgradeRunMetadata(RunState run,bool allowExistingCapacity){
        run.regionInstanceId=run.runId+":ForestRuins:1";run.contentRevision="B05-1";run.materialStack=99;run.potionStack=5;run.supplySlots=allowExistingCapacity?Math.Max(6,SupplyCount(run.checkpoint.materials,run.checkpoint.potions)):6;
        foreach(var item in run.entryGear){item.origin=run.legacyProtected?ItemOrigin.LegacyProtected:ItemOrigin.DeploymentProtected;item.originRunId=run.runId;}
        foreach(var item in run.checkpoint.gear){item.origin=run.entryGear.Any(e=>e.id==item.id)?(run.legacyProtected?ItemOrigin.LegacyProtected:ItemOrigin.DeploymentProtected):ItemOrigin.RunLoot;item.originRunId=run.runId;}
    }
    void InitializeRunMetadata(RunState run,bool legacy){UpgradeRunMetadata(run,legacy);if(!legacy){run.materialStack=Math.Max(1,materialStack);run.potionStack=Math.Max(1,potionStack);run.supplySlots=Math.Max(1,supplySlots);}foreach(var item in session.hero.GetComponent<AdventureLoadout>().items){item.origin=run.legacyProtected?ItemOrigin.LegacyProtected:ItemOrigin.DeploymentProtected;item.originRunId=run.runId;}}
    public string SourceLabel(GearItem item){if(ActiveRun==null)return "营地资产";if(Protects(item.id))return ActiveRun.legacyProtected?"旧档保护 · 本局归还":"入场保护 · 失败归还";return "本局战利品 · 死亡丢失";}
    public static string GoalLabel(ExpeditionGoal goal)=>new[]{"采集制造","寻宝构筑","讨伐测试目标"}[(int)goal];
}
public partial class PlayerInventory
{
    public bool CanCarryDelta(MaterialKind kind,int amount){var flow=Flow;if(flow==null||!flow.Tracking)return true;int[] counts=Enumerable.Range(0,6).Select(i=>Count((MaterialKind)i)).ToArray();counts[(int)kind]+=amount;return AdventureFlow.SupplyCount(counts,healthPotions,flow.ActiveRun.materialStack,flow.ActiveRun.potionStack)<=flow.SupplyLimit;}
    bool CanCarryCraftedPotions(int count){var flow=Flow;if(flow==null||!flow.Tracking)return true;int[] counts=Enumerable.Range(0,6).Select(i=>Count((MaterialKind)i)).ToArray();counts[0]=Math.Max(0,counts[0]-count);counts[1]=Math.Max(0,counts[1]-count);return AdventureFlow.SupplyCount(counts,healthPotions+count,flow.ActiveRun.materialStack,flow.ActiveRun.potionStack)<=flow.SupplyLimit;}
    public string SupplyLabel {get{var flow=Flow;return flow!=null&&flow.Enabled?$"素材/药水堆栈 {flow.SupplyUsed()}/{flow.SupplyLimit} 格 · 材料 {flow.ActiveRun?.materialStack??flow.materialStack}/药水 {flow.ActiveRun?.potionStack??flow.potionStack} 每堆":"材料与药水（自动堆叠，不占装备格）";}}
}
