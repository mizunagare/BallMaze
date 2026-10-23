using UnityEngine;

public enum WorldEventKind { Treasure, Altar }

public class WorldEventPoint : MonoBehaviour
{
    public WorldEventKind Kind { get; private set; }
    public bool Used { get; private set; }
    public float interactionRange = 2.5f;
    public string Title => Kind == WorldEventKind.Treasure ? "物资宝箱" : "技能祭坛";
    public string Action => Kind == WorldEventKind.Treasure ? "开启宝箱" : "接受赐福";
    Transform lid;
    Renderer glow;
    public void Configure(WorldEventKind kind, Transform chestLid, Renderer indicator)
    {
        Kind = kind;
        lid = chestLid;
        glow = indicator;
    }
    public bool CanInteract(ThirdPersonHero hero)
    {
        if (Used || !gameObject.activeInHierarchy || hero == null || hero.Health == null || hero.Health.Dead || hero.GameplayPaused) return false;
        if (hero.Progression.PendingChoices > 0 || hero.gameObject.scene != gameObject.scene) return false;
        Vector3 origin = hero.transform.position + Vector3.up * .7f;
        Vector3 aim = transform.position + Vector3.up * .7f;
        if (Vector3.Distance(origin, aim) > interactionRange) return false;
        return !Physics.Linecast(origin, aim, out var hit, ~0, QueryTriggerInteraction.Ignore)
            || hit.collider.GetComponentInParent<WorldEventPoint>() == this;
    }
    public bool Interact(ThirdPersonHero hero)
    {
        if (!CanInteract(hero)) return false;
        // Mark consumed before opening rewards so repeated input cannot grant twice.
        Used = true;
        if (Kind == WorldEventKind.Treasure) {
            LootPickup.SpawnGear(AdventureItems.Roll(Object.FindFirstObjectByType<CombatSession>().Wave,true), transform.position + Vector3.up * 1.2f + transform.forward);
            int hides = Random.Range(2, 6), shards = Random.Range(1, 3);
            var flow=AdventureFlow.Find(hero);if(flow!=null&&flow.Tracking){LootPickup.Spawn(MaterialKind.MonsterHide,hides,transform.position+Vector3.up*.6f+Vector3.left);LootPickup.Spawn(MaterialKind.CrystalShard,shards,transform.position+Vector3.up*.6f+Vector3.right);}else{hero.Inventory.Add(MaterialKind.MonsterHide,hides);hero.Inventory.Add(MaterialKind.CrystalShard,shards);}
            hero.Inventory.NotifyMessage($"宝箱奖励：野怪皮 ×{hides}，晶石碎片 ×{shards}；冒险奖励在箱旁，按 E 拾取（满容量时保留）");
            if (lid != null) lid.localRotation = Quaternion.Euler(-65, 0, 0);
        }
        else {
            hero.Progression.GrantSkillChoice();
            hero.Inventory.NotifyMessage("祭坛已赐福：请选择一项技能");
        }
        RestoreUsed(true);
        return true;
    }
    public void RestoreUsed(bool used)
    {
        Used = used;
        if (lid != null) lid.localRotation = Quaternion.Euler(used ? -65 : 0, 0, 0);
        if (glow != null && used) {
            var properties = new MaterialPropertyBlock();
            properties.SetColor("_BaseColor", new Color(.25f, .27f, .29f));
            glow.SetPropertyBlock(properties);
        }
    }
    void OnGUI()
    {
        Camera camera = Camera.main;
        if (camera == null) return;
        var orbit = camera.GetComponent<OrbitCamera>();
        if (orbit != null && orbit.target != null && orbit.target.TryGetComponent<ThirdPersonHero>(out var hero)
            && (hero.Inventory.IsOpen || hero.Progression.IsChoosing)) return;
        Vector3 screen = camera.WorldToScreenPoint(transform.position + Vector3.up * 2);
        if (screen.z <= 0 || Vector3.Distance(camera.transform.position, transform.position) > 24) return;
        CombatChineseUI.Apply();
        GUI.Box(new Rect(screen.x - 80, Screen.height - screen.y, 160, 26), Used ? (Kind == WorldEventKind.Treasure ? "宝箱已开启" : "祭坛已使用") : Title);
    }
}


