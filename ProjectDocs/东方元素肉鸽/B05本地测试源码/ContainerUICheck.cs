using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
public static class ContainerUICheck {
 static EditorWindow gameView;static int settle,stage=-1,step,resolution;static bool requested;static double deadline;static CombatSession session;static AdventureLoadout gear;static GearItem sword,a,b;static string output;static Vector2 source,target;static MethodInfo queue;
 public static void Run(){Directory.CreateDirectory("C:/Users/guan/Documents/unitytest/ContainerPreview");ShaderUtil.allowAsyncCompilation=false;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");deadline=EditorApplication.timeSinceStartup+240;EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}    static void SetResolution(int width, int height)
    {
        var assembly = typeof(Editor).Assembly;
        Type sizesType = assembly.GetType("UnityEditor.GameViewSizes");
        Type baseType = typeof(ScriptableSingleton<>).MakeGenericType(sizesType);
        object sizes = baseType.GetProperty("instance").GetValue(null);
        Type groupType = assembly.GetType("UnityEditor.GameViewSizeGroupType");
        object group = sizesType.GetMethod("GetGroup").Invoke(sizes, new[] { Enum.Parse(groupType, "Standalone") });
        Type sizeType = assembly.GetType("UnityEditor.GameViewSize");
        Type modeType = assembly.GetType("UnityEditor.GameViewSizeType");
        object size = Activator.CreateInstance(sizeType, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic, null,
            new object[] { Enum.Parse(modeType, "FixedResolution"), width, height, "药水界面检查" }, null);
        group.GetType().GetMethod("AddCustomSize").Invoke(group, new[] { size });
        int index = (int)group.GetType().GetMethod("GetBuiltinCount").Invoke(group, null) + (int)group.GetType().GetMethod("GetCustomCount").Invoke(group, null) - 1;
        gameView = EditorWindow.GetWindow(assembly.GetType("UnityEditor.GameView"));
        gameView.position = new Rect(20, 20, width + 20, height + 50);
        gameView.GetType().GetProperty("selectedSizeIndex", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic).SetValue(gameView, index);
        gameView.Show(); gameView.Repaint();
        settle = 0;
    }

 static Vector2 Point(bool board,int x,int y){float left=CombatUI.Width/2-560+28,top=CombatUI.Height/2-335+128;float cell=board?39:31.5f;return new Vector2(left+(board?0:386)+(x+.5f)*cell,top+(board?68:64)+(y+.5f)*cell)*CombatUI.Scale;}
 static void Mouse(EventType type,Vector2 p){queue.Invoke(null,new object[]{new Event{type=type,button=0,mousePosition=p,displayIndex=0}});}
 static void Key(){queue.Invoke(null,new object[]{new Event{type=EventType.KeyDown,keyCode=KeyCode.R,character='r'}});queue.Invoke(null,new object[]{new Event{type=EventType.KeyUp,keyCode=KeyCode.R}});}
 static void Require(bool value,string text){if(!value)throw new Exception(text);}
 static void SetupInput(){session.hero.Inventory.SetOpen(false);gear.Starter();gear.SelectMain(gear.items.First(i=>i.type==GearType.Bow));sword=gear.items.First(i=>i.type==GearType.Sword);Require(gear.Move(sword,true,1,1),"UI setup failed");session.hero.Inventory.OpenPage(PlayerInventory.Page.Items);step=0;settle=0;stage=0;}
 static void InputStep(){
  if(++settle<5)return;settle=0;
  switch(step++){
   case 0:Mouse(EventType.MouseDown,Point(true,1,1));break;
   case 1:Require(ContainerInventoryView.SelectedId==sword.id,"Real pointer selection failed at "+Screen.width+"x"+Screen.height);Mouse(EventType.MouseDrag,Point(false,8,4));break;
   case 2:Require(ContainerInventoryView.Dragging,"Real MouseDrag did not start");Key();break;
   case 3:Mouse(EventType.MouseUp,Point(false,8,4));break;
   case 4:Require(!sword.board&&sword.x==8&&sword.y==4&&sword.rotation==1&&!ContainerInventoryView.Dragging,"Real drag + R rotation/drop failed");a=AdventureItems.New(GearType.Accessory,GearQuality.White);b=AdventureItems.New(GearType.Accessory,GearQuality.Green);gear.Add(a);gear.Add(b);Require(gear.Move(a,false,7,6)&&gear.Move(b,false,9,6),"Swap UI setup failed");Mouse(EventType.MouseDown,Point(false,7,6));break;
   case 5:Mouse(EventType.MouseDrag,Point(false,9,6));break;
   case 6:Mouse(EventType.MouseUp,Point(false,9,6));break;
   case 7:Require(a.x==9&&a.y==6&&b.x==7&&b.y==6,"Real pointer swap failed");Mouse(EventType.MouseDown,Point(false,9,6));break;
   case 8:Mouse(EventType.MouseDrag,Vector2.zero);break;
   case 9:Mouse(EventType.MouseUp,Vector2.zero);break;
   case 10:Require(a.x==9&&a.y==6&&!ContainerInventoryView.Dragging,"Outside drop did not cancel");Require(!session.Saves.ConfirmationOpen,"R opened new-game dialog inside bag");Debug.Log("CONTAINER_REAL_GUI_INPUT_PASSED "+Screen.width+"x"+Screen.height);if(resolution==0){resolution=1;SetResolution(1920,1080);SetupInput();}else PrepareCapture(0);break;
  }
 }
 static void PrepareCapture(int index){stage=index+1;settle=0;requested=false;output="C:/Users/guan/Documents/unitytest/ContainerPreview/"+new[]{"Inventory1080","Containers1080","Overflow1080","Inventory720","Containers720","LightRig720"}[index]+".png";if(File.Exists(output))File.Delete(output);
  var hero=session.hero;if(index==0){gear.Starter();hero.Inventory.RestoreInventory(new[]{24,18,6,42,36,28},5,true,0);gear.SelectMain(gear.items.First(i=>i.type==GearType.Bow));var armor=AdventureItems.New(GearType.Armor,GearQuality.Red);gear.Add(armor);gear.Move(armor,true,0,0);var s=gear.items.First(i=>i.type==GearType.Sword);gear.Place(s,true,4,2,1,false,out _);for(int i=0;i<5;i++)gear.Add(AdventureItems.New((GearType)(4+i),(GearQuality)i));ContainerInventoryView.Select(armor.id);hero.Inventory.OpenPage(PlayerInventory.Page.Items);}
  if(index==1||index==4){ContainerInventoryView.Select(gear.items.First(i=>i.definitionId=="rig_light").id);hero.Inventory.OpenPage(PlayerInventory.Page.Equipment);}
  if(index==2){var item=AdventureItems.New(GearType.Staff,GearQuality.Gold);item.overflow=true;item.x=item.y=-1;gear.items.Add(item);hero.Inventory.OpenPage(PlayerInventory.Page.Overflow);}
  if(index==5){Require(gear.EquipContainer(gear.items.First(i=>i.definitionId=="rig_light")),"Light rig screenshot setup failed");session.hero.Inventory.OpenPage(PlayerInventory.Page.Items);ContainerInventoryView.Select(gear.items.First(i=>i.worn&&i.type==GearType.ChestRig).id);}
  if(index==3){SetResolution(1280,720);hero.Inventory.OpenPage(PlayerInventory.Page.Items);}
 }
 static void Tick(){try{
  if(EditorApplication.timeSinceStartup>deadline)throw new Exception("UI check timeout");ShaderUtil.allowAsyncCompilation=false;if(!EditorApplication.isPlaying||Time.time<.4f)return;EditorApplication.QueuePlayerLoopUpdate();
  if(stage==-1){session=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(session==null)return;gear=session.hero.GetComponent<AdventureLoadout>();session.Restart();foreach(var enemy in session.enemies)enemy.enabled=false;session.hero.enabled=false;Application.runInBackground=true;InputSystem.settings.backgroundBehavior=InputSettings.BackgroundBehavior.IgnoreFocus;queue=typeof(EditorGUIUtility).GetMethod("QueueGameViewInputEvent",BindingFlags.Static|BindingFlags.NonPublic|BindingFlags.Public);Require(queue!=null,"Native GUI queue unavailable");SetResolution(1280,720);SetupInput();return;}
  gameView.Repaint();if(stage==0){InputStep();return;}
  if(++settle<100||ShaderUtil.anythingCompiling)return;if(!requested){ScreenCapture.CaptureScreenshot(output);requested=true;return;}if(!File.Exists(output)||new FileInfo(output).Length<2000)return;
  Debug.Log("CONTAINER_UI_CAPTURED "+output);if(stage<6){PrepareCapture(stage);return;}EditorApplication.update-=Tick;EditorApplication.Exit(0);
 }catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}

