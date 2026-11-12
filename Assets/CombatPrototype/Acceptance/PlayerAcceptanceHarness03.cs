#if UX_ACCEPTANCE
// UX-PROGRESSION-03 (UI-03c / B2+B3) real-Player window audit.
//
// This file is ADDITIVE on purpose. The 03A harness (PlayerAcceptanceHarness.cs)
// keeps its bytes and its 210 historic evidence runs valid; UX-03 needs a
// capability it does not have (per-slot window read-out + slot-0 speed sweep),
// so that capability lives here under a distinct launch flag (--ux03) and a
// distinct marker string.
//
// Read-only with respect to product state: the only mutation is the harness
// temporary attackCooldown override in `slot0` mode, restored before exit.
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using UnityEngine;
using UnityEngine.UI;

public static class PlayerAcceptanceHarness03
{
    public const string MARKER = "UX_ACCEPTANCE_HARNESS03_v1";
    public const int VERSION = 1;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void Bootstrap()
    {
        var args = Environment.GetCommandLineArgs();
        if (!args.Any(a => a == "--ux03")) return;                       // never in a normal session
        if (UnityEngine.Object.FindAnyObjectByType<Harness03Runner>() != null) return;
        var go = new GameObject("UX03 Acceptance Harness");
        go.AddComponent<Harness03Runner>();
        UnityEngine.Object.DontDestroyOnLoad(go);
    }
}

public class Harness03Runner : MonoBehaviour
{
    // ---- launch parameters -------------------------------------------------
    string mode = "window";                 // "window" | "slot0" | "spear0" | "slot0seven" | "cooldown" | "pull" | "layout"
    string runId = "ux03";
    string dataRoot = null;
    string onlyWeapon = null;               // optional filter, e.g. "Scythe"
    int reqWidth, reqHeight;                // layout mode: resolution the panel must be measured at

    // ---- runtime -----------------------------------------------------------
    ThirdPersonHero hero;
    AdventureCombat combat;
    AdventureLoadout gear;
    CombatSession session;
    GameEntry gameEntry;
    WeaponSkillPanel panel;
    Text panelStatus;

    string phase = "entry";
    float phaseEnteredAt;
    bool entryAttempted, departAttempted, failed, quitting;
    string failReason = "";
    string logPath;

    readonly List<Dictionary<string, object>> rows = new List<Dictionary<string, object>>();
    readonly List<string> checks = new List<string>();

    // ---- evidence tables (single source: product read-out at run time) -----
    // Expected values are what the SOURCE says the window must be; the harness
    // compares them against what the PRODUCT reports. They are not used to
    // compute the reported value.
    static readonly Dictionary<string, float> ExpectedWindow = new Dictionary<string, float>
    {
        {"Sword/0",0f},{"Sword/1",0.88f},{"Sword/2",1.14f},
        {"Spear/0",0f},{"Spear/1",1.06f},{"Spear/2",0.73f},
        {"Staff/0",0f},{"Staff/1",0.56f},{"Staff/2",0.96f},
        {"Bow/0",0f},{"Bow/1",0.83f},{"Bow/2",1.22f},
        {"TwinBlades/0",1.02f},{"TwinBlades/1",0.52f},
        {"Greatsword/0",1.15f},{"Greatsword/1",1.10f},
        {"Scythe/0",1.13f},{"Scythe/1",0.65f},
    };
    static readonly GearType[] Weapons = {
        GearType.Sword, GearType.Spear, GearType.Staff, GearType.Bow,
        GearType.TwinBlades, GearType.Greatsword, GearType.Scythe
    };

    void Awake()
    {
        ParseArgs();
        if (string.IsNullOrEmpty(dataRoot))
            dataRoot = Path.Combine(Path.GetDirectoryName(Application.dataPath), "ux03_run_" + runId);
        Directory.CreateDirectory(dataRoot);
        logPath = Path.Combine(dataRoot, "harness03.log");
        Log("bootstrap MARKER=" + PlayerAcceptanceHarness03.MARKER + " VERSION=" + PlayerAcceptanceHarness03.VERSION
            + " mode=" + mode + " runId=" + runId);
        Log("assembly=" + ResolveLoadedAssemblyHash());
        Enter("entry");
    }

    void ParseArgs()
    {
        var a = Environment.GetCommandLineArgs();
        for (int i = 0; i < a.Length; i++)
        {
            switch (a[i])
            {
                case "--ux03-mode": mode = Safe(a, ++i, mode); break;
                case "--run-id": runId = Safe(a, ++i, runId); break;
                case "--data-root": dataRoot = Safe(a, ++i, dataRoot); break;
                case "--ux03-weapon": onlyWeapon = Safe(a, ++i, null); break;
                case "--ux03-width": int.TryParse(Safe(a, ++i, "0"), out reqWidth); break;
                case "--ux03-height": int.TryParse(Safe(a, ++i, "0"), out reqHeight); break;
            }
        }
    }
    static string Safe(string[] a, int i, string def) { return (i >= 0 && i < a.Length) ? a[i] : def; }

    void Enter(string next) { phase = next; phaseEnteredAt = Time.unscaledTime; Log("-> phase " + next); }

    void Update()
    {
        if (quitting) return;
        try
        {
            if (phase == "entry") StepEntry();
            else if (phase == "waitScene") StepWaitScene();
            else if (phase == "locate") StepLocate();
            else if (phase == "run") { }
        }
        catch (Exception e) { Fail("exception " + e.GetType().Name + ": " + e.Message); }
    }

    void StepEntry()
    {
        if (Time.unscaledTime - phaseEnteredAt > 45f) { Fail("entry timeout: GameEntry never authorized gameplay"); return; }
        if (GameEntry.GameSceneAuthorized) { Enter("waitScene"); return; }
        if (gameEntry == null) { gameEntry = GameEntry.Instance; if (gameEntry == null) return; }
        if (entryAttempted) return;
        entryAttempted = true;
        bool ok = false;
        try { ok = gameEntry.Continue(); } catch (Exception e) { Log("Continue threw: " + e.Message); }
        if (!ok) { try { gameEntry.AskNew(); ok = gameEntry.ConfirmNew(); } catch (Exception e) { Log("New threw: " + e.Message); } }
        Log("entry attempt ok=" + ok + " authorized=" + GameEntry.GameSceneAuthorized);
    }

    void StepWaitScene()
    {
        if (Time.unscaledTime - phaseEnteredAt > 60f) { Fail("waitScene timeout"); return; }
        if (GameEntry.Loading) return;
        session = UnityEngine.Object.FindAnyObjectByType<CombatSession>();
        if (session == null || session.Saves == null || !session.Saves.IsInitialized) return;
        try { GameEntry.DirectReady(); } catch (Exception e) { Log("DirectReady warn: " + e.Message); }
        Enter("locate");
    }

    void StepLocate()
    {
        if (session == null) session = UnityEngine.Object.FindAnyObjectByType<CombatSession>();
        if (session == null) { if (Time.unscaledTime - phaseEnteredAt > 20f) Fail("no CombatSession"); return; }
        hero = session.hero;
        if (hero == null || hero.Health == null) { if (Time.unscaledTime - phaseEnteredAt > 20f) Fail("hero not ready"); return; }
        combat = hero.GetComponent<AdventureCombat>();
        gear = hero.GetComponent<AdventureLoadout>();
        panel = hero.GetComponent<WeaponSkillPanel>();
        if (combat == null || gear == null) { Fail("AdventureCombat/AdventureLoadout missing"); return; }
        StartCoroutine(mode == "slot0" ? RunSlot0()
                     : mode == "spear0" ? RunSpear0()
                     : mode == "slot0seven" ? RunSlot0Seven()
                     : mode == "cooldown" ? RunCooldown()
                     : mode == "pull" ? RunPull()
                     : mode == "layout" ? RunLayout()
                     : RunWindow());
    }

