using System;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
public static class HeroDodgeRuntimeCheck
{
    static CombatSession session; static Keyboard keyboard; static int phase; static double deadline, pausedAt;
    static float began, cooldown; static Vector3 position; static GameObject wall; static Quaternion pose;
    static void Require(bool value,string message){if(!value)throw new Exception(message);}
    public static void Run(){EditorSceneManager.OpenScene("Assets/CombatPrototype/ForestRuins.unity");deadline=EditorApplication.timeSinceStartup+80;EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
    static void Move(Transform actor,Vector3 p){var cc=actor.GetComponent<CharacterController>();cc.enabled=false;actor.position=p;cc.enabled=true;Physics.SyncTransforms();}
    static void Input(params Key[] keys){InputSystem.QueueStateEvent(keyboard,new KeyboardState(keys));typeof(InputSystem).GetMethod("Update",System.Reflection.BindingFlags.Static|System.Reflection.BindingFlags.NonPublic,null,new[]{typeof(InputUpdateType)},null).Invoke(null,new object[]{InputUpdateType.Dynamic});}
    static void Tick(){try{
        if(EditorApplication.timeSinceStartup>deadline)throw new Exception("Dodge check timeout");
        if(!EditorApplication.isPlaying||Time.time<.4f)return;
        session=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(session==null||session.hero.Dodge==null)return;
        var hero=session.hero;var dodge=hero.Dodge;
        if(phase==0){
            Application.runInBackground=true;InputSystem.settings.backgroundBehavior=InputSettings.BackgroundBehavior.IgnoreFocus;InputSystem.settings.editorInputBehaviorInPlayMode=InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;
            session.Restart();session.Waves.BuildWave(5);session.orbit.enabled=false;Camera.main.transform.rotation=Quaternion.Euler(20,90,0);
            foreach(var e in session.enemies){e.enabled=false;var b=e.GetComponent<BossBrain>();if(b!=null)b.enabled=false;Move(e.transform,new Vector3(12,.1f,12));}
            foreach(var p in session.Events.Points)p.gameObject.SetActive(false);
            Move(hero.transform,new Vector3(0,.1f,0));hero.transform.rotation=Quaternion.identity;
            keyboard=InputSystem.AddDevice<Keyboard>();InputSystem.EnableDevice(keyboard);Input();phase=1;return;
        }
        if(phase==1){
            Input(Key.W,Key.Space);hero.SendMessage("Update");Input();
            Require(dodge.IsRolling&&dodge.IsInvulnerable&&Vector3.Dot(dodge.Direction,Vector3.right)>.999f,"Actual Space/W camera-relative dodge failed");
            Require(!dodge.TryDodge(Vector3.forward),"Repeated roll bypassed cooldown");
            var melee=session.enemies.First(e=>e.archetype==EnemyArchetype.Melee);Move(melee.transform,new Vector3(1.3f,.1f,0));
            float enemyHealth=melee.Health.Current;hero.Attack();Require(melee.Health.Current==enemyHealth,"Attacked during roll");
            session.Feedback.ResetFeedback();float health=hero.Health.Current;
            hero.Health.Damage(20);melee.ReleaseAttack();
            var boss=session.enemies.Single(e=>e.archetype==EnemyArchetype.Boss);Move(boss.transform,new Vector3(0,.1f,2));var brain=boss.GetComponent<BossBrain>();
            Require(brain.BeginAttack(BossAttack.Slam),"Slam setup failed");brain.ResolveAttack();
            Require(brain.BeginAttack(BossAttack.Charge),"Charge setup failed");brain.ResolveAttack();brain.AdvanceCharge(.18f);brain.ResetBrain();
            var shot=EnemyProjectile.Fire(melee,hero.transform.position+Vector3.up+Vector3.forward*3,hero.transform.position+Vector3.up,20,10,melee.projectileMaterial);shot.Advance(.5f);
            Require(hero.Health.Current==health&&session.Feedback.DamageNumberCount==0,"Damage/feedback leaked through roll immunity (melee/slam/charge/projectile)");
            foreach(var e in session.enemies)Move(e.transform,new Vector3(12,.1f,12));
            began=Time.time;phase=2;return;
        }
        if(phase==2){
            if(Time.time-began<.09f)return;
            Require(dodge.IsInvulnerable,"Invulnerability ended early");
            var model=hero.GetComponent<FantasyActorVisual>().model;Require(Quaternion.Angle(model.transform.localRotation,Quaternion.identity)>20,"Rolling model did not rotate");
            hero.Inventory.SetOpen(true);pausedAt=EditorApplication.timeSinceStartup;cooldown=dodge.CooldownRemaining;position=hero.transform.position;pose=model.transform.localRotation;phase=3;return;
        }
        if(phase==3){
            if(EditorApplication.timeSinceStartup-pausedAt<.3)return;
            Require(dodge.IsInvulnerable&&Mathf.Abs(dodge.CooldownRemaining-cooldown)<.001f&&Vector3.Distance(position,hero.transform.position)<.001f,"Inventory did not freeze roll/cooldown/immunity");
            Require(Quaternion.Angle(pose,hero.GetComponent<FantasyActorVisual>().model.transform.localRotation)<.1f,"Roll pose moved while paused");
            Require(!dodge.TryDodge(Vector3.back),"Roll input accepted in inventory");hero.Inventory.SetOpen(false);phase=4;return;
        }
        if(phase==4){
            if(Time.time-began<.27f)return;
            Require(dodge.IsRolling&&!dodge.IsInvulnerable,"Roll recovery should be vulnerable");float health=hero.Health.Current;hero.Health.Damage(12);Require(hero.Health.Current==health-12,"Damage ignored after i-frames");phase=5;return;
        }
        if(phase==5){
            if(Time.time-began<.48f)return;
            Require(!dodge.IsRolling&&Mathf.Abs(hero.transform.position.x-4.2f)<.15f&&Mathf.Abs(hero.transform.position.z)<.1f,"Actual roll distance/direction wrong: "+hero.transform.position);
            Require(dodge.CooldownRemaining>0&&!dodge.TryDodge(Vector3.right),"Cooldown ended early");
            Require(Quaternion.Angle(hero.GetComponent<FantasyActorVisual>().model.transform.localRotation,Quaternion.identity)<.5f,"Roll pose did not restore");
            Require(hero.Progression.GrantSkillChoice(),"Skill pause setup failed");pausedAt=EditorApplication.timeSinceStartup;cooldown=dodge.CooldownRemaining;phase=6;return;
        }
        if(phase==6){
            if(EditorApplication.timeSinceStartup-pausedAt<.25)return;
            Require(Mathf.Abs(cooldown-dodge.CooldownRemaining)<.001f&&!dodge.TryDodge(Vector3.forward),"Skill selection did not pause/block dodge");
            Require(hero.Progression.SelectChoice(0),"Skill selection failed");phase=7;return;
        }
        if(phase==7){
            if(dodge.CooldownRemaining>0)return;
            Move(hero.transform,new Vector3(0,.1f,0));hero.transform.rotation=Quaternion.LookRotation(Vector3.forward);
            wall=GameObject.CreatePrimitive(PrimitiveType.Cube);wall.transform.position=new Vector3(0,1.5f,1);wall.transform.localScale=new Vector3(4,3,.2f);Physics.SyncTransforms();
            Require(dodge.TryDodge(Vector3.zero)&&Vector3.Dot(dodge.Direction,Vector3.forward)>.999f,"No-input facing fallback failed");began=Time.time;phase=8;return;
        }
        if(phase==8){
            if(Time.time-began<.48f)return;
            Require(hero.transform.position.z<.6f&&hero.transform.position.z>=0,"Roll crossed wall: "+hero.transform.position);
            UnityEngine.Object.DestroyImmediate(wall);phase=9;return;
        }
        if(phase==9){
            if(dodge.CooldownRemaining>0)return;
            Move(hero.transform,new Vector3(0,.1f,0));Require(dodge.TryDodge(new Vector3(100,0,100)),"Diagonal roll failed");began=Time.time;phase=10;return;
        }
        if(phase==10){
            if(Time.time-began<.48f)return;
            Require(Mathf.Abs(Vector3.ProjectOnPlane(hero.transform.position,Vector3.up).magnitude-4.2f)<.15f,"Diagonal dodge distance wrong: "+hero.transform.position+" magnitude="+Vector3.ProjectOnPlane(hero.transform.position,Vector3.up).magnitude+" time="+(Time.time-began));
            session.Restart();Require(dodge.CooldownRemaining==0&&!dodge.IsRolling&&!dodge.IsInvulnerable,"Restart retained dodge state");
            hero.Health.Damage(9999);Require(hero.Health.Dead&&!dodge.TryDodge(Vector3.forward),"Dead hero can roll");session.Restart();
            Require(dodge.TryDodge(Vector3.forward),"Restart did not restore dodge");session.Waves.BuildWave(2);Require(dodge.IsRolling&&dodge.CooldownRemaining>0,"Wave change reset dodge cooldown");session.Restart();
            Debug.Log("HERO_DODGE_RUNTIME_PASSED: actual Space + camera-relative input, 4.2m/normalized diagonal movement, idle-facing fallback, wall collision, melee/slam/charge/projectile immunity, vulnerable recovery, attack lockout, bag/skill pause, cooldown/wave retention, death protection and restart pose/state reset.");
            InputSystem.RemoveDevice(keyboard);EditorApplication.update-=Tick;EditorApplication.Exit(0);
        }
    }catch(Exception e){Debug.LogException(e);Time.timeScale=1;if(keyboard!=null&&keyboard.added)InputSystem.RemoveDevice(keyboard);EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
