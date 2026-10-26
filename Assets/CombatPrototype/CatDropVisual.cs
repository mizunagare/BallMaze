using UnityEngine;
// Only the world mesh changes. Loot ID, save position, pickup range and source ledger are untouched.
public sealed class CatDropVisual:MonoBehaviour {
 LootPickup loot;GameObject model;string prior;
 void Awake(){loot=GetComponent<LootPickup>();}
 void LateUpdate(){if(loot==null)return;string key=loot.Gear!=null?loot.Gear.Icon:AdventureCatalog.Material(loot.Kind).iconKey;if(prior==key)return;prior=key;if(model!=null){model.SetActive(false);Destroy(model);}var prefab=Resources.Load<GameObject>("CatWorld/Props/"+key);if(prefab==null)return;var old=GetComponent<Renderer>();if(old!=null)old.enabled=false;model=Instantiate(prefab,transform,false);model.name="猫族世界掉落模型";model.transform.localScale=Vector3.one*1.5f;}
}