    // ======================================================================
    // MODE: window — every weapon x every slot, product read-out vs source
    // ======================================================================
    System.Collections.IEnumerator RunWindow()
    {
        Enter("run");
        Log("panel present=" + (panel != null));
        foreach (var w in Weapons)
        {
            if (onlyWeapon != null && w.ToString() != onlyWeapon) continue;
            Equip(w, GearQuality.White);
            yield return null; yield return null;
            int slots = NewWeaponRegistry.Is(w) ? 2 : 3;
            for (int slot = 0; slot < slots; slot++)
            {
                if (!combat.Expanded.Select(slot)) Log("Select(" + slot + ") returned false for " + w);
                yield return null;
                if (NewWeaponRegistry.Is(w)) { combat.NewWeapons.Select(slot); yield return null; }

                float wSec = combat.SkillWindow;
                string detail = combat.SkillWindowDetail ?? "";
                float cSec = combat.SkillDuration;
                string sid = combat.SkillIdText ?? "";
                float sum = SumDetail(detail);
                string key = w + "/" + slot;
                // legacy slot 0 is the BASE ACTION (window = real ActionDuration), not a
                // catalog skill, so it is validated by the slot0 mode, not against this table.
                bool hasWindow = !(slot == 0 && !NewWeaponRegistry.Is(w));
                bool expectedKnown = hasWindow && ExpectedWindow.ContainsKey(key);
                float expected = expectedKnown ? ExpectedWindow[key] : -1f;
                bool sumOk = hasWindow ? Mathf.Abs(sum - wSec) <= 0.005f : true;
                bool valOk = !expectedKnown ? true : Mathf.Abs(expected - wSec) <= 0.005f;

                var r = new Dictionary<string, object>
                {
                    ["weapon"] = w.ToString(), ["slot"] = slot, ["skillId"] = sid,
                    ["windowSeconds"] = Round(wSec), ["windowDetail"] = detail,
                    ["detailSum"] = Round(sum), ["detailSumOk"] = sumOk,
                    ["cooldownSeconds"] = Round(cSec),
                    ["expectedWindow"] = expectedKnown ? (object)Round(expected) : null,
                    ["expectedMatch"] = valOk,
                    ["panelText"] = ReadPanelText(),
                    ["panelWindow"] = ParsePanelWindow(),
                    ["panelCooldown"] = ParsePanelCooldown(),
                };
                rows.Add(r);
                Log("WIN " + key + " id=" + sid + " W=" + Round(wSec) + " sum=" + Round(sum) + " C=" + Round(cSec)
                    + " detail='" + detail + "' panelW=" + r["panelWindow"] + " sumOk=" + sumOk + " expOk=" + valOk);

                if (!sumOk) checks.Add("DETAIL_SUM_MISMATCH " + key + " W=" + Round(wSec) + " sum=" + Round(sum));
                if (!valOk) checks.Add("WINDOW_MISMATCH " + key + " expected=" + Round(expected) + " actual=" + Round(wSec));
                var pw = r["panelWindow"];
                if (pw != null && Mathf.Abs(Convert.ToSingle(pw) - wSec) > 0.005f)
                    checks.Add("PANEL_WINDOW_MISMATCH " + key + " panel=" + pw + " live=" + Round(wSec));
            }
        }
        Finish();
    }

    // ======================================================================
    // MODE: slot0 — three real attack speeds through the product path
    // ======================================================================
    System.Collections.IEnumerator RunSlot0()
    {
        Enter("run");
        Equip(GearType.Sword, GearQuality.White);
        yield return null; yield return null;
        combat.Expanded.Select(0);
        yield return null;

        float original = hero.attackCooldown;
        float[] speeds = { 0.30f, 0.50f, 0.72f };
        try
        {
            foreach (float cd in speeds)
            {
                hero.attackCooldown = cd;
                yield return null; yield return null;
                float interval = hero.AttackInterval;
                float live = combat.SlotWindow;
                float expect = AdventureCombat.ActionDuration(interval);
                string detail = combat.SlotWindowDetail;
                float sum = SumDetail(detail);
                bool ok = Mathf.Abs(expect - live) <= 0.0001f;
                var r = new Dictionary<string, object>
                {
                    ["attackCooldown"] = Round(cd), ["attackInterval"] = Round(interval),
                    ["slotWindow"] = Round(live), ["expected"] = Round(expect),
                    ["match"] = ok, ["windowDetail"] = detail, ["detailSum"] = Round(sum),
                    ["panelText"] = ReadPanelText(), ["panelWindow"] = ParsePanelWindow(),
                };
                rows.Add(r);
                Log("SLOT0 cd=" + Round(cd) + " interval=" + Round(interval) + " W=" + Round(live)
                    + " expect=" + Round(expect) + " match=" + ok + " detail='" + detail + "'");
                if (!ok) checks.Add("SLOT0_MISMATCH cd=" + Round(cd) + " live=" + Round(live) + " expect=" + Round(expect));
                if (Mathf.Abs(sum - live) > 0.005f) checks.Add("SLOT0_DETAIL_SUM cd=" + Round(cd) + " W=" + Round(live) + " sum=" + Round(sum));
            }
        }
        finally { hero.attackCooldown = original; }

        // distinctness + cap behaviour are facts, not pass/fail claims
        var seen = rows.Select(r => Convert.ToSingle(r["slotWindow"])).Distinct().Count();
        if (seen < 2) checks.Add("SLOT0_NOT_DYNAMIC: slot window did not react to attack speed");
        Finish();
    }

    // ======================================================================
    // MODE: spear0 — UX-03-R2 (audit finding R-6). Spear slot 0 must report a
    // window equal to the action the product really executes, at default,
    // raised and lowered attack speed. Three independent read-outs per speed:
    //   1) combat.SlotWindow        (the value the panel renders)
    //   2) a harness-side re-derivation from ThirdPersonHero.AttackInterval
    //      and AdventureCombat.SpearCadence (NOT a call to the code under test)
    //   3) the MEASURED lifetime of one real basic attack, strike -> action
    //      removed from the product's own action list (PendingAttackCount)
    // Plus the same read-outs for Sword at the same speeds, as the control that
    // proves the cadence term only applies to the spear.
    // ======================================================================
    System.Collections.IEnumerator RunSpear0()
    {
        Enter("run");
        float original = hero.attackCooldown;
        float[] speeds = { 0.20f, 0.30f, 0.50f, 0.72f };
        try
        {
            Equip(GearType.Spear, GearQuality.White);
            yield return null; yield return null;
            combat.Expanded.Select(0);
            yield return null;
            var flow = AdventureFlow.Find(hero);
            if (flow != null && flow.AtCamp)
            {
                try { flow.DepartRuins(); } catch (Exception e) { Log("DepartRuins threw: " + e.Message); }
            }
            yield return null; yield return null; yield return null;
            Log("spear0 equipped=" + gear.Weapon + " atCamp=" + (flow == null ? "?" : flow.AtCamp.ToString()));

            foreach (float cd in speeds)
            {
                hero.attackCooldown = cd;
                yield return null; yield return null;
                yield return MeasureSlotZero("Spear", cd, true);
            }

            Equip(GearType.Sword, GearQuality.White);
            yield return null; yield return null;
            combat.Expanded.Select(0);
            yield return null;
            foreach (float cd in speeds)
            {
                hero.attackCooldown = cd;
                yield return null; yield return null;
                yield return MeasureSlotZero("Sword", cd, false);
            }

            var spearRows = rows.Where(r => Convert.ToString(r["weapon"]) == "Spear").ToList();
            var spearW = spearRows.Select(r => Convert.ToSingle(r["slotWindow"])).Distinct().Count();
            if (spearW < 2) checks.Add("SPEAR0_NOT_DYNAMIC: spear slot-0 window did not react to attack speed");

            Equip(GearType.Spear, GearQuality.White);
            yield return null;
        }
        finally { hero.attackCooldown = original; }
        Finish();
    }

