using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class T06RegWorkbenchCheck
{
 const string Root="C:/Users/guan/Documents/unitytest/T06Validation/regression/workbench";static double deadline;static bool read;
 public static void Run()=>Begin(false);public static void Read()=>Begin(true);
 static void Begin(bool value){read=value;deadline=EditorApplication.timeSinceStartup+150;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Require(bool value,string message){if(!value)throw new Exception(message);}
 static void Finish(CombatSession s,string message){typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);Debug.Log(message);EditorApplication.update-=Tick;EditorApplication.Exit(0);}
 static int[] Bag(PlayerInventory bag)=>Enumerable.Range(0,6).Select(i=>bag.Count((MaterialKind)i)).ToArray();
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Workbench timeout");if(!EditorApplication.isPlaying||Time.time<.5f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;s.Flow.LegacyHarness=true;var hero=s.hero;var gear=hero.GetComponent<AdventureLoadout>();var camp=s.Camp;var bag=hero.Inventory;
 Require(AdventureRecipes.All.Length==29&&AdventureRecipes.All.Select(r=>r.recipeId).Distinct().Count()==29,"Missing/duplicate data definitions");
 if(read){s.Saves.InitializeStorage(Root+"/run",true);Require(camp.CaptureRecipes().Length==29&&s.Wave==1&&hero.Progression.Level==1&&bag.Count(MaterialKind.Ore)==0,"Permanent recipes not restored across process/new run");Require(camp.Items.Count==1&&camp.Items[0].quality==GearQuality.Red,"Existing warehouse lost");Require(!gear.CanCraft(GearType.Sword,GearQuality.Purple),"Advanced craft allowed outside camp after load");Finish(s,"WORKBENCH_CROSS_PROCESS_ALL_29_UNLOCKS_NEW_RUN_AND_WAREHOUSE_PASSED");return;}
 s.Restart();hero.enabled=false;foreach(var e in s.enemies)e.enabled=false;bag.RestoreInventory(new[]{2000,2000,2000,2000,2000,2000},4,true,0);Directory.CreateDirectory(Root+"/run");s.Saves.InitializeStorage(Root+"/run",false);camp.RestoreRecipes(null);
 var before=Bag(bag);int count=gear.items.Count;Require(!gear.CanCraft(GearType.Sword,GearQuality.Purple)&&!gear.Craft(GearType.Sword,GearQuality.Red)&&before.SequenceEqual(Bag(bag))&&gear.items.Count==count,"Locked craft spent materials or created item");
 for(int t=0;t<9;t++)for(int q=0;q<2;q++){Require(gear.Craft((GearType)t,(GearQuality)q),"Basic field recipe regressed");gear.items.RemoveAt(gear.items.Count-1);}
 foreach(string id in AdventureCatalog.ContainerIds)if(!AdventureRecipes.Advanced(AdventureCatalog.Container(id).quality)){Require(gear.CraftContainer(id),"Basic container craft regressed");gear.items.RemoveAt(gear.items.Count-1);}
 Require(!camp.UnlockRecipe("gear_sword_2"),"Unlock allowed in battle/outside camp");
 foreach(var e in s.enemies){e.experienceReward=0;e.Health.Damage(100000);e.DropLootOnce();}hero.Progression.Clear();Require(camp.Enter(),"Cannot enter workbench camp");
 before=Bag(bag);Require(!camp.UnlockRecipe("gear_sword_3")&&before.SequenceEqual(Bag(bag)),"Skipped prerequisite spent materials");Require(camp.UnlockRecipe("gear_sword_2"),"Purple research failed");before=Bag(bag);Require(!camp.UnlockRecipe("gear_sword_2")&&before.SequenceEqual(Bag(bag)),"Duplicate unlock charged twice");
 int ore=bag.Count(MaterialKind.Ore);bag.TryRemove(MaterialKind.Ore,ore);before=Bag(bag);Require(!camp.UnlockRecipe("gear_staff_2")&&before.SequenceEqual(Bag(bag)),"Insufficient research spent partial materials");bag.Add(MaterialKind.Ore,ore);
 var field=typeof(CombatSaveSystem).GetField("folder",BindingFlags.Instance|BindingFlags.NonPublic);string folder=(string)field.GetValue(s.Saves),bad=Root+"/not-directory";File.WriteAllText(bad,"fixture");field.SetValue(s.Saves,bad);before=Bag(bag);count=gear.items.Count;
 Require(!camp.UnlockRecipe("gear_staff_2")&&!camp.Knows("gear_staff_2")&&camp.Knows("gear_sword_2")&&before.SequenceEqual(Bag(bag)),"Failed unlock not rolled back");Require(!gear.Craft(GearType.Sword,GearQuality.Purple)&&gear.items.Count==count&&before.SequenceEqual(Bag(bag)),"Failed manufacture not rolled back");field.SetValue(s.Saves,folder);
 // Every advanced equipment recipe + both advanced containers must pass backend guards.
 foreach(var recipe in AdventureRecipes.All.OrderBy(r=>(int)r.quality)){
 if(!camp.Knows(recipe.recipeId))Require(camp.UnlockRecipe(recipe.recipeId),"Cannot unlock "+recipe.recipeId);
 int n=gear.items.Count;Require(string.IsNullOrEmpty(recipe.containerId)?gear.Craft(recipe.type,recipe.quality):gear.CraftContainer(recipe.containerId),"Cannot manufacture "+recipe.recipeId);Require(gear.items.Count==n+1,"Manufacture count wrong");var item=gear.items.Last();Require(item.quality==recipe.quality&&item.type==recipe.type,"Manufacture wrong quality/type");gear.items.Remove(item);
 }
 Require(camp.CaptureRecipes().Length==29,"Missing permanent unlocks");
 while(gear.Add(AdventureItems.New(GearType.Accessory,GearQuality.White))){}before=Bag(bag);Require(!gear.Craft(GearType.Sword,GearQuality.Purple)&&before.SequenceEqual(Bag(bag)),"Full bag spent resources");gear.Starter();
 var relic=AdventureItems.New(GearType.Bow,GearQuality.Red);Require(gear.Add(relic)&&camp.DepositEquipment(relic.id),"Warehouse regression");
 bag.SetOpen(false);before=Bag(bag);Require(!gear.Craft(GearType.Sword,GearQuality.Purple)&&before.SequenceEqual(Bag(bag)),"Unlocked advanced craft bypassed camp restriction");
 s.Saves.RequestNewGame();Require(s.Saves.ConfirmNewGame()&&camp.CaptureRecipes().Length==29&&camp.Items.Count==1,"New run erased recipes/warehouse");Require(s.Saves.SaveProgress(false)&&s.Saves.LoadProgress(false)&&camp.CaptureRecipes().Length==29,"V6 save/read failed");var envelope=JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(s.Saves.SavePath));Require(envelope.version==6,"Wrong schema");
 Finish(s,"WORKBENCH_BASIC_18_ADVANCED_29_PREREQUISITES_ATOMICITY_FULL_BAG_NEW_RUN_V6_PASSED");
 }catch(Exception ex){Debug.LogException(ex);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
