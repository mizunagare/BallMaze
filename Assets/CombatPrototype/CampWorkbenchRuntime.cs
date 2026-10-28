using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
public partial class CampRuntime
{
    readonly HashSet<string> unlockedRecipes=new HashSet<string>();
    public bool CanUseWorkbench=>Ready;
    public int AvailableMaterial(MaterialKind kind)=>session.hero.Inventory.Count(kind)+(Ready?materials[(int)kind]:0);
    internal void PayMaterials(IEnumerable<MaterialStack> costs)
    {
        var total=costs.GroupBy(c=>c.material).Select(g=>new MaterialStack{material=g.Key,amount=g.Sum(c=>c.amount)}).ToArray();
        if(!Ready||total.Any(c=>c.amount<0||AvailableMaterial(c.material)<c.amount))throw new InvalidOperationException("营地材料不足或状态未就绪");
        foreach(var c in total){int fromBag=Math.Min(session.hero.Inventory.Count(c.material),c.amount);if(!session.hero.Inventory.TryRemove(c.material,fromBag)&&fromBag>0)throw new InvalidOperationException("随身材料发生变化");materials[(int)c.material]-=c.amount-fromBag;}
    }
    public string[] CaptureRecipes()=>unlockedRecipes.OrderBy(id=>id).ToArray();
    public bool Knows(string id)=>id!=null&&unlockedRecipes.Contains(id);
    public void RestoreRecipes(string[] ids){unlockedRecipes.Clear();if(ids!=null)foreach(string id in ids)unlockedRecipes.Add(id);}
    public void MigrateRecipes(IEnumerable<GearItem> owned)
    {
        unlockedRecipes.Clear();
        foreach(var item in owned){
            var recipe=item.Container?AdventureRecipes.Container(item.definitionId):AdventureRecipes.Gear(item.type,item.quality);
            while(recipe!=null){if(!unlockedRecipes.Add(recipe.recipeId))break;recipe=AdventureRecipes.Find(recipe.prerequisiteId);}
        }
    }
    public string UnlockReason(CraftingRecipeDefinition recipe)
    {
        if(recipe==null)return "缺少配方数据。";
        if(Knows(recipe.recipeId))return "配方已永久解锁。";
        if(!Ready)return "请先回营，并确认存档状态正常。";
        if(!string.IsNullOrEmpty(recipe.prerequisiteId)&&!Knows(recipe.prerequisiteId))return AdventureRecipes.Find(recipe.prerequisiteId)!=null?"需要先解锁："+AdventureRecipes.Find(recipe.prerequisiteId).displayName:"缺少前置配方数据。";
        if(recipe.unlockCost.Any(c=>AvailableMaterial(c.material)<c.amount))return "背包与营地仓库材料不足。";
        return "";
    }
    public bool UnlockRecipe(string id)
    {
        var recipe=AdventureRecipes.Find(id);if(recipe==null||Knows(id)||UnlockReason(recipe)!="")return false;
        bool success=Commit(()=>{PayMaterials(recipe.unlockCost);unlockedRecipes.Add(id);});
        if(success)session.hero.Inventory.NotifyMessage("已永久解锁："+recipe.displayName);return success;
    }
    public bool Manufacture(GearType type,GearQuality quality)
    {
        var gear=session.hero.GetComponent<AdventureLoadout>();if(!Ready||!gear.CanCraft(type,quality))return false;
        bool success=Commit(()=>{if(!gear.CraftNow(type,quality))throw new InvalidOperationException("材料或背包空间不足");Onboarding.Crafted(session);});
        if(success)session.hero.Inventory.NotifyCategorized("已制作："+AdventureItems.QualityName(quality)+AdventureItems.TypeName(type)+"；消耗 "+CraftingCosts.Text(CraftingCosts.Gear(quality))+"（随身优先）；产物已入背包并保存。","craft");return success;
    }
    public bool ManufactureContainer(string id)
    {
        var gear=session.hero.GetComponent<AdventureLoadout>();if(!Ready||!gear.CanCraftContainer(id))return false;
        bool success=Commit(()=>{if(!gear.CraftContainerNow(id))throw new InvalidOperationException("材料或背包空间不足");Onboarding.Crafted(session);});
        if(success)session.hero.Inventory.NotifyCategorized("已制作："+AdventureCatalog.Container(id).displayName+"；消耗 "+CraftingCosts.Text(CraftingCosts.Container(id))+"（随身优先）；产物已入背包并保存。","craft");return success;
    }
    public bool ChangeContainer(GearItem item){var gear=session.hero.GetComponent<AdventureLoadout>();if(!Ready||!gear.PreviewContainer(item,out _,out _))return false;return Commit(()=>{if(!gear.EquipContainerNow(item))throw new InvalidOperationException("容器预览已变化");});}
    public bool ManufacturePotions(int quantity){if(!Ready||!session.hero.Inventory.CanCraftPotions(quantity))return false;return Commit(()=>{if(!session.hero.Inventory.CraftPotionsNow(quantity))throw new InvalidOperationException("药水材料或容量已变化");Onboarding.Crafted(session);});}
}