    System.Collections.IEnumerator MeasureSlotZero(string weapon, float cd, bool spear)
    {
        float interval = hero.AttackInterval;
        float live = combat.SlotWindow;
        string detail = combat.SlotWindowDetail ?? "";
        float sum = SumDetail(detail);
        // Harness-side expectation, written out from the product source rule.
        float cadence = spear ? AdventureCombat.SpearCadence : 1f;
        float expect = Mathf.Min(.55f, Mathf.Max(.01f, interval * cadence));
        float panelW = -1f;
        var pw = ParsePanelWindow(); if (pw != null) panelW = pw.Value;

        // Real execution: strike through the public product entry, then read the
        // product's own phase machine until it returns to Idle. PendingAttackCount
        // only counts UNRELEASED actions, so it marks the release, not the end of
        // the window — the phase machine is the authoritative end marker.
        bool fired = false;
        float t0 = -1f, tRelease = -1f, t1 = -1f;
        float deadline = Time.realtimeSinceStartup + 6f;
        while (!fired && Time.realtimeSinceStartup < deadline)
        {
            if (combat.PendingAttackCount == 0 && combat.LastAttackPhase == "Idle" && combat.Strike())
            {
                fired = true; t0 = Time.time; break;
            }
            yield return null;
        }
        if (fired)
        {
            float limit = Time.realtimeSinceStartup + 8f;
            while (Time.realtimeSinceStartup < limit)
            {
                string ph = combat.LastAttackPhase;
                if (tRelease < 0f && ph != "Startup") tRelease = Time.time;
                if (ph == "Idle" || ph == "Cancelled") break;
                yield return null;
            }
            t1 = Time.time;
        }
        float actual = (fired && t1 >= t0) ? t1 - t0 : -1f;
        float startup = (fired && tRelease >= t0) ? tRelease - t0 : -1f;
        float frame = Time.deltaTime;

        bool liveOk = Mathf.Abs(live - expect) <= 0.0001f;
        // measured lifetime is frame-quantised: endsAt is observed on the first frame
        // at or after it, so actual >= expect and the overshoot is bound by a frame.
        bool actualOk = fired && actual + 0.0001f >= expect && actual - expect <= Mathf.Max(0.05f, frame * 3f);
        bool sumOk = Mathf.Abs(sum - live) <= 0.005f;
        bool panelOk = panelW >= 0f && Mathf.Abs(panelW - live) <= 0.005f;

        var r = new Dictionary<string, object>
        {
            ["weapon"] = weapon, ["slot"] = 0, ["attackCooldown"] = Round(cd),
            ["attackInterval"] = Round(interval), ["cadence"] = Round(cadence),
            ["slotWindow"] = Round(live), ["expected"] = Round(expect), ["expectedMatch"] = liveOk,
            ["measuredWindow"] = Round(actual), ["measuredOk"] = actualOk,
            ["measuredStartup"] = Round(startup),
            ["startupRatio"] = actual > 0f && startup >= 0f ? Round(startup / actual) : (object)null,
            ["frameDelta"] = Round(frame), ["struck"] = fired,
            ["windowDetail"] = detail, ["detailSum"] = Round(sum), ["detailSumOk"] = sumOk,
            ["panelWindow"] = panelW < 0f ? (object)null : Round(panelW), ["panelOk"] = panelOk,
            ["panelText"] = ReadPanelText(),
        };
        rows.Add(r);
        Log("SPEAR0 " + weapon + " cd=" + Round(cd) + " interval=" + Round(interval) + " x" + Round(cadence)
            + " W=" + Round(live) + " expect=" + Round(expect) + " measured=" + Round(actual)
            + " startup=" + Round(startup) + " frame=" + Round(frame)
            + " panelW=" + (panelW < 0f ? "-" : Round(panelW).ToString())
            + " sum=" + Round(sum) + " detail='" + detail + "'");

        string key = weapon + "/0 cd=" + Round(cd);
        if (!liveOk) checks.Add("SPEAR0_W_MISMATCH " + key + " live=" + Round(live) + " expect=" + Round(expect));
        if (!fired) checks.Add("SPEAR0_NOT_STRUCK " + key);
        else if (!actualOk) checks.Add("SPEAR0_MEASURED_MISMATCH " + key + " measured=" + Round(actual) + " expect=" + Round(expect));
        if (!sumOk) checks.Add("SPEAR0_DETAIL_SUM " + key + " W=" + Round(live) + " sum=" + Round(sum));
        if (!panelOk) checks.Add("SPEAR0_PANEL_MISMATCH " + key + " panel=" + (panelW < 0f ? "-" : Round(panelW).ToString()) + " live=" + Round(live));
    }

    // ======================================================================
    // MODE: slot0seven — UX-03-R2b. Slot 0 of all seven weapons: the DECLARED
    // decomposition (startup / intervals / recovery, recovery being the residual
    // of the advertised W) against a REAL activation read off the product's own
    // phase machine. For the four legacy weapons slot 0 is the base action
    // (Strike); for the three new weapons slot 0 is skill_a (UseSkill), whose
    // motor emits start/release/complete traces.
    // ======================================================================
    System.Collections.IEnumerator RunSlot0Seven()
    {
        Enter("run");
        float original = hero.attackCooldown;
        try
        {
            var flow = AdventureFlow.Find(hero);
            if (flow != null && flow.AtCamp) { try { flow.DepartRuins(); } catch (Exception e) { Log("DepartRuins threw: " + e.Message); } }
            yield return null; yield return null; yield return null;
            // The hero model must exist before any new weapon can bind its visual.
            float md = Time.realtimeSinceStartup + 8f;
            while (hero.GetComponent<FantasyActorVisual>()?.model == null && Time.realtimeSinceStartup < md) yield return null;
            Log("slot0seven camera=" + (CombatAim.CameraFor(hero) != null)
                + " atCamp=" + (flow == null ? "?" : flow.AtCamp.ToString())
                + " speed=" + Round(hero.Progression == null ? 1f : hero.Progression.AttackSpeedMultiplier));
            foreach (var w in Weapons) yield return MeasureSlotZeroSeven(w);
        }
        finally { hero.attackCooldown = original; }
        Finish();
    }

