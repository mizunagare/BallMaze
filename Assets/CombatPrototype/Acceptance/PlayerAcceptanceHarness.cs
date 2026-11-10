#if UX_ACCEPTANCE
// ============================================================================
// UX-PROGRESSION-03A REAL PLAYER ACCEPTANCE HARNESS
// ----------------------------------------------------------------------------
// Compiled ONLY into the Acceptance Build (gated by the UX_ACCEPTANCE scripting
// define). Shipping / Release builds define nothing here, so this entire file
// compiles out and the shipping package contains zero harness / test markers.
//
// Runs INSIDE the real built Player (WanxiangGuitu.exe) and proves real gameplay:
//   1. Parses a per-run scenario + runId + buildSha + isolated data-root from the
//      command line (NEVER touches the default AppData / persistentDataPath).
//   2. Uses ONLY real product entry points + the public business API:
//        - GameEntry.Instance.Continue() / AskNew() + ConfirmNew()  (authorize)
//        - AdventureItems.New / AdventureLoadout.SelectMain            (loadout)
//        - WeaponSkillExpansion.Select (delegates to NewWeaponCombat for new
//          weapons) + PlayerInput.Focus / Barrier                     (skill slot)
//      It does NOT write any product private field, does NOT call internal
//      Release/Hit/ApplyDamage, does NOT kill enemies, does NOT fake affix
//      effects. Affixes are configured on the equipped item via the public
//      GearItem.affixes field (the product then applies them for real).
//   3. Injects REAL keyboard input via InputSystem (KeyDown then KeyUp) so the
//      skill travels the genuine PlayerInput -> AdventureCombat.UseSkill path.
//      A virtual keyboard is installed as the active Keyboard so injection is
//      deterministic regardless of any physical keyboard on the host.
//   4. Observes REAL business events: WeaponSkillExpansion.Observed /
//      NewWeaponCombat.Observed (skill lifecycle) and AdventureCombat.MeleeObserved
//      (real damage before/after).
//   5. Writes an isolated result JSON containing runId / processId / buildSha,
//      the observed skill lifecycle, damage, a cooldown allow/block verdict, and
//      an optional skill-description consistency check.
//   6. Quits with exit code 0 on PASS, 1 on FAIL (driver enforces this).
//
// MARKER string is grepped by the driver to PROVE presence in Acceptance EXE and
// ABSENCE from Shipping EXE.
// ============================================================================
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;

public static class PlayerAcceptanceHarness
{
    public const string MARKER = "UX_ACCEPTANCE_HARNESS_v1";
    public const int VERSION = 1;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void Bootstrap()
    {
        var args = Environment.GetCommandLineArgs();
        if (!args.Any(a => a == "--acceptance")) return; // never runs in a normal player session
        if (UnityEngine.Object.FindAnyObjectByType<HarnessRunner>() != null) return; // avoid duplicates across scene loads
        var go = new GameObject("UX Acceptance Harness");
        go.AddComponent<HarnessRunner>();
        UnityEngine.Object.DontDestroyOnLoad(go);
    }
}

public class HarnessRunner : MonoBehaviour
{
    // ---- parsed launch parameters -------------------------------------------
    string scenarioId = "unknown";
    string runId = "unknown";
    string buildSha = "unknown";
    string dataRoot = null;
    GearType weapon = GearType.Sword;
    GearQuality quality = GearQuality.White;
    int affix = -1;
    int slot = 1;
    float chargeSeconds = 0f;
    float expectedCooldown = 0f;
    string descContains = null;
    string descExcludes = null;
    bool expectZeroDamage = false;

    // ---- runtime state ------------------------------------------------------
    CombatSession session;
    ThirdPersonHero hero;
    AdventureCombat combat;
    WeaponSkillExpansion expanded;
    NewWeaponCombat newWeapons;
    AdventureLoadout gear;
    AdventureFlow flow;
    GameEntry gameEntry;
    float startedAt;
    string phase = "entry";
    float phaseEnteredAt;
    bool failed = false;
    string failReason = "";
    bool quitting = false;
    bool entryAttempted = false;
    bool entryAuthorized = false;
    bool departAttempted = false;

