#if UX06_ACCEPTANCE
using System;
using System.Collections;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.AI;
using UnityEngine.InputSystem.LowLevel;

// Isolated acceptance only. Drives existing entry/departure/settlement APIs and
// actual input controls for movement/interactions. Never sets positions, HP,
// event flags, receipts or ObjectiveHistory. UI native input is checked separately.
public sealed class RegionRecordsPlayerProbe : MonoBehaviour
{
    string root,region,runId,output;
    Keyboard keyboard;
    bool walkFailed,finishing;
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void Boot()
    {
        var args=Environment.GetCommandLineArgs();int at=Array.IndexOf(args,"-ux06-region");
        if(at<0)return;
        string isolated=ValidationStorage.Root(args,true);
        if(isolated==null || at+2>=args.Length)throw new Exception("Explicit isolation and Run ID required");
        var go=new GameObject("UX06 isolated Player driver");DontDestroyOnLoad(go);
        var probe=go.AddComponent<RegionRecordsPlayerProbe>();probe.root=isolated;
        probe.region=args[at+1];probe.runId=args[at+2];
        probe.output=Path.Combine(isolated,"ux06-results",probe.runId);Directory.CreateDirectory(probe.output);
        Application.runInBackground=true;probe.StartCoroutine(probe.Run());
    }
    void Log(string name,string data)
    { File.AppendAllText(Path.Combine(output,"events.jsonl"),JsonUtility.ToJson(new Event{name=name,data=data,utc=DateTime.UtcNow.ToString("o")})+"\n"); }
    [Serializable] class Event {public string name,data,utc;}
    [Serializable] class UiState
    { public bool historyOpen,regionRecordsOpen,ugui;public int regionIndex,historyRegion,historyPage,historyType,regionPage;public long revision;public string profile,visibleText,globalRng,saveSha;public float attack,defense; }
    object Read(AdventureFlow f,string name)=>typeof(AdventureFlow).GetField(name,System.Reflection.BindingFlags.NonPublic|System.Reflection.BindingFlags.Instance).GetValue(f);
    [Serializable] class Result {public string verdict,reason,runId,region;public int pid;}
    void Finish(bool ok,string reason)
    {
        if(finishing)return;finishing=true;
        if(keyboard!=null)InputSystem.QueueStateEvent(keyboard,new KeyboardState());
        File.WriteAllText(Path.Combine(output,"result.json"),JsonUtility.ToJson(new Result{verdict=ok?"PASS":"FAIL",reason=reason,runId=runId,region=region,pid=System.Diagnostics.Process.GetCurrentProcess().Id},true));
        StartCoroutine(QuitAfterUpdate(ok?0:1));
    }
    IEnumerator QuitAfterUpdate(int code)
    {
        yield return null;yield return new WaitForSecondsRealtime(.3f);
        Log("normal-quit-request","exit="+code+"; outside screenshot/end-of-frame callback");
        Application.Quit(code);
    }
    IEnumerator Run()
    {
        float end=Time.realtimeSinceStartup+120;
        while(GameEntry.Instance?.Info==null && Time.realtimeSinceStartup<end)yield return null;
        var entry=GameEntry.Instance;
        if(entry==null){Finish(false,"title timeout");yield break;}
        if(entry.Info.canContinue){if(!entry.Continue()){Finish(false,"continue rejected");yield break;}}
        else { entry.AskNew();if(!entry.ConfirmNew()){Finish(false,"new profile rejected");yield break;} }
        CombatSession session=null;
        while(Time.realtimeSinceStartup<end)
        { session=FindAnyObjectByType<CombatSession>();if(session?.Saves.IsInitialized==true && !GameEntry.Loading)break;yield return null; }
        if(session?.Saves.IsInitialized!=true){Finish(false,"game ready timeout");yield break;}
        var flow=session.Flow;
        if(!flow.AtCamp || flow.HasResult){Finish(false,"expected camp without unsettled result");yield break;}
        var before=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
        Log("cold-published-profile",JsonUtility.ToJson(before.profile));
        if(region=="ui")
        {
            Log("ui-awaiting-foreground",output);
            float foregroundDeadline=Time.realtimeSinceStartup+120;
            while((!File.Exists(Path.Combine(output,"start.signal")) || !Application.isFocused || !PlayerInput.Focused) && Time.realtimeSinceStartup<foregroundDeadline)yield return null;
            if(!Application.isFocused||!PlayerInput.Focused){Finish(false,"UI foreground not confirmed");yield break;}
            yield return new WaitForSecondsRealtime(.5f);
            float originalInterval=session.Saves.autoSaveInterval;
            session.Saves.autoSaveInterval=3600;
            Log("ui-timing-control","test-only autosave interval=3600; first scheduled normal autosave allowed; original="+originalInterval);
            long beforeScheduled=flow.Revision;float saveWait=Time.realtimeSinceStartup+12;
            while(flow.Revision==beforeScheduled && Time.realtimeSinceStartup<saveWait)yield return null;
            if(flow.Revision==beforeScheduled){Finish(false,"UI timing control failed to observe scheduled autosave");yield break;}
            before=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
            Log("ui-ready",session.Saves.SavePath);
            session.hero.Inventory.OpenPage(PlayerInventory.Page.Camp);
            yield return null;yield return null;
            string memoryBefore=JsonUtility.ToJson(flow.Profile),rngBefore=JsonUtility.ToJson(UnityEngine.Random.state);
            float attackBefore=session.hero.AttackPower,defenseBefore=session.hero.Defense;
            File.WriteAllText(Path.Combine(output,"readonly-baseline.json"),JsonUtility.ToJson(new UiState {revision=flow.Revision,profile=memoryBefore,globalRng=rngBefore,attack=attackBefore,defense=defenseBefore,saveSha=SaveSchemaMigration.FingerprintFile(session.Saves.SavePath)},true));
            // Read-only telemetry. Commands only finish or switch renderer, never construct data.
            while(Time.realtimeSinceStartup<end+1500)
            {
                var visible=FindObjectsByType<UnityEngine.UI.Text>(FindObjectsSortMode.None).Where(t=>t.isActiveAndEnabled);
                File.WriteAllText(Path.Combine(output,"ui-state.json"),JsonUtility.ToJson(new UiState {
                    historyOpen=(bool)Read(flow,"historyOpen"),regionRecordsOpen=(bool)Read(flow,"regionRecordsOpen"),
                    regionPage=(int)Read(flow,"regionRecordPage"),ugui=PlayerHudPresenter.Running,regionIndex=(int)Read(flow,"regionRecordIndex"),
                    historyRegion=(int)Read(flow,"historyRegion"),historyPage=(int)Read(flow,"historyPage"),historyType=(int)Read(flow,"historyType"),
                    revision=flow.Revision,profile=JsonUtility.ToJson(flow.Profile),globalRng=JsonUtility.ToJson(UnityEngine.Random.state),attack=session.hero.AttackPower,defense=session.hero.Defense,visibleText=string.Join("\n",visible.Select(t=>t.text))},true));
                var command=Path.Combine(output,"command.txt");
                if(File.Exists(command))
                {
                    string value=File.ReadAllText(command).Trim();File.Move(command,command+"."+Time.frameCount);
                    if(value=="capture") { ScreenCapture.CaptureScreenshot(Path.Combine(output,"ui-"+Time.frameCount+".png"));Log("screenshot",Time.frameCount.ToString()); }
                    else if(value=="imgui") { PlayerHudPresenter.Instance.enabled=false;Log("renderer","IMGUI"); }
                    else if(value=="ugui") { PlayerHudPresenter.Instance.enabled=true;Log("renderer","uGUI"); }
                    else if(value=="finish")
                    {
                        var after=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
                        bool unchanged=JsonUtility.ToJson(before)==JsonUtility.ToJson(after) && memoryBefore==JsonUtility.ToJson(flow.Profile) && rngBefore==JsonUtility.ToJson(UnityEngine.Random.state) && attackBefore==session.hero.AttackPower && defenseBefore==session.hero.Defense;
                        File.WriteAllText(Path.Combine(output,"readonly-final.json"),JsonUtility.ToJson(new UiState {revision=flow.Revision,profile=JsonUtility.ToJson(flow.Profile),globalRng=JsonUtility.ToJson(UnityEngine.Random.state),attack=session.hero.AttackPower,defense=session.hero.Defense,saveSha=SaveSchemaMigration.FingerprintFile(session.Saves.SavePath)},true));
                        session.Saves.autoSaveInterval=originalInterval;
                        Log("read-only-check","revision="+after.revision+"; unchanged="+unchanged+"; original autosave interval restored; normal exit save is outside observation window");
                        Finish(unchanged,"native UI observation completed; all read-only comparisons="+unchanged);yield break;
                    }
                }
                yield return new WaitForSecondsRealtime(.25f);
            }
            Finish(false,"UI observation timeout");yield break;
        }
        Log("awaiting-foreground",output);
        float focusDeadline=Time.realtimeSinceStartup+120;
        while(!File.Exists(Path.Combine(output,"start.signal")) && Time.realtimeSinceStartup<focusDeadline)yield return null;
        if(!File.Exists(Path.Combine(output,"start.signal"))){Finish(false,"external foreground confirmation not received");yield break;}
        keyboard=InputSystem.AddDevice<Keyboard>();keyboard.MakeCurrent();
        flow.SelectExpeditionGoal(ExpeditionGoal.Treasure);
        bool departed=region==ObjectiveCatalog.Ruins?flow.DepartRuins():region==ObjectiveCatalog.Cavern?flow.DepartCavern():flow.Depart(AdventureMode.ForestExploration);
        if(!departed){Finish(false,"departure rejected "+flow.DepartureReason);yield break;}
        Log("product-departure",flow.ActiveRun.runId+" "+flow.ActiveRun.region);
        yield return new WaitForSecondsRealtime(.5f);
        if(region==ObjectiveCatalog.Forest)
        {
            var chests=session.Events.Points.Where(p=>p.Kind==WorldEventKind.Treasure).OrderBy(p=>Vector3.Distance(session.hero.transform.position,p.transform.position)).Take(3).ToArray();
            foreach(var chest in chests){yield return Interact(session,chest);if(walkFailed)break;}
        }
        else if(region==ObjectiveCatalog.Ruins)
        {
            foreach(var id in new[]{"c1:lever","c1:door","c1:archive","c1:hidden"})
            { yield return Interact(session,session.Events.Points.Single(p=>p.entityId==id));if(walkFailed)break; }
        }
        else
        {
            yield return Walk(session,new Vector3(0,0,405),1.5f);
            if(!walkFailed)yield return Interact(session,session.Events.Points.Single(p=>p.entityId==CrystalCavernLayout.Lever));
            if(!walkFailed)yield return Interact(session,session.Events.Points.Single(p=>p.entityId==CrystalCavernLayout.Chest));
            if(!walkFailed)yield return Walk(session,new Vector3(0,0,410),1.5f);
            if(!walkFailed)yield return Walk(session,new Vector3(43,0,430),1.5f);
            if(!walkFailed)yield return Walk(session,new Vector3(58,0,432),1.5f);
            if(!walkFailed)yield return Interact(session,session.Events.Points.Single(p=>p.entityId==CrystalCavernLayout.BridgeLever));
            if(!walkFailed)yield return Interact(session,session.Events.Points.Single(p=>p.entityId==CrystalCavernLayout.LakeChest));
        }
        if(walkFailed || session.hero.Health.Dead){Finish(false,"natural movement or interaction failed; no state bypass");yield break;}
        Log("objective-live",ObjectiveEvaluator.Evaluate(ObjectiveEvaluator.Live(session)).ToString());
        var alive=session.enemies.Where(e=>e!=null && !e.Health.Dead).ToArray();
        var exit=flow.ExitConfigs().Where(e=>!e.repairRequired)
            .OrderByDescending(e=>alive.Length==0?999f:alive.Min(a=>Vector3.Distance(a.transform.position,e.position))).First();
        Log("safe-exit-selected",exit.id+" reason="+flow.ExtractionReasonFor(exit));
        yield return Walk(session,exit.position,1.2f);
        if(walkFailed){Finish(false,"return walk failed");yield break;}
        yield return Press(Key.H);
        end=Time.realtimeSinceStartup+30;
        while(!flow.HasResult&&Time.realtimeSinceStartup<end)yield return null;
        if(!flow.HasResult){Finish(false,"normal extraction did not produce settlement");yield break;}
        Log("pending",JsonUtility.ToJson(CombatSaveSystem.InspectReadOnly(session.Saves.SavePath)));
        if(!flow.CommitSettlement()){Finish(false,"commit rejected");yield break;}
        var committed=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
        Log("committed",JsonUtility.ToJson(committed));
        if(!flow.AcknowledgeSettlement()){Finish(false,"camp return rejected");yield break;}
        var published=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
        string profile=JsonUtility.ToJson(published.profile);
        for(int i=0;i<10;i++)foreach(string id in new[]{ObjectiveCatalog.Forest,ObjectiveCatalog.Ruins,ObjectiveCatalog.Cavern})
            { var view=RegionRecords.Query(published.profile,id);Log("region-query",view.title+" | "+view.coverage+" | "+string.Join(" | ",view.records)+" | "+string.Join(" | ",view.recent)); }
        bool retained=published.profile.objectiveHistory.Any(e=>e.runId==committed.settlement.runId);
        bool readOnly=profile==JsonUtility.ToJson(published.profile);
        ScreenCapture.CaptureScreenshot(Path.Combine(output,"camp.png"));yield return new WaitForEndOfFrame();
        Finish(retained&&readOnly&&committed.settlement.status==SettlementStatus.Committed,"normal movement/interactions/extraction; retained="+retained+"; projection readOnly="+readOnly);
    }
    IEnumerator Press(Key key)
    {
        InputSystem.QueueStateEvent(keyboard,new KeyboardState(key));Log("input-key",key.ToString());
        yield return new WaitForSecondsRealtime(.12f);
        InputSystem.QueueStateEvent(keyboard,new KeyboardState());yield return new WaitForSecondsRealtime(.15f);
    }
    IEnumerator Interact(CombatSession session,WorldEventPoint point)
    {
        yield return Walk(session,point.transform.position,1.75f);
        if(walkFailed)yield break;
        for(int i=0;i<4&&!point.Used;i++)yield return Press(Key.E);
        Log("product-interaction",point.entityId+" used="+point.Used+" at="+session.hero.transform.position);
        if(!point.Used)walkFailed=true;
    }
    // Reuses the P1C driver's periodically recomputed NavMesh path and
    // short back/side detours. These are real directional inputs, not world edits.
    IEnumerator Walk(CombatSession session,Vector3 goal,float range)
    {
        var hero=session.hero;var path=new NavMeshPath();Vector3[] corners=null;
        float end=Time.realtimeSinceStartup+150,repathAt=0,checkAt=Time.realtimeSinceStartup;
        float duty=0,sampleAt=0,detourUntil=0;int detours=0,sign=1;
        Vector3 last=hero.transform.position,detour=Vector3.zero;
        Log("walk-start",last+" -> "+goal);
        while(Vector3.ProjectOnPlane(goal-hero.transform.position,Vector3.up).magnitude>range)
        {
            float now=Time.realtimeSinceStartup;
            if(hero.Health.Dead||now>end){walkFailed=true;break;}
            if(hero.Progression.IsChoosing){yield return Press(Key.Digit1);continue;}
            if(now>=repathAt)
            {
                repathAt=now+.8f;
                bool ok=NavMesh.SamplePosition(hero.transform.position,out var start,6,NavMesh.AllAreas) &&
                    NavMesh.SamplePosition(goal,out var finish,6,NavMesh.AllAreas) &&
                    NavMesh.CalculatePath(start.position,finish.position,NavMesh.AllAreas,path) &&
                    path.status==NavMeshPathStatus.PathComplete;
                corners=ok?path.corners:null;
            }
            Vector3 direction=Vector3.ProjectOnPlane(goal-hero.transform.position,Vector3.up);
            if(corners!=null && corners.Length>1)
            {
                int i=1;while(i<corners.Length-1 && Vector3.ProjectOnPlane(corners[i]-hero.transform.position,Vector3.up).magnitude<1.1f)i++;
                direction=Vector3.ProjectOnPlane(corners[i]-hero.transform.position,Vector3.up);
            }
            if(now<detourUntil)direction=detour;
            if(now-checkAt>1.6f)
            {
                if(Vector3.Distance(last,hero.transform.position)<.6f)
                {
                    sign=-sign;detour=Vector3.Cross(Vector3.up,direction.normalized)*sign;
                    detourUntil=now+1.1f;detours++;
                    Log("walk-detour",hero.transform.position+" direction="+detour+" attempt="+detours);
                    if(detours>12){walkFailed=true;break;}
                }
                last=hero.transform.position;checkAt=now;
            }
            direction.Normalize();
            var forward=Vector3.ProjectOnPlane(hero.cameraTransform.forward,Vector3.up).normalized;
            var right=Vector3.ProjectOnPlane(hero.cameraTransform.right,Vector3.up).normalized;
            float x=Vector3.Dot(direction,right),y=Vector3.Dot(direction,forward);
            bool primaryX=Mathf.Abs(x)>Mathf.Abs(y);
            float ratio=primaryX?Mathf.Abs(y/x):Mathf.Abs(x/y);
            duty+=ratio/(.70710678f+.29289322f*ratio);
            bool secondary=duty>=1;if(secondary)duty-=1;
            var keys=new List<Key>();if(primaryX||secondary)keys.Add(x>=0?Key.D:Key.A);if(!primaryX||secondary)keys.Add(y>=0?Key.W:Key.S);
            if(Vector3.ProjectOnPlane(goal-hero.transform.position,Vector3.up).magnitude>4)keys.Add(Key.LeftShift);
            InputSystem.QueueStateEvent(keyboard,new KeyboardState(keys.ToArray()));
            if(now>=sampleAt)
            {sampleAt=now+.5f;Log("movement-input",hero.transform.position+" keys="+string.Join(",",keys)+" dt="+Time.deltaTime+" hp="+hero.Health.Current+" focused="+PlayerInput.Focused+" paused="+hero.GameplayPaused);}
            yield return null;
        }
        InputSystem.QueueStateEvent(keyboard,new KeyboardState());yield return new WaitForSecondsRealtime(.15f);
        if(walkFailed)
        {
            Log("walk-obstacles",string.Join(";",Physics.OverlapSphere(hero.transform.position,3).Select(c=>c.name+" "+c.bounds)));
            ScreenCapture.CaptureScreenshot(Path.Combine(output,"walk-failure.png"));yield return new WaitForEndOfFrame();
        }
        Log("walk-end",hero.transform.position+" success="+!walkFailed);
    }
}
#endif
