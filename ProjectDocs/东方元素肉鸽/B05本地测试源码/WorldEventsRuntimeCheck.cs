using System;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class WorldEventsRuntimeCheck
{
    static double deadline;
    static int phase;
    static CombatSession session;
    static void Require(bool value, string message) { if (!value) throw new Exception(message); }
    public static void Run()
    {
        EditorSceneManager.OpenScene("Assets/CombatPrototype/CombatPlayground.unity");
        deadline = EditorApplication.timeSinceStartup + 60;
        EditorApplication.update += Tick;
        EditorApplication.EnterPlaymode();
    }
    static void Move(Vector3 position)
    {
        var controller = session.hero.GetComponent<CharacterController>();
        controller.enabled = false;
        session.hero.transform.position = position;
        controller.enabled = true;
        Physics.SyncTransforms();
    }
    static void Approach(WorldEventPoint point)
    {
        for (int i = 0; i < 8; i++) {
            Vector3 offset = Quaternion.Euler(0, i * 45, 0) * Vector3.back * 1.8f;
            Move(point.transform.position + offset + Vector3.up * .1f);
            if (point.CanInteract(session.hero)) return;
        }
        throw new Exception("Could not approach event");
    }
    static void CheckLayout()
    {
        var points = session.Events.Points;
        Require(points.Count == 4, "Expected four events");
        Require(points.Count(point => point.Kind == WorldEventKind.Treasure) == 2 && points.Count(point => point.Kind == WorldEventKind.Altar) == 2, "Event distribution incorrect");
        for (int i = 0; i < points.Count; i++) for (int j = i + 1; j < points.Count; j++)
            Require(Vector3.Distance(points[i].transform.position, points[j].transform.position) >= 5, "Events overlap");
    }
    static void Resolve()
    {
        var p = session.hero.Progression;
        while (p.PendingChoices > 0) { p.BeginChoice(); Require(p.SelectChoice(0), "Reward could not be resolved"); }
    }
    static void Tick()
    {
        try {
            if (EditorApplication.timeSinceStartup > deadline) throw new Exception("Event runtime check timeout");
            if (!EditorApplication.isPlaying || Time.time < .2f) return;
            session = UnityEngine.Object.FindFirstObjectByType<CombatSession>();
            if (session == null || session.Events == null || session.Events.Points.Count == 0) return;
            var hero = session.hero;
            var bag = hero.Inventory;
            var p = hero.Progression;
            if (phase == 0) {
                CheckLayout();
                var chest = session.Events.Points.First(point => point.Kind == WorldEventKind.Treasure);
                Move(chest.transform.position + Vector3.back * 8);
                Require(!chest.Interact(hero) && bag.Materials.Count == 0, "Remote chest interaction succeeded");
                Approach(chest);
                bag.SetOpen(true);
                Require(!chest.Interact(hero), "Chest opened during pause");
                bag.SetOpen(false);
                var loot = LootPickup.Spawn(MaterialKind.MonsterHide, 2, hero.transform.position + Vector3.up * .5f);
                Require(bag.InteractNearest() && loot.Collected && !chest.Used, "E activated loot and chest together or chose farther target");
                Require(bag.InteractNearest() && chest.Used, "Nearest chest interaction failed");
                int hides = bag.Count(MaterialKind.MonsterHide), shards = bag.Count(MaterialKind.CrystalShard);
                Require(hides >= 4 && hides <= 7 && shards >= 1 && shards <= 2, "Chest reward outside range");
                Require(!chest.Interact(hero) && hides == bag.Count(MaterialKind.MonsterHide), "Chest rewarded twice");
                phase = 1;
                return;
            }
            if (phase == 1) {
                var altar = session.Events.Points.First(point => point.Kind == WorldEventKind.Altar);
                Approach(altar);
                // A solid obstacle between player and altar must prevent interaction.
                var wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
                wall.transform.position = Vector3.Lerp(hero.transform.position, altar.transform.position, .5f) + Vector3.up;
                wall.transform.localScale = new Vector3(.7f, 2, .7f);
                Physics.SyncTransforms();
                Require(!altar.Interact(hero), "Interacted through wall");
                wall.SetActive(false);
                UnityEngine.Object.Destroy(wall);
                Physics.SyncTransforms();
                int level = p.Level, xp = p.Experience;
                Require(bag.InteractNearest() && altar.Used && p.IsChoosing && Time.timeScale == 0, "Altar did not open skill reward");
                Require(p.Level == level && p.Experience == xp && p.PendingChoices == 1, "Altar changed XP/level");
                Require(!altar.Interact(hero), "Altar rewarded twice");
                Require(p.Offers.Count == 3 && p.Offers.Distinct().Count() == 3, "Altar skills not unique");
                // A kill arriving while an altar choice is open must queue its upgrade.
                p.GainExperience(25);
                Require(p.PendingChoices == 2 && p.Level == 2 && p.Experience == 5, "Altar/upgrade queue lost reward");
                Resolve();
                Require(Enum.GetValues(typeof(BasicSkill)).Cast<BasicSkill>().Sum(skill => p.Rank(skill)) == 2 && Time.timeScale == 1, "Skills not applied or pause stuck");
                foreach (var enemy in session.enemies) { enemy.Health.Damage(999); enemy.DropLootOnce(); }
                Resolve();
                phase = 2;
                return;
            }
            if (phase == 2) {
                var old = session.Events.Points.ToArray();
                int level = p.Level;
                Require(session.NextWave(), "Next wave failed");
                CheckLayout();
                Require(p.Level == level && session.Events.Points.All(point => !point.Used), "Next wave lost growth or left used events");
                Require(old.All(point => !point.gameObject.activeInHierarchy), "Old events still interactable");
                Require(old.Where((point, index) => point.transform.position != session.Events.Points[index].transform.position).Any(), "Positions did not reroll");
                var altar = session.Events.Points.First(point => point.Kind == WorldEventKind.Altar);
                Approach(altar);
                Require(altar.Interact(hero), "Fresh altar unavailable");
                session.Restart();
                CheckLayout();
                Require(Time.timeScale == 1 && !p.IsChoosing && p.Level == 1 && bag.Materials.Count == 0 && session.Events.Points.All(point => !point.Used), "Restart did not clear event reward / pause");
                Debug.Log("WORLD_EVENTS_RUNTIME_PASSED: safe randomized layout, nearest-only E, loot priority, distance/LOS/pause checks, chest reward ranges, one-shot altar, mixed skill queue, wave reroll and restart.");
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
