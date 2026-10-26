using UnityEngine;
// Title-only stage: no CombatSession, controllers, save initializer or gameplay HUD.
public static class CatTitleStage {
 public static void Build(Transform parent){Spawn(parent,"Hero",new Vector3(4,0,7),145,.95f);Spawn(parent,"Keeper",new Vector3(1.8f,0,10),165,.8f);Spawn(parent,"Smith",new Vector3(6.5f,0,11),135,.8f);Prop(parent,"warehouse",new Vector3(1, .4f,11),1.4f);Prop(parent,"workbench",new Vector3(7,.7f,10),1.7f);CatWorldArt.Part(parent,"营地归途旗","Box",new Vector3(3,2,11),new Vector3(1.1f,.6f,.08f),"Red");CatWorldArt.Part(parent,"旗杆","Box",new Vector3(2.5f,1.3f,11),new Vector3(.09f,2.6f,.09f),"Wood");}
 static void Spawn(Transform p,string kind,Vector3 position,float yaw,float scale){var prefab=Resources.Load<GameObject>("CatWorld/Actors/"+kind);if(prefab==null)return;var g=Object.Instantiate(prefab,p,false);g.name="标题营地 · "+kind;g.transform.localPosition=position;g.transform.localRotation=Quaternion.Euler(0,yaw,0);g.transform.localScale=Vector3.one*scale;}
 static void Prop(Transform p,string key,Vector3 position,float scale){var prefab=Resources.Load<GameObject>("CatWorld/Props/"+key);if(prefab==null)return;var g=Object.Instantiate(prefab,p,false);g.transform.localPosition=position;g.transform.localScale=Vector3.one*scale;}
}
