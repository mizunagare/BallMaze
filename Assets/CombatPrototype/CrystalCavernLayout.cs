using System;
using System.IO;
using System.Linq;
using UnityEngine;

public static class CrystalCavernLayout
{
    public const string Map = "crystal-cavern";
    public const string Region = "CrystalCavern";
    public const string Content = "C2.1-CAVERN-1";
    public const string Prefab = "CrystalCavern/Cavern";
    public const string Content22 = "C2.2-CAVERN-1";
    public const string Prefab22 = "CrystalCavernC22/Cavern";
    public const int Generation22 = 11;
    public const string Content23 = "C2.3-CAVERN-1";
    public const string Prefab23 = "CrystalCavernC23/Cavern";
    public const int Generation23 = 12;
    public const string Lake = "c23:lake";
    public const string FarShore = "c23:far-shore";
    public const string BridgeLever = "c23:bridge:lever";
    public const string LakeChest = "c23:far-shore:chest";
    public const string Chamber = "c22:chamber";
    public const string Lever = "c22:chamber:lever";
    public const string Chest = "c22:chamber:chest";
    public const string Elite = "c22:channel:crystal-core";
    public const string HazardId = "c2:energy-pulse";
    public const int Generation = 10;
    public const int FirstMineId = 2100;

    public static bool Is(ForestLayout layout) => layout != null && (layout.revision == 7 || layout.revision == 8 || layout.revision == 9) && layout.mapId == Map;

    public static ForestLayout Generate(int seed)
    {
        var entry = new Vector3(0, .1f, 387);
        return new ForestLayout
        {
            mapId = Map, mapAssetVersion = Content, revision = 7, seed = seed, requestedSeed = seed,
            entry = entry, boundsCenter = new Vector3(12, 2, 399), boundsSize = new Vector3(50, 10, 47),
            terrain = new ForestTerrain(), rocks = Array.Empty<Vector3>(),
            points = new[]
            {
                Point("entry", "洞窟入口", entry, ForestSiteKind.Entrance, 0),
                Point("veins", "水晶矿脉区", new Vector3(0, .1f, 408), ForestSiteKind.Mineral, 1),
                Point("channel", "能量通道", new Vector3(29, .1f, 410), ForestSiteKind.Legacy, 2)
            },
            routes = new[]
            {
                new ForestRoute { from = "c2:entry", to = "c2:veins" },
                new ForestRoute { from = "c2:veins", to = "c2:channel" }
            },
            nodes = new[]
            {
                Vein("west", new Vector3(-5.5f, 0, 403), MaterialKind.Ore),
                Vein("north", new Vector3(-3.8f, 0, 413), MaterialKind.CrystalShard)
            },
            encounters = new[]
            {
                new ForestEncounter { id = "c2:veins:watcher", poi = "c2:veins", home = new Vector3(5.8f, .1f, 412), type = 0 }
            },
            exits = new[]
            {
                new ExtractionConfig { id = "c2:exit-entry", label = "洞窟入口归途", position = new Vector3(0, .1f, 384) }
            }
        };
    }

    public static bool Expanded(ForestLayout layout) => Is(layout) && (layout.revision == 8 || layout.revision == 9);
    public static bool HasLake(ForestLayout layout) => Is(layout) && layout.revision == 9;
    public static bool KnownContent(string content) => content == Content || content == Content22 || content == Content23;
    public static int GenerationFor(ForestLayout layout) => HasLake(layout) ? Generation23 : Expanded(layout) ? Generation22 : Generation;
    public static string PrefabFor(ForestLayout layout) => HasLake(layout) ? Prefab23 : Expanded(layout) ? Prefab22 : Prefab;

    public static ForestLayout GenerateLake(int seed)
    {
        var layout = GenerateExpanded(seed);
        layout.revision = 9;
        layout.mapAssetVersion = Content23;
        layout.boundsCenter = new Vector3(29, 3, 410);
        layout.boundsSize = new Vector3(116, 20, 65);
        layout.points = layout.points.Concat(new[] {
            new ForestPoi { id = Lake, label = "地下湖 · 环湖分路", position = new Vector3(40,.1f,410), siteKind = ForestSiteKind.Entrance },
            new ForestPoi { id = "c23:outer", label = "外环岩岸 · 较长安全路", position = new Vector3(58,.1f,432), siteKind = ForestSiteKind.Entrance },
            new ForestPoi { id = "c23:inner", label = "内环石径 · 巡守", position = new Vector3(58,.1f,394), siteKind = ForestSiteKind.Entrance, risk = 1 },
            new ForestPoi { id = FarShore, label = "对岸晶石补给", position = new Vector3(78,.1f,410), siteKind = ForestSiteKind.Ruins }
        }).ToArray();
        layout.routes = layout.routes.Concat(new[] {
            new ForestRoute { from = "c2:channel", to = Lake },
            new ForestRoute { from = Lake, to = "c23:outer" },
            new ForestRoute { from = "c23:outer", to = FarShore },
            new ForestRoute { from = Lake, to = "c23:inner" },
            new ForestRoute { from = "c23:inner", to = FarShore }
        }).ToArray();
        layout.nodes = layout.nodes.Concat(new[] {
            new ForestNode { id = "c23:mine-ore", position = new Vector3(52,0,433), kind = (int)MaterialKind.Ore },
            new ForestNode { id = "c23:mine-crystal", position = new Vector3(80,0,417), kind = (int)MaterialKind.CrystalShard }
        }).ToArray();
        layout.encounters = layout.encounters.Append(new ForestEncounter {
            id = "c23:inner:watcher", poi = "c23:inner", home = new Vector3(59,.1f,394), type = 0
        }).ToArray();
        return layout;
    }

