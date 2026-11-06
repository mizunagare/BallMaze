using UnityEngine;

public enum WorldEventKind { Treasure, Altar }

public class WorldEventPoint : MonoBehaviour
{
    public string entityId;
    public WorldEventKind Kind { get; private set; }
    public bool Used { get; private set; }
    public float interactionRange = 2.5f;
    public string Title => RuinsExploration.Title(this) ?? (ForestRegionRuntime.LakeLever(this) != null ? "开启回程石桥" : null) ?? (ForestRegionRuntime.CavernLever(this) != null ? "矿室晶纹机关" : null) ?? (Kind == WorldEventKind.Treasure ? (ForestRewards.Site(this,entityId)?.label??"物资")+"宝箱" : "技能祭坛");
    public string Action => RuinsExploration.Title(this) ?? (ForestRegionRuntime.LakeLever(this) != null ? "开启回程石桥" : null) ?? (ForestRegionRuntime.CavernLever(this) != null ? "开启隐藏矿室" : null) ?? (Kind == WorldEventKind.Treasure ? "开启宝箱" : "接受赐福");
    Transform lid;
    public Transform VisualLid=>lid;
    Renderer glow;
    public void Configure(WorldEventKind kind, Transform chestLid, Renderer indicator)
    {
        Kind = kind;
        lid = chestLid;
        glow = indicator;
        if(GetComponent<CatEventVisual>()==null)gameObject.AddComponent<CatEventVisual>();
    }
    public bool CanInteract(ThirdPersonHero hero)
    {
        if ((RuinsExploration.For(this) is RuinsExploration ruins?!ruins.CanUse(this):Used) || !gameObject.activeInHierarchy || hero == null || hero.Health == null || hero.Health.Dead || hero.GameplayPaused) return false;
        if (entityId == CrystalCavernLayout.Chest && !ForestRegionRuntime.CavernChestOpen(this)) return false;
        if (hero.Progression.PendingChoices > 0 || hero.gameObject.scene != gameObject.scene) return false;
        Vector3 origin = hero.transform.position + Vector3.up * .7f;
        Vector3 aim = transform.position + Vector3.up * .7f;
        if (Vector3.Distance(origin, aim) > interactionRange) return false;
        return !Physics.Linecast(origin, aim, out var hit, ~0, QueryTriggerInteraction.Ignore)
            || hit.collider.GetComponentInParent<WorldEventPoint>() == this
            || RuinsExploration.For(this)?.DoorContact(this,hit.collider)==true;
    }
    public bool Interact(ThirdPersonHero hero)
    {
        if (!CanInteract(hero)) return false;
        if(RuinsExploration.For(this) is RuinsExploration ruins)return ruins.Interact(this,hero);
        if (ForestRegionRuntime.LakeLever(this) is ForestRegionRuntime lake)
        {
            if (!lake.OpenLakeBridge())
            {
                hero.Inventory.NotifyMessage("回程桥门未开启，可以重试；环湖道路仍可返回");
                return false;
            }
            RestoreUsed(true);
            hero.Inventory.NotifyMessage("回程石桥已开启 · 双向通行，向西返回洞窟入口");
            return true;
        }
        if (ForestRegionRuntime.CavernLever(this) is ForestRegionRuntime cavern)
        {
            if (!cavern.OpenCavernChamber())
            {
                hero.Inventory.NotifyMessage("矿室机关未开启，可以重试");
                return false;
            }
            RestoreUsed(true);
            hero.Inventory.NotifyMessage("矿室已开启 · 沿青色晶纹进入，原路可返回");
            return true;
        }
        // Mark consumed before opening rewards so repeated input cannot grant twice.
        Used = true;
        if (Kind == WorldEventKind.Treasure && ForestRewards.Site(this,entityId) is ForestPoi site) {
            foreach(var reward in ForestRewards.Chest(site.siteKind,this)){var loot=LootPickup.Spawn(reward.material,reward.amount,transform.position+Vector3.up*.6f+Vector3.right*((int)reward.material*.35f-1));UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(loot.gameObject,gameObject.scene);}
            if(ForestRewards.ShouldDropChestGear(site.siteKind,AdventureRandom.Value(owner:this))){var loot=LootPickup.SpawnGear(AdventureItems.Roll(Object.FindFirstObjectByType<CombatSession>().Wave,true,owner:this),transform.position+Vector3.up+Vector3.forward);UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(loot.gameObject,gameObject.scene);}
            hero.Inventory.NotifyMessage(site.label+"：奖励已落地，靠近按 "+PlayerInput.Key(PlayerAction.Interact)+" 拾取");
        }
        else if (Kind == WorldEventKind.Treasure) {
            LootPickup.SpawnGear(AdventureItems.Roll(Object.FindFirstObjectByType<CombatSession>().Wave,true,owner:this), transform.position + Vector3.up * 1.2f + transform.forward);
            var ranges=ForestRewards.LegacyChestRanges();
            int hides = AdventureRandom.Range(ranges[0].min,ranges[0].max+1,owner:this), shards = AdventureRandom.Range(ranges[1].min,ranges[1].max+1,owner:this);
            var flow=AdventureFlow.Find(hero);if(flow!=null&&flow.Tracking){LootPickup.Spawn(MaterialKind.MonsterHide,hides,transform.position+Vector3.up*.6f+Vector3.left);LootPickup.Spawn(MaterialKind.CrystalShard,shards,transform.position+Vector3.up*.6f+Vector3.right);}else{hero.Inventory.Add(MaterialKind.MonsterHide,hides);hero.Inventory.Add(MaterialKind.CrystalShard,shards);}
            hero.Inventory.NotifyMessage($"宝箱奖励：野怪皮 ×{hides}，晶石碎片 ×{shards}；冒险奖励在箱旁，按 "+PlayerInput.Key(PlayerAction.Interact)+" 拾取（满容量时保留）");
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
        if(PlayerHudPresenter.Running)return;
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
