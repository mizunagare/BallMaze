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
        var prefab = Resources.Load<GameObject>(CrystalCavernLayout.Prefab);
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
        S.Events.RestoreEvents(Array.Empty<SavedWorldEvent>());
        cavern.Bind(S, Layout);
        Physics.SyncTransforms();

        var sources = cavern.Floors.Select(c => Source(c, 0)).Concat(cavern.Blockers.Select(c => Source(c, 1))).ToList();
        var settings = NavMesh.GetSettingsByIndex(0);
        settings.agentRadius = .6f;
        settings.agentHeight = 2.5f;
        settings.agentClimb = .4f;
        navData = NavMeshBuilder.BuildNavMeshData(settings, sources, Layout.WorldBounds, Vector3.zero, Quaternion.identity);
        if (navData == null) throw new InvalidOperationException("洞窟导航构建失败");
        nav = NavMesh.AddNavMeshData(navData);
        if (!nav.valid || Layout.points.Any(p => !PathComplete(Layout.entry, p.position)) ||
            !TryInteractionApproach(Layout.exits[0], out _))
            throw new InvalidOperationException("洞窟路线或免费出口不可达");

        S.enemies = Layout.encounters.Select(e =>
        {
            var actor = S.Waves.CreateEncounter(root.transform, e.id, e.home, (EnemyArchetype)e.type);
            actor.gameObject.AddComponent<EncounterGuard>().Configure(this, e);
            actor.name = "洞窟巡守";
            return actor;
        }).ToArray();
        Physics.SyncTransforms();
        Ready = true;
        InvalidateRoutes();
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

    public BoxCollider[] Floors => floors;
    public BoxCollider[] Blockers => blockers;

    public void Bind(CombatSession session, ForestLayout layout)
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
        exit.Configure(layout.exits[0], true);
        hazard.Bind(session);
    }
}
