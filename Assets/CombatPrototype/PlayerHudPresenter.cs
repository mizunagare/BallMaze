using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.UI;
// Runtime-built uGUI view. It owns presentation only; all actions enter existing domains.
[DefaultExecutionOrder(20000)]
public sealed class PlayerHudPresenter:MonoBehaviour {
 public static PlayerHudPresenter Instance {get;private set;}public static bool Running=>Instance!=null&&Instance.isActiveAndEnabled;
 CombatSession s;ThirdPersonHero hero;AdventureCombat combat;AdventureLoadout gear;InteractionResolver resolver;
 GameObject root,play,context,details,notifications;CanvasScaler scaler;Font font;Sprite flatSprite;HudIconCatalog icons;
 GameObject targetPanel;Text targetText;Image targetIcon;float nextTarget;
 Image saveIcon;Text health,level,region,prompt,secondary,notice,detailText,saveText;Image hp,xp,progress;Image contextIcon;
 readonly List<RectTransform> buttons=new List<RectTransform>();readonly List<RectTransform> groups=new List<RectTransform>();
 public IReadOnlyList<RectTransform> LayoutGroups=>groups;public string VisibleEId {get;private set;}public string VisibleHId {get;private set;}
 public string VisibleSecondary=>secondary==null?"":secondary.text;
 public string VisiblePrompt=>prompt==null?"":prompt.text;public bool ContextVisible=>context!=null&&context.activeSelf;
 public float UiScale {get;private set;}=1;public string Detail {get;private set;}="";public string CriticalMessage {get;private set;}="";
 float oldTime;CursorLockMode oldLock;bool oldCursor;Slot main,reserve,skill,roll,potion,supply;string lastSave;float nextDetails;
 readonly Color surface=new Color(.035f,.055f,.07f,.9f),ink=new Color(.94f,.94f,.88f),muted=new Color(.63f,.72f,.73f),gold=new Color(.95f,.73f,.38f);
 class Slot {public Image icon,mask;public Text name,key,value;public Button button;}
 void Awake(){if(Instance!=null&&Instance!=this){enabled=false;return;}Instance=this;s=GetComponent<CombatSession>();}
 void Start(){hero=s.hero;combat=hero.GetComponent<AdventureCombat>();gear=hero.GetComponent<AdventureLoadout>();resolver=hero.Inventory.Interactions;icons=new HudIconCatalog();flatSprite=Sprite.Create(Texture2D.whiteTexture,new Rect(0,0,Texture2D.whiteTexture.width,Texture2D.whiteTexture.height),new Vector2(.5f,.5f));font=Font.CreateDynamicFontFromOSFont(new[]{"Microsoft YaHei","SimHei","Noto Sans CJK SC"},24);Build();}
 RectTransform Box(string name,Transform parent,Vector2 anchor,Vector2 pivot,Vector2 size,Vector2 position,bool panel=true){var g=new GameObject(name,typeof(RectTransform));g.transform.SetParent(parent,false);var r=g.GetComponent<RectTransform>();r.anchorMin=r.anchorMax=anchor;r.pivot=pivot;r.sizeDelta=size;r.anchoredPosition=position;if(panel){var image=g.AddComponent<Image>();image.color=surface;image.raycastTarget=false;}return r;}
 Text TextAt(Transform parent,string name,string value,int size,Vector2 position,Vector2 dimensions,Color? color=null){var r=Box(name,parent,new Vector2(0,1),new Vector2(0,1),dimensions,position,false);var t=r.gameObject.AddComponent<Text>();t.font=font;t.fontSize=size;t.color=color??ink;t.text=value;t.raycastTarget=false;t.horizontalOverflow=HorizontalWrapMode.Wrap;t.verticalOverflow=VerticalWrapMode.Truncate;t.supportRichText=false;return t;}
 Image ImageAt(Transform parent,string name,Vector2 position,Vector2 size,Color color){var r=Box(name,parent,new Vector2(0,1),new Vector2(0,1),size,position,false);var i=r.gameObject.AddComponent<Image>();i.sprite=flatSprite;i.color=color;i.raycastTarget=false;return i;}
 void Label(Text t,string value){if(t.text!=value)t.text=value;}
 Image Bar(Transform parent,string name,Vector2 position,Vector2 size,Color fill){ImageAt(parent,name+"Background",position,size,new Color(.18f,.23f,.25f));var i=ImageAt(parent,name,position,size,fill);i.type=Image.Type.Filled;i.fillMethod=Image.FillMethod.Horizontal;return i;}
 Button Click(RectTransform r,Action action){var i=r.GetComponent<Image>()??r.gameObject.AddComponent<Image>();i.raycastTarget=true;var b=r.gameObject.AddComponent<Button>();b.targetGraphic=i;b.navigation=new Navigation{mode=Navigation.Mode.None};b.onClick.AddListener(()=>{if(hero.Inventory.ClosedFrame!=Time.frameCount)action();EventSystem.current?.SetSelectedGameObject(null);});buttons.Add(r);return b;}
 Button SmallButton(Transform parent,string label,Vector2 position,Vector2 size,Action action){var r=Box(label,parent,new Vector2(0,1),new Vector2(0,1),size,position);string icon=label.StartsWith("M ")?"route":label.StartsWith("F1 ")?"help":null;if(icon!=null){var image=ImageAt(r,"ButtonIcon",new Vector2(5,-7),new Vector2(20,20),Color.white);image.sprite=icons.Get(icon);image.preserveAspect=true;}TextAt(r,label+"Text",label,17,new Vector2(icon==null?8:29,-5),size-new Vector2(icon==null?12:31,4));return Click(r,action);}
 Slot MakeSlot(Transform parent,string name,string key,float x,Action action){var r=Box(name,parent,new Vector2(0,1),new Vector2(0,1),new Vector2(82,78),new Vector2(x,-6));var v=new Slot();v.button=Click(r,()=>{if(!hero.GameplayPaused)action();});v.icon=ImageAt(r,"Icon",new Vector2(23,-8),new Vector2(38,38),Color.white);v.icon.preserveAspect=true;v.mask=ImageAt(r,"Cooldown",new Vector2(23,-8),new Vector2(38,38),new Color(0,0,0,.75f));v.mask.type=Image.Type.Filled;v.mask.fillMethod=Image.FillMethod.Vertical;v.name=TextAt(r,"Name",name,13,new Vector2(4,-47),new Vector2(74,20));v.name.alignment=TextAnchor.MiddleCenter;v.key=TextAt(r,"Key",key,12,new Vector2(4,-4),new Vector2(24,18),gold);v.value=TextAt(r,"Value","",15,new Vector2(4,-64),new Vector2(74,19));v.value.alignment=TextAnchor.MiddleCenter;return v;}
 void Build(){root=new GameObject("PlayerHUD_UI01",typeof(RectTransform),typeof(Canvas),typeof(CanvasScaler),typeof(GraphicRaycaster));root.transform.SetParent(transform,false);var c=root.GetComponent<Canvas>();c.renderMode=RenderMode.ScreenSpaceOverlay;c.sortingOrder=0;scaler=root.GetComponent<CanvasScaler>();scaler.uiScaleMode=CanvasScaler.ScaleMode.ScaleWithScreenSize;scaler.referenceResolution=new Vector2(1280,720);scaler.screenMatchMode=CanvasScaler.ScreenMatchMode.MatchWidthOrHeight;scaler.matchWidthOrHeight=1;
 if(EventSystem.current==null){var es=new GameObject("HUD EventSystem",typeof(EventSystem),typeof(InputSystemUIInputModule));es.transform.SetParent(root.transform,false);es.GetComponent<InputSystemUIInputModule>().AssignDefaultActions();}
 play=Box("Player HUD",root.transform,Vector2.zero,Vector2.zero,Vector2.zero,Vector2.zero,false).gameObject;var pr=play.GetComponent<RectTransform>();pr.anchorMin=Vector2.zero;pr.anchorMax=Vector2.one;pr.offsetMin=pr.offsetMax=Vector2.zero;
 var status=Box("Status",play.transform,new Vector2(0,1),new Vector2(0,1),new Vector2(252,80),new Vector2(20,-20));groups.Add(status);
 level=TextAt(status,"Level","",17,new Vector2(12,-8),new Vector2(58,24),gold);health=TextAt(status,"Health","",19,new Vector2(78,-8),new Vector2(162,28));hp=Bar(status,"HealthFill",new Vector2(12,-40),new Vector2(228,13),new Color(.8f,.26f,.28f));xp=Bar(status,"Experience",new Vector2(12,-65),new Vector2(228,4),new Color(.16f,.7f,.68f));
 var corner=Box("Area",play.transform,Vector2.one,Vector2.one,new Vector2(250,85),new Vector2(-20,-20));groups.Add(corner);region=TextAt(corner,"Region","",18,new Vector2(12,-6),new Vector2(230,26),gold);SmallButton(corner,"M 路线",new Vector2(10,-38),new Vector2(104,34),()=>SetDetails("路线"));SmallButton(corner,"F1 帮助",new Vector2(125,-38),new Vector2(115,34),()=>SetDetails("帮助"));
 var objective=Box("CraftingTarget",play.transform,Vector2.one,Vector2.one,new Vector2(250,92),new Vector2(-20,-115));targetPanel=objective.gameObject;groups.Add(objective);targetIcon=ImageAt(objective,"Icon",new Vector2(8,-12),new Vector2(26,26),Color.white);targetText=TextAt(objective,"TargetText","",15,new Vector2(40,-6),new Vector2(200,49),gold);SmallButton(objective,"目标详情",new Vector2(10,-57),new Vector2(104,28),()=>SetDetails("目标"));SmallButton(objective,"取消目标",new Vector2(125,-57),new Vector2(115,28),()=>CraftingTargets.Clear(hero));
 var actions=Box("Actions",play.transform,new Vector2(.5f,0),new Vector2(.5f,0),new Vector2(550,96),new Vector2(0,16));groups.Add(actions);
 main=MakeSlot(actions,"主武器","鼠1",9,()=>combat.Strike());reserve=MakeSlot(actions,"副武器","V",99,()=>combat.SwitchWeapon());skill=MakeSlot(actions,"技能","F",189,()=>combat.UseSkill());roll=MakeSlot(actions,"翻滚","空格",279,()=>hero.Dodge.TryDodge(hero.MoveDirection));potion=MakeSlot(actions,"药水","Q",369,()=>{if(hero.Inventory.PotionOnQuickbar)hero.Inventory.UseHealthPotion();});supply=MakeSlot(actions,"补给","B",459,()=>hero.Inventory.OpenPage(PlayerInventory.Page.Items));
 var ctx=Box("Context",play.transform,new Vector2(.5f,0),new Vector2(.5f,0),new Vector2(600,110),new Vector2(0,126));context=ctx.gameObject;groups.Add(ctx);contextIcon=ImageAt(ctx,"Target",new Vector2(14,-18),new Vector2(34,34),Color.white);contextIcon.preserveAspect=true;prompt=TextAt(ctx,"Primary","",20,new Vector2(64,-10),new Vector2(520,57));secondary=TextAt(ctx,"Secondary","",17,new Vector2(64,-67),new Vector2(520,35),gold);progress=Bar(ctx,"ExtractionProgress",new Vector2(14,-98),new Vector2(572,5),new Color(.2f,.72f,.75f));
 var n=Box("Messages",play.transform,new Vector2(.5f,0),new Vector2(.5f,0),new Vector2(600,52),new Vector2(0,248));notifications=n.gameObject;groups.Add(n);notice=TextAt(n,"Notification","",17,new Vector2(12,-5),new Vector2(480,44));SmallButton(n,"F5 重试",new Vector2(498,-9),new Vector2(90,33),()=>s.Saves.SaveProgress());
 saveIcon=ImageAt(play.transform,"SaveIcon",new Vector2(24,-109),new Vector2(18,18),gold);saveText=TextAt(play.transform,"SaveStatus","",15,new Vector2(48,-108),new Vector2(270,26),muted);
 var d=Box("Details",root.transform,new Vector2(.5f,.5f),new Vector2(.5f,.5f),new Vector2(720,420),Vector2.zero);details=d.gameObject;groups.Add(d);d.GetComponent<Image>().raycastTarget=true;buttons.Add(d);var viewport=Box("DetailViewport",d,Vector2.up,Vector2.up,new Vector2(675,310),new Vector2(22,-20));viewport.pivot=Vector2.up;viewport.GetComponent<Image>().color=Color.clear;viewport.gameObject.AddComponent<RectMask2D>();buttons.Add(viewport);detailText=TextAt(viewport,"DetailsText","",18,Vector2.zero,new Vector2(675,310));detailText.rectTransform.pivot=Vector2.up;var fit=detailText.gameObject.AddComponent<ContentSizeFitter>();fit.verticalFit=ContentSizeFitter.FitMode.PreferredSize;var scroll=viewport.gameObject.AddComponent<ScrollRect>();scroll.viewport=viewport;scroll.content=detailText.rectTransform;scroll.horizontal=false;scroll.movementType=ScrollRect.MovementType.Clamped;SmallButton(d,"关闭",new Vector2(20,-365),new Vector2(120,34),()=>SetDetails(""));SmallButton(d,"UI 100/125/150%",new Vector2(156,-365),new Vector2(220,34),()=>SetUiScale(UiScale<1.1f?1.25f:UiScale<1.4f?1.5f:1));SmallButton(d,"制造目标",new Vector2(396,-365),new Vector2(150,34),()=>SetDetails("目标"));details.SetActive(false);
 }
 public void SetUiScale(float scale){UiScale=Mathf.Clamp(scale,1,1.5f);if(scaler!=null)scaler.referenceResolution=new Vector2(1280,720)/UiScale;}
 public void SetDetails(string page){
  if(page=="诊断"&&!Application.isEditor&&!Debug.isDebugBuild)return;
  if(page==Detail)page="";if(!string.IsNullOrEmpty(page)&&(hero==null||hero.Health.Dead||hero.Inventory.IsOpen||hero.SaveMenuOpen||hero.Progression.IsChoosing||s.Flow.BlockCombat))return;
  if(page!=""&&Detail==""){oldTime=Time.timeScale;oldLock=Cursor.lockState;oldCursor=Cursor.visible;hero.HudPanelOpen=true;Time.timeScale=0;Cursor.lockState=CursorLockMode.None;Cursor.visible=true;}
  if(page==""&&Detail!=""){hero.HudPanelOpen=false;hero.HudClosedFrame=Time.frameCount;if(!hero.Inventory.IsOpen&&!hero.SaveMenuOpen&&!hero.Progression.IsChoosing){Time.timeScale=oldTime;Cursor.lockState=oldLock;Cursor.visible=oldCursor;}}
  Detail=page;if(details!=null)details.SetActive(page!="");nextDetails=0;
 }
 public static bool BlocksPointer(){if(!Running||Instance.hero==null||Cursor.lockState==CursorLockMode.Locked||Mouse.current==null)return false;var pos=Mouse.current.position.ReadValue();foreach(var r in Instance.buttons)if(r!=null&&r.gameObject.activeInHierarchy&&RectTransformUtility.RectangleContainsScreenPoint(r,pos))return true;return false;}
 void SlotState(Slot v,string icon,string name,float cooldown,float duration,bool available=true,string value=""){
  var sprite=icons.Get(icon);if(v.icon.sprite!=sprite)v.icon.sprite=sprite;v.icon.enabled=sprite!=null;v.icon.color=available?Color.white:new Color(.4f,.4f,.4f);Label(v.name,name);v.mask.fillAmount=Mathf.Clamp01(cooldown/Mathf.Max(.1f,duration));Label(v.value,cooldown>0?cooldown.ToString("0.0")+"秒":value);v.button.interactable=available&&cooldown<=0&&!hero.GameplayPaused;
 }
 public double LastUpdateMicroseconds {get;private set;}
 public string SkillIconKey=>skill?.icon.sprite?.name;
 public float SkillMask=>skill==null?0:skill.mask.fillAmount;
 void LateUpdate(){long t=System.Diagnostics.Stopwatch.GetTimestamp();try{RefreshView();}finally{LastUpdateMicroseconds=(System.Diagnostics.Stopwatch.GetTimestamp()-t)*1000000.0/System.Diagnostics.Stopwatch.Frequency;}}
 void RefreshView(){if(root==null)return;var k=Keyboard.current;if(k!=null){if(k.f2Key.wasPressedThisFrame&&Detail!="")SetUiScale(UiScale<1.1f?1.25f:UiScale<1.4f?1.5f:1);if(k.f1Key.wasPressedThisFrame)SetDetails("帮助");if(k.mKey.wasPressedThisFrame)SetDetails("路线");if(k.f3Key.wasPressedThisFrame)SetDetails("诊断");}
  if(Detail!=""&&(hero.Inventory.IsOpen||hero.SaveMenuOpen||hero.Progression.IsChoosing))SetDetails("");
  bool gameplay=s.Flow.ActiveRun!=null&&!s.Flow.HasResult&&!hero.SaveMenuOpen&&!hero.Inventory.IsOpen&&!hero.Progression.IsChoosing&&!s.Flow.Frozen;
  // A save failure is persistent and separate from ordinary notifications, including camp.
  CriticalMessage=!string.IsNullOrEmpty(s.Flow.Error)?s.Flow.Error:s.Saves.SaveFailed?s.Saves.FailureDetail:"";
  play.SetActive(gameplay&&Detail=="");
  if(Detail!=""&&Time.unscaledTime>=nextDetails){nextDetails=Time.unscaledTime+.25f;DrawDetails();}
  if(!play.activeSelf)return;
  Label(health,$"{hero.Health.Current:0} / {hero.Health.maxHealth:0}");Label(level,"Lv."+hero.Progression.Level);hp.fillAmount=hero.Health.Current/hero.Health.maxHealth;xp.fillAmount=(float)hero.Progression.Experience/hero.Progression.RequiredExperience;
  if(Time.unscaledTime>=nextTarget){nextTarget=Time.unscaledTime+.3f;bool tracked=CraftingTargets.Valid(s.Flow.Profile?.craftingTarget);targetPanel.SetActive(tracked);if(tracked){Label(targetText,CraftingTargets.Compact(s));var t=s.Flow.Profile.craftingTarget;targetIcon.sprite=icons.Get(string.IsNullOrEmpty(t.containerId)?AdventureItems.Icon(t.type):AdventureCatalog.Item(t.containerId).iconKey);targetIcon.enabled=targetIcon.sprite!=null;}}
  Label(region,s.Flow.ActiveRun.mode==AdventureMode.ForestExploration?"森林 · 开发中":$"第{s.Wave}波 · 剩余{s.enemies.Count(e=>!e.Health.Dead)}");
  SlotState(main,gear.Main?.Icon,"主武器",combat.AttackRemaining,hero.AttackInterval);SlotState(reserve,gear.Reserve?.Icon,"切换",combat.SwitchRemaining,.7f,gear.Reserve!=null,gear.Reserve==null?"未配置":"");
  SlotState(skill,"skill_"+gear.Weapon.ToString().ToLowerInvariant(),combat.SkillName,combat.SkillRemaining,combat.SkillDuration);SlotState(roll,"dodge","翻滚",hero.Dodge.CooldownRemaining,Mathf.Max(hero.Dodge.duration,hero.Dodge.cooldown));SlotState(potion,"potion","药水",hero.Inventory.PotionCooldownRemaining,hero.Inventory.PotionCooldown,hero.Inventory.PotionOnQuickbar&&hero.Inventory.HealthPotionCount>0,hero.Inventory.PotionOnQuickbar?hero.Inventory.HealthPotionCount.ToString():"未配置");SlotState(supply,"supply","补给",0,1,true,s.Flow.SupplyUsed()+"/"+s.Flow.SupplyLimit);
  resolver.EnsureFresh();resolver.Present();VisibleEId=resolver.DisplayedE?.targetId;VisibleHId=resolver.DisplayedH?.targetId;
  var a=resolver.DisplayedE;var b=resolver.DisplayedH;bool extracting=s.Flow.ActiveRun.phase==RunPhase.Extracting;
  context.SetActive(a!=null||b!=null||extracting);progress.enabled=extracting;context.transform.Find("ExtractionProgressBackground").gameObject.SetActive(extracting);
  if(extracting){float remaining=s.Flow.ActiveRun.extractionRemaining;var x=s.Flow.ExitConfigs().FirstOrDefault(e=>e.id==s.Flow.ActiveRun.exitId);progress.fillAmount=1-remaining/Mathf.Max(.1f,x?.duration??s.Flow.extractionDuration);Label(prompt,$"撤离中   {remaining:0.0} 秒");Label(secondary,a!=null&&a.Signature!=b?.Signature?OfferText(a,"E")+"\n[H] 取消撤离":"["+(a!=null?"E / H":"H")+"] 取消 · 受击或离开会中断");contextIcon.sprite=icons.Get("exit");}
  else{bool same=a!=null&&b!=null&&a.Signature==b.Signature;Label(prompt,OfferText(a??b,same?"E / H":a!=null?"E":"H"));Label(secondary,!same&&a!=null&&b!=null?OfferText(b,"H"):"");contextIcon.sprite=icons.Get((a??b)?.icon);}
  bool compact=UiScale>1.01f;float width=compact?300:600;
  var cr=context.GetComponent<RectTransform>();cr.anchorMin=cr.anchorMax=new Vector2(compact?0:.5f,0);cr.pivot=new Vector2(compact?0:.5f,0);cr.anchoredPosition=new Vector2(compact?20:0,126);
  prompt.rectTransform.sizeDelta=new Vector2(width-80,120);
  secondary.rectTransform.sizeDelta=new Vector2(width-80,100);
  float firstHeight=extracting?30:Mathf.Clamp(prompt.preferredHeight,28,120);
  prompt.rectTransform.sizeDelta=new Vector2(width-80,firstHeight);
  secondary.rectTransform.anchoredPosition=new Vector2(64,-(18+firstHeight));
  secondary.rectTransform.sizeDelta=new Vector2(width-80,100);
  float secondHeight=string.IsNullOrEmpty(secondary.text)?0:Mathf.Clamp(secondary.preferredHeight,24,100);
  float contextHeight=Mathf.Max(extracting?90:56,firstHeight+secondHeight+32);
  context.GetComponent<RectTransform>().sizeDelta=new Vector2(width,contextHeight);
  progress.rectTransform.sizeDelta=new Vector2(width-28,5);
  context.transform.Find("ExtractionProgressBackground").GetComponent<RectTransform>().sizeDelta=progress.rectTransform.sizeDelta;
  progress.rectTransform.anchoredPosition=new Vector2(14,-(contextHeight-12));
  context.transform.Find("ExtractionProgressBackground").GetComponent<RectTransform>().anchoredPosition=progress.rectTransform.anchoredPosition;
  contextIcon.enabled=contextIcon.sprite!=null;
  string message=CriticalMessage!=""?CriticalMessage:hero.Inventory.Notifications.Text;notifications.SetActive(!string.IsNullOrEmpty(message));Label(notice,message);notice.color=CriticalMessage!=""?new Color(1,.65f,.45f):ink;notifications.transform.GetChild(1).gameObject.SetActive(CriticalMessage!="");var nr=notifications.GetComponent<RectTransform>();nr.anchorMin=nr.anchorMax=new Vector2(compact?1:.5f,0);nr.pivot=new Vector2(compact?1:.5f,0);nr.sizeDelta=new Vector2(compact?300:600,compact?(CriticalMessage!=""?122:64):52);nr.anchoredPosition=new Vector2(compact?-20:0,compact?126:context.activeSelf?126+contextHeight+12:126);
  notice.rectTransform.sizeDelta=new Vector2(compact?276:480,compact?70:44);notifications.transform.GetChild(1).GetComponent<RectTransform>().anchoredPosition=new Vector2(compact?12:498,compact?-80:-9);
  Label(saveText,s.Saves.SaveFailed?"保存失败 · 请重试":Time.unscaledTime-s.Saves.LastSavedAt<2?"已保存":"");saveIcon.sprite=icons.Get(s.Saves.SaveFailed?"error":"save");saveIcon.enabled=!string.IsNullOrEmpty(saveText.text);
 }
 string OfferText(InteractionOffer offer,string key){if(offer==null)return "";string line="["+key+"] "+offer.title;if(offer.action==InteractionAction.Repair)line+="\n"+offer.Cost+(offer.executable?" · 仅本局有效":offer.heldWood<offer.wood||offer.heldStone<offer.stone?" · 缺材料":" · "+offer.reason);else if(!offer.executable)line+=" · "+offer.reason;return line;}
 void DrawDetails(){string value="";if(Detail=="帮助")value="操作与规则\n鼠1 普攻 · F 武器技能 · V 切换武器 · 空格 翻滚\nQ 药水 · B/Tab 背包 · C 角色 · WASD 移动 · Shift 跑步\nE 最近互动 · H 当前出口（不需清场）· Esc 释放鼠标\n渡口先修复，再引导撤离；材料为持有/所需，仅本局有效。\n退出保存检查点；失败丢本局战利品，已用材料不恢复。\nM 路线 · F1 帮助 · F2 UI大小 "+(UiScale*100).ToString("0")+"%";
  else if(Detail=="路线"){var layout=GetComponent<ForestRegionRuntime>()?.Layout;value="森林测试 · 地点收益与路线\n"+(layout==null?"当前为波次测试。":string.Join("\n",layout.points.Select(p=>p.label+" · "+(layout.revision>=3?ForestRewards.Summary(p.siteKind):"旧版收益配置")))+"\n\n"+CraftingTargets.Recommendations(s))+"\n普通出口免费；林地西侧渡口木2石1。";}
  else if(Detail=="目标")value=CraftingTargets.Details(s);
  else if(Detail=="诊断"){var run=s.Flow.ActiveRun;value="开发诊断（默认关闭）\nRun "+run?.runId+"\n区域 "+run?.regionInstanceId+"\n种子 "+run?.seed+" 内容 "+run?.contentRevision+"\n检查点 "+s.Flow.Revision+" 坐标 "+hero.transform.position+"\n带入 "+string.Join(",",run?.broughtRemaining??new int[0])+"\n本局 "+string.Join(",",run?.earnedRemaining??new int[0])+"\n恢复不保留飞行弹体/攻击前摇；正式版无诊断入口。";}
  Label(detailText,value);
 }
 void OnDestroy(){if(hero!=null&&Detail!="")SetDetails("");icons?.Dispose();if(flatSprite!=null)Destroy(flatSprite);if(font!=null)Destroy(font);if(root!=null)Destroy(root);if(Instance==this)Instance=null;}
}
