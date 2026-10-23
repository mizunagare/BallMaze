using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using Object=UnityEngine.Object;
public static class T06RegDualWeaponCheck
{
 static CombatSession session;static AdventureLoadout gear;static AdventureCombat combat;static int phase;static float until;static double deadline;static Keyboard keyboard;static string active,reserve;static float cooldown;
 const string Root="C:/Users/guan/Documents/unitytest/T06Validation/regression/dual";
 public static void Run(){deadline=EditorApplication.timeSinceStartup+120;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Require(bool yes,string text){if(!yes)throw new Exception(text);}
 static void Key(bool down){InputSystem.QueueStateEvent(keyboard,down?new KeyboardState(UnityEngine.InputSystem.Key.V):new KeyboardState());typeof(InputSystem).GetMethod("Update",BindingFlags.Static|BindingFlags.NonPublic,null,new[]{typeof(InputUpdateType)},null).Invoke(null,new object[]{InputUpdateType.Dynamic});combat.SendMessage("Update");}
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Dual weapon timeout");if(!EditorApplication.isPlaying||Time.time<.5f)return;
 if(session==null){session=Object.FindFirstObjectByType<CombatSession>();if(session==null)return;session.Flow.LegacyHarness=true;gear=session.hero.GetComponent<AdventureLoadout>();combat=session.hero.GetComponent<AdventureCombat>();}
 var hero=session.hero;
 if(phase==0){session.Restart();hero.enabled=false;foreach(var e in session.enemies)e.enabled=false;
 // Read untouched v3 fixture, then prove old IDs, stats and layouts survive v4 write/read.
 if(File.Exists(Root+"/legacy-v3/save-v3-before-containers.json"))File.Copy(Root+"/legacy-v3/save-v3-before-containers.json",Root+"/legacy-v3/save.json",true);session.Saves.InitializeStorage(Root+"/legacy-v3",true);Require(gear.Main.type==GearType.Bow&&gear.Reserve==null&&Mathf.Abs(hero.AttackPower-41)<.01f,"V3 migration changed old stats/main");Require(File.Exists(Root+"/legacy-v3/save-v3-before-containers.json"),"V3 migration archive missing");
 string snapshot=JsonUtility.ToJson(new Items{gear=gear.items.ToArray()});Require(session.Saves.SaveProgress(false)&&session.Saves.LoadProgress(false),"V3 to V4 save/read failed");Require(snapshot==JsonUtility.ToJson(new Items{gear=gear.items.ToArray()}),"V3 item identity/layout/stats changed");
 gear.Starter();hero.Inventory.RestoreInventory(new[]{50,50,50,50,50,50},4,true,0);hero.RestorePosition(new Vector3(0,.1f,-7),0);foreach(var e in session.enemies)e.enabled=false;
 var sword=gear.Main;var bow=gear.items.First(i=>i.type==GearType.Bow);Require(gear.SelectReserve(bow),"Cannot assign reserve");float attack=gear.Attack;bow.savedAttack=999;Require(gear.Attack==attack,"Reserve leaked stats");Require(!gear.Move(bow,true,0,0),"Reserve allowed on board");int count=gear.items.Count;gear.Salvage(bow);Require(gear.items.Count==count,"Reserve salvaged");Require(!gear.SelectReserve(sword),"Same weapon in two slots");
 combat.ResetCombat();Require(combat.UseSkill(),"Skill refused");cooldown=combat.SkillRemaining;active=sword.id;reserve=bow.id;
 InputSystem.settings.backgroundBehavior=InputSettings.BackgroundBehavior.IgnoreFocus;InputSystem.settings.editorInputBehaviorInPlayMode=InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;keyboard=InputSystem.AddDevice<Keyboard>();InputSystem.EnableDevice(keyboard);Key(false);Key(true);Require(gear.mainWeapon==reserve&&gear.reserveWeapon==active,"Real V did not switch");Require(combat.SkillRemaining>=cooldown-.2f&&!combat.UseSkill()&&!combat.SwitchWeapon()&&!combat.Strike(),"Switch reset cooldown or lacked lock");Key(false);
 hero.Inventory.SetOpen(true);float remain=combat.SwitchRemaining;Require(!combat.SwitchWeapon(),"Paused switch allowed");until=Time.unscaledTime+.4f;cooldown=remain;phase=1;return;
 }
 if(phase==1){if(Time.unscaledTime<until)return;Require(Mathf.Abs(cooldown-combat.SwitchRemaining)<.01f,"Paused cooldown elapsed");hero.Inventory.SetOpen(false);until=Time.time+.8f;phase=2;return;}
 if(phase==2){if(Time.time<until)return;Require(combat.SwitchWeapon()&&gear.mainWeapon==active,"Switch back failed");
 var e=session.enemies[0];e.Health.maxHealth=10000;e.RestoreState(new SavedEnemy{position=new Vector3(0,.1f,-5),health=10000});e.enabled=false;hero.Health.RestoreHealth(30);var item=AdventureItems.New(GearType.Sword,GearQuality.Red);item.affixes=new[]{0,3};float hp=e.Health.Current;WeaponHit.Apply(hero,e,100,e.transform.position,Vector3.forward,item,false);Require(Mathf.Abs(hp-e.Health.Current-115)<.01f&&Mathf.Abs(hero.Health.Current-36.9f)<.01f,"Sharp/lifesteal failed");var copy=item.Clone();copy.affixes[0]=4;Require(item.affixes[0]==0,"Affix clone shared memory");
 item.affixes=new[]{4,5};e.Health.RestoreHealth(3000);hp=e.Health.Current;WeaponHit.Apply(hero,e,100,e.transform.position,Vector3.forward,item,true);Require(Mathf.Abs(hp-e.Health.Current-162.5f)<.01f,"Execute/charged damage failed");
 Require(gear.Add(item),"Engrave setup full");int crystals=hero.Inventory.Count(MaterialKind.CrystalShard);Require(gear.Engrave(item,0)&&item.affixes.SequenceEqual(new[]{0,5})&&hero.Inventory.Count(MaterialKind.CrystalShard)==crystals-2&&!gear.Engrave(item,0)&&hero.Inventory.Count(MaterialKind.CrystalShard)==crystals-2,"Engrave transaction failed");
 // Each type/quality produces distinct exclusive projectiles and melee behavior.
 for(int t=0;t<4;t++)for(int q=0;q<5;q++){AdventureProjectile.Clear(hero.gameObject.scene);var w=AdventureItems.New((GearType)t,(GearQuality)q);Require(w.affixes.Length==(q==0?0:q<3?1:2)&&w.affixes.Distinct().Count()==w.affixes.Length,"Invalid affix roll");gear.Starter();Require(gear.Add(w)&&gear.SelectMain(w),"Quality test equip failed");combat.ResetCombat();Require(combat.UseSkill(),"Quality skill failed");int n=Object.FindObjectsByType<AdventureProjectile>(FindObjectsSortMode.None).Count(p=>p.isActiveAndEnabled);int expected=t==0?(q<2?0:q<3?1:3):t==1?(q==4?1:0):t==2?(q<3?1:3):(q<2?5:q<4?7:9);Require(n==expected,"Quality exclusive shot count wrong "+t+"/"+q+" count="+n);}
 gear.Starter();var red=AdventureItems.New(GearType.Staff,GearQuality.Red);red.affixes=new[]{3,5};Require(gear.Add(red)&&gear.SelectMain(red),"Save setup equip failed");gear.SelectReserve(gear.items.First(i=>i.type==GearType.Bow));combat.RestoreCooldown(5,1,.6f);active=gear.mainWeapon;reserve=gear.reserveWeapon;hero.RestorePosition(new Vector3(30,.1f,30),0);combat.RestoreCooldown(5,1,.6f);hero.Progression.Clear();session.RestoreWave(3);foreach(var enemy in session.enemies)enemy.enabled=false;
 session.Saves.InitializeStorage(Root+"/save-v4",false);Require(session.Saves.SaveProgress(false),"V4 save failed");gear.ClearReserve();red.affixes=new[]{0};Require(session.Saves.LoadProgress(false),"V4 read failed");Require(gear.mainWeapon==active&&gear.reserveWeapon==reserve&&gear.Main.affixes.SequenceEqual(new[]{3,5})&&combat.SkillRemaining>4.5f&&combat.AttackRemaining>.8f&&combat.SwitchRemaining>.4f,"V4 slots/affixes/cooldowns lost");
 Require(JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(session.Saves.SavePath)).version==6,"Schema is not V4");
 
 Debug.Log("DUAL_WEAPON_V_INPUT_PAUSE_AFFIXES_20_SKILLS_V3_V4_SAVE_PASSED");
 typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(session.Saves,false);
 hero.RestorePosition(new Vector3(0,.1f,-7),0);hero.Health.RestoreHealth(30);var target=session.enemies[0];target.Health.maxHealth=10000;target.RestoreState(new SavedEnemy{position=new Vector3(0,.1f,-2),health=10000});target.enabled=false;for(int i=1;i<session.enemies.Length;i++){session.enemies[i].RestoreState(new SavedEnemy{position=new Vector3(20+i,.1f,20),health=1000});session.enemies[i].enabled=false;}Physics.SyncTransforms();
 var source=gear.Main;source.affixes=new[]{0,3};AdventureProjectile.Spawn(hero,hero.transform.position+Vector3.up*1.25f+Vector3.forward*.7f,Vector3.forward,100,0,16,source,false);source.affixes=new[]{5};gear.SelectMain(gear.Reserve);until=Time.time+1;phase=3;return;
 }
 if(phase==3){if(Time.time<until)return;Require(Mathf.Abs(session.enemies[0].Health.Current-9885)<.1f&&Mathf.Abs(hero.Health.Current-36.9f)<.1f,"In-flight projectile lost captured affixes after switch");Debug.Log("DUAL_PROJECTILE_SNAPSHOT_AND_ENGRAVE_ATOMICITY_PASSED");InputSystem.RemoveDevice(keyboard);typeof(CombatSaveSystem).GetField("initialized",BindingFlags.Instance|BindingFlags.NonPublic).SetValue(session.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);
 }
 }catch(Exception ex){Debug.LogException(ex);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
 [Serializable]class Items{public GearItem[] gear;}
}



