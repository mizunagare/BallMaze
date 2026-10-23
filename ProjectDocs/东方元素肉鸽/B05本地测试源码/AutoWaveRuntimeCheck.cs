using System;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class AutoWaveRuntimeCheck
{
    static double deadline, began;
    static int phase, level;
    static float remaining;
    static CombatSession session;
    public static void Run()
    {
        EditorSceneManager.OpenScene("Assets/CombatPrototype/CombatPlayground.unity");
        deadline = EditorApplication.timeSinceStartup + 45;
        EditorApplication.update += Tick;
        EditorApplication.EnterPlaymode();
    }
    static void Require(bool value, string message) { if (!value) throw new Exception(message); }
    static void Resolve()
    {
        var p = session.hero.Progression;
        while (p.PendingChoices > 0) { p.BeginChoice(); Require(p.SelectChoice(0), "Choice queue stuck"); }
    }
    static void Tick()
    {
        try {
            if (EditorApplication.timeSinceStartup > deadline) throw new Exception("Auto wave check timed out");
            if (!EditorApplication.isPlaying || Time.time < .3f) return;
            session = UnityEngine.Object.FindFirstObjectByType<CombatSession>();
            if (session == null || session.Waves == null) return;
            var hero = session.hero;
            if (phase == 0) {
                Require(session.nextWaveDelay == 10, "Default intermission is not ten seconds");
                session.Restart();
                session.nextWaveDelay = 1.5f; // Exercise the same real Update path with a shorter test delay.
                foreach (var enemy in session.enemies) { enemy.Health.Damage(99999); enemy.DropLootOnce(); }
                Resolve();
                level = hero.Progression.Level;
                began = EditorApplication.timeSinceStartup;
                phase = 1;
                return;
            }
            if (phase == 1) {
                if (!session.WaitingForNextWave || session.NextWaveRemaining > 1.3f) return;
                Require(session.Wave == 1 && session.NextWaveRemaining > 0, "Countdown skipped intermission");
                hero.Inventory.SetOpen(true);
                remaining = session.NextWaveRemaining;
                began = EditorApplication.timeSinceStartup;
                phase = 2;
                return;
            }
            if (phase == 2) {
                if (EditorApplication.timeSinceStartup - began < .35) return;
                Require(Mathf.Abs(session.NextWaveRemaining - remaining) < .001f && session.CountdownPaused, "Backpack did not freeze countdown");
                hero.Inventory.Add(MaterialKind.MonsterHide, 2);
                hero.Inventory.Add(MaterialKind.CrystalShard, 1);
                Require(hero.Equipment.Craft(EquipmentKind.HideArmor), "Cannot craft during intermission");
                hero.Equipment.Equip(EquipmentKind.HideArmor, true);
                hero.Inventory.SetOpen(false);
                phase = 3;
                return;
            }
            if (phase == 3) {
                if (session.NextWaveRemaining > remaining - .1f) return;
                Require(session.NextWaveRemaining < remaining && session.Wave == 1, "Countdown did not resume");
                hero.Progression.GrantSkillChoice();
                remaining = session.NextWaveRemaining;
                began = EditorApplication.timeSinceStartup;
                phase = 4;
                return;
            }
            if (phase == 4) {
                if (EditorApplication.timeSinceStartup - began < .35) return;
                Require(session.CountdownPaused && Mathf.Abs(session.NextWaveRemaining - remaining) < .001f, "Skill choice did not freeze countdown");
                Resolve();
                phase = 5;
                return;
            }
            if (phase == 5) {
                if (session.Wave == 1) return;
                Require(session.Wave == 2 && session.enemies.Length == 4 && !session.WaitingForNextWave && session.NextWaveRemaining == 0, "Automatic next wave failed or countdown leaked");
                Require(hero.Progression.Level == level && hero.Equipment.ArmorEquipped && session.Events.Points.Count == 4, "Automatic transition lost growth/equipment/events");
                Require(session.enemies.All(enemy => !enemy.Health.Dead), "Automatic wave enemies not alive");
                foreach (var enemy in session.enemies) { enemy.Health.Damage(999999); enemy.DropLootOnce(); }
                Require(hero.Progression.PendingChoices > 0, "No pending level to test");
                began = EditorApplication.timeSinceStartup;
                phase = 6;
                return;
            }
            if (phase == 6) {
                if (!session.WaitingForNextWave || EditorApplication.timeSinceStartup - began < .35) return;
                Require(session.Wave == 2 && session.CountdownPaused && session.NextWaveRemaining > 1.49f, "Pending rewards consumed countdown time");
                Resolve();
                hero.Health.Damage(999999);
                phase = 7;
                return;
            }
            Require(session.Wave == 2 && !session.WaitingForNextWave && session.NextWaveRemaining == 0, "Death did not stop intermission");
            session.Restart();
            Require(session.Wave == 1 && !session.WaitingForNextWave && session.NextWaveRemaining == 0 && !hero.Health.Dead && Time.timeScale == 1, "Restart did not reset countdown");
            Debug.Log("AUTO_WAVE_RUNTIME_PASSED: default delay, actual Update countdown, backpack/skill/pending reward pause, intermission crafting, automatic wave growth and retention, death stop and restart reset.");
            EditorApplication.update -= Tick;
            EditorApplication.Exit(0);
        }
        catch (Exception exception) {
            Debug.LogException(exception); Time.timeScale = 1;
            EditorApplication.update -= Tick;
            EditorApplication.Exit(1);
        }
    }
}
