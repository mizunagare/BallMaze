using System;
using System.IO;
using System.Linq;
using UnityEngine;
public class T06SmokeDriver : MonoBehaviour
{
 const string Root="C:/Users/guan/Documents/unitytest/T06Validation";
 CombatSession s;int phase;float began;bool read;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]static void Setup(){var args=Environment.GetCommandLineArgs();if(args.Contains("-t06-smoke")||args.Contains("-t06-read")){var o=new GameObject("Validation only smoke driver");var d=o.AddComponent<T06SmokeDriver>();d.read=args.Contains("-t06-read");d.began=Time.realtimeSinceStartup;}}
 void Need(bool b,string m){if(!b)throw new Exception(m);}
 void Clear(){foreach(var e in s.enemies){e.enabled=false;e.experienceReward=0;var boss=e.GetComponent<BossBrain>();if(boss!=null)boss.enabled=false;e.Health.Damage(1000000);e.DropLootOnce();}s.hero.Progression.Clear();}
 void Finish(string marker){Need(s.Saves.SaveProgress(false),"Final build save");File.WriteAllText(Root+"/"+marker+".txt","PASS "+DateTime.UtcNow.ToString("o")+"\nUnity "+Application.unityVersion+"\nwarehouse="+s.Flow.Profile.warehouse.Length+"\nsettlements="+s.Flow.Profile.committedRuns.Length);Debug.Log(marker+" PASS");enabled=false;Application.Quit(0);}
 void Update(){try{
 if(Time.realtimeSinceStartup-began>90)throw new Exception("Build smoke timed out phase="+phase);if(s==null){if(Time.time<.4f)return;s=UnityEngine.Object.FindAnyObjectByType<CombatSession>();if(s==null)return;s.hero.enabled=false;s.Saves.InitializeStorage(Root+"/build-profile",read);s.Saves.autoSaveInterval=10000;
 if(read){Need(s.Flow.AtCamp&&s.Flow.Profile.warehouse.Length==1&&s.Flow.Profile.committedRuns.Length==2&&s.hero.Progression.Level==1,"Player restart ownership mismatch");Finish("BUILD_RESTART_SMOKE");return;}
 Need(s.Flow.AtCamp&&s.hero.GetComponent<FantasyActorVisual>().model!=null,"Fresh camp/model missing");s.hero.Inventory.RestoreInventory(new[]{10,10,10,10,10,10},3,true,0);Need(s.Flow.Depart(AdventureMode.EndlessWaves),"Player departure");phase=1;return;}
 var f=s.Flow;var g=s.hero.GetComponent<AdventureLoadout>();
 if(phase==1){foreach(var e in s.enemies)e.enabled=false;Vector3 pos=s.hero.transform.position;s.hero.GetComponent<CharacterController>().Move(Vector3.forward);Need(Vector3.Distance(pos,s.hero.transform.position)>.5f,"Controller did not move");var c=s.hero.GetComponent<AdventureCombat>();Need(c.Strike(),"Player attack failed");var p=LootPickup.SpawnGear(AdventureItems.New(GearType.Accessory,GearQuality.Red),s.hero.transform.position+Vector3.forward);Need(p.PickUp(s.hero.Inventory),"Player gear pickup");s.hero.Inventory.Add(MaterialKind.Wood,9);Clear();s.hero.RestorePosition(f.ExitPosition,0);f.extractionDuration=.3f;Need(f.BeginExtraction(),"Player extraction failed");phase=2;return;}
 if(phase==2){if(f.Settlement==null)return;Need(f.Settlement.outcome==AdventureOutcome.Extracted&&f.CommitSettlement()&&f.AcknowledgeSettlement(),"Player successful settlement");Need(f.Profile.warehouse.Length==1&&f.Profile.materials[3]==9,"Player reward count");Need(f.Depart(AdventureMode.TestChallenge),"Player redepart");phase=3;return;}
 if(phase==3){s.hero.Health.Damage(1000000);phase=4;return;}
 if(phase==4){if(f.Settlement==null)return;Need(f.Settlement.outcome==AdventureOutcome.Death&&f.CommitSettlement()&&f.AcknowledgeSettlement()&&f.AtCamp,"Player death return");Finish("BUILD_PLAYABLE_LOOP_SMOKE");}
 }catch(Exception ex){Debug.LogException(ex);File.WriteAllText(Root+"/BUILD_SMOKE_FAIL.txt",ex.ToString());enabled=false;Application.Quit(1);}}
}