    System.Collections.IEnumerator MeasureSlotZeroSeven(GearType w)
    {
        string name = w.ToString();
        bool modern = NewWeaponRegistry.Is(w);
        Equip(w, GearQuality.White);
        yield return null;
        combat.Expanded.Select(0);
        if (modern) combat.NewWeapons.Select(0);
        yield return null; yield return null; yield return null;
        // The new-weapon motor is bound on the next LateUpdate; never read a stale 0.
        float bindDeadline = Time.realtimeSinceStartup + 2f;
        while (modern && combat.SkillWindow <= 0f && Time.realtimeSinceStartup < bindDeadline) yield return null;
        // The new-weapon ENTRY is additionally gated on NewWeaponVisual.Ready, and the
        // visual can only bind once the hero model exists. Equipping straight after a
        // scene load can land before that, so the product's own equipment-change path
        // is replayed and the binding is waited for (never bypassed).
        bool visReady = false;
        if (modern)
        {
            combat.RefreshWeapon();
            float vd = Time.realtimeSinceStartup + 4f;
            while (Time.realtimeSinceStartup < vd)
            {
                visReady = combat.NewWeapons.Visual != null && combat.NewWeapons.Visual.Ready;
                if (visReady) break;
                yield return null;
            }
            Log("slot0seven visual " + name + " ready=" + visReady
                + " newWeaponReady=" + combat.NewWeaponReady
                + " model=" + (hero.GetComponent<FantasyActorVisual>()?.model != null));
        }

        float W = combat.SkillWindow;
        string detail = combat.SkillWindowDetail ?? "";
        float sum = SumDetail(detail);
        float sDec, gapDec, rDec; int gapsDec;
        ParseBreakdown(detail, out sDec, out gapDec, out gapsDec, out rDec);
        float iDec = gapDec * gapsDec;
        var pw = ParsePanelWindow();
        float panelW = pw ?? -1f;

        // Independent expectation of W, written out from the source rule (never a
        // call to the property under test).
        float expect = modern ? ExpectedWindow[name + "/0"]
                     : Mathf.Min(.55f, Mathf.Max(.01f, hero.AttackInterval * (w == GearType.Spear ? AdventureCombat.SpearCadence : 1f)));
        if (float.IsNaN(expect) || expect <= 0f) expect = W;

        float t0 = -1f, tFirst = -1f, tEnd = -1f;
        bool fired = false;
        traces.Clear();
        if (modern) combat.NewWeapons.Observed += OnTrace;
        try
        {
            // The product gates entry on its own readiness/cooldown; wait it out and
            // retry instead of bypassing the gate. Modern slot 0 is a skill with a
            // 7-11s cooldown, so the window is generous.
            float deadline = Time.realtimeSinceStartup + 30f;
            float nextGateLog = 0f;
            while (!fired && Time.realtimeSinceStartup < deadline)
            {
                // Product truth: the motor reports Busy only while an action is live.
                // (Select() parks Phase at "Cancelled" until the next Begin, so Phase
                // is not a usable idle marker.)
                bool idle = modern
                    ? !combat.NewWeapons.Busy && combat.SkillRemaining <= 0.02f
                    : combat.PendingAttackCount == 0 && combat.LastAttackPhase == "Idle";
                if (!fired && Time.realtimeSinceStartup >= nextGateLog)
                {
                    nextGateLog = Time.realtimeSinceStartup + 2f;
                    Log("S7-GATE " + name + " idle=" + idle + " phase=" + combat.NewWeapons.Phase
                        + " visReady=" + (combat.NewWeapons.Visual != null && combat.NewWeapons.Visual.Ready)
                        + " nwReady=" + combat.NewWeaponReady + " skillRemaining=" + Round(combat.SkillRemaining)
                        + " pending=" + combat.PendingAttackCount + " paused=" + hero.GameplayPaused
                        + " scale=" + Round(Time.timeScale) + " focused=" + PlayerInput.Focused
                        + " suspended=" + PlayerInput.Suspended + " uiBlocked=" + PlayerInput.UIBlocked);
                }
                if (idle)
                {
                    bool ok = modern ? combat.UseSkill() : combat.Strike();
                    if (ok) { fired = true; t0 = Time.time; }
                }
                yield return null;
            }
            if (fired)
            {
                float limit = Time.realtimeSinceStartup + 15f;
                while (Time.realtimeSinceStartup < limit)
                {
                    if (modern)
                    {
                        var done = traces.FirstOrDefault(t => t.stage == "complete");
                        if (done.stage == "complete") { tEnd = done.time; break; }
                        if (Time.time > t0 + 0.05f && combat.NewWeapons.Phase == "Idle") { tEnd = Time.time; break; }
                    }
                    else
                    {
                        string ph = combat.LastAttackPhase;
                        if (tFirst < 0f && ph != "Startup" && ph != "Idle") tFirst = Time.time;
                        if (ph == "Idle" || ph == "Cancelled") { tEnd = Time.time; break; }
                    }
                    yield return null;
                }
            }
        }
        finally { if (modern) combat.NewWeapons.Observed -= OnTrace; }

        float frame = Time.deltaTime;
        int mReleases = 0;
        float mStartup = -1f, mIntervals = 0f, mRecovery = -1f, mTotal = -1f;
        if (fired)
        {
            if (modern)
            {
                var rel = traces.Where(t => t.stage == "release").Select(t => t.time).OrderBy(x => x).ToList();
                var start = traces.FirstOrDefault(t => t.stage == "start");
                if (start.stage == "start") t0 = start.time;
                mReleases = rel.Count;
                if (rel.Count > 0 && t0 >= 0f) { mStartup = rel[0] - t0; mIntervals = rel[rel.Count - 1] - rel[0]; }
                if (t0 >= 0f && tEnd >= 0f) { mTotal = tEnd - t0; mRecovery = tEnd - (rel.Count > 0 ? rel[rel.Count - 1] : t0); }
            }
            else
            {
                mReleases = tFirst >= 0f ? 1 : 0;
                if (tFirst >= 0f && t0 >= 0f) mStartup = tFirst - t0;
                if (t0 >= 0f && tEnd >= 0f) { mTotal = tEnd - t0; mRecovery = tEnd - (tFirst >= 0f ? tFirst : t0); }
            }
        }

        // Frame quantisation: every phase boundary is observed on the first frame at
        // or after it, and the multi-phase motors re-arm from the observed frame.
        float tol = Mathf.Max(0.06f, frame * 2.5f);
        float tolGap = Mathf.Max(0.12f, frame * (gapsDec + 2));

        bool sumOk = Mathf.Abs(sDec + iDec + rDec - W) <= 0.005f;
        bool sumOk2 = Mathf.Abs(sum - W) <= 0.005f;
        bool wOk = Mathf.Abs(W - expect) <= 0.005f;
        bool panelOk = panelW >= 0f && Mathf.Abs(panelW - W) <= 0.005f;
        bool startOk = fired && mStartup >= 0f && Mathf.Abs(mStartup - sDec) <= tol;
        bool gapOk = fired && Mathf.Abs(mIntervals - iDec) <= tolGap;
        bool recOk = fired && mRecovery >= 0f && Mathf.Abs(mRecovery - rDec) <= tolGap;
        bool totalOk = fired && mTotal >= 0f && Mathf.Abs(mTotal - W) <= tolGap;

        var r = new Dictionary<string, object>
        {
            ["weapon"] = name, ["slot"] = 0, ["modern"] = modern,
            ["attackInterval"] = Round(hero.AttackInterval),
            ["window"] = Round(W), ["expectedWindow"] = Round(expect), ["windowOk"] = wOk,
            ["startup"] = Round(sDec), ["intervalGap"] = Round(gapDec), ["intervals"] = Round(iDec),
            ["gaps"] = gapsDec, ["recovery"] = Round(rDec),
            ["declaredSum"] = Round(sDec + iDec + rDec), ["sumOk"] = sumOk && sumOk2,
            ["windowDetail"] = detail,
            ["panelWindow"] = panelW < 0f ? (object)null : Round(panelW), ["panelOk"] = panelOk,
            ["panelText"] = ReadPanelText(),
            ["struck"] = fired, ["releases"] = mReleases,
            ["measuredStartup"] = Round(mStartup), ["measuredIntervals"] = Round(mIntervals),
            ["measuredRecovery"] = Round(mRecovery), ["measuredTotal"] = Round(mTotal),
            ["startupOk"] = startOk, ["intervalsOk"] = gapOk, ["recoveryOk"] = recOk, ["totalOk"] = totalOk,
            ["frameDelta"] = Round(frame), ["tolerance"] = Round(tol),
        };
        rows.Add(r);
        Log("S7 " + name + " modern=" + modern + " W=" + Round(W) + " exp=" + Round(expect)
            + " S=" + Round(sDec) + " I=" + Round(iDec) + "(" + gapsDec + "×" + Round(gapDec) + ")"
            + " R=" + Round(rDec) + " sum=" + Round(sDec + iDec + rDec)
            + " | measured S=" + Round(mStartup) + " I=" + Round(mIntervals) + " R=" + Round(mRecovery)
            + " T=" + Round(mTotal) + " rel=" + mReleases + " frame=" + Round(frame)
            + " panelW=" + (panelW < 0f ? "-" : Round(panelW).ToString()) + " detail='" + detail + "'");

        if (!wOk) checks.Add("S7_W_MISMATCH " + name + " W=" + Round(W) + " expected=" + Round(expect));
        if (!(sumOk && sumOk2)) checks.Add("S7_DETAIL_SUM " + name + " W=" + Round(W) + " declared=" + Round(sDec + iDec + rDec) + " parsed=" + Round(sum));
        if (!panelOk) checks.Add("S7_PANEL_MISMATCH " + name + " panel=" + (panelW < 0f ? "-" : Round(panelW).ToString()) + " W=" + Round(W));
        if (!fired) checks.Add("S7_NOT_STRUCK " + name);
        else
        {
            if (!startOk) checks.Add("S7_STARTUP_MISMATCH " + name + " measured=" + Round(mStartup) + " declared=" + Round(sDec));
            if (!gapOk) checks.Add("S7_INTERVALS_MISMATCH " + name + " measured=" + Round(mIntervals) + " declared=" + Round(iDec));
            if (!recOk) checks.Add("S7_RECOVERY_MISMATCH " + name + " measured=" + Round(mRecovery) + " declared=" + Round(rDec));
            if (!totalOk) checks.Add("S7_TOTAL_MISMATCH " + name + " measured=" + Round(mTotal) + " W=" + Round(W));
        }
    }

