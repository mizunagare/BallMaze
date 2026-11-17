// R2 FIX FLOAT STOP-GATE SIDECAR ONLY. Not an Assets/product source file.
// Calls actual Unity Mono Enumerable.Sum and the unchanged loaded B2AttackModel.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using UnityEngine;
namespace B2R2FixFloat
{
 [Serializable] public class Config { public string runId,buildId,dllSHA256,exeSHA256,driverSHA256; }
 [Serializable] public class Fixture { public GearItem[] items; }
 [Serializable] public class Step {
  public string runId,kind="accumulation-step",itemId,inputSingleR,inputAsDoubleR,inputBitsHex,inputBitsUInt32;
  public int prefixCount,frame;
  public string oldAccumulatorType="System.Double",oldDoubleBeforeR,oldDoubleAfterR,oldDoubleBitsHex;
  public string oldTraceCastSingleR,oldTraceCastBitsHex,oldActualPrefixSingleR,oldActualPrefixBitsHex;
  public string newAccumulatorType="System.Double (restored Sum semantics)",newTraceSingleR,newTraceBitsHex,newActualPrefixSingleR,newActualPrefixBitsHex;
  public bool oldTraceMatchesActualPrefix,newTraceMatchesActualPrefix;
 }
 [Serializable] public class PrefixCase { public string kind="case-prefix",label; public int count; public string[] ids; public string oldBits,newBits; public long ulp; }
 [Serializable] public class Comparison { public string label,rigId,bagId; public float rigBonus,bagBonus; public string[] inputIds,inputBits; public PrefixCase[] prefixes; public bool bitwiseEqual; }
 [Serializable] public class Result {
  public Comparison[] comparisons; public bool additionalCasesPass, transientRigFixture; public long worstUlp; public int totalPrefixComparisons;
  public string runId,buildId,verdict,error,unityVersion,platform,os,processor,environmentVersion,monoDisplayName;
  public string productAssemblyPath,productAssemblySHA256,productAssemblyMvid,driverAssemblyPath,driverAssemblySHA256,exeSHA256;
  public string coreAssemblyPath,coreAssemblySHA256,coreAssemblyName,coreImageRuntimeVersion;
  public bool isMono,isEditor,identityMatches,inputsMatch,fixturesUnchanged,randomStateUnchanged,tracesMatch;
  public int pid,pointerBits,frame,requestedExitCode;
  public string[] orderedActiveIds,orderedInputSingleBitsHex;
  public string oldActualSingleR,oldActualAsDoubleR,oldActualBitsHex,oldActualBitsUInt32;
  public string newActualSingleR,newActualAsDoubleR,newActualBitsHex,newActualBitsUInt32;
  public long ulpDifference;
  public string fixtureBeforeJson,fixtureAfterJson,randomBeforeJson,randomAfterJson;
  public string oldPath="Original Unique/Active selector Enumerable.Sum(Single) + zero rig/bag";
  public string newPath="Actual loaded B2AttackModel.ComputeAttack(items, mainId, null, null)";
  public Step[] steps;
 }
 public sealed class Driver : MonoBehaviour {
  static string root; Config config;
  static string F(float x)=>x.ToString("R",CultureInfo.InvariantCulture);
  static string D(double x)=>x.ToString("R",CultureInfo.InvariantCulture);
  static uint Bits(float x)=>BitConverter.ToUInt32(BitConverter.GetBytes(x),0);
  static string H(float x)=>Bits(x).ToString("X8",CultureInfo.InvariantCulture);
  static string SHA(string path){using(var h=SHA256.Create())using(var f=File.OpenRead(path))return string.Concat(h.ComputeHash(f).Select(x=>x.ToString("x2")));}
  static string Location(Assembly a,string fallback)=>!string.IsNullOrEmpty(a.Location)?a.Location:fallback;
  [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
  public static void Boot(){root=Environment.GetEnvironmentVariable("UNITY_TEST_ROOT");if(string.IsNullOrEmpty(root)||!File.Exists(Path.Combine(root,"r2-float-config.json")))return;var g=new GameObject("R2 actual Mono float comparison");DontDestroyOnLoad(g);g.AddComponent<Driver>();}
  IEnumerator Start(){yield return null;yield return null;var output=new Result();try{config=JsonUtility.FromJson<Config>(File.ReadAllText(Path.Combine(root,"r2-float-config.json")));output=Evaluate();}catch(Exception e){output.runId=config==null?"":config.runId;output.verdict="PROBE_ERROR";output.error=e.ToString();output.requestedExitCode=3;}File.WriteAllText(Path.Combine(root,"result.json"),JsonUtility.ToJson(output,true));File.WriteAllText(Path.Combine(root,"complete.txt"),output.verdict);UnityEngine.Debug.Log("R2 FLOAT "+output.verdict+" old="+output.oldActualBitsHex+" new="+output.newActualBitsHex+" ULP="+output.ulpDifference);Application.Quit(output.requestedExitCode);}

  static float OldAttack(List<GearItem> list,string mainId,ContainerDefinition rig,ContainerDefinition bag){var main=list.Find(i=>i.id==mainId&&i.InBag&&i.Weapon);return list.GroupBy(i=>i.id).Select(g=>g.First()).Where(i=>!i.overflow&&!i.worn&&(i.board||i==main)).Sum(i=>i.Attack)+(rig!=null?rig.attackBonus:0f)+(bag!=null?bag.attackBonus:0f);}
  Comparison CompareCase(string label,List<GearItem> list,string mainId,ContainerDefinition rig,ContainerDefinition bag){
   var c=new Comparison{label=label,rigId=rig==null?"null":rig.definitionId,bagId=bag==null?"null":bag.definitionId,rigBonus=rig==null?0:rig.attackBonus,bagBonus=bag==null?0:bag.attackBonus,inputIds=list.Select(i=>i.id).ToArray(),inputBits=list.Select(i=>H(i.Attack)).ToArray()};var prefixes=new List<PrefixCase>();
   for(int n=1;n<=list.Count;n++){var p=list.Take(n).ToList();float a=OldAttack(p,mainId,rig,bag),b=B2AttackModel.ComputeAttack(p,mainId,rig,bag);var q=new PrefixCase{label=label,count=n,ids=p.Select(i=>i.id).ToArray(),oldBits=H(a),newBits=H(b),ulp=Math.Abs((long)Bits(a)-(long)Bits(b))};prefixes.Add(q);File.AppendAllText(Path.Combine(root,"state-changes.jsonl"),JsonUtility.ToJson(q)+Environment.NewLine);}
   c.prefixes=prefixes.ToArray();c.bitwiseEqual=prefixes.All(p=>p.ulp==0);return c;
  }
  Comparison[] ExtraCases(List<GearItem> original,string mainId){
   var forward=original.Select(i=>i.Clone()).ToList();var reverse=original.Select(i=>i.Clone()).Reverse().ToList();var multi=original.Select(i=>i.Clone()).ToList();
   multi.Add(new GearItem{id="FIX-float-green-accessory",type=GearType.Accessory,quality=GearQuality.Green,definitionId="accessory",dataRevision=1,savedAttack=9.5f,x=2,y=0,board=true,affixes=new int[0]});
   multi.Add(new GearItem{id="FIX-float-white-accessory",type=GearType.Accessory,quality=GearQuality.White,definitionId="accessory",dataRevision=1,savedAttack=4f,x=3,y=0,board=true,affixes=new int[0]});
   multi.Add(new GearItem{id="FIX-float-purple-arms",type=GearType.Arms,quality=GearQuality.Purple,definitionId="arms",dataRevision=1,savedAttack=15.05f,x=4,y=0,board=true,affixes=new int[0]});
   // Catalog rigs all have attackBonus=0. This is a transient input clone ONLY,
   // never written to Resources/catalog/assets or an equipped item.
   var rig=UnityEngine.Object.Instantiate(AdventureCatalog.Container("rig_standard"));rig.definitionId="TEST_ONLY_NONZERO_RIG";rig.attackBonus=3.25f;var bag=AdventureCatalog.Container("bag_relic");
   return new[]{CompareCase("forward-original-bits",forward,mainId,null,null),CompareCase("reverse-enumeration",reverse,mainId,null,null),CompareCase("multi-active-six",multi,mainId,null,null),CompareCase("nonzero-rig-transient-input",forward,mainId,rig,null),CompareCase("nonzero-bag-catalog-relic",forward,mainId,null,bag),CompareCase("rig-then-bag-add-order",forward,mainId,rig,bag),CompareCase("same-input-order-repeat",forward,mainId,null,null)};
  }

  Result Evaluate(){
   var result=new Result {runId=config.runId,buildId=config.buildId,pid=Process.GetCurrentProcess().Id,frame=Time.frameCount,pointerBits=IntPtr.Size*8,
    unityVersion=Application.unityVersion,platform=Application.platform.ToString(),isEditor=Application.isEditor,environmentVersion=Environment.Version.ToString(),os=SystemInfo.operatingSystem,processor=SystemInfo.processorType};
   var mono=typeof(object).Assembly.GetType("Mono.Runtime");result.isMono=mono!=null;
   try{result.monoDisplayName=mono==null?"NOT_MONO":(string)mono.GetMethod("GetDisplayName",BindingFlags.Static|BindingFlags.NonPublic).Invoke(null,null);}catch(Exception e){result.monoDisplayName="unavailable: "+e.GetType().Name;}
   var product=typeof(B2AttackModel).Assembly;var own=Assembly.GetExecutingAssembly();var core=typeof(Enumerable).Assembly;
   result.productAssemblyPath=Location(product,Path.Combine(Application.dataPath,"Managed/Assembly-CSharp.dll"));result.productAssemblySHA256=SHA(result.productAssemblyPath);result.productAssemblyMvid=product.ManifestModule.ModuleVersionId.ToString();
   result.driverAssemblyPath=Location(own,Path.Combine(Application.dataPath,"Managed/B2R2FixFloatProbe.dll"));result.driverAssemblySHA256=SHA(result.driverAssemblyPath);result.exeSHA256=SHA(Process.GetCurrentProcess().MainModule.FileName);
   result.coreAssemblyPath=Location(core,Path.Combine(Application.dataPath,"Managed/System.Core.dll"));result.coreAssemblySHA256=SHA(result.coreAssemblyPath);result.coreAssemblyName=core.FullName;result.coreImageRuntimeVersion=core.ImageRuntimeVersion;
   result.identityMatches=result.productAssemblySHA256==config.dllSHA256&&result.driverAssemblySHA256==config.driverSHA256&&result.exeSHA256==config.exeSHA256;
   var randomBefore=UnityEngine.Random.state;result.randomBeforeJson=JsonUtility.ToJson(randomBefore);
   // Test fixtures, NOT live Inventory/GearItem mutation; no New/Random/FreezeNewStats calls.
   var main=new GearItem{id="R2-float-white-main",type=GearType.Sword,quality=GearQuality.White,definitionId="sword",dataRevision=1,savedAttack=8f,x=0,y=0,board=false,worn=false,overflow=false,affixes=new int[0]};
   var green=new GearItem{id="R2-float-green-arms",type=GearType.Arms,quality=GearQuality.Green,definitionId="arms",dataRevision=1,savedAttack=6.650000095367432f,x=0,y=0,board=true,worn=false,overflow=false,affixes=new int[0]};
   var white=new GearItem{id="R2-float-white-arms",type=GearType.Arms,quality=GearQuality.White,definitionId="arms",dataRevision=1,savedAttack=2.799999952316284f,x=1,y=0,board=true,worn=false,overflow=false,affixes=new int[0]};
   var items=new List<GearItem>{main,green,white};var fixture=new Fixture{items=items.ToArray()};result.fixtureBeforeJson=JsonUtility.ToJson(fixture);
   // Verbatim old identity/active expression; original Main must be an owned InBag weapon.
   var originalMain=items.Find(i=>i.id==main.id&&i.InBag&&i.Weapon);
   var active=items.GroupBy(i=>i.id).Select(g=>g.First()).Where(i=>!i.overflow&&!i.worn&&(i.board||i==originalMain)).ToArray();
   result.orderedActiveIds=active.Select(i=>i.id).ToArray();result.orderedInputSingleBitsHex=active.Select(i=>H(i.Attack)).ToArray();
   result.inputsMatch=active.Length==3&&Bits(active[0].Attack)==Bits(8f)&&Bits(active[1].Attack)==Bits(6.650000095367432f)&&Bits(active[2].Attack)==Bits(2.799999952316284f);
   File.WriteAllText(Path.Combine(root,"input-events.jsonl"),"{\"kind\":\"fixture-initialization-not-user-ui\",\"detail\":\"Three immutable fixture GearItem values in the same actual Unity Mono process; no inventory or final AttackPower write.\"}"+Environment.NewLine);
   var steps=new List<Step>();double oldTrace=0d;double newTrace=0d;
   for(int i=0;i<active.Length;i++){
    float v=active[i].Attack;var s=new Step{runId=config.runId,itemId=active[i].id,prefixCount=i+1,frame=Time.frameCount,inputSingleR=F(v),inputAsDoubleR=D((double)v),inputBitsHex=H(v),inputBitsUInt32=Bits(v).ToString(CultureInfo.InvariantCulture),oldDoubleBeforeR=D(oldTrace)};
    oldTrace+=(double)v;newTrace+=v;s.oldDoubleAfterR=D(oldTrace);s.oldDoubleBitsHex=unchecked((ulong)BitConverter.DoubleToInt64Bits(oldTrace)).ToString("X16",CultureInfo.InvariantCulture);s.oldTraceCastSingleR=F((float)oldTrace);s.oldTraceCastBitsHex=H((float)oldTrace);
    // Real Enumerable.Sum and real product method for EVERY prefix, not Python emulation.
    float oldPrefix=active.Take(i+1).Sum(item=>item.Attack);var prefix=items.Take(i+1).ToList();float newPrefix=B2AttackModel.ComputeAttack(prefix,main.id,null,null);
    s.oldActualPrefixSingleR=F(oldPrefix);s.oldActualPrefixBitsHex=H(oldPrefix);s.newTraceSingleR=F((float)newTrace);s.newTraceBitsHex=H((float)newTrace);s.newActualPrefixSingleR=F(newPrefix);s.newActualPrefixBitsHex=H(newPrefix);
    s.oldTraceMatchesActualPrefix=Bits(oldPrefix)==Bits((float)oldTrace);s.newTraceMatchesActualPrefix=Bits(newPrefix)==Bits((float)newTrace);steps.Add(s);File.AppendAllText(Path.Combine(root,"state-changes.jsonl"),JsonUtility.ToJson(s)+Environment.NewLine);
   }
   float oldActual=active.Sum(i=>i.Attack)+0f+0f;float newActual=B2AttackModel.ComputeAttack(items,main.id,null,null);
   result.oldActualSingleR=F(oldActual);result.oldActualAsDoubleR=D((double)oldActual);result.oldActualBitsHex=H(oldActual);result.oldActualBitsUInt32=Bits(oldActual).ToString(CultureInfo.InvariantCulture);
   result.newActualSingleR=F(newActual);result.newActualAsDoubleR=D((double)newActual);result.newActualBitsHex=H(newActual);result.newActualBitsUInt32=Bits(newActual).ToString(CultureInfo.InvariantCulture);result.ulpDifference=Math.Abs((long)Bits(oldActual)-(long)Bits(newActual));
   result.comparisons=ExtraCases(items,main.id);result.transientRigFixture=true;result.additionalCasesPass=result.comparisons.All(c=>c.bitwiseEqual);result.worstUlp=result.comparisons.SelectMany(c=>c.prefixes).Max(p=>p.ulp);result.totalPrefixComparisons=result.comparisons.Sum(c=>c.prefixes.Length);
   result.steps=steps.ToArray();result.tracesMatch=steps.All(x=>x.oldTraceMatchesActualPrefix&&x.newTraceMatchesActualPrefix);
   result.fixtureAfterJson=JsonUtility.ToJson(fixture);result.fixturesUnchanged=result.fixtureBeforeJson==result.fixtureAfterJson;var randomAfter=UnityEngine.Random.state;result.randomAfterJson=JsonUtility.ToJson(randomAfter);result.randomStateUnchanged=randomBefore.Equals(randomAfter);
   bool valid=result.identityMatches&&result.inputsMatch&&result.isMono&&!result.isEditor&&result.fixturesUnchanged&&result.randomStateUnchanged&&result.tracesMatch;
   result.verdict=!valid?"INVALID_PROBE_STOP":result.ulpDifference==0&&result.additionalCasesPass?"BITWISE_EQUAL":"BIT_DIFFERENCE_STOP";
   result.requestedExitCode=!valid?3:result.ulpDifference==0&&result.additionalCasesPass?0:21;
   return result;
  }
 }
}
