using UnityEngine;
public static class WorkbenchView
{
    static GearType type;static GearQuality quality=GearQuality.Purple;static string container;
    public static GearType SelectedType=>type;public static GearQuality SelectedQuality=>quality;public static string SelectedContainer=>container;
    public static void Select(GearType t,GearQuality q,string id=null){type=t;quality=q<GearQuality.Purple?GearQuality.Purple:q;container=id;}
    public static void Draw(ThirdPersonHero hero,float x,float y)
    {
        var camp=AdventureRecipes.Camp(hero);var gear=hero.GetComponent<AdventureLoadout>();var bag=hero.Inventory;
        for(int n=0;n<3;n++)if(CombatUI.Button(new Rect(x+n*143,y,133,32),new[]{"紫色配方","金色配方","红色配方"}[n],true,(int)quality==n+2&&container==null)){quality=(GearQuality)(n+2);container=null;if((int)type>=9)type=GearType.Sword;}
        for(int n=0;n<9;n++){
            var rect=new Rect(x+n%3*143,y+44+n/3*68,133,60);
            if(CombatUI.Button(rect,"",true,container==null&&(int)type==n)){type=(GearType)n;container=null;}
            AdventureInventoryView.DrawIcon(new Rect(rect.x+5,rect.y+8,35,35),AdventureItems.Icon((GearType)n),Color.white);CombatUI.Text(new Rect(rect.x+47,rect.y+15,80,28),AdventureItems.TypeName((GearType)n),18);
        }
        string[] containers={"rig_heavy","bag_relic"};for(int n=0;n<2;n++){var d=AdventureCatalog.Container(containers[n]);if(CombatUI.Button(new Rect(x+n*216,y+254,205,32),d.displayName,true,container==containers[n])){container=containers[n];type=d.type;quality=d.quality;}}
        CombatUI.Text(new Rect(x,y+300,432,52),$"随身：铁矿 {bag.Count(MaterialKind.Ore)}  晶石 {bag.Count(MaterialKind.CrystalShard)}\n领主核心 {bag.Count(MaterialKind.BossCore)} · 营地材料合并支付，先随身后仓库",16,CombatUI.Muted);
        var recipe=container==null?AdventureRecipes.Gear(type,quality):AdventureRecipes.Container(container);float dx=x+465;
        if(recipe==null){CombatUI.Text(new Rect(dx,y+25,560,70),"缺少配方定义，暂时无法解锁或制造。",20);return;}
        if(CombatUI.Button(new Rect(dx+405,y+65,145,30),"追踪材料"))CraftingTargets.Select(hero,type,quality,container);
        bool known=camp.Knows(recipe.recipeId);AdventureInventoryView.DrawIcon(new Rect(dx,y+3,50,50),recipe.Icon,AdventureItems.Color(recipe.quality));
        CombatUI.Text(new Rect(dx+65,y,510,32),recipe.displayName,24,AdventureItems.Color(recipe.quality),true);
        CombatUI.Text(new Rect(dx+65,y+36,510,28),known?"已永久解锁 · 重开保留":"未解锁 · 先研究，再单独支付制造材料",17,known?CombatUI.Gold:CombatUI.Muted);
        CombatUI.Text(new Rect(dx,y+83,568,54),"一次性解锁："+AdventureRecipes.UnlockCost(recipe),18);
        var prerequisite=AdventureRecipes.Find(recipe.prerequisiteId);CombatUI.Text(new Rect(dx,y+142,568,46),"前置配方："+(prerequisite==null?"无":prerequisite.displayName)+"\n"+(known?"已有配方不会重复扣除解锁材料。":camp.UnlockReason(recipe)),16,CombatUI.Muted);
        string cost=container==null?gear.Recipe(recipe.quality):ContainerCost(container);
        CombatUI.Text(new Rect(dx,y+199,568,50),"每次制造："+cost,18);
        if(CombatUI.Button(new Rect(dx,y+260,240,38),known?"配方已解锁":"永久解锁配方",!known&&camp.UnlockReason(recipe)==""))camp.UnlockRecipe(recipe.recipeId);
        bool can=container==null?gear.CanCraft(type,quality):gear.CanCraftContainer(container);
        if(CombatUI.Button(new Rect(dx+253,y+260,280,38),can?"制造并存入背包":"待解锁 / 材料或空间不足",can)){if(container==null)gear.Craft(type,quality);else gear.CraftContainer(container);}
        CombatUI.Text(new Rect(dx,y+360,568,70),CraftingTargets.Compact(CraftingTargets.Owner(hero))+" · 缺口含仓库及未解锁前置费",16,CombatUI.Gold);
        CombatUI.Text(new Rect(dx,y+310,568,42),"高级装备必须在营地制造；现有掉落、宝箱和装备使用不受配方限制。",16,CombatUI.Muted);
    }
    static string ContainerCost(string id){var d=AdventureCatalog.Container(id);return $"木材 ×{d.woodCost} · 野怪皮 ×{d.hideCost} · 铁矿 ×{d.oreCost}";}
}
