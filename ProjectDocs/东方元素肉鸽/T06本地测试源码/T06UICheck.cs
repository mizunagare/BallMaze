using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
public static class T06UICheck
{
 const string Root="C:/Users/guan/Documents/unitytest/T06Validation";
 static CombatSession s;static EditorWindow view;static MethodInfo queue;static Keyboard keyboard;static int phase,settle,resume,capResolution;static double deadline;static bool requested,restart;static string label,output;
 static Vector2? release;
 static AdventureFlow F=>s.Flow;static AdventureLoadout G=>s.hero.GetComponent<AdventureLoadout>();static PlayerInventory B=>s.hero.Inventory;
 public static void Run()=>Begin(false);public static void Restart()=>Begin(true);
 static void Begin(bool restore){restart=restore;Directory.CreateDirectory(Root+"/screenshots");deadline=EditorApplication.timeSinceStartup+300;ShaderUtil.allowAsyncCompilation=false;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string m){if(!b)throw new Exception(m);}
 static void Size(int w,int h){typeof(ContainerUICheck).GetMethod("SetResolution",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{w,h});view=(EditorWindow)typeof(ContainerUICheck).GetField("gameView",BindingFlags.Static|BindingFlags.NonPublic).GetValue(null);}
 static void Click(float x,float y){var p=new Vector2(x,y)*CombatUI.Scale;queue.Invoke(null,new object[]{new Event{type=EventType.MouseDown,button=0,mousePosition=p,displayIndex=0}});release=p;Debug.Log("T06_GUI_CLICK "+phase+" "+p+" screen="+Screen.width+"x"+Screen.height+" camp="+F.AtCamp+" open="+B.IsOpen+" page="+B.CurrentPage+" menu="+s.hero.SaveMenuOpen);}
 static void CampButton(){Click(CombatUI.Width/2+399,CombatUI.Height/2-191);}
 static void Confirm(){Click(CombatUI.Width/2+300,CombatUI.Height/2+273);}
 static void InputE(){InputSystem.QueueStateEvent(keyboard,new KeyboardState(Key.E));typeof(InputSystem).GetMethod("Update",BindingFlags.Static|BindingFlags.NonPublic,null,new[]{typeof(InputUpdateType)},null).Invoke(null,new object[]{InputUpdateType.Dynamic});B.SendMessage("Update");InputSystem.QueueStateEvent(keyboard,new KeyboardState());typeof(InputSystem).GetMethod("Update",BindingFlags.Static|BindingFlags.NonPublic,null,new[]{typeof(InputUpdateType)},null).Invoke(null,new object[]{InputUpdateType.Dynamic});}
 static void Clear(){foreach(var e in s.enemies){e.experienceReward=0;e.enabled=false;var brain=e.GetComponent<BossBrain>();if(brain!=null)brain.enabled=false;e.Health.Damage(1000000);e.DropLootOnce();}s.hero.Progression.Clear();}
 static void Capture(string name,int next){label=name;resume=next;phase=900;settle=0;requested=false;capResolution=0;Size(1280,720);}
 static void End(){typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);if(keyboard!=null)InputSystem.RemoveDevice(keyboard);Debug.Log("T06_NATIVE_UI_EVIDENCE_PASSED");EditorApplication.update-=Tick;EditorApplication.Exit(0);}
 static void CaptureTick(){if(++settle<100||ShaderUtil.anythingCompiling)return;if(!requested){output=Root+"/screenshots/"+label+(capResolution==0?"720":"1080")+".png";if(File.Exists(output))File.Delete(output);ScreenCapture.CaptureScreenshot(output);requested=true;return;}if(!File.Exists(output)||new FileInfo(output).Length<2000)return;
 File.WriteAllText(Path.ChangeExtension(output,".txt"),"Live Unity runtime capture; simulated fixture combat/pickups; actual native GUI clicks and E input.\nrevision="+F.Revision+"\nrun="+(F.ActiveRun?.runId??"none")+"\noutcome="+(F.Settlement==null?"none":AdventureFlow.OutcomeLabel(F.Settlement.outcome))+"\nwarehouse="+F.Profile.warehouse.Length+"\npending="+F.Profile.pending.Length+"\nprofile="+F.Profile.profileId);Debug.Log("T06_CAPTURED "+output);
 if(capResolution==0){capResolution=1;Size(1920,1080);settle=0;requested=false;return;}Size(1280,720);phase=resume;settle=0;}
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("UI timeout phase="+phase);ShaderUtil.allowAsyncCompilation=false;if(!EditorApplication.isPlaying)return;EditorApplication.QueuePlayerLoopUpdate();
 if(s==null){if(Time.time<.4f)return;s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;queue=typeof(EditorGUIUtility).GetMethod("QueueGameViewInputEvent",BindingFlags.Static|BindingFlags.NonPublic|BindingFlags.Public);Size(1280,720);Application.runInBackground=true;s.Saves.InitializeStorage(Root+"/ui-state",restart);s.hero.enabled=false;InputSystem.settings.backgroundBehavior=InputSettings.BackgroundBehavior.IgnoreFocus;InputSystem.settings.editorInputBehaviorInPlayMode=InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;keyboard=InputSystem.AddDevice<Keyboard>();InputSystem.EnableDevice(keyboard);
 if(restart){Need(F.AtCamp&&F.Profile.warehouse.Length==200&&F.Profile.pending.Length==2,"Restart counts wrong");phase=50;return;}
 B.RestoreInventory(new[]{5,12,2,10,10,10},3,true,0);var sword=AdventureItems.New(GearType.Sword,GearQuality.Purple);sword.affixes=new[]{0};Need(G.Add(sword)&&G.SelectMain(sword),"UI sword seed");G.SelectReserve(G.items.First(i=>i.type==GearType.Bow));var armor=AdventureItems.New(GearType.Armor,GearQuality.Green);G.Add(armor);G.AutoMove(armor);B.OpenPage(PlayerInventory.Page.Camp);s.Saves.SaveProgress(false);phase=0;return;}
 view.Repaint();if(release.HasValue){queue.Invoke(null,new object[]{new Event{type=EventType.MouseUp,button=0,mousePosition=release.Value,displayIndex=0}});release=null;return;}if(phase==900){CaptureTick();return;}if(++settle<10)return;settle=0;
 switch(phase){
 case 0:CampButton();phase=1;break;
 case 1:Need(F.Preparing,"Native preparation button failed");Capture("Departure",2);break;
 case 2:Confirm();phase=3;break;
 case 3:Need(F.ActiveRun!=null,"Native departure confirm failed");foreach(var e in s.enemies)e.enabled=false;var loot=LootPickup.SpawnGear(AdventureItems.New(GearType.Accessory,GearQuality.Red),s.hero.transform.position+Vector3.forward);Need(loot.PickUp(B),"Evidence pickup");B.Add(MaterialKind.Wood,9);Clear();s.hero.RestorePosition(F.ExitPosition,0);InputE();Need(F.ActiveRun.phase==RunPhase.Extracting,"Actual E extraction failed");Time.timeScale=0;Capture("ExtractionCountdown",4);break;
 case 4:Time.timeScale=1;phase=5;break;
 case 5:if(F.Settlement==null)break;Capture("SuccessSettlement",6);break;
 case 6:Confirm();phase=7;break;
 case 7:Need(F.Settlement.status==SettlementStatus.Committed,"Native commit failed");Confirm();phase=8;break;
 case 8:Need(F.AtCamp&&!F.HasResult,"Native return camp failed");CampButton();phase=9;break;
 case 9:Confirm();phase=10;break;
 case 10:Need(F.ActiveRun!=null,"Second native departure failed");var lost=LootPickup.SpawnGear(AdventureItems.New(GearType.Arms,GearQuality.Purple),s.hero.transform.position+Vector3.forward);Need(lost.PickUp(B),"Loss fixture pickup");B.Add(MaterialKind.CrystalShard,4);s.hero.Health.Damage(1000000);phase=11;break;
 case 11:if(F.Settlement==null)break;Need(F.Settlement.outcome==AdventureOutcome.Death,"UI death not locked");Capture("DeathSettlement",12);break;
 case 12:Confirm();phase=13;break;
 case 13:Confirm();phase=14;break;
 case 14:Need(F.AtCamp&&!F.HasResult,"Death native camp return");s.Camp.Restore(Enumerable.Range(0,200).Select(_=>AdventureItems.New(GearType.Accessory,GearQuality.White)).ToArray(),new int[6]);s.Saves.SaveProgress(false);CampButton();phase=15;break;
 case 15:Confirm();phase=16;break;
 case 16:Need(F.ActiveRun!=null,"Full stash departure");foreach(var t in new[]{GearType.Accessory,GearType.Staff}){var p=LootPickup.SpawnGear(AdventureItems.New(t,GearQuality.Red),s.hero.transform.position+Vector3.forward);Need(p.PickUp(B),"Full pending fixture pickup");}Clear();s.hero.RestorePosition(F.ExitPosition,0);InputE();phase=17;break;
 case 17:if(F.Settlement==null)break;Confirm();phase=18;break;
 case 18:Confirm();phase=19;break;
 case 19:Need(F.AtCamp&&F.Profile.pending.Length==2&&F.Profile.warehouse.Length==200,"Pending overflow counts");Click(CombatUI.Width/2+64,CombatUI.Height/2-147);phase=20;break;
 case 20:Click(CombatUI.Width/2-332,CombatUI.Height/2-37);Capture("FullWarehousePending",21);break;
 case 21:Need(!F.Depart(AdventureMode.EndlessWaves),"UI pending bypass");s.Saves.SaveProgress(false);End();break;
 case 50:Click(CombatUI.Width/2+64,CombatUI.Height/2-147);phase=51;break;
 case 51:Click(CombatUI.Width/2-332,CombatUI.Height/2-37);Capture("RestartRestoredPending",52);break;
 case 52:End();break;
 }
 }catch(Exception e){Debug.LogException(e);if(s!=null)typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
