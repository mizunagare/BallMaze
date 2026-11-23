#if UX05_ENTRY_PROBE
using System;
using System.Collections;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.UI;

public sealed class ObjectiveHistoryEntryProbe : MonoBehaviour
{
    string evidence, root, mode, save;
    long initialRevision;
    bool capacityStepPassed;
    [Serializable] sealed class Event { public string name, detail, utc; }
    [Serializable] sealed class Result { public string status, reason, mode; public long initialRevision, finalRevision; }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void StartIfRequested()
    {
        var args = Environment.GetCommandLineArgs();
        int at = Array.IndexOf(args, "-ux05-entry-probe");
        if (at < 0) return;
        var root = ValidationStorage.Root(args, true);
        if (at + 2 >= args.Length || !args[at + 2].All(c => (c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z' || c >= '0' && c <= '9') || c == '-'))
            throw new InvalidOperationException("Missing probe mode or safe Run ID");
        Application.runInBackground = true;
        var go = new GameObject("UX05 isolated integration probe");
        DontDestroyOnLoad(go);
        var probe = go.AddComponent<ObjectiveHistoryEntryProbe>();
        probe.root = root;
        probe.mode = args[at + 1];
        probe.evidence = Path.Combine(root, "probe-results", args[at + 2]);
        Directory.CreateDirectory(probe.evidence);
        probe.StartCoroutine(probe.Run());
    }

    IEnumerator Run()
    {
        float until = Time.realtimeSinceStartup + 90;
        while (GameEntry.Instance?.GetComponent<TitleMenu>()?.Canvas == null && Time.realtimeSinceStartup < until)
            yield return null;
        var entry = GameEntry.Instance;
        if (entry == null || !entry.GetComponent<TitleMenu>()) { Finish(false,"title unavailable",0); yield break; }
        var menu = entry.GetComponent<TitleMenu>();
#if UX05_V9_FIXTURE_PROBE
        if (mode == "legacy-pending" &&
            (!Click(menu,"新游戏") || !Click(menu,"确认建立新档案")))
        { Finish(false,"v9 fresh game action unavailable",0); yield break; }
#endif
        EventLog("title-ready", entry.Info?.status.ToString());
#if UX_ACCEPTANCE && UX05_V10_OBJECTIVE_PROBE
        if (mode.StartsWith("r1-migrate-",StringComparison.Ordinal))
        {
            RunMigrationBoundary(entry,menu);
            yield break;
        }
#endif
        if (mode == "inspect-reject")
        {
            bool rejected=!entry.Info.canContinue && !Directory.Exists(entry.CurrentDirectory) &&
                (entry.Info.status==SaveAvailability.Incompatible || entry.Info.status==SaveAvailability.Corrupt);
            EventLog("old-source-rejected",entry.Info.reason);
            Finish(rejected,"invalid or future v9 source rejected without target writes",0);
            yield break;
        }
        if (mode == "migrate-cut")
        {
            GroundLootStore.ValidationHook=phase=>
            {
                if(phase!="before-page-write")return;
                EventLog("migration-process-cut",phase);
                System.Threading.Thread.Sleep(System.Threading.Timeout.Infinite);
            };
            if(!Click(menu,"读取存档")||!Click(menu,"明确选择新版"))
            { Finish(false,"migration fault route unavailable",0); yield break; }
            GroundLootStore.ValidationHook=null;
            Finish(false,"migration cut point not reached",0);
            yield break;
        }
#if UX05_V10_OBJECTIVE_PROBE
        if (mode == "objective-new" || mode == "objective-capacity" || mode == "objective-pending-stop" || mode == "objective-abandon-after-goal" || mode == "r1-save-readback" || mode == "r1-save-stale" || mode == "r1-ui-empty" || mode == "r1-ui-imgui-empty")
        {
            if (!Click(menu,"新游戏") || !Click(menu,"确认建立新档案"))
            { Finish(false,"new game action unavailable",0); yield break; }
        }
        else
#endif
        if (mode == "migrate")
        {
            if (Directory.Exists(entry.CurrentDirectory)) { Finish(false,"already migrated before explicit action",0); yield break; }
            if (!Click(menu, "读取存档") || !Click(menu, "明确选择新版"))
            { Finish(false,"explicit migrate action unavailable",0); yield break; }
            EventLog("explicit-migration-clicked", GameEntry.Error);
            if (!entry.Info.canContinue || entry.Info.version != 10)
            { Finish(false,"migration not readable",0); yield break; }
            if (!Click(menu, "读取所示自动档")) { Finish(false,"migrated archive not selectable",0); yield break; }
        }
        else if (mode != "legacy-pending")
        {
            if (!Click(menu, "继续游戏")) { Finish(false,"continue action unavailable",0); yield break; }
        }

        CombatSaveSystem saves = null;
        while (Time.realtimeSinceStartup < until)
        {
            saves = FindAnyObjectByType<CombatSaveSystem>();
            if (saves != null && saves.IsInitialized && !GameEntry.Loading) break;
            yield return null;
        }
        if (saves == null || !saves.IsInitialized) { Finish(false,"gameplay ready timeout",0); yield break; }
        save = saves.SavePath;
        var first = CombatSaveSystem.InspectReadOnly(save);
        initialRevision = first.revision;
        int version = mode == "legacy" || mode == "legacy-pending" ? 9 : 10;
        string leaf = version == 9 ? "ForestRuins" : "ForestRuins-v10";
        if (first.sourceVersion != version || Path.GetFileName(Path.GetDirectoryName(save)) != leaf)
        { Finish(false,"wrong storage version or root",first.revision); yield break; }
        EventLog("game-ready",save);
#if UX05_V9_FIXTURE_PROBE
        if (mode == "legacy-pending") { yield return ProduceV9Pending(saves,first); yield break; }
#endif
#if UX05_V10_OBJECTIVE_PROBE
        if (mode == "objective-new" || mode == "objective-repeat" || mode == "objective-pending-stop" || mode == "objective-abandon-after-goal" || mode == "r1-save-readback" || mode == "r1-save-stale")
        {
            yield return CompleteRealGoal(saves,first);
            yield break;
        }
#if UX_ACCEPTANCE
        if (mode.StartsWith("r1-ui-",StringComparison.Ordinal))
        {
            yield return VerifyR1HistoryUI(saves,first);
            yield break;
        }
#endif
        if (mode == "objective-capacity")
        {
            yield return CompleteCapacityRun(saves,first);
            yield break;
        }
        if (mode == "objective-capacity-readback")
        {
            var history=first.profile.objectiveHistory;
            bool ok=history.Length==128 && history.Select(row=>row.runId).Distinct().Count()==128 &&
                first.profile.committedRuns.Length==129 && !history.Any(row=>row.runId==first.profile.committedRuns[0]);
            if(!ok) { Finish(false,"cold process did not find both history and permanent identities",first.revision); yield break; }
            yield return InspectCapacityPages(saves,first);
            yield break;
        }
        if (mode == "objective-pending-resume")
        {
            var flow=FindAnyObjectByType<CombatSession>().Flow;
            var row=first.settlement?.plan?.objectiveHistory?.LastOrDefault();
            bool ready=first.hasSettlement && first.settlement.status==SettlementStatus.Pending &&
                first.profile.objectiveHistory.Length==0 && row!=null;
            if (!ready) { Finish(false,"cold process did not load the frozen Pending result",first.revision); yield break; }
            EventLog("cold-pending-loaded",JsonUtility.ToJson(row));
            bool published=flow.CommitSettlement();
            var committed=CombatSaveSystem.InspectReadOnly(save);
            var previous=SaveSchemaMigration.FingerprintFile(save);
            bool duplicate=flow.CommitSettlement() && previous==SaveSchemaMigration.FingerprintFile(save);
            bool ok=published && duplicate && committed.hasSettlement && committed.settlement.status==SettlementStatus.Committed &&
                committed.profile.objectiveHistory.Length==1 &&
                JsonUtility.ToJson(row)==JsonUtility.ToJson(committed.profile.objectiveHistory[0]) &&
                committed.profile.committedRuns.Count(x=>x==row.runId)==1;
            EventLog("cold-pending-published",JsonUtility.ToJson(committed.profile.objectiveHistory.LastOrDefault()));
            Finish(ok,"cold Pending resumed same times, history and reward plan with one durable publication",committed.revision);
            yield break;
        }
#if UX_ACCEPTANCE
        if (mode=="r1-rules")
        {
            yield return VerifyR1RuleProtection(saves,first);
            yield break;
        }
#endif
        if (mode == "inventory-gates")
        {
            yield return CheckProtectedInventory(saves,first.revision);
            yield break;
        }
        if (mode == "objective-ui")
        {
            yield return InspectHistoryView(saves,first.revision);
            yield break;
        }
        if (mode == "objective-readback" || mode == "objective-repeat-readback")
        {
            var history=first.profile.objectiveHistory;
            int expected=mode=="objective-repeat-readback"?2:1;
            bool ok=history.Length==expected && history.Select(row=>row.runId).Distinct().Count()==expected &&
                history.All(row=>row.objectiveId=="forest.treasure" && first.profile.committedRuns.Contains(row.runId));
            foreach(var row in history) EventLog("cross-process-history",JsonUtility.ToJson(row));
            Finish(ok,"cold process history readback",first.revision);
            yield break;
        }
#endif
        if (mode == "legacy" || mode == "migrate" || mode == "resume") yield return new WaitForSecondsRealtime(12);
        var kb = InputSystem.AddDevice<Keyboard>();
        InputSystem.QueueStateEvent(kb,new KeyboardState(Key.F5));
        EventLog("input-f5-down", save);
        yield return null;
        InputSystem.QueueStateEvent(kb,new KeyboardState());
        yield return new WaitForSecondsRealtime(1);
        InputSystem.RemoveDevice(kb);
        var final = CombatSaveSystem.InspectReadOnly(save);
        Finish(final.sourceVersion == version && final.revision > initialRevision,
            "product save path/version and revision read back",final.revision);
    }

#if UX05_V10_OBJECTIVE_PROBE
    IEnumerator InspectCapacityPages(CombatSaveSystem saves, CombatSaveData first)
    {
        var session=FindAnyObjectByType<CombatSession>();
        session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
        string before=SaveSchemaMigration.FingerprintFile(save);
        yield return null;
        yield return new WaitForEndOfFrame();
        var canvas=FindObjectsByType<Canvas>(FindObjectsSortMode.None).SingleOrDefault(c=>c.name=="冒险历程入口");
        if(canvas==null || !ClickIn(canvas,"冒险历程")) { Finish(false,"uGUI history unavailable",first.revision); yield break; }
        yield return null;
        bool ok=ViewContains(canvas,"1 / 7") &&
            canvas.GetComponentsInChildren<Text>().Count(t=>t.name=="Objective")==20;
        for(int page=2;page<=7 && ok;page++)
        {
            ok=ClickIn(canvas,"下一页");
            yield return null;
            ok=ok && ViewContains(canvas,page+" / 7") &&
                canvas.GetComponentsInChildren<Text>().Count(t=>t.name=="Objective")== (page==7?8:20);
        }
        ok=ok && !ClickIn(canvas,"下一页") && ClickIn(canvas,"上一页");
        yield return null;
        ok=ok && ViewContains(canvas,"6 / 7") && before==SaveSchemaMigration.FingerprintFile(save);
        EventLog("history-page-readback","page counts expected 20,20,20,20,20,20,8; unchanged save="+(before==SaveSchemaMigration.FingerprintFile(save)));
        Finish(ok,"cold process verified 128 entries, 129 permanent identities and all seven read-only uGUI pages",first.revision);
    }

    IEnumerator CompleteCapacityRun(CombatSaveSystem saves, CombatSaveData initial)
    {
        var previous=initial;
        for (int i=1;i<=129;i++)
        {
            capacityStepPassed=false;
            yield return CompleteRealGoal(saves,previous);
            if (!capacityStepPassed) yield break;
            var committed=CombatSaveSystem.InspectReadOnly(save);
            if (committed.profile.objectiveHistory.Length!=Math.Min(i,128) ||
                committed.profile.committedRuns.Length!=i ||
                (i==129 && (committed.profile.objectiveHistory[0].runId!=previous.profile.objectiveHistory[1].runId ||
                    !committed.profile.committedRuns.Contains(previous.profile.objectiveHistory[0].runId))))
            { Finish(false,"history capacity or permanent terminal identity mismatch at "+i,committed.revision); yield break; }
            if (i==128 || i==129)
                EventLog("capacity-boundary", "commits="+i+"; retained="+committed.profile.objectiveHistory.Length+
                    "; oldest="+committed.profile.objectiveHistory[0].runId);
            previous=committed;
        }
        Finish(true,"129 real product departures, chest objectives and extractions; initial entry trimmed",previous.revision);
    }

    IEnumerator CompleteRealGoal(CombatSaveSystem saves, CombatSaveData initial)
    {
        var session=FindAnyObjectByType<CombatSession>();
        var flow=session.Flow;
        var hero=session.hero;
        var combat=hero.GetComponent<AdventureCombat>();
        if (combat?.Expanded==null || !combat.Expanded.Select(1))
        { Finish(false,"unable to select a non-default skill slot before departure",initial.revision); yield break; }
        if (!flow.SelectExpeditionGoal(ExpeditionGoal.Treasure) || !flow.Depart(AdventureMode.ForestExploration))
        { Finish(false,"departure rejected: "+flow.DepartureReason,initial.revision); yield break; }
        int slot=NewWeaponRegistry.Is(combat.Gear.Weapon)?combat.NewWeapons.Selected:combat.Expanded.Selected;
        if (slot!=0) { Finish(false,"successful departure did not restore default skill slot",initial.revision); yield break; }
        EventLog("skill-slot-restored","slot=0");
        yield return null;
        var sourceRun=flow.ActiveRun.runId;
        int opened=0;
        foreach(var chest in session.Events.Points.Where(p=>p!=null && p.Kind==WorldEventKind.Treasure && !p.Used).ToArray())
        {
            hero.RestorePosition(chest.transform.position + new Vector3(0,.1f,-1.7f),0);
            session.orbit.RestoreView(0,8);
            Physics.SyncTransforms();
            yield return null;
            bool interacted=chest.Interact(hero);
            EventLog("product-chest-interaction", chest.entityId+" accepted="+interacted+" used="+chest.Used);
            if (interacted && chest.Used && ++opened==3) break;
        }
        if (opened!=3) { Finish(false,"fewer than three real chests opened",initial.revision); yield break; }
        if(mode=="objective-abandon-after-goal")
        {
            bool selectionRejected=!flow.SelectExpeditionGoal(ExpeditionGoal.Challenge) &&
                flow.ActiveRun.goal==ExpeditionGoal.Treasure;
            var state=ObjectiveEvaluator.Evaluate(ObjectiveEvaluator.Live(session));
            flow.OpenAbandon();
            bool abandoned=flow.ConfirmAbandon();
            var pendingFailure=CombatSaveSystem.InspectReadOnly(save);
            bool confirmed=flow.CommitSettlement();
            var result=CombatSaveSystem.InspectReadOnly(save);
            EventLog("abandon-after-goal", "conditionsMet="+state.conditionsMet+"; goalChangeRejected="+selectionRejected+
                "; history="+result.profile.objectiveHistory.Length+"; outcome="+result.settlement?.outcome);
            bool abandonVerified=state.conditionsMet && !state.achieved && selectionRejected && abandoned && confirmed &&
                pendingFailure.settlement?.plan.objectiveHistory.Length==0 &&
                result.settlement?.outcome==AdventureOutcome.Abandoned &&
                result.settlement.status==SettlementStatus.Committed && result.profile.objectiveHistory.Length==0 &&
                result.profile.committedRuns.Count(x=>x==sourceRun)==1;
            Finish(abandonVerified,"three real chests, in-flight goal change rejected, actual abandon/settlement writes no success history",result.revision);
            yield break;
        }
        var exits=flow.ExitConfigs().Where(e=>!e.repairRequired).ToArray();
        if (exits.Length==0) {Finish(false,"no unrepaired exit",initial.revision);yield break;}
        var alive=session.enemies.Where(e=>e!=null && e.Health!=null && !e.Health.Dead).ToArray();
        var exit=exits.OrderByDescending(e=>alive.Length==0?999f:alive.Min(en=>Vector3.Distance(en.transform.position,e.position))).First();
        hero.RestorePosition(exit.position,0);
        Physics.SyncTransforms();
        yield return null;
        if (!flow.BeginExtraction(exit.id))
        { Finish(false,"extraction rejected: "+flow.ExtractionReasonFor(exit),initial.revision); yield break; }
        EventLog("product-extraction",exit.id);
        if(mode=="objective-capacity")
        {
            Time.timeScale=8;
            EventLog("acceptance-extraction-clock","Unity timeScale=8; product countdown and outcome unchanged");
        }
        float until=Time.realtimeSinceStartup+30;
        while (!flow.HasResult && Time.realtimeSinceStartup<until && flow.ActiveRun?.phase==RunPhase.Extracting)
            yield return null;
        if(mode=="objective-capacity" && !flow.HasResult) Time.timeScale=1;
        var pending=CombatSaveSystem.InspectReadOnly(save);
        var row=pending.settlement?.plan?.objectiveHistory?.SingleOrDefault(e=>e.runId==sourceRun);
        if (!pending.hasSettlement || pending.settlement.status!=SettlementStatus.Pending ||
            pending.profile.objectiveHistory.Any(e=>e.runId==sourceRun) || row==null || row.objectiveId!="forest.treasure")
        { Finish(false,"durable Pending candidate not found",pending.revision); yield break; }
        EventLog("pending-frozen",JsonUtility.ToJson(row));
#if UX_ACCEPTANCE
        if (mode=="r1-save-stale" || mode=="r1-save-readback")
        {
            Finish(VerifyR1CommitFailure(saves,flow,pending,row),"fresh real Pending, publication fault and exact durable recovery",flow.Revision);
            yield break;
        }
#endif
        if (mode=="objective-pending-stop")
        {
            Finish(true,"real objective Pending flushed; clean exit before player confirms settlement",pending.revision);
            yield break;
        }
        if (mode=="objective-capacity")
        {
            bool committedNormally=flow.CommitSettlement();
            var priorRetry=CombatSaveSystem.InspectReadOnly(save);
            string publishedFingerprint=SaveSchemaMigration.FingerprintFile(save);
            bool duplicate=flow.CommitSettlement() && publishedFingerprint==SaveSchemaMigration.FingerprintFile(save);
            bool acknowledgedNormally=flow.AcknowledgeSettlement();
            var persisted=CombatSaveSystem.InspectReadOnly(save);
            capacityStepPassed=committedNormally && duplicate && acknowledgedNormally &&
                persisted.profile.objectiveHistory.Count(e=>e.runId==sourceRun)==1 &&
                priorRetry.profile.materials.SequenceEqual(persisted.profile.materials);
            if(!capacityStepPassed) Finish(false,"real commit or duplicate rejected",persisted.revision);
            yield break;
        }
        saves.WriteValidationHook=phase=>{if(phase=="before-publish")throw new IOException("UX05 injected before publish");};
        bool failed = !flow.CommitSettlement();
        saves.WriteValidationHook=null;
        if (!failed || !saves.LoadProgress() || flow.Settlement?.status!=SettlementStatus.Pending ||
            flow.Settlement.plan.objectiveHistory.Last().committedAtUtc!=row.committedAtUtc)
        {Finish(false,"failed publication did not preserve original Pending",pending.revision);yield break;}
        EventLog("pending-restored",JsonUtility.ToJson(flow.Settlement.plan.objectiveHistory.Last()));
        saves.WriteValidationHook=phase=>{if(phase=="after-publish")throw new IOException("UX05 injected after publish");};
        bool recorded=flow.CommitSettlement();
        saves.WriteValidationHook=null;
        var committed=CombatSaveSystem.InspectReadOnly(save);
        bool replay=flow.CommitSettlement();
        bool acknowledged=flow.AcknowledgeSettlement();
        var after=CombatSaveSystem.InspectReadOnly(save);
        bool ok=recorded && replay && acknowledged && committed.settlement.status==SettlementStatus.Committed &&
            committed.profile.committedRuns.Count(id=>id==sourceRun)==1 &&
            after.profile.objectiveHistory.Count(e=>e.runId==sourceRun)==1 &&
            after.profile.objectiveHistory.Last().committedAtUtc==row.committedAtUtc &&
            after.profile.objectiveHistory.Last().completedAtUtc==row.completedAtUtc &&
            JsonUtility.ToJson(committed.profile.objectiveHistory.Last())==JsonUtility.ToJson(after.profile.objectiveHistory.Last()) &&
            committed.profile.materials.SequenceEqual(after.profile.materials);
        EventLog("committed-readback",JsonUtility.ToJson(after.profile.objectiveHistory.LastOrDefault()));
        Finish(ok,"actual chest and extraction chain; controlled navigation; fail-before / verify-after / duplicate commit",after.revision);
    }
#endif

#if UX05_V9_FIXTURE_PROBE
    IEnumerator ProduceV9Pending(CombatSaveSystem saves, CombatSaveData initial)
    {
        var session=FindAnyObjectByType<CombatSession>();
        var flow=session.Flow;
        var hero=session.hero;
        if (!flow.SelectExpeditionGoal(ExpeditionGoal.Treasure) || !flow.Depart(AdventureMode.ForestExploration))
        { Finish(false,"fixture departure rejected",initial.revision); yield break; }
        yield return null;
        int opened=0;
        foreach(var chest in session.Events.Points.Where(p=>p!=null && p.Kind==WorldEventKind.Treasure && !p.Used).ToArray())
        {
            hero.RestorePosition(chest.transform.position + new Vector3(0,.1f,-1.7f),0);
            session.orbit.RestoreView(0,8);
            Physics.SyncTransforms();
            yield return null;
            bool interacted=chest.Interact(hero);
            EventLog("v9-fixture-chest",chest.entityId+" "+interacted);
            if (interacted && chest.Used && ++opened==3) break;
        }
        if (opened!=3) {Finish(false,"three chests not opened",initial.revision);yield break;}
        var exit=flow.ExitConfigs().FirstOrDefault(e=>e.id=="exit:entry" && !e.repairRequired);
        if (exit==null){Finish(false,"entry exit unavailable",initial.revision);yield break;}
        hero.RestorePosition(exit.position,0);
        Physics.SyncTransforms();
        yield return null;
        if (!flow.BeginExtraction(exit.id)){Finish(false,"extraction rejected",initial.revision);yield break;}
        float until=Time.realtimeSinceStartup+20;
        while (!flow.HasResult && Time.realtimeSinceStartup<until && flow.ActiveRun?.phase==RunPhase.Extracting)
            yield return null;
        if(mode=="objective-capacity" && !flow.HasResult) Time.timeScale=1;
        var pending=CombatSaveSystem.InspectReadOnly(save);
        bool ok=pending.hasActiveRun && pending.hasSettlement && pending.settlement.status==SettlementStatus.Pending &&
            pending.settlement.outcome==AdventureOutcome.Extracted && pending.activeRun.checkpoint.loot.Length>0;
        EventLog("fixture-live-paged-loot",pending.activeRun?.checkpoint?.loot?.Length.ToString());
        Finish(ok,"legacy Player Pending fixture with actual world drops",pending.revision);
    }
#endif

#if UX05_V10_OBJECTIVE_PROBE
    IEnumerator InspectHistoryView(CombatSaveSystem saves, long revision)
    {
        var session=FindAnyObjectByType<CombatSession>();
        session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
        string before=SaveSchemaMigration.FingerprintFile(saves.SavePath);
        yield return null;
        yield return new WaitForEndOfFrame();
        var canvas=FindObjectsByType<Canvas>(FindObjectsSortMode.None).SingleOrDefault(c=>c.name=="冒险历程入口");
        if (canvas==null || !ClickIn(canvas, "冒险历程"))
        {Finish(false,"history uGUI entry not present",revision);yield break;}
        yield return null;
        bool displayed=ViewContains(canvas,"扫箱") && ViewContains(canvas,"成功撤离");
        bool filtered=ClickIn(canvas,"全部地区");
        yield return null;
        filtered=filtered && ViewContains(canvas,"扫箱") && ClickIn(canvas,"全部类型");
        yield return null;
        filtered=filtered && ViewContains(canvas,"当前筛选无匹配目标") && ClickIn(canvas,"采集");
        yield return null;
        filtered=filtered && ViewContains(canvas,"扫箱");
        bool unchanged=SaveSchemaMigration.FingerprintFile(saves.SavePath)==before;
        EventLog("history-view-rendered",string.Join("\n",canvas.GetComponentsInChildren<Text>().Select(t=>t.text)));
        Finish(displayed&&filtered&&unchanged,"uGUI entry, history name, region/type filter and no save mutation",revision);
    }

    static bool ViewContains(Canvas canvas,string value) =>
        canvas.GetComponentsInChildren<Text>().Any(text=>text.text.Contains(value));

    bool ClickIn(Canvas canvas,string title)
    {
        var button=canvas.GetComponentsInChildren<Button>().SingleOrDefault(b=>b.name==title&&b.interactable);
        if(button==null||EventSystem.current==null)return false;
        EventLog("history-pointer-click",title);
        return ExecuteEvents.Execute(button.gameObject,new PointerEventData(EventSystem.current){button=PointerEventData.InputButton.Left},ExecuteEvents.pointerClickHandler);
    }
#endif

#if UX05_V10_OBJECTIVE_PROBE
    IEnumerator CheckProtectedInventory(CombatSaveSystem saves, long revision)
    {
        var session=FindAnyObjectByType<CombatSession>();
        var gear=session.hero.GetComponent<AdventureLoadout>();
        session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
        yield return null;
        var gold=gear.items.FirstOrDefault(i=>i.quality==GearQuality.Gold&&i.InBag&&!gear.Carried(i));
        var red=gear.items.FirstOrDefault(i=>i.quality==GearQuality.Red&&i.InBag&&!gear.Carried(i));
        if(gold==null||red==null){Finish(false,"B1 fixture missing bag gold/red",revision);yield break;}
        int ore=session.hero.Inventory.Count(MaterialKind.Ore);
        gear.Salvage(gold);
        gear.Salvage(red);
        bool gated=gear.items.Any(i=>i.id==gold.id)&&gear.items.Any(i=>i.id==red.id)&&
            session.hero.Inventory.Count(MaterialKind.Ore)==ore;
        EventLog("B1-real-salvage-gate",gold.id+" "+red.id+" kept="+gated);
        bool deposit=session.Camp.DepositEquipment(gold.id);
        if(!deposit || !session.Flow.Profile.warehouse.Any(i=>i.id==gold.id))
        {Finish(false,"gold warehouse deposit failed",revision);yield break;}
        bool withdrew=session.Camp.WithdrawEquipment(gold.id);
        var candidate=gear.items.FirstOrDefault(i=>i.id==gold.id);
        if(!withdrew||candidate==null||gear.Main==null)
        {Finish(false,"gold withdraw or main missing",revision);yield break;}
        string before=SaveSchemaMigration.FingerprintFile(save);
        bool favorited=B2Collection.Add(candidate.id) && B2Collection.IsFavorite(candidate.id) &&
            !B2Collection.CanQuickDismantle(candidate);
        var position=new Vector2Int(candidate.x,candidate.y);
        string oldMain=gear.Main.id;
        var invalid=gear.PreviewReplace(candidate.id,red.id,position,B2EquipRole.Main);
        var prediction=gear.PreviewReplace(candidate.id,oldMain,position,B2EquipRole.Main);
        bool previewReadOnly=gear.Main.id==oldMain && SaveSchemaMigration.FingerprintFile(save)==before;
        bool replaced=prediction.feasible&&gear.ApplyReplace(candidate.id,oldMain,position,B2EquipRole.Main,out _);
        bool predicted=replaced&&gear.Main.id==candidate.id&&
            Mathf.Abs(gear.AttackSnapshot().attackPower-prediction.after.attackPower)<.0001f;
        EventLog("B2-replace-business-path","candidate="+candidate.id+" old="+oldMain+
            " feasible="+prediction.feasible+" nonmutating="+previewReadOnly+" actualMatches="+predicted);
        Finish(gated&&favorited&&previewReadOnly&&!invalid.feasible&&predicted,
            "B1 real gold/red gates and warehouse; B2 favorite, wrong-ID rejection and real preview/apply",revision);
    }
#endif

#if UX_ACCEPTANCE && UX05_V10_OBJECTIVE_PROBE
    void RunMigrationBoundary(GameEntry entry, TitleMenu menu)
    {
        var phase = mode.Substring("r1-migrate-".Length);
        bool hit = false;
        void Observe(string check, string path)
        {
            bool invalid = phase == "bad-candidate" && check == "candidate-ready";
            bool lost = phase == "lost-receipt" && check == "after-replace";
            if (!(check == phase || invalid || lost)) return;
            hit = true;
            EventLog("r1-migration-boundary", check);
            if (invalid)
            {
                var envelope = JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(path));
                envelope.checksum = new string('0',64);
                File.WriteAllText(path,JsonUtility.ToJson(envelope));
                return;
            }
            if (lost) throw new IOException("R1 injected lost migration receipt");
            EventLog("migration-process-cut",check);
            System.Threading.Thread.Sleep(System.Threading.Timeout.Infinite);
        }
        SaveSchemaMigration.MigrationValidationHook = Observe;
        GroundLootStore.ValidationHook = check => Observe(check,null);
        bool clicked;
        try { clicked = Click(menu,"读取存档") && Click(menu,"明确选择新版"); }
        finally { SaveSchemaMigration.MigrationValidationHook = null; GroundLootStore.ValidationHook = null; }
        if (phase == "lost-receipt")
        {
            var current = CombatSaveSystem.InspectReadOnly(Path.Combine(entry.CurrentDirectory,"save.json"));
            bool ok = clicked && hit && current.sourceVersion == 10 &&
                current.profile.objectiveHistory.Length == 0 && current.profile.objectiveHistoryLegacyUnknown &&
                current.hasSettlement && current.settlement.status == SettlementStatus.Pending && entry.Info.canContinue;
            EventLog("migration-receipt-recovered",GameEntry.Error);
            Finish(ok,"published migration independently readable with unchanged legacy Pending",current.revision);
        }
        else
        {
            bool ok = clicked && hit && phase == "bad-candidate" && !Directory.Exists(entry.CurrentDirectory) &&
                !entry.Info.canContinue && !string.IsNullOrEmpty(GameEntry.Error);
            EventLog("migration-candidate-rejected",GameEntry.Error);
            Finish(ok,"checksum mismatch blocked candidate publication",0);
        }
    }
#endif

#if UX_ACCEPTANCE && UX05_V10_OBJECTIVE_PROBE
    bool VerifyR1CommitFailure(CombatSaveSystem saves, AdventureFlow flow, CombatSaveData pending, ObjectiveHistoryEntry row)
    {
        var previous = SaveSchemaMigration.FingerprintFile(save);
        string backup = save + ".bak";
        bool stale = mode=="r1-save-stale", arrived = false;
        FileStream denied = null;
        saves.WriteValidationHook = phase =>
        {
            if (phase != (stale?"before-publish":"after-publish")) return;
            arrived = true;
            if (stale) File.Copy(save, backup, true);
            else denied = new FileStream(save,FileMode.Open,FileAccess.Read,FileShare.None);
        };
        bool first, refused, paused;
        try
        {
            first = !flow.CommitSettlement();
            paused = flow.SettlementNeedsRead;
            refused = !flow.CommitSettlement() && !flow.AcknowledgeSettlement();
        }
        finally
        {
            saves.WriteValidationHook = null;
            denied?.Dispose();
        }
        var disk = CombatSaveSystem.InspectReadOnly(save);
        bool expected = stale
            ? previous == SaveSchemaMigration.FingerprintFile(save) && disk.revision == pending.revision &&
                disk.settlement.status == SettlementStatus.Pending
            : disk.revision == pending.revision + 1 && disk.settlement.status == SettlementStatus.Committed;
        EventLog("r1-commit-fault",$"arrived={arrived}; initialRejected={first}; needsRead={paused}; replayBlocked={refused}; expectedDisk={expected}");
        if(!(arrived && first && paused && refused && expected && saves.LoadProgress(false))) return false;
        if(stale && !flow.CommitSettlement()) return false;
        var final = CombatSaveSystem.InspectReadOnly(save);
        var fingerprint = SaveSchemaMigration.FingerprintFile(save);
        bool exact = final.settlement.status == SettlementStatus.Committed &&
            JsonUtility.ToJson(final.profile) == JsonUtility.ToJson(pending.settlement.plan) &&
            final.profile.objectiveHistory.Count(r=>r.SameKey(row)) == 1 &&
            JsonUtility.ToJson(final.profile.objectiveHistory.Single(r=>r.SameKey(row))) == JsonUtility.ToJson(row) &&
            final.profile.committedRuns.Count(r=>r==row.runId) == 1 &&
            flow.CommitSettlement() && SaveSchemaMigration.FingerprintFile(save)==fingerprint;
        EventLog("r1-commit-recovered",$"profileEqualsFrozenPlan={exact}; published={fingerprint}; run={row.runId}");
        return exact;
    }

    IEnumerator VerifyR1RuleProtection(CombatSaveSystem saves,CombatSaveData initial)
    {
        var session=FindAnyObjectByType<CombatSession>();
        var flow=session.Flow;
        var gear=session.hero.GetComponent<AdventureLoadout>();
        var run=new RunState{runId="r1-comparative-drop",regionInstanceId="r1-forest",seed=471,
            region=ObjectiveCatalog.Forest,mode=AdventureMode.ForestExploration,contentRevision=NewWeaponDrop.Revision("B06-B4-R1")};
        string SampleDrops()=>string.Join("|",Enumerable.Range(0,256).Select(i=>
            JsonUtility.ToJson(NewWeaponDrop.Preview(run,"enemy:"+i,EnemyArchetype.Melee))));
        string Snapshot()=>JsonUtility.ToJson(gear.AttackSnapshot())+"|"+gear.Defense.ToString("R",
            System.Globalization.CultureInfo.InvariantCulture)+"|"+string.Join(",",session.Camp.Materials)+"|"+
            string.Join(",",Enumerable.Range(0,6).Select(i=>session.hero.Inventory.Count((MaterialKind)i)))+"|"+
            string.Join(",",session.Camp.CaptureRecipes())+"|"+SampleDrops();
        var baseline=Snapshot();
        var original=flow.Profile.regions;
        string saveFingerprint=SaveSchemaMigration.FingerprintFile(save);
        string[] evidence = { "ForestRuins", "AncientRuins", "CrystalCavern", "forest:hunts-complete" };
        bool equal=true;
        foreach(var region in evidence)
        {
            // Controlled in-memory view of the same player. Never store contradictory boss or region metadata.
            flow.Profile.regions=original.Concat(new[]{region}).Distinct().ToArray();
            session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
            yield return null;
            var value=Snapshot();
            bool same=baseline==value;
            EventLog("r1-region-reward-comparison",region+" attack,defense,bag,warehouse,recipes,256 deterministic drop results: "+same);
            equal=equal && same;
        }
        flow.Profile.regions=original;
        EventLog("r1-region-reward-baseline",baseline);
        Finish(equal && saveFingerprint==SaveSchemaMigration.FingerprintFile(save),
            "runtime isolated comparison of proposed region metric inputs; same equipment, deterministic drop inputs, materials and recipes",initial.revision);
    }
    [System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential)]
    struct NativePoint { public int x, y; }

    [System.Runtime.InteropServices.DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
    [System.Runtime.InteropServices.DllImport("user32.dll")] static extern bool ClientToScreen(IntPtr window, ref NativePoint point);
    [System.Runtime.InteropServices.DllImport("user32.dll")] static extern bool SetCursorPos(int x, int y);
    [System.Runtime.InteropServices.DllImport("user32.dll")] static extern bool GetCursorPos(out NativePoint point);
    [System.Runtime.InteropServices.DllImport("user32.dll")]
    static extern void mouse_event(uint flags, uint x, uint y, uint data, UIntPtr extraInfo);

    IEnumerator VerifyR1HistoryUI(CombatSaveSystem saves, CombatSaveData first)
    {
        var session = FindAnyObjectByType<CombatSession>();
        session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
        yield return new WaitForEndOfFrame();
        string fingerprint = SaveSchemaMigration.FingerprintFile(save);
        var original = ObjectiveCatalog.All.Single(c=>c.id=="forest.treasure");
        int at = Array.IndexOf(ObjectiveCatalog.All,original);
        ObjectiveCatalog.All[at] = new ObjectiveCard(original.id,original.region,original.goal,"R1 临时新名称",
            original.oneLine,original.nextHint,original.conditions);
        bool imgui = mode.Contains("imgui");
        var presenter = PlayerHudPresenter.Instance;
        if(imgui && presenter!=null) presenter.enabled=false;
        ObjectiveHistoryEntry[] painted = null;
        string notice = null;
        int viewedPage = 0, pageCount = 0;
        AdventureFlow.ObserveHistoryRepaint = (n,rows,p,total) => {notice=n;painted=rows;viewedPage=p;pageCount=total;};
        yield return null;
        var canvas=FindObjectsByType<Canvas>(FindObjectsSortMode.None).SingleOrDefault(c=>c.name=="冒险历程入口");
        var window = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle;
        bool nativeClickPosted = window != IntPtr.Zero;
        IEnumerator Activate(string label,float x,float y)
        {
            if(imgui)
            {
                // Pointer input is permitted only while our own isolated Player is foreground.
                var point=new NativePoint{x=(int)(x*CombatUI.Scale),y=(int)(y*CombatUI.Scale)};
                if(window==IntPtr.Zero || GetForegroundWindow()!=window ||
                    !ClientToScreen(window,ref point) || !GetCursorPos(out var originalCursor) ||
                    !SetCursorPos(point.x,point.y))
                { nativeClickPosted=false; yield break; }
                yield return new WaitForSecondsRealtime(.08f);
                if(GetForegroundWindow()!=window) { nativeClickPosted=false; yield break; }
                mouse_event(0x0002,0,0,0,UIntPtr.Zero);
                mouse_event(0x0004,0,0,0,UIntPtr.Zero);
                yield return new WaitForSecondsRealtime(.15f);
                if(GetForegroundWindow()==window) SetCursorPos(originalCursor.x,originalCursor.y);
            }
            else if(canvas!=null) ClickIn(canvas,label);
            EventLog("r1-history-input",label);
            yield return null;
            yield return new WaitForEndOfFrame();
        }
        float left=CombatUI.Width/2-530, top=CombatUI.Height/2-320;
        yield return Activate("冒险历程",CombatUI.Width-102,CombatUI.Height-41);
        string[] RenderedIds() => imgui ? (painted??Array.Empty<ObjectiveHistoryEntry>()).Select(r=>r.runId).ToArray()
            : canvas!=null ? canvas.GetComponentsInChildren<Text>().Where(t=>t.name=="Objective")
                .Select(t=>t.text.Substring(t.text.LastIndexOf(" Run ",StringComparison.Ordinal)+5)).ToArray() : Array.Empty<string>();
        bool Notice(string value) => imgui ? notice!=null && notice.Contains(value) : canvas!=null && ViewContains(canvas,value);
        bool Page(int current,int total) => imgui ? viewedPage==current && pageCount==total : Notice(current+" / "+total);
        var expected = first.profile.objectiveHistory.OrderByDescending(r=>r.completedAtUtc,StringComparer.Ordinal)
            .ThenByDescending(r=>r.committedAtUtc,StringComparer.Ordinal).ThenBy(r=>r.runId,StringComparer.Ordinal).ToArray();
        bool ok;
        if(expected.Length==0)
        {
            ok=Page(1,1) && Notice("尚无已记录的完成目标") &&
                Notice("旧版目标历史未知")==first.profile.objectiveHistoryLegacyUnknown;
        }
        else
        {
            int pages=(expected.Length+19)/20;
            ok=pages==7;
            for(int p=1;p<=pages;p++)
            {
                var ids=RenderedIds();
                EventLog("r1-history-render",$"{p}/{pages} "+string.Join(",",ids));
                ok=ok && Page(p,pages) && ids.SequenceEqual(expected.Skip((p-1)*20).Take(20).Select(r=>r.runId));
                if(p<pages) yield return Activate("下一页",left+254,top+586);
            }
            yield return Activate("上一页",left+100,top+586);
            ok=ok && Page(6,7);
            yield return Activate("全部地区",left+108,top+92);
            var forest=expected.Where(r=>r.regionId==ObjectiveCatalog.Forest).ToArray();
            ok=ok && RenderedIds().SequenceEqual(forest.Take(20).Select(r=>r.runId));
            yield return Activate("全部类型",left+220,top+92);
            ok=ok && RenderedIds().Length==0 && Notice("当前筛选无匹配目标");
            yield return Activate("采集",left+220,top+92);
            ok=ok && RenderedIds().SequenceEqual(forest.Where(r=>r.objectiveId=="forest.treasure").Take(20).Select(r=>r.runId));
            ok=ok && (imgui ? painted.All(r=>r.displayNameSnapshot=="扫箱") : Notice("扫箱") && !Notice("R1 临时新名称"));
        }
        yield return Activate("关闭",left+915,top+92);
        bool closed=imgui ? !(bool)typeof(AdventureFlow).GetField("historyOpen",System.Reflection.BindingFlags.Instance|System.Reflection.BindingFlags.NonPublic).GetValue(session.Flow)
            : canvas!=null && !ViewContains(canvas,"按完成时间从新到旧") && !ViewContains(canvas,"尚无已记录的完成目标");
        AdventureFlow.ObserveHistoryRepaint=null;
        ObjectiveCatalog.All[at]=original;
        if(imgui && presenter!=null) presenter.enabled=true;
        EventLog("r1-history-summary",$"imgui={imgui}; nativeClickPosted={nativeClickPosted}; history={expected.Length}; unknown={first.profile.objectiveHistoryLegacyUnknown}; render={ok}; closed={closed}");
        Finish(ok && closed && fingerprint==SaveSchemaMigration.FingerprintFile(save),
            "actual history controls, sorted rows, title snapshot and unchanged save",first.revision);
    }
#endif

    bool Click(TitleMenu menu,string title)
    {
        var button = menu.GetComponentsInChildren<Button>()
            .SingleOrDefault(b => b.gameObject.name == title && b.isActiveAndEnabled && b.interactable);
        if (button == null || EventSystem.current == null) return false;
        var click = new PointerEventData(EventSystem.current) { button = PointerEventData.InputButton.Left };
        EventLog("pointer-click",title);
        return ExecuteEvents.Execute(button.gameObject,click,ExecuteEvents.pointerClickHandler);
    }

    void EventLog(string name,string detail)
    {
        File.AppendAllText(Path.Combine(evidence,"events.jsonl"),
            JsonUtility.ToJson(new Event {name=name,detail=detail,utc=DateTime.UtcNow.ToString("o")}) + "\n");
    }

    void Finish(bool ok,string cause,long revision)
    {
        File.WriteAllText(Path.Combine(evidence,"result.json"),JsonUtility.ToJson(new Result {
            status=ok?"PASS":"FAIL",reason=cause,mode=mode,initialRevision=initialRevision,finalRevision=revision},true));
        Application.Quit(ok?0:1);
    }
}
#endif









