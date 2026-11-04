using System;using UnityEngine;
[DefaultExecutionOrder(500)]
public sealed class NewWeaponVisual:MonoBehaviour {
 ThirdPersonHero hero;GameObject right,left;Transform rh,lh;Quaternion rr,lr;bool posed;float started,duration;int hand;bool moving;GearType type;
 public bool Ready=>right!=null&&(type!=GearType.TwinBlades||left!=null)&&rh!=null&&lh!=null;public Transform Right=>right?.transform;public Transform Left=>left?.transform;
 void Awake(){hero=GetComponent<ThirdPersonHero>();}
 public void Rebuild(GearType type,GameObject model){Hide();this.type=type;if(!NewWeaponRegistry.Is(type)||model==null)return;foreach(var bone in model.GetComponentsInChildren<Transform>(true)){if(bone.name=="1H_Sword"||bone.name=="1H_Sword_Offhand"||bone.name=="Badge_Shield")bone.gameObject.SetActive(false);if(bone.name=="handslot.r")rh=bone;if(bone.name=="handslot.l")lh=bone;}var prefab=Resources.Load<GameObject>("NewWeapons/Models/"+NewWeaponRegistry.Icon(type));if(prefab==null||rh==null||lh==null){Debug.LogError("NEW_WEAPON_VISUAL_BINDING_MISSING "+type);return;}right=Instantiate(prefab,rh,false);right.name=NewWeaponRegistry.Name(type)+"·右手";if(type==GearType.TwinBlades){left=Instantiate(prefab,lh,false);left.name="双刃·左手";left.transform.localRotation=Quaternion.Euler(0,180,0);}}
 public void BeginMotion(int hand,float duration){this.hand=hand;this.duration=duration;started=Time.time;moving=true;}
 public void StopMotion(){moving=false;Restore();}
 void Update(){Restore();}
 void Restore(){if(!posed)return;if(rh!=null)rh.localRotation=rr;if(lh!=null)lh.localRotation=lr;posed=false;}
 void LateUpdate(){if(!Ready||!moving||hero.Health.Dead||hero.GameplayPaused)return;float t=(Time.time-started)/Mathf.Max(.01f,duration);if(t>=1){moving=false;return;}rr=rh.localRotation;lr=lh.localRotation;posed=true;float swing=Mathf.Sin(t*Mathf.PI)*(type==GearType.Greatsword?115:80);rh.localRotation=rr*Quaternion.Euler(hand==1?0:swing,0,hand==2?-swing*.4f:0);lh.localRotation=lr*Quaternion.Euler(hand==0?0:-swing,0,hand==2?swing*.4f:0);}
 public void Hide(){Restore();moving=false;if(right!=null){right.SetActive(false);Destroy(right);}if(left!=null){left.SetActive(false);Destroy(left);}right=left=null;rh=lh=null;}
 void OnDisable(){Hide();}void OnDestroy(){Hide();}
}
public sealed class NewWeaponTrace:MonoBehaviour {
 Material material;ThirdPersonHero owner;float age;
 public static void Capsule(Vector3 a,Vector3 b,float r,UnityEngine.SceneManagement.Scene scene,ThirdPersonHero owner,Color color){var g=new GameObject("新武器实际胶囊边界");UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(g,scene);var t=g.AddComponent<NewWeaponTrace>();t.owner=owner;t.material=new Material(Shader.Find("Universal Render Pipeline/Unlit")){color=color};var line=g.AddComponent<LineRenderer>();line.sharedMaterial=t.material;line.startWidth=line.endWidth=.025f;line.positionCount=51;for(int i=0;i<25;i++){float angle=i*Mathf.PI*2/24;line.SetPosition(i,a+new Vector3(Mathf.Cos(angle)*r,0,Mathf.Sin(angle)*r));line.SetPosition(25+i,b+new Vector3(Mathf.Cos(angle)*r,0,Mathf.Sin(angle)*r));}line.SetPosition(50,a+Vector3.right*r);}
 void Update(){if(owner==null||owner.Health.Dead){Destroy(gameObject);return;}if(owner.GameplayPaused||Time.timeScale<=0)return;age+=Time.deltaTime;if(age>=.19f)Destroy(gameObject);}
 void OnDestroy(){if(material!=null)Destroy(material);}
}
