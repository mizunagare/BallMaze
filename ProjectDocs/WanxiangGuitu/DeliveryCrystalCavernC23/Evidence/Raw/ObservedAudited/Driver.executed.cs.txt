using System;
using System.Collections;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace CavernValidation
{
    public sealed partial class Driver : MonoBehaviour
    {
        static string root;
        CombatSession session;
        ThirdPersonHero hero;
        ForestRegionRuntime region;
        string mode;
        CavernEnergyHazard observedHazard;
        float nextTrace;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        public static void Boot()
        {
            if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable("UNITY_TEST_ROOT"))) return;
            root = GameEntry.TestRoot;
            if (string.IsNullOrEmpty(root) || !File.Exists(Path.Combine(root,"cavern-test.txt"))) return;
            if (FindAnyObjectByType<Driver>() != null) return;
            Application.runInBackground = true;
            var host = new GameObject("C2.1 isolated validation");
            DontDestroyOnLoad(host);
            host.AddComponent<Driver>();
        }

        void Check(string name, bool passed, string detail = "")
        {
            var row = name + "\t" + (passed ? "PASS" : "FAIL") + "\t" + detail.Replace('\n',' ') + "\n";
            File.AppendAllText(Path.Combine(root,"assertions.tsv"),row);
            Debug.Log("CAVERN_CHECK " + row.Trim());
            if (!passed) throw new InvalidOperationException(name + ": " + detail);
        }

        IEnumerator Start()
        {
            mode = File.ReadAllText(Path.Combine(root,"cavern-test.txt")).Trim();
            var stack = new System.Collections.Generic.Stack<IEnumerator>();
            stack.Push(Run());
            while (stack.Count != 0)
            {
                object next=null;
                bool more;
                try
                {
                    more=stack.Peek().MoveNext();
                    if(more)next=stack.Peek().Current;
                }
                catch (Exception e)
                {
                    File.WriteAllText(Path.Combine(root,"failure.txt"),e.ToString());
                    Exit(1);
                    yield break;
                }
                if(!more) stack.Pop();
                else if(next is IEnumerator nested) stack.Push(nested);
                else yield return next;
            }
            File.WriteAllText(Path.Combine(root,"complete.txt"),"PASS");
            Exit(0);
        }

        static void Exit(int code)
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.Exit(code);
#else
            Application.Quit(code);
