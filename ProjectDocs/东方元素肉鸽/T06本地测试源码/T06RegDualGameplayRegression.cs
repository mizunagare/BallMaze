using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using Object=UnityEngine.Object;
public static class T06RegDualGameplayRegression
{
 static int phase,shotType;static float until,before;static double deadline;static CombatSession session;static AdventureLoadout gear;static AdventureCombat combat;
 const string Folder="C:/Users/guan/Documents/unitytest/T06Validation/regression/dual/gameplay";
 public static void Run(){phase=0;deadline=EditorApplication.timeSinceStartup+120;EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Require(bool value,string text){if(!value)throw new Exception(text);}
 static void Done(string text){Debug.Log("CONTAINER_GAMEPLAY_REGRESSION_PASSED "+text);typeof(CombatSaveSystem).GetField("initialized",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic).SetValue(session.Saves,false);EditorApplication.update-=Tick;EditorApplication.Exit(0);}
 static void Tick(){try{
 if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Gameplay regression timeout");if(!EditorApplication.isPlaying||Time.time<.5f)return;
 if(session==null){session=Object.FindFirstObjectByType<CombatSession>();if(session==null)return;session.Flow.LegacyHarness=true;gear=session.hero.GetComponent<AdventureLoadout>();combat=session.hero.GetComponent<AdventureCombat>();}
 var hero=session.hero;var bag=hero.Inventory;
 if(phase==0){session.Restart();hero.enabled=false;foreach(var e in session.enemies)e.enabled=false;
  var enemy=session.enemies[0];enemy.Health.maxHealth=10000;enemy.RestoreState(new SavedEnemy{position=new Vector3(0,.1f,-5.5f),yaw=0,health=10000});enemy.enabled=false;hero.RestorePosition(new Vector3(0,.1f,-7),0);Physics.SyncTransforms();before=enemy.Health.Current;
  Require(combat.Strike()&&enemy.Health.Current<before,"Sword attack regressed");Require(!combat.Strike(),"Attack cooldown bypassed");before=enemy.Health.Current;Require(combat.UseSkill()&&enemy.Health.Current<before&&!combat.UseSkill(),"Sword skill regressed");
  bag.SetOpen(true);Require(!combat.Strike()&&!combat.UseSkill(),"Bag no longer pauses combat");bag.SetOpen(false);shotType=1;phase=1;until=Time.time+.2f;return;
 }        if(phase==1&&Time.time>=until){
            var enemy=session.enemies[0];hero.RestorePosition(new Vector3(0,.1f,-7),0);combat.ResetCombat();
            gear.SelectMain(gear.items.First(i=>i.type==(GearType)shotType));combat.ResetCombat();
            Require(hero.GetComponent<FantasyActorVisual>().model.GetComponentsInChildren<Transform>().Any(t=>t.name=="主武器外观"),"Weapon model missing");
            float z=shotType==1?-4.2f:-.5f;enemy.RestoreState(new SavedEnemy{position=new Vector3(0,.1f,z),yaw=0,health=10000});enemy.enabled=false;Physics.SyncTransforms();
            before=enemy.Health.Current;Require(combat.Strike(),"Weapon attack rejected");phase=2;until=Time.time+.9f;return;
        }
        if(phase==2&&Time.time>=until){
            Require(session.enemies[0].Health.Current<before,"Weapon damage failed type="+shotType);
            before=session.enemies[0].Health.Current;Require(combat.UseSkill(),"Weapon active rejected");phase=3;until=Time.time+.9f;return;
        }
        if(phase==3&&Time.time>=until){
            Require(session.enemies[0].Health.Current<before,"Active skill damage failed type="+shotType);
            if(++shotType<4){phase=1;until=Time.time+.1f;return;}
            Debug.Log("ADVENTURE_FOUR_WEAPONS_AND_SKILLS_PASSED");
            var node=Object.FindObjectsByType<AdventureResource>(FindObjectsSortMode.None).First(n=>n.nodeId==0);
            hero.RestorePosition(node.transform.position-Vector3.forward*1.3f,0);gear.SelectMain(gear.items.First(i=>i.type==GearType.Sword));combat.ResetCombat();Physics.SyncTransforms();
            Require(gear.EquipContainer(gear.items.First(i=>i.definitionId=="bag_gather")),"Gathering bag equip failed");
            float hp=node.Health;Require(combat.Strike()&&node.Health<hp,"Melee cannot gather");var randomState=UnityEngine.Random.state;int expectedYield=UnityEngine.Random.Range(3,7)+1;UnityEngine.Random.state=randomState;node.Hit(10000,hero);Require(node.Health==0,"Gather node did not deplete");
            var loot=Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).First(l=>l.Kind==MaterialKind.Wood&&l.Gear==null);hero.RestorePosition(loot.transform.position-Vector3.forward*.8f,0);Physics.SyncTransforms();Require(loot.Amount==expectedYield,"Gathering backpack yield bonus failed");int amount=bag.Count(MaterialKind.Wood);Require(loot.PickUp(bag)&&bag.Count(MaterialKind.Wood)>amount&&!loot.PickUp(bag),"Harvest pickup duplicate/missing");
            foreach(var l in Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None)){l.gameObject.SetActive(false);Object.Destroy(l.gameObject);}
            session.RestoreWave(5);foreach(var e in session.enemies)e.enabled=false;
            var boss=session.enemies.First(e=>e.archetype==EnemyArchetype.Boss);boss.experienceReward=0;boss.Health.Damage(100000);boss.DropLootOnce();
            var gearDrops=Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Where(l=>l.Gear!=null).ToArray();Require(gearDrops.Length==1&&gearDrops[0].Gear.quality>=GearQuality.Purple,"Boss did not drop guaranteed epic-or-better gear");boss.DropLootOnce();Require(Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Count(l=>l.Gear!=null)==1,"Boss duplicated gear reward");
            hero.RestorePosition(new Vector3(0,.1f,-7),0);session.Events.RestoreEvents(new[]{new SavedWorldEvent{kind=WorldEventKind.Treasure,position=new Vector3(0,0,-5)}});Physics.SyncTransforms();
            Require(session.Events.Points[0].Interact(hero)&&!session.Events.Points[0].Interact(hero),"Chest interaction repeated or failed");Require(Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None).Count(l=>l.Gear!=null)==2,"Chest missing equipment drop");
            foreach(var l in Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None)){l.gameObject.SetActive(false);Object.Destroy(l.gameObject);}
            Debug.Log("ADVENTURE_BOSS_AND_CHEST_DROPS_PASSED");
            session.RestoreWave(3);foreach(var e in session.enemies)e.enabled=false;
            gear.SelectMain(gear.items.First(i=>i.type==GearType.Bow));hero.RestorePosition(new Vector3(30,.1f,30),0);combat.RestoreCooldown(3);
            bag.RestoreInventory(new[]{40,30,10,123,321,456},3,true,0);
            LootPickup.SpawnGear(AdventureItems.New(GearType.Staff,GearQuality.Gold),new Vector3(31,.5f,30));
            LootPickup.Spawn(MaterialKind.Wood,8,new Vector3(32,.5f,30));
            Directory.CreateDirectory(Folder+"/save");session.Saves.InitializeStorage(Folder+"/save",false);Require(session.Saves.SaveProgress(false),"Version2 save failed");
            Done("ADVENTURE_RUNTIME_AND_SAVE_WRITE_PASSED");
        }
    }catch(Exception e){Debug.LogException(e);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}



