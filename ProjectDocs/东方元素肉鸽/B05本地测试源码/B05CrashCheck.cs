using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class B05CrashCheck
{
 const string Root="C:/Users/guan/Documents/unitytest/B05Validation";static string point;static bool read;static double deadline;
 public static void BeforeLock()=>Begin("before-terminal-save",false);public static void AfterLock()=>Begin("after-terminal-save",false);public static void BeforeCommit()=>Begin("before-settlement-save",false);public static void AfterCommit()=>Begin("after-settlement-save",false);
 public static void ReadBeforeLock()=>Begin("before-terminal-save",true);public static void ReadAfterLock()=>Begin("after-terminal-save",true);public static void ReadBeforeCommit()=>Begin("before-settlement-save",true);public static void ReadAfterCommit()=>Begin("after-settlement-save",true);
 static void Begin(string p,bool r){point=p;read=r;deadline=EditorApplication.timeSinceStartup+100;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string m){if(!b)throw new Exception(m);}
 static void Tick(){try{if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Crash fixture timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;string path=Root+"/crash-"+point;s.Saves.InitializeStorage(path,read);var f=s.Flow;
 if(read){if(point=="before-terminal-save"){Need(f.ActiveRun!=null&&f.Settlement==null&&f.Profile.warehouse.Length==0,"Pre-lock boundary mismatch");}else{Need(f.Settlement!=null&&f.Settlement.outcome==AdventureOutcome.Extracted,"Crash lost unique outcome");Need(f.CommitSettlement()&&f.CommitSettlement()&&f.AcknowledgeSettlement()&&f.Profile.warehouse.Length==1&&f.Profile.committedRuns.Length==1,"Crash commit recovery duplicated/lost reward");}Debug.Log("B05_V12_PROCESS_KILL_RECOVERY_PASS "+point);typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);return;}
 s.hero.enabled=false;Need(f.Depart(AdventureMode.TestChallenge),"Crash depart");foreach(var e in s.enemies)e.enabled=false;Need(s.hero.GetComponent<AdventureLoadout>().Add(AdventureItems.New(GearType.Accessory,GearQuality.Gold)),"Crash loot");s.hero.transform.position=f.ExitPosition;Need(f.BeginExtraction(),"Crash start exit");
 f.ValidationHook=boundary=>{if(boundary==point){File.WriteAllText(path+"/kill-marker.txt",boundary+" run="+f.ActiveRun?.runId);System.Diagnostics.Process.GetCurrentProcess().Kill();}};
 f.ActiveRun.extractionRemaining=0;f.SendMessage("Update");f.ResolveTerminal();f.CommitSettlement();throw new Exception("Crash hook did not kill process");
 }catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