#endif
        }

        void LateUpdate()
        {
            if((mode!="trace"&&!mode.StartsWith("lake"))||hero==null||Time.unscaledTime<nextTrace)return;
            nextTrace=Time.unscaledTime+.1f;
            var p=hero.transform.position;
            var enemy=session.enemies.FirstOrDefault();
            var e=enemy==null?Vector3.zero:enemy.transform.position;
            var row=FormattableString.Invariant(
                $"{Time.frameCount}\t{Time.unscaledTime:F3}\t{p.x:F3}\t{p.y:F3}\t{p.z:F3}\t{hero.Health.Current:F2}\t{e.x:F3}\t{e.z:F3}\t{observedHazard?.Phase}\t{observedHazard?.Remaining:F3}\t{session.orbit.AppliedDistance:F3}\t{hero.GameplayPaused}\n");
            File.AppendAllText(Path.Combine(root,"continuous.tsv"),row);
            if(mode.StartsWith("lake")) foreach(var actor in session.enemies)
                File.AppendAllText(Path.Combine(root,"ai.tsv"),$"{Time.frameCount}\t{Time.unscaledTime:F3}\t{actor.entityId}\t{actor.enabled}\t{actor.State}\t{actor.transform.position}\t{actor.Health.Current}\n");
        }

        IEnumerator Wait(string name, Func<bool> test, float timeout=15)
        {
            float end=Time.realtimeSinceStartup+timeout;
            while (!test() && Time.realtimeSinceStartup<end) yield return null;
            Check(name,test());
        }

        string InputState(AdventureCombat combat) =>
            $"focus={PlayerInput.Focused} blocked={PlayerInput.UIBlocked} paused={hero.GameplayPaused} flow={session.Flow.BlockCombat} flowError={session.Flow.Error} gear={combat.Gear.Weapon} scale={Time.timeScale} choices={hero.Progression.PendingChoices}";

        IEnumerator RequestAttack(AdventureCombat combat, bool skill, string name)
        {
            float until=Time.realtimeSinceStartup+1;
            bool accepted=false;
            while(!accepted&&Time.realtimeSinceStartup<until)
            {
                if(!PlayerInput.Focused)PlayerInput.Focus(true);
                accepted=skill?combat.UseSkill():combat.Strike();
                if(!accepted)yield return null;
            }
            Check(name,accepted,InputState(combat));
        }
        IEnumerator Move(string name, float x, float z)
        {
            var goal = new Vector3(x,0,z);
            Vector3 Offset()=>Vector3.ProjectOnPlane(goal-hero.transform.position,Vector3.up);
            float end=Time.realtimeSinceStartup+10;
            while(Offset().sqrMagnitude>.12f && Time.realtimeSinceStartup<end && !hero.Health.Dead)
            {
                hero.MoveCharacter(Vector3.ClampMagnitude(Offset(),Time.deltaTime*9));
                yield return null;
            }
            Check(name,Offset().sqrMagnitude<=.12f,hero.transform.position.ToString());
        }

        IEnumerator Shot(string name)
        {
            if (Application.isEditor) yield break;
            yield return new WaitForEndOfFrame();
            Check("shoulder-camera-"+name,session.orbit.shoulderMode&&session.orbit.CameraPositionClear,
                "distance="+session.orbit.AppliedDistance);
            var image=ScreenCapture.CaptureScreenshotAsTexture();
            File.WriteAllBytes(Path.Combine(root,name+".png"),image.EncodeToPNG());
            Destroy(image);
        }

        IEnumerator Run()
        {
            yield return Wait("title-ready",()=>GameEntry.Instance!=null&&GameEntry.Instance.Info!=null);
            var title=GameEntry.Instance;
            if(mode=="trace")
                File.WriteAllText(Path.Combine(root,"continuous.tsv"),"frame\trealtime\theroX\theroY\theroZ\thealth\tenemyX\tenemyZ\tenergyPhase\tremaining\tcameraDistance\tpaused\n");
            if(mode=="lake-store"||mode=="lake-routes"||mode=="lake"||mode=="lake-live"||mode=="lake-inner"||mode=="lake-closed"||mode=="materials"||mode=="hazard"||mode=="chamber"||mode=="elite"||mode=="combo"||mode=="start"||mode=="trace"||mode=="crystal"||mode=="death"||(mode=="weapons"||mode=="live")||mode=="forest"||mode=="ruins")
            {
                title.AskNew();
                Check("new-confirmed",title.ConfirmNew(),GameEntry.Error);
            }
            else Check("continue-selected",title.Continue(),GameEntry.Error);
            yield return Wait("game-ready",()=>(session=FindAnyObjectByType<CombatSession>())!=null&&session.Saves.IsInitialized&&!GameEntry.Loading,35);
            hero=session.hero;
            PlayerInput.Focus(true);
            yield return null;
            if(mode=="old-ruins-resume"||mode=="old-forest-resume")
            {
                region=session.GetComponent<ForestRegionRuntime>();
                Check("old-in-flight-resume",region.Ready&&!CrystalCavernLayout.Is(region.Layout)&&
                    (mode=="old-ruins-resume"?RuinsLayout.Is(region.Layout):region.Layout.revision<=5));
                yield break;
            }
            if(mode=="warehouse")
            {
                var prior=File.ReadAllLines(Path.Combine(root,"expected.txt"));
                var disk=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
                Check("warehouse-camp-restored",session.Flow.AtCamp&&!disk.hasActiveRun);
                Check("warehouse-durable-receipt",disk.settlement.runId==prior[0]&&disk.settlement.acknowledged&&
                    disk.settlement.status==SettlementStatus.Committed&&disk.profile.committedRuns.Count(x=>x==prior[0])==1);
                Check("warehouse-durable-materials",disk.profile.materials[(int)MaterialKind.Ore]==int.Parse(prior[1])&&
                    disk.profile.materials[(int)MaterialKind.CrystalShard]==int.Parse(prior[2]),string.Join(",",disk.profile.materials));
                Check("warehouse-reconfirm-idempotent",session.Flow.CommitSettlement()&&session.Flow.AcknowledgeSettlement()&&
                    session.Flow.Profile.materials.SequenceEqual(disk.profile.materials));
                yield break;
            }            if(mode=="forest"||mode=="ruins")
            {
                Check("old-region-depart",mode=="forest"?session.Flow.Depart(AdventureMode.ForestExploration):session.Flow.DepartRuins());
                region=session.GetComponent<ForestRegionRuntime>();
                Check("old-region-layout",region.Ready&&(mode=="forest"?region.Layout.revision<=5:RuinsLayout.Is(region.Layout)));
                Check("old-region-save",session.Saves.SaveProgress(false));
                Check("old-region-save-catalog",CombatSaveSystem.InspectReadOnly(session.Saves.SavePath).activeRun.region==
                    (mode=="forest"?"ForestRuins":RuinsLayout.Region));
                yield break;
            }
            if(!mode.Contains("resume")&&mode!="restore"&&mode!="material-resume"&&mode!="legacy-cavern"&&mode!="chamber-resume"&&mode!="chamber-repeat"&&mode!="elite-resume")
            {
                if(mode=="weapons"||mode=="live"||mode=="lake-live")
                {
                    var loadout=hero.GetComponent<AdventureLoadout>();
                    foreach(var type in new[]{GearType.Sword,GearType.Spear,GearType.Staff,GearType.Bow,
                        GearType.TwinBlades,GearType.Greatsword,GearType.Scythe})
                        if(!loadout.items.Any(i=>i.type==type))
                            Check("synthetic-equip-"+type,loadout.Add(AdventureItems.New(type,GearQuality.White,hero)));
                }
                Check("cavern-depart",session.Flow.DepartCavern(),session.Saves.Status);
            }
            region=session.GetComponent<ForestRegionRuntime>();
            Check("cavern-identity",region.Ready&&CrystalCavernLayout.Is(region.Layout)&&session.Flow.ActiveRun.region==CrystalCavernLayout.Region);
            if(mode=="legacy-c22-resume")
            {
                Check("legacy-c22-exact-version",region.Layout.revision==8&&session.Flow.ActiveRun.contentRevision==CrystalCavernLayout.Content22&&session.Flow.ActiveRun.generationVersion==11);
                Check("legacy-c22-no-new-entities",!session.Events.Points.Any(e=>e.entityId.StartsWith("c23:"))&&region.Layout.nodes.Length==2&&region.Layout.encounters.Length==2);
                var oldPrefab=Resources.Load<GameObject>(CrystalCavernLayout.Prefab22);
                var expectedRegion=oldPrefab.GetComponent<CrystalCavernRegion>();
                var actualRegion=region.PresentationRoot.GetComponent<CrystalCavernRegion>();
                Check("legacy-c22-original-prefab",CrystalCavernLayout.PrefabFor(region.Layout)==CrystalCavernLayout.Prefab22&&
                    region.PresentationRoot.name==oldPrefab.name+"(Clone)"&&!actualRegion.BridgeOpen&&
                    actualRegion.Floors.Length==expectedRegion.Floors.Length&&actualRegion.Blockers.Length==expectedRegion.Blockers.Length&&
                    expectedRegion.Floors.All(f=>actualRegion.Floors.Any(a=>a.name==f.name&&a.transform.position==f.transform.position&&a.size==f.size&&a.GetComponent<Renderer>().sharedMaterial==f.GetComponent<Renderer>().sharedMaterial)),
                    "actual="+region.PresentationRoot.name+" resource="+CrystalCavernLayout.PrefabFor(region.Layout));
                Check("legacy-c22-resave",session.Saves.SaveProgress(false));
                yield break;
            }
            var shaders=region.PresentationRoot.GetComponentsInChildren<Renderer>()
                .SelectMany(r=>r.sharedMaterials).Where(m=>m!=null && new[]{"Slate","Basalt","Rift","Vein","EnergyRecovery","EnergyWarning","EnergyActive"}.Contains(m.name)).Distinct().ToArray();
            Check("cavern-materials-supported",shaders.Length>=5&&shaders.All(m=>m.shader!=null&&m.shader.isSupported&&
                m.shader.name=="Universal Render Pipeline/Lit"),string.Join(",",shaders.Select(m=>m.name)));
            if(mode.StartsWith("lake")){yield return LakeRun();yield break;}
            var hazard=region.PresentationRoot.GetComponentInChildren<CavernEnergyHazard>();
            observedHazard=hazard;
            var mine=region.PresentationRoot.GetComponentsInChildren<AdventureResource>().First(r=>r.kind==MaterialKind.Ore);
            var combat=hero.GetComponent<AdventureCombat>();

            if(mode=="legacy-cavern")
            {
                Check("legacy-layout-version",region.Layout.revision==7&&region.Layout.mapAssetVersion=="C2.1-CAVERN-1"&&
                    session.Flow.ActiveRun.generationVersion==10&&region.Layout.points.Length==3&&session.Events.Points.Count==0);
                Check("legacy-crystal-pickup-restored",hero.Inventory.Count(MaterialKind.CrystalShard)>0&&
                    region.PresentationRoot.GetComponentsInChildren<AdventureResource>().Any(n=>n.kind==MaterialKind.CrystalShard&&n.Health==0));
                yield break;
            }

            if(mode=="materials")
            {
                foreach(var kind in new[]{MaterialKind.Ore,MaterialKind.CrystalShard})
                {
                    var vein=region.PresentationRoot.GetComponentsInChildren<AdventureResource>().Single(n=>n.kind==kind);
                    hero.RestorePosition(vein.transform.position+new Vector3(0,.1f,-1.55f),0);
                    session.orbit.RestoreView(0,9);
                    PlayerInput.Focus(true);
                    combat.ResetCombat();
                    yield return null;
                    for(int i=0;i<8&&vein.Health>0;i++)
                    {
                        combat.Strike();
                        yield return new WaitForSeconds(combat.BasicInterval+.15f);
                    }
                    Check("mine-exhausted-"+kind,vein.Health==0);
                    var materialDrop=FindObjectsByType<LootPickup>().Single(p=>p.Kind==kind&&!p.Collected);
                    yield return Move("walk-to-pickup-"+kind,materialDrop.transform.position.x,materialDrop.transform.position.z);
                    var resolver=hero.Inventory.Interactions;
                    resolver.Refresh();
                    var materialOffer=resolver.E;
                    int before=hero.Inventory.Count(kind);
                    Check("material-pickup-"+kind,materialOffer?.targetId==materialDrop.InteractionId&&
                        resolver.Execute(materialOffer)&&hero.Inventory.Count(kind)==before+materialDrop.Amount);
                    Check("material-pickup-once-"+kind,!resolver.Execute(materialOffer));
                }
                Check("both-materials-save",session.Saves.SaveProgress(false));
                File.WriteAllLines(Path.Combine(root,"expected.txt"),new[]{session.Flow.ActiveRun.runId,
                    hero.Inventory.Count(MaterialKind.Ore).ToString(),hero.Inventory.Count(MaterialKind.CrystalShard).ToString(),
                    session.Flow.Profile.materials[(int)MaterialKind.Ore].ToString(),session.Flow.Profile.materials[(int)MaterialKind.CrystalShard].ToString()});
                yield break;
            }

            if(mode=="material-resume")
            {
                var prior=File.ReadAllLines(Path.Combine(root,"expected.txt"));
                int ore=int.Parse(prior[1]),crystal=int.Parse(prior[2]);
                Check("materials-same-run",session.Flow.ActiveRun.runId==prior[0]);
                Check("both-materials-restored",hero.Inventory.Count(MaterialKind.Ore)==ore&&
                    hero.Inventory.Count(MaterialKind.CrystalShard)==crystal&&
                    region.PresentationRoot.GetComponentsInChildren<AdventureResource>().All(n=>n.Health==0));
                Check("hazard-safe-after-load",hazard.Phase==CavernEnergyHazard.CyclePhase.Recovery);
                yield return Move("mining-return-to-hub",0,406);
                yield return Move("mining-return-to-exit",0,385);
                var resolver=hero.Inventory.Interactions;
                resolver.Refresh();
                resolver.Present();
                Check("real-material-extraction",resolver.ExecuteDisplayed(true));
                yield return Wait("materials-pending",()=>session.Flow.HasResult);
                var receipt=session.Flow.Settlement;
                Check("both-materials-in-receipt",receipt.outcome==AdventureOutcome.Extracted&&receipt.runId==prior[0]&&
                    receipt.keptMaterials[(int)MaterialKind.Ore]==ore&&receipt.keptMaterials[(int)MaterialKind.CrystalShard]==crystal,
                    receipt.settlementId+" "+string.Join(",",receipt.keptMaterials));
                Check("commit-twice",session.Flow.CommitSettlement()&&session.Flow.CommitSettlement());
                Check("materials-back-at-camp",session.Flow.AcknowledgeSettlement()&&session.Flow.AtCamp);
                var disk=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
                int finalOre=ore+int.Parse(prior[3]),finalCrystal=crystal+int.Parse(prior[4]);
                Check("material-warehouse-exact",disk.profile.materials[(int)MaterialKind.Ore]==finalOre&&
                    disk.profile.materials[(int)MaterialKind.CrystalShard]==finalCrystal&&
                    disk.profile.committedRuns.Count(x=>x==prior[0])==1&&disk.settlement.settlementId==receipt.settlementId,
                    string.Join(",",disk.profile.materials));
                File.WriteAllLines(Path.Combine(root,"expected.txt"),new[]{prior[0],finalOre.ToString(),finalCrystal.ToString()});
                yield break;
            }

            if(mode=="hazard")
            {
                var center=new Vector3(21,.1f,410);
                hero.RestorePosition(center,90);
                float initial=hero.Health.Current;
                Check("hazard-in-recovery",hazard.Phase==CavernEnergyHazard.CyclePhase.Recovery);
                yield return new WaitForSeconds(.12f);
                Check("recovery-volume-safe",hero.Health.Current==initial);
                hero.RestorePosition(new Vector3(18,.1f,410),90);
                yield return Wait("hazard-in-warning",()=>hazard.Phase==CavernEnergyHazard.CyclePhase.Warning);
                hero.RestorePosition(center,90);
                yield return new WaitForSeconds(.12f);
                Check("warning-entry-safe",hero.Health.Current==initial);
                yield return Wait("pulse-imminent",()=>hazard.Remaining<=.13f);
                int evades=0;
                hero.Health.AttackEvaded+=_=>evades++;
                Check("real-dodge-request",hero.Dodge.TryDodge(Vector3.right));
                yield return Wait("real-pulse-evaded",()=>evades>0,1);
                Check("no-hp-loss-on-dodge",hero.Health.Current==initial&&hazard.Phase==CavernEnergyHazard.CyclePhase.Active);
                yield break;
            }
#if C22 || UNITY_EDITOR
            if(mode=="chamber"||mode=="chamber-resume"||mode=="chamber-repeat")
            {
                var room=region.Layout.points.Single(n=>n.id==CrystalCavernLayout.Chamber);
                var lever=session.Events.Points.Single(n=>n.entityId==CrystalCavernLayout.Lever);
                var chest=session.Events.Points.Single(n=>n.entityId==CrystalCavernLayout.Chest);
                Check("c22-content-mapping",region.Layout.revision==8&&region.Layout.mapAssetVersion==CrystalCavernLayout.Content22&&
                    session.Flow.ActiveRun.generationVersion==11);
                if(mode=="chamber")
                {
                    Check("closed-room-disconnected",!region.PathComplete(region.Layout.entry,room.position));
                    Check("closed-gate-physical",Physics.Linecast(new Vector3(-9,1,409.5f),new Vector3(-12,1,409.5f),out var gate)&&
                        gate.collider.name.Contains("实体矿室机关门"));
                    yield return Move("c22-entry-to-veins",0,405);
                    yield return Move("c22-find-lever",-6.3f,406.8f);
                    yield return Shot("01-chamber-closed");
                    var resolver=hero.Inventory.Interactions;
                    resolver.Refresh();
                    var leverOffer=resolver.E;
                    Check("c22-real-lever-interaction",leverOffer?.targetId==lever.entityId&&resolver.Execute(leverOffer),
                        leverOffer?.targetId??"none");
                    Check("lever-reentry-no-duplicate",!resolver.Execute(leverOffer)&&lever.Used);
                }
                else
                {
                    var saved=File.ReadAllLines(Path.Combine(root,"expected.txt"));
                    Check("same-c22-run-restored",session.Flow.ActiveRun.runId==saved[0]);
                    Check("lever-and-chest-state-restored",lever.Used&&chest.Used);
                    Check("no-second-chest-reward",!chest.Interact(hero));
                    var ids=FindObjectsByType<LootPickup>().Where(o=>!o.Collected&&o.transform.position.x<-19).Select(o=>o.InteractionId).OrderBy(id=>id).ToArray();
                    Check("ground-loot-restored-once",ids.Length>=2&&(saved.Length==1||ids.SequenceEqual(saved.Skip(1))),string.Join(",",ids));
                    hero.RestorePosition(new Vector3(-8,.1f,409.5f),270);
                }
                Check("open-room-reachable-and-return",region.PathComplete(region.Layout.entry,room.position)&&region.PathComplete(room.position,region.Layout.entry));
                Check("open-gate-no-wall",!Physics.Linecast(new Vector3(-9,1,409.5f),new Vector3(-12,1,409.5f)));
                yield return Move("physical-through-door",-12,409.5f);
                yield return Move("physical-into-chamber",-21,409.5f);
                Check("chamber-roof-physical",Physics.Raycast(new Vector3(-21,2,409.5f),Vector3.up,9));
                session.orbit.RestoreView(270,7);
                yield return Shot("02-inside-chamber");
                if(mode=="chamber")
                {
                    var resolver=hero.Inventory.Interactions;
                    resolver.Refresh();
                    var chestOffer=resolver.E;
                    Check("c22-real-chest-open",chestOffer?.targetId==chest.entityId&&resolver.Execute(chestOffer),
                        chestOffer?.targetId??"none");
                    int count=FindObjectsByType<LootPickup>().Count(o=>!o.Collected&&o.transform.position.x<-19);
                    Check("ordinary-chest-loot-once",count>=2&&!resolver.Execute(chestOffer)&&
                        FindObjectsByType<LootPickup>().Count(o=>!o.Collected&&o.transform.position.x<-19)==count);
                }
                yield return Move("physical-return-through-door",-8,409.5f);
                if(mode=="chamber")
                {
                    Check("c22-room-state-save",session.Saves.SaveProgress(false));
                    File.WriteAllLines(Path.Combine(root,"expected.txt"),new[]{session.Flow.ActiveRun.runId}.Concat(FindObjectsByType<LootPickup>()
                        .Where(o=>!o.Collected&&o.transform.position.x<-19).Select(o=>o.InteractionId).OrderBy(id=>id)));
                }
                if(mode=="chamber-repeat")
                {
                    var oldRun=session.Flow.ActiveRun.runId;
                    var oldDrops=File.ReadAllLines(Path.Combine(root,"expected.txt")).Skip(1).ToArray();
                    yield return Move("chamber-repeat-to-veins",0,406);
                    yield return Move("chamber-repeat-to-exit",0,385);
                    var resolver=hero.Inventory.Interactions;
                    resolver.Refresh();
                    resolver.Present();
                    Check("chamber-real-extraction",resolver.ExecuteDisplayed(true));
                    yield return Wait("chamber-extraction-pending",()=>session.Flow.HasResult);
                    Check("chamber-extraction-commit",session.Flow.Settlement.outcome==AdventureOutcome.Extracted&&
                        session.Flow.CommitSettlement()&&session.Flow.AcknowledgeSettlement());
                    Check("c22-next-real-run",session.Flow.DepartCavern()&&session.Flow.ActiveRun.runId!=oldRun);
                    lever=session.Events.Points.Single(n=>n.entityId==CrystalCavernLayout.Lever);
                    chest=session.Events.Points.Single(n=>n.entityId==CrystalCavernLayout.Chest);
                    Check("new-run-closed-and-unused",!lever.Used&&!chest.Used&&!region.PathComplete(region.Layout.entry,room.position));
                    yield return Move("second-run-to-veins",0,405);
                    yield return Move("second-run-find-lever",-6.3f,406.8f);
                    resolver.Refresh();
                    Check("second-run-open-lever",resolver.E?.targetId==lever.entityId&&resolver.Execute(resolver.E));
                    yield return Move("second-run-through-door",-12,409.5f);
                    yield return Move("second-run-to-chest",-21,409.5f);
                    resolver.Refresh();
                    Check("new-run-chest-awards-again",resolver.E?.targetId==chest.entityId&&resolver.Execute(resolver.E));
                    var drops=FindObjectsByType<LootPickup>().Where(o=>!o.Collected&&o.transform.position.x<-19).Select(o=>o.InteractionId).ToArray();
                    Check("new-run-ordinary-loot-new-identities",oldDrops.Length>=2&&drops.Length>=2&&!drops.Intersect(oldDrops).Any(),
                        string.Join(",",drops));
                }                yield break;
            }

            if(mode=="combo")
            {
                var actor=session.enemies.Single(e=>e.entityId==CrystalCavernLayout.Elite);
                var core=actor.GetComponent<CrystalCoreElite>();
                session.enemies.Single(e=>e!=actor).enabled=false;
                var eliteSpawn=actor.transform.position;
                hero.RestorePosition(new Vector3(29,.1f,407.05f),0);
                yield return Wait("combo-elite-warning",()=>core.Phase==CrystalCoreElite.CombatPhase.Warning);
                yield return Wait("combo-first-release",()=>core.Phase==CrystalCoreElite.CombatPhase.Exposed);
                yield return Wait("combo-hazard-warning",()=>hazard.Phase==CavernEnergyHazard.CyclePhase.Warning);
                yield return Move("combo-lateral-lane",24.6f,407.05f);
                yield return Move("combo-enter-warning-volume",24.6f,409.25f);
                float hp=hero.Health.Current;
                Check("combo-no-new-windup-in-hazard",core.Phase!=CrystalCoreElite.CombatPhase.Warning);
                yield return Move("combo-escape-to-lane",24.6f,407.05f);
                yield return Wait("combo-active",()=>hazard.Phase==CavernEnergyHazard.CyclePhase.Active);
                Check("combo-no-mandatory-hit",hero.Health.Current==hp&&!hazard.Area.Contains(hero.transform.position+Vector3.up*.65f));
                yield return Move("combo-passage-to-refuge",17.5f,407.05f);
                yield return Wait("combo-elite-follows-real-navmesh",()=>Vector3.Distance(eliteSpawn,actor.transform.position)>.6f);
                Check("combo-lane-nav",region.PathComplete(new Vector3(29,.1f,407.05f),new Vector3(17.5f,.1f,407.05f)));
                yield return Shot("05-c22-lane");
                yield break;
            }
            if(mode=="elite"||mode=="elite-resume")
            {
                var target=session.enemies.Single(e=>e.entityId==CrystalCavernLayout.Elite);
                var core=target.GetComponent<CrystalCoreElite>();
                if(mode=="elite-resume")
                {
                    Check("elite-run-restored",session.Flow.ActiveRun.runId==File.ReadAllText(Path.Combine(root,"expected.txt")).Trim());
                    Check("elite-death-restored",target.Health.Dead&&!target.GetComponent<CharacterController>().enabled);
                    int count=FindObjectsByType<LootPickup>().Count(o=>!o.Collected);
                    target.DropLootOnce();
                    Check("elite-restored-drop-once",count>0&&FindObjectsByType<LootPickup>().Count(o=>!o.Collected)==count);
                    yield break;
                }
                session.enemies.Single(e=>e.entityId=="c2:veins:watcher").enabled=false;
                Check("elite-shell-start",core.Phase==CrystalCoreElite.CombatPhase.Shell);
                target.Health.Observed+=e=>{if(e.kind==HealthObservationKind.Damage)File.AppendAllText(Path.Combine(root,"elite.tsv"),$"{Time.frameCount}\t{core.Phase}\t{e.before}\t{e.after}\n");};
                hero.RestorePosition(new Vector3(28.9f,.1f,407.9f),0);
                session.orbit.RestoreView(0,3);
                PlayerInput.Focus(true);
                yield return new WaitForSeconds(.18f);
                yield return Wait("elite-real-warning",()=>core.Phase==CrystalCoreElite.CombatPhase.Warning);
                float beforeShell=target.Health.Current;
                combat.ResetCombat();
                bool shellStrike=false;
                while(core.Phase==CrystalCoreElite.CombatPhase.Warning&&!shellStrike)
                {
                    if(!PlayerInput.Focused)PlayerInput.Focus(true);
                    shellStrike=combat.Strike();
                    if(!shellStrike)yield return null;
                }
                Check("elite-shell-strike",shellStrike,InputState(combat));
                yield return Wait("elite-shell-takes-reduced-hit",()=>target.Health.Current<beforeShell,1);
                float shellHit=beforeShell-target.Health.Current;
                yield return Shot("03-elite-warning");
                float heroHp=hero.Health.Current;
                yield return Wait("elite-exposure-after-release",()=>core.Phase==CrystalCoreElite.CombatPhase.Exposed);
                Check("elite-real-attack-hp",hero.Health.Current<heroHp,heroHp+"→"+hero.Health.Current);
                yield return Shot("04-elite-exposure");
                float beforeExposed=target.Health.Current;
                combat.ResetCombat();
                yield return RequestAttack(combat,false,"elite-exposed-strike");
                yield return Wait("elite-exposed-takes-hit",()=>target.Health.Current<beforeExposed,1);
                Check("elite-exposure-vs-shell",beforeExposed-target.Health.Current>shellHit,
                    shellHit+"→"+(beforeExposed-target.Health.Current));
                yield return Wait("elite-recovery",()=>core.Phase==CrystalCoreElite.CombatPhase.Recovery);
                yield return Wait("elite-next-warning",()=>core.Phase==CrystalCoreElite.CombatPhase.Warning);
                heroHp=hero.Health.Current;
                hero.SaveMenuOpen=true;
                float time=core.Remaining;
                yield return new WaitForSecondsRealtime(.2f);
                Check("elite-pause-freezes-window",core.Phase==CrystalCoreElite.CombatPhase.Warning&&time==core.Remaining&&hero.Health.Current==heroHp);
                hero.SaveMenuOpen=false;
                yield return Move("elite-evade-pulse-outside-cone",25.75f,407.0f);
                yield return Wait("elite-second-release",()=>core.Phase==CrystalCoreElite.CombatPhase.Exposed);
                Check("elite-dodge-cone-no-hp",hero.Health.Current==heroHp);
                hero.RestorePosition(target.transform.position+new Vector3(0,0,-1.65f),0);
                session.orbit.RestoreView(0,3);
                yield return null;
                for(int i=0;i<20&&!target.Health.Dead&&!hero.Health.Dead;i++)
                {
                    combat.Strike();
                    yield return new WaitForSecondsRealtime(combat.BasicInterval+.15f);
                }
                Check("elite-killed-by-real-attacks",target.Health.Dead);
                int drops=FindObjectsByType<LootPickup>().Count(o=>!o.Collected);
                target.DropLootOnce();
                Check("elite-drops-not-duplicated",drops>0&&FindObjectsByType<LootPickup>().Count(o=>!o.Collected)==drops);
                Check("elite-dead-checkpoint",session.Saves.SaveProgress(false));
                File.WriteAllText(Path.Combine(root,"expected.txt"),session.Flow.ActiveRun.runId);
                yield break;
            }
#endif
            if (mode=="live")
            {
                var target=session.enemies.Single(e=>e.entityId=="c2:veins:watcher");
                var loadout=hero.GetComponent<AdventureLoadout>();
                var trace=Path.Combine(root,"combat.tsv");
                void Log(string line)=>File.AppendAllText(trace,line+"\n");
                target.enabled=false;
                var controller=target.GetComponent<CharacterController>();
                target.Health.Observed+=e=>{if(e.kind==HealthObservationKind.Damage)Log($"hp\t{target.entityId}\t{e.before}\t{e.after}\t{e.frame}");};
                combat.MeleeObserved+=e=>Log($"melee\t{e.attack}\t{e.collider?.name}\t{e.point}\t{e.forward}\t{e.reason}\t{e.before}\t{e.after}");
                AdventureProjectile.Observed+=e=>Log($"projectile\t{e.stage}\t{e.from}\t{e.to}\t{e.collider?.name}\t{e.frame}");
                hero.GetComponent<NewWeaponCombat>().Observed+=e=>Log($"new-weapon\t{e.stage}\t{e.a}\t{e.b}\t{e.radius}\t{e.target?.name}\t{e.before}\t{e.after}");
                foreach(var type in new[]{GearType.Sword,GearType.Spear,GearType.Staff,GearType.Bow,GearType.TwinBlades,GearType.Greatsword,GearType.Scythe})
                {
                    Check("select-live-"+type,loadout.SelectMain(loadout.items.First(i=>i.type==type)));
                    foreach(bool skill in new[]{false,true})
                    {
                        combat.ResetCombat();
                        target.Health.ResetHealth();
                        controller.enabled=false;
                        float reach=type==GearType.Staff||type==GearType.Bow?3.8f:1.38f;
                        target.transform.position=new Vector3(0,.1f,405+reach);
                        controller.enabled=true;
                        hero.RestorePosition(new Vector3(0,.1f,405),0);
                        session.orbit.RestoreView(0,0);
                        PlayerInput.Focus(true);
                        Physics.SyncTransforms();
                        yield return new WaitForSeconds(.15f);
                        float hp=target.Health.Current;
                        string name=type+(skill?"-default-skill":"-basic");
                        Log($"trial\t{name}\t{target.entityId}\t{hero.transform.position}\t{target.transform.position}");
                        yield return RequestAttack(combat,skill,"request-"+name);
                        yield return Wait("live-hit-"+name,()=>target.Health.Current<hp,3);
                        yield return new WaitForSeconds(1.1f);
                    }
                }
                yield break;
            }
            if(mode=="crystal")
            {
                var crystal=region.PresentationRoot.GetComponentsInChildren<AdventureResource>().Single(r=>r.kind==MaterialKind.CrystalShard);
                hero.RestorePosition(crystal.transform.position+new Vector3(0,.1f,-1.55f),0);
                session.orbit.RestoreView(0,9);
                PlayerInput.Focus(true);
                yield return null;
                for(int i=0;i<8&&crystal.Health>0;i++)
                {
                    combat.Strike();
                    yield return new WaitForSeconds(combat.BasicInterval+.12f);
                }
                Check("crystal-actual-attacks",crystal.Health==0);
                var drop=FindObjectsByType<LootPickup>().Single(p=>p.Kind==MaterialKind.CrystalShard&&!p.Collected);
                var resolver=hero.Inventory.Interactions;
                resolver.Refresh();
                int before=hero.Inventory.Count(MaterialKind.CrystalShard);
                Check("crystal-resolver-target",resolver.E?.targetId==drop.InteractionId);
                Check("crystal-actual-pickup",resolver.Execute(resolver.E)&&hero.Inventory.Count(MaterialKind.CrystalShard)==before+drop.Amount);
                Check("crystal-checkpoint-save",session.Saves.SaveProgress(false));
                Check("crystal-checkpoint-id",CombatSaveSystem.InspectReadOnly(session.Saves.SavePath).activeRun.checkpoint.resources
                    .Any(n=>n.entityId=="c2:mine-north"&&n.health==0));
                yield break;
            }

            if(mode=="weapons")
            {
                hero.RestorePosition(new Vector3(29,.1f,412.8f),90);
                session.orbit.RestoreView(90,8);
                yield return null;
                var loadout=hero.GetComponent<AdventureLoadout>();
                int newReleases=0;
                hero.GetComponent<NewWeaponCombat>().Observed += e => { if(e.stage=="release")newReleases++; };
                foreach(var type in new[]{GearType.Sword,GearType.Spear,GearType.Staff,GearType.Bow,
                    GearType.TwinBlades,GearType.Greatsword,GearType.Scythe})
                {
                    var item=loadout.items.First(i=>i.type==type);
                    Check("select-"+type,loadout.SelectMain(item));
                    combat.ResetCombat();
                    PlayerInput.Focus(true);
                    yield return null;
                    bool recent=NewWeaponRegistry.Is(type);
                    int before=recent?newReleases:combat.LastReleaseFrame;
                    Check("strike-"+type,combat.Strike());
                    yield return new WaitForSeconds(.9f);
                    Check("strike-released-"+type,(recent?newReleases:combat.LastReleaseFrame)>before);
                    if(recent) yield return Wait("basic-recovery-"+type,()=>!hero.GetComponent<NewWeaponCombat>().Busy);
                    before=recent?newReleases:combat.LastReleaseFrame;
                    Check("skill-"+type,combat.UseSkill());
                    yield return new WaitForSeconds(1.4f);
                    Check("skill-released-"+type,(recent?newReleases:combat.LastReleaseFrame)>before);
                }
                combat.ResetCombat();
                Check("select-staff-wall",loadout.SelectMain(loadout.items.First(i=>i.type==GearType.Staff)));
                hero.RestorePosition(new Vector3(6.9f,.1f,400),90);
                session.orbit.RestoreView(90,3);
                string wallImpact=null;
                AdventureProjectile.Observed += e =>
                {
                    if(e.stage=="sweep-contact" && e.collider!=null)wallImpact=e.collider.name;
                };
                yield return new WaitForSeconds(.2f);
                Check("strike-staff-wall",combat.Strike());
                yield return Wait("real-projectile-contact",()=>wallImpact!=null,4);
                Check("projectile-stops-at-cave-wall",wallImpact.Contains("转角南壁"),wallImpact);
                yield break;
            }

            if(mode=="restore")
            {
                var prior=File.ReadAllLines(Path.Combine(root,"expected.txt"));
                Check("same-run",session.Flow.ActiveRun.runId==prior[0]);
                Check("mined-state-recovered",mine.Health==0);
                Check("loot-picked-recovered",hero.Inventory.Count(MaterialKind.Ore)==int.Parse(prior[1])&&
                    !FindObjectsByType<LootPickup>().Any(p=>p.Kind==MaterialKind.Ore&&!p.Collected));
                Check("hazard-safe-after-restore",hazard.Phase==CavernEnergyHazard.CyclePhase.Recovery);
                yield return Move("return-through-turn",10.5f,410);
                yield return Move("return-to-mine",0,410);
                yield return Move("return-to-entry",0,385);
                var resolver=hero.Inventory.Interactions;
                resolver.Refresh();
                resolver.Present();
                Check("extract-with-resolver",resolver.ExecuteDisplayed(true));
                yield return Wait("extraction-pending",()=>session.Flow.HasResult);
                Check("real-extraction",session.Flow.Settlement.outcome==AdventureOutcome.Extracted);
                Check("ore-in-source-ledger-settlement",session.Flow.Settlement.keptMaterials[(int)MaterialKind.Ore]==int.Parse(prior[1]),
                    "ore="+session.Flow.Settlement.keptMaterials[(int)MaterialKind.Ore]);
                Check("settlement-commits",session.Flow.CommitSettlement(),session.Flow.Error);
                Check("camp-acknowledged",session.Flow.AcknowledgeSettlement()&&session.Flow.AtCamp&&!session.Flow.HasResult);
                Check("hazard-unloaded",!region.Active&&(!hazard||!hazard.isActiveAndEnabled));
                Check("new-run-after-extraction",session.Flow.DepartCavern()&&session.Flow.ActiveRun.runId!=prior[0]);
                Check("new-run-mining-reset",region.PresentationRoot.GetComponentsInChildren<AdventureResource>().All(n=>n.Health==n.maxHealth));
                yield break;
            }

            if(mode=="death")
            {
                hero.RestorePosition(new Vector3(22,.1f,410),90);
                hero.Health.RestoreHealth(1);
                yield return Wait("hazard-produces-death-outcome",()=>session.Flow.HasResult,20);
                Check("death-normal-outcome",session.Flow.Settlement.outcome==AdventureOutcome.Death);
                Check("death-commit",session.Flow.CommitSettlement());
                Check("death-unloads-hazard",!region.Active&&(!hazard||!hazard.isActiveAndEnabled));
                yield break;
            }

            yield return Shot("01-entry");
            yield return Move("entry-to-mine",0,405);
            var enemy=session.enemies.Single();
            var spawn=enemy.transform.position;
            yield return Move("enter-enemy-detection",3,408);
            yield return Wait("enemy-traverses-navmesh",()=>Vector3.Distance(spawn,enemy.transform.position)>.7f);
            Check("roof-collision",Physics.Raycast(new Vector3(0,2,402),Vector3.up,10));
            Check("crystal-column-collision",Physics.Linecast(new Vector3(4.3f,1,403),new Vector3(4.3f,1,409)));
            yield return Move("approach-ore", -5.5f,401.4f);
            hero.RestorePosition(hero.transform.position,0);
            session.orbit.RestoreView(0,9);
            PlayerInput.Focus(true);
            yield return null;
            for(int i=0;i<8&&mine.Health>0;i++)
            {
                combat.Strike();
                yield return new WaitForSeconds(combat.BasicInterval+.12f);
            }
            Check("ore-actual-attacks",mine.Health==0);
            var loot=FindObjectsByType<LootPickup>().Single(p=>p.Kind==MaterialKind.Ore&&!p.Collected);
            yield return Move("walk-to-ground-loot",loot.transform.position.x,loot.transform.position.z);
            int carried=hero.Inventory.Count(MaterialKind.Ore);
            var pickup=hero.Inventory.Interactions;
            pickup.Refresh();
            var offer=pickup.E;
            Check("ore-resolver-target",offer?.targetId==loot.InteractionId);
            Check("ore-actual-pickup",pickup.Execute(offer)&&hero.Inventory.Count(MaterialKind.Ore)==carried+loot.Amount);
            Check("duplicate-pickup-refused",!pickup.Execute(offer));
            yield return Shot("02-mining");
            yield return Move("mine-to-corridor-turn",8.5f,410);
            yield return Move("turn-into-channel",16,410);
            yield return Move("side-lane-access",17.8f,407.1f);
            yield return Move("pass-hazard-along-side",27.1f,407.1f);
            yield return Move("channel-end",29,410);
            session.orbit.RestoreView(270,10);
            yield return null;
            yield return Shot("03-channel");
            yield return Wait("hazard-warning",()=>hazard.Phase==CavernEnergyHazard.CyclePhase.Warning);
            yield return Shot("04-warning");
            var start=hero.Health.Current;
            yield return Wait("hazard-active-while-avoiding",()=>hazard.Phase==CavernEnergyHazard.CyclePhase.Active);
            yield return new WaitForSeconds(.12f);
            Check("out-of-range-safe",hero.Health.Current==start);
            hero.RestorePosition(new Vector3(24,.1f,410),90);
            var wall=GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall.transform.position=new Vector3(23,1,410);
            wall.transform.localScale=new Vector3(.3f,2,1.6f);
            Physics.SyncTransforms();
            yield return new WaitForSeconds(.12f);
            Check("wall-shields-active-hazard",hero.Health.Current==start);
            hero.SaveMenuOpen=true;
            var phase=hazard.Phase;
            float remaining=hazard.Remaining;
            yield return new WaitForSecondsRealtime(.22f);
            Check("hazard-pauses",hazard.Phase==phase&&hazard.Remaining==remaining&&hero.Health.Current==start);
            hero.SaveMenuOpen=false;
            wall.SetActive(false);
            Destroy(wall);
            yield return Wait("active-hazard-causes-health-loss",()=>hero.Health.Current<start,5);
            yield return Shot("05-active");
            var afterPulse=hero.Health.Current;
            yield return new WaitForSeconds(.15f);
            Check("same-pulse-damages-at-most-once",hero.Health.Current==afterPulse,"damage="+(start-afterPulse));
            yield return Move("leave-active-range",27,410);
            Check("running-checkpoint-write",session.Saves.SaveProgress(false));
            File.WriteAllText(Path.Combine(root,"expected.txt"),session.Flow.ActiveRun.runId+"\n"+hero.Inventory.Count(MaterialKind.Ore)+"\n");
        }
    }
}

#if UNITY_EDITOR
public static class CavernValidationEditor
{
    public static void Begin()
    {
        UnityEditor.SceneManagement.EditorSceneManager.OpenScene(GameEntry.BootPath);
        UnityEditor.EditorApplication.EnterPlaymode();
    }
}
#endif