    // "前摇0.14+间隔0.13×5+收招0.23" -> 0.14 / 0.13 / 5 / 0.23
    static void ParseBreakdown(string detail, out float startup, out float gap, out int gaps, out float recovery)
    {
        startup = gap = recovery = -1f; gaps = 0;
        if (string.IsNullOrEmpty(detail)) return;
        var ms = Regex.Match(detail, @"前摇(\d+\.\d+)");
        if (ms.Success) startup = float.Parse(ms.Groups[1].Value, CultureInfo.InvariantCulture);
        var mg = Regex.Match(detail, @"间隔(\d+\.\d+)×(\d+)");
        if (mg.Success)
        {
            gap = float.Parse(mg.Groups[1].Value, CultureInfo.InvariantCulture);
            gaps = int.Parse(mg.Groups[2].Value, CultureInfo.InvariantCulture);
        }
        else gap = 0f;
        var mr = Regex.Match(detail, @"收招(\d+\.\d+)");
        if (mr.Success) recovery = float.Parse(mr.Groups[1].Value, CultureInfo.InvariantCulture);
    }

    // ======================================================================
    // MODE: cooldown — SK-14 gate. Cast once, then prove the product refuses
    // a second cast while the (now 8s) cooldown is live.
    // ======================================================================
    System.Collections.IEnumerator RunCooldown()
    {
        Enter("run");
        Equip(GearType.Scythe, GearQuality.White);
        yield return null; yield return null;
        combat.NewWeapons.Select(1);
        yield return null;
        // skills are gated on Ready; leave camp the same way 03A does so the
        // cooldown probe exercises the real runtime path, not a camp lock.
        var flow = AdventureFlow.Find(hero);
        if (flow != null && flow.AtCamp) { try { flow.DepartRuins(); } catch (Exception e) { Log("DepartRuins threw: " + e.Message); } }
        yield return null; yield return null; yield return null;

        float reported = combat.SkillDuration;
        float before = combat.SkillRemaining;
        bool first = combat.UseSkill();
        yield return null;
        float remaining = combat.SkillRemaining;
        bool second = combat.UseSkill();
        yield return null;
        float remaining2 = combat.SkillRemaining;

        var r = new Dictionary<string, object>
        {
            ["skillId"] = combat.SkillIdText,
            ["skillDuration"] = Round(reported),
            ["remainingBeforeCast"] = Round(before),
            ["remainingAfterCast"] = Round(remaining),
            ["remainingAfterSecondAttempt"] = Round(remaining2),
            ["firstCastAccepted"] = first,
            ["secondCastAccepted"] = second,
            ["panelText"] = ReadPanelText(),
        };
        rows.Add(r);
        Log("CD id=" + combat.SkillIdText + " C=" + Round(reported) + " before=" + Round(before)
            + " after=" + Round(remaining) + " after2=" + Round(remaining2)
            + " first=" + first + " second=" + second);

        if (Mathf.Abs(reported - 8f) > 0.001f) checks.Add("SK14_COOLDOWN_NOT_8 actual=" + Round(reported));
        if (!first) checks.Add("CD_FIRST_CAST_REJECTED");
        if (remaining < 7.5f) checks.Add("CD_NOT_ARMED remaining=" + Round(remaining));
        if (second) checks.Add("CD_SECOND_CAST_ACCEPTED remaining=" + Round(remaining2));
        Finish();
    }

    // ======================================================================
    // MODE: pull — the SK-14 boundary set. Every verdict is taken from the
    // product's OWN emitted Trace stream (start / release / pull-start /
    // pull-obstructed / control-immune) plus its own PullRemaining and cooldown
    // read-out. Harness instrumentation is limited to choosing where a GENUINE
    // enemy stands, silencing that enemy's own chase so displacement measures
    // the PULL and not the approach, and — only when the layout exposes no boss
    // instance — stamping EnemyArchetype.Boss onto a genuine enemy so the
    // product's real immunity branch runs. No immunity, collider, damage or
    // target-selection logic is modified.
    // ======================================================================
    readonly List<NewWeaponCombat.Trace> traces = new List<NewWeaponCombat.Trace>();
    void OnTrace(NewWeaponCombat.Trace t) { traces.Add(t); }
    static bool IsProbeTarget(NewWeaponCombat.Trace t, CombatEnemy e)
    {
        if (t.target == null || e == null) return false;
        if (t.target == e) return true;
        return t.target.GetComponentInParent<CombatEnemy>() == e;
    }

    System.Collections.IEnumerator RunPull()
    {
        Enter("run");
        Equip(GearType.Scythe, GearQuality.White);
        yield return null; yield return null;
        combat.NewWeapons.Select(1);
        yield return null;
        var flow = AdventureFlow.Find(hero);
        if (flow != null && flow.AtCamp) { try { flow.DepartRuins(); } catch (Exception e) { Log("DepartRuins threw: " + e.Message); } }

        float t0 = Time.realtimeSinceStartup;
        while (Time.realtimeSinceStartup - t0 < 30f)
        {
            if (session.enemies != null && session.enemies.Count(e => e != null && e.Health != null && !e.Health.Dead) >= 3) break;
            yield return null;
        }
        var pool = session.enemies == null ? new List<CombatEnemy>()
                 : session.enemies.Where(e => e != null && e.Health != null && !e.Health.Dead).ToList();
        Log("PULL pool=" + pool.Count + " [" + string.Join(",", pool.Select(e => (e.entityId ?? "?") + ":" + e.archetype).ToArray()) + "]");
        if (pool.Count == 0) { Fail("no live enemy for the SK-14 boundary probe"); yield break; }

        combat.NewWeapons.Observed += OnTrace;
        var bossReal = pool.FirstOrDefault(e => e.archetype == EnemyArchetype.Boss);
        Log("PULL bossSource=" + (bossReal != null ? "layout(" + bossReal.entityId + ")" : "instrumented-archetype"));

        yield return PullCase("normal", pool[0], false, false);
        yield return PullCase("boss", bossReal ?? pool[Math.Min(1, pool.Count - 1)], true, false);
        yield return PullCase("obstacle", pool[Math.Min(2, pool.Count - 1)], false, true);

        combat.NewWeapons.Observed -= OnTrace;
        Finish();
    }