    // ---- recorded evidence --------------------------------------------------
    List<string> logLines = new List<string>();
    string logPath = null;
    List<Dictionary<string, object>> observations = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> damages = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> keyEvents = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> casts = new List<Dictionary<string, object>>();
    List<float> skillStarts = new List<float>();
    List<float> skillCompletes = new List<float>();
    float cast1DownAt = -1f, cast2DownAt = -1f, probeDownAt = -1f;
    bool blockedDuringCooldown = false;
    Keyboard virtKb = null;
    // Legacy slot-0 "basic skill" casts go through BeginAttack and emit NO
    // Observed start/complete events (those only exist for expansion skills and
    // new weapons). For those scenarios the public LastAttackId/LastAttackPhase
    // transition is the real cast evidence.
    bool useAttackPhaseProbe = false;
    long attackIdBaseline = 0;

    // ALL harness-internal timing uses UNSCALED time: GameEntry holds
    // Time.timeScale=0 until the save system boots, which would freeze
    // Time.time-based timeouts and silently hang the run.
    void Log(string s)
    {
        var line = string.Format("{0:0.000} [{1}] {2}", Time.unscaledTime, phase, s);
        logLines.Add(line);
        try { if (logPath != null) File.AppendAllText(logPath, line + "\n"); } catch { }
    }

    // ========================================================================
    // SETUP
    // ========================================================================
    void Start()
    {
        startedAt = Time.unscaledTime;
        ParseArgs();
        EnsureIsolatedRoot();
        EnsureKeyboard();
        phase = "entry"; phaseEnteredAt = Time.unscaledTime;
        Log("harness v" + PlayerAcceptanceHarness.VERSION + " scenario=" + scenarioId + " run=" + runId + " weapon=" + weapon + " slot=" + slot + " affix=" + affix + " charge=" + chargeSeconds + " cd=" + expectedCooldown);
    }

