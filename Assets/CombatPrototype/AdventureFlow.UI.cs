using System.Linq;
using UnityEngine;
public partial class AdventureFlow
{
    AdventureMode selectedMode=AdventureMode.ForestExploration;
    ExpeditionGoal selectedGoal;
    Vector2 carryScroll,resultScroll,pendingScroll;
    string selectedPending,discardConfirm;
    public static string OutcomeLabel(AdventureOutcome outcome)=>new[]{"成功撤离","死亡结算","主动放弃","测试挑战完成"}[(int)outcome];
    void OnGUI()
    {
        if(!Enabled)return;
        var old=CombatUI.Begin();int depth=GUI.depth;GUI.depth=-160;
        if(Preparing)DrawPreparation();else if(AbandonPrompt)DrawAbandon();else if(HasResult)DrawSettlement();else if(!string.IsNullOrEmpty(Error)){Panel("存档 / 恢复受阻");CombatUI.Text(new Rect(Left+28,Top+100,900,130),Error,23,CombatUI.Gold);if(CombatUI.Button(new Rect(Left+28,Top+290,300,45),"重试读取完整存档"))session.Saves.LoadProgress();}
        else if(ActiveRun!=null&&!session.hero.Inventory.IsOpen&&!session.hero.Progression.IsChoosing&&!session.hero.SaveMenuOpen){
            CombatUI.Panel(new Rect(CombatUI.Width/2-290,18,580,120));
            CombatUI.Text(new Rect(CombatUI.Width/2-275,23,550,27),ActiveRun.mode==AdventureMode.ForestExploration?"万象归途 · 森林布局测试":ActiveRun.mode==AdventureMode.EndlessWaves?"万象归途 · 原波次测试":"万象归途 · 冒险测试 · "+GoalLabel(ActiveRun.goal),19,CombatUI.Gold);
            CombatUI.Text(new Rect(CombatUI.Width/2-275,52,550,47),ActiveRun.legacyProtected?"迁移保护：已有物资本局首次结算受保护，新所得按来源记账。":$"检查点 #{Revision}：{CheckpointSummary}\n退出续此点；飞行弹体 / 攻击前摇重置，R 主动放弃。",15,CombatUI.Muted);
            CombatUI.Text(new Rect(CombatUI.Width/2-275,97,550,25),"补给堆栈 "+SupplyUsed()+"/"+SupplyLimit+" · 装备受现有网格限制 · 暂无主线成果",14,CombatUI.Muted);
            if(ActiveRun.phase==RunPhase.Extracting){CombatUI.Panel(new Rect(CombatUI.Width/2-260,CombatUI.Height/2-50,520,115));CombatUI.Text(new Rect(CombatUI.Width/2-240,CombatUI.Height/2-37,480,38),$"撤离引导 {ActiveRun.extractionRemaining:0.0} 秒",27,CombatUI.Gold,true);CombatUI.Text(new Rect(CombatUI.Width/2-240,CombatUI.Height/2+9,480,50),"离开范围 / 受伤 / 再按 H 可取消；附近有怪仍可引导，下一波已暂停。",17);}
            else if(Vector3.Distance(session.hero.transform.position,ExitPosition)<ExitRange+1&&!session.hero.Inventory.IsOpen){CombatUI.Panel(new Rect(CombatUI.Width/2-270,CombatUI.Height-258,540,44));CombatUI.Text(new Rect(CombatUI.Width/2-255,CombatUI.Height-252,510,33),ExtractionReason==""?ChallengeReached?"E / H 普通祭坛撤离（测试目标已完成）":"E / H 普通祭坛撤离（5 秒，不需清场）":ExtractionReason,17,CombatUI.Gold);}
            else if(ChallengeReached)CombatUI.Text(new Rect(CombatUI.Width/2-290,145,580,45),"测试目标完成：可继续战斗探索，或随时去普通祭坛撤离。",18,CombatUI.Gold);
        }
        GUI.depth=depth;GUI.matrix=old;
    }
    float Left=>CombatUI.Width/2-530;
    float Top=>CombatUI.Height/2-320;
    void Panel(string title){CombatUI.Fill(new Rect(0,0,CombatUI.Width,CombatUI.Height),new Color(0,0,0,.65f));CombatUI.Panel(new Rect(Left,Top,1060,640));CombatUI.Text(new Rect(Left+28,Top+18,990,43),"万象归途 · "+title,28,CombatUI.Gold,true);}
    void DrawPreparation()
    {
        Panel("出征准备 · ForestRuins 测试冒险");float x=Left+28,y=Top+82;
        if(CombatUI.Button(new Rect(x,y,300,35),"冒险测试 · 随时尝试撤离",true,selectedMode==AdventureMode.TestChallenge))selectedMode=AdventureMode.TestChallenge;
        if(CombatUI.Button(new Rect(x+630,y,340,35),"森林探索 · 兴趣点与路线",true,selectedMode==AdventureMode.ForestExploration))selectedMode=AdventureMode.ForestExploration;
        if(CombatUI.Button(new Rect(x+315,y,300,35),"原波次测试 · 每五波首领",true,selectedMode==AdventureMode.EndlessWaves))selectedMode=AdventureMode.EndlessWaves;
        for(int g=0;g<3;g++)if(CombatUI.Button(new Rect(x+g*220,y+44,210,30),GoalLabel((ExpeditionGoal)g),true,(int)selectedGoal==g))selectedGoal=(ExpeditionGoal)g;
        var gear=session.hero.GetComponent<AdventureLoadout>();CombatUI.Text(new Rect(x,y+82,970,62),"手持："+(gear.Main?.Name??"未配置")+"    备用："+(gear.Reserve?.Name??"未配置")+"\n容器："+gear.Rig.displayName+" / "+gear.Bag.displayName,19);
        CombatUI.Text(new Rect(x,y+145,970,86),"轻惩罚：入场非消耗性装备受保护，冒险中禁止拆解。失败归还入场布局与原始词缀；已花材料、已用药水不恢复。\n成功带回仍持有的本局战利品；失败丢失本局新物资、等级与临时技能。仓库和历史配方保留。\n退出只保存检查点，不等于撤离。目标完成可继续探索，不授正式徽章；普通祭坛无需清场。",17,CombatUI.Muted);
        carryScroll=GUI.BeginScrollView(new Rect(x,y+291,970,130),carryScroll,new Rect(0,0,940,Mathf.Max(200,gear.items.Count*32+4)));
        for(int n=0;n<gear.items.Count;n++){var item=gear.items[n];AdventureInventoryView.DrawIcon(new Rect(0,n*32,27,27),item.Icon,AdventureItems.Color(item.quality));CombatUI.Text(new Rect(38,n*32,890,30),item.Name+(item.worn?" · 穿戴容器":item.board?" · 胸挂":" · 背包")+$"  {item.Size.x}×{item.Size.y}",17);}
        GUI.EndScrollView();
        CombatUI.Text(new Rect(x,y+236,970,50),"携带材料："+string.Join(" · ",Enumerable.Range(0,6).Select(k=>PlayerInventory.Label((MaterialKind)k)+" "+session.hero.Inventory.Count((MaterialKind)k)))+"\n药水："+session.hero.Inventory.HealthPotionCount+" · 补给堆栈 "+SupplyUsed()+"/"+supplySlots,16);
        string reason=DepartureReason;CombatUI.Text(new Rect(x,y+434,970,35),reason==""?"携带清单将随本次冒险一起保存，保存成功后才进入战斗。":reason,17,CombatUI.Gold);
        if(CombatUI.Button(new Rect(x,y+490,300,43),"返回营地整备"))ClosePreparation();if(CombatUI.Button(new Rect(x+650,y+490,320,43),"确认出征",reason==""))Depart(selectedMode);
    }
    void DrawAbandon()
    {
        Panel("主动放弃本次冒险？");CombatUI.Text(new Rect(Left+28,Top+100,970,145),"采用死亡相同的保留规则：\n归还入场装备与剩余带入消耗品；丢失本局新装备、新材料和临时成长。\n已花费材料与药水不返还，永久仓库及历史配方不回滚。\n正常退出游戏无需放弃，下次可以继续同一个 Run。",23);
        if(CombatUI.Button(new Rect(Left+28,Top+360,330,48),"取消，继续本局"))CancelAbandon();if(CombatUI.Button(new Rect(Left+665,Top+360,330,48),"确认放弃并生成失败结算"))ConfirmAbandon();
    }
    void DrawSettlement()
    {
        Panel(OutcomeLabel(Settlement.outcome)+" · "+(Settlement.status==SettlementStatus.Committed?"已提交":"待提交"));float x=Left+28,y=Top+83;
        CombatUI.Text(new Rect(x,y,980,90),(Settlement.status==SettlementStatus.Committed?"结算已保存，重新打开不会再次发奖。":"结局已锁定，确认后一次性提交收益与去重记录。")+$"\n归还 {Settlement.returnedGear.Length} 件 · 带回 {Settlement.keptGear.Length} 件 · 损失 {Settlement.lostGear.Length} 件 · 待领取 {Settlement.plan.pending.Length} 项\n本局材料：带回 {CountsLabel(Settlement.keptMaterials)} / 损失 {CountsLabel(Settlement.lostMaterials)}",18,CombatUI.Gold);
        resultScroll=GUI.BeginScrollView(new Rect(x,y+100,980,305),resultScroll,new Rect(0,0,940,Mathf.Max(320,(Settlement.returnedGear.Length+Settlement.keptGear.Length+Settlement.lostGear.Length)*31+255)));float row=0;
        foreach(var item in Settlement.keptGear){CombatUI.Text(new Rect(10,row,920,28),"带回："+item.Name,18,AdventureItems.Color(item.quality));row+=31;}
        foreach(var item in Settlement.lostGear){CombatUI.Text(new Rect(10,row,920,28),"损失："+item.Name,18,CombatUI.Health);row+=31;}
        CombatUI.Text(new Rect(0,row,940,28),"归还入场装备："+Settlement.returnedGear.Length+" 件（采用入场容器布局）",21,CombatUI.Gold);row+=34;
        foreach(var item in Settlement.returnedGear){CombatUI.Text(new Rect(10,row,920,28),item.Name+" · 入场保护归还",17,AdventureItems.Color(item.quality));row+=31;}
        CombatUI.Text(new Rect(0,row+6,940,70),"剩余带入材料："+CountsLabel(Settlement.returnedMaterials)+"\n本局带回材料："+CountsLabel(Settlement.keptMaterials)+"\n本局损失材料："+CountsLabel(Settlement.lostMaterials),17);row+=88;
        CombatUI.Text(new Rect(0,row,940,83),$"归还药水 {Settlement.returnedPotions} · 损失本局药水 {Settlement.lostPotions} · 清除局内等级提升 {Settlement.lostLevel} 与临时技能\n永久解锁：{(Settlement.permanentUnlocks.Length==0?"无新增（历史解锁保留）":string.Join("、",Settlement.permanentUnlocks))}\n待领取：{Settlement.plan.pending.Length} 项 · {(Settlement.legacyProtection?"本局使用一次性迁移保护":"入场保护按出征清单执行")}",18);GUI.EndScrollView();
        CombatUI.Text(new Rect(x,y+420,980,55),string.IsNullOrEmpty(Error)?"新装备优先存入仓库；满仓收益进入持久化待领取区。先处理待领取，再次出征。":Error,18,string.IsNullOrEmpty(Error)?CombatUI.Muted:CombatUI.Health);
        if(Settlement.status==SettlementStatus.Pending){if(CombatUI.Button(new Rect(x+620,y+490,350,43),journalDurable?"确认结算并保存":"重试保存结局 / 结算"))CommitSettlement();}
        else if(CombatUI.Button(new Rect(x+620,y+490,350,43),"返回营地 / 重试回营"))AcknowledgeSettlement();
    }
    static string CountsLabel(int[] amounts)=>string.Join(" · ",Enumerable.Range(0,6).Where(k=>amounts[k]>0).Select(k=>PlayerInventory.Label((MaterialKind)k)+" "+amounts[k]).DefaultIfEmpty("无"));
    public void DrawPending(float x,float y)
    {
        CombatUI.Text(new Rect(x,y,1030,32),$"待领取 {Profile.pending.Length} 项 · 未处理完前不能出征",23,CombatUI.Gold,true);
        pendingScroll=GUI.BeginScrollView(new Rect(x,y+48,620,345),pendingScroll,new Rect(0,0,595,Mathf.Max(335,Profile.pending.Length*72)));
        for(int n=0;n<Profile.pending.Length;n++){var p=Profile.pending[n];string label=p.equipment?p.item.Name:PlayerInventory.Label(p.material)+" ×"+p.amount;string icon=p.equipment?p.item.Icon:AdventureCatalog.Material(p.material).iconKey;AdventureInventoryView.DrawIcon(new Rect(0,n*72+10,36,36),icon,p.equipment?AdventureItems.Color(p.item.quality):Color.white);if(CombatUI.Button(new Rect(47,n*72,540,60),label+"\n"+p.reason,true,selectedPending==p.pendingId))selectedPending=p.pendingId;}GUI.EndScrollView();
        var item=Profile.pending.FirstOrDefault(p=>p.pendingId==selectedPending);if(item==null){CombatUI.Text(new Rect(x+650,y+55,380,100),"选中物品后可领取到仓库或背包；也可明确确认弃置。",20);return;}
        CombatUI.Text(new Rect(x+650,y+53,380,88),item.reason+"\n来源冒险："+(item.sourceRunId??"未知"),17,CombatUI.Muted);
        if(CombatUI.Button(new Rect(x+650,y+160,360,40),"领取到永久仓库"))ClaimPending(item.pendingId,true);
        if(CombatUI.Button(new Rect(x+650,y+212,360,40),"领取到随身背包"))ClaimPending(item.pendingId,false);
        if(discardConfirm!=item.pendingId){if(CombatUI.Button(new Rect(x+650,y+283,360,38),"弃置此项…"))discardConfirm=item.pendingId;}
        else{CombatUI.Text(new Rect(x+650,y+270,370,38),"弃置无法撤销，物品将永久删除。",17,CombatUI.Health);if(CombatUI.Button(new Rect(x+650,y+318,175,35),"确认永久弃置")){DiscardPending(item.pendingId);discardConfirm=null;}if(CombatUI.Button(new Rect(x+835,y+318,175,35),"取消"))discardConfirm=null;}
    }
}