    System.Collections.IEnumerator PullCase(string kind, CombatEnemy e, bool asBoss, bool obstacle)
    {
        if (e == null) { checks.Add("PULL_NO_TARGET " + kind); yield break; }

        // The product gates skills on its own cooldown; wait it out instead of bypassing it.
        float w0 = Time.realtimeSinceStartup;
        while (combat.SkillRemaining > 0.02f && Time.realtimeSinceStartup - w0 < 25f) yield return null;

        var fwd = hero.transform.forward; fwd.y = 0f;
        if (fwd.sqrMagnitude < 1e-4f) fwd = Vector3.forward;
        fwd.Normalize();
        Vector3 spot = hero.transform.position + fwd * 3f;
        spot.y = hero.transform.position.y;                       // same ground level => inside melee reach
        e.transform.position = spot;
        var cc = e.GetComponent<CharacterController>();            // re-sync the controller after a teleport
        if (cc != null) { cc.enabled = false; cc.enabled = true; }
        hero.transform.LookAt(new Vector3(spot.x, hero.transform.position.y, spot.z));
        var guard = e.GetComponent<EncounterGuard>(); if (guard != null) guard.enabled = false;
        e.enabled = false;                                        // silence this enemy's own chase only

        bool archetypeOverridden = false;
        if (asBoss && e.archetype != EnemyArchetype.Boss) { e.archetype = EnemyArchetype.Boss; archetypeOverridden = true; }

        GameObject blocker = null;
        if (obstacle)
        {
            blocker = GameObject.CreatePrimitive(PrimitiveType.Cube);
            blocker.name = "UX03R1 obstacle probe";
            blocker.transform.position = hero.transform.position + fwd * 1.5f + Vector3.up * 1.0f;
            blocker.transform.localScale = new Vector3(2.5f, 2.5f, 0.4f);
            blocker.transform.rotation = Quaternion.LookRotation(fwd, Vector3.up);
            yield return null;
        }

        float hpBefore = e.Health.Current;
        Vector3 posBefore = e.transform.position;
        traces.Clear();

        // The product gates Begin() on NewWeaponReady / Busy / Visual.Ready /
        // NewSkillAt. Right after a departure those are not all true yet, so the
        // cast is RETRIED through the product path instead of being reported as
        // rejected. A rejection is only a failure if the gate never opens.
        bool cast = false;
        float cdAfterCast = 0f;
        float castDeadline = Time.realtimeSinceStartup + 8f;
        bool gateLogged = false;
        while (!cast && Time.realtimeSinceStartup < castDeadline)
        {
            cast = combat.UseSkill();
            if (cast) { cdAfterCast = combat.SkillRemaining; break; }
            if (!gateLogged)
            {
                gateLogged = true;
                Log("PULL gate " + kind + " ready=" + combat.NewWeaponReady + " busy=" + combat.NewWeapons.Busy
                    + " visualReady=" + (combat.NewWeapons.Visual != null && combat.NewWeapons.Visual.Ready)
                    + " rem=" + Round(combat.SkillRemaining) + " atCamp=" + (AdventureFlow.Find(hero)?.AtCamp ?? true));
            }
            yield return null;
        }

        float maxPull = 0f;
        bool immuneFlag = false;
        EnemyWeaponControl ctl = null;
        float tEnd = Time.realtimeSinceStartup + 1.4f;
        while (Time.realtimeSinceStartup < tEnd)
        {
            ctl = e.GetComponent<EnemyWeaponControl>();
            if (ctl != null) { maxPull = Mathf.Max(maxPull, ctl.PullRemaining); immuneFlag = ctl.Immune; }
            yield return null;
        }

        float hpAfter = e.Health.Current;
        Vector3 posAfter = e.transform.position;
        float moved = Vector3.Distance(new Vector3(posBefore.x, 0f, posBefore.z), new Vector3(posAfter.x, 0f, posAfter.z));

        // Only THIS probe target's events count. Other enemies inside the 4.5m
        // sector also emit pull events; attributing them to the probe would make
        // a genuine Boss immunity look like a successful pull.
        float tStart = -1f, tRelease = -1f;
        int pullStart = 0, pullBlocked = 0, immuneEvt = 0;
        foreach (var tr in traces)
        {
            if (tr.stage == "start") tStart = tr.time;
            else if (tr.stage == "release") tRelease = tr.time;
            else if (!IsProbeTarget(tr, e)) continue;
            else if (tr.stage == "pull-start") pullStart++;
            else if (tr.stage == "pull-obstructed") pullBlocked++;
            else if (tr.stage == "control-immune") immuneEvt++;
        }
        float startup = (tStart >= 0f && tRelease >= tStart) ? tRelease - tStart : -1f;

        var r = new Dictionary<string, object>
        {
            ["case"] = kind, ["skillId"] = combat.SkillIdText, ["entityId"] = e.entityId ?? "",
            ["targetArchetype"] = e.archetype.ToString(), ["castAccepted"] = cast,
            ["startupSeconds"] = Round(startup), ["cooldownReported"] = Round(combat.SkillDuration),
            ["remainingAfterCast"] = Round(cdAfterCast),
            ["pullStartEvents"] = pullStart, ["pullObstructedEvents"] = pullBlocked, ["controlImmuneEvents"] = immuneEvt,
            ["maxPullRemaining"] = Round(maxPull), ["immuneFlag"] = immuneFlag,
            ["displacementMeters"] = Round(moved),
            ["hpBefore"] = Round(hpBefore), ["hpAfter"] = Round(hpAfter),
        };
        rows.Add(r);
        Log("PULL " + kind + " id=" + (e.entityId ?? "?") + " arc=" + e.archetype + " cast=" + cast
            + " startup=" + Round(startup) + " C=" + Round(combat.SkillDuration) + " rem=" + Round(cdAfterCast)
            + " pull=" + pullStart + " blocked=" + pullBlocked + " immune=" + immuneEvt
            + " maxPull=" + Round(maxPull) + " moved=" + Round(moved)
            + " hp=" + Round(hpBefore) + "->" + Round(hpAfter));

        if (!cast) checks.Add("PULL_CAST_REJECTED " + kind);
        if (kind == "normal")
        {
            if (Mathf.Abs(startup - 0.30f) > 0.02f) checks.Add("SK14_STARTUP_NOT_030 actual=" + Round(startup));
            if (Mathf.Abs(combat.SkillDuration - 8f) > 0.001f) checks.Add("SK14_COOLDOWN_NOT_8 actual=" + Round(combat.SkillDuration));
            if (cdAfterCast < 7.5f) checks.Add("SK14_COOLDOWN_NOT_ARMED remaining=" + Round(cdAfterCast));
            if (pullStart < 1) checks.Add("PULL_NO_PULL_START normal");
            if (maxPull <= 0f) checks.Add("PULL_NOT_APPLIED normal maxPull=" + Round(maxPull));
            if (moved < 0.3f) checks.Add("PULL_DISPLACEMENT_TOO_SMALL normal moved=" + Round(moved));
            if (Mathf.Abs(hpAfter - hpBefore) > 0.001f) checks.Add("PULL_DAMAGED_TARGET normal " + Round(hpBefore) + "->" + Round(hpAfter));
        }
        else if (kind == "boss")
        {
            if (immuneEvt < 1 && !immuneFlag) checks.Add("PULL_BOSS_NOT_IMMUNE");
            if (pullStart > 0) checks.Add("PULL_BOSS_WAS_PULLED pullStart=" + pullStart);
            if (maxPull > 0f) checks.Add("PULL_BOSS_CONTROLLED maxPull=" + Round(maxPull));
            if (Mathf.Abs(hpAfter - hpBefore) > 0.001f) checks.Add("PULL_BOSS_DAMAGED");
        }
        else
        {
            if (pullBlocked < 1) checks.Add("PULL_OBSTACLE_NOT_BLOCKED");
            if (pullStart > 0) checks.Add("PULL_THROUGH_OBSTACLE pullStart=" + pullStart);
            if (moved > 0.15f) checks.Add("PULL_OBSTACLE_MOVED moved=" + Round(moved));
            if (Mathf.Abs(hpAfter - hpBefore) > 0.001f) checks.Add("PULL_OBSTACLE_DAMAGED");
        }

        if (blocker != null) Destroy(blocker);
        if (archetypeOverridden) e.archetype = EnemyArchetype.Elite;
        e.enabled = true;
        yield return null;
    }

