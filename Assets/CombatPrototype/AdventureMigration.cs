using System;
using System.Collections.Generic;
using System.Linq;
public static class AdventureMigration
{
    public static void UpgradeV7(CombatSaveData data)
    {
        if(!data.hasActiveRun)return;var run=data.activeRun;AdventureFlow.UpgradeRunMetadata(run,true);
        if(run.phase==RunPhase.Extracting){run.phase=RunPhase.Running;run.extractionRemaining=0;}
    }
    public static void Normalize(CombatSaveData data,int version)
    {
        if(data==null||version<3)return;
        var recover=new List<PendingReward>();var gear=(data.gear??new GearItem[0]).ToList();
        foreach(var item in gear.ToArray())if(item!=null&&Missing(item)){gear.Remove(item);recover.Add(Pending(item));}
        var warehouse=(data.warehouseGear??new GearItem[0]).ToList();foreach(var item in warehouse.ToArray())if(item!=null&&Missing(item)){warehouse.Remove(item);recover.Add(Pending(item));}
        if(recover.Count>0){foreach(string id in new[]{"rig_standard","bag_standard"}){var d=AdventureCatalog.Container(id);if(!gear.Any(i=>i.worn&&i.type==d.type)){var replacement=AdventureItems.NewContainer(id);replacement.worn=true;gear.Add(replacement);}}}
        // A valid item with an invalid anchor moves to visible migration storage, never deleted.
        var rig=gear.FirstOrDefault(i=>i!=null&&i.worn&&i.type==GearType.ChestRig);var bag=gear.FirstOrDefault(i=>i!=null&&i.worn&&i.type==GearType.Backpack);var occupied=new HashSet<string>();
        if(rig!=null&&bag!=null)foreach(var item in gear){if(item==null||item.worn||item.overflow)continue;var definition=AdventureCatalog.Container(item.board?rig.definitionId:bag.definitionId);bool valid=item.x>=0&&item.y>=0&&item.rotation>=0&&item.rotation<4;var cells=valid?item.Cells(item.rotation).Select(p=>new UnityEngine.Vector2Int(p.x+item.x,p.y+item.y)).ToArray():new UnityEngine.Vector2Int[0];valid&=cells.All(p=>definition.Allows(p.x,p.y)&&!occupied.Contains(item.board+":"+p.x+":"+p.y));if(valid)foreach(var p in cells)occupied.Add(item.board+":"+p.x+":"+p.y);else{item.overflow=true;item.board=false;item.x=item.y=-1;}}
        data.gear=gear.ToArray();data.warehouseGear=warehouse.ToArray();data.migrationRecovery=recover.ToArray();
        if(!gear.Any(i=>i!=null&&i.id==data.mainWeapon&&i.Weapon&&i.InBag))data.mainWeapon=gear.FirstOrDefault(i=>i!=null&&i.Weapon&&i.InBag)?.id;
        if(!gear.Any(i=>i!=null&&i.id==data.reserveWeapon&&i.Weapon&&i.InBag)||data.mainWeapon==data.reserveWeapon)data.reserveWeapon=null;
    }
    static bool Missing(GearItem item)=>AdventureCatalog.Item(item.definitionId)==null||item.Container&&AdventureCatalog.Container(item.definitionId)==null;
    static PendingReward Pending(GearItem item)=>new PendingReward{pendingId="legacy-recovery:"+item.id,reason="迁移恢复：缺失物品或容器模板（补回模板后可取回）",sourceRunId="legacy",equipment=true,item=item.Clone()};
}
