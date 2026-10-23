using System.Linq;
using UnityEngine;
public static class WeaponLoadoutView
{
    static string selected;static Vector2 scroll;
    public static void Select(string id){selected=id;}
    public static void Draw(ThirdPersonHero hero,float x,float y)
    {
        var gear=hero.GetComponent<AdventureLoadout>();var bag=hero.Inventory;
        CombatUI.Text(new Rect(x,y,1040,28),"V 切换手持与备用 · 只有手持词缀生效 · 共用技能冷却",21,CombatUI.Gold);
        Slot(gear.Main,"手持武器",x,y+40);Slot(gear.Reserve,"备用武器",x+340,y+40);
        if(CombatUI.Button(new Rect(x+700,y+46,145,34),"清空备用槽",gear.Reserve!=null))gear.ClearReserve();
        CombatUI.Text(new Rect(x+700,y+88,340,46),"两把武器仍占背包格子，\n移入胸挂或分解前先解除配置。",16,CombatUI.Muted);
        var weapons=gear.items.Where(i=>i.Weapon&&i.InBag).ToArray();
        scroll=GUI.BeginScrollView(new Rect(x,y+150,325,240),scroll,new Rect(0,0,300,weapons.Length*54));
        for(int n=0;n<weapons.Length;n++){var i=weapons[n];AdventureInventoryView.DrawIcon(new Rect(2,n*54+5,34,34),i.Icon,AdventureItems.Color(i.quality));if(CombatUI.Button(new Rect(45,n*54,250,45),i.Name,true,selected==i.id))selected=i.id;}GUI.EndScrollView();
        var item=weapons.FirstOrDefault(i=>i.id==selected)??weapons.FirstOrDefault();if(item==null)return;selected=item.id;
        float r=x+350;
        CombatUI.Text(new Rect(r,y+150,650,32),item.Name+"  攻击 +"+item.Attack.ToString("0.#"),23,AdventureItems.Color(item.quality),true);
        CombatUI.Text(new Rect(r,y+190,660,85),WeaponTraits.Describe(item),17);
        CombatUI.Text(new Rect(r,y+250,660,66),WeaponTraits.Exclusive(item),18,CombatUI.Gold);
        if(CombatUI.Button(new Rect(r,y+320,180,34),gear.Main==item?"当前手持":"设为手持",gear.Main!=item))gear.SelectMain(item);
        if(CombatUI.Button(new Rect(r+194,y+320,180,34),gear.Reserve==item?"当前备用":"设为备用",!gear.Carried(item)))gear.SelectReserve(item);
        CombatUI.Text(new Rect(r,y+358,660,25),"定向铭刻：晶石碎片 ×2，替换第一词缀；金 / 红保留第二词缀。",16,CombatUI.Muted);
        for(int a=0;a<WeaponTraits.Names.Length;a++){int col=a%3,row=a/3;GUI.Label(new Rect(r+col*216,y+390+row*28,204,26),new GUIContent("",WeaponTraits.Descriptions[a]));if(CombatUI.Button(new Rect(r+col*216,y+390+row*28,204,26),WeaponTraits.Names[a],bag.Count(MaterialKind.CrystalShard)>=2&&!WeaponTraits.Has(item,a)))gear.Engrave(item,a);}

        CombatUI.Text(new Rect(x,y+395,325,48),string.IsNullOrEmpty(GUI.tooltip)?"悬停铭刻按钮查看词缀效果。\n铭刻只影响当前选择的武器。":GUI.tooltip,16,CombatUI.Muted);
    }
    static void Slot(GearItem i,string label,float x,float y){AdventureInventoryView.DrawIcon(new Rect(x,y+4,52,52),i!=null?i.Icon:"sword",i!=null?AdventureItems.Color(i.quality):CombatUI.Muted);CombatUI.Text(new Rect(x+65,y,270,28),label,18,CombatUI.Gold);CombatUI.Text(new Rect(x+65,y+32,270,52),i!=null?i.Name:"未配置 · 从下方选择武器",17);}
}


