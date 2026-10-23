using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class B05CapacityEdgesCheck
{
 static double deadline;static void Need(bool b,string m){if(!b)throw new Exception(m);}
 public static void Run(){deadline=EditorApplication.timeSinceStartup+120;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Tick(){try{if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Capacity timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;s.Saves.InitializeStorage("C:/Users/guan/Documents/unitytest/B05Validation/capacity-"+Guid.NewGuid().ToString("N"),false);var g=s.hero.GetComponent<AdventureLoadout>();var b=s.hero.Inventory;var f=s.Flow;b.RestoreInventory(new[]{0,0,0,0,0,100000000},0,true,0);var salvage=AdventureItems.New(GearType.Accessory,GearQuality.Red);Need(g.Add(salvage),"Limit salvage setup");g.Salvage(salvage);Need(g.items.Contains(salvage)&&b.Count(MaterialKind.Ore)==100000000,"Maximum material limit swallowed salvage");b.RestoreInventory(new[]{5,5,0,297,0,0},5,true,0);Need(f.Depart(AdventureMode.TestChallenge)&&f.SupplyUsed()==6,"Potion supply fixture");Need(!b.CanCraftPotions(1)&&!b.CraftPotions(1)&&b.Count(MaterialKind.MonsterHide)==5&&b.Count(MaterialKind.CrystalShard)==5&&b.HealthPotionCount==5,"Full potion output spent ingredients");while(g.Add(AdventureItems.New(GearType.Accessory,GearQuality.White))){}string layout=JsonUtility.ToJson(new Items{items=g.items.ToArray()});var small=g.items.First(i=>i.definitionId=="bag_gather");Need(!g.EquipContainer(small)&&JsonUtility.ToJson(new Items{items=g.items.ToArray()})==layout,"Shrinking container mutated layout");s.hero.Inventory.SetOpen(false);var loot=LootPickup.SpawnGear(AdventureItems.New(GearType.Accessory,GearQuality.Gold),s.hero.transform.position+Vector3.forward);Need(!loot.PickUp(b)&&!loot.Collected&&g.items.Count(i=>i.id==loot.Gear.id)==0,"Full grid swallowed equipment");Debug.Log("B05_V15_GRID_SHRINK_LOOT_POTION_AND_MAX_MATERIAL_LIMIT_PASS");typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);}catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
 [Serializable]class Items{public GearItem[] items;}
}
