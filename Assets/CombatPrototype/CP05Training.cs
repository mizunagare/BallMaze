using System;using System.Collections;using UnityEngine;using UnityEngine.SceneManagement;using UnityEngine.UI;using UnityEngine.EventSystems;
// Explicit, isolated playable training feature. Not a save/settlement or victory harness.
public sealed class CP05TrainingMarker:MonoBehaviour {}
public sealed class CP05Training : MonoBehaviour {
 public static CP05Training Instance {get;private set;}
 public ThirdPersonHero Hero {get;private set;}public CombatEnemy[] Enemies {get;private set;}public string Error {get;private set;}
 static string ownedRoot;Text status;bool restarting;Scene arena;int generation;
 readonly string sceneScope=Guid.NewGuid().ToString("N");
 public bool Restarting=>restarting;
 public string NextSceneName=>"CP05 Independent Training "+sceneScope+" "+(generation+1);
 sealed class Swap {
  public Scene oldScene,newScene;public ThirdPersonHero oldHero;public CombatEnemy[] oldEnemies;public Text oldStatus;
  public GameObject[] roots;public bool[] active;public float oldScale;public bool built;
  public System.Collections.Generic.List<Material> oldMaterials,newMaterials;
 }
 Swap pending;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]static void ResetTraining(){SceneManager.sceneLoaded-=Loaded;Instance=null;ownedRoot=null;}
 void Awake(){if(Instance!=null&&Instance!=this){Destroy(gameObject);return;}Instance=this;SceneManager.sceneUnloaded+=Unloaded;}
 void Unloaded(Scene scene){if(!restarting&&arena.IsValid()&&scene.handle==arena.handle)Destroy(gameObject);}
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]static void Entry(){if(Array.IndexOf(Environment.GetCommandLineArgs(),"-cp05-training")<0)return;try{ownedRoot=ValidationStorage.Root(Environment.GetCommandLineArgs(),true);if(string.IsNullOrEmpty(ownedRoot))throw new Exception("isolated storage required");SceneManager.sceneLoaded+=Loaded;}catch(Exception e){Debug.LogError("CP05_TRAINING_REJECTED "+e);if(!Application.isEditor)Application.Quit(2);}}
 static void Loaded(Scene scene,LoadSceneMode mode){if(scene.path!=GameEntry.TitlePath)return;SceneManager.sceneLoaded-=Loaded;StartIsolated();}
 public static void StartIsolated(){if(Instance!=null)return;ownedRoot=ValidationStorage.Root(Environment.GetCommandLineArgs(),true);if(string.IsNullOrEmpty(ownedRoot))throw new Exception("isolated storage required");if(UnityEngine.Object.FindFirstObjectByType<CombatSession>()!=null)throw new InvalidOperationException("请先正常返回标题，再进入独立训练。");var go=new GameObject("CP05 Training Launcher");DontDestroyOnLoad(go);go.AddComponent<CP05Training>();}
 IEnumerator Start(){yield return null;yield return Restart();}
 public bool RequestRestart(){if(restarting)return false;StartCoroutine(Restart());return true;}
 IEnumerator Replace(Swap swap){
  if(UnityEngine.Object.FindFirstObjectByType<CombatSession>()!=null)throw new InvalidOperationException("正式冒险存在时不能重开训练。");
  swap.oldScene=arena.IsValid()&&arena.isLoaded?arena:SceneManager.GetActiveScene();
  if(!arena.IsValid()&&swap.oldScene.path!=GameEntry.TitlePath)throw new InvalidOperationException("独立训练只从标题场景初始化。");
  swap.oldHero=Hero;swap.oldEnemies=Enemies;swap.oldStatus=status;swap.oldMaterials=ownedMaterials;swap.oldScale=Time.timeScale;
  string name=NextSceneName;generation++;swap.newScene=SceneManager.CreateScene(name);
  swap.roots=swap.oldScene.GetRootGameObjects();swap.active=new bool[swap.roots.Length];
  for(int i=0;i<swap.roots.Length;i++){swap.active[i]=swap.roots[i].activeSelf;swap.roots[i].SetActive(false);}
  SceneManager.SetActiveScene(swap.newScene);swap.newMaterials=new System.Collections.Generic.List<Material>();ownedMaterials=swap.newMaterials;
  Create(swap.newScene);
  if(Hero==null||Enemies==null||Enemies.Length!=2||TrainingLootContext.For(Hero)==null)throw new InvalidOperationException("训练新实例未完整建立。");
  swap.built=true;var unload=SceneManager.UnloadSceneAsync(swap.oldScene);if(unload==null)throw new InvalidOperationException("旧训练场无法卸载。");yield return unload;
  if(swap.oldScene.isLoaded)throw new InvalidOperationException("旧训练场卸载未完成。");
  arena=swap.newScene;ReleaseMaterials(swap.oldMaterials);Time.timeScale=1;Error=null;
  Debug.Log("CP05_TRAINING_READY stage="+CombatAssistOptions.Stage+" storage="+ownedRoot);
 }
 IEnumerator Restart(){
  if(restarting)yield break;restarting=true;PlayerInput.Barrier();Error=null;var swap=new Swap();pending=swap;var steps=Replace(swap);Exception failure=null;
  try{
   while(true){bool next=false;object current=null;try{next=steps.MoveNext();if(next)current=steps.Current;}catch(Exception e){failure=e;break;}if(!next)break;yield return current;}
   if(failure!=null){AsyncOperation cleanup=null;try{cleanup=Recover(swap);}catch(Exception recovery){failure=new AggregateException(failure,recovery);}if(cleanup!=null)yield return cleanup;Error="训练重开未完成，已保留可用实例，可再次重试："+failure.Message;Debug.LogWarning("CP05_TRAINING_RETRYABLE "+failure);}
  }finally{(steps as IDisposable)?.Dispose();pending=null;restarting=false;}
 }
 AsyncOperation Recover(Swap swap){
  if(swap.oldScene.IsValid()&&swap.oldScene.isLoaded){
   if(swap.newScene.IsValid()&&swap.newScene.isLoaded)foreach(var root in swap.newScene.GetRootGameObjects())root.SetActive(false);
   SceneManager.SetActiveScene(swap.oldScene);Hero=swap.oldHero;Enemies=swap.oldEnemies;status=swap.oldStatus;ownedMaterials=swap.oldMaterials;
   if(swap.roots!=null)for(int i=0;i<swap.roots.Length;i++)if(swap.roots[i]!=null)swap.roots[i].SetActive(swap.active[i]);
   ReleaseMaterials(swap.newMaterials);Time.timeScale=swap.oldScale;
   return swap.newScene.IsValid()&&swap.newScene.isLoaded?SceneManager.UnloadSceneAsync(swap.newScene):null;
  }
  if(swap.built&&swap.newScene.IsValid()&&swap.newScene.isLoaded){arena=swap.newScene;ownedMaterials=swap.newMaterials;ReleaseMaterials(swap.oldMaterials);Time.timeScale=1;}
  return null;
 }
 static void ReleaseMaterials(System.Collections.Generic.List<Material> materials){if(materials==null)return;foreach(var material in materials)if(material!=null)Destroy(material);materials.Clear();}
 void Create(Scene scene){
  var hp=Resources.Load<GameObject>("CP05Training/Hero");var ep=Resources.Load<GameObject>("CP05Training/Enemy");if(hp==null||ep==null)throw new Exception("Training assets absent");
  var loot=new GameObject("Training temporary loot context").AddComponent<TrainingLootContext>();loot.Initialize(AdventureRandom.NewSeed());
  Box("Ground",new Vector3(0,-.5f,10),new Vector3(40,1,65),new Color(.22f,.32f,.25f));Box("Wall",new Vector3(-3,1.5f,8),new Vector3(2,3,1),Color.gray);Box("Rock",new Vector3(3,.7f,5),new Vector3(1.5f,1.4f,1.5f),new Color(.4f,.45f,.45f));
  new GameObject("Training Combat Feedback").AddComponent<CombatFeedback>();
  var light=new GameObject("Training Sun").AddComponent<Light>();light.type=LightType.Directional;light.intensity=1.2f;light.transform.rotation=Quaternion.Euler(45,-25,0);
  var g=Instantiate(hp,new Vector3(0,.15f,0),Quaternion.identity);Hero=g.GetComponent<ThirdPersonHero>();g.AddComponent<CP05TrainingMarker>();loot.BindHero(Hero);
  var camera=new GameObject("Training Camera",typeof(Camera),typeof(AudioListener));camera.tag="MainCamera";var c=camera.GetComponent<Camera>();c.fieldOfView=65;c.nearClipPlane=.05f;c.farClipPlane=160;var orbit=camera.AddComponent<OrbitCamera>();orbit.target=Hero.transform;Hero.cameraTransform=camera.transform;
  Enemies=new CombatEnemy[2];for(int i=0;i<2;i++){var enemy=Instantiate(ep,new Vector3(i==0?-1.5f:2.5f,.15f,i==0?8:15),Quaternion.identity).GetComponent<CombatEnemy>();enemy.entityId="training:"+i;enemy.target=Hero;Enemies[i]=enemy;}
  UI();
 }
 void Box(string name,Vector3 pos,Vector3 size,Color color){var g=GameObject.CreatePrimitive(PrimitiveType.Cube);g.name=name;g.transform.position=pos;g.transform.localScale=size;var m=new Material(Shader.Find("Universal Render Pipeline/Lit")){color=color};g.GetComponent<Renderer>().sharedMaterial=m;ownedMaterials.Add(m);}
 System.Collections.Generic.List<Material> ownedMaterials=new System.Collections.Generic.List<Material>();
 void UI(){var c=new GameObject("Training Controls",typeof(Canvas),typeof(CanvasScaler),typeof(GraphicRaycaster));c.GetComponent<Canvas>().renderMode=RenderMode.ScreenSpaceOverlay;c.GetComponent<CanvasScaler>().uiScaleMode=CanvasScaler.ScaleMode.ScaleWithScreenSize;c.GetComponent<CanvasScaler>().referenceResolution=new Vector2(1280,720);
  new GameObject("Training EventSystem",typeof(EventSystem),typeof(UnityEngine.InputSystem.UI.InputSystemUIInputModule));
  Button(c.transform,"原镜头 / 肩后",12,()=>{Hero.cameraTransform.GetComponent<OrbitCamera>().shoulderMode=!Hero.cameraTransform.GetComponent<OrbitCamera>().shoulderMode;});Button(c.transform,"远程辅助 / 自由",190,()=>CombatAssistOptions.Ranged=!CombatAssistOptions.Ranged).interactable=CombatAssistOptions.Stage!="B1";Button(c.transform,"近战辅助 / 自由",368,()=>CombatAssistOptions.Melee=!CombatAssistOptions.Melee).interactable=CombatAssistOptions.Stage=="B3";
  for(int i=0;i<4;i++){int t=i;Button(c.transform,new[]{"剑","枪","杖","弓"}[i],550+i*70,()=>{var gear=Hero.GetComponent<AdventureLoadout>();var item=gear.items.Find(x=>x.type==(GearType)t&&x.Weapon&&x.InBag);if(item!=null)gear.SelectMain(item);},64);}
  Button(c.transform,"重开训练",860,()=>RequestRestart(),120);
  var info=new GameObject("Training Status",typeof(RectTransform),typeof(Text));info.transform.SetParent(c.transform,false);var ir=info.GetComponent<RectTransform>();ir.anchorMin=ir.anchorMax=new Vector2(0,1);ir.pivot=new Vector2(0,1);ir.anchoredPosition=new Vector2(12,-94);ir.sizeDelta=new Vector2(1000,24);status=info.GetComponent<Text>();status.font=CatUI.Font;status.fontSize=16;status.raycastTarget=false;
  var text=new GameObject("Training help",typeof(RectTransform),typeof(Text));text.transform.SetParent(c.transform,false);var tr=text.GetComponent<RectTransform>();tr.anchorMin=tr.anchorMax=new Vector2(0,1);tr.pivot=new Vector2(0,1);tr.anchoredPosition=new Vector2(12,-55);tr.sizeDelta=new Vector2(1000,70);var label=text.GetComponent<Text>();label.font=CatUI.Font;label.fontSize=17;label.text="CP05 "+CombatAssistOptions.Stage+" · Esc释放鼠标操作按钮，右键捕获镜头\nWASD移动 / 普攻与技能沿用当前键位。独立训练无正式存档或结算。";label.raycastTarget=false;
  var dot=new GameObject("Reticle",typeof(RectTransform),typeof(Image));dot.transform.SetParent(c.transform,false);dot.GetComponent<RectTransform>().sizeDelta=new Vector2(5,5);dot.GetComponent<Image>().raycastTarget=false;
 }
 UnityEngine.UI.Button Button(Transform parent,string title,float x,Action action,float width=170){var g=new GameObject(title,typeof(RectTransform),typeof(Image),typeof(Button));g.transform.SetParent(parent,false);var r=g.GetComponent<RectTransform>();r.anchorMin=r.anchorMax=new Vector2(0,1);r.pivot=new Vector2(0,1);r.anchoredPosition=new Vector2(x,-12);r.sizeDelta=new Vector2(width,32);g.GetComponent<Image>().color=new Color(.16f,.22f,.2f,.95f);g.GetComponent<Button>().onClick.AddListener(()=>{Hero.GetComponent<AdventureCombat>().CancelPending();PlayerInput.Barrier();action();});var l=new GameObject("Text",typeof(RectTransform),typeof(Text));l.transform.SetParent(g.transform,false);var lr=l.GetComponent<RectTransform>();lr.anchorMin=Vector2.zero;lr.anchorMax=Vector2.one;lr.offsetMin=lr.offsetMax=Vector2.zero;var t=l.GetComponent<Text>();t.font=CatUI.Font;t.fontSize=16;t.alignment=TextAnchor.MiddleCenter;t.text=title;t.raycastTarget=false;return g.GetComponent<UnityEngine.UI.Button>();}
 void Update(){if(status!=null&&Hero!=null)status.text="生命 "+Hero.Health.Current.ToString("0")+" / "+Hero.Health.maxHealth.ToString("0")+" · 远程辅助 "+(CombatAssistOptions.Ranged?"开":"关")+" · 近战辅助 "+(CombatAssistOptions.Melee?"开":"关")+(Hero.Health.Dead?" · 已倒下，可重开训练":"")+(string.IsNullOrEmpty(Error)?" · 临时掉落，无波次加成":" · "+Error);}
 void OnDestroy(){SceneManager.sceneUnloaded-=Unloaded;if(Instance==this)Instance=null;ReleaseMaterials(ownedMaterials);if(pending!=null){ReleaseMaterials(pending.oldMaterials);ReleaseMaterials(pending.newMaterials);}}
}