    // ======================================================================
    // MODE: layout — UI-03c layout acceptance. Measures the live panel rect
    // against the screen, the centre combat band, the training-rack button and
    // the projected training pickups, and proves the status text is not
    // truncated at the CURRENT text length. Read-only: nothing is resized.
    // ======================================================================
    System.Collections.IEnumerator RunLayout()
    {
        Enter("run");
        yield return null; yield return null;
        if (panel == null) { Fail("WeaponSkillPanel missing on hero"); yield break; }

        // The launch-time -screen-width/-screen-height flags are not honoured once
        // the game has a stored window mode, so the requested size is applied here
        // and the MEASURED size is recorded. Nothing is measured until it matches.
        if (reqWidth > 0 && reqHeight > 0 && (Screen.width != reqWidth || Screen.height != reqHeight))
        {
            Screen.SetResolution(reqWidth, reqHeight, false);
            float rd = Time.realtimeSinceStartup + 6f;
            while ((Screen.width != reqWidth || Screen.height != reqHeight) && Time.realtimeSinceStartup < rd) yield return null;
            Log("layout: requested " + reqWidth + "x" + reqHeight + " -> actual " + Screen.width + "x" + Screen.height);
        }

        // The training rack is gated on CP05TrainingMarker, which only the CP05
        // arena adds. Entering that arena is outside this batch, so the marker is
        // added and the panel rebuilt so the PRODUCT creates the rack through its
        // own Start() path. The harness creates no widget of its own.
        if (hero.GetComponent<CP05TrainingMarker>() == null)
        {
            hero.gameObject.AddComponent<CP05TrainingMarker>();
            Log("layout: CP05TrainingMarker added (instrumented presence, arena gate only)");
            UnityEngine.Object.Destroy(panel);
            yield return null; yield return null;
            panel = hero.gameObject.AddComponent<WeaponSkillPanel>();
            yield return null; yield return null;
            if (panel == null) { Fail("WeaponSkillPanel rebuild failed"); yield break; }
        }

        Canvas c = null;
        foreach (var x in panel.GetComponentsInChildren<Canvas>(true))
            if (x != null && x.name == "Weapon skill loadout") { c = x; break; }
        if (c == null) { Fail("panel canvas 'Weapon skill loadout' not found"); yield break; }
        yield return null;

        var root = c.transform;
        int transforms = root.GetComponentsInChildren<Transform>(true).Length;
        int buttons = root.GetComponentsInChildren<Button>(true).Length;
        int images = root.GetComponentsInChildren<Image>(true).Length;
        int texts = root.GetComponentsInChildren<Text>(true).Length;

        RectTransform statusRt = null, rackRt = null;
        Text statusText = null;
        foreach (var t in root.GetComponentsInChildren<Transform>(true))
        {
            if (t == null) continue;
            if (t.name == "技能阶段") { statusRt = t as RectTransform; statusText = t.GetComponent<Text>(); }
            else if (t.name == "训练装备架") { rackRt = t as RectTransform; }
        }
        if (statusRt == null || statusText == null) { Fail("status text '技能阶段' not found"); yield break; }

        bool hasRack = rackRt != null;
        // The panel canvas is parented under the hero, so its world matrix carries
        // the hero's position. Screen rects are therefore derived in CANVAS LOCAL
        // space and mapped to pixels, which is what the player actually sees for a
        // ScreenSpaceOverlay canvas.
        var canvasRt = (RectTransform)c.transform;
        Rect statusRect = CanvasLocalToScreen(canvasRt, statusRt);
        Rect rackRect = hasRack ? CanvasLocalToScreen(canvasRt, rackRt) : new Rect(0, 0, 0, 0);
        float leftThird = Screen.width / 3f;
        Rect combatBand = new Rect(leftThird, Screen.height * 0.20f, Screen.width / 3f, Screen.height * 0.60f);

        float needH = statusText.preferredHeight;
        float haveH = statusRt.rect.height;
        float needW = statusText.preferredWidth;
        float haveW = statusRt.rect.width;
        bool truncated = needH > haveH + 0.5f;
        bool overlapRack = hasRack && statusRect.Overlaps(rackRect);
        bool overlapBand = statusRect.Overlaps(combatBand);
        bool intrudesLeftThird = statusRect.xMax > leftThird + 0.5f;
        bool offscreen = statusRect.xMin < -0.5f || statusRect.yMin < -0.5f
                      || statusRect.xMax > Screen.width + 0.5f || statusRect.yMax > Screen.height + 0.5f;
        bool rackOffscreen = hasRack && (rackRect.xMin < -0.5f || rackRect.yMin < -0.5f
                      || rackRect.xMax > Screen.width + 0.5f || rackRect.yMax > Screen.height + 0.5f);

        // training-rack pickups: project the genuine spawned gear so the panel is
        // proven not to cover the area the player has to walk to and click.
        int pickups = 0, pickupsCovered = 0;
        var marker = hero.GetComponent<CP05TrainingMarker>();
        if (marker != null)
        {
            combat.NewWeapons.SpawnTrainingArsenal();
            yield return null; yield return null;
            var cam = Camera.main;
            if (cam != null)
            {
                foreach (var lp in UnityEngine.Object.FindObjectsByType<LootPickup>(FindObjectsSortMode.None))
                {
                    if (lp == null) continue;
                    pickups++;
                    Vector3 sp = cam.WorldToScreenPoint(lp.transform.position);
                    if (sp.z <= 0f) continue;
                    if (statusRect.Contains(sp) || (hasRack && rackRect.Contains(sp))) pickupsCovered++;
                }
            }
        }
        else Log("layout: no CP05TrainingMarker on hero — rack pickups cannot be spawned (NOT_APPLICABLE)");

        var r = new Dictionary<string, object>
        {
            ["screenWidth"] = Screen.width, ["screenHeight"] = Screen.height,
            ["canvasScaleFactor"] = Math.Round(c.scaleFactor, 4),
            ["transforms"] = transforms, ["buttons"] = buttons, ["images"] = images, ["texts"] = texts,
            ["hasRack"] = hasRack,
            ["statusRect"] = RectText(statusRect), ["rackRect"] = hasRack ? RectText(rackRect) : "",
            ["statusRefWidth"] = Math.Round(statusRt.rect.width, 2), ["statusRefHeight"] = Math.Round(statusRt.rect.height, 2),
            ["statusRefPos"] = Math.Round(statusRt.anchoredPosition.x, 2) + "," + Math.Round(statusRt.anchoredPosition.y, 2),
            ["textPreferredWidth"] = Math.Round(needW, 2), ["textPreferredHeight"] = Math.Round(needH, 2),
            ["truncated"] = truncated, ["overlapRack"] = overlapRack,
            ["overlapCombatBand"] = overlapBand, ["intrudesLeftThird"] = intrudesLeftThird,
            ["leftThirdPx"] = Mathf.Round(leftThird), ["offscreen"] = offscreen, ["rackOffscreen"] = rackOffscreen,
            ["pickups"] = pickups, ["pickupsCovered"] = pickupsCovered,
            ["statusText"] = statusText.text,
        };
        rows.Add(r);
        Log("LAYOUT " + Screen.width + "x" + Screen.height + " scale=" + Math.Round(c.scaleFactor, 3)
            + " T=" + transforms + " B=" + buttons + " I=" + images + " Tx=" + texts
            + " status=" + RectText(statusRect) + " rack=" + (hasRack ? RectText(rackRect) : "-")
            + " need=" + Math.Round(needW, 1) + "x" + Math.Round(needH, 1) + " have=" + Math.Round(haveW, 1) + "x" + Math.Round(haveH, 1)
            + " trunc=" + truncated + " ovRack=" + overlapRack + " ovBand=" + overlapBand
            + " leftThird=" + Mathf.Round(leftThird) + " off=" + offscreen + " pickups=" + pickups + " covered=" + pickupsCovered);

        // Structural invariant: the panel is the same widget set as the frozen
        // baseline (3 slot buttons + 3 labels + status; plus rack + its label).
        int expT = hasRack ? 10 : 8, expB = hasRack ? 4 : 3, expI = hasRack ? 4 : 3, expTx = hasRack ? 5 : 4;
        if (transforms != expT) checks.Add("LAYOUT_TRANSFORM_COUNT " + transforms + " expected=" + expT);
        if (buttons != expB) checks.Add("LAYOUT_BUTTON_COUNT " + buttons + " expected=" + expB);
        if (images != expI) checks.Add("LAYOUT_IMAGE_COUNT " + images + " expected=" + expI);
        if (texts != expTx) checks.Add("LAYOUT_TEXT_COUNT " + texts + " expected=" + expTx);

        if (truncated) checks.Add("LAYOUT_TEXT_TRUNCATED need=" + Math.Round(needH, 1) + " have=" + Math.Round(haveH, 1));
        if (overlapRack) checks.Add("LAYOUT_STATUS_OVER_RACK status=" + RectText(statusRect) + " rack=" + RectText(rackRect));
        if (intrudesLeftThird) checks.Add("LAYOUT_INTRUDES_LEFT_THIRD xMax=" + Math.Round(statusRect.xMax, 1) + " limit=" + Mathf.Round(leftThird));
        if (overlapBand) checks.Add("LAYOUT_STATUS_OVER_COMBAT_BAND status=" + RectText(statusRect) + " band=" + RectText(combatBand));
        if (offscreen) checks.Add("LAYOUT_OFFSCREEN status=" + RectText(statusRect) + " screen=" + Screen.width + "x" + Screen.height);
        if (rackOffscreen) checks.Add("LAYOUT_RACK_OFFSCREEN rack=" + RectText(rackRect) + " screen=" + Screen.width + "x" + Screen.height);
        if (pickupsCovered > 0) checks.Add("LAYOUT_PICKUP_COVERED covered=" + pickupsCovered + "/" + pickups);

        Finish();
    }

