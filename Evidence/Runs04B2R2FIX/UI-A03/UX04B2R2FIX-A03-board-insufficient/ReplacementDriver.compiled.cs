// UX04B2R2FIX observation SIDECAR. Never ship. No auto-build or auto-launch.
// SETUP uses normal GameEntry/factory/Add/Place APIs. TEST uses physical InputSystem
// events -> EventSystem -> product Buttons. Supplemental API probes are labelled.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.UI;

namespace B2R2FixReplacement
{
 public sealed class Driver : MonoBehaviour
 {
  [Serializable] public class Config { public string runId, mode, buildId, dllSHA256, driverSHA256, exeSHA256; }
  static string root;
  Config cfg;
  CombatSession session; ThirdPersonHero hero; AdventureLoadout gear; PlayerInventory inv;
  GearItem candidate, old, companion;
  B2EquipRole role; Vector2Int target; int turn;
  bool failed, finished; int seq, checks, passes;
  string error="", observedEvaluation="null", commitText="";
  string productHash,driverHash,exeHash;
  [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
  public static void Boot() {
   string p=Environment.GetEnvironmentVariable("UNITY_TEST_ROOT");
   if(string.IsNullOrEmpty(p)||!File.Exists(Path.Combine(p,"replacement-config.json")))return;
   root=p; Application.runInBackground=true;
   var go=new GameObject("UX04B2R2FIX replacement observer"); DontDestroyOnLoad(go);go.AddComponent<Driver>();
  }
  static string F(float n)=>n.ToString("R",CultureInfo.InvariantCulture);
  static string Q(string s) { if(s==null)return "null";return "\""+s.Replace("\\","\\\\").Replace("\"","\\\"").Replace("\r","\\r").Replace("\n","\\n").Replace("\t","\\t")+"\""; }
  static string B(bool b)=>b?"true":"false";
  static string J(object o)=>o==null?"null":JsonUtility.ToJson(o);
  static string Hash(string s) { unchecked { ulong h=14695981039346656037UL;foreach(char c in s){h^=c;h*=1099511628211UL;}return h.ToString("x16"); } }
  static string SHA(string p) { using(var a=SHA256.Create())using(var s=File.OpenRead(p))return BitConverter.ToString(a.ComputeHash(s)).Replace("-","").ToLowerInvariant(); }
  static string Dict(Dictionary<string,string> d)=>"{"+string.Join(",",d.OrderBy(x=>x.Key,StringComparer.Ordinal).Select(x=>Q(x.Key)+":"+Q(x.Value)))+"}";
  void Append(string file,string json)=>File.AppendAllText(Path.Combine(root,file),json+"\n");
  void Event(string kind,string detail) { Append("input-events.jsonl","{\"kind\":"+Q(kind)+",\"detail\":"+Q(detail)+",\"frame\":"+Time.frameCount+",\"realtime\":"+F(Time.realtimeSinceStartup)+"}"); }
  void Check(string name,bool ok,string detail) {
   checks++;if(ok)passes++;else{failed=true;error+=name+": "+detail+"\n";}
   Append("checks.jsonl","{\"name\":"+Q(name)+",\"pass\":"+B(ok)+",\"detail\":"+Q(detail)+"}");
  }
  void Require(bool ok,string detail) { Check(detail,ok,detail);if(!ok)throw new InvalidOperationException(detail); }
  IEnumerator Frames(int n=6){float until=Time.realtimeSinceStartup+.12f;for(int i=0;i<n||Time.realtimeSinceStartup<until;i++)yield return null;}
  // Complete item serialized fields plus independently readable derived fields and geometry.
  string Item(GearItem i) {
   if(i==null)return "null";
   return "{\"fields\":"+J(i)+",\"attack\":"+F(i.Attack)+",\"defense\":"+F(i.Defense)+",\"inBag\":"+B(i.InBag)+",\"weapon\":"+B(i.Weapon)+",\"container\":"+B(i.Container)+",\"definition\":"+J(i.Definition)+",\"size\":"+J(i.Size)+",\"cells\":["+string.Join(",",i.Cells(i.rotation).Select(p=>"["+p.x+","+p.y+"]"))+"]}";
  }
  string Items(IEnumerable<GearItem> items)=>"["+string.Join(",",items.Select(Item))+"]";
  string Scalars(object o) {
   var d=new Dictionary<string,string>();
   foreach(var f in o.GetType().GetFields(BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic).OrderBy(x=>x.Name,StringComparer.Ordinal)) {
    Type t=f.FieldType;
    if(t.IsPrimitive||t.IsEnum||t==typeof(string)||t==typeof(decimal)) {
     object v=f.GetValue(o);d[f.Name]=v==null?null:v is float?F((float)v):Convert.ToString(v,CultureInfo.InvariantCulture);
    }
   } return Dict(d);
  }
  string NotificationRaw() {
   var queue=inv.Notifications;var field=queue.GetType().GetField("pickups",BindingFlags.Instance|BindingFlags.NonPublic);
   var pickups=(System.Collections.IDictionary)field.GetValue(queue);var entries=new List<string>();
   foreach(System.Collections.DictionaryEntry e in pickups)entries.Add("{\"kind\":"+Convert.ToInt32(e.Key)+",\"amount\":"+Convert.ToInt32(e.Value)+"}");
   return "{\"allScalarFields\":"+Scalars(queue)+",\"pickupsOrdered\":["+string.Join(",",entries)+"]}";
  }
  string InventoryRaw()=>"{\"notifications\":"+NotificationRaw()+",\"warehouseItems\":"+Items(AdventureRecipes.Camp(hero).Items)+",\"campMaterials\":["+string.Join(",",AdventureRecipes.Camp(hero).Materials)+"],\"serialized\":"+J(inv)+",\"allScalarFields\":"+Scalars(inv)+",\"materialsOrdered\":["+string.Join(",",inv.Materials.Select(J))+"],\"gearItemOrder\":["+string.Join(",",gear.items.Select(i=>Q(i.id)))+"],\"healthPotions\":"+inv.HealthPotionCount+",\"quickbar\":"+B(inv.PotionOnQuickbar)+",\"cooldownRemaining\":"+F(inv.PotionCooldownRemaining)+",\"isOpen\":"+B(inv.IsOpen)+",\"page\":"+Q(inv.CurrentPage.ToString())+"}";
  Dictionary<string,string> Nine() {
   var d=new Dictionary<string,string>();
   d["GearItem"]=Items(gear.items.OrderBy(i=>i.id,StringComparer.Ordinal));
   d["Inventory"]=InventoryRaw();
   d["EquipmentGrid"]="["+string.Join(",",gear.items.OrderBy(i=>i.id,StringComparer.Ordinal).Select(i=>"{\"id\":"+Q(i.id)+",\"x\":"+i.x+",\"y\":"+i.y+",\"rotation\":"+i.rotation+",\"board\":"+B(i.board)+",\"worn\":"+B(i.worn)+",\"overflow\":"+B(i.overflow)+",\"cells\":["+string.Join(",",i.Cells(i.rotation).Select(p=>"["+(p.x+i.x)+","+(p.y+i.y)+"]"))+"]}"))+"]";
   d["Main"]="{\"id\":"+Q(gear.mainWeapon)+",\"item\":"+Item(gear.Main)+"}";
   d["Reserve"]="{\"id\":"+Q(gear.reserveWeapon)+",\"item\":"+Item(gear.Reserve)+"}";
   d["Worn"]=Items(gear.items.Where(i=>i.worn).OrderBy(i=>i.id,StringComparer.Ordinal));
   d["Overflow"]=Items(gear.items.Where(i=>i.overflow).OrderBy(i=>i.id,StringComparer.Ordinal));
   d["AttackPower"]="{\"attackPower\":"+F(hero.AttackPower)+",\"defense\":"+F(hero.Defense)+",\"loadoutAttack\":"+F(gear.Attack)+",\"loadoutDefense\":"+F(gear.Defense)+",\"baseDamage\":"+F(hero.attackDamage)+",\"strengthRank\":"+hero.Progression.Rank(BasicSkill.Strength)+",\"progressionBonus\":"+F(hero.Progression.AttackBonus)+",\"basicPower\":"+F(hero.GetComponent<AdventureCombat>().BasicPower)+",\"snapshot\":"+J(gear.AttackSnapshot())+"}";
   d["Container"]="{\"rig\":"+J(gear.Rig)+",\"bag\":"+J(gear.Bag)+"}";
   return d;
  }
  string RandomRaw() {
   var training=UnityEngine.Object.FindObjectsByType<TrainingLootContext>(FindObjectsSortMode.None).FirstOrDefault(c=>c.gameObject.scene==hero.gameObject.scene);
   object streams=training==null?null:typeof(TrainingLootContext).GetProperty("Streams",BindingFlags.Instance|BindingFlags.NonPublic|BindingFlags.Public).GetValue(training,null);
   return "{\"unityState\":"+J(UnityEngine.Random.state)+",\"activeRun\":"+J(session.Flow.ActiveRun)+",\"trainingStreams\":"+J(streams)+"}";
  }
  string SavesRaw() {
   string dir=Path.GetDirectoryName(session.Saves.SavePath);
   return "["+string.Join(",",Directory.GetFiles(dir,"*",SearchOption.AllDirectories).OrderBy(x=>x,StringComparer.Ordinal).Select(p=>"{\"relativePath\":"+Q(p.Substring(dir.Length).Replace('\\','/'))+",\"bytes\":"+new FileInfo(p).Length+",\"sha256\":"+Q(SHA(p))+",\"base64\":"+Q(Convert.ToBase64String(File.ReadAllBytes(p)))+"}"))+"]";
  }
  class State {
   public Dictionary<string,string> raw;public string random,saves,json;
  }
  State Capture() {
   var s=new State{raw=Nine(),random=RandomRaw(),saves=SavesRaw()};
   var hashes=s.raw.ToDictionary(x=>x.Key,x=>Hash(x.Value));
   s.json="{\"canonical\":"+Dict(s.raw)+",\"fingerprints\":"+Dict(hashes)+",\"random\":"+s.random+",\"saveFiles\":"+s.saves+",\"itemsOrdered\":"+Items(gear.items)+",\"warehouse\":"+Items(AdventureRecipes.Camp(hero).Items)+"}";
   return s;
  }
  bool Same(State a,State b)=>a.raw.All(x=>b.raw[x.Key]==x.Value)&&a.random==b.random&&a.saves==b.saves;
  void Observe(string stage,string detail,State s=null) {
   Append("observations.jsonl","{\"seq\":"+(++seq)+",\"stage\":"+Q(stage)+",\"detail\":"+Q(detail)+",\"frame\":"+Time.frameCount+",\"runId\":"+Q(cfg.runId)+",\"mode\":"+Q(cfg.mode)+",\"buildId\":"+Q(cfg.buildId)+",\"state\":"+(s==null?"null":s.json)+"}");
  }
  string UIRequestJson() {
   // Observe product UI session fields only; never assign request values or invoke handlers.
   var request=ContainerInventoryView.Replacement;
   return "{\"mode\":"+Q(request.replace?"Replace":"Add")+",\"candidateGearId\":"+Q(request.candidateId)+",\"replacedGearId\":"+Q(request.replacedId)+",\"target\":{\"x\":"+request.target.x+",\"y\":"+request.target.y+"},\"rotation\":"+request.rotation+",\"role\":"+Q(request.role.ToString())+",\"roleValue\":"+(int)request.role+",\"evaluated\":"+B(request.evaluated)+"}";
  }
  void Change(string tag,State a,State b,string eval,string result) {
   Append("state-changes.jsonl","{\"tag\":"+Q(tag)+",\"request\":"+(tag.StartsWith("UI-",StringComparison.Ordinal)?UIRequestJson():"null")+",\"before\":"+a.json+",\"after\":"+b.json+",\"allNineEqual\":"+B(a.raw.All(x=>b.raw[x.Key]==x.Value))+",\"randomEqual\":"+B(a.random==b.random)+",\"saveEqual\":"+B(a.saves==b.saves)+",\"evaluation\":"+eval+",\"uiResult\":"+Q(result)+"}");
  }
  Button Button(string name)=>UnityEngine.Object.FindObjectsByType<Button>(FindObjectsInactive.Include,FindObjectsSortMode.None).FirstOrDefault(b=>b.gameObject.activeInHierarchy&&b.name==name);
  Vector2 Centre(RectTransform rt) {
   var c=rt.GetComponentInParent<Canvas>();var cam=c!=null&&c.renderMode!=RenderMode.ScreenSpaceOverlay?c.worldCamera:null;
   var pts=new Vector3[4];rt.GetWorldCorners(pts);return RectTransformUtility.WorldToScreenPoint(cam,(pts[0]+pts[2])*.5f);
  }
  bool Hit(Button b,Vector2 p,out string first) {
   var es=EventSystem.current;var hits=new List<RaycastResult>();es.RaycastAll(new PointerEventData(es){position=p},hits);
   first=hits.Count==0?"none":hits[0].gameObject.name;
   return hits.Count>0&&hits[0].gameObject.GetComponentInParent<Button>()==b;
  }
  Mouse MouseDevice(){if(Mouse.current==null)InputSystem.AddDevice<Mouse>();return Mouse.current;}
  IEnumerator Click(string suffix) {
   string name="ReplacementPreview:"+suffix;var b=Button(name);Require(b!=null,"button exists "+name);
   var es=EventSystem.current;Require(es!=null&&es.currentInputModule!=null&&es.currentInputModule.isActiveAndEnabled&&es.currentInputModule.GetType().Name=="InputSystemUIInputModule","real active InputSystem EventSystem");
   // Real wheel events, never set ScrollRect.normalizedPosition or invoke handlers.
   string first;Vector2 at=Centre(b.GetComponent<RectTransform>());
   for(int n=0;n<80&&!Hit(b,at,out first);n++) {
    var scroll=b.GetComponentInParent<ScrollRect>();if(scroll==null)break;
    Vector2 wheelAt=Centre(scroll.viewport!=null?scroll.viewport:scroll.GetComponent<RectTransform>());
    float delta=at.y>wheelAt.y?8f:-8f;
    Event("mouse-wheel",name+" step="+n+" viewportCentreX="+F(wheelAt.x)+" viewportCentreY="+F(wheelAt.y)+" targetCentreX="+F(at.x)+" targetCentreY="+F(at.y)+" delta="+F(delta));
    InputSystem.QueueStateEvent(MouseDevice(),new MouseState{position=wheelAt,scroll=new Vector2(0,delta)});yield return Frames(3);
    at=Centre(b.GetComponent<RectTransform>());
   }
   bool hit=Hit(b,at,out first);Event("ugui-raycast",name+" firstHit="+first+" accepted="+hit+" interactable="+b.interactable);
   Require(hit&&b.interactable,"clickable top raycast "+name);
   Event("mouse-down",name+" x="+F(at.x)+" y="+F(at.y));
   InputSystem.QueueStateEvent(MouseDevice(),new MouseState{position=at}.WithButton(MouseButton.Left));yield return Frames(2);
   InputSystem.QueueStateEvent(MouseDevice(),new MouseState{position=at});Event("mouse-up",name+" x="+F(at.x)+" y="+F(at.y));yield return Frames(4);
  }
  string Text(string name) {
   var t=UnityEngine.Object.FindObjectsByType<Text>(FindObjectsInactive.Include,FindObjectsSortMode.None).FirstOrDefault(x=>x.gameObject.activeInHierarchy&&x.name=="ReplacementPreview:"+name);
   return t==null?"":t.text;
  }
  object UIValue(string name) {
   // Read ONLY product UI result; no UI handler or Apply calls from this sidecar.
   var model=ContainerInventoryView.Replacement;
   var property=model.GetType().GetProperty(name,BindingFlags.Public|BindingFlags.Instance);
   return property==null?null:property.GetValue(model,null);
  }
  B2AttackEvaluation ReadEvaluation() {
   object v=UIValue("LastEvaluation");Require(v is B2AttackEvaluation,"product UI exposes LastEvaluation");return (B2AttackEvaluation)v;
  }
  string EvalJson(B2AttackEvaluation e)=>J(e).TrimEnd('}')+",\"candidateGearId\":"+Q(e.candidateGearId)+",\"replacedGearId\":"+Q(e.replacedGearId)+",\"oldContribution\":"+F(e.oldContribution)+",\"newContribution\":"+F(e.newContribution)+",\"oldContributionAfter\":"+F(e.oldContributionAfter)+",\"newContributionBefore\":"+F(e.newContributionBefore)+",\"capacityBefore\":"+e.capacityBefore+",\"capacityAfter\":"+e.capacityAfter+",\"swapped\":"+B(e.swapped)+",\"oldReturnedToBag\":"+B(e.oldReturnedToBag)+",\"projectedMainId\":"+Q(e.projectedMainId)+",\"projectedReserveId\":"+Q(e.projectedReserveId)+",\"projectedItemsComplete\":"+Items(e.ProjectedItems??new List<GearItem>())+"}";
  IEnumerator Shot(string stage) {
   string p=Path.Combine(root,"screenshots",stage+".png");ScreenCapture.CaptureScreenshot(p);yield return Frames(8);
   Require(File.Exists(p),"screenshot "+stage);Event("screenshot",p);
  }
  GearItem New(GearType t,GearQuality q) {
   var i=AdventureItems.New(t,q,hero);Require(gear.Add(i),"setup normal factory/Add "+t+" "+q);
   Event("setup-api","AdventureItems.New+AdventureLoadout.Add id="+i.id+" type="+t+" quality="+q);return i;
  }
  void Place(GearItem i,bool board,int x,int y,int r) {
   string reason;bool ok=gear.Place(i,board,x,y,r,false,out reason);
   Event("setup-api","AdventureLoadout.Place id="+i.id+" board="+board+" x="+x+" y="+y+" rotation="+r+" success="+ok+" reason="+reason);Require(ok,"setup legal Place "+i.id+" "+reason);
  }
  void RightEdge(GearItem i) {
   for(int y=0;y<gear.Height(false);y++)if(gear.FitsAt(i,false,gear.Width(false)-1,y,0)){Place(i,false,gear.Width(false)-1,y,0);return;}
   throw new InvalidOperationException("setup has no legal natural-width right edge");
  }
  void Setup() {
   Event("setup-api","normal GameEntry fresh isolated profile; no dimensions/stat edits; no Random writes");
   var ranks=new int[6];ranks[(int)BasicSkill.Strength]=3;hero.Progression.RestoreProgress(5,0,ranks,new string[0],new int[0]);
   Event("setup-api","normal save restore Progression.RestoreProgress Strength=3; AP not assigned");
   role=B2EquipRole.Board;target=new Vector2Int(0,2);turn=0;
   switch(cfg.mode) {
    case "accessory":case "arms":
     var t=cfg.mode=="arms"?GearType.Arms:GearType.Accessory;
     old=New(t,GearQuality.Green);Place(old,true,target.x,target.y,0);
     companion=New(t,GearQuality.White);Place(companion,true,3,2,0);
     candidate=New(t,GearQuality.Purple);break;
    case "main":
     role=B2EquipRole.Main;old=gear.Main;Require(old!=null,"starter main real ID");candidate=New(GearType.Sword,GearQuality.Purple);target=new Vector2Int(candidate.x,candidate.y);break;
    case "board-insufficient":
     old=New(GearType.Accessory,GearQuality.White);Place(old,true,target.x,target.y,0);
     for(int y=0;y<gear.Height(true);y++)for(int x=0;x<gear.Width(true);x++){
      if(!gear.Rig.Allows(x,y)||gear.items.Any(i=>i.board&&!i.worn&&!i.overflow&&i.Cells(i.rotation).Any(c=>c.x+i.x==x&&c.y+i.y==y)))continue;
      var blocker=New(GearType.Accessory,GearQuality.White);Place(blocker,true,x,y,0);
     }
     Require(gear.UsedCells==gear.Rig.Capacity,"setup real board full by legal natural 1x1 accessories");
     candidate=New(GearType.Arms,GearQuality.Purple);turn=1;break;
    case "legal-swap":
     old=New(GearType.Accessory,GearQuality.Green);Place(old,true,target.x,target.y,0);
     candidate=New(GearType.Accessory,GearQuality.Purple);RightEdge(candidate);break;
    case "illegal-swap":
     old=New(GearType.Arms,GearQuality.Green);Place(old,true,target.x,target.y,1);
     candidate=New(GearType.Accessory,GearQuality.Purple);RightEdge(candidate);break;
    default:throw new InvalidOperationException("unknown scenario "+cfg.mode);
   }
   Require(old.id!=candidate.id&&gear.items.Count(i=>i.id==old.id)==1&&gear.items.Count(i=>i.id==candidate.id)==1,"real unique factory candidate and replaced IDs");
   Observe("fixture","setup only; candidate="+candidate.id+" replaced="+old.id+" role="+role+" target="+target+" rotation="+turn,Capture());
  }
  IEnumerator Exercise() {
   yield return Click("Open");yield return Click("ModeReplace");yield return Click("Role:"+role);
   yield return Click("Candidate:"+candidate.id);yield return Click("Replaced:"+old.id);
   // Even identical source/target values are explicitly selected via real controls.
   if(role==B2EquipRole.Board){yield return Click("XPlus");yield return Click("XMinus");yield return Click("YPlus");yield return Click("YMinus");}
   for(int i=0;i<turn;i++)yield return Click("Rotate");
   yield return Shot("01-selection");
   var before=Capture();yield return Click("Evaluate");var after=Capture();var evaluation=ReadEvaluation();
   observedEvaluation=EvalJson(evaluation);string display=Text("Request")+"\n"+Text("Result");
   Change("UI-Evaluate",before,after,observedEvaluation,display);
   Check("Evaluate-all-nine-random-save-unchanged",Same(before,after),"physical UI Evaluate, complete before/after kernel");
   bool successExpected=cfg.mode!="illegal-swap"&&cfg.mode!="board-insufficient";
   Check("Evaluate-expected-feasibility",evaluation.feasible==successExpected,evaluation.reason);
   Check("Evaluate-real-identities",evaluation.candidateGearId==candidate.id&&evaluation.replacedGearId==old.id,"candidate/replaced must be exact full owned IDs");
   Check("Evaluate-result-visible",display.Contains(candidate.id)&&display.Contains(old.id),display);
   Check("Evaluate-role",evaluation.role==role,"role="+evaluation.role);
   if(!successExpected)Check("geometry-reason-present",!string.IsNullOrEmpty(evaluation.reason),evaluation.reason);
   yield return Shot("02-evaluated");
   var commitBefore=Capture();yield return Click("Commit");var commitAfter=Capture();
   commitText=Text("CommitResult");if(string.IsNullOrEmpty(commitText))commitText=Text("Result");
   object okValue=UIValue("LastCommitSucceeded");object whyValue=UIValue("LastCommitReason");
   Require(okValue is bool,"UI LastCommitSucceeded observable");bool committed=(bool)okValue;
   Change("UI-Commit",commitBefore,commitAfter,observedEvaluation,commitText+"\nreason="+Convert.ToString(whyValue));
   Check("Commit-expected-outcome",committed==successExpected,commitText);
   if(!successExpected) {
    Check("failed-Commit-all-nine-random-save-unchanged",Same(commitBefore,commitAfter),"actual rejected UI Commit atomicity");
    Check("failed-Commit-reason",!string.IsNullOrEmpty(Convert.ToString(whyValue)),Convert.ToString(whyValue));
   } else {
    Check("exact-selected-contributions",evaluation.oldContribution==old.Attack&&evaluation.newContribution==candidate.Attack&&evaluation.oldContributionAfter==0&&evaluation.newContributionBefore==0,"only exact selected old/new IDs change active contribution");
    Check("active-count-not-added",evaluation.after.activeCount==evaluation.before.activeCount,"replacement is not addition");
    Check("selected-old-returned-inactive",gear.items.Single(i=>i.id==old.id).InBag&&gear.items.Single(i=>i.id==candidate.id).id!=old.id,"old ID retained in bag, selected new ID unique");
    Check("Commit-predicted-AP",BitConverter.SingleToInt32Bits(hero.AttackPower)==BitConverter.SingleToInt32Bits(evaluation.after.attackPower),"actual="+F(hero.AttackPower)+" projected="+F(evaluation.after.attackPower));
    Check("Commit-predicted-basic",BitConverter.SingleToInt32Bits(hero.GetComponent<AdventureCombat>().BasicPower)==BitConverter.SingleToInt32Bits(evaluation.after.basicPower),"actual basicPower vs projected");
    Check("Commit-ID-set-preserved",gear.items.Select(i=>i.id).OrderBy(x=>x).SequenceEqual(evaluation.ProjectedItems.Select(i=>i.id).OrderBy(x=>x)),"no fake IDs, no old deletion/new duplicate");
    Check("Commit-projected-item-fields",string.Join(";",gear.items.OrderBy(i=>i.id).Select(J))==string.Join(";",evaluation.ProjectedItems.OrderBy(i=>i.id).Select(J)),"actual complete serialized items vs projected");
    Check("Commit-main-reserve",gear.mainWeapon==evaluation.projectedMainId&&gear.reserveWeapon==evaluation.projectedReserveId,"exact slots");
    if(companion!=null)Check("same-type-companion-preserved",gear.items.Single(i=>i.id==companion.id).board,"replacement removes only selected old contribution");
   }
   Observe("post-commit","complete actual items/AP/contributions; UI reason="+commitText,commitAfter);
   yield return Shot("03-committed");yield return Click("Close");
  }
  // These are additional API observations, NEVER counted as real UI actions.
  B2AttackEvaluation ApiProbe(string label,Func<B2AttackEvaluation> query,Func<B2AttackEvaluation,bool> predicate) {
   var a=Capture();var e=query();var b=Capture();Change("ADDITIONAL-API-"+label,a,b,EvalJson(e),e.reason);
   Check("API-"+label+"-readonly",Same(a,b),"same-stack API probe, not UI");Check("API-"+label+"-authority",predicate(e),EvalJson(e));return e;
  }
  void Authority() {
   Observe("authority-strength","ADDITIONAL API observation only; actual rank=3, bonus=15",Capture());
   Check("authority-Strength3",hero.Progression.Rank(BasicSkill.Strength)==3&&hero.Progression.AttackBonus==15,"normal restore setup, no AP assignment");
   // ADDITIONAL API ONLY: Add on an empty cell must preserve every existing board item.
   Event("setup-api","ADDITIONAL Board Add readonly probe setup after completed six-case UI action; no Add commit");
   var addCandidate=New(GearType.Accessory,GearQuality.White);
   Require(addCandidate.InBag&&!gear.Carried(addCandidate),"API Board Add normal owned nonCarried candidate");
   var oldBoardFields=gear.items.Where(i=>i.board&&!i.worn&&!i.overflow).ToDictionary(i=>i.id,i=>J(i));
   var scanBefore=Capture();bool foundEmpty=false;var addPosition=Vector2Int.zero;string scanReason="";int scanned=0;
   for(int y=0;y<gear.Height(true)&&!foundEmpty;y++)for(int x=0;x<gear.Width(true)&&!foundEmpty;x++) {
    scanned++;if(gear.CanPlace(addCandidate,true,x,y,addCandidate.rotation,false,out scanReason)){foundEmpty=true;addPosition=new Vector2Int(x,y);}
   }
   var scanAfter=Capture();
   Change("ADDITIONAL-API-BoardAdd-CanPlaceScan",scanBefore,scanAfter,"null","scanned="+scanned+" foundEmpty="+foundEmpty+" target="+addPosition+" lastReason="+scanReason);
   Check("API-BoardAdd-CanPlaceScan-readonly",Same(scanBefore,scanAfter),"normal CanPlace only, swap=false, no mutation or commit");
   ApiProbe("BoardAdd-empty-or-full",()=>gear.PreviewAdd(addCandidate.id,addPosition,B2EquipRole.Board,addCandidate.rotation),e=> {
    if(!foundEmpty)return !e.feasible&&!string.IsNullOrEmpty(e.reason);
    var projected=e.ProjectedItems;
    return e.feasible&&projected!=null&&e.candidateGearId==addCandidate.id&&string.IsNullOrEmpty(e.replacedGearId)
     &&e.after.activeCount==e.before.activeCount+1&&e.newContribution==addCandidate.Attack&&e.newContributionBefore==0
     &&projected.Count(i=>i.board&&!i.worn&&!i.overflow)==oldBoardFields.Count+1
     &&oldBoardFields.All(pair=>projected.Any(i=>i.id==pair.Key&&J(i)==pair.Value))
     &&gear.items.Select(i=>i.id).OrderBy(id=>id).SequenceEqual(projected.Select(i=>i.id).OrderBy(id=>id))
     &&e.projectedMainId==gear.mainWeapon&&e.projectedReserveId==gear.reserveWeapon;
   });
   var reserve=New(GearType.Sword,GearQuality.Green);
   ApiProbe("Reserve0",()=>gear.PreviewAdd(reserve.id,new Vector2Int(reserve.x,reserve.y),B2EquipRole.Reserve),e=>e.feasible&&e.after.reserveContribution==0&&e.deltaAttackPower==0);
   float ap=hero.AttackPower;Require(gear.SelectReserve(reserve),"setup actual SelectReserve");
   Event("setup-api","ADDITIONAL authority actual SelectReserve id="+reserve.id);
   Check("authority-actual-Reserve0",gear.Reserve==reserve&&hero.AttackPower==ap&&gear.AttackSnapshot().reserveContribution==0,"real reserve contributes zero");
   var container=AdventureItems.NewContainer("bag_relic");Require(gear.Add(container),"setup authority normal NewContainer/Add bag_relic");
   Event("setup-api","ADDITIONAL authority only: normal bag_relic factory id="+container.id+" immutable asset attackBonus=6");
   var worn=gear.items.Single(i=>i.worn&&i.type==GearType.Backpack);
   // Worn item BODY Attack is zero; its container SLOT contributes the catalog bonus.
   var wornEvaluation=ApiProbe("Worn-and-container-nonzero",()=>gear.PreviewReplace(container.id,worn.id,new Vector2Int(-1,-1),B2EquipRole.Worn,0),e=>e.feasible&&e.newContribution==6&&e.after.containerBonus==6&&e.after.progressionBonus==15);
   var projectedWorn=wornEvaluation.ProjectedItems==null?null:wornEvaluation.ProjectedItems.SingleOrDefault(i=>i.id==container.id);
   Check("API-Worn-body-Attack0",container.Attack==0&&wornEvaluation.itemAttack==0&&projectedWorn!=null&&projectedWorn.Attack==0,"body Attack is zero, distinct from slot total contribution");
   Check("API-Worn-excluded-from-Active",projectedWorn!=null&&projectedWorn.worn&&!projectedWorn.board&&!projectedWorn.overflow&&!B2AttackModel.Active(wornEvaluation.ProjectedItems,wornEvaluation.projectedMainId).Any(i=>i.id==container.id),"worn body never enters Active item set");
   Check("API-Worn-slot-bonus6",AdventureCatalog.Container(container.definitionId).attackBonus==6&&wornEvaluation.newContribution==6&&wornEvaluation.after.containerBonus==6&&wornEvaluation.deltaAttackPower==6,"catalog slot bonus +6, projected container total +6 and actual preview delta AP +6");
   GearItem overflow=null;ap=hero.AttackPower;
   for(int n=0;n<128&&overflow==null;n++){var item=AdventureItems.New(GearType.Greatsword,GearQuality.Green,hero);gear.AddOrStore(item);Event("setup-api","ADDITIONAL authority normal factory/AddOrStore id="+item.id+" overflow="+item.overflow);if(item.overflow)overflow=item;}
   Require(overflow!=null,"normal AddOrStore produces actual overflow");
   Check("authority-actual-Overflow0",overflow.Attack>0&&!overflow.board&&!overflow.worn&&hero.AttackPower==ap,"natural overflow positive Attack excluded from real AP");
   Observe("authority-actual-reserve-worn-overflow","ADDITIONAL API only, not UI acceptance",Capture());
  }
  IEnumerator Main() {
   cfg=JsonUtility.FromJson<Config>(File.ReadAllText(Path.Combine(root,"replacement-config.json")));
   Directory.CreateDirectory(Path.Combine(root,"screenshots"));
   productHash=SHA(typeof(AdventureLoadout).Assembly.Location);driverHash=SHA(typeof(Driver).Assembly.Location);
   exeHash=SHA(System.Diagnostics.Process.GetCurrentProcess().MainModule.FileName);
   Require(!Application.isEditor&&Type.GetType("Mono.Runtime")!=null,"actual standalone Mono");
   Require(productHash==cfg.dllSHA256&&driverHash==cfg.driverSHA256&&exeHash==cfg.exeSHA256,"runtime build identity matches receipt");
   float until=Time.realtimeSinceStartup+70;bool started=false;
   while(!GameEntry.GameSceneAuthorized&&Time.realtimeSinceStartup<until) {
    var ge=GameEntry.Instance;if(ge!=null&&!started){started=true;Event("setup-api","GameEntry.AskNew/ConfirmNew fresh isolated storage");ge.AskNew();ge.ConfirmNew();}yield return null;
   }
   Require(GameEntry.GameSceneAuthorized,"normal GameEntry authorized");until=Time.realtimeSinceStartup+90;
   while(GameEntry.Loading&&Time.realtimeSinceStartup<until)yield return null;
   session=FindAnyObjectByType<CombatSession>();Require(session!=null,"normal session exists");GameEntry.DirectReady();hero=session.hero;Require(hero!=null,"normal hero exists");gear=hero.GetComponent<AdventureLoadout>();inv=hero.Inventory;
   Require(gear!=null&&inv!=null,"normal loadout inventory exist");yield return Frames(15);
   Setup();inv.OpenPage(PlayerInventory.Page.Items);Event("setup-api","Inventory.OpenPage(Items) normal paused UI entry");yield return Frames(20);
   Require(inv.IsOpen&&CatInventoryPresenter.Running,"normal product uGUI inventory open");
   yield return Exercise();Authority();
  }
  // Flatten nested enumerators so any exception writes a concrete failed result.
  IEnumerator Guard() {
   var stack=new Stack<IEnumerator>();stack.Push(Main());
   while(stack.Count>0) {
    object current=null;bool next=false;Exception caught=null;
    try { next=stack.Peek().MoveNext();if(next)current=stack.Peek().Current; }catch(Exception e){caught=e;}
    if(caught!=null){failed=true;error+=caught+"\n";Event("driver-exception",caught.ToString());break;}
    if(!next){stack.Pop();continue;}if(current is IEnumerator){stack.Push((IEnumerator)current);continue;}yield return current;
   }
   Finish();
  }
  void Finish() {
   if(finished)return;finished=true;
   string json="{\"runId\":"+Q(cfg==null?"":cfg.runId)+",\"mode\":"+Q(cfg==null?"":cfg.mode)+",\"buildId\":"+Q(cfg==null?"":cfg.buildId)+",\"pid\":"+System.Diagnostics.Process.GetCurrentProcess().Id+",\"productDLLSHA256\":"+Q(productHash)+",\"driverSHA256\":"+Q(driverHash)+",\"exeSHA256\":"+Q(exeHash)+",\"isMono\":"+B(Type.GetType("Mono.Runtime")!=null)+",\"isEditor\":"+B(Application.isEditor)+",\"result\":"+Q(failed?"FAIL":"PASS")+",\"checks\":"+checks+",\"passed\":"+passes+",\"failed\":"+(checks-passes)+",\"error\":"+Q(error)+",\"evaluation\":"+observedEvaluation+",\"commitText\":"+Q(commitText)+",\"requestedExitCode\":"+(failed?3:0)+"}";
   File.WriteAllText(Path.Combine(root,"result.json"),json);Application.Quit(failed?3:0);
  }
  void Start(){StartCoroutine(Guard());}
 }
}
