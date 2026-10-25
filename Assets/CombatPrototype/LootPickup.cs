using UnityEngine;

public class LootPickup : MonoBehaviour
{
    public string InteractionId {get;private set;} = System.Guid.NewGuid().ToString("N");
    public void RestoreInteractionId(string id){if(!string.IsNullOrEmpty(id))InteractionId=id;}
    public MaterialKind Kind { get; private set; }
    public int Amount { get; private set; }
    public bool Collected { get; private set; }
    public GearItem Gear { get; private set; }
    public string ItemLabel => Gear != null ? Gear.Name : PlayerInventory.Label(Kind);
    public static LootPickup SpawnGear(GearItem item, Vector3 position) { if(item.dataRevision==0)item.UpgradeLegacy();item.worn=item.overflow=item.board=false;item.x=item.y=-1; var loot = Spawn(MaterialKind.CrystalShard, 1, position); loot.Gear = item; loot.name = "掉落装备 - " + item.Name; loot.material.color = AdventureItems.Color(item.quality); return loot; }
    Material material;
    float baseHeight;
    public Vector3 SavePosition => new Vector3(transform.position.x, baseHeight, transform.position.z);
    public static LootPickup Spawn(MaterialKind kind, int amount, Vector3 position)
    {
        var obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
        obj.name = $"掉落物 - {PlayerInventory.Label(kind)} x{amount}";
        obj.transform.position = position;
        obj.transform.localScale = Vector3.one * .35f;
        // Dropped materials are visual markers; they never block movement or the camera.
        obj.GetComponent<Collider>().enabled = false;
        var loot = obj.AddComponent<LootPickup>();
        loot.Kind = kind;
        loot.Amount = amount;
        loot.baseHeight = position.y;
        loot.material = new Material(Shader.Find("Universal Render Pipeline/Lit"));
        loot.material.color = kind == MaterialKind.BossCore ? new Color(.1f, 1, 1) : kind == MaterialKind.MonsterHide ? new Color(1, .65f, .16f) : new Color(.6f, .3f, 1);
        obj.GetComponent<Renderer>().sharedMaterial = loot.material;
        return loot;
    }
    void Update()
    {
        transform.Rotate(0, 60 * Time.deltaTime, 0);
        var position = transform.position;
        position.y = baseHeight + Mathf.Sin(Time.time * 3) * .08f;
        transform.position = position;
    }
    public bool CanPickUp(PlayerInventory inventory)
    {
        if (Collected || inventory == null || inventory.IsOpen || !gameObject.activeSelf) return false;
        var hero = inventory.GetComponent<ThirdPersonHero>();
        if (hero == null || hero.Health == null || hero.Health.Dead || hero.GameplayPaused) return false;
        Vector3 origin = inventory.transform.position + Vector3.up * .5f;
        if (Vector3.Distance(origin, transform.position) > inventory.pickupRange) return false;
        if (!Physics.Linecast(origin, transform.position, out var hit, ~0, QueryTriggerInteraction.Ignore)
            || hit.collider.transform.IsChildOf(inventory.transform)) return true;
        // Historical chest rewards can be embedded in their box collider. Opening
        // the box exposes those rewards without moving saved loot or ignoring walls.
        if (!OpenedChestContains(hit.collider)) return false;
        Vector3 line = transform.position - origin;
        foreach (var obstacle in Physics.RaycastAll(origin, line.normalized, line.magnitude, ~0, QueryTriggerInteraction.Ignore))
            if (!obstacle.collider.transform.IsChildOf(inventory.transform) && !OpenedChestContains(obstacle.collider)) return false;
        return true;
    }
    bool OpenedChestContains(Collider collider)
    {
        var chest = collider.GetComponentInParent<WorldEventPoint>();
        return chest != null && chest.Used && chest.Kind == WorldEventKind.Treasure && collider.bounds.Contains(SavePosition);
    }
    public bool PickUp(PlayerInventory inventory)
    {
        if (!CanPickUp(inventory)) return false;
        var owner=inventory.GetComponent<ThirdPersonHero>();var flow=AdventureFlow.Find(owner);int oldCount=inventory.Count(Kind),oldEarned=flow?.ActiveRun?.earnedRemaining[(int)Kind]??0;
        if (Gear != null && !inventory.GetComponent<AdventureLoadout>().Add(Gear)) { inventory.NotifyMessage("背包空间不足，请整理或分解装备后再拾取。"); return false; }
        if(Gear==null&&!inventory.Add(Kind,Amount))return false;
        Collected = true;
        if(Gear==null)inventory.NotifyPickup(Kind, Amount);else inventory.NotifyMessage("拾取："+Gear.Name);
        gameObject.SetActive(false);
        Onboarding.Picked(owner,this,oldCount,oldEarned);
        Destroy(gameObject);
        return true;
    }
    void OnDestroy() { if (material != null) Destroy(material); }
}






