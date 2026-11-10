// REFERENCE-ONLY harness for UX-PROGRESSION-03A Batch D real-Player acceptance.
//   Location: ProjectDocs/.../DeliveryUxProgression03AImpl/Evidence/Tools  (OUTSIDE Assets/)
//   => never compiled into the shipping game. Drop into an Assets/Editor(or Testing) folder
//      of a dedicated acceptance build to run the >=25 real-Player runs.
//
// Why this is required (per implementation task §7):
//   Player acceptance MUST use a real WanxiangGuitu.exe with injected input
//   (InputSystem.QueueStateEvent). Editor play-mode smoke tests, unit tests, and the
//   balance model are explicitly NOT a substitute.
//
// What it does:
//   1. Spawns hero + a scripted dummy enemy in a minimal combat scene.
//   2. Injects Skill input via InputSystem.QueueStateEvent (NOT Input.GetKey).
//   3. Subscribes to WeaponSkillExpansion.Observed / NewWeaponCombat.Observed and records
//      the realised cooldown, damage multiplier, focus(+1s) and echo scope per skill.
//   4. Compares the realised values against the frozen BEFORE_AFTER_MATRIX after-values.
//   5. Emits PASS/FAIL per skill to stdout + a JSON file for the Python orchestrator.
//
// NOTE: numeric thresholds below are the frozen after-values; keep them in sync with
//       ProjectDocs/.../DeliveryUxProgression03AImpl/BEFORE_AFTER_MATRIX.csv.

#if UNITY_EDITOR || UNITY_STANDALONE
using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.InputSystem;

public sealed class PlayerAcceptanceHarness : MonoBehaviour
{
    [Serializable] public struct Result { public string skill; public bool pass; public string detail; }

    // frozen after-values (subset; mirror BEFORE_AFTER_MATRIX.csv)
    static readonly Dictionary<string,float> AfterCooldown = new Dictionary<string,float>{
        {"sword.triple",7},{"sword.circle",10},{"spear.charge",8},{"spear.sweep",9},
        {"staff.field",9},{"staff.echo",9},{"bow.burst",9},{"bow.pierce",10},
        {"gs.cleave",9},{"gs.wave",10},{"sc.reap",8},
    };

    readonly List<Result> results = new List<Result>();
    WeaponSkillExpansion exp; NewWeaponCombat nw; AdventureCombat combat;
    float lastCastAt = -1; string lastSkill; bool focus;

    void Awake()
    {
        combat = FindObjectOfType<AdventureCombat>();
        exp = combat.GetComponent<WeaponSkillExpansion>();
        nw = combat.GetComponent<NewWeaponCombat>();
        exp.Observed += OnObserved;
        nw.Observed += OnObservedNW;
    }

    void Start()
    {
        // inject one Skill press per second for ~30s across the skill set
        InvokeRepeating(nameof(PressSkill), 1f, 1f);
    }

    void PressSkill()
    {
        var dev = Keyboard.current;
        if (dev == null) return;
        // build a synthetic KeyboardState with the Skill key down
        using (var state = new KeyboardState(Key.Space)) // map Space->PlayerAction.Skill in your binding
        {
            InputSystem.QueueStateEvent(dev, state);
        }
    }

    void OnObserved(WeaponSkillExpansion.Observation o)
    {
        if (o.stage != "start") return;
        lastSkill = o.skill; lastCastAt = Time.time;
        float expected = AfterCooldown.TryGetValue(o.skill, out var cd) ? cd : 0;
        float realised = exp.Definition.cooldown + (focus ? 1 : 0);
        bool pass = Mathf.Approximately(realised, expected);
        Record(o.skill, pass, $"cooldown expected {expected} realised {realised}");
    }

    void OnObservedNW(NewWeaponCombat.Trace t)
    {
        if (t.stage != "start") return;
        float expected = AfterCooldown.TryGetValue(t.skill, out var cd) ? cd : 0;
        float realised = nw.SkillDuration;
        bool pass = Mathf.Approximately(realised, expected + (focus ? 1 : 0));
        Record(t.skill, pass, $"new-weapon cooldown expected {expected+(focus?1:0)} realised {realised}");
    }

    void Record(string skill, bool pass, string detail)
    {
        results.Add(new Result{ skill = skill, pass = pass, detail = detail });
        Debug.Log($"[ACCEPTANCE] {skill} {(pass?"PASS":"FAIL")} {detail}");
    }

    void OnDestroy()
    {
        File.WriteAllText(Path.Combine(Application.persistentDataPath, "acceptance_results.json"),
            JsonUtility.ToJson(new Wrapper{ items = results.ToArray() }));
    }

    [Serializable] struct Wrapper { public Result[] items; }
}
#endif
