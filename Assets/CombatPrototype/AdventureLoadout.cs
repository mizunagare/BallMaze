using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class AdventureLoadout : MonoBehaviour
{
    public List<GearItem> items = new List<GearItem>();
    public string mainWeapon, reserveWeapon;
    public GearItem Reserve => items.Find(i=>i.id==reserveWeapon&&i.InBag&&i.Weapon);
    public bool Carried(GearItem i)=>i!=null&&(i.id==mainWeapon||i.id==reserveWeapon);
    ThirdPersonHero hero;
    public GearItem Main => items.Find(i => i.id == mainWeapon && i.InBag && i.Weapon);
    public GearType Weapon => Main != null ? Main.type : GearType.Sword;
    IEnumerable<GearItem> Unique => items.GroupBy(i=>i.id).Select(g=>g.First());
    IEnumerable<GearItem> Active => Unique.Where(i => !i.overflow && !i.worn && (i.board || i == Main));
    public ContainerDefinition Rig => ContainerFor(items,true);
    public ContainerDefinition Bag => ContainerFor(items,false);
    public float Attack => Active.Sum(i=>i.Attack) + (Rig?.attackBonus??0) + (Bag?.attackBonus??0);
    public float Defense => Active.Where(i=>i.board).Sum(i=>i.Defense) + (Rig?.defenseBonus??0) + (Bag?.defenseBonus??0);
    public float MoveBonus => (Rig?.moveBonus??0)+(Bag?.moveBonus??0);
    public int HarvestBonus => (Rig?.harvestBonus??0)+(Bag?.harvestBonus??0);
    public int UsedCells => Unique.Where(i=>i.board&&!i.overflow&&!i.worn).Sum(i=>i.Cells(i.rotation).Count());
    public int OverflowCount => items.Count(i=>i.overflow);
    public int Width(bool board)=>Definition(board).width;
    public int Height(bool board)=>Definition(board).height;
    public ContainerDefinition Definition(bool board)=>board?Rig:Bag;
    static ContainerDefinition ContainerFor(IReadOnlyList<GearItem> list,bool board)
    {
        var type=board?GearType.ChestRig:GearType.Backpack;
        var worn=list.FirstOrDefault(i=>i.worn&&i.type==type);
        return AdventureCatalog.Container(worn!=null?worn.definitionId:board?"rig_standard":"bag_standard");
    }
    void Awake(){hero=GetComponent<ThirdPersonHero>();}
    void Start(){if(items.Count==0)Starter();Refresh();}
    public void Starter()
    {
        items.Clear();mainWeapon=reserveWeapon=null;EnsureContainers();
        for(int t=0;t<4;t++){var item=AdventureItems.New((GearType)t,GearQuality.White);AddOrStore(item);if(t==0&&!item.overflow)mainWeapon=item.id;}
        AddOrStore(AdventureItems.NewContainer("rig_light"));AddOrStore(AdventureItems.NewContainer("bag_gather"));Refresh();
    }
    void EnsureContainers()
    {
        foreach(string id in new[]{"rig_standard","bag_standard"}){
            var d=AdventureCatalog.Container(id);
            if(items.Any(i=>i.worn&&i.type==d.type))continue;
            var item=AdventureItems.NewContainer(id);item.worn=true;items.Add(item);
        }
    }
    bool Owns(GearItem item)=>item!=null&&items.Count(i=>i.id==item.id)==1&&items.Contains(item);
    static bool Fit(IReadOnlyList<GearItem> list,ContainerDefinition container,GearItem item,bool board,int x,int y,int rotation,params GearItem[] ignore)
    {
        if(container==null||item==null||rotation<0||rotation>3)return false;
        var cells=new HashSet<Vector2Int>();
        foreach(var p in item.Cells(rotation)){var cell=p+new Vector2Int(x,y);if(!container.Allows(cell.x,cell.y))return false;cells.Add(cell);}
        foreach(var other in list){
            if(other==item||ignore.Contains(other)||other.worn||other.overflow||other.board!=board)continue;
            foreach(var p in other.Cells(other.rotation))if(cells.Contains(p+new Vector2Int(other.x,other.y)))return false;
        }return true;
    }
    public bool Fits(GearItem item,bool board,int x,int y)=>Fit(items,Definition(board),item,board,x,y,item.rotation);
    public bool FitsAt(GearItem item,bool board,int x,int y,int rotation)=>Fit(items,Definition(board),item,board,x,y,rotation);
    static bool Find(IReadOnlyList<GearItem> list,ContainerDefinition d,GearItem item,bool board,out Vector2Int p,out int rotation)
    {
        for(int r=0;r<4;r++){
            int turn=(item.rotation+r)%4;
            if(item.Definition!=null&&!item.Definition.canRotate&&turn!=0)continue;
            for(int y=0;y<d.height;y++)for(int x=0;x<d.width;x++)if(Fit(list,d,item,board,x,y,turn)){p=new Vector2Int(x,y);rotation=turn;return true;}
        }p=default;rotation=0;return false;
    }
    public bool FindSpace(GearItem item,bool board,out Vector2Int p){for(int y=0;y<Height(board);y++)for(int x=0;x<Width(board);x++)if(Fits(item,board,x,y)){p=new Vector2Int(x,y);return true;}p=default;return false;}
    public bool CanAdd(GearItem item)=>item!=null&&!items.Any(i=>i.id==item.id)&&Find(items,Bag,item,false,out _,out _);
    public bool Add(GearItem item)
    {
        if(item==null||items.Any(i=>i.id==item.id))return false;
        if(item.dataRevision==0)item.UpgradeLegacy();
        if(!Find(items,Bag,item,false,out var p,out var r))return false;
        item.board=item.overflow=item.worn=false;item.x=p.x;item.y=p.y;item.rotation=r;items.Add(item);var flow=AdventureFlow.Find(hero);if(flow!=null&&flow.Tracking){item.origin=ItemOrigin.RunLoot;item.originRunId=flow.ActiveRun.runId;}return true;
    }
    public void AddOrStore(GearItem item){if(item==null||items.Any(i=>i.id==item.id))return;if(Add(item))return;item.board=item.worn=false;item.overflow=true;item.x=item.y=-1;items.Add(item);}
    static HashSet<Vector2Int> PositionedCells(GearItem item,int x,int y,int rotation)=>new HashSet<Vector2Int>(item.Cells(rotation).Select(c=>c+new Vector2Int(x,y)));
    public bool CanPlace(GearItem item,bool board,int x,int y,int rotation,bool swap,out string reason)
    {
        reason="";
        if(!Owns(item)||item.worn){reason="此物品不能移动。";return false;}
        if(rotation<0||rotation>3||item.Definition!=null&&!item.Definition.canRotate&&rotation!=0){reason="该物品不允许旋转。";return false;}
        if(board&&item.Container){reason="胸挂和背包需要使用‘更换容器’，不能作为盘内装备。";return false;}
        if(board&&Carried(item)){reason="请先选择另一把主武器。";return false;}
        if(Fit(items,Definition(board),item,board,x,y,rotation))return true;
        if(!swap||item.overflow){reason="位置越界、格子不可用或与装备重叠。";return false;}
        var cells=PositionedCells(item,x,y,rotation);
        var collisions=items.Where(i=>i!=item&&!i.worn&&!i.overflow&&i.board==board&&PositionedCells(i,i.x,i.y,i.rotation).Overlaps(cells)).ToArray();
        if(collisions.Length!=1){reason="交换时只能覆盖一件装备。";return false;}
        var other=collisions[0];
        if(item.board&&(other.Container||Carried(other))){reason="交换会将容器或主武器放入胸挂，已取消。";return false;}
        if(!Fit(items,Definition(board),item,board,x,y,rotation,other)||!Fit(items,Definition(item.board),other,item.board,item.x,item.y,other.rotation,item)){reason="双方尺寸不兼容，交换已取消。";return false;}
        if(item.board==board&&cells.Overlaps(PositionedCells(other,item.x,item.y,other.rotation))){reason="交换后的两件装备会重叠。";return false;}
        return true;
    }
    public bool Place(GearItem item,bool board,int x,int y,int rotation,bool swap,out string reason)
    {
        if(!CanPlace(item,board,x,y,rotation,swap,out reason))return false;
        var cells=PositionedCells(item,x,y,rotation);
        var other=items.FirstOrDefault(i=>i!=item&&!i.worn&&!i.overflow&&i.board==board&&PositionedCells(i,i.x,i.y,i.rotation).Overlaps(cells));
        if(other!=null){other.board=item.board;other.x=item.x;other.y=item.y;}
        item.board=board;item.x=x;item.y=y;item.rotation=rotation;item.overflow=false;Refresh();return true;
    }
    public bool Move(GearItem item,bool board,int x,int y)=>Place(item,board,x,y,item.rotation,false,out _);
    public bool Rotate(GearItem item,out string reason)=>Place(item,item.board,item.x,item.y,(item.rotation+1)%4,false,out reason);
    public bool AutoMove(GearItem item)
    {
        bool board=!item.board&&!item.Container&&!item.overflow;
        if(!Owns(item)||!Find(items,Definition(board),item,board,out var p,out var rotation)||!Place(item,board,p.x,p.y,rotation,false,out _)){hero.Inventory.NotifyMessage("目标空间不足，或该物品不能放入目标容器。");return false;}return true;
    }
    public bool SelectMain(GearItem item){if(!Owns(item)||!item.Weapon||!item.InBag)return false;if(item.id==reserveWeapon)reserveWeapon=mainWeapon;mainWeapon=item.id;GetComponent<AdventureCombat>()?.EquipmentChanged();Refresh();return true;}
    public bool SelectReserve(GearItem item){if(!Owns(item)||!item.Weapon||!item.InBag||item.id==mainWeapon)return false;reserveWeapon=item.id;Refresh();return true;}
    public bool Engrave(GearItem item,int affix)
    {
        if(!Owns(item)||!item.Weapon||!item.InBag||affix<0||affix>=WeaponTraits.Names.Length||hero.Health.Dead)return false;
        if(WeaponTraits.Has(item,affix))return false;
        if(!hero.Inventory.TryRemove(MaterialKind.CrystalShard,2))return false;
        var list=item.affixes==null?new List<int>():item.affixes.ToList();
        if(list.Count>0)list.RemoveAt(0);list.Remove(affix);list.Insert(0,affix);item.affixes=list.ToArray();
        Refresh();hero.Inventory.NotifyMessage("已铭刻："+WeaponTraits.Names[affix]);return true;
    }
    public void ClearReserve(){reserveWeapon=null;Refresh();}
    public bool SwapWeapons(){if(Main==null||Reserve==null)return false;var old=mainWeapon;mainWeapon=reserveWeapon;reserveWeapon=old;Refresh();return true;}
    public void RestoreReserve(string id){reserveWeapon=id;if(Reserve==null||id==mainWeapon)reserveWeapon=null;}
    public bool PreviewContainer(GearItem candidate,out List<GearItem> result,out string reason)
    {
        result=null;reason="";
        if(!Owns(candidate)||!candidate.Container||candidate.worn){reason="请选择未穿戴的胸挂或背包。";return false;}
        var d=AdventureCatalog.Container(candidate.definitionId);if(d==null){reason="缺少容器定义。";return false;}
        bool board=candidate.type==GearType.ChestRig;
        var copy=items.Select(i=>i.Clone()).ToList();var next=copy.First(i=>i.id==candidate.id);var previous=copy.First(i=>i.worn&&i.type==candidate.type);
        previous.worn=false;previous.overflow=true;previous.board=false;previous.x=previous.y=-1;
        next.worn=true;next.overflow=next.board=false;next.x=next.y=-1;next.rotation=0;
        var pending=copy.Where(i=>!i.worn&&!i.overflow&&i.board==board).OrderByDescending(i=>i.Cells(i.rotation).Count()).ToList();
        foreach(var item in pending)item.overflow=true;
        foreach(var item in pending){
            var container=ContainerFor(copy,board);
            if(Fit(copy,container,item,board,item.x,item.y,item.rotation)){item.overflow=false;continue;}
            if(!Find(copy,container,item,board,out var p,out var turn)){reason=$"容量或形状不兼容：{item.Name} 无处摆放。请先整理；物品未移动。";return false;}
            item.x=p.x;item.y=p.y;item.rotation=turn;item.overflow=false;
        }
        if(!Find(copy,ContainerFor(copy,false),previous,false,out var back,out var r)){reason="背包无法收回旧容器，请先留出空间。";return false;}
        previous.x=back.x;previous.y=back.y;previous.rotation=r;previous.overflow=false;
        result=copy;reason=$"可更换：{d.width}×{d.height}，{d.Capacity} 个可用格。旧容器将收回背包。";return true;
    }
    public bool EquipContainer(GearItem item)
    {
        if(!PreviewContainer(item,out var result,out var reason)){hero.Inventory.NotifyMessage(reason);return false;}
        items=result;hero.Inventory.NotifyMessage("已更换："+item.Name+"；旧容器已收回背包。");Refresh();return true;
    }
    public void Refresh(){GetComponent<AdventureCombat>()?.RefreshWeapon();hero?.Health?.RefreshVisuals();}
    public string Recipe(GearQuality q){int n=(int)q+1;return $"木材 ×{n*2}  石头 ×{n}  铁矿 ×{n*2}"+(n>1?$"  晶石 ×{n-1}":"")+(n>=4?$"  核心 ×{n-3}":"");}
    public bool CanCraft(GearType t,GearQuality q)
    {
        if((int)t<0||(int)t>=9||(int)q<0||(int)q>4)return false;if(AdventureRecipes.Advanced(q)&&!AdventureRecipes.Access(hero,AdventureRecipes.Gear(t,q)))return false;var bag=hero.Inventory;int n=(int)q+1;var item=new GearItem{type=t,quality=q,definitionId=AdventureCatalog.GearIds[(int)t]};
        return !hero.Health.Dead&&Find(items,Bag,item,false,out _,out _)&&bag.Count(MaterialKind.Wood)>=n*2&&bag.Count(MaterialKind.Stone)>=n&&bag.Count(MaterialKind.Ore)>=n*2&&bag.Count(MaterialKind.CrystalShard)>=n-1&&bag.Count(MaterialKind.BossCore)>=Mathf.Max(0,n-3);
    }
    public bool Craft(GearType t,GearQuality q)
    {
        if(!CanCraft(t,q))return false;
        return AdventureRecipes.Advanced(q)?AdventureRecipes.Camp(hero).Manufacture(t,q):CraftNow(t,q);
    }
    internal bool CraftNow(GearType t,GearQuality q)
    {
        if(!CanCraft(t,q))return false;var item=AdventureItems.New(t,q);if(!Add(item))return false;int n=(int)q+1;var bag=hero.Inventory;
        bag.TryRemove(MaterialKind.Wood,n*2);bag.TryRemove(MaterialKind.Stone,n);bag.TryRemove(MaterialKind.Ore,n*2);if(n>1)bag.TryRemove(MaterialKind.CrystalShard,n-1);if(n>3)bag.TryRemove(MaterialKind.BossCore,n-3);
        bag.NotifyMessage("制作成功："+item.Name+"，已放入背包。");return true;
    }
    public bool CanCraftContainer(string id)
    {
        var d=AdventureCatalog.Container(id);if(d==null||hero.Health.Dead)return false;if(AdventureRecipes.Advanced(d.quality)&&!AdventureRecipes.Access(hero,AdventureRecipes.Container(id)))return false;
        return hero.Inventory.Count(MaterialKind.Wood)>=d.woodCost&&hero.Inventory.Count(MaterialKind.MonsterHide)>=d.hideCost&&hero.Inventory.Count(MaterialKind.Ore)>=d.oreCost&&Find(items,Bag,AdventureItems.NewContainer(id),false,out _,out _);
    }
    public bool CraftContainer(string id)
    {
        if(!CanCraftContainer(id))return false;
        var d=AdventureCatalog.Container(id);
        return AdventureRecipes.Advanced(d.quality)?AdventureRecipes.Camp(hero).ManufactureContainer(id):CraftContainerNow(id);
    }
    internal bool CraftContainerNow(string id)
    {
        if(!CanCraftContainer(id))return false;var d=AdventureCatalog.Container(id);var item=AdventureItems.NewContainer(id);if(!Add(item))return false;
        if(d.woodCost>0)hero.Inventory.TryRemove(MaterialKind.Wood,d.woodCost);if(d.hideCost>0)hero.Inventory.TryRemove(MaterialKind.MonsterHide,d.hideCost);if(d.oreCost>0)hero.Inventory.TryRemove(MaterialKind.Ore,d.oreCost);
        hero.Inventory.NotifyMessage("已制作："+item.Name+"，可在容器页更换。");return true;
    }
    public bool ProtectedEntry(GearItem item)=>item!=null&&AdventureFlow.Find(hero)!=null&&AdventureFlow.Find(hero).Protects(item.id);
    public void Salvage(GearItem item)
    {
        if(!Owns(item)||item.worn||item.board||Carried(item)||ProtectedEntry(item))return;
        if(hero.Inventory.Count(MaterialKind.Ore)>CampRuntime.MaterialLimit-((int)item.quality+1)||!hero.Inventory.CanCarryDelta(MaterialKind.Ore,(int)item.quality+1)){hero.Inventory.NotifyMessage("素材堆栈已满，未拆解装备。");return;}items.Remove(item);hero.Inventory.Add(MaterialKind.Ore,(int)item.quality+1);hero.Inventory.NotifyMessage("已分解为铁矿。");Refresh();
    }
    public void Restore(GearItem[] saved,string main)
    {
        items=saved.Select(i=>i.Clone()).ToList();mainWeapon=main;reserveWeapon=null;
        bool legacy=items.Any(i=>i.dataRevision==0);
        foreach(var item in items)if(item.dataRevision==0)item.UpgradeLegacy();
        EnsureContainers();
        if(legacy){RepairLegacyLayout();AddOrStore(AdventureItems.NewContainer("rig_light"));AddOrStore(AdventureItems.NewContainer("bag_gather"));}
        Refresh();
    }
    void RepairLegacyLayout()
    {
        var pending=items.Where(i=>!i.worn).ToArray();foreach(var i in pending)i.overflow=true;
        foreach(var item in pending){bool board=item.board;if(Fit(items,Definition(board),item,board,item.x,item.y,item.rotation)){item.overflow=false;continue;}
            if(Find(items,Definition(board),item,board,out var p,out var r)){item.x=p.x;item.y=p.y;item.rotation=r;item.overflow=false;}else{item.x=item.y=-1;item.overflow=true;}}
    }
    public void Migrate(int sword,int armor,bool swordOn,bool armorOn)
    {
        items.Clear();mainWeapon=reserveWeapon=null;EnsureContainers();
        if(sword>0){var i=new GearItem{id=System.Guid.NewGuid().ToString("N"),type=GearType.Sword,quality=(GearQuality)Mathf.Clamp(sword-1,0,4),legacyTier=sword};i.UpgradeLegacy();AddOrStore(i);if(swordOn&&!i.overflow)mainWeapon=i.id;}
        if(armor>0){var i=new GearItem{id=System.Guid.NewGuid().ToString("N"),type=GearType.Armor,quality=(GearQuality)Mathf.Clamp(armor-1,0,4),legacyTier=armor};i.UpgradeLegacy();AddOrStore(i);if(armorOn)AutoMove(i);}
        for(int t=0;t<4;t++)if(!items.Any(i=>i.type==(GearType)t))AddOrStore(AdventureItems.New((GearType)t,GearQuality.White));
        if(string.IsNullOrEmpty(mainWeapon)){var i=items.FirstOrDefault(g=>g.type==GearType.Sword&&g.legacyTier==0&&g.InBag);if(i==null){i=AdventureItems.New(GearType.Sword,GearQuality.White);AddOrStore(i);}if(i.InBag)mainWeapon=i.id;}
        AddOrStore(AdventureItems.NewContainer("rig_light"));AddOrStore(AdventureItems.NewContainer("bag_gather"));Refresh();
    }
}

