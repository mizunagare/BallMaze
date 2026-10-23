using UnityEngine;
public static class AdventureInventoryView
{
    static int craftType, craftQuality;
    public static void Draw(PlayerInventory bag, ThirdPersonHero hero, float x, float y, bool crafting)
    {
        if(crafting) Crafting(bag,hero,hero.GetComponent<AdventureLoadout>(),x,y);
        else ContainerInventoryView.Draw(bag,hero,x,y);
    }
    public static void DrawIcon(Rect r,string key,Color tint){var tex=AdventureItems.Texture(key);if(tex==null)return;var old=GUI.color;GUI.color=tint;GUI.DrawTexture(r,tex,ScaleMode.ScaleToFit,true);GUI.color=old;}    static void Crafting(PlayerInventory bag,ThirdPersonHero hero,AdventureLoadout gear,float x,float y)
    {
        CombatUI.Text(new Rect(x,y,540,28),"打造装备",23,CombatUI.Gold,true);
        for(int i=0;i<9;i++){
            var r=new Rect(x+(i%3)*142,y+45+(i/3)*80,130,70);
            if(CombatUI.Button(r,"",true,craftType==i))craftType=i;
            DrawIcon(new Rect(r.x+7,r.y+9,44,44),AdventureItems.Icon((GearType)i),Color.white);
            CombatUI.Text(new Rect(r.x+55,r.y+22,74,30),AdventureItems.TypeName((GearType)i),18);
        }
        float dx=x+465;var q=(GearQuality)craftQuality;var type=(GearType)craftType;var sample=new GearItem{type=type,quality=q,definitionId=AdventureCatalog.GearIds[(int)type]};sample.FreezeNewStats();
        for(int i=0;i<5;i++)if(CombatUI.Button(new Rect(dx+i*112,y+5,104,34),new[]{"白色","绿色","紫色","金色","红色"}[i],true,craftQuality==i))craftQuality=i;
        DrawIcon(new Rect(dx,y+65,90,90),AdventureItems.Icon(type),AdventureItems.Color(q));
        CombatUI.Text(new Rect(dx+112,y+65,400,35),sample.Name,25,AdventureItems.Color(q),true);
        CombatUI.Text(new Rect(dx+112,y+105,400,65),$"攻击 +{sample.Attack:0.#}    防御 +{sample.Defense:0.#}\n占用 {sample.Size.x}×{sample.Size.y} 格",20);
        CombatUI.Text(new Rect(dx,y+190,550,68),"消耗："+gear.Recipe(q),19);
        if(CombatUI.Button(new Rect(dx+380,y+151,160,32),"追踪材料"))CraftingTargets.Select(hero,type,q);
        bool can=gear.CanCraft(type,q);
        if(type<=GearType.Bow)CombatUI.Text(new Rect(dx,y+320,580,42),"新武器随机词缀：白色 0 条，绿 / 紫 1 条，金 / 红 2 条。\n紫色起解锁专属技能，可在“双武器与词缀”页查看和铭刻。",16,CombatUI.Muted);
        bool advanced=AdventureRecipes.Advanced(q);var blueprint=AdventureRecipes.Gear(type,q);var camp=AdventureRecipes.Camp(hero);
        string label=advanced&&(camp==null||!camp.Knows(blueprint!=null?blueprint.recipeId:null))?"配方未解锁":advanced&&!camp.InCamp?"需在营地工作台制造":can?"制作并放入背包":"材料或背包空间不足";
        if(CombatUI.Button(new Rect(dx,y+270,260,44),label,can))gear.Craft(type,q);
        if(advanced&&CombatUI.Button(new Rect(dx+272,y+270,240,44),"前往工作台 / 解锁")){CampInventoryView.OpenWorkbench(type,q);bag.OpenPage(PlayerInventory.Page.Camp);}
        CombatUI.Text(new Rect(x,y+300,405,60),$"木材 {bag.Count(MaterialKind.Wood)}  石头 {bag.Count(MaterialKind.Stone)}  铁矿 {bag.Count(MaterialKind.Ore)}\n晶石 {bag.Count(MaterialKind.CrystalShard)}  核心 {bag.Count(MaterialKind.BossCore)}",18,CombatUI.Muted);
        DrawIcon(new Rect(x,y+370,44,44),"potion",Color.white);
        CombatUI.Text(new Rect(x+55,y+365,390,55),$"回血药水 ×{bag.HealthPotionCount}\n每瓶消耗：野怪皮 1 + 晶石碎片 1",17);
        if(CombatUI.Button(new Rect(dx,y+370,158,38),"制作 1 瓶",bag.CanCraftPotions(1)))bag.CraftPotions();
        if(CombatUI.Button(new Rect(dx+170,y+370,158,38),"制作 5 瓶",bag.CanCraftPotions(5)))bag.CraftPotions(5);
        if(CombatUI.Button(new Rect(dx+340,y+370,158,38),"使用药水",bag.HealthPotionCount>0))bag.UseHealthPotion();
    }
}



