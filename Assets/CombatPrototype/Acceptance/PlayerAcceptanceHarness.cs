#if UX_ACCEPTANCE
// ============================================================================
// UX-PROGRESSION-03A REAL PLAYER ACCEPTANCE HARNESS  —  PH-R2
// ----------------------------------------------------------------------------
// Compiled ONLY into the Acceptance Build (gated by the UX_ACCEPTANCE scripting
// define). Shipping / Release builds define nothing here, so this entire file
// compiles out and the shipping package contains zero harness / test markers.
//
// PH-R2 extends PH-R1 with REAL combat-effect verification:
//   * Target preparation (PH-R2-02): locate a genuine enemy (prefer the wave-1
//     Elite, 140 HP so it survives multi-hit combos), record its identity
//     (entityId / archetype), initial / max HP, and the attacker's AttackPower /
//     Defense. Verify the target is alive, not disengaged, not invincible. The
//     harness NEVER modifies the target's HP directly and NEVER fakes events.
//   * Unified read-only damage forensics (PH-R2-03): subscribe to the target's
//     CombatHealth.Observed (a product event that fires for EVERY real hit type
//     — melee / projectile / AOE / scythe / twin) and emit two artifacts:
//       - target-events.jsonl : every health observation on the target
//       - damage-events.jsonl : the unified forensic record per hit
//     The record carries runId / skillId / targetId / attackId / hitId / hitTime
//     / targetHealthBefore / targetHealthAfter / actualDamage / expectedDamage
//     / attackerPosition / targetPosition / hitPosition / skillPhase.
//     expectedDamage is derived from hero.AttackPower x the frozen per-hit
//     fraction (read from WeaponSkillCatalog for legacy skills, or the frozen
//     new-weapon motor table) x charge scale x affix multipliers. This NEVER
//     touches the real damage settlement path.
//   * T3 scenario modes (PH-R2-06 twin counter, PH-R2-07 soul pull): a genuine
//     enemy attack rejected by the hero's dodge i-frames -> actual-evaded-attack
//     -> within 0.85s a real F (slot 1) counter that must empower (1.8x) and
//     consume the evade exactly once; and a genuine scythe pull that must emit
//     pull-start, move the target toward the hero, and deal ZERO damage.
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
    public const string MARKER = "UX_ACCEPTANCE_HARNESS_v1"; // unchanged: shipping-exclusion grep identity
    public const int VERSION = 3;                            // PH-R2-R1-FIX (single settle clock)

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
    string buildId = "unknown";
    string expectedExeSha = "unknown";
    string expectedDllSha = "unknown";
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
    // PH-R2: scenario mode + verification knobs
    string mode = "damage";            // "damage" | "twin_counter" | "soul_pull"
    bool verifyDamage = false;          // require real HP delta to match the frozen model
    float damageTolerance = 0.06f;      // relative tolerance for per-hit / total match
    string targetArchetype = "Elite";   // preferred target archetype for prep
    float pullReachMeters = 4.5f;       // PH-R2-07 geometry expectation (4.5 * area)

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

    // PH-R2 target state
    CombatEnemy target = null;
    string targetEntityId = "";
    string targetArchetypeObserved = "";
    float targetInitialHP = -1f;
    float targetMaxHP = -1f;
    float attackerAttackPower = -1f;
    float attackerDefense = -1f;
    bool targetPrepared = false;
    Vector3 targetPosBefore = Vector3.zero;
    Vector3 targetPosAfter = Vector3.zero;

    // ---- recorded evidence --------------------------------------------------
    List<string> logLines = new List<string>();
    string logPath = null;
    List<Dictionary<string, object>> observations = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> damages = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> keyEvents = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> casts = new List<Dictionary<string, object>>();
    List<float> skillStarts = new List<float>();
    List<float> skillCompletes = new List<float>();

    // PH-R2 forensic artifacts
    List<Dictionary<string, object>> targetEvents = new List<Dictionary<string, object>>();
    List<Dictionary<string, object>> damageForensics = new List<Dictionary<string, object>>();
    int attackCounter = 0;
    int hitCounter = 0;
    float cast1StartAt = -1f;
    // PH-R2-R1-FIX-01: the damage-settle window MUST be measured on ONE clock.
    //  * lastDamageUnscaledTime : Time.unscaledTime  -> the ONLY clock used by
    //    any settle/close decision (same clock as phaseEnteredAt / skillStarts).
    //  * lastDamageActiveTime   : the PRODUCT'S raw HealthObservation.activeTime
    //    (CombatHealth sets it from Time.timeAsDouble). Kept for forensics only.
    //    It is NEVER subtracted from Time.unscaledTime (that was defect F-1b).
    float lastDamageUnscaledTime = -1f;
    double lastDamageActiveTime = -1d;
    float damageWindowStart = -1f;          // unscaledTime
    float damageWindowClosedAt = -1f;       // unscaledTime, when forensics froze
    string damageWindowCloseReason = "";    // "quiet" | "hardcap" | ""
    int expectedHits = 0;
    float expectedPerHit = 0f;
    float expectedTotal = 0f;
    bool uniformHits = true;
    bool damageWindowClosed = false;
    bool damageVerdict = true;
    string damageNote = "";

    // PH-R2-R1-01: Player-computed assembly identity. These are filled by the
    // Player itself from the ACTUALLY LOADED managed assembly, not from args.
    string loadedAssemblyPath = "";
    string loadedAssemblySha256 = "";
    string loadedAssemblyName = "";
    bool identityVerified = false;
    string identityNote = "";
    // PH-R2-R1-02: second-counter strictness -> INCOMPLETE when no contact.
    string incompleteReason = "";
    // PH-R2-R1-03: per-hit expected ratios for non-uniform skills (staff.field).
    float[] expectedHitRatios = null;

    // PH-R2 T3 state
    float cast1DownAt = -1f, cast2DownAt = -1f, probeDownAt = -1f;
    bool blockedDuringCooldown = false;
    Keyboard virtKb = null;
    bool useAttackPhaseProbe = false;
    long attackIdBaseline = 0;
    // twin counter
    bool evadeSeen = false;
    float evadeSeenAt = -1f;
    float counterDownAt = -1f;
    bool counterCastAttempted = false;
    bool counterReleased = false;
    bool counterRepositioned = false;
    bool counterEmpowered = false;
    bool counterContactSeen = false;
    float counterDamage = 0f;
    bool secondCounterAttempted = false;
    bool secondCounterEmpowered = false;
    bool secondCounterContactSeen = false;
    // soul pull
    float pullDownAt = -1f;
    bool pullKeyReleased = false;
    float pullPeakDisplacement = 0f;
    float dodgeKeyDownAt = -100f;
    float dodgeDownAt = -100f;
    bool dodgeKeyHeld = false;
    bool dodgeRollObserved = false;
    bool pullStartSeen = false;
    bool pullObstructedSeen = false;
    bool controlImmuneSeen = false;
    bool pullCastAttempted = false;

    // PH-R2-R1-FIX-01: ONE auditable predicate owns the settle decision, so the
    // same rule is used by closeDamageWindow / cooldownAllow and by the runtime
    // time-base probe. Its signature makes the two-clock bug IMPOSSIBLE to
    // reintroduce: there is no parameter that accepts a product activeTime.
    internal const float DamageQuietPeriodSeconds = 1.2f;

    internal static bool DamageWindowShouldClose(float nowUnscaled, float lastDamageUnscaled,
                                                float windowStartUnscaled, float hardCapSeconds)
    {
        if (windowStartUnscaled < 0f) return true;                 // nothing armed
        bool quiet = lastDamageUnscaled >= 0f && (nowUnscaled - lastDamageUnscaled) > DamageQuietPeriodSeconds;
        bool capped = (nowUnscaled - windowStartUnscaled) > hardCapSeconds;
        return quiet || capped;
    }

    internal static string DamageWindowCloseReason(float nowUnscaled, float lastDamageUnscaled,
                                                   float windowStartUnscaled, float hardCapSeconds)
    {
        if (windowStartUnscaled < 0f) return "empty";
        if (lastDamageUnscaled >= 0f && (nowUnscaled - lastDamageUnscaled) > DamageQuietPeriodSeconds) return "quiet";
        if ((nowUnscaled - windowStartUnscaled) > hardCapSeconds) return "hardcap";
        return "";
    }

    // ALL harness-internal timing uses UNSCALED time (PH-R2-01): GameEntry holds
    // Time.timeScale=0 until the save system boots, which would freeze
    // Time.time-based timeouts and silently hang the run. Enter() also records
    // unscaled time (PH-R1 mixed Time.time here — fixed in R2).
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
        ResolveLoadedAssemblyIdentity(); // PH-R2-R1-01: Player hashes what it REALLY loaded
        phase = "entry"; phaseEnteredAt = Time.unscaledTime;
        Log("harness v" + PlayerAcceptanceHarness.VERSION + " scenario=" + scenarioId + " run=" + runId + " weapon=" + weapon + " slot=" + slot + " affix=" + affix + " charge=" + chargeSeconds + " cd=" + expectedCooldown + " mode=" + mode + " verifyDamage=" + verifyDamage);
        // PH-R2-R1-FIX-01: a dedicated runtime probe for the settle clock. It
        // needs neither the scene nor the save system, so it runs immediately.
        if (mode == "timebase") { Log("mode=timebase -> runtime clock probe"); Enter("timebase_probe"); }
    }

    // PH-R2-R1-01 §3.2: identity forensics computed INSIDE the Player from the
    // assembly that actually contains this code. Assembly.GetExecutingAssembly()
    // returns the managed assembly (Assembly-CSharp.dll) the harness was compiled
    // into; .Location is the real on-disk path loaded by the Player. We hash that
    // file and compare it with the driver-supplied EXPECTATION. We NEVER copy the
    // command-line SHA into the result and claim success. If the runtime cannot
    // expose a readable assembly path, identityVerified stays false and the run
    // FAILs explicitly (no silent fallback to args).
    void ResolveLoadedAssemblyIdentity()
    {
        try
        {
            var asm = System.Reflection.Assembly.GetExecutingAssembly();
            loadedAssemblyName = asm != null ? asm.GetName().Name : "";
            string loc = asm != null ? asm.Location : "";
            loadedAssemblyPath = loc ?? "";
            string resolution = "Assembly.GetExecutingAssembly().Location";
            // Some Unity runtimes report an empty Location. Fall back to the
            // Player's OWN data directory (Application.dataPath), which is where
            // the managed assembly is actually loaded from. This is still a real
            // on-disk file resolved by the Player, NOT a command-line SHA. If
            // neither yields a readable file we FAIL explicitly.
            if (string.IsNullOrEmpty(loadedAssemblyPath) || !File.Exists(loadedAssemblyPath))
            {
                string candidate = Path.Combine(Application.dataPath, "Managed", "Assembly-CSharp.dll");
                if (File.Exists(candidate)) { loadedAssemblyPath = candidate; resolution = "Application.dataPath/Managed/Assembly-CSharp.dll"; }
            }
            if (string.IsNullOrEmpty(loadedAssemblyPath) || !File.Exists(loadedAssemblyPath))
            {
                identityVerified = false;
                identityNote = "Player cannot resolve a readable loaded assembly path (Location='" + (loc ?? "") + "'); refusing to fall back to command-line SHA";
                Log("ASSEMBLY IDENTITY FAIL: " + identityNote);
                return;
            }
            using (var s = System.Security.Cryptography.SHA256.Create())
            using (var f = File.OpenRead(loadedAssemblyPath))
            {
                byte[] hash = s.ComputeHash(f);
                var sb = new System.Text.StringBuilder();
                foreach (byte b in hash) sb.Append(b.ToString("x2"));
                loadedAssemblySha256 = sb.ToString();
            }
            bool expectedValid = !string.IsNullOrEmpty(expectedDllSha) && expectedDllSha.Length == 64 && expectedDllSha != "unknown";
            identityVerified = expectedValid && string.Equals(loadedAssemblySha256, expectedDllSha, StringComparison.OrdinalIgnoreCase);
            identityNote = identityVerified
                ? "Player-computed loaded assembly SHA256 matches expectedDllSha"
                : ("Player-computed loaded assembly SHA256 mismatch or missing expectation (computed=" + loadedAssemblySha256 + ", expected=" + expectedDllSha + ")");
            Log("ASSEMBLY IDENTITY name=" + loadedAssemblyName + " resolution=" + resolution +
                " path=" + loadedAssemblyPath + " sha256=" + loadedAssemblySha256 +
                " expected=" + expectedDllSha + " verified=" + identityVerified);
        }
        catch (Exception e)
        {
            identityVerified = false;
            identityNote = "Player assembly identity resolution threw: " + e.GetType().Name + ": " + e.Message;
            Log("ASSEMBLY IDENTITY FAIL: " + identityNote);
        }
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
                // PH-R2-R1-01: build identity passed by the driver is EXPECTATION
                // only. The Player MUST independently hash the assembly it has
                // actually loaded; identityVerified is computed here, never
                // copied from the command line.
                case "--build-id": buildId = SafeArg(args, ++i, buildId); break;
                case "--expected-exe-sha": expectedExeSha = SafeArg(args, ++i, expectedExeSha); break;
                case "--expected-dll-sha": expectedDllSha = SafeArg(args, ++i, expectedDllSha); break;
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
                // PH-R2 new knobs
                case "--mode": mode = SafeArg(args, ++i, "damage"); break;
                case "--verify-damage": verifyDamage = SafeArg(args, ++i, "false") == "true"; break;
                case "--damage-tolerance": damageTolerance = float.Parse(SafeArg(args, ++i, "0.06"), System.Globalization.CultureInfo.InvariantCulture); break;
                case "--target-archetype": targetArchetype = SafeArg(args, ++i, "Elite"); break;
            }
        }
        if (string.IsNullOrEmpty(dataRoot))
        {
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
            try { ok = gameEntry.Continue(); }
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
        try { GameEntry.DirectReady(); } catch (Exception e) { Log("DirectReady warn: " + e.Message); }
        Enter("locate");
    }

    // ---- combat scenario ----------------------------------------------------
    void Step()
    {
        switch (phase)
        {
            // PH-R2-R1-FIX-01: clock probe, runs before any scene dependency.
            case "timebase_probe":
                StepTimebaseProbe();
                break;

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
                if (expanded != null && !expanded.Select(slot)) Log("rearm: Select(slot=" + slot + ") returned false");
                PlayerInput.Focus(true);
                useAttackPhaseProbe = slot == 0 && (int)weapon < 4 && combat != null;
                if (useAttackPhaseProbe) { attackIdBaseline = combat.LastAttackId; Log("legacy slot-0 probe armed, baseline attackId=" + attackIdBaseline); }
                Enter("target_prepare");
                break;

            // PH-R2-02: locate a genuine enemy target and verify identity / freshness
            case "target_prepare":
                if (Time.unscaledTime - phaseEnteredAt > 25f) { Fail("target_prepare timeout: no valid enemy target found"); return; }
                if (!PrepareTarget()) return; // sets target + records identity; fails internally if preconditions unmet
                attackerAttackPower = hero.AttackPower;
                attackerDefense = hero.Defense;
                SubscribeTarget();
                targetPrepared = true;
                Log("target prepared: id=" + targetEntityId + " archetype=" + targetArchetypeObserved + " initialHP=" + targetInitialHP + " maxHP=" + targetMaxHP + " attackerAP=" + attackerAttackPower + " attackerDef=" + attackerDefense);
                ComputeExpectedModel();
                Enter("warmup");
                break;

            case "warmup":
                // give the field a moment to settle; then (damage mode) place the
                // genuine target adjacent to the stationary hero so the selected
                // skill's reach is satisfied. The enemy, its HP and all damage events
                // stay real.
                if (Time.unscaledTime - phaseEnteredAt > 1.5f)
                {
                    if (mode == "twin_counter") { Enter("counter_loop"); break; }
                    if (mode == "soul_pull") { Enter("pull_wait"); break; }
                    // damage mode: place the genuine target 1.0m from the hero
                    RepositionTargetAdjacentToHero(1.0f);
                    Log("placed genuine target adjacent to hero (real enemy/HP/damage); proceeding to cast1");
                    Enter("cast1");
                }
                break;

            case "cast1":
                ProbeLegacyCast();
                FaceTarget();
                RepositionTargetAdjacentToHero(1.0f); // keep the genuine target in reach each frame
                if (cast1DownAt < 0f)
                {
                    PlayerInput.Focus(true); Inject(true, Key.F); RecordCast("cast1", true); cast1DownAt = Time.unscaledTime; Log("F down (cast1)");
                }
                if (cast1DownAt >= 0f && skillStarts.Count < 1 && Time.unscaledTime - cast1DownAt > 3f) { Inject(false, Key.F); Fail("cast1 produced no skill START (Selected=" + CurrentSelected() + " Focused=" + PlayerInput.Focused + " Suspended=" + PlayerInput.Suspended + " UIBlocked=" + PlayerInput.UIBlocked + " Ready=" + ReadyProbe() + ")"); return; }
                if (cast1DownAt >= 0f && skillStarts.Count >= 1)
                {
                    cast1StartAt = damageWindowStart = skillStarts[0];
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
                RepositionTargetAdjacentToHero(1.0f); // keep the genuine target in reach while the combo resolves
                if (skillCompletes.Count >= 1) { Log("cast1 complete"); Enter(expectedCooldown > 0f ? "cooldownBlock" : "closeDamageWindow"); }
                else if (Time.unscaledTime - cast1DownAt > 14f) Fail("cast1 never completed");
                break;

            case "closeDamageWindow":
                // PH-R2-03: keep the window open until damage settles (covers late
                // impact-field pulses for staff.field), then finalize forensics.
                if (damageWindowStart < 0f) { Enter("done"); break; }
                // PH-R2-R1-FIX-01: settle decision on the SINGLE unscaled clock.
                if (DamageWindowShouldClose(Time.unscaledTime, lastDamageUnscaledTime, damageWindowStart, 4.5f))
                {
                    damageWindowCloseReason = DamageWindowCloseReason(Time.unscaledTime, lastDamageUnscaledTime, damageWindowStart, 4.5f);
                    damageWindowClosedAt = Time.unscaledTime;
                    damageWindowClosed = true;
                    Log("damage window closed reason=" + damageWindowCloseReason + " lastDamageUnscaled=" + lastDamageUnscaledTime.ToString("0.000") + " lastDamageActive=" + lastDamageActiveTime.ToString("0.000"));
                    FinalizeDamageForensics();
                    Enter("done");
                }
                break;

            case "cooldownBlock":
                if (skillStarts.Count < 1) { Fail("cooldownBlock reached without a first start"); return; }
                if (probeDownAt < 0f) { PlayerInput.Focus(true); Inject(true, Key.F); RecordCast("probeBlocked", true); probeDownAt = Time.unscaledTime; return; }
                if (Time.unscaledTime - probeDownAt < 0.7f) return;
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
                RepositionTargetAdjacentToHero(1.0f); // keep the genuine target in reach for the second cast
                if (cast2DownAt < 0f)
                {
                    FaceTarget();
                    PlayerInput.Focus(true);
                    Inject(true, Key.F); RecordCast("cast2", true); cast2DownAt = Time.unscaledTime; Log("F down (cast2, after cooldown)");
                }
                if (cast2DownAt >= 0f && skillStarts.Count < 2 && Time.unscaledTime - cast2DownAt > 3f) { Inject(false, Key.F); Fail("cast2 after cooldown did not start (Selected=" + CurrentSelected() + ")"); return; }
                if (cast2DownAt >= 0f && skillStarts.Count >= 2)
                {
                    Inject(false, Key.F); Log("F up (cast2)");
                    // allow any late damage from cast2 to settle, then close window
                    if (DamageWindowShouldClose(Time.unscaledTime, lastDamageUnscaledTime, damageWindowStart, 6f))
                    {
                        damageWindowCloseReason = DamageWindowCloseReason(Time.unscaledTime, lastDamageUnscaledTime, damageWindowStart, 6f);
                        damageWindowClosedAt = Time.unscaledTime;
                        damageWindowClosed = true;
                        Log("damage window closed reason=" + damageWindowCloseReason + " (after cooldown recast) lastDamageUnscaled=" + lastDamageUnscaledTime.ToString("0.000"));
                        FinalizeDamageForensics();
                        Enter("done");
                    }
                }
                break;

            // ---- PH-R2-06 twin counter ----
            case "counter_loop":
                if (Time.unscaledTime - phaseEnteredAt > 22f) { Fail("counter_loop timeout: never observed a real attack rejected by dodge i-frames (actual-evaded-attack)"); return; }
                // keep the genuine enemy adjacent to the stationary hero so it
                // telegraphs and releases a real melee attack the hero can dodge.
                RepositionTargetAdjacentToHero(1.7f);
                FaceTarget();
                TryDodgeForEvade();
                if (evadeSeen) { Log("evade observed at " + evadeSeenAt.ToString("0.000") + "; proceeding to counter cast"); Enter("counter_cast"); }
                break;

            case "counter_cast":
                // The dodge flings the hero ~4.2m away. We must NOT reposition the
                // hero (CampFacilities clamps it back to camp bounds); instead we
                // place the GENUINE target adjacent to wherever the hero landed, so
                // the counter's ~1.8m reach can connect within the 0.85s empower
                // window. The dodge, evade, empower and damage settlement all remain
                // REAL product paths; no target HP is modified and no event faked.
                if (hero != null && hero.Dodge != null && hero.Dodge.IsRolling) break; // wait for the roll to finish
                if (!counterRepositioned && target != null && hero != null)
                {
                    RepositionTargetAdjacentToHero(1.5f);
                    counterRepositioned = true;
                    Log("placed genuine target adjacent to (post-dodge) hero for counter contact (dist=" + Vector3.Distance(target.transform.position, hero.transform.position).ToString("0.##") + "m)");
                }
                if (!counterCastAttempted)
                {
                    counterCastAttempted = true;
                    PlayerInput.Focus(true);
                    if (expanded != null && !expanded.Select(1)) Log("counter: Select(1) returned false");
                    Inject(true, Key.F); RecordCast("counter", true); counterDownAt = Time.unscaledTime; Log("F down (counter, slot1)");
                }
                if (!counterContactSeen)
                {
                    if (Time.unscaledTime - counterDownAt > 6f) Fail("counter produced no contact within 6s");
                    break;
                }
                // first (empowered) counter contact observed: release the key, then
                // attempt a SECOND counter only after the skill cooldown (TwinBlade
                // counter cd ~8s) clears, to positively verify consume-once. If the
                // second cast is still blocked, the core is already verified.
                if (!counterReleased) { Inject(false, Key.F); counterReleased = true; Log("F up (counter) empowered=" + counterEmpowered + " damage=" + counterDamage.ToString("0.##")); }
                if (!secondCounterAttempted)
                {
                    if (Time.unscaledTime - counterDownAt > 9.5f && (newWeapons == null || !newWeapons.Busy))
                    {
                        secondCounterAttempted = true;
                        PlayerInput.Focus(true);
                        Inject(true, Key.F); RecordCast("counter2", true); counterDownAt = Time.unscaledTime;
                        Log("second counter attempt after cooldown (no fresh evade) to verify consume-once");
                    }
                }
                else if (secondCounterContactSeen)
                {
                    Inject(false, Key.F); Log("F up (counter2) empowered=" + secondCounterEmpowered);
                    Enter("done");
                }
                else if (Time.unscaledTime - counterDownAt > 6f)
                {
                    Log("second counter did not contact within window (cooldown/again); core empowered-counter verified");
                    Enter("done");
                }
                break;

            // ---- PH-R2-07 soul pull ----
            case "pull_wait":
                if (Time.unscaledTime - phaseEnteredAt > 12f) { Fail("pull_wait timeout: target not in pull range"); return; }
                // place the genuine enemy within the scythe pull reach (4.5m radius),
                // in front of the hero with LOS, so the pull engages and visibly
                // displaces it. The hero stays put (camp-clamp safe).
                RepositionTargetAdjacentToHero(3.0f);
                FaceTarget();
                if (TargetInReach(pullReachMeters)) { targetPosBefore = TargetPos(); Enter("pull_cast"); }
                break;

            case "pull_cast":
                if (!pullCastAttempted)
                {
                    pullCastAttempted = true;
                    targetPosBefore = TargetPos();   // isolate the pull displacement from prior enemy drift
                    PlayerInput.Focus(true);
                    if (expanded != null && !expanded.Select(1)) Log("pull: Select(1) returned false");
                    Inject(true, Key.F); RecordCast("pull", true); pullDownAt = Time.unscaledTime; Log("F down (pull, slot1)");
                }
                targetPosAfter = TargetPos();
                float disp = Vector3.Distance(targetPosBefore, targetPosAfter);
                if (disp > pullPeakDisplacement) pullPeakDisplacement = disp;
                if (pullStartSeen || controlImmuneSeen || pullObstructedSeen)
                {
                    if (!pullKeyReleased) { Inject(false, Key.F); pullKeyReleased = true; Log("F up (pull)"); }
                    // Finish() requires skillCompletes>=1. Entering "done" the
                    // instant pull-start arrives drops the REAL complete trace
                    // (it lands ~1s later), so wait for it. Displacement is
                    // measured by PEAK, not the last frame, so a returning enemy
                    // cannot erase the observed movement.
                    if (skillCompletes.Count >= 1 || Time.unscaledTime - pullDownAt > 4.5f)
                    {
                        Log("pull settled: completes=" + skillCompletes.Count + " peakDisplacement=" + pullPeakDisplacement.ToString("0.##") + "m");
                        Enter("done");
                    }
                }
                else if (Time.unscaledTime - pullDownAt > 6f) Fail("pull produced no pull-start / control-immune / pull-obstructed within 6s");
                break;

            case "done":
                Finish();
                break;
        }
    }

    bool ReadyProbe() { try { return combat != null && hero != null && hero.Health != null && !hero.Health.Dead && PlayerInput.Focused; } catch { return false; } }

    // Real-cast evidence for legacy slot-0 basic skills via public combat state:
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

    // PH-R2-02: choose a genuine enemy target.
    bool PrepareTarget()
    {
        if (session == null || session.enemies == null) { Log("PrepareTarget: no enemy registry"); return false; }
        if (target != null)
        {
            // re-validate the previously chosen target each frame until accepted
            if (!ValidateTarget(target)) return false;
            return true;
        }
        // prefer the requested archetype, else any alive, engaged enemy
        CombatEnemy best = null;
        foreach (var e in session.enemies)
        {
            if (e == null) continue;
            bool match = string.Equals(e.archetype.ToString(), targetArchetype, StringComparison.OrdinalIgnoreCase);
            if (match && ValidateTarget(e)) { best = e; break; }
        }
        if (best == null)
        {
            foreach (var e in session.enemies)
            {
                if (e == null) continue;
                if (ValidateTarget(e)) { best = e; break; }
            }
        }
        if (best == null) { if (Time.unscaledTime - phaseEnteredAt > 8f) Fail("no valid enemy target (all dead / disengaged / invincible)"); return false; }
        target = best;
        targetEntityId = best.entityId ?? "";
        targetArchetypeObserved = best.archetype.ToString();
        targetInitialHP = best.Health != null ? best.Health.Current : -1f;
        targetMaxHP = best.Health != null ? best.Health.maxHealth : -1f;
        // PH-R2: neutralize the genuine enemy's EncounterGuard. The guard snaps the
        // enemy back toward its home spawn whenever it strays >24m, which would undo
        // any test-only repositioning. Disabling it lets the enemy stay where the
        // harness places it; every other combat behavior (chase / telegraph / damage
        // settlement) is untouched. This is harness instrumentation only — no spawn,
        // HP, or event is faked.
        var guard = target.GetComponent<EncounterGuard>();
        if (guard != null) { guard.enabled = false; Log("disabled target EncounterGuard (home=" + Vec(guard.home) + ")"); }
        return true;
    }

    bool ValidateTarget(CombatEnemy e)
    {
        if (e == null || e.Health == null) return false;
        if (e.Health.Dead || e.Health.Current <= 0) return false;            // not dead
        if (e.State == EnemyCombatState.Dead || e.State == EnemyCombatState.Returning) return false; // not disengaged / despawned
        // NOTE: we do NOT require e.target == hero here. Wave-1 enemies may not
        // have assigned their attack target yet at target-prep time, but as live
        // members of session.enemies they are genuine, valid combatants. The
        // harness only ever damages this enemy via real product settlement paths.
        return true;
    }

    void SubscribeTarget()
    {
        if (target != null && target.Health != null)
            target.Health.Observed += OnTargetHealth;
    }

    void OnTargetHealth(HealthObservation o)
    {
        // PH-R2-R1-FIX-01: record BOTH clocks explicitly and by name. The product
        // clock (activeTime = Time.timeAsDouble) is kept raw for forensics; the
        // harness clock (unscaledTime) is what every settle decision uses.
        float uNow = Time.unscaledTime;
        var rec = new Dictionary<string, object>
        {
            ["kind"] = o.kind.ToString(),
            ["before"] = o.before,
            ["after"] = o.after,
            ["applied"] = o.applied,
            ["activeTime"] = o.activeTime,
            ["activeTimeClock"] = "Time.timeAsDouble (CombatHealth.activeTime)",
            ["unscaledTime"] = uNow,
            ["unscaledTimeClock"] = "Time.unscaledTime (harness)",
            ["clockOffsetUnscaledMinusActive"] = uNow - o.activeTime,
            ["frame"] = o.frame,
            ["deathTransition"] = o.deathTransition,
            ["heroPos"] = Vec(hero != null ? hero.transform.position : Vector3.zero),
            ["targetPos"] = Vec(target != null ? target.transform.position : Vector3.zero),
            ["targetId"] = targetEntityId,
        };
        targetEvents.Add(rec);
        if (o.kind == HealthObservationKind.Damage && o.applied > 0)
        {
            lastDamageActiveTime = o.activeTime;     // product clock, forensics only
            lastDamageUnscaledTime = uNow;           // harness clock, decisions only
            RecordDamageHit(o);
        }
    }

    // PH-R2-03: append a unified forensic hit record, correlating the damage to
    // the currently active cast via the damage window.
    void RecordDamageHit(HealthObservation o)
    {
        // The forensic window closes when FinalizeDamageForensics() runs. Any
        // later hit (e.g. the cooldown re-cast) must NOT be appended: the model
        // describes ONE complete cast, so a second cast would double the count.
        if (damageWindowClosed) return;
        // PH-R2-R1-FIX-01: window START is also an unscaled-clock value. Mixing
        // the product activeTime in here was the same two-clock defect.
        if (damageWindowStart < 0f) damageWindowStart = Time.unscaledTime;
        attackCounter = Math.Max(attackCounter, skillStarts.Count > 0 ? 1 : attackCounter);
        hitCounter++;
        // PH-R2-R1-03: for NON-UNIFORM skills (staff.field) the expected damage
        // is derived PER HIT from the frozen ratio array, indexed by hit sequence,
        // never from a single uniform perHit multiplier.
        float ratio = expectedPerHit;
        if (expectedHitRatios != null)
            ratio = expectedHitRatios[Math.Min(hitCounter - 1, expectedHitRatios.Length - 1)];
        float expected = ratio * attackerAttackPower;
        if (o.before <= 0) expected = 0; // overkill guard
        var rec = new Dictionary<string, object>
        {
            ["runId"] = runId,
            ["skillId"] = scenarioId,
            ["targetId"] = targetEntityId,
            ["attackId"] = attackCounter,
            ["hitId"] = hitCounter,
            ["hitTime"] = o.activeTime,
            ["hitActiveTime"] = o.activeTime,
            ["hitActiveTimeClock"] = "Time.timeAsDouble (CombatHealth.activeTime)",
            ["hitUnscaledTime"] = Time.unscaledTime,
            ["hitUnscaledTimeClock"] = "Time.unscaledTime (harness)",
            ["targetHealthBefore"] = o.before,
            ["targetHealthAfter"] = o.after,
            ["actualDamage"] = o.applied,
            ["expectedDamage"] = expected,
            ["attackerPosition"] = Vec(hero != null ? hero.transform.position : Vector3.zero),
            ["targetPosition"] = Vec(target != null ? target.transform.position : Vector3.zero),
            ["hitPosition"] = Vec(target != null ? target.transform.position : Vector3.zero),
            ["skillPhase"] = mode == "twin_counter" ? "counter" : (mode == "soul_pull" ? "pull" : "cast1"),
        };
        damageForensics.Add(rec);
        Log("FORENSIC hit#" + hitCounter + " before=" + o.before.ToString("0.#") + " after=" + o.after.ToString("0.#") + " actual=" + o.applied.ToString("0.##") + " expected=" + expected.ToString("0.##"));
    }

    // PH-R2-03: frozen per-hit model (auditable). Legacy skills read their power
    // from WeaponSkillCatalog where possible; new weapons use the frozen motor
    // table. Echo (affix 2) is a RADIUS effect and never changes damage, so it is
    // intentionally NOT applied here. 聚能 (affix 5) applies x1.25 to skill hits.
    void ComputeExpectedModel()
    {
        if (!verifyDamage) return;
        float ap = hero != null ? hero.AttackPower : 25f;
        bool focus = (affix == 5);
        float affixMul = focus ? 1.25f : 1f;
        float chargeScale = (chargeSeconds > 0f) ? 1.85f : 1f; // full charge reached at release
        string key = weapon.ToString() + "|" + slot;
        expectedHits = 0; expectedPerHit = 0f; expectedTotal = 0f; uniformHits = true;
        expectedHitRatios = null; // PH-R2-R1-03: reset per-run non-uniform model

        // legacy expansion / slot-0 AOE -> read catalog power where defined
        var legacyMap = new Dictionary<string, float>
        {
            {"Sword|1",0.65f},{"Sword|2",0.85f},{"Spear|1",1.20f},{"Spear|2",0.85f},
            {"Staff|1",0.65f},{"Staff|2",0.70f},{"Bow|1",0.62f},{"Bow|2",1.35f},{"Sword|0",2.00f},
        };
        var legacyHits = new Dictionary<string, int>
        {
            {"Sword|1",3},{"Sword|2",3},{"Spear|1",1},{"Spear|2",2},
            {"Staff|1",4},{"Staff|2",3},{"Bow|1",3},{"Bow|2",1},{"Sword|0",1},
        };
        var newMap = new Dictionary<string, float>
        {
            {"Greatsword|0",1.70f},{"Greatsword|1",1.30f},{"TwinBlades|0",0.40f},
            {"TwinBlades|1",0.65f},{"Scythe|0",0.45f},{"Scythe|1",0.0f},
        };
        var newHits = new Dictionary<string, int>
        {
            {"Greatsword|0",1},{"Greatsword|1",1},{"TwinBlades|0",6},
            {"TwinBlades|1",1},{"Scythe|0",3},{"Scythe|1",0},
        };

        if (legacyMap.ContainsKey(key))
        {
            expectedPerHit = legacyMap[key] * chargeScale * affixMul;
            expectedHits = legacyHits[key];
            if (key == "Staff|1")
            {
                // PH-R2-R1-03: staff.field is 1 impact hit at 65% followed by
                // three 40% field pulses. Ratios are looked up per hitIndex so
                // the first hit is never confused with the later pulses.
                uniformHits = false;
                expectedHitRatios = new float[] { 0.65f, 0.40f, 0.40f, 0.40f };
                float sum = 0f;
                for (int k = 0; k < expectedHitRatios.Length; k++)
                    expectedHitRatios[k] = expectedHitRatios[k] * chargeScale * affixMul;
                foreach (float r in expectedHitRatios) sum += r;
                expectedTotal = sum * ap;
                expectedPerHit = expectedHitRatios[0];
            }
            else expectedTotal = expectedPerHit * expectedHits * ap;
        }
        else if (newMap.ContainsKey(key))
        {
            expectedPerHit = newMap[key] * affixMul; // new weapons: phase>=10 -> skill=true -> focus applies
            expectedHits = newHits[key];
            expectedTotal = expectedPerHit * expectedHits * ap;
        }
        else
        {
            Log("ComputeExpectedModel: unknown weapon|slot " + key + "; forensics will report actual only");
        }
        Log("EXPECTED model key=" + key + " ap=" + ap + " affixMul=" + affixMul + " chargeScale=" + chargeScale + " perHit=" + expectedPerHit.ToString("0.###") + " hits=" + expectedHits + " total=" + expectedTotal.ToString("0.##") + " uniform=" + uniformHits);
    }

    void FinalizeDamageForensics()
    {
        if (!verifyDamage) return;
        // Values are boxed as float by RecordDamageHit / ComputeExpectedModel;
        // unboxing a boxed float via (double) throws InvalidCastException, so use
        // Convert.ToSingle which is type-agnostic for the boxed numeric value.
        float actualTotal = damageForensics.Sum(r => Convert.ToSingle(r["actualDamage"]));
        int actualHits = damageForensics.Count;
        damageVerdict = true; damageNote = "";
        if (expectedHits == 0 && actualHits == 0)
        {
            // zero-damage skill (e.g. scythe pull) — handled by its own verdict
            damageNote = "no damage expected/observed (zero-damage skill)";
        }
        else if (expectedHits == 0 && actualHits > 0)
        {
            damageVerdict = false; damageNote = "expected 0 hits but observed " + actualHits;
        }
        else
        {
            // count check
            if (actualHits != expectedHits)
            {
                // staff.field late pulses may still be arriving; tolerate if within window
                damageVerdict = false;
                damageNote += " hitCount mismatch expected=" + expectedHits + " actual=" + actualHits;
            }
            // per-hit / total check
            float tol = Math.Max(1.0f, expectedTotal * damageTolerance);
            if (uniformHits)
            {
                foreach (var r in damageForensics)
                {
                    float diff = Math.Abs(Convert.ToSingle(r["actualDamage"]) - Convert.ToSingle(r["expectedDamage"]));
                    if (diff > tol) { damageVerdict = false; damageNote += " perHit off by " + diff.ToString("0.##"); break; }
                }
            }
            else
            {
                // PH-R2-R1-03 non-uniform (staff.field): check EACH hit against
                // its own stage ratio AND the total. The aggregate alone must not
                // mask a first-hit/late-pulse mix-up.
                for (int k = 0; k < damageForensics.Count; k++)
                {
                    var r = damageForensics[k];
                    float want = expectedHitRatios != null
                        ? expectedHitRatios[Math.Min(k, expectedHitRatios.Length - 1)] * attackerAttackPower
                        : Convert.ToSingle(r["expectedDamage"]);
                    float got = Convert.ToSingle(r["actualDamage"]);
                    float recorded = Convert.ToSingle(r["expectedDamage"]);
                    if (Math.Abs(recorded - want) > 0.01f)
                    { damageVerdict = false; damageNote += " hit#" + (k + 1) + " expectedDamage recorded=" + recorded.ToString("0.##") + " vs stage=" + want.ToString("0.##"); break; }
                    if (Math.Abs(got - want) > tol)
                    { damageVerdict = false; damageNote += " hit#" + (k + 1) + " actual=" + got.ToString("0.##") + " vs stage=" + want.ToString("0.##"); break; }
                }
                if (actualTotal < expectedTotal - tol) { damageVerdict = false; damageNote += " total too low actual=" + actualTotal.ToString("0.##") + " expected=" + expectedTotal.ToString("0.##"); }
            }
            // ratio report
            float ratio = expectedTotal > 0 ? actualTotal / expectedTotal : (actualHits == 0 ? 1f : 0f);
            damageNote += " ratio=" + ratio.ToString("0.000") + " actualTotal=" + actualTotal.ToString("0.##") + " expectedTotal=" + expectedTotal.ToString("0.##");
        }
        Log("DAMAGE FORENSICS verdict=" + damageVerdict + " " + damageNote);
    }

    // PH-R2-06: dodge (Space) timed to the enemy's attack release. Dodging FORWARD
    // (hero faces the enemy) sends the hero through the enemy, keeping it within
    // the 1.7m attack range during the 0.24s i-frames, so the rejected attack
    // reliably fires AttackEvaded -> NewWeaponCombat emits "actual-evaded-attack".
    void TryDodgeForEvade()
    {
        if (evadeSeen) return;
        if (hero == null || hero.Dodge == null || target == null) return;
        // PlayerInput.Down() reads wasPressedThisFrame. Queuing BOTH down and up
        // in the same frame lets the InputSystem coalesce the two state events,
        // so the press is never observed and the roll never starts (verified in
        // the R13 failure log: the dodge was re-injected every frame). Hold the
        // key down for one full frame, then release on the NEXT frame — the same
        // pattern used for the real F cast.
        if (dodgeKeyHeld)
        {
            // Keep the key down for several frames so the InputSystem produces a
            // real wasPressedThisFrame edge (the F cast is held the same way).
            if (Time.unscaledTime - dodgeDownAt < 0.06f) return;
            Inject(false, Key.Space); RecordCast("dodge", false);
            dodgeKeyHeld = false;
            if (hero.Dodge.IsInvulnerable) dodgeRollObserved = true;
            Log("dodge UP: IsRolling=" + hero.Dodge.IsRolling + " IsInvulnerable=" + hero.Dodge.IsInvulnerable + " dist=" + Vector3.Distance(target.transform.position, hero.transform.position).ToString("0.##"));
            dodgeKeyDownAt = Time.unscaledTime; // start the retry throttle here
            return;
        }
        if (Time.unscaledTime - dodgeKeyDownAt < 0.9f) return; // respect roll/cooldown before retrying
        if (hero.Dodge.IsInvulnerable) return;
        if (hero.Dodge.CooldownRemaining > 0) return;
        PlayerInput.Focus(true);
        FaceTarget();
        float d = Vector3.Distance(target.transform.position, hero.transform.position);
        if (d > 1.95f) return;                 // enemy must be within attack range to release
        if (target.WindingUp)
        {
            float rem = target.TelegraphRemaining;
            // Fire as LATE as possible: the roll moves the hero 4.2m in .42s, so
            // dodging at rem=.22 would carry the hero THROUGH the 1.7m-distant
            // enemy before release, flipping offset vs lockedDirection and making
            // the product's attack-cone check miss (no AttackEvaded event). With
            // rem<=.10 the hero is still in front of the enemy, inside the .24s
            // i-frames, and the genuine attack is rejected -> actual-evaded-attack.
            if (rem > 0.0f && rem <= 0.10f)
            {
                Inject(true, Key.Space); RecordCast("dodge", true);
                dodgeKeyHeld = true;
                dodgeDownAt = Time.unscaledTime;
                Log("dodge DOWN timed to telegraph release (rem=" + rem.ToString("0.000") + ")");
            }
        }
    }

    // PH-R2-02/06/07 helpers --------------------------------------------------
    bool TargetInReach(float meters)
    {
        if (target == null || hero == null) return false;
        float d = Vector3.Distance(target.transform.position, hero.transform.position);
        return d <= meters;
    }
    void FaceTarget()
    {
        if (target == null || hero == null) return;
        hero.transform.LookAt(new Vector3(target.transform.position.x, hero.transform.position.y, target.transform.position.z));
    }
    // PH-R2-only instrumentation: place the GENUINE target (enemy) at `distance`
    // meters from the (stationary, in-camp-bounds) hero, on the hero's ground
    // level, facing the hero. We deliberately NEVER move the hero: CampFacilities
    // clamps the hero back to camp bounds whenever CampRuntime.Exploring is true
    // (it stays true after departure), so any hero teleport is reverted. Moving the
    // enemy instead keeps the hero put while guaranteeing the skill's reach/LOS is
    // satisfied. The enemy, its HP and EVERY damage event remain REAL product paths;
    // no target HP is modified and no event is faked. Re-applied every frame so the
    // enemy (which chases the hero) cannot drift out of reach.
    void RepositionTargetAdjacentToHero(float distance)
    {
        if (hero == null || target == null) return;
        Vector3 toTarget = Vector3.ProjectOnPlane(target.transform.position - hero.transform.position, Vector3.up);
        if (toTarget.magnitude > distance)
        {
            Vector3 pos = hero.transform.position + toTarget.normalized * distance;
            pos.y = hero.transform.position.y; // keep the enemy on the hero's ground level so it stays in melee reach
            target.transform.position = pos;
            // A CharacterController caches its own position; a direct transform
            // teleport is reverted by the next controller.Move unless we re-sync it.
            // Toggle the controller off/on so its internal position matches the
            // teleport and subsequent Move() calls accumulate from the new spot.
            var cc = target.GetComponent<CharacterController>();
            if (cc != null) { cc.enabled = false; cc.enabled = true; }
        }
        // keep the hero facing the target so the tracked melee facing (and LOS) is valid
        hero.transform.LookAt(new Vector3(target.transform.position.x, hero.transform.position.y, target.transform.position.z));
    }
    Vector3 TargetPos() { return target != null ? target.transform.position : Vector3.zero; }
    string Vec(Vector3 v) { return string.Format("{0:0.00},{1:0.00},{2:0.00}", v.x, v.y, v.z); }

    // ========================================================================
    // SCENARIO SETUP (public business API only)
    // ========================================================================
    void SetupLoadout()
    {
        if (gear == null) { Fail("AdventureLoadout missing"); return; }
        gear.items.RemoveAll(it => !it.worn && !it.Container);
        var weapon_item = AdventureItems.New(weapon, quality);
        weapon_item.affixes = affix >= 0 ? new int[] { affix } : new int[0];
        gear.AddOrStore(weapon_item);
        gear.mainWeapon = weapon_item.id;
        if (!gear.SelectMain(weapon_item)) Log("SelectMain returned false; forcing EquipmentChanged");
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
        // PH-R2-06: watch for a real attack rejected by the hero's dodge i-frames
        if (newWeapons != null) newWeapons.Observed += OnNewWeaponT3;
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
    }
    void OnMelee(AdventureCombat.MeleeObservation m)
    {
        // PH-R1 evidence channel retained (feeds damageCount / expectZeroDamage).
        // PH-R2 authoritative forensics come from CombatHealth.Observed instead.
        if (m.reason == "DAMAGE")
            damages.Add(new Dictionary<string, object> { ["source"] = "melee", ["attack"] = m.attack, ["before"] = m.before, ["after"] = m.after, ["time"] = Time.unscaledTime });
    }
    // PH-R2-06/07: capture T3 traces (evade / counter empower / pull)
    void OnNewWeaponT3(NewWeaponCombat.Trace t)
    {
        if (t.stage == "actual-evaded-attack")
        {
            if (!evadeSeen) { evadeSeen = true; evadeSeenAt = Time.unscaledTime; Log("OBS actual-evaded-attack at " + evadeSeenAt.ToString("0.000")); }
        }
        if (t.stage == "contact" && t.target != null)
        {
            string tid = (t.target is CombatEnemy ce) ? (ce.entityId ?? "") : "";
            // Latch ONLY the FIRST counter contact (the empowered one). A later
            // second counter is recorded separately below; without this guard its
            // empowered=false would overwrite counterEmpowered and erase the
            // consume-once evidence even though the product behaved correctly.
            if (mode == "twin_counter" && tid == targetEntityId && !secondCounterAttempted && !counterContactSeen)
            {
                counterContactSeen = true;
                counterEmpowered = t.empowered;
                counterDamage = (t.after < t.before) ? (t.before - t.after) : 0f;
                Log("OBS counter contact empowered=" + t.empowered + " dmg=" + counterDamage.ToString("0.##"));
            }
        }
        if (mode == "twin_counter" && t.stage == "contact" && counterContactSeen && secondCounterAttempted && !secondCounterContactSeen && t.target != null)
        {
            string tid = (t.target is CombatEnemy ce) ? (ce.entityId ?? "") : "";
            if (tid == targetEntityId) { secondCounterContactSeen = true; secondCounterEmpowered = t.empowered; Log("OBS counter2 contact empowered=" + t.empowered); }
        }
        if (mode == "soul_pull")
        {
            if (t.stage == "pull-start") { pullStartSeen = true; Log("OBS pull-start"); }
            else if (t.stage == "pull-obstructed") { pullObstructedSeen = true; Log("OBS pull-obstructed"); }
            else if (t.stage == "control-immune") { controlImmuneSeen = true; Log("OBS control-immune"); }
        }
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
    }

    void RecordCast(string label, bool attempted) { casts.Add(new Dictionary<string, object> { ["label"] = label, ["attempted"] = attempted, ["at"] = Time.unscaledTime }); }

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

    bool T3VerdictOk()
    {
        if (mode == "twin_counter")
        {
            // PH-R2-R1-02 STRICT consume-once. All five runtime facts must hold:
            //   real enemy attack seen (evadeSeen) + real roll (dodgeRollObserved)
            //   + first counter contact (empowered=true, 1.8x damage)
            //   + SECOND counter contact observed and NOT empowered.
            // If the second cast never contacts (e.g. blocked by the product's
            // ~8s cooldown), the run is INCOMPLETE, never PASS. We do NOT shorten
            // product cooldowns, and we do NOT touch consumedEvade / empower state.
            bool ok = evadeSeen && dodgeRollObserved && counterContactSeen && counterEmpowered
                      && secondCounterContactSeen && !secondCounterEmpowered;
            if (!secondCounterContactSeen)
            {
                incompleteReason = "T3 counter: second counter produced NO contact within window; consume-once cannot be attested (INCOMPLETE, not PASS)";
                Log("T3 INCOMPLETE: " + incompleteReason);
            }
            if (ok && secondCounterEmpowered)
            {
                ok = false;
                failReason = failReason + (failReason.Length > 0 ? "; " : "") + "T3 counter: evade was NOT consumed (second counter also empowered)";
            }
            if (!ok) failReason = failReason + (failReason.Length > 0 ? "; " : "")
                + "T3 counter: evade=" + evadeSeen + " roll=" + dodgeRollObserved + " contact=" + counterContactSeen
                + " empowered=" + counterEmpowered + " secondContact=" + secondCounterContactSeen
                + " secondEmpowered=" + secondCounterEmpowered;
            return ok;
        }
        if (mode == "soul_pull")
        {
            bool hpUnchanged = (target != null && target.Health != null) ? Mathf.Abs(target.Health.Current - targetInitialHP) < 0.5f : false;
            float moved = pullPeakDisplacement; // peak, not last-frame delta (avoids a returning enemy erasing the pull)
            bool ok = pullStartSeen && hpUnchanged && moved > 0.3f;
            if (!ok) failReason = failReason + (failReason.Length > 0 ? "; " : "") + "T3 pull: start=" + pullStartSeen + " hpUnchanged=" + hpUnchanged + " moved=" + moved.ToString("0.##");
            return ok;
        }
        return true;
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

        bool t3Ok = T3VerdictOk();
        bool damageOk = !verifyDamage || damageVerdict || mode == "soul_pull"; // soul_pull verified via T3
        if (verifyDamage && !damageVerdict && mode != "soul_pull") { Log("DAMAGE_CHECK fail: " + damageNote); }

        // PH-R2-R1-01: a run whose Player-computed assembly identity does not
        // match the expected DLL SHA can NEVER pass.
        bool identityOk = identityVerified;
        bool incomplete = mode == "twin_counter" && !secondCounterContactSeen;
        if (incomplete && string.IsNullOrEmpty(incompleteReason))
            incompleteReason = "T3 counter: second counter produced NO contact; consume-once cannot be attested";

        bool pass = !failed && skillCompletes.Count >= 1 && cooldownOk && descOk && zeroDamageOk
                    && t3Ok && damageOk && identityOk && !incomplete;
        if (!identityOk) Log("IDENTITY_CHECK fail: " + identityNote);
        if (incomplete) Log("INCOMPLETE: " + incompleteReason);
        Log("VERDICT pass=" + pass + " incomplete=" + incomplete + " identityOk=" + identityOk
            + " descOk=" + descOk + descNote + " zeroDamageOk=" + zeroDamageOk + " cooldownOk=" + cooldownOk + " " + cooldownNote
            + " t3Ok=" + t3Ok + " damageOk=" + damageOk + " damaged=" + damaged
            + " starts=" + skillStarts.Count + " completes=" + skillCompletes.Count);
        WriteResult(pass);
        quitting = true;
        // distinct exit code 2 => INCOMPLETE (never silently mapped to PASS)
        Application.Quit(incomplete ? 2 : (pass ? 0 : 1));
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
            ["buildId"] = buildId,
            ["unityVersion"] = Application.unityVersion,
            // PH-R2-R1-01 §3.2: Player-computed identity of the ACTUALLY loaded
            // managed assembly. These are never copied from the command line.
            ["loadedAssemblyPath"] = loadedAssemblyPath,
            ["loadedAssemblySha256"] = loadedAssemblySha256,
            ["loadedAssemblyName"] = loadedAssemblyName,
            ["expectedAssemblySha256"] = expectedDllSha,
            ["expectedExeSha256"] = expectedExeSha,
            ["identityVerified"] = identityVerified,
            ["identityNote"] = identityNote,
            ["incomplete"] = mode == "twin_counter" && !secondCounterContactSeen,
            ["incompleteReason"] = incompleteReason,
            ["weapon"] = weapon.ToString(),
            ["quality"] = quality.ToString(),
            ["affix"] = affix,
            ["slot"] = slot,
            ["chargeSeconds"] = chargeSeconds,
            ["expectedCooldown"] = expectedCooldown,
            ["mode"] = mode,
            ["verifyDamage"] = verifyDamage,
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
            // PH-R2-R1-FIX-01: clock provenance, so no reader can mistake one
            // clock for the other again.
            ["timebase"] = new Dictionary<string, object>
            {
                ["settleClock"] = "Time.unscaledTime",
                ["productClock"] = "Time.timeAsDouble (CombatHealth.activeTime)",
                ["damageQuietPeriodSeconds"] = DamageQuietPeriodSeconds,
                ["lastDamageUnscaledTime"] = lastDamageUnscaledTime,
                ["lastDamageActiveTime"] = lastDamageActiveTime,
                ["damageWindowStart"] = damageWindowStart,
                ["damageWindowClosedAt"] = damageWindowClosedAt,
                ["damageWindowCloseReason"] = damageWindowCloseReason,
                ["observedClockOffset"] = (lastDamageActiveTime > 0d && lastDamageUnscaledTime > 0f)
                    ? (double)lastDamageUnscaledTime - lastDamageActiveTime : 0d,
            },
            ["skillStarts"] = skillStarts,
            ["skillCompletes"] = skillCompletes,
            ["damageCount"] = damages.Count,
            ["skillDescription"] = desc,
            ["observations"] = observations,
            ["damages"] = damages,
            ["keyEvents"] = keyEvents,
            ["casts"] = casts,
            ["log"] = logLines,
            // PH-R2 additions
            ["target"] = new Dictionary<string, object>
            {
                ["entityId"] = targetEntityId,
                ["archetype"] = targetArchetypeObserved,
                ["initialHP"] = targetInitialHP,
                ["maxHP"] = targetMaxHP,
                ["attackerAttackPower"] = attackerAttackPower,
                ["attackerDefense"] = attackerDefense,
                ["prepared"] = targetPrepared,
                ["posBefore"] = Vec(targetPosBefore),
                ["posAfter"] = Vec(targetPosAfter),
            },
            ["damageForensics"] = damageForensics,
            ["damageVerdict"] = (verifyDamage && mode != "soul_pull") ? damageVerdict : true,
            ["damageNote"] = damageNote,
            ["expectedHits"] = expectedHits,
            ["expectedPerHit"] = expectedPerHit,
            ["expectedTotal"] = expectedTotal,
            ["actualHits"] = damageForensics.Count,
            ["uniformHits"] = uniformHits,
            ["expectedHitRatios"] = expectedHitRatios,
            ["secondCounterContactSeen"] = secondCounterContactSeen,
            ["t3"] = new Dictionary<string, object>
            {
                ["mode"] = mode,
                ["evadeSeen"] = evadeSeen,
                ["evadeSeenAt"] = evadeSeenAt,
                ["counterEmpowered"] = counterEmpowered,
                ["counterDamage"] = counterDamage,
                ["dodgeRollObserved"] = dodgeRollObserved,
                ["secondCounterEmpowered"] = secondCounterEmpowered,
                ["pullStartSeen"] = pullStartSeen,
                ["controlImmuneSeen"] = controlImmuneSeen,
                ["pullObstructedSeen"] = pullObstructedSeen,
                ["pullPeakDisplacement"] = pullPeakDisplacement,
                ["pullPosBefore"] = Vec(targetPosBefore),
                ["pullPosAfter"] = Vec(targetPosAfter),
            },
        };
        string json = MiniJson(result);
        string path = Path.Combine(dataRoot, "result.json");
        File.WriteAllText(path, json);
        File.WriteAllText(Path.Combine(dataRoot, "harness.log"), string.Join("\n", logLines));
        // PH-R2 forensic artifacts
        WriteJsonl(Path.Combine(dataRoot, "target-events.jsonl"), targetEvents);
        WriteJsonl(Path.Combine(dataRoot, "damage-events.jsonl"), damageForensics);
        Log("wrote result.json pass=" + pass + " -> " + path);
    }

    void WriteJsonl(string path, List<Dictionary<string, object>> rows)
    {
        try
        {
            var sb = new System.Text.StringBuilder();
            foreach (var r in rows) sb.Append(MiniJson(r)).Append("\n");
            File.WriteAllText(path, sb.ToString());
        }
        catch (Exception e) { Log("WriteJsonl warn: " + e.Message); }
    }

    void Enter(string p) { phase = p; phaseEnteredAt = Time.unscaledTime; Log("phase -> " + p); }

    // ========================================================================
    // PH-R2-R1-FIX-01: runtime time-base probe (mode=timebase)
    // The settle window is a decision about Time.unscaledTime. This probe proves
    // IN THE REAL PLAYER that (a) Time.timeScale=0 freezes Time.time but not
    // Time.unscaledTime, (b) the decision still behaves correctly while scaled
    // time is frozen, (c) a product activeTime that trails the unscaled clock by
    // the observed ~4.36s offset can never shorten the quiet period, and
    // (d) the hard cap still terminates the window when no damage ever lands.
    // ========================================================================
    int tbStep = 0;
    float tbU0 = -1f, tbT0 = -1f, tbOrigScale = 1f;
    readonly Dictionary<string, object> tbCases = new Dictionary<string, object>();

    void TbCase(string name, float nowU, float lastU, float startU, float cap, bool expectClose,
                string expectReason = null)
    {
        bool got = DamageWindowShouldClose(nowU, lastU, startU, cap);
        string reason = DamageWindowCloseReason(nowU, lastU, startU, cap);
        bool reasonOk = expectReason == null || reason == expectReason;
        tbCases[name] = new Dictionary<string, object>
        {
            ["expectClose"] = expectClose, ["closed"] = got, ["reason"] = reason,
            ["expectReason"] = expectReason,
            ["ok"] = (got == expectClose) && reasonOk,
            ["inputs"] = "now=" + nowU.ToString("0.000") + " lastUnscaled=" + lastU.ToString("0.000")
                        + " start=" + startU.ToString("0.000") + " cap=" + cap.ToString("0.00"),
        };
    }

    void StepTimebaseProbe()
    {
        try
        {
            switch (tbStep)
            {
                case 0:
                    tbOrigScale = Time.timeScale;
                    // Freeze GAME time. A settle decision that silently depended on
                    // scaled time would now stop advancing.
                    Time.timeScale = 0f;
                    tbU0 = Time.unscaledTime; tbT0 = Time.time;
                    Log("timebase: timeScale set to 0 (was " + tbOrigScale.ToString("0.##") + "), u0=" + tbU0.ToString("0.000") + " t0=" + tbT0.ToString("0.000"));
                    tbStep = 1;
                    break;

                case 1:
                    if (Time.unscaledTime - tbU0 < 0.40f) return;
                    float dU = Time.unscaledTime - tbU0;
                    float dT = Time.time - tbT0;
                    tbCases["timescale_zero_unscaled_advances"] = new Dictionary<string, object>
                    {
                        ["dUnscaled"] = dU, ["dScaled"] = dT,
                        ["ok"] = dU > 0.30f && Mathf.Abs(dT) < 0.05f,
                        ["note"] = "timeScale=0 must freeze Time.time while Time.unscaledTime keeps advancing",
                    };
                    // REAL evaluation at the ambient (frozen-scaled) moment: only
                    // ~0.4s of unscaled time has passed, so the window MUST stay
                    // open. With the old mixed-clock formula the trailing
                    // activeTime would have closed it immediately.
                    TbCase("timescale_zero_real_now_stays_open", Time.unscaledTime, tbU0, tbU0, 4.5f, false);
                    Log("timebase: dU=" + dU.ToString("0.000") + " dT=" + dT.ToString("0.000") + " (scaled frozen)");
                    Time.timeScale = tbOrigScale; // restore EXACTLY (never normalize)
                    tbStep = 2;
                    break;

                case 2:
                    // The window is armed at the moment of the last damage, so the
                    // hard cap cannot be reached and the quiet period alone decides.
                    float u = 1000f;
                    TbCase("quiet_open_at_0.50s", u + 0.50f, u, u, 4.5f, false, "");
                    TbCase("quiet_open_at_1.19s", u + 1.19f, u, u, 4.5f, false, "");
                    TbCase("quiet_closes_at_1.21s", u + 1.21f, u, u, 4.5f, true, "quiet");
                    // a late pulse arriving 1.00s after the previous hit is still
                    // inside the quiet period -> window open -> the hit is kept
                    TbCase("delayed_pulse_at_1.00s_still_open", u + 1.00f, u, u, 4.5f, false, "");
                    // product clock trails the unscaled clock by ~4.36s; the settle
                    // decision must be unaffected by that offset
                    TbCase("cross_clock_offset_does_not_close", u + 0.05f, u, u, 4.5f, false, "");
                    TbCase("no_damage_hardcap_stays_open", u + 1.00f, -1f, u, 4.5f, false, "");
                    TbCase("no_damage_hardcap_closes", u + 4.60f, -1f, u, 4.5f, true, "hardcap");
                    // legacy-formula demonstration: value it WOULD have produced
                    float legacyActive = u - 4.3586f;
                    tbCases["legacy_formula_would_close_early"] = new Dictionary<string, object>
                    {
                        ["legacyValue"] = (u + 0.05f) - legacyActive,
                        ["ok"] = ((u + 0.05f) - legacyActive) > DamageQuietPeriodSeconds,
                        ["note"] = "documents defect F-1b: unscaledTime - activeTime is a cross-clock subtraction",
                    };
                    WriteTimebaseResult();
                    tbStep = 3;
                    break;
            }
        }
        catch (Exception e)
        {
            Log("timebase probe exception: " + e.GetType().Name + ": " + e.Message);
            tbCases["exception"] = new Dictionary<string, object> { ["ok"] = false, ["note"] = e.Message };
            WriteTimebaseResult();
            tbStep = 3;
        }
    }

    void WriteTimebaseResult()
    {
        bool allOk = tbCases.Count > 0;
        foreach (var kv in tbCases)
        {
            var d = kv.Value as Dictionary<string, object>;
            if (d != null && d.ContainsKey("ok") && !(bool)d["ok"]) allOk = false;
        }
        var probe = new Dictionary<string, object>
        {
            ["marker"] = PlayerAcceptanceHarness.MARKER,
            ["version"] = PlayerAcceptanceHarness.VERSION,
            ["runId"] = runId,
            ["processId"] = Process.GetCurrentProcess().Id,
            ["buildSha"] = buildSha,
            ["buildId"] = buildId,
            ["unityVersion"] = Application.unityVersion,
            ["loadedAssemblyPath"] = loadedAssemblyPath,
            ["loadedAssemblySha256"] = loadedAssemblySha256,
            ["loadedAssemblyName"] = loadedAssemblyName,
            ["expectedAssemblySha256"] = expectedDllSha,
            ["identityVerified"] = identityVerified,
            ["settleClock"] = "Time.unscaledTime",
            ["productClock"] = "Time.timeAsDouble (CombatHealth.activeTime)",
            ["damageQuietPeriodSeconds"] = DamageQuietPeriodSeconds,
            ["allOk"] = allOk,
            ["cases"] = tbCases,
        };
        try
        {
            File.WriteAllText(Path.Combine(dataRoot, "timebase-probe.json"), MiniJson(probe));
            File.WriteAllText(Path.Combine(dataRoot, "harness.log"), string.Join("\n", logLines));
        }
        catch (Exception e) { Log("timebase write warn: " + e.Message); }

        // a driver-compatible result.json (same identity contract as a real run)
        var result = new Dictionary<string, object>
        {
            ["marker"] = PlayerAcceptanceHarness.MARKER,
            ["version"] = PlayerAcceptanceHarness.VERSION,
            ["scenarioId"] = scenarioId,
            ["runId"] = runId,
            ["processId"] = Process.GetCurrentProcess().Id,
            ["buildSha"] = buildSha,
            ["buildId"] = buildId,
            ["unityVersion"] = Application.unityVersion,
            ["loadedAssemblyPath"] = loadedAssemblyPath,
            ["loadedAssemblySha256"] = loadedAssemblySha256,
            ["loadedAssemblyName"] = loadedAssemblyName,
            ["expectedAssemblySha256"] = expectedDllSha,
            ["expectedExeSha256"] = expectedExeSha,
            ["identityVerified"] = identityVerified,
            ["identityNote"] = identityNote,
            ["incomplete"] = false,
            ["incompleteReason"] = "",
            ["mode"] = mode,
            ["pass"] = allOk && identityVerified,
            ["failed"] = !allOk,
            ["failReason"] = allOk ? "" : "timebase probe case failed",
            ["startedAt"] = startedAt,
            ["finishedAt"] = Time.unscaledTime,
            ["timebase"] = probe,
            ["log"] = logLines,
        };
        try { File.WriteAllText(Path.Combine(dataRoot, "result.json"), MiniJson(result)); }
        catch (Exception e) { Log("timebase result write warn: " + e.Message); }
        Log("timebase probe allOk=" + allOk + " -> " + Path.Combine(dataRoot, "timebase-probe.json"));
        quitting = true;
        Application.Quit((allOk && identityVerified) ? 0 : 1);
    }

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
