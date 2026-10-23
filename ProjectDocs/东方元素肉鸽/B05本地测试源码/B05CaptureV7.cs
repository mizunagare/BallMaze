using System;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
public static class B05CaptureV7
{
 static double deadline;
 public static void Run(){deadline=EditorApplication.timeSinceStartup+90;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string m){if(!b)throw new Exception(m);}
 static void Tick(){try{if(EditorApplication.timeSinceStartup>deadline)throw new Exception("v7 fixture timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;const string root="C:/Users/guan/Documents/unitytest/B05Validation";s.Saves.InitializeStorage(root+"/v7-source",false);s.hero.Inventory.RestoreInventory(new[]{1,1,0,500,1,0},8,true,0);Need(s.Saves.SaveProgress(false),"v7 camp save");Need(JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(s.Saves.SavePath)).version==7,"Expected v7 baseline");File.Copy(s.Saves.SavePath,root+"/fixtures/v7-camp.json",true);Need(s.Flow.Depart(AdventureMode.TestChallenge),"v7 depart");s.hero.Inventory.Add(MaterialKind.Ore,7);Need(s.Saves.SaveProgress(false),"v7 Run save");File.Copy(s.Saves.SavePath,root+"/fixtures/v7-run.json",true);s.Flow.OpenAbandon();s.Flow.ConfirmAbandon();File.Copy(s.Saves.SavePath,root+"/fixtures/v7-pending.json",true);Need(s.Flow.CommitSettlement(),"v7 commit");File.Copy(s.Saves.SavePath,root+"/fixtures/v7-committed.json",true);typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);Debug.Log("B05_V7_RUNTIME_FIXTURES_CAPTURED");EditorApplication.update-=Tick;EditorApplication.Exit(0);}catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
