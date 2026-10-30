using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

[Serializable] public class CraftingTarget { public GearType type; public GearQuality quality; public string containerId; }
public static class CraftingCosts
{
    public static int Available(ThirdPersonHero hero,MaterialKind kind){var camp=AdventureRecipes.Camp(hero);return camp!=null&&camp.CanUseWorkbench?camp.AvailableMaterial(kind):hero.Inventory.Count(kind);}
    public static bool CanPay(ThirdPersonHero hero,IEnumerable<MaterialStack> costs){var camp=AdventureRecipes.Camp(hero);if(camp!=null&&camp.InCamp&&!camp.CanUseWorkbench)return false;return costs.GroupBy(c=>c.material).All(g=>g.Sum(c=>c.amount)<=Available(hero,g.Key));}
    public static void Pay(ThirdPersonHero hero,IEnumerable<MaterialStack> costs){var camp=AdventureRecipes.Camp(hero);if(camp!=null&&camp.InCamp){camp.PayMaterials(costs);return;}if(!CanPay(hero,costs))throw new InvalidOperationException("材料已变化");foreach(var c in costs)if(!hero.Inventory.TryRemove(c.material,c.amount))throw new InvalidOperationException("材料扣除失败");}
    public static MaterialStack[] Gear(GearQuality quality){int n=(int)quality+1;return new[]{S(MaterialKind.Wood,n*2),S(MaterialKind.Stone,n),S(MaterialKind.Ore,n*2),S(MaterialKind.CrystalShard,n-1),S(MaterialKind.BossCore,Math.Max(0,n-3))}.Where(s=>s.amount>0).ToArray();}
    public static MaterialStack[] Container(string id){var d=AdventureCatalog.Container(id);return d==null?new MaterialStack[0]:new[]{S(MaterialKind.Wood,d.woodCost),S(MaterialKind.MonsterHide,d.hideCost),S(MaterialKind.Ore,d.oreCost)}.Where(s=>s.amount>0).ToArray();}
    static MaterialStack S(MaterialKind m,int n)=>new MaterialStack{material=m,amount=n};
    public static string Text(IEnumerable<MaterialStack> costs)=>string.Join(" · ",costs.Select(s=>PlayerInventory.Label(s.material)+" ×"+s.amount));
}
public class CraftingNeed { public MaterialKind kind; public int required,bag,warehouse; public int Missing=>Math.Max(0,required-bag-warehouse); }
public static class CraftingTargets
{
    public static bool Valid(CraftingTarget t)=>t!=null&&(string.IsNullOrEmpty(t.containerId)?(int)t.type>=0&&(int)t.type<9&&(int)t.quality>=0&&(int)t.quality<=4:AdventureCatalog.Container(t.containerId)!=null);
    public static CraftingRecipeDefinition Recipe(CraftingTarget t)=>string.IsNullOrEmpty(t.containerId)?AdventureRecipes.Gear(t.type,t.quality):AdventureRecipes.Container(t.containerId);
    public static string Name(CraftingTarget t)=>!Valid(t)?"未标记制造目标":!string.IsNullOrEmpty(t.containerId)?AdventureCatalog.Container(t.containerId).displayName:AdventureItems.QualityName(t.quality)+AdventureItems.TypeName(t.type);
    public static MaterialStack[] Costs(CraftingTarget t)=>!Valid(t)?new MaterialStack[0]:string.IsNullOrEmpty(t.containerId)?CraftingCosts.Gear(t.quality):CraftingCosts.Container(t.containerId);
    public static CraftingNeed[] Needs(CombatSession s)
    {
        var t=s.Flow.Profile?.craftingTarget;if(!Valid(t))return new CraftingNeed[0];var amounts=new int[6];
        foreach(var c in Costs(t))amounts[(int)c.material]+=c.amount;
        // Include each still-locked prerequisite once, separately from manufacturing itself.
        var seen=new HashSet<string>();var r=Recipe(t);
        while(r!=null&&seen.Add(r.recipeId)){if(!s.Camp.Knows(r.recipeId))foreach(var c in r.unlockCost)amounts[(int)c.material]+=c.amount;r=AdventureRecipes.Find(r.prerequisiteId);}
        return Enumerable.Range(0,6).Where(i=>amounts[i]>0).Select(i=>new CraftingNeed{kind=(MaterialKind)i,required=amounts[i],bag=s.hero.Inventory.Count((MaterialKind)i),warehouse=s.Camp.Materials[i]}).ToArray();
    }
    public static bool Select(ThirdPersonHero hero,GearType type,GearQuality quality,string container=null)
    {
        var s=Owner(hero);var target=new CraftingTarget{type=type,quality=quality,containerId=container};
        if(s?.Flow.Profile==null||s.Flow.HasResult||s.Flow.Frozen||!Valid(target))return false;
        var old=s.Flow.Profile.craftingTarget;
        if(Valid(old)&&old.type==target.type&&old.quality==target.quality&&(old.containerId??"")== (target.containerId??"")&&!s.Saves.SaveFailed)return true;
        s.Flow.Profile.craftingTarget=target;bool saved=s.Saves.SaveProgress(false);
        hero.Inventory.NotifyMessage(saved?"已追踪："+Name(target)+" · "+PlayerInput.Key(PlayerAction.Route)+" 查看缺口与地点":"目标已选择，保存失败；请重试保存。不会扣材料。");return saved;
    }
    static CraftingTarget Untracked()=>new CraftingTarget{type=(GearType)(-1),quality=GearQuality.White,containerId=""};
    public static bool Clear(ThirdPersonHero hero){var s=Owner(hero);if(s?.Flow.Profile==null||s.Flow.HasResult||s.Flow.Frozen)return false;s.Flow.Profile.craftingTarget=Untracked();return s.Saves.SaveProgress(false);}
    public static CombatSession Owner(ThirdPersonHero hero)=>UnityEngine.Object.FindObjectsByType<CombatSession>(FindObjectsSortMode.None).FirstOrDefault(s=>s.hero==hero);
    // Called inside the same manufacturing transaction as consumption and product creation.
    // A one-shot target ends with an explicit inactive value in the existing v9 field; no reward/history is invented.
    public static bool Matches(CombatSession s,GearType type,GearQuality quality,string container=null){var t=s?.Flow?.Profile?.craftingTarget;return Valid(t)&&t.type==type&&t.quality==quality&&(t.containerId??"")== (container??"");}
    public static bool Manufactured(CombatSession s,GearType type,GearQuality quality,string container=null){if(!Matches(s,type,quality,container))return false;s.Flow.Profile.craftingTarget=Untracked();return true;}
    static string TargetStatus(CombatSession s,CraftingTarget t){if(!s.Saves.CanCommitWarehouse||s.Saves.SaveFailed)return "保存异常 / 待核对，请先恢复存档";var r=Recipe(t);if(r!=null&&AdventureRecipes.Advanced(t.quality)&&!s.Camp.Knows(r.recipeId))return "未解锁 · 含前置研究费用";if(!s.Camp.InCamp)return "材料已齐 · 回营制作";if(!s.Camp.CanUseWorkbench)return "材料已齐 · 打开营地工作台";var g=s.hero.GetComponent<AdventureLoadout>();return (string.IsNullOrEmpty(t.containerId)?g.CanCraft(t.type,t.quality):g.CanCraftContainer(t.containerId))?"可制作 · 工作台完成后结束追踪":"材料已齐 · 检查背包空间/状态";}
    public static string Compact(CombatSession s){var t=s.Flow.Profile?.craftingTarget;if(!Valid(t))return "";var missing=Needs(s).Where(n=>n.Missing>0).ToArray();return Name(t)+"\n"+(missing.Length>0?PlayerInventory.Label(missing[0].kind)+" -"+missing[0].Missing+(missing.Length>1?" 等"+missing.Length+"项":""):TargetStatus(s,t));}
    public static string Details(CombatSession s)
    {
        var t=s.Flow.Profile?.craftingTarget;if(!Valid(t))return "在制作页或工作台选择“追踪材料”。\n"+GoalFeedback(s)+"\n"+Recommendations(s);
        string text=Name(t)+"（含未解锁前置配方费用）\n"+string.Join("\n",Needs(s).Select(n=>$"{PlayerInventory.Label(n.kind)}：随身{n.bag} / 仓库{n.warehouse} / 需求{n.required} · 缺{n.Missing}"));
        return text+"\n"+TargetStatus(s,t)+"\n营地工作台统一使用随身与仓库材料；本局随身收益尚未安全入仓。\n"+GoalFeedback(s)+"\n"+Recommendations(s);
    }
    public static string Recommendations(CombatSession s)
    {
        var region=s.GetComponent<ForestRegionRuntime>();var layout=region?.Layout;
        if(layout==null)return "出征森林后，按实际未耗尽资源、宝箱、遭遇与路线推荐地点。";
        var needs=Needs(s).Where(n=>n.Missing>0).Select(n=>n.kind).ToArray();var lines=new List<string>();
        var evaluations=RouteScoring.Evaluate(s);var ranked=RouteScoring.Ranked(evaluations);
        foreach(var evaluation in ranked) {
            string materials=string.Join("/",Enumerable.Range(0,6).Where(i=>evaluation.expectedMaterials[i]>0).Select(i=>PlayerInventory.Label((MaterialKind)i)));
            string gear=evaluation.groundGearCount>0?"/地面装备":evaluation.expectedGear>0?"/装备机会":"";
            string risk=evaluation.risk.pathElites>0?"途经精英警戒附近":"未见精英贴近路径";
            if(evaluation.bypassDistance>=0)risk+=" · 可绕行约"+evaluation.bypassDistance.ToString("0")+"米";
            var exit=evaluation.exits.Single(e=>e.id==evaluation.chosenExit);
            string escape=exit.label+(exit.requiresRepair?"（需修：木"+exit.repairWood+"石"+exit.repairStone+"）":exit.availability=="REPAIRED"?"（已修）":"（免费）");
            lines.Add(evaluation.label+"（余敌"+evaluation.livingEnemies+"）："+materials+gear+
                " · 余：采集"+evaluation.remainingNodes+" 箱"+evaluation.unopenedChests+" 地面"+evaluation.groundGroups+"组"+
                " · 导航约"+evaluation.navigationDistance.ToString("0")+"米 · "+risk+" · 撤离："+escape+" · 评分"+evaluation.totalScore.ToString("0"));
        }
        if(needs.Contains(MaterialKind.BossCore)){
            bool liveBoss=s.enemies.Any(e=>!e.Health.Dead&&e.GetComponent<ForestBossBrain>()!=null);
            bool groundCore=UnityEngine.Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Any(l=>l.gameObject.scene==s.gameObject.scene&&!l.Collected&&l.Gear==null&&l.Kind==MaterialKind.BossCore);
            lines.Add(liveBoss||groundCore?"领主核心：森林首领为可选挑战；已掉落核心需拾取，当前可达来源见路线。可绕行或免费撤离。":layout.bossVersion>0?"领主核心：当前森林已无可见来源；可继续探索或免费撤离。":"领主核心：当前旧布局无森林首领来源；可选波次首领挑战，普通撤离不需要核心。");
        }
        string summary="仅表示材料倾向，具体随机装备不保证；撤离以当前出口条件为准。";
        if(ranked.Length==0)summary=!evaluations.Any(e=>e.reachable)?"暂无完整导航路径，不提供有效推荐。":!evaluations.Any(e=>e.reachable&&e.exitAvailable)?"当前没有可用撤离路径（出口不可达或修复材料不足），暂无有效推荐。":"当前地点无匹配剩余来源；可查看已验证出口条件再决定撤离。";
        return string.Join("\n",lines)+"\n"+summary;
    }
    public static bool At(ForestLayout layout,Vector3 position,string id)=>layout.points.OrderBy(p=>(p.position-position).sqrMagnitude).First().id==id;
    static bool RemainingGear(CombatSession s,ForestPoi poi){var layout=s.GetComponent<ForestRegionRuntime>()?.Layout;return layout!=null&&UnityEngine.Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Any(l=>l.gameObject.scene==s.gameObject.scene&&!l.Collected&&l.Gear!=null&&At(layout,l.transform.position,poi.id));}
    public static string RemainingSummary(CombatSession s,ForestPoi poi){
        var layout=s.GetComponent<ForestRegionRuntime>()?.Layout;if(layout==null)return "";
        int nodes=UnityEngine.Object.FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Count(n=>n.gameObject.scene==s.gameObject.scene&&n.Health>0&&At(layout,n.transform.position,poi.id));
        int chests=s.Events.Points.Count(e=>!e.Used&&e.Kind==WorldEventKind.Treasure&&e.entityId!=null&&e.entityId.StartsWith(poi.id+":"));
        int enemies=s.enemies.Count(e=>!e.Health.Dead&&e.GetComponent<EncounterGuard>()?.poi==poi.id);
        int ground=UnityEngine.Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Count(l=>l.gameObject.scene==s.gameObject.scene&&!l.Collected&&At(layout,l.transform.position,poi.id));
        return "余：采集"+nodes+" 箱"+chests+" 敌"+enemies+" 地面"+ground+"组";
    }
    public static MaterialKind[] Available(CombatSession s,ForestPoi poi)
    {
        var layout=s.GetComponent<ForestRegionRuntime>()?.Layout;if(layout==null)return new MaterialKind[0];var set=new HashSet<MaterialKind>();
        var alive=UnityEngine.Object.FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).Where(n=>n.gameObject.scene==s.gameObject.scene&&n.Health>0).Select(n=>n.StableId).ToHashSet();
        foreach(var node in layout.nodes.Where(n=>alive.Contains(n.id)&&layout.points.OrderBy(p=>(p.position-n.position).sqrMagnitude).First().id==poi.id))set.Add((MaterialKind)(node.kind+3));
        if(s.Events.Points.Any(p=>!p.Used&&p.Kind==WorldEventKind.Treasure&&p.entityId!=null&&p.entityId.StartsWith(poi.id+":"))){
            foreach(var m in layout.revision>=3?ForestRewards.ChestMaterials(poi.siteKind):new[]{MaterialKind.MonsterHide,MaterialKind.CrystalShard})set.Add(m);
        }
        foreach(var enemy in s.enemies.Where(e=>!e.Health.Dead&&e.GetComponent<EncounterGuard>()?.poi==poi.id)){set.Add(MaterialKind.MonsterHide);if(enemy.crystalAmount>0||layout.revision>=3&&poi.siteKind==ForestSiteKind.Outpost)set.Add(MaterialKind.CrystalShard);}
        foreach(var loot in UnityEngine.Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Where(l=>l.gameObject.scene==s.gameObject.scene&&!l.Collected&&l.Gear==null))if(layout.points.OrderBy(p=>(p.position-loot.transform.position).sqrMagnitude).First().id==poi.id)set.Add(loot.Kind);
        return set.OrderBy(m=>m).ToArray();
    }
    public static string GoalFeedback(CombatSession s){var run=s.Flow.ActiveRun;if(run==null)return "目标材料含未解锁前置费用；不会自动解锁或发奖。";
        int harvested=run.earnedRemaining.Sum(),chests=s.Events.Points.Count(e=>e.Kind==WorldEventKind.Treasure&&e.Used),defeated=s.enemies.Count(e=>e.Health.Dead);
        return run.goal==ExpeditionGoal.Gather?$"采集目标：本局仍持有材料 {harvested}；按材料缺口选地点。":run.goal==ExpeditionGoal.Treasure?$"寻宝目标：已开宝箱 {chests}；未拾取物仍在地面。":$"讨伐目标：击败 {defeated}/{s.enemies.Length}；哨站风险较高。无需清场也可撤离。";
    }
    // Legacy callers retain their signature; distance always comes from a live
    // matching world, never a graph edge sum or a fabricated straight-line value.
    public static string Route(ForestLayout layout,Vector3 from,string target) {
        var region=UnityEngine.Object.FindObjectsByType<ForestRegionRuntime>(FindObjectsSortMode.None).FirstOrDefault(r=>r.Ready&&ReferenceEquals(r.Layout,layout));
        if(region==null)return null;var result=region.NavigationRoute(from,target);var point=layout.points.FirstOrDefault(p=>p.id==target);
        return result.reachable&&point!=null?point.label+" · 导航约"+result.distance.ToString("0")+"米":null;
    }
}
