using System;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class B05BlockedRecoveryCheck
{
 static double deadline;
 public static void Run(){deadline=EditorApplication.timeSinceStartup+120;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string s){if(!b)throw new Exception(s);}
 static void Tick(){try{if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Recovery timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;string root="C:/Users/guan/Documents/unitytest/B05Validation/blocked-"+Guid.NewGuid().ToString("N");s.Saves.InitializeStorage(root,false);Need(s.Saves.SaveProgress(false),"Seed blocked fixture");string raw=File.ReadAllText(s.Saves.SavePath);File.WriteAllText(s.Saves.SavePath,"bad primary");File.WriteAllText(s.Saves.BackupPath,"bad backup");Need(!s.Saves.LoadProgress(false)&&s.Flow.Enabled&&!string.IsNullOrEmpty(s.Flow.Error)&&Time.timeScale==0&&s.hero.SaveMenuOpen,"Corrupt recovery not visibly blocked");Need(!s.Saves.SaveProgress(false)&&File.ReadAllText(s.Saves.SavePath)=="bad primary"&&File.ReadAllText(s.Saves.BackupPath)=="bad backup","Broken originals overwritten");s.Flow.OpenPreparation();Need(!s.Flow.Preparing,"H bypassed recovery blocker");File.WriteAllText(s.Saves.SavePath,raw);Need(s.Saves.LoadProgress(false)&&s.Flow.AtCamp&&s.Flow.Error==""&&s.Camp.InCamp,"Repaired retry failed");Debug.Log("B05_A09_BOTH_CORRUPT_BLOCK_AND_RETRY_PASS");typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);}catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
