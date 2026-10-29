using System;
using System.Linq;
using UnityEngine;

// Uses the existing pause/menu surface so combat and hotkeys keep their current behavior.
public static class ContainerInventoryView
{
    static string selectedId, draggingId, templateId="rig_light";
    static bool armed, dragging, placing;
    static int filter, rotation, control;
    static Vector2 start;
    static Vector2Int grab;
    static Vector2 grabPoint;
    static Vector2 containerScroll, overflowScroll;
    public static bool Dragging=>dragging;
    public static string SelectedId=>selectedId;
    public static int Rotation=>rotation;
    public static Vector2Int Grab=>grab;
    public static Vector2 GrabPoint=>grabPoint;
    public static void CancelInteraction(){armed=dragging=placing=false;draggingId=null;if(GUIUtility.hotControl==control)GUIUtility.hotControl=0;}
    public static void Select(string id){selectedId=id;}
    public static void BeginDrag(GearItem item,Vector2Int offset){BeginDrag(item,offset,new Vector2(.5f,.5f));}
    public static void BeginDrag(GearItem item,Vector2Int offset,Vector2 fraction){selectedId=draggingId=item.id;grab=offset;grabPoint=(Vector2)offset+new Vector2(Mathf.Clamp(fraction.x,.001f,.999f),Mathf.Clamp(fraction.y,.001f,.999f));rotation=item.rotation;armed=dragging=true;placing=false;filter=0;}
    public static bool DropOn(AdventureLoadout gear,bool board,int x,int y,out string reason)
    {
        var item=gear.items.Find(i=>i.id==(draggingId??selectedId));
        reason="";bool result=item!=null&&gear.Place(item,board,x,y,rotation,true,out reason);
        if(item==null)reason="物品已不存在。";
        CancelInteraction();return result;
    }
    public static void RotateSelection(AdventureLoadout gear)
    {
        var item=gear.items.Find(i=>i.id==(draggingId??selectedId));if(item==null||item.worn)return;
        if(item.Definition!=null&&!item.Definition.canRotate)return;
        if(armed||dragging||placing){if(armed){dragging=true;filter=0;}var old=item.SizeAt(rotation);grab=new Vector2Int(old.y-1-grab.y,grab.x);grabPoint=new Vector2(old.y-grabPoint.y,grabPoint.x);rotation=(rotation+1)%4;}
        else if(!gear.Rotate(item,out var reason))gear.GetComponent<PlayerInventory>().NotifyMessage(reason);
    }
    public static void Draw(PlayerInventory bag,ThirdPersonHero hero,float x,float y)
    {
        var gear=hero.GetComponent<AdventureLoadout>();
        float rigCell=Mathf.Min(39,330f/gear.Width(true),240f/gear.Height(true));
        float bagCell=Mathf.Min(35,420f/gear.Width(false),252f/gear.Height(false));
        var rigRect=new Rect(x,y+68,gear.Width(true)*rigCell,gear.Height(true)*rigCell);
        var bagRect=new Rect(x+386,y+64,gear.Width(false)*bagCell,gear.Height(false)*bagCell);
        control=GUIUtility.GetControlID("背包拖放".GetHashCode(),FocusType.Passive);
        Input(gear,bag,rigRect,bagRect,rigCell,bagCell);
        CombatUI.Text(new Rect(x,y,370,28),$"{gear.Rig.displayName}  {gear.UsedCells}/{gear.Rig.Capacity} 格",21,CombatUI.Gold,true);
        CombatUI.Text(new Rect(x,y+31,370,25),$"攻击 +{gear.Attack:0.#}  防御 +{gear.Defense:0.#}  移速 {gear.MoveBonus:+0%;-0%;0%}",16);
        CombatUI.Text(new Rect(x+386,y,440,28),$"{gear.Bag.displayName}  {gear.Bag.width}×{gear.Bag.height}",21,CombatUI.Ink,true);
        var labels=new[]{"全部","装备","武器","素材"};
        for(int i=0;i<4;i++)if(CombatUI.Button(new Rect(x+386+i*108,y+30,100,28),labels[i],!dragging&&!placing,filter==i))filter=i;
        Grid(gear,true,rigRect,rigCell);Grid(gear,false,bagRect,bagCell);
        CombatUI.Text(new Rect(x,y+315,355,45),"拖动装备移动 / 交换 · "+PlayerInput.Key(PlayerAction.Rotate)+" 旋转\n右键取消拖放；灰色格不可使用",16,CombatUI.Muted);
        if(CombatUI.Button(new Rect(x,y+368,310,34),"更换 / 制造胸挂与背包",!dragging)){CancelInteraction();bag.OpenPage(PlayerInventory.Page.Equipment);}
        if(gear.OverflowCount>0&&CombatUI.Button(new Rect(x,y+410,310,30),$"迁移暂存：{gear.OverflowCount} 件（点击取回）",!dragging)){CancelInteraction();bag.OpenPage(PlayerInventory.Page.Overflow);}
        Materials(bag,x+386,y+326);
        Details(gear,bag,x+858,y);
        Ghost(gear,rigRect,bagRect,rigCell,bagCell);
    }
    static bool Visible(GearItem i)=>filter==0||filter==1&&!i.Weapon||filter==2&&i.Weapon;
    static GearItem Hit(AdventureLoadout gear,bool board,Rect rect,float cell,Vector2 mouse)
    {
        if(!rect.Contains(mouse))return null;var p=new Vector2Int(Mathf.FloorToInt((mouse.x-rect.x)/cell),Mathf.FloorToInt((mouse.y-rect.y)/cell));
        return gear.items.FirstOrDefault(i=>!i.worn&&!i.overflow&&i.board==board&&(board||Visible(i))&&i.Cells(i.rotation).Any(c=>c+new Vector2Int(i.x,i.y)==p));
    }
    static void Input(AdventureLoadout gear,PlayerInventory bag,Rect rig,Rect pack,float rigCell,float bagCell)
    {
        var e=Event.current;var mouse=e.mousePosition;
        if((e.type==EventType.KeyDown||e.type==EventType.MouseDown)&&PlayerInput.Down(PlayerAction.Rotate)){RotateSelection(gear);e.Use();}
        if(e.type==EventType.MouseDown&&e.button==1&&(armed||placing)){CancelInteraction();e.Use();return;}
        if(e.type==EventType.MouseDown&&e.button==0&&(rig.Contains(mouse)||pack.Contains(mouse))){
            bool board=rig.Contains(mouse);var rect=board?rig:pack;float cell=board?rigCell:bagCell;
            if(placing){int px=Mathf.FloorToInt((mouse.x-rect.x)/cell),py=Mathf.FloorToInt((mouse.y-rect.y)/cell);if(!DropOn(gear,board,px,py,out var reason))bag.NotifyMessage(reason);e.Use();return;}
            var item=Hit(gear,board,rect,cell,mouse);
            if(item!=null){selectedId=item.id;draggingId=item.id;start=mouse;rotation=item.rotation;grab=new Vector2Int(Mathf.FloorToInt((mouse.x-rect.x)/cell)-item.x,Mathf.FloorToInt((mouse.y-rect.y)/cell)-item.y);grabPoint=new Vector2((mouse.x-rect.x)/cell-item.x,(mouse.y-rect.y)/cell-item.y);armed=true;GUIUtility.hotControl=control;e.Use();}
        }
        if(e.type==EventType.MouseDrag&&armed){if((mouse-start).sqrMagnitude>16){dragging=true;filter=0;}e.Use();}
        if(e.type==EventType.MouseUp&&e.button==0&&armed){
            if(dragging&&(rig.Contains(mouse)||pack.Contains(mouse))){bool board=rig.Contains(mouse);var rect=board?rig:pack;float cell=board?rigCell:bagCell;int px=Mathf.FloorToInt((mouse.x-rect.x)/cell)-grab.x,py=Mathf.FloorToInt((mouse.y-rect.y)/cell)-grab.y;if(!DropOn(gear,board,px,py,out var reason))bag.NotifyMessage(reason);}
            else CancelInteraction();e.Use();
        }
    }
    static void Grid(AdventureLoadout gear,bool board,Rect r,float cell)
    {
        for(int y=0;y<gear.Height(board);y++)for(int x=0;x<gear.Width(board);x++){
            var area=new Rect(r.x+x*cell,r.y+y*cell,cell-2,cell-2);bool valid=gear.Definition(board).Allows(x,y);CombatUI.Fill(area,valid?CombatUI.Raised:new Color(.035f,.04f,.045f));
            if(!valid){CombatUI.Fill(new Rect(area.center.x-1,area.y+5,2,area.height-10),new Color(.3f,.32f,.34f));}
        }
        foreach(var item in gear.items){
            if(item.worn||item.overflow||item.board!=board||!board&&!Visible(item))continue;
            var color=AdventureItems.Color(item.quality);if(dragging&&item.id==draggingId)color*=.35f;
            foreach(var p in item.Cells(item.rotation))CombatUI.Fill(new Rect(r.x+(item.x+p.x)*cell,r.y+(item.y+p.y)*cell,cell-2,cell-2),Color.Lerp(CombatUI.Raised,color,item.id==selectedId?.42f:.18f));
            var area=new Rect(r.x+item.x*cell,r.y+item.y*cell,item.Size.x*cell-2,item.Size.y*cell-2);CombatUI.Fill(new Rect(area.x,area.y,area.width,2),color);
            AdventureInventoryView.DrawIcon(new Rect(area.x+4,area.y+4,area.width-8,area.height-8),item.Icon,color);
            if(gear.Carried(item))CombatUI.Text(new Rect(area.x,area.yMax-20,area.width,20),gear.Main==item?"主":"备",13,CombatUI.Gold,true);
        }
    }
    static void Ghost(AdventureLoadout gear,Rect rig,Rect bag,float rigCell,float bagCell)
    {
        if(!dragging&&!placing)return;var item=gear.items.Find(i=>i.id==(draggingId??selectedId));if(item==null)return;
        var mouse=Event.current.mousePosition;bool board=rig.Contains(mouse);var r=board?rig:bag;float cell=board?rigCell:bagCell;
        int x=Mathf.FloorToInt((mouse.x-r.x)/cell)-(placing?0:grab.x),y=Mathf.FloorToInt((mouse.y-r.y)/cell)-(placing?0:grab.y);
        bool inside=rig.Contains(mouse)||bag.Contains(mouse);string reason="松开鼠标取消";bool valid=inside&&gear.CanPlace(item,board,x,y,rotation,true,out reason);
        if(inside)foreach(var p in item.Cells(rotation))CombatUI.Fill(new Rect(r.x+(x+p.x)*cell,r.y+(y+p.y)*cell,cell-2,cell-2),valid?new Color(.25f,.9f,.5f,.6f):new Color(1,.2f,.25f,.6f));
        var size=item.SizeAt(rotation);AdventureInventoryView.DrawIcon(new Rect(mouse.x-(placing?0:grabPoint.x)*cell,mouse.y-(placing?0:grabPoint.y)*cell,size.x*cell,size.y*cell),item.Icon,AdventureItems.Color(item.quality));
        CombatUI.Panel(new Rect(mouse.x-120,mouse.y-35,270,28));CombatUI.Text(new Rect(mouse.x-114,mouse.y-33,258,24),valid?"松开放置 / 交换 · "+PlayerInput.Key(PlayerAction.Rotate)+" 旋转":inside?reason:"松开取消 · "+PlayerInput.Key(PlayerAction.Rotate)+" 旋转",14,valid?CombatUI.Experience:CombatUI.Gold);
    }
    static void Materials(PlayerInventory bag,float x,float y)
    {
        CombatUI.Text(new Rect(x,y,445,22),bag.SupplyLabel,16,CombatUI.Muted);
        string[] keys={"hide","crystal","core","wood","stone","ore","potion"};
        for(int i=0;i<7;i++){var r=new Rect(x+i*62,y+25,56,54);CombatUI.Fill(r,CombatUI.Raised);AdventureInventoryView.DrawIcon(new Rect(r.x+9,r.y+2,34,31),(i==6?AdventureCatalog.Item("health_potion")?.iconKey:AdventureCatalog.Material((MaterialKind)i)?.iconKey)??keys[i],Color.white);int n=i==6?bag.HealthPotionCount:bag.Count((MaterialKind)i);CombatUI.Text(new Rect(r.x+3,r.y+32,50,22),n.ToString(),15);if(GUI.Button(r,GUIContent.none,GUIStyle.none))bag.NotifyMessage((i==6?"回血药水":PlayerInventory.Label((MaterialKind)i))+$" ×{n}");}
        if(CombatUI.Button(new Rect(x,y+86,174,28),"使用回血药水",bag.HealthPotionCount>0&&!dragging))bag.UseHealthPotion();
        if(CombatUI.Button(new Rect(x+184,y+86,248,28),bag.PotionOnQuickbar?"从 Q 道具栏移除":"放入 Q 道具栏",!dragging))bag.SetPotionQuickbar(!bag.PotionOnQuickbar);
    }
    static void Details(AdventureLoadout gear,PlayerInventory bag,float x,float y)
    {
        var item=gear.items.Find(i=>i.id==selectedId);
        if(item==null){CombatUI.Text(new Rect(x,y+42,194,220),"选择物品查看详情\n\n占格按类型定义\n品质与占格独立\n\n拖动时 "+PlayerInput.Key(PlayerAction.Rotate)+" 旋转\n覆盖单件可交换",18,CombatUI.Muted);return;}
        AdventureInventoryView.DrawIcon(new Rect(x+46,y+30,76,76),item.Icon,AdventureItems.Color(item.quality));
        CombatUI.Text(new Rect(x,y+120,194,58),item.Name,21,AdventureItems.Color(item.quality),true);
        string status=item.worn?"当前穿戴容器":item.overflow?"迁移暂存 · 不加属性":item.board?"胸挂内 · 已生效":gear.Main==item?"当前主武器":gear.Reserve==item?"备用武器 · 不加属性":"背包内 · 未生效";
        string text=$"占格 {item.Size.x}×{item.Size.y} · {item.rotation*90}°\n攻击 +{item.Attack:0.#}\n防御 +{item.Defense:0.#}\n{status}";
        if(item.Container){var d=AdventureCatalog.Container(item.definitionId);text=$"布局 {d.width}×{d.height} / {d.Capacity} 格\n{d.description}\n{status}";}
        if(item.widthOverride>0)text+="\n旧型占格已保留";
        CombatUI.Text(new Rect(x,y+184,194,102),text,16);
        CombatUI.Text(new Rect(x,y+272,194,24),AdventureFlow.Find(bag.GetComponent<ThirdPersonHero>())?.SourceLabel(item)??"营地资产",14,CombatUI.Gold);
        if(CombatUI.Button(new Rect(x,y+294,182,30),item.overflow?"自动取回背包":item.board?"取回背包":item.Container?"查看容器更换":"自动放入胸挂",!item.worn&&!dragging)){
            if(item.Container&&!item.overflow){CancelInteraction();bag.OpenPage(PlayerInventory.Page.Equipment);}else gear.AutoMove(item);
        }
        if(CombatUI.Button(new Rect(x,y+332,88,30),"旋转 90°",!item.worn&&!dragging)){if(item.overflow&&!placing){placing=true;rotation=item.rotation;}RotateSelection(gear);}
        if(CombatUI.Button(new Rect(x+94,y+332,88,30),"摆放",!item.worn&&!dragging)){placing=true;draggingId=null;rotation=item.rotation;filter=0;}
        if(item.Weapon&&CombatUI.Button(new Rect(x,y+370,182,30),"配置双武器 / 查看词缀",!dragging)){WeaponLoadoutView.Select(item.id);bag.OpenPage(PlayerInventory.Page.Weapons);}
        if(CombatUI.Button(new Rect(x,y+408,182,30),gear.ProtectedEntry(item)?"入场保护 · 不可拆解":"分解为铁矿",!gear.ProtectedEntry(item)&&!item.worn&&!item.board&&!gear.Carried(item)&&!dragging))gear.Salvage(item);
    }
    public static void Containers(PlayerInventory bag,ThirdPersonHero hero,float x,float y)
    {
        var gear=hero.GetComponent<AdventureLoadout>();
        CombatUI.Text(new Rect(x,y,430,30),"穿戴与更换容器",23,CombatUI.Gold,true);
        CombatUI.Text(new Rect(x,y+35,430,34),$"当前：{gear.Rig.displayName} / {gear.Bag.displayName}",17);
        var owned=gear.items.Where(i=>i.Container).ToArray();containerScroll=GUI.BeginScrollView(new Rect(x,y+78,425,268),containerScroll,new Rect(0,0,400,owned.Length*57));
        for(int i=0;i<owned.Length;i++){var item=owned[i];if(CombatUI.Button(new Rect(0,i*57,395,49),item.Name+(item.worn?"（穿戴中）":item.overflow?"（暂存）":""),true,selectedId==item.id))selectedId=item.id;}GUI.EndScrollView();
        float dx=x+460;CombatUI.Text(new Rect(dx,y,580,30),"制造胸挂与背包",23,CombatUI.Ink,true);
        for(int i=0;i<AdventureCatalog.ContainerIds.Length;i++){var d=AdventureCatalog.Container(AdventureCatalog.ContainerIds[i]);if(CombatUI.Button(new Rect(dx+i%3*190,y+42+i/3*55,178,46),d.displayName,true,templateId==d.definitionId))templateId=d.definitionId;}
        var recipe=AdventureCatalog.Container(templateId);CombatUI.Text(new Rect(dx,y+164,560,55),$"{recipe.width}×{recipe.height}，{recipe.Capacity} 格 · {recipe.description}",18,CombatUI.Gold);
        CombatUI.Text(new Rect(dx,y+227,565,30),$"消耗：木材 {recipe.woodCost} · 野怪皮 {recipe.hideCost} · 铁矿 {recipe.oreCost}",18);
        if(CombatUI.Button(new Rect(dx,y+318,180,30),"追踪材料"))CraftingTargets.Select(hero,recipe.type,recipe.quality,templateId);
        bool advanced=AdventureRecipes.Advanced(recipe.quality);
        if(CombatUI.Button(new Rect(dx,y+271,300,38),gear.CanCraftContainer(templateId)?"制作并放入背包":advanced?"需解锁配方并在营地制造":"材料或背包空间不足",gear.CanCraftContainer(templateId)))gear.CraftContainer(templateId);
        if(advanced&&CombatUI.Button(new Rect(dx+312,y+271,230,38),"工作台 / 配方解锁")){CampInventoryView.OpenWorkbench(recipe.type,recipe.quality,templateId);bag.OpenPage(PlayerInventory.Page.Camp);}
        var selected=gear.items.Find(i=>i.id==selectedId&&i.Container);
        if(selected==null){CombatUI.Text(new Rect(x,y+355,420,70),"在左侧选择未穿戴容器，查看更换预览。",18,CombatUI.Muted);return;}
        bool can=gear.PreviewContainer(selected,out _,out var reason);
        CombatUI.Text(new Rect(x,y+354,425,92),selected.Name+"\n"+reason,17,can?CombatUI.Experience:CombatUI.Muted);
        if(CombatUI.Button(new Rect(dx,y+343,330,40),"确认更换选中容器",can))gear.EquipContainer(selected);
        CombatUI.Text(new Rect(dx,y+394,570,46),"更换会完整检查两边空间；不兼容时保持原状。\n旧容器收回背包，暂存物品不会自动加入属性。",16,CombatUI.Muted);
    }
    public static void Overflow(PlayerInventory bag,ThirdPersonHero hero,float x,float y)
    {
        var gear=hero.GetComponent<AdventureLoadout>();var list=gear.items.Where(i=>i.overflow).ToArray();
        CombatUI.Text(new Rect(x,y,1000,34),$"迁移暂存 · {list.Length} 件",24,CombatUI.Gold,true);
        CombatUI.Text(new Rect(x,y+43,1000,45),"这里的物品完整保留但不提供属性。腾出空间后可取回，不需要重新获取。",18,CombatUI.Muted);
        overflowScroll=GUI.BeginScrollView(new Rect(x,y+103,1045,335),overflowScroll,new Rect(0,0,1020,Mathf.Max(320,list.Length*66)));
        for(int n=0;n<list.Length;n++){var item=list[n];AdventureInventoryView.DrawIcon(new Rect(0,n*66,50,50),item.Icon,AdventureItems.Color(item.quality));CombatUI.Text(new Rect(70,n*66+8,570,40),item.Name+$"  {item.Size.x}×{item.Size.y}  攻击 +{item.Attack:0.#} / 防御 +{item.Defense:0.#}",18,AdventureItems.Color(item.quality));
            if(CombatUI.Button(new Rect(660,n*66+6,160,36),"自动取回背包"))gear.AutoMove(item);
            if(CombatUI.Button(new Rect(835,n*66+6,160,36),"手动选择位置")){CancelInteraction();selectedId=item.id;rotation=item.rotation;bag.OpenPage(PlayerInventory.Page.Items);placing=true;}
        }GUI.EndScrollView();
    }
}


