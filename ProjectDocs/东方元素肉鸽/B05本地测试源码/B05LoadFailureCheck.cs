using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class B05LoadFailureCheck
{
 static double deadline;static void Need(bool b,string m){if(!b)throw new Exception(m);}
 public static void Run(){deadline=EditorApplication.timeSinceStartup+120;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Tick(){try{if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Load failure timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;s.Saves.InitializeStorage("C:/Users/guan/Documents/unitytest/B05Validation/load-fault-"+Guid.NewGuid().ToString("N"),false);Need(s.Saves.SaveProgress(false),"Camp baseline");string raw=File.ReadAllText(s.Saves.SavePath);var f=s.Flow;var gear=s.hero.GetComponent<AdventureLoadout>();string[] ids=gear.items.Select(i=>i.id).ToArray();
 f.ValidationHook=p=>{if(p=="before-run-load")throw new IOException("injected run world initialization failure");};Need(!f.Depart(AdventureMode.TestChallenge)&&f.AtCamp&&s.Camp.InCamp&&gear.items.Select(i=>i.id).SequenceEqual(ids),"Run loading failure lost owners");
 f.ValidationHook=p=>{if(p=="before-run-load"||p=="before-camp-load")throw new IOException("injected load and fallback failure");};Need(!f.Depart(AdventureMode.TestChallenge)&&f.ActiveRun==null&&!string.IsNullOrEmpty(f.Error)&&s.hero.SaveMenuOpen&&Time.timeScale==0&&!s.Saves.SaveProgress(false)&&File.ReadAllText(s.Saves.SavePath)==raw,"Fallback failure overwrote original or left playable limbo");f.ValidationHook=null;Need(s.Saves.LoadProgress(false)&&f.AtCamp&&f.Error==""&&gear.items.Select(i=>i.id).SequenceEqual(ids),"Loading failure retry cannot recover");Need(f.Depart(AdventureMode.TestChallenge),"Retry did not create exactly one Run");f.OpenAbandon();f.ConfirmAbandon();f.ValidationHook=p=>{if(p=="before-camp-load")throw new IOException("injected committed camp initialization failure");};Need(!f.CommitSettlement()&&f.ActiveRun==null&&f.Settlement.status==SettlementStatus.Committed,"Camp failed after commit lost durability");f.ValidationHook=null;Need(s.Saves.LoadProgress(false)&&f.AcknowledgeSettlement()&&f.Profile.committedRuns.Length==1,"Committed camp retry duplicated");Debug.Log("B05_V20_RUN_LOAD_ROLLBACK_FALLBACK_FREEZE_AND_COMMITTED_CAMP_RETRY_PASS");typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);}catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
