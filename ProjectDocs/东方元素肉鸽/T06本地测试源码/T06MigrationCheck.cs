using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class T06MigrationCheck
{
 const string Root="C:/Users/guan/Documents/unitytest/T06Validation";static double deadline;
 public static void Run(){deadline=EditorApplication.timeSinceStartup+180;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string text){if(!b)throw new Exception(text);}
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Migration timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;var f=s.Flow;var gear=s.hero.GetComponent<AdventureLoadout>();
 for(int version=1;version<=6;version++){
 string folder=Root+"/migration-v"+version+"-"+Guid.NewGuid().ToString("N");Directory.CreateDirectory(folder);string fixture=Root+"/fixtures/v"+version+".json";var oldEnv=JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(fixture));Need(oldEnv.version==version,"Wrong historical fixture version "+version);var old=JsonUtility.FromJson<CombatSaveData>(oldEnv.payload);File.Copy(fixture,folder+"/save.json");s.Saves.InitializeStorage(folder,true);
 Need(f.Enabled&&f.ActiveRun!=null&&f.ActiveRun.legacyProtected&&f.ActiveRun.mode==AdventureMode.EndlessWaves,"Legacy Run not adopted");Need(s.hero.Progression.Level==old.level&&s.Wave==old.wave&&s.hero.Inventory.Count(MaterialKind.MonsterHide)==old.materials[0],"Legacy progress changed");
 if(version>=2)foreach(var i in old.gear){var now=gear.items.Single(j=>j.id==i.id);Need(now.type==i.type&&now.quality==i.quality&&now.x==i.x&&now.y==i.y,"Legacy identity/layout changed");if(version>=3)Need(now.savedAttack==i.savedAttack&&now.rotation==i.rotation,"Legacy stats/rotation changed");if(version>=4)Need((now.affixes??new int[0]).SequenceEqual(i.affixes??new int[0]),"Legacy affix changed");}
 if(version>=5)Need(s.Camp.Items.Select(i=>i.id).OrderBy(i=>i).SequenceEqual(old.warehouseGear.Select(i=>i.id).OrderBy(i=>i))&&s.Camp.Materials.SequenceEqual(old.warehouseMaterials),"Legacy warehouse changed");if(version==6)Need(s.Camp.CaptureRecipes().SequenceEqual(old.unlockedRecipes.OrderBy(i=>i)),"Legacy recipes changed");
 Need(File.ReadAllText(folder+"/save-v"+version+"-before-adventure-v7.json")==File.ReadAllText(fixture),"Migration backup not raw original");string runId=f.ActiveRun.runId;var ids=gear.items.Select(i=>i.id).OrderBy(i=>i).ToArray();Need(s.Saves.LoadProgress(false)&&f.ActiveRun.runId==runId&&ids.SequenceEqual(gear.items.Select(i=>i.id).OrderBy(i=>i)),"Repeated migration recreated run/items");
 int baseline=s.hero.Inventory.Count(MaterialKind.Ore);s.hero.Inventory.Add(MaterialKind.Ore,7);s.hero.Health.Damage(1000000);f.ResolveTerminal();Need(f.Settlement.legacyProtection&&f.Settlement.lostMaterials[5]==7&&f.Settlement.returnedMaterials[5]==baseline,"Legacy grace leaked into new material");Need(f.CommitSettlement()&&f.AcknowledgeSettlement()&&s.hero.Inventory.Count(MaterialKind.Ore)==baseline,"Legacy failure confiscated old supplies");
 Debug.Log("T06_A10_V"+version+"_PASS historical synthetic runtime fixture, IDs/layout/materials/permanent state preserved");
 }
 Debug.Log("T06_A11_PASS one-time legacy protection, no victory, no duplicated items, new acquisitions excluded");
 typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);
 }catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
