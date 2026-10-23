using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
public static class B05LiveRegression
{
 const string Root="C:/Users/guan/Documents/unitytest/B05Validation";static CombatSession s;static int phase;static double deadline;static Keyboard keyboard;static string main,reserve,run;
 static void Need(bool b,string m){if(!b)throw new Exception(m);}
 public static void Run(){deadline=EditorApplication.timeSinceStartup+150;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Key(bool down){InputSystem.QueueStateEvent(keyboard,down?new KeyboardState(UnityEngine.InputSystem.Key.V):new KeyboardState());typeof(InputSystem).GetMethod("Update",BindingFlags.Static|BindingFlags.NonPublic,null,new[]{typeof(InputUpdateType)},null).Invoke(null,new object[]{InputUpdateType.Dynamic});s.hero.GetComponent<AdventureCombat>().SendMessage("Update");}
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Live regression timeout "+phase);if(!EditorApplication.isPlaying)return;if(s==null){if(Time.time<.4f)return;s=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(s==null)return;}
 var f=s.Flow;var g=s.hero.GetComponent<AdventureLoadout>();var b=s.hero.Inventory;var c=s.hero.GetComponent<AdventureCombat>();
 if(phase==0){
 // Reuse exact grid/drag/rotate/swap controller assertions from batch one, before enabling lifecycle.
 typeof(ContainerRuntimeCheck).GetField("session",BindingFlags.NonPublic|BindingFlags.Static).SetValue(null,s);typeof(ContainerRuntimeCheck).GetField("gear",BindingFlags.NonPublic|BindingFlags.Static).SetValue(null,g);foreach(var method in new[]{"DefinitionAndGridTests","ContainerTests"})typeof(ContainerRuntimeCheck).GetMethod(method,BindingFlags.NonPublic|BindingFlags.Static).Invoke(null,null);
 s.Saves.InitializeStorage(Root+"/live-v7",false);s.hero.enabled=false;b.RestoreInventory(new[]{20,20,0,20,20,20},3,true,0);b.OpenPage(PlayerInventory.Page.Camp);Need(s.Camp.UnlockRecipe("gear_sword_2")&&g.Craft(GearType.Sword,GearQuality.Purple),"Live v7 camp workbench failed");Need(g.SelectReserve(g.items.First(i=>i.type==GearType.Bow)),"Live reserve selection");Need(f.Depart(AdventureMode.EndlessWaves),"Live departure");foreach(var e in s.enemies)e.enabled=false;
 InputSystem.settings.backgroundBehavior=InputSettings.BackgroundBehavior.IgnoreFocus;InputSystem.settings.editorInputBehaviorInPlayMode=InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;keyboard=InputSystem.AddDevice<Keyboard>();phase=1;return;}
 if(phase==1){Need(c.UseSkill(),"Live skill start");main=g.mainWeapon;reserve=g.reserveWeapon;Key(true);Need(g.mainWeapon==reserve&&g.reserveWeapon==main&&c.SkillRemaining>6&&!c.UseSkill()&&!c.SwitchWeapon(),"Live V reset cooldown");Key(false);c.RestoreCooldown(5,1,.6f);run=f.ActiveRun.runId;Need(s.Saves.SaveProgress(false)&&s.Saves.LoadProgress(false),"Live v7 roundtrip");Need(f.ActiveRun.runId==run&&g.mainWeapon==reserve&&g.reserveWeapon==main&&c.SkillRemaining>4.8f&&c.AttackRemaining>.8f&&c.SwitchRemaining>.4f,"Live v7 cooldown not restored");Need(!c.SwitchWeapon()&&!c.UseSkill()&&!c.Strike(),"Live immediate actions bypass cooldown");s.hero.Health.Damage(1000000);f.ResolveTerminal();Need(f.CommitSettlement()&&f.AcknowledgeSettlement()&&s.Camp.Knows("gear_sword_2"),"Permanent recipe erased on death");Debug.Log("B05_A13_PASS native V + v7 same-Run slots and all combat cooldowns");
 // Artificial v6 anomaly fixture; raw original archived before normalization.
 var env=JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(Root+"/fixtures/v6.json"));var data=JsonUtility.FromJson<CombatSaveData>(env.payload);var invalid=data.gear.First(i=>!i.worn&&i.id!=data.mainWeapon&&i.id!=data.reserveWeapon);string invalidId=invalid.id;invalid.x=999;var missing=AdventureItems.New(GearType.Accessory,GearQuality.Red);missing.definitionId="missing_t06_fixture";string missingId=missing.id;data.gear=data.gear.Concat(new[]{missing}).ToArray();env.payload=JsonUtility.ToJson(data);env.checksum=(string)typeof(CombatSaveSystem).GetMethod("Checksum",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,new object[]{env.payload});string raw=JsonUtility.ToJson(env,true);string folder=Root+"/anomaly-"+Guid.NewGuid().ToString("N");Directory.CreateDirectory(folder);File.WriteAllText(folder+"/save.json",raw);s.Saves.InitializeStorage(folder,true);
 Need(f.ActiveRun!=null&&g.items.Single(i=>i.id==invalidId).overflow&&f.Profile.pending.Single().item.id==missingId,"Migration anomaly silently lost item");Need(File.ReadAllText(folder+"/save-v6-before-adventure-v7.json")==raw,"Raw anomalous backup missing");s.hero.Health.Damage(1000000);f.ResolveTerminal();Need(f.CommitSettlement()&&f.AcknowledgeSettlement()&&s.Saves.LoadProgress(false),"Anomaly settlement/reload");Need(g.items.Single(i=>i.id==invalidId).overflow&&f.Profile.pending.Single().item.id==missingId&&!f.Depart(AdventureMode.EndlessWaves)&&!f.ClaimPending(f.Profile.pending[0].pendingId,false),"Recovery pending/layout protection bypass");Debug.Log("B05_A14_PASS grid drag/rotation/swap/container replacement; invalid anchors visible after death; missing template persistent recovery");
 typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);InputSystem.RemoveDevice(keyboard);EditorApplication.update-=Tick;EditorApplication.Exit(0);}
 }catch(Exception e){Debug.LogException(e);if(s!=null)typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(s.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
