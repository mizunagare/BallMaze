using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class T06FirstCheck
{
 static CombatSession s;static int phase;static double deadline;
 const string Root="C:/Users/guan/Documents/unitytest/T06Validation/first";
 public static void Run(){deadline=EditorApplication.timeSinceStartup+120;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string msg){if(!b)throw new Exception(msg);}
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;
 if(s==null){s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;}
 var f=s.Flow;var g=s.hero.GetComponent<AdventureLoadout>();var bag=s.hero.Inventory;
 if(phase==0){s.Saves.InitializeStorage(Root,false);Need(f.AtCamp&&s.Camp.InCamp&&Time.timeScale==0,"New camp failed");Need(s.Saves.SaveProgress(false)&&s.Saves.LoadProgress(false)&&f.AtCamp,"New camp v7 read failed");bag.Add(MaterialKind.Wood,10);Need(f.Depart(AdventureMode.EndlessWaves)&&f.ActiveRun!=null,"Departure failed");bag.Add(MaterialKind.Wood,7);Need(bag.TryRemove(MaterialKind.Wood,9),"Spend failed");Need(f.ActiveRun.broughtRemaining[3]==8&&f.ActiveRun.earnedRemaining[3]==0,"Ledger failed");var newItem=AdventureItems.New(GearType.Accessory,GearQuality.Red);Need(g.Add(newItem),"Loot setup");s.hero.Health.Damage(100000);f.ResolveTerminal();Need(f.Settlement!=null&&f.Settlement.outcome==AdventureOutcome.Death,"Death lock failed");Need(f.CommitSettlement(),"Death commit failed: "+f.Error);Need(f.AcknowledgeSettlement()&&f.AtCamp&&bag.Count(MaterialKind.Wood)==8&&!g.items.Any(i=>i.id==newItem.id),"Death return failed");Need(f.Depart(AdventureMode.EndlessWaves),"Second depart failed");bag.Add(MaterialKind.Stone,9);f.OpenAbandon();f.ConfirmAbandon();Need(f.CommitSettlement()&&f.AcknowledgeSettlement()&&bag.Count(MaterialKind.Stone)==0,"Abandon failed");Need(s.Saves.LoadProgress(false)&&f.AtCamp&&f.Profile.committedRuns.Length==2,"Committed reload failed");
 Debug.Log("T06_FIRST_CONTINUOUS_DEPART_DEATH_CAMP_ABANDON_V7_PASSED");typeof(CombatSaveSystem).GetField("initialized",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);}
 }catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
