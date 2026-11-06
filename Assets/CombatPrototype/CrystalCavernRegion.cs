using System;
using System.Linq;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.SceneManagement;

public partial class ForestRegionRuntime
{
    void BuildCavern(ForestLayout layout)
    {
        layout.Validate();
        Clear();
        Layout = AdventureData.Clone(layout);
        var prefab = Resources.Load<GameObject>(CrystalCavernLayout.PrefabFor(Layout));
        if (prefab == null) throw new InvalidOperationException("缺少水晶洞窟固定资源");

        foreach (var collider in FindObjectsByType<Collider>().Where(c =>
            c.gameObject.scene == gameObject.scene && c.enabled && !c.isTrigger &&
            c.GetComponentInParent<ThirdPersonHero>() == null &&
            c.GetComponentInParent<CombatEnemy>() == null &&
            c.GetComponentInParent<LootPickup>() == null))
        {
            ruinsHiddenCollision.Add(collider);
            collider.enabled = false;
        }
        foreach (var actor in FindObjectsByType<CombatEnemy>().Select(e => e.gameObject)
            .Concat(FindObjectsByType<AdventureResource>().Select(n => n.gameObject))
            .Where(o => o.scene == gameObject.scene).Distinct())
        {
            hidden.Add(actor);
            actor.SetActive(false);
        }

        root = Instantiate(prefab);
        SceneManager.MoveGameObjectToScene(root, gameObject.scene);
        var cavern = root.GetComponent<CrystalCavernRegion>();
        if (cavern == null) throw new InvalidOperationException("缺少洞窟固定资源绑定");
        var events = CrystalCavernLayout.Events(Layout);
        foreach (var point in events)
            point.used = CrystalCavernLayout.Used(S.Flow.ActiveRun?.checkpoint?.events, point.entityId);
        cavern.Bind(S, Layout, CrystalCavernLayout.Used(events, CrystalCavernLayout.Lever));
        cavern.SetBridge(CrystalCavernLayout.Used(events, CrystalCavernLayout.BridgeLever));
        S.Events.RestoreEvents(events);
        RebuildCavernNavigation(cavern);
        S.enemies = Layout.encounters.Select(e =>
        {
            var actor = S.Waves.CreateEncounter(root.transform, e.id, e.home, (EnemyArchetype)e.type);
            actor.gameObject.AddComponent<EncounterGuard>().Configure(this, e);
            if (e.id == CrystalCavernLayout.Elite)
            {
                actor.name = "晶核精英";
                actor.CrystalElite = actor.gameObject.AddComponent<CrystalCoreElite>();
                actor.CrystalElite.Bind(actor, cavern.Hazard);
            }
            else actor.name = "洞窟巡守";
            return actor;
        }).ToArray();
        Physics.SyncTransforms();
        Ready = true;
        InvalidateRoutes();
    }

    void RebuildCavernNavigation(CrystalCavernRegion cavern)
    {
        Physics.SyncTransforms();
        var sources = cavern.Floors.Select(c => Source(c, 0))
            .Concat(cavern.Blockers.Where(c => c.enabled && c.gameObject.activeInHierarchy).Select(c => Source(c, 1))).ToList();
        var settings = NavMesh.GetSettingsByIndex(0);
        settings.agentRadius = .6f;
        settings.agentHeight = 2.5f;
        settings.agentClimb = .4f;
        var next = NavMeshBuilder.BuildNavMeshData(settings, sources, Layout.WorldBounds, Vector3.zero, Quaternion.identity);
        if (next == null) throw new InvalidOperationException("洞窟导航构建失败");
        var previous = navData;
        if (nav.valid) nav.Remove();
        nav = NavMesh.AddNavMeshData(next);
        if (!nav.valid || Layout.points.Any(p =>
                PathComplete(Layout.entry, p.position) != (p.id != CrystalCavernLayout.Chamber || cavern.ChamberOpen)) ||
            !TryInteractionApproach(Layout.exits[0], out _) ||
            CrystalCavernLayout.HasLake(Layout) &&
                (!NavMesh.SamplePosition(new Vector3(45,.1f,410), out var bridgeStart, 2, NavMesh.AllAreas) ||
                 !NavMesh.Raycast(bridgeStart.position,new Vector3(74,.1f,410),out _,NavMesh.AllAreas) != cavern.BridgeOpen))
        {
            if (nav.valid) nav.Remove();
            Destroy(next);
            if (previous != null) nav = NavMesh.AddNavMeshData(previous);
            throw new InvalidOperationException("洞窟路线、矿室门或免费出口的导航状态不符");
        }
        navData = next;
        if (previous != null) Destroy(previous);
        InvalidateRoutes();
    }

