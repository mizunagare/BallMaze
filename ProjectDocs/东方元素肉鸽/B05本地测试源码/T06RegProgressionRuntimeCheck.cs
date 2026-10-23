using System;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class T06RegProgressionRuntimeCheck
{
    static double deadline;
    static int phase;
    static CombatSession session;
    public static void Run()
    {
        EditorSceneManager.OpenScene("Assets/CombatPrototype/CombatPlayground.unity");
        deadline = EditorApplication.timeSinceStartup + 60;
        EditorApplication.update += Tick;
        EditorApplication.EnterPlaymode();
    }
    static void Require(bool value, string message) { if (!value) throw new Exception(message); }
    static void Resolve(HeroProgression progression)
    {
        int safety = 100;
        while (progression.PendingChoices > 0 && safety-- > 0) {
            progression.BeginChoice();
            Require(progression.IsChoosing && progression.Offers.Count == 3 && progression.Offers.Distinct().Count() == 3, "Offers not unique");
            Require(progression.SelectChoice(0), "Choice failed");
        }
        Require(safety > 0, "Choice queue stuck");
    }
    static void Tick()
    {
        try {
            if (EditorApplication.timeSinceStartup > deadline) throw new Exception("Progression test timed out");
            if (!EditorApplication.isPlaying || Time.time < .2f) return;
            session = UnityEngine.Object.FindFirstObjectByType<CombatSession>();
            if (session == null || session.hero.Progression == null) return;
            var hero = session.hero;
            var p = hero.Progression;
            var bag = hero.Inventory;
            if (phase == 0) {
                session.Restart();
                Require(p.Level == 1 && p.Experience == 0, "Initial level wrong");
                session.enemies[0].Health.Damage(999);
                phase = 1;
                return;
            }
            if (phase == 1) {
                if (p.Level == 1) return;
                Require(p.Level == 2 && p.Experience == 5 && p.PendingChoices == 1, "Kill XP threshold wrong");
                session.enemies[0].DropLootOnce();
                Require(p.Level == 2 && p.Experience == 5, "Kill granted XP twice");
                p.BeginChoice();
                Require(Time.timeScale == 0 && hero.GameplayPaused, "Upgrade did not pause");
                bag.SetOpen(true);
                Require(!bag.IsOpen, "Backpack opened over upgrade");
                Require(!p.SelectChoice(-1) && p.PendingChoices == 1, "Invalid choice consumed reward");
                Resolve(p);
                Require(Time.timeScale == 1 && !p.IsChoosing, "Selecting skill did not resume");
                session.Restart();
                p.GainExperience(200);
                Require(p.Level == 6 && p.Experience == 0 && p.PendingChoices == 5, "Multi-level XP queue wrong");
                Resolve(p);
                Require(Enum.GetValues(typeof(BasicSkill)).Cast<BasicSkill>().Sum(skill => p.Rank(skill)) == 5, "Lost queued selections");
                session.Restart();
                // Exercise each actual random offer; select an untested skill whenever it appears.
                var seen = new System.Collections.Generic.HashSet<BasicSkill>();
                for (int attempt = 0; seen.Count < 6 && attempt < 100; attempt++) {
                    p.GainExperience(p.RequiredExperience - p.Experience);
                    p.BeginChoice();
                    int choice = 0;
                    for (int i = 0; i < p.Offers.Count; i++) if (!seen.Contains(p.Offers[i])) { choice = i; break; }
                    var selected = p.Offers[choice];
                    float hp = hero.Health.Current;
                    int oldVitality = p.Rank(BasicSkill.Vitality);
                    p.SelectChoice(choice);
                    seen.Add(selected);
                    Require(hero.AttackPower == hero.attackDamage + hero.Equipment.AttackBonus + p.Rank(BasicSkill.Strength) * 5, "Strength ineffective");
                    Require(hero.Defense == hero.Equipment.Defense + p.Rank(BasicSkill.IronSkin) * 2, "Defense ineffective");
                    Require(Mathf.Approximately(hero.MoveMultiplier, 1 + p.Rank(BasicSkill.Speed) * .1f), "Move multiplier ineffective");
                    Require(Mathf.Approximately(hero.AttackInterval, .5f / (1 + p.Rank(BasicSkill.Frenzy) * .15f)), "Attack speed ineffective");
                    Require(Mathf.Approximately(hero.AttackRange, 1.8f + p.Rank(BasicSkill.Reach) * .25f), "Reach ineffective");
                    Require(hero.Health.maxHealth == 100 + p.Rank(BasicSkill.Vitality) * 25, "Vitality max health ineffective");
                    if (p.Rank(BasicSkill.Vitality) > oldVitality) Require(hero.Health.Current == hp + 25, "Vitality healing missing");
                }
                Require(seen.Count == 6, "Not all skills exercised");
                bag.Add(MaterialKind.MonsterHide, 3);
                bag.Add(MaterialKind.CrystalShard, 2);
                Require(hero.Equipment.Craft(EquipmentKind.CrystalSword) && hero.Equipment.Craft(EquipmentKind.HideArmor), "Crafting regression");
                hero.Equipment.Equip(EquipmentKind.CrystalSword, true);
                hero.Equipment.Equip(EquipmentKind.HideArmor, true);
                Require(hero.AttackPower == hero.attackDamage + hero.Equipment.AttackBonus + p.AttackBonus && hero.Defense == hero.Equipment.Defense + p.DefenseBonus, "Equipment and skill bonuses conflict");
                hero.Health.ResetHealth();
                float before = hero.Health.Current;
                hero.Health.Damage(30);
                Require(hero.Health.Current == before - Mathf.Max(1, 30 - hero.Defense), "Combined defense not applied to damage");
                foreach (var enemy in session.enemies) { enemy.Health.Damage(999); enemy.DropLootOnce(); }
                Resolve(p);
                phase = 2;
                return;
            }
            if (phase == 2) {
                int level = p.Level;
                Require(session.NextWave(), "Next wave failed after clearing");
                Require(session.Wave == 2 && p.Level == level && hero.Equipment.HasSword, "Next wave reset growth");
                foreach (var enemy in session.enemies) Require(!enemy.Health.Dead, "Wave did not revive enemies");
                session.Restart();
                bag.SetOpen(true);
                p.GainExperience(25);
                p.BeginChoice();
                Require(!p.IsChoosing && bag.IsOpen, "Upgrade nested inside backpack pause");
                bag.SetOpen(false);
                p.BeginChoice();
                Require(p.IsChoosing && Time.timeScale == 0, "Deferred choice did not open");
                session.Restart();
                Require(Time.timeScale == 1 && !p.IsChoosing && p.Level == 1 && p.PendingChoices == 0 && p.Experience == 0, "Reset left pending level or pause");
                Require(hero.Health.maxHealth == 100 && hero.Health.Current == 100 && hero.AttackPower == hero.attackDamage + hero.Equipment.AttackBonus && hero.Defense == hero.Equipment.Defense && hero.MoveMultiplier == 1, "Reset retained bonuses");
                Debug.Log("PROGRESSION_RUNTIME_PASSED: kill XP once, thresholds, unique offers, all six skills, queued levels, equipment stacking, real damage reduction, pause coordination, wave retention and full reset.");
                EditorApplication.update -= Tick;
                EditorApplication.Exit(0);
            }
        }
        catch (Exception exception) {
            Debug.LogException(exception);
            Time.timeScale = 1;
            EditorApplication.update -= Tick;
            EditorApplication.Exit(1);
        }
    }
}