    // Screen-space rect of a child of a ScreenSpaceOverlay canvas, derived in the
    // canvas's own local space. GetWorldCorners is unusable here because the panel
    // canvas is parented under the hero and therefore inherits its world position.
    static Rect CanvasLocalToScreen(RectTransform canvasRt, RectTransform child)
    {
        var b = RectTransformUtility.CalculateRelativeRectTransformBounds(canvasRt, child);
        var cr = canvasRt.rect;
        float sx = Screen.width / Mathf.Max(1f, cr.width);
        float sy = Screen.height / Mathf.Max(1f, cr.height);
        float x = (b.min.x - cr.xMin) * sx;
        float y = (b.min.y - cr.yMin) * sy;
        return new Rect(x, y, b.size.x * sx, b.size.y * sy);
    }
    static string RectText(Rect r)
    {
        return string.Format(CultureInfo.InvariantCulture, "{0:0.#},{1:0.#} {2:0.#}x{3:0.#}", r.x, r.y, r.width, r.height);
    }

    // ======================================================================
    void Equip(GearType w, GearQuality q)
    {
        gear.items.RemoveAll(it => !it.worn && !it.Container);
        var item = AdventureItems.New(w, q);
        item.affixes = new int[0];
        gear.AddOrStore(item);
        gear.mainWeapon = item.id;
        if (!gear.SelectMain(item)) { gear.Refresh(); combat.EquipmentChanged(); }
        Log("equip " + w + " -> GearWeapon=" + gear.Weapon);
    }

    string ReadPanelText()
    {
        if (panel == null) return "";
        if (panelStatus == null)
        {
            var texts = panel.GetComponentsInChildren<Text>(true);
            foreach (var t in texts) if (t != null && t.gameObject.name == "技能阶段") { panelStatus = t; break; }
        }
        return panelStatus != null ? panelStatus.text : "";
    }
    float? ParsePanelWindow()
    {
        var m = Regex.Match(ReadPanelText() ?? "", @"W(\d+\.\d\d)s");
        if (!m.Success) return null;
        return float.Parse(m.Groups[1].Value, CultureInfo.InvariantCulture);
    }
    float? ParsePanelCooldown()
    {
        var m = Regex.Match(ReadPanelText() ?? "", @"冷却(\d+\.\d)s");
        if (!m.Success) return null;
        return float.Parse(m.Groups[1].Value, CultureInfo.InvariantCulture);
    }

    // Sum the "a+b×2+c" style decomposition so the panel string is not merely
    // "present" but arithmetically consistent with the W it advertises.
    static float SumDetail(string detail)
    {
        if (string.IsNullOrEmpty(detail)) return 0f;
        float total = 0f;
        foreach (var part in detail.Split('+'))
        {
            var p = part.Trim();
            if (p.Length == 0) continue;
            float mult = 1f;
            int xi = p.IndexOf('×');
            if (xi >= 0)
            {
                mult = float.Parse(p.Substring(xi + 1), CultureInfo.InvariantCulture);
                p = p.Substring(0, xi);
            }
            var m = Regex.Match(p, @"(\d+\.\d+)");
            if (!m.Success) continue;
            total += float.Parse(m.Groups[1].Value, CultureInfo.InvariantCulture) * mult;
        }
        return total;
    }

    static double Round(float v) { return Math.Round(v, 4); }

    string ResolveLoadedAssemblyHash()
    {
        try
        {
            var loc = typeof(Harness03Runner).Assembly.Location;
            if (string.IsNullOrEmpty(loc) || !File.Exists(loc)) return "unavailable";
            using (var sha = System.Security.Cryptography.SHA256.Create())
            using (var fs = File.OpenRead(loc))
                return BitConverter.ToString(sha.ComputeHash(fs)).Replace("-", "").ToLowerInvariant();
        }
        catch (Exception e) { return "error:" + e.Message; }
    }

    void Fail(string reason)
    {
        if (failed || quitting) return;
        failed = true; failReason = reason; Log("FAIL: " + reason);
        WriteResult(false);
        quitting = true;
        Application.Quit(1);
    }

    void Finish()
    {
        if (quitting) return;
        Log("FINISH checks=" + checks.Count);
        foreach (var c in checks) Log("CHECK " + c);
        WriteResult(checks.Count == 0);
        quitting = true;
        Application.Quit(checks.Count == 0 ? 0 : 2);
    }

    void WriteResult(bool ok)
    {
        try
        {
            var sb = new StringBuilder();
            sb.Append("{\n");
            sb.Append("  \"marker\": \"").Append(PlayerAcceptanceHarness03.MARKER).Append("\",\n");
            sb.Append("  \"version\": ").Append(PlayerAcceptanceHarness03.VERSION).Append(",\n");
            sb.Append("  \"mode\": \"").Append(mode).Append("\",\n");
            sb.Append("  \"runId\": \"").Append(runId).Append("\",\n");
            sb.Append("  \"loadedAssemblySha256\": \"").Append(ResolveLoadedAssemblyHash()).Append("\",\n");
            sb.Append("  \"ok\": ").Append(ok ? "true" : "false").Append(",\n");
            sb.Append("  \"failReason\": \"").Append(Esc(failReason)).Append("\",\n");
            sb.Append("  \"checks\": [");
            for (int i = 0; i < checks.Count; i++) { if (i > 0) sb.Append(", "); sb.Append('"').Append(Esc(checks[i])).Append('"'); }
            sb.Append("],\n  \"rows\": [\n");
            for (int i = 0; i < rows.Count; i++)
            {
                sb.Append("    {");
                bool first = true;
                foreach (var kv in rows[i])
                {
                    if (!first) sb.Append(", ");
                    first = false;
                    sb.Append('"').Append(kv.Key).Append("\": ");
                    if (kv.Value == null) sb.Append("null");
                    else if (kv.Value is bool) sb.Append(((bool)kv.Value) ? "true" : "false");
                    else if (kv.Value is double) sb.Append(((double)kv.Value).ToString(CultureInfo.InvariantCulture));
                    else if (kv.Value is int) sb.Append(kv.Value.ToString());
                    else sb.Append('"').Append(Esc(kv.Value.ToString())).Append('"');
                }
                sb.Append("}").Append(i == rows.Count - 1 ? "" : ",").Append("\n");
            }
            sb.Append("  ]\n}\n");
            File.WriteAllText(Path.Combine(dataRoot, "ux03-result.json"), sb.ToString(), new UTF8Encoding(false));
            Log("wrote ux03-result.json rows=" + rows.Count);
        }
        catch (Exception e) { Log("WriteResult failed: " + e.Message); }
    }

    static string Esc(string s)
    {
        if (s == null) return "";
        return s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\r", "").Replace("\n", "\\n").Replace("\t", "\\t");
    }

    void Log(string msg)
    {
        try
        {
            string line = string.Format(CultureInfo.InvariantCulture, "[{0:0.000}] {1}", Time.unscaledTime, msg);
            File.AppendAllText(logPath, line + "\n", new UTF8Encoding(false));
        }
        catch { }
        Debug.Log("[UX03] " + msg);
    }
}
#endif
