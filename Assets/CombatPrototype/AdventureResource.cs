using System;
using UnityEngine;

[Serializable] public class SavedResource { public int id; public string entityId; public float health; }
public class AdventureResource : MonoBehaviour
{
    public int nodeId;
    public string entityId;
    public string StableId => string.IsNullOrEmpty(entityId)?"resource:"+nodeId:entityId;
    public MaterialKind kind;
    public float maxHealth = 65;
    public float Health {get;private set;}
    public const int HarvestMinimum=3, HarvestMaximumExclusive=7;
    public float ExpectedHarvest(ThirdPersonHero hero)=>(HarvestMinimum+HarvestMaximumExclusive-1)*.5f+hero.GetComponent<AdventureLoadout>().HarvestBonus;
    Vector3 originalScale;
    float flashUntil;
    void Awake(){Health=maxHealth;originalScale=transform.localScale;}
    public void Restore(float hp){Health=Mathf.Clamp(hp,0,maxHealth);foreach(var r in GetComponentsInChildren<Renderer>(true))r.enabled=Health>0;foreach(var c in GetComponentsInChildren<Collider>(true))c.enabled=Health>0;transform.localScale=originalScale;}
    public void Hit(float damage,ThirdPersonHero hero)
    {
        if(Health<=0||damage<=0||hero.Health.Dead||hero.GameplayPaused)return;
        Health=Mathf.Max(0,Health-damage);flashUntil=Time.time+.16f;
        AdventurePulse.Spawn(transform.position+Vector3.up*.15f,.8f,new Color(.4f,1,.55f));
        if(Health<=0){var loot=LootPickup.Spawn(kind,AdventureRandom.Range(HarvestMinimum,HarvestMaximumExclusive,owner:this)+hero.GetComponent<AdventureLoadout>().HarvestBonus,transform.position+Vector3.up*.5f);UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(loot.gameObject,gameObject.scene);Restore(0);Onboarding.Resource(hero,loot);hero.Inventory.NotifyCategorized(PlayerInventory.Label(kind)+"已掉落，靠近按 "+PlayerInput.Key(PlayerAction.Interact)+" 拾取。",AdventureCatalog.Material(kind).iconKey);}
    }
    void Update(){if(Health>0)transform.localScale=originalScale*(Time.time<flashUntil?1+Mathf.Sin(Time.time*90)*.035f:1);}
    void OnGUI(){var camera=Camera.main;if(camera==null||Health<=0||Vector3.Distance(camera.transform.position,transform.position)>13)return;var hero=FindFirstObjectByType<ThirdPersonHero>();if(hero==null||hero.GameplayPaused||Vector3.Distance(hero.transform.position,transform.position)>4.5f)return;var p=camera.WorldToScreenPoint(transform.position+Vector3.up*2.4f);if(p.z<=0)return;CombatChineseUI.Apply();GUI.Box(new Rect(p.x-72,Screen.height-p.y,144,25),PlayerInventory.Label(kind)+$" {Health:0}/{maxHealth:0}");}
}