    void ParseArgs()
    {
        var args = Environment.GetCommandLineArgs();
        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "--scenario-id": scenarioId = SafeArg(args, ++i, scenarioId); break;
                case "--run-id": runId = SafeArg(args, ++i, runId); break;
                case "--build-sha": buildSha = SafeArg(args, ++i, buildSha); break;
                case "--data-root": dataRoot = SafeArg(args, ++i, dataRoot); break;
                case "--weapon": weapon = (GearType)Enum.Parse(typeof(GearType), SafeArg(args, ++i, "Sword")); break;
                case "--quality": quality = (GearQuality)Enum.Parse(typeof(GearQuality), SafeArg(args, ++i, "White")); break;
                case "--affix": affix = int.Parse(SafeArg(args, ++i, "-1")); break;
                case "--slot": slot = int.Parse(SafeArg(args, ++i, "1")); break;
                case "--charge": chargeSeconds = float.Parse(SafeArg(args, ++i, "0"), System.Globalization.CultureInfo.InvariantCulture); break;
                case "--expected-cooldown": expectedCooldown = float.Parse(SafeArg(args, ++i, "0"), System.Globalization.CultureInfo.InvariantCulture); break;
                case "--desc-contains": descContains = SafeArg(args, ++i, null); break;
                case "--desc-excludes": descExcludes = SafeArg(args, ++i, null); break;
                case "--expect-zero-damage": expectZeroDamage = SafeArg(args, ++i, "false") == "true"; break;
            }
        }
        if (string.IsNullOrEmpty(dataRoot))
        {
            // fall back to the isolated storage root the game itself uses
            for (int i = 0; i < args.Length; i++) if (args[i] == "-wanxiang-storage-root" && i + 1 < args.Length) { dataRoot = args[i + 1]; break; }
        }
    }
    static string SafeArg(string[] a, int i, string def) { return (i >= 0 && i < a.Length) ? a[i] : def; }

    void EnsureIsolatedRoot()
    {
        if (string.IsNullOrEmpty(dataRoot))
            dataRoot = Path.Combine(Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName), "acceptance_run_" + runId);
        Directory.CreateDirectory(dataRoot);
        logPath = Path.Combine(dataRoot, "harness.log");
    }

    // Force a virtual keyboard to be the active Keyboard so that the harness's
    // injected key events are the ones PlayerInput actually polls. On a host with
    // a physical keyboard, Keyboard.current would otherwise be the physical one
    // and injected events would never reach PlayerInput.
    void EnsureKeyboard()
    {
        try
        {
            var others = InputSystem.devices.Where(d => d is Keyboard && d != virtKb).ToList();
            foreach (var d in others) InputSystem.RemoveDevice(d);
            if (virtKb == null) virtKb = InputSystem.AddDevice<Keyboard>();
            Log("keyboard ready; current=" + (Keyboard.current != null ? Keyboard.current.name : "null") + " virtual=" + (virtKb != null ? virtKb.name : "null"));
        }
        catch (Exception e) { Log("keyboard ensure warn: " + e.Message); }
    }

    // ========================================================================
    // MAIN STATE MACHINE (runs every frame)
    // ========================================================================
    void Update()
    {
        if (quitting) return;
        try
        {
            if (phase == "entry") StepEntry();
            else if (phase == "waitScene") StepWaitScene();
            else Step();
        }
        catch (Exception e) { Fail("exception: " + e.GetType().Name + ": " + e.Message); }
    }

    // ---- real product entry flow (public API only) -------------------------
    void StepEntry()
    {
        if (Time.unscaledTime - phaseEnteredAt > 45f) { Fail("entry timeout: GameEntry never authorized gameplay"); return; }
        if (GameEntry.GameSceneAuthorized)
        {
            entryAuthorized = true;
            Enter("waitScene"); return;
        }
        if (gameEntry == null)
        {
            gameEntry = GameEntry.Instance;
            if (gameEntry == null) { Log("waiting for GameEntry.Instance..."); return; }
            Log("GameEntry.Instance present (Loading=" + GameEntry.Loading + ")");
        }
        if (!entryAttempted)
        {
            entryAttempted = true;
            bool ok = false;
            try { ok = gameEntry.Continue(); }       // public API: title -> continue flow
            catch (Exception e) { Log("Continue threw: " + e.Message); }
            if (!ok)
            {
                try { gameEntry.AskNew(); ok = gameEntry.ConfirmNew(); }
                catch (Exception e) { Log("NewGame threw: " + e.Message); }
            }
            Log("entry attempt ok=" + ok + " authorized=" + GameEntry.GameSceneAuthorized + " Loading=" + GameEntry.Loading);
        }
    }

    void StepWaitScene()
    {
        if (Time.unscaledTime - phaseEnteredAt > 60f) { Fail("waitScene timeout: gameplay scene never initialized"); return; }
        if (GameEntry.Loading) { Log("still loading..."); return; }
        session = UnityEngine.Object.FindAnyObjectByType<CombatSession>();
        if (session == null) { Log("no CombatSession yet..."); return; }
        if (session.Saves == null) { Log("Saves not created yet..."); return; }
        if (!session.Saves.IsInitialized) { Log("Saves not initialized yet..."); return; }
        // NOTE: the game legitimately holds Time.timeScale=0 while at camp.
        // Departure (AdventureFlow.Depart) restores timeScale=1 for the field.
        try { GameEntry.DirectReady(); } catch (Exception e) { Log("DirectReady warn: " + e.Message); }
        Enter("locate");
    }

    // ---- combat scenario ----------------------------------------------------
    void Step()
    {
        switch (phase)
        {
            case "locate":
                if (session == null) session = UnityEngine.Object.FindAnyObjectByType<CombatSession>();
                if (session == null) { if (Time.unscaledTime - phaseEnteredAt > 20f) Fail("no CombatSession in scene"); return; }
                hero = session.hero;
                if (hero == null || hero.Health == null) { if (Time.unscaledTime - phaseEnteredAt > 20f) Fail("hero/Health not ready"); return; }
                combat = hero.GetComponent<AdventureCombat>();
                gear = hero.GetComponent<AdventureLoadout>();
                expanded = combat != null ? combat.Expanded : null;
                newWeapons = combat != null ? combat.NewWeapons : null;
                if (combat == null) { Fail("no AdventureCombat on hero"); return; }
                Enter("setup");
                break;

            case "setup":
                // Equip the run loadout IN CAMP so Departure carries it into the
                // field (Depart restores the captured camp gear for the run).
                SetupLoadout();
                CheckDescription();
                Subscribe();
                Enter("depart");
                break;

            case "depart":
                if (Time.unscaledTime - phaseEnteredAt > 15f) { Fail("depart timeout"); return; }
                if (flow == null) flow = AdventureFlow.Find(hero);
                if (flow == null) { Log("waiting for AdventureFlow..."); return; }
                if (departAttempted) return;
                departAttempted = true;
                if (!flow.AtCamp) { Fail("not AtCamp at setup time; cannot depart"); return; }
                bool ok = false;
                try { ok = flow.DepartRuins(); } catch (Exception e) { Log("DepartRuins threw: " + e.Message); }
                Log("DepartRuins ok=" + ok + " reason='" + flow.DepartureReason + "' activeRun=" + (flow.ActiveRun != null));
                if (!ok) { Fail("departure rejected: " + flow.DepartureReason); return; }
                Enter("rearm");
                break;

            case "rearm":
                if (Time.unscaledTime - phaseEnteredAt > 10f) { Fail("rearm timeout"); return; }
                if (flow == null || flow.ActiveRun == null) { Log("waiting for ActiveRun..."); return; }
                if (Time.timeScale <= 0f) { Time.timeScale = 1f; Log("safety: restored timeScale=1 after departure"); }
                // Restart/Restore during Depart may reset transient selection state.
                if (expanded != null && !expanded.Select(slot)) Log("rearm: Select(slot=" + slot + ") returned false");
                PlayerInput.Focus(true);
                // legacy slot-0 basic skill: arm the attack-phase probe
                useAttackPhaseProbe = slot == 0 && (int)weapon < 4 && combat != null;
                if (useAttackPhaseProbe) { attackIdBaseline = combat.LastAttackId; Log("legacy slot-0 probe armed, baseline attackId=" + attackIdBaseline); }
                Enter("warmup");
                break;

            case "warmup":
                // give the field a moment to settle; do NOT read private Ready.
                if (Time.unscaledTime - phaseEnteredAt > 1.5f) Enter("cast1");
                break;

            case "cast1":
                ProbeLegacyCast();
                FaceNearestEnemy();
                // Focus(true) calls Barrier() internally; it must be applied ONCE
                // per cast attempt, never per frame (a per-frame Barrier keeps
                // UIBlocked true forever and blocks all input).
                if (cast1DownAt < 0f) { PlayerInput.Focus(true); Inject(true, Key.F); RecordCast("cast1", true); cast1DownAt = Time.unscaledTime; Log("F down (cast1)"); }
                if (cast1DownAt >= 0f && skillStarts.Count < 1 && Time.unscaledTime - cast1DownAt > 3f) { Inject(false, Key.F); Fail("cast1 produced no skill START (Selected=" + CurrentSelected() + " Focused=" + PlayerInput.Focused + " Suspended=" + PlayerInput.Suspended + " UIBlocked=" + PlayerInput.UIBlocked + " Ready=" + ReadyProbe() + ")"); return; }
                if (cast1DownAt >= 0f && skillStarts.Count >= 1)
                {
                    if (chargeSeconds > 0f)
                    {
                        if (Time.unscaledTime - cast1DownAt < chargeSeconds) return;
                        Inject(false, Key.F); Log("F up (cast1 charge done)");
                    }
                    else { Inject(false, Key.F); Log("F up (cast1)"); }
                    Enter("waitComplete1");
                }
                break;

            case "waitComplete1":
                ProbeLegacyCast();
                if (skillCompletes.Count >= 1) { Log("cast1 complete"); Enter(expectedCooldown > 0f ? "cooldownBlock" : "done"); }
                else if (Time.unscaledTime - cast1DownAt > 14f) Fail("cast1 never completed");
                break;

            case "cooldownBlock":
                if (skillStarts.Count < 1) { Fail("cooldownBlock reached without a first start"); return; }
                if (probeDownAt < 0f) { PlayerInput.Focus(true); Inject(true, Key.F); RecordCast("probeBlocked", true); probeDownAt = Time.unscaledTime; return; }
                if (Time.unscaledTime - probeDownAt < 0.7f) return;
                // 0.7s into the cooldown window: a SECOND start must NOT have appeared.
                Inject(false, Key.F); RecordCast("probeBlocked", false);
                if (skillStarts.Count >= 2)
                {
                    float gap = skillStarts[1] - skillStarts[0];
                    if (gap < expectedCooldown - 0.6f) { Fail("re-cast during cooldown was NOT blocked (cooldown broken); gap=" + gap.ToString("0.00") + " expected>=" + expectedCooldown); return; }
                }
                blockedDuringCooldown = true; Log("probe during cooldown correctly produced no early start");
                Enter("cooldownAllow");
                break;

            case "cooldownAllow":
                if (skillStarts.Count < 1) { Fail("cooldownAllow reached without a first start"); return; }
                float waitUntil = skillStarts[0] + expectedCooldown + 0.1f;
                if (Time.unscaledTime < waitUntil) return;
                if (cast2DownAt < 0f)
                {
                    FaceNearestEnemy();
                    PlayerInput.Focus(true);
                    Inject(true, Key.F); RecordCast("cast2", true); cast2DownAt = Time.unscaledTime; Log("F down (cast2, after cooldown)");
                }                if (cast2DownAt >= 0f && skillStarts.Count < 2 && Time.unscaledTime - cast2DownAt > 3f) { Inject(false, Key.F); Fail("cast2 after cooldown did not start (Selected=" + CurrentSelected() + ")"); return; }
                if (cast2DownAt >= 0f && skillStarts.Count >= 2)
                {
                    Inject(false, Key.F); Log("F up (cast2)");
                    Enter("done");
                }
                break;

            case "done":
                Finish();
                break;
        }
    }

    bool ReadyProbe() { try { return combat != null && hero != null && hero.Health != null && !hero.Health.Dead && PlayerInput.Focused; } catch { return false; } }

    // Real-cast evidence for legacy slot-0 basic skills via public combat state:
    // LastAttackId increments and LastAttackPhase leaves "Idle" when the cast runs.
    void ProbeLegacyCast()
    {
        if (!useAttackPhaseProbe || combat == null) return;
        if (skillStarts.Count == 0 && combat.LastAttackId > attackIdBaseline && combat.LastAttackPhase != "Idle")
        {
            skillStarts.Add(Time.unscaledTime);
            Log("OBS(legacy basic) start attackId=" + combat.LastAttackId + " phase=" + combat.LastAttackPhase);
        }
        if (skillStarts.Count > 0 && skillCompletes.Count == 0 && combat.LastAttackPhase == "Idle")
        {
            skillCompletes.Add(Time.unscaledTime);
            Log("OBS(legacy basic) complete");
        }
    }

    int CurrentSelected() { return expanded != null ? expanded.Selected : -1; }

    // ========================================================================
    // SCENARIO SETUP (public business API only)
    // ========================================================================
    void SetupLoadout()
    {
        if (gear == null) { Fail("AdventureLoadout missing"); return; }
        // Keep the worn containers (rig/bag) so Rig/Bag resolve and departure
        // rules pass; drop the default weapons, then carry exactly the weapon
        // this run exercises (AddOrStore places it properly in the bag).
        gear.items.RemoveAll(it => !it.worn && !it.Container);
        var weapon_item = AdventureItems.New(weapon, quality);
        weapon_item.affixes = affix >= 0 ? new int[] { affix } : new int[0];
        gear.AddOrStore(weapon_item);
        gear.mainWeapon = weapon_item.id;
        if (!gear.SelectMain(weapon_item)) Log("SelectMain returned false; forcing EquipmentChanged");
        // WeaponSkillExpansion.Select delegates to NewWeaponCombat.Select for new
        // weapons, so a single call covers both legacy and new weapon skill slots.
        if (expanded == null) { Fail("WeaponSkillExpansion missing"); return; }
        if (!expanded.Select(slot)) Log("Select(slot=" + slot + ") returned false");
        Log("loadout set: weapon=" + weapon + " quality=" + quality + " affix=" + affix + " slot=" + slot + " Selected=" + CurrentSelected() + " GearWeapon=" + gear.Weapon + " overflow=" + weapon_item.overflow);
    }

    void CheckDescription()
    {
        if (descContains == null && descExcludes == null) return;
        string desc = "";
        try { desc = combat != null ? combat.SkillDescription : ""; } catch (Exception e) { Log("SkillDescription read warn: " + e.Message); }
        Log("SkillDescription=" + desc);
        if (descContains != null && desc.IndexOf(descContains, StringComparison.Ordinal) < 0) Log("DESC_CHECK fail: missing '" + descContains + "'");
        if (descExcludes != null && desc.IndexOf(descExcludes, StringComparison.Ordinal) >= 0) Log("DESC_CHECK fail: unexpectedly contains '" + descExcludes + "'");
    }

    void Subscribe()
    {
        if (expanded != null) expanded.Observed += OnExpanded;
        if (newWeapons != null) newWeapons.Observed += OnNewWeapon;
        if (combat != null) combat.MeleeObserved += OnMelee;
    }
    void OnExpanded(WeaponSkillExpansion.Observation o)
    {
        var d = new Dictionary<string, object> { ["source"] = "expanded", ["skill"] = o.skill, ["stage"] = o.stage, ["attack"] = o.attack, ["pulse"] = o.pulse, ["time"] = o.time };
        observations.Add(d);
        if (o.stage == "start") { skillStarts.Add(Time.unscaledTime); Log("OBS start skill=" + o.skill); }
        if (o.stage == "complete") { skillCompletes.Add(Time.unscaledTime); Log("OBS complete skill=" + o.skill); }
    }
    void OnNewWeapon(NewWeaponCombat.Trace t)
    {
        var d = new Dictionary<string, object> { ["source"] = "newweapon", ["weapon"] = t.weapon, ["skill"] = t.skill, ["stage"] = t.stage, ["phase"] = t.phase, ["empowered"] = t.empowered, ["time"] = t.time };
        observations.Add(d);
        if (t.stage == "start") { skillStarts.Add(Time.unscaledTime); Log("OBS(new) start skill=" + t.skill); }
        if (t.stage == "complete") { skillCompletes.Add(Time.unscaledTime); Log("OBS(new) complete skill=" + t.skill); }
        if ((t.stage == "contact" || t.stage == "volume") && t.target != null && t.after < t.before)
            damages.Add(new Dictionary<string, object> { ["source"] = "newweapon", ["weapon"] = t.weapon, ["skill"] = t.skill, ["stage"] = t.stage, ["before"] = t.before, ["after"] = t.after, ["time"] = t.time, ["empowered"] = t.empowered });
    }
    void OnMelee(AdventureCombat.MeleeObservation m)
    {
        if (m.reason == "DAMAGE")
            damages.Add(new Dictionary<string, object> { ["source"] = "melee", ["attack"] = m.attack, ["before"] = m.before, ["after"] = m.after, ["time"] = Time.unscaledTime });
    }

    // ========================================================================
    // INPUT INJECTION (real InputSystem key down / up on the virtual keyboard)
    // ========================================================================
    void Inject(bool down, Key key)
    {
        var kb = virtKb ?? Keyboard.current;
        if (kb == null) { Log("no keyboard device to inject"); return; }
        InputSystem.QueueStateEvent(kb, down ? new KeyboardState(key) : new KeyboardState());
        keyEvents.Add(new Dictionary<string, object> { ["key"] = key.ToString(), ["pressed"] = down, ["frame"] = Time.frameCount, ["time"] = Time.unscaledTime });
        Log("inject " + key + " down=" + down);
    }

    void RecordCast(string label, bool attempted) { casts.Add(new Dictionary<string, object> { ["label"] = label, ["attempted"] = attempted, ["at"] = Time.unscaledTime }); }

    void FaceNearestEnemy()
    {
        if (session == null || session.enemies == null || hero == null) return;
        Transform best = null; float d = float.PositiveInfinity;
        foreach (var e in session.enemies)
        {
            if (e == null) continue;
            var t = e.transform; if (t == null) continue;
            float nd = Vector3.SqrMagnitude(t.position - hero.transform.position);
            if (nd < d) { d = nd; best = t; }
        }
        if (best != null) hero.transform.LookAt(new Vector3(best.position.x, hero.transform.position.y, best.position.z));
    }

    // ========================================================================
    // VERDICT + OUTPUT
    // ========================================================================
    void Fail(string reason)
    {
        if (failed) return;
        failed = true; failReason = reason; Log("FAIL: " + reason);
        WriteResult(false);
        quitting = true;
        Application.Quit(1);
    }

    void Finish()
    {
        bool descOk = true;
        string descNote = "";
        if (descContains != null) { bool has = (combat != null ? combat.SkillDescription : "").IndexOf(descContains, StringComparison.Ordinal) >= 0; if (!has) { descOk = false; descNote += " descContains missing"; } }
        if (descExcludes != null) { bool has = (combat != null ? combat.SkillDescription : "").IndexOf(descExcludes, StringComparison.Ordinal) >= 0; if (has) { descOk = false; descNote += " descExcludes present"; } }

        bool cooldownOk = true;
        string cooldownNote = "";
        float measured = -1f;
        if (expectedCooldown > 0f)
        {
            measured = (skillStarts.Count >= 2) ? (skillStarts[1] - skillStarts[0]) : -1f;
            if (!blockedDuringCooldown) { cooldownOk = false; cooldownNote = "re-cast during cooldown was not blocked"; }
            else if (measured < 0) { cooldownOk = false; cooldownNote = "second start never observed"; }
            else if (measured < expectedCooldown - 0.6f) { cooldownOk = false; cooldownNote = "second cast allowed too early measured=" + measured.ToString("0.00") + " expected=" + expectedCooldown; }
            else if (measured > expectedCooldown + 1.5f) { cooldownOk = false; cooldownNote = "second cast allowed too late measured=" + measured.ToString("0.00") + " expected=" + expectedCooldown; }
            else cooldownNote = "measured=" + measured.ToString("0.00") + " expected=" + expectedCooldown;
        }
        bool damaged = damages.Count > 0;
        bool zeroDamageOk = !expectZeroDamage || damages.Count == 0;
        if (expectZeroDamage && damages.Count > 0) Log("ZERO_DAMAGE_CHECK fail: " + damages.Count + " damage events observed (expected 0)");
        bool pass = !failed && skillCompletes.Count >= 1 && cooldownOk && descOk && zeroDamageOk;
        Log("VERDICT pass=" + pass + " descOk=" + descOk + descNote + " zeroDamageOk=" + zeroDamageOk + " cooldownOk=" + cooldownOk + " " + cooldownNote + " damaged=" + damaged + " starts=" + skillStarts.Count + " completes=" + skillCompletes.Count);
        WriteResult(pass);
        quitting = true;
        Application.Quit(pass ? 0 : 1);
    }

    void WriteResult(bool pass)
    {
        float measured = (skillStarts.Count >= 2) ? (skillStarts[1] - skillStarts[0]) : -1f;
        string desc = "";
        try { desc = combat != null ? combat.SkillDescription : ""; } catch { desc = ""; }
        var result = new Dictionary<string, object>
        {
            ["marker"] = PlayerAcceptanceHarness.MARKER,
            ["version"] = PlayerAcceptanceHarness.VERSION,
            ["scenarioId"] = scenarioId,
            ["runId"] = runId,
            ["processId"] = Process.GetCurrentProcess().Id,
            ["buildSha"] = buildSha,
            ["unityVersion"] = Application.unityVersion,
            ["weapon"] = weapon.ToString(),
            ["quality"] = quality.ToString(),
            ["affix"] = affix,
            ["slot"] = slot,
            ["chargeSeconds"] = chargeSeconds,
            ["expectedCooldown"] = expectedCooldown,
            ["descContains"] = descContains,
            ["descExcludes"] = descExcludes,
            ["expectZeroDamage"] = expectZeroDamage,
            ["entryAuthorized"] = entryAuthorized,
            ["pass"] = pass,
            ["failed"] = failed,
            ["failReason"] = failReason,
            ["startedAt"] = startedAt,
            ["finishedAt"] = Time.unscaledTime,
            ["cooldownMeasured"] = measured,
            ["cast1DownAt"] = cast1DownAt,
            ["cast2DownAt"] = cast2DownAt,
            ["blockedDuringCooldown"] = blockedDuringCooldown,
            ["skillStarts"] = skillStarts,
            ["skillCompletes"] = skillCompletes,
            ["damageCount"] = damages.Count,
            ["skillDescription"] = desc,
            ["observations"] = observations,
            ["damages"] = damages,
            ["keyEvents"] = keyEvents,
            ["casts"] = casts,
            ["log"] = logLines,
        };
        string json = MiniJson(result);
        string path = Path.Combine(dataRoot, "result.json");
        File.WriteAllText(path, json);
        File.WriteAllText(Path.Combine(dataRoot, "harness.log"), string.Join("\n", logLines));
        Log("wrote result.json pass=" + pass + " -> " + path);
    }

    void Enter(string p) { phase = p; phaseEnteredAt = Time.time; Log("phase -> " + p); }

    // ========================================================================
    // minimal JSON writer (Unity Mono lacks System.Text.Json)
    // ========================================================================
    static string MiniJson(object o)
    {
        var sb = new System.Text.StringBuilder();
        WriteValue(sb, o);
        return sb.ToString();
    }
    static void WriteValue(System.Text.StringBuilder sb, object o)
    {
        if (o == null) { sb.Append("null"); return; }
        if (o is string s) { sb.Append("\"").Append(s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n")).Append("\""); return; }
        if (o is bool b) { sb.Append(b ? "true" : "false"); return; }
        if (o is int || o is long || o is float || o is double)
        {
            if (o is float f) sb.Append(f.ToString("0.######", System.Globalization.CultureInfo.InvariantCulture));
            else if (o is double dbl) sb.Append(dbl.ToString("0.######", System.Globalization.CultureInfo.InvariantCulture));
            else sb.Append(o.ToString());
            return;
        }
        if (o is IDictionary<string, object> dict)
        {
            sb.Append("{"); bool first = true;
            foreach (var kv in dict) { if (!first) sb.Append(","); first = false; sb.Append("\"").Append(kv.Key).Append("\": "); WriteValue(sb, kv.Value); }
            sb.Append("}"); return;
        }
        if (o is System.Collections.IEnumerable en)
        {
            sb.Append("["); bool first = true;
            foreach (var item in en) { if (!first) sb.Append(","); first = false; WriteValue(sb, item); }
            sb.Append("]"); return;
        }
        sb.Append("null");
    }
}
#endif
