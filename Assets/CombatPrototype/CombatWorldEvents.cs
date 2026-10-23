using System.Collections.Generic;
using UnityEngine;

public class CombatWorldEvents : MonoBehaviour
{
    readonly List<WorldEventPoint> points = new List<WorldEventPoint>();
    public IReadOnlyList<WorldEventPoint> Points => points;
    GameObject root;
    Material wood, gold, stone, crystal;
    void Start() { ResetEvents(); }
    Material MakeMaterial(Color color) => new Material(Shader.Find("Universal Render Pipeline/Lit")) { color = color };
    public void ResetEvents()
    {
        PrepareRoot();
        for (int i = 0; i < 4; i++) {
            if (!TryLocation(out Vector3 position)) {
                Debug.LogWarning("没有找到安全的事件生成位置，本次略过一个事件。");
                continue;
            }
            points.Add(Build(i < 2 ? WorldEventKind.Treasure : WorldEventKind.Altar, position));
            Physics.SyncTransforms();
        }
    }
    public void RestoreEvents(SavedWorldEvent[] saved)
    {
        PrepareRoot();
        foreach (var state in saved) { var point = Build(state.kind, state.position); point.RestoreUsed(state.used); points.Add(point); }
        Physics.SyncTransforms();
    }
    void PrepareRoot()
    {
        if (root != null) { root.SetActive(false); Destroy(root); }
        points.Clear();
        Physics.SyncTransforms();
        if (wood == null) {
            wood = MakeMaterial(new Color(.4f, .22f, .08f));
            gold = MakeMaterial(new Color(1, .72f, .12f));
            stone = MakeMaterial(new Color(.36f, .43f, .53f));
            crystal = MakeMaterial(new Color(.65f, .25f, 1));
        }
        root = new GameObject("本波随机事件：宝箱与祭坛");
        UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(root, gameObject.scene);
    }
    bool TryLocation(out Vector3 result)
    {
        for (int attempt = 0; attempt < 250; attempt++) {
            Vector3 test = new Vector3(Random.Range(-36f, 36f), 5, Random.Range(-36f, 36f));
            if (!Physics.Raycast(test, Vector3.down, out var floor, 8, ~0, QueryTriggerInteraction.Ignore)) continue;
            if (floor.collider.gameObject.scene != gameObject.scene || floor.normal.y < .9f || floor.point.y > .3f) continue;
            Vector3 ground = floor.point;
            // Reject occupied locations and leave enough room to walk around each event.
            if (Physics.CheckBox(ground + Vector3.up * 1.1f, new Vector3(1, .8f, 1), Quaternion.identity, ~0, QueryTriggerInteraction.Ignore)) continue;
            bool spaced = true;
            foreach (var point in points) if (Vector3.Distance(point.transform.position, ground) < 5) spaced = false;
            if (!spaced) continue;
            result = ground;
            return true;
        }
        result = Vector3.zero;
        return false;
    }
    WorldEventPoint Build(WorldEventKind kind, Vector3 position)
    {
        var obj = new GameObject(kind == WorldEventKind.Treasure ? "物资宝箱" : "技能祭坛");
        obj.transform.SetParent(root.transform);
        obj.transform.position = position;
        var point = obj.AddComponent<WorldEventPoint>();
        if (kind == WorldEventKind.Treasure) {
            Part("箱体", PrimitiveType.Cube, obj.transform, new Vector3(0, .45f, 0), new Vector3(1.4f, .9f, 1), wood, true);
            var pivot = new GameObject("箱盖转轴").transform;
            pivot.SetParent(obj.transform, false);
            pivot.localPosition = new Vector3(0, .9f, .5f);
            var lid = Part("金色箱盖", PrimitiveType.Cube, pivot, new Vector3(0, .08f, -.5f), new Vector3(1.5f, .16f, 1.1f), gold, false);
            Part("锁扣", PrimitiveType.Cube, obj.transform, new Vector3(0, .6f, -.53f), new Vector3(.2f, .3f, .08f), gold, false);
            point.Configure(kind, pivot, lid.GetComponent<Renderer>());
        }
        else {
            Part("祭坛底座", PrimitiveType.Cylinder, obj.transform, new Vector3(0, .18f, 0), new Vector3(1.8f, .18f, 1.8f), stone, true);
            Part("石柱", PrimitiveType.Cube, obj.transform, new Vector3(0, .7f, 0), new Vector3(.65f, .8f, .65f), stone, true);
            var jewel = Part("赐福晶石", PrimitiveType.Cube, obj.transform, new Vector3(0, 1.5f, 0), Vector3.one * .55f, crystal, false);
            jewel.transform.localRotation = Quaternion.Euler(30, 45, 30);
            point.Configure(kind, null, jewel.GetComponent<Renderer>());
        }
        return point;
    }
    GameObject Part(string name, PrimitiveType shape, Transform parent, Vector3 position, Vector3 scale, Material material, bool collision)
    {
        var obj = GameObject.CreatePrimitive(shape);
        obj.name = name;
        obj.transform.SetParent(parent, false);
        obj.transform.localPosition = position;
        obj.transform.localScale = scale;
        obj.GetComponent<Renderer>().sharedMaterial = material;
        obj.GetComponent<Collider>().enabled = collision;
        return obj;
    }
    void OnDestroy()
    {
        if (root != null) Destroy(root);
        if (wood != null) Destroy(wood);
        if (gold != null) Destroy(gold);
        if (stone != null) Destroy(stone);
        if (crystal != null) Destroy(crystal);
    }
}

