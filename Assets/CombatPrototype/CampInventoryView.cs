using System.Linq;
using UnityEngine;
public static class CampInventoryView
{
    public static void OpenWorkbench(GearType type,GearQuality quality,string container=null){mode=2;WorkbenchView.Select(type,quality,container);}
    static int mode,quantity=1;static string bagId,warehouseId;static Vector2 bagScroll,warehouseScroll;
    public static int Section=>mode;
    public static void SelectSection(int section){if(section>=0&&section<=3)mode=section;}
    public static void Draw(ThirdPersonHero hero,float x,float y)
    {
        var session=Object.FindFirstObjectByType<CombatSession>();var camp=session.Camp;var gear=hero.GetComponent<AdventureLoadout>();var bag=hero.Inventory;
        if(!camp.InCamp){
            if(session.Flow.Enabled){CombatUI.Text(new Rect(x,y,1000,130),"冒险中不能直接存货或回营。\n无需清场，靠近起点普通祭坛按 E / H，完成 5 秒引导撤离。\n主动放弃使用死亡保留规则；正常退出会保存本局检查点。",22,CombatUI.Gold);if(CombatUI.Button(new Rect(x,y+125,320,42),"继续当前冒险"))bag.SetOpen(false);if(CombatUI.Button(new Rect(x,y+180,320,42),"主动放弃本次冒险…"))session.Flow.OpenAbandon();return;}
            CombatUI.Text(new Rect(x,y,900,38),"营地与永久仓库",27,CombatUI.Gold,true);
            CombatUI.Text(new Rect(x,y+62,940,92),"清场后按 H 回营整备，关闭面板即可回到原位置继续冒险。\n永久仓库保留装备品质、词缀与材料；重新开局仍会保留仓库。\n回营期间暂停战斗、技能冷却和下一波倒计时。",20);
            string reason=camp.EntryReason;CombatUI.Text(new Rect(x,y+185,900,55),reason==""?"当前可以回营。":reason,20,CombatUI.Muted);
            if(CombatUI.Button(new Rect(x,y+270,260,44),"前往营地  H",reason==""))camp.Enter();return;
        }
        CombatUI.Text(new Rect(x,y,720,30),mode==2?$"营地工作台 · 永久配方 {camp.CaptureRecipes().Length}/{AdventureRecipes.All.Length}":$"永久仓库 · 装备 {camp.Items.Count}/{CampRuntime.Capacity} 件 · 存取后立即保存",23,CombatUI.Gold,true);
        if(CombatUI.Button(new Rect(x+826,y,210,32),session.Flow.Enabled?"出征准备":"返回冒险  H / Esc")){if(session.Flow.Enabled)session.Flow.OpenPreparation();else bag.SetOpen(false);}
        if(CombatUI.Button(new Rect(x,y+44,160,32),"装备存取",true,mode==0))mode=0;
        if(CombatUI.Button(new Rect(x+172,y+44,160,32),"材料存取",true,mode==1))mode=1;
        if(CombatUI.Button(new Rect(x+344,y+44,160,32),"营地工作台",true,mode==2))mode=2;
        if(session.Flow.Enabled&&CombatUI.Button(new Rect(x+516,y+44,160,32),"待领取 "+session.Flow.Profile.pending.Length,true,mode==3))mode=3;
        if(session.Flow.AtCamp&&CombatUI.Button(new Rect(x+688,y+44,160,32),"营地走动"))camp.Explore();
        if(session.Flow.AtCamp&&CombatUI.Button(new Rect(x+860,y+44,175,32),"帮助 / 教程")){if(camp.Explore())PlayerHudPresenter.Instance.SetDetails("教程");}
        if(mode==3&&session.Flow.Enabled){session.Flow.DrawPending(x,y+90);return;}
        if(mode==2){WorkbenchView.Draw(hero,x,y+90);return;}
        if(mode==0){
            CombatUI.Text(new Rect(x,y+94,500,28),"随身背包",21,CombatUI.Gold);CombatUI.Text(new Rect(x+548,y+94,500,28),"永久仓库 · 不提供战斗属性",21,CombatUI.Gold);
            var carried=gear.items.Where(i=>i.InBag).ToArray();var stored=camp.Items.ToArray();
            bagScroll=List(carried,bagId,x,y+133,ref bagId,bagScroll,gear,true);warehouseScroll=List(stored,warehouseId,x+548,y+133,ref warehouseId,warehouseScroll,gear,false);
            var a=carried.FirstOrDefault(i=>i.id==bagId);var b=stored.FirstOrDefault(i=>i.id==warehouseId);
            if(CombatUI.Button(new Rect(x,y+342,240,34),"存入选中装备",a!=null&&!gear.Carried(a)&&camp.Items.Count<CampRuntime.Capacity))camp.DepositEquipment(a.id);
            if(CombatUI.Button(new Rect(x+548,y+342,240,34),"取回选中装备",b!=null))camp.WithdrawEquipment(b.id);
            CombatUI.Text(new Rect(x,y+389,500,55),a==null?"选择装备。手持、备用和穿戴中的物品需先替换，才能存入。":Detail(a),16,CombatUI.Muted);
            CombatUI.Text(new Rect(x+548,y+389,500,55),b==null?"取回需要背包有可用空间；空间不足时物品仍留在仓库。":Detail(b),16,CombatUI.Muted);
        }
        else{
            CombatUI.Text(new Rect(x,y+93,510,26),"每次存取数量",18,CombatUI.Muted);int[] amounts={1,10,100,int.MaxValue};string[] labels={"1","10","100","全部"};for(int n=0;n<4;n++)if(CombatUI.Button(new Rect(x+190+n*83,y+88,75,30),labels[n],true,quantity==amounts[n]))quantity=amounts[n];
            for(int i=0;i<6;i++){
                var kind=(MaterialKind)i;float row=y+135+i*47;var definition=AdventureCatalog.Material(kind);AdventureInventoryView.DrawIcon(new Rect(x,row+1,31,31),definition.iconKey,Color.white);
                CombatUI.Text(new Rect(x+43,row,210,32),PlayerInventory.Label(kind),19);
                int backpack=bag.Count(kind),warehouse=camp.Materials[i];CombatUI.Text(new Rect(x+260,row,420,32),$"背包 {backpack}     仓库 {warehouse}",18);
                int put=quantity==int.MaxValue?backpack:quantity,take=quantity==int.MaxValue?warehouse:quantity;
                if(CombatUI.Button(new Rect(x+710,row,143,32),"存入仓库",put>0&&backpack>=put&&warehouse<=CampRuntime.MaterialLimit-put))camp.TransferMaterial(kind,put,true);
                if(CombatUI.Button(new Rect(x+868,row,143,32),"取回背包",take>0&&warehouse>=take&&backpack<=CampRuntime.MaterialLimit-take))camp.TransferMaterial(kind,take,false);
            }
            CombatUI.Text(new Rect(x,y+425,1040,24),"仅随身材料可用于当前制作；仓库材料需先取回。每种材料上限一亿。",16,CombatUI.Muted);
        }
    }
    static string Detail(GearItem i)=>i.Name+"  攻击 +"+i.Attack.ToString("0.#")+" / 防御 +"+i.Defense.ToString("0.#")+"\n"+(i.Weapon?"词缀："+(i.affixes==null||i.affixes.Length==0?"无":string.Join(" / ",i.affixes.Select(a=>WeaponTraits.Names[a]))):"品质、物品编号与属性随装备保留。");
    static Vector2 List(GearItem[] items,string selected,float x,float y,ref string id,Vector2 scroll,AdventureLoadout gear,bool bag)
    {
        scroll=GUI.BeginScrollView(new Rect(x,y,510,195),scroll,new Rect(0,0,485,Mathf.Max(190,items.Length*53)));
        for(int n=0;n<items.Length;n++){var i=items[n];AdventureInventoryView.DrawIcon(new Rect(4,n*53+5,34,34),i.Icon,AdventureItems.Color(i.quality));string suffix=bag&&gear.Carried(i)?"（携带中）":"";if(CombatUI.Button(new Rect(48,n*53,430,44),i.Name+suffix,true,selected==i.id))id=i.id;}GUI.EndScrollView();return scroll;
    }
}
