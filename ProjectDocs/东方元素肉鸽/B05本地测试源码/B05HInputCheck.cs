using System;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
public static class B05HInputCheck
{
 static double deadline;static Keyboard keyboard;
 public static void Run(){deadline=EditorApplication.timeSinceStartup+90;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Need(bool b,string m){if(!b)throw new Exception(m);}
 static void H(AdventureFlow flow){var update=typeof(InputSystem).GetMethod("Update",BindingFlags.Static|BindingFlags.NonPublic,null,new[]{typeof(InputUpdateType)},null);InputSystem.QueueStateEvent(keyboard,new KeyboardState(Key.H));update.Invoke(null,new object[]{InputUpdateType.Dynamic});flow.SendMessage("Update");InputSystem.QueueStateEvent(keyboard,new KeyboardState());update.Invoke(null,new object[]{InputUpdateType.Dynamic});}
 static void Tick(){try{if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Native H timeout");if(!EditorApplication.isPlaying||Time.time<.4f)return;var s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;s.Saves.InitializeStorage("C:/Users/guan/Documents/unitytest/B05Validation/h-input",false);s.hero.enabled=false;Need(s.Flow.Depart(AdventureMode.TestChallenge),"H depart");foreach(var e in s.enemies)e.enabled=false;InputSystem.settings.backgroundBehavior=InputSettings.BackgroundBehavior.IgnoreFocus;InputSystem.settings.editorInputBehaviorInPlayMode=InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;keyboard=InputSystem.AddDevice<Keyboard>();InputSystem.EnableDevice(keyboard);s.hero.RestorePosition(new Vector3(25,.1f,25),0);H(s.Flow);Need(s.Flow.ActiveRun.phase==RunPhase.Running&&!s.Camp.InCamp,"Native remote H teleported");s.hero.RestorePosition(s.Flow.ExitPosition,0);H(s.Flow);Need(s.Flow.ActiveRun.phase==RunPhase.Extracting&&s.Flow.ActiveRun.extractionRemaining<=5&&s.Flow.ActiveRun.extractionRemaining>4.5f,"Native legal H not a 5 sec extraction");H(s.Flow);Need(s.Flow.ActiveRun.phase==RunPhase.Running&&s.Flow.Settlement==null,"Native H cancel granted outcome");Debug.Log("B05_V04_NATIVE_H_DISTANCE_START_AND_CANCEL_PASS");typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);InputSystem.RemoveDevice(keyboard);EditorApplication.update-=Tick;EditorApplication.Exit(0);}catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