    public static ForestLayout GenerateExpanded(int seed)
    {
        var layout = Generate(seed);
        layout.revision = 8;
        layout.mapAssetVersion = Content22;
        layout.boundsCenter = new Vector3(4, 2, 399);
        layout.boundsSize = new Vector3(66, 10, 47);
        layout.points = layout.points.Append(new ForestPoi
        {
            id = Chamber, label = "隐藏矿室", position = new Vector3(-21, .1f, 410),
            siteKind = ForestSiteKind.Mineral, risk = 1
        }).ToArray();
        layout.routes = layout.routes.Append(new ForestRoute { from = "c2:veins", to = Chamber }).ToArray();
        layout.encounters = layout.encounters.Append(new ForestEncounter
        {
            id = Elite, poi = "c2:channel", home = new Vector3(29, .1f, 410), type = (int)EnemyArchetype.Elite
        }).ToArray();
        return layout;
    }

    public static SavedWorldEvent[] Events(ForestLayout layout)
    {
        var events = Expanded(layout) ? new[] {
        new SavedWorldEvent { entityId = Lever, kind = WorldEventKind.Altar, position = new Vector3(-7.7f, 0, 406.8f) },
        new SavedWorldEvent { entityId = Chest, kind = WorldEventKind.Treasure, position = new Vector3(-22, 0, 411.5f) }
        } : Array.Empty<SavedWorldEvent>();
        return !HasLake(layout) ? events : events.Concat(new[] {
            new SavedWorldEvent { entityId = BridgeLever, kind = WorldEventKind.Altar, position = new Vector3(76,0,413) },
            new SavedWorldEvent { entityId = LakeChest, kind = WorldEventKind.Treasure, position = new Vector3(80,0,405) }
        }).ToArray();
    }

    public static bool Used(SavedWorldEvent[] events, string id) => events?.Any(e => e.entityId == id && e.used) == true;
    static ForestPoi Point(string id, string label, Vector3 position, ForestSiteKind kind, int risk) =>
        new ForestPoi { id = "c2:" + id, label = label, position = position, siteKind = kind, risk = risk };

    static ForestNode Vein(string id, Vector3 position, MaterialKind kind) =>
        new ForestNode { id = "c2:mine-" + id, position = position, kind = (int)kind };

    public static void Validate(ForestLayout layout)
    {
        if (!Is(layout) || JsonUtility.ToJson(layout) != JsonUtility.ToJson(HasLake(layout) ? GenerateLake(layout.seed) : Expanded(layout) ? GenerateExpanded(layout.seed) : Generate(layout.seed)))
            throw new InvalidDataException("洞窟布局版本或固定身份不合法");
    }

    public static void ValidateCheckpoint(CombatCheckpoint checkpoint)
    {
        if (!Is(checkpoint.forest)) return;
        Validate(checkpoint.forest);
        var nodes = checkpoint.forest.nodes;
        if (checkpoint.resources == null || checkpoint.resources.Length != nodes.Length ||
            nodes.Where((node, index) => checkpoint.resources.Count(resource =>
                resource.entityId == node.id && resource.id == FirstMineId + index &&
                resource.health >= 0 && resource.health <= CrystalCavernRegion.MineHealth) != 1).Any() ||
            !ValidEvents(checkpoint.forest, checkpoint.events))
            throw new InvalidDataException("洞窟矿脉或交互快照不合法");
    }

    static bool ValidEvents(ForestLayout layout, SavedWorldEvent[] saved)
    {
        var expected = Events(layout);
        return saved != null && saved.Length == expected.Length &&
            expected.All(e => saved.Count(s => s != null && s.entityId == e.entityId &&
                s.kind == e.kind && s.position == e.position) == 1) &&
            (!Used(saved, Chest) || Used(saved, Lever));
    }}
