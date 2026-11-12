using UnityEngine;using UnityEngine.UI;using UnityEngine.InputSystem;
// Presentation only: selection calls the runtime controller and the original input barrier.
public sealed class WeaponSkillPanel:MonoBehaviour {
 WeaponSkillExpansion skills;ThirdPersonHero hero;Canvas canvas;Text[] labels;Text status;
 void Start(){skills=GetComponent<WeaponSkillExpansion>();hero=GetComponent<ThirdPersonHero>();var root=new GameObject("Weapon skill loadout",typeof(Canvas),typeof(CanvasScaler),typeof(GraphicRaycaster));root.transform.SetParent(transform,false);canvas=root.GetComponent<Canvas>();canvas.renderMode=RenderMode.ScreenSpaceOverlay;canvas.sortingOrder=2;var scale=root.GetComponent<CanvasScaler>();scale.uiScaleMode=CanvasScaler.ScaleMode.ScaleWithScreenSize;scale.referenceResolution=new Vector2(1280,720);labels=new Text[3];for(int i=0;i<3;i++){int slot=i;var g=new GameObject("技能槽"+i,typeof(RectTransform),typeof(Image),typeof(Button));g.transform.SetParent(root.transform,false);var rect=g.GetComponent<RectTransform>();rect.anchorMin=rect.anchorMax=rect.pivot=new Vector2(0,1);rect.anchoredPosition=new Vector2(12,-160-i*32);rect.sizeDelta=new Vector2(230,30);g.GetComponent<Image>().color=new Color(.08f,.15f,.14f,.9f);g.GetComponent<Button>().onClick.AddListener(()=>skills.Select(slot));var text=new GameObject("Label",typeof(RectTransform),typeof(Text));text.transform.SetParent(g.transform,false);var tr=text.GetComponent<RectTransform>();tr.anchorMin=Vector2.zero;tr.anchorMax=Vector2.one;tr.offsetMin=tr.offsetMax=Vector2.zero;labels[i]=text.GetComponent<Text>();labels[i].font=CatUI.Font;labels[i].fontSize=15;labels[i].alignment=TextAnchor.MiddleCenter;labels[i].raycastTarget=false;}
 var info=new GameObject("技能阶段",typeof(RectTransform),typeof(Text));info.transform.SetParent(root.transform,false);var r=info.GetComponent<RectTransform>();r.anchorMin=r.anchorMax=r.pivot=new Vector2(0,1);r.anchoredPosition=new Vector2(12,-258);r.sizeDelta=new Vector2(340,118);status=info.GetComponent<Text>();status.font=CatUI.Font;status.fontSize=14;status.raycastTarget=false;if(GetComponent<CP05TrainingMarker>()!=null){var rack=new GameObject("训练装备架",typeof(RectTransform),typeof(Image),typeof(Button));rack.transform.SetParent(root.transform,false);var rect=rack.GetComponent<RectTransform>();rect.anchorMin=rect.anchorMax=rect.pivot=new Vector2(0,1);rect.anchoredPosition=new Vector2(12,-400);rect.sizeDelta=new Vector2(230,30);rack.GetComponent<Image>().color=new Color(.12f,.25f,.22f,.9f);rack.GetComponent<Button>().onClick.AddListener(()=>{hero.GetComponent<AdventureCombat>().NewWeapons.SpawnTrainingArsenal();PlayerInput.Barrier();});var label=new GameObject("Label",typeof(RectTransform),typeof(Text));label.transform.SetParent(rack.transform,false);var rlabel=label.GetComponent<RectTransform>();rlabel.anchorMin=Vector2.zero;rlabel.anchorMax=Vector2.one;rlabel.offsetMin=rlabel.offsetMax=Vector2.zero;var t=label.GetComponent<Text>();t.text="训练装备架（临时）";t.font=CatUI.Font;t.fontSize=15;t.alignment=TextAnchor.MiddleCenter;t.raycastTarget=false;}}
 void Update(){if(canvas==null)return;canvas.enabled=hero!=null&&!hero.Health.Dead&&!hero.GameplayPaused;var combat=hero.GetComponent<AdventureCombat>();Hotkeys(combat);if(NewWeaponRegistry.Is(combat.Gear.Weapon)){for(int i=0;i<3;i++){labels[i].transform.parent.gameObject.SetActive(i<2);if(i<2){labels[i].text=(combat.NewWeapons.Selected==i?"◆ ":"◇ ")+"["+(i+1)+"] "+NewWeaponCombat.NameFor(combat.Gear.Weapon,i);labels[i].color=Color.white;}}status.text=PlayerInput.Key(PlayerAction.Skill)+" · "+(combat.NewWeapons.Phase=="Startup"?"准备":combat.NewWeapons.Phase=="Recovery"?"收招":"就绪")+" · 1/2 切槽"+AffixInfo(combat,false,combat.NewWeapons.Selected);return;}for(int i=0;i<3;i++)labels[i].transform.parent.gameObject.SetActive(true);for(int i=0;i<3;i++){string name=i==0?"基础动作":"["+i+"] "+(WeaponSkillCatalog.Get(combat.Gear.Weapon,i)?.name??"—");labels[i].text=(skills.Selected==i?"◆ ":"◇ ")+name;labels[i].color=skills.Selected==i?new Color(1,.8f,.35f):Color.white;}string phase=skills.Phase=="Charging"?"蓄势":skills.Phase=="Startup"?"准备":skills.Phase=="Release"?"释放":skills.Phase=="Recovery"?"恢复":skills.Phase=="Cancelled"?"已取消":"就绪";status.text=PlayerInput.Key(PlayerAction.Skill)+" 释放当前技能 · "+phase+(skills.Phase=="Charging"?" "+(skills.ChargeFraction*100).ToString("0")+"%":"")+" · 1/2 切槽"+AffixInfo(combat,true,skills.Selected);}
 // UX-PROGRESSION-01 P1: 1/2 select the two extension slots. Field context only,
 // never while dead / rolling / UI-blocked / paused / at camp, and never a cast.
 void Hotkeys(AdventureCombat combat){
  var k=Keyboard.current;if(k==null||hero==null||combat==null||skills==null)return;
  if(!PlayerInput.Focused||PlayerInput.UIBlocked)return;
  if(hero.Health==null||hero.Health.Dead||hero.GameplayPaused||Time.timeScale<=0)return;
  if(hero.Dodge!=null&&hero.Dodge.IsRolling)return;
  if(hero.Inventory!=null&&hero.Inventory.IsOpen)return;
  var flow=AdventureFlow.Find(hero);if(flow==null||flow.AtCamp||flow.HasResult||flow.Preparing||flow.AbandonPrompt)return;
  bool modern=NewWeaponRegistry.Is(combat.Gear.Weapon);
  if(k.digit1Key.wasPressedThisFrame)skills.Select(modern?0:1);
  else if(k.digit2Key.wasPressedThisFrame)skills.Select(modern?1:2);
 }
 void OnDestroy(){if(canvas!=null)Destroy(canvas.gameObject);}
 // UX-PROGRESSION-03A P-04 U-03: 暴露词缀作用范围 / 聚能代价 / 冷却，使玩家可见哪些技能生效回响、聚能增加多少（冻结规格）
 string AffixInfo(AdventureCombat combat,bool legacy,int selected){
   bool echo=legacy?selected==0:true;                 // 旧武器仅槽0技能适用回响；新武器技能均适用
   bool focus=WeaponTraits.Has(combat.Gear.Main,5);    // 聚能 = 词缀 id 5
   string id=combat.SkillIdText;                       // 唯一技能标识，用于专属机制提示
   string note=id=="twin.counter"?" · 强化窗0.85s（未强化0.65×／强化1.8×）":id=="scythe.pull"?" · 0 伤害 · Boss 免疫":"";
   string detail=string.IsNullOrEmpty(combat.SkillWindowDetail)?"":"（"+combat.SkillWindowDetail+"）";
   return " · W"+combat.SkillWindow.ToString("0.00")+"s"+detail
     +" 冷却"+combat.SkillDuration.ToString("0.0")+"s"
     +" 回响"+(echo?"适用":"不适用")
     +" 聚能"+(focus?" +25%伤害 +1s冷却":" 未装备")
     +note;
 }
}
