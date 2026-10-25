using System.Collections.Generic;
using System.Linq;
using UnityEngine;

// Renderer ownership only. Never change actor activity, collision, navigation or combat state.
[DefaultExecutionOrder(22000)]
public sealed class CameraActorFade:MonoBehaviour {
 public const float Opacity=.22f;
 public int OccludedActors {get;private set;}
 public int FadedRenderers=>previous.Count;
 public int OwnedMaterialCount=>cache.Count;
 readonly Dictionary<Material,Material> cache=new Dictionary<Material,Material>();
 readonly Dictionary<Renderer,Material[]> previous=new Dictionary<Renderer,Material[]>();
 MaterialPropertyBlock block;
 Material basis;
 void Awake(){block=new MaterialPropertyBlock();}
 public void Refresh(){Restore();OccludedActors=0;var orbit=GetComponent<OrbitCamera>();var hero=orbit.target==null?null:orbit.target.GetComponent<ThirdPersonHero>();
  var flow=hero==null?null:AdventureFlow.Find(hero);
  if(flow?.ActiveRun?.mode!=AdventureMode.ForestExploration){ClearCache();return;}
  Vector3 focus=hero.transform.position+Vector3.up*1.5f;var line=focus-transform.position;float length=line.magnitude;if(length<.01f)return;
  var actors=new HashSet<CombatEnemy>();
  foreach(var hit in Physics.SphereCastAll(transform.position,.45f,line.normalized,Mathf.Max(0,length-.1f),~0,QueryTriggerInteraction.Ignore)){var e=hit.collider.GetComponentInParent<CombatEnemy>();if(e!=null&&!e.Health.Dead&&e.gameObject.scene==hero.gameObject.scene)actors.Add(e);}
  foreach(var c in Physics.OverlapSphere(transform.position,.4f,~0,QueryTriggerInteraction.Ignore)){var e=c.GetComponentInParent<CombatEnemy>();if(e!=null&&!e.Health.Dead&&e.gameObject.scene==hero.gameObject.scene)actors.Add(e);}
  // The rendered 3.3m boss is taller/wider than its navigation capsule. Include
  // visual bounds so shoulders and crowns cannot evade the camera-line check.
  var session=flow.GetComponent<CombatSession>();var bodyHeights=new[]{.35f,1.1f,1.8f};
  foreach(var e in session.enemies){if(e==null||e.Health.Dead)continue;var visual=e.GetComponent<FantasyActorVisual>();if(visual==null||visual.model==null)continue;foreach(var r in visual.model.GetComponentsInChildren<Renderer>()){if(!r.enabled)continue;var bounds=r.bounds;bounds.Expand(.5f);foreach(float height in bodyHeights){var toBody=hero.transform.position+Vector3.up*height-transform.position;if(bounds.IntersectRay(new Ray(transform.position,toBody.normalized),out var d)&&d<toBody.magnitude-.1f){actors.Add(e);break;}}}}
  foreach(var actor in actors){var visual=actor.GetComponent<FantasyActorVisual>();if(visual!=null&&visual.model!=null)Fade(visual.model);var body=actor.GetComponent<Renderer>();if(body!=null&&body.enabled)FadeRenderer(body);foreach(Transform child in actor.transform)if(child.name=="角卫枝冠"||child.name=="潮灵水冠")Fade(child.gameObject);OccludedActors++;}
  if(length<1.2f){var visual=hero.GetComponent<FantasyActorVisual>();if(visual!=null&&visual.model!=null)Fade(visual.model);}
 }
 void Fade(GameObject model){foreach(var r in model.GetComponentsInChildren<Renderer>())if(r.enabled)FadeRenderer(r);}
 void FadeRenderer(Renderer r){
  if(basis==null)basis=Resources.Load<Material>("CombatFeedback/ActorFade");if(basis==null)return;
   var original=r.sharedMaterials;var faded=new Material[original.Length];bool supported=true;
   for(int i=0;i<original.Length;i++){var source=original[i];if(source==null){supported=false;break;}
    if(!cache.TryGetValue(source,out var ghost)){ghost=new Material(basis){name="相机遮挡淡化 · "+source.name};cache.Add(source,ghost);string map=source.HasProperty("_BaseMap")?"_BaseMap":source.HasProperty("_MainTex")?"_MainTex":null;if(map!=null){ghost.SetTexture("_BaseMap",source.GetTexture(map));ghost.SetTextureScale("_BaseMap",source.GetTextureScale(map));ghost.SetTextureOffset("_BaseMap",source.GetTextureOffset(map));}}
    if(source.HasProperty("_BaseColor"))ghost.SetColor("_BaseColor",source.GetColor("_BaseColor"));else if(source.HasProperty("_Color"))ghost.SetColor("_BaseColor",source.GetColor("_Color"));faded[i]=ghost;
   }
   if(!supported)return;previous[r]=original;r.sharedMaterials=faded;r.GetPropertyBlock(block);block.SetFloat("_CameraFade",Opacity);r.SetPropertyBlock(block);
 }
 public void Restore(){foreach(var pair in previous){if(pair.Key==null)continue;var now=pair.Key.sharedMaterials;bool changed=false;for(int i=0;i<now.Length;i++){var match=cache.FirstOrDefault(p=>p.Value==now[i]);if(match.Key!=null){now[i]=match.Key;changed=true;}}if(changed)pair.Key.sharedMaterials=now;}previous.Clear();}
 void ClearCache(){foreach(var m in cache.Values)if(m!=null)Destroy(m);cache.Clear();}
 void LateUpdate(){Refresh();}
 void OnDisable(){Restore();ClearCache();OccludedActors=0;}
 void OnDestroy(){Restore();ClearCache();}
}