    internal bool OpenCavernChamber()
    {
        var cavern = root?.GetComponent<CrystalCavernRegion>();
        if (!Ready || !CrystalCavernLayout.Expanded(Layout) || cavern == null || cavern.ChamberOpen) return false;
        cavern.SetChamber(true);
        try { RebuildCavernNavigation(cavern); }
        catch (InvalidOperationException error)
        {
            cavern.SetChamber(false);
            Physics.SyncTransforms();
            Debug.LogError(error.Message);
            return false;
        }
        return true;
    }

    internal static ForestRegionRuntime CavernLever(WorldEventPoint point)
    {
        return point.entityId == CrystalCavernLayout.Lever ? CavernFor(point) : null;
    }

    internal static ForestRegionRuntime LakeLever(WorldEventPoint point) =>
        point.entityId == CrystalCavernLayout.BridgeLever && CrystalCavernLayout.HasLake(CavernFor(point)?.Layout) ? CavernFor(point) : null;

    internal bool OpenLakeBridge()
    {
        var cavern = root?.GetComponent<CrystalCavernRegion>();
        if (!Ready || !CrystalCavernLayout.HasLake(Layout) || cavern == null || cavern.BridgeOpen) return false;
        cavern.SetBridge(true);
        try { RebuildCavernNavigation(cavern); }
        catch (InvalidOperationException error)
        {
            cavern.SetBridge(false);
            Physics.SyncTransforms();
            Debug.LogError(error.Message);
            return false;
        }
        return true;
    }

    internal static bool CavernChestOpen(WorldEventPoint point) =>
        CavernFor(point)?.root.GetComponent<CrystalCavernRegion>().ChamberOpen == true;

    static ForestRegionRuntime CavernFor(WorldEventPoint point)
    {
        var region = FindFirstObjectByType<CombatSession>()?.GetComponent<ForestRegionRuntime>();
        return region != null && region.Ready && region.gameObject.scene == point.gameObject.scene &&
            CrystalCavernLayout.Expanded(region.Layout) ? region : null;
    }
    static NavMeshBuildSource Source(BoxCollider collider, int area) => new NavMeshBuildSource
    {
        shape = NavMeshBuildSourceShape.Box,
        transform = Matrix4x4.TRS(collider.bounds.center, Quaternion.identity, Vector3.one),
        size = collider.bounds.size,
        area = area
    };
}

public sealed class CrystalCavernRegion : MonoBehaviour
{
    public const float MineHealth = 65;
    [SerializeField] BoxCollider[] floors;
    [SerializeField] BoxCollider[] blockers;
    [SerializeField] AdventureResource[] veins;
    [SerializeField] ExtractionPoint exit;
    [SerializeField] CavernEnergyHazard hazard;

    [SerializeField] BoxCollider chamberDoor;
    [SerializeField] BoxCollider[] bridgeDoors;

    public bool BridgeOpen => bridgeDoors != null && bridgeDoors.Length == 2 && bridgeDoors.All(d => d != null && !d.gameObject.activeSelf);
    internal void SetBridge(bool open)
    {
        if (bridgeDoors == null) return;
        foreach (var door in bridgeDoors) if (door != null) door.gameObject.SetActive(!open);
    }

    public CavernEnergyHazard Hazard => hazard;
    public bool ChamberOpen => chamberDoor != null && !chamberDoor.gameObject.activeSelf;
    internal void SetChamber(bool open)
    {
        if (chamberDoor != null) chamberDoor.gameObject.SetActive(!open);
    }

    public BoxCollider[] Floors => floors;
    public BoxCollider[] Blockers => blockers;

    public void Bind(CombatSession session, ForestLayout layout, bool chamberOpen)
    {
        if (veins.Length != layout.nodes.Length) throw new InvalidOperationException("洞窟矿脉资源不完整");
        for (int index = 0; index < veins.Length; index++)
        {
            var node = layout.nodes[index];
            var vein = veins[index];
            if (vein.StableId != node.id || vein.nodeId != CrystalCavernLayout.FirstMineId + index ||
                vein.transform.position != node.position || (int)vein.kind != node.kind || vein.maxHealth != MineHealth)
                throw new InvalidOperationException("洞窟矿脉资源身份不匹配");
        }
        if (CrystalCavernLayout.Expanded(layout) != (chamberDoor != null))
            throw new InvalidOperationException("洞窟资源与机关版本不匹配");
        if (CrystalCavernLayout.HasLake(layout) != (bridgeDoors != null && bridgeDoors.Length == 2 && bridgeDoors.All(d => d != null)))
            throw new InvalidOperationException("地下湖桥门与版本不匹配");
        SetChamber(chamberOpen);
        exit.Configure(layout.exits[0], true);
        hazard.Bind(session);
    }
}
