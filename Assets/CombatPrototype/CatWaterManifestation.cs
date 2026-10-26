using UnityEngine;
[DefaultExecutionOrder(23000)]
public sealed class CatWaterManifestation:MonoBehaviour {
 GameObject previous;
 void LateUpdate(){var brain=GetComponent<ForestBossBrain>();var water=brain?.VisualManifestation;if(water==null||water==previous)return;previous=water;var prefab=Resources.Load<GameObject>("CatWorld/Actors/Tide");if(prefab==null)return;var renderer=water.GetComponent<Renderer>();if(renderer!=null)renderer.enabled=false;var cat=Instantiate(prefab,water.transform,false);cat.name="湖心潮灵猫 · 水面显灵（仅表现）";cat.transform.localPosition=Vector3.down*.4f;cat.transform.localScale=new Vector3(.65f,.45f,.65f);}
}
