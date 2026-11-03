using System;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using UnityEngine;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Profile;
using UnityEditor.Build.Reporting;

// Editor-only release gate. No player diagnostics/consent code.
public sealed class ReleaseDiagnosticsGuard : IPreprocessBuildWithReport, IPostprocessBuildWithReport {
 public const string ProfilePath="Assets/BuildProfiles/WindowsRelease.asset";
 const string Guid="41a786737e7b4d5f97bc861a8cdf267a";
 static readonly BindingFlags Flags=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance|BindingFlags.Static;
 static string profileHash,connectHash,output; static DateTime started;
 public int callbackOrder=>int.MaxValue;
 public static string Hash(string path){using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(File.ReadAllBytes(path))).Replace("-","").ToLowerInvariant();}
 static void Require(bool ok,string why){if(!ok)throw new BuildFailedException("Release privacy gate: "+why);}
 public static BuildProfile ValidateProfile(){
  Require(Application.unityVersion=="6000.6.5f1","Unity version");
  var p=BuildProfile.GetActiveBuildProfile();
  Require(p!=null&&AssetDatabase.GetAssetPath(p)==ProfilePath&&AssetDatabase.AssetPathToGUID(ProfilePath)==Guid,"profile identity");
  Require((BuildTarget)typeof(BuildProfile).GetProperty("buildTarget",Flags).GetValue(p)==BuildTarget.StandaloneWindows64,"target");
  var platform=typeof(BuildProfile).GetProperty("platformBuildProfile",Flags).GetValue(p);
  var container=platform.GetType().GetProperty("insightsSettingsContainer",Flags).GetValue(platform);
  Require(container.GetType().GetProperty("buildProfileEngineDiagnosticsState",Flags).GetValue(container).ToString()=="Disabled","Diagnostics must be Disabled");
  return p;
 }
 static string Read(string type,string property){var t=AppDomain.CurrentDomain.GetAssemblies().Select(a=>a.GetType(type)).FirstOrDefault(x=>x!=null);Require(t!=null,"native bridge missing: "+type);return t.GetProperty(property,Flags)?.GetValue(null)?.ToString();}
 public static void NativeGate(){
  Require(Read("UnityEditor.EngineDiagnostics.EngineDiagnosticsSettings","enabled")=="False","EngineDiagnostics enabled");
  Require(Read("UnityEditor.CrashReporting.CrashReportingSettings","canUploadReports")=="False","CrashReporting upload enabled");
  Require(Read("UnityEngine.Connect.UnityConnectSettings","enabled")=="False","UnityConnect enabled");
 }
 public void OnPreprocessBuild(BuildReport report){
  if((report.summary.options&BuildOptions.Development)!=0)return;
  ValidateProfile();NativeGate();
  output=Path.GetFullPath(report.summary.outputPath);var marker=output+".release.json";
  if(File.Exists(marker))File.Delete(marker); // invalidate only derived publication receipt
  Require(!File.Exists(output),"fresh output required; existing executable rejected");
  profileHash=Hash(ProfilePath);connectHash=Hash("ProjectSettings/UnityConnectSettings.asset");started=DateTime.UtcNow;
 }
 [Serializable] public class Services {public bool EnableUnityConnect,EnablePerformanceReporting,EnableAnalytics,EnableCrashReporting,EnableInsights;}
 [Serializable] class Config {public string DestinationPath;public bool Development;public Services Services;}
 // Extract exact JSON object, respecting strings; require each security field exactly once.
 public static string Object(string json,string key){
  string token="\""+key+"\"";int at=json.IndexOf(token,StringComparison.Ordinal);Require(at>=0&&json.IndexOf(token,at+token.Length,StringComparison.Ordinal)<0,"missing/duplicate "+key);
  int start=json.IndexOf('{',at+token.Length);Require(start>=0,"object missing");int depth=0;bool quoted=false,escape=false;
  for(int i=start;i<json.Length;i++){char c=json[i];if(quoted){if(escape)escape=false;else if(c=='\\')escape=true;else if(c=='\"')quoted=false;continue;}if(c=='\"')quoted=true;else if(c=='{')depth++;else if(c=='}'&&--depth==0)return json.Substring(start,i-start+1);}throw new BuildFailedException("Invalid JSON object");
 }
 public static void ValidateBee(string json,string expected){
  string body=Object(json,"PlayerBuildProgramLibrary.Data.PlayerBuildConfig");string services=Object(body,"Services");
  foreach(string f in new[]{"EnableUnityConnect","EnablePerformanceReporting","EnableAnalytics","EnableCrashReporting","EnableInsights"}){
   var matches=System.Text.RegularExpressions.Regex.Matches(services,"\""+f+"\"\\s*:\\s*(false|true)(?=\\s*[,}])");Require(matches.Count==1&&matches[0].Groups[1].Value=="false","Bee service "+f);
  }
  var c=JsonUtility.FromJson<Config>(body);Require(c!=null&&c.Services!=null&&!c.Development&&Path.GetFullPath(c.DestinationPath)==Path.GetFullPath(expected),"Bee output/development mismatch");
 }
 public void OnPostprocessBuild(BuildReport report){
  if((report.summary.options&BuildOptions.Development)!=0)return;
  ValidateProfile();NativeGate();Require(output==Path.GetFullPath(report.summary.outputPath)&&profileHash==Hash(ProfilePath)&&connectHash==Hash("ProjectSettings/UnityConnectSettings.asset"),"input changed / no matching preflight");
  Require(File.Exists(output)&&File.GetLastWriteTimeUtc(output)>=started,"stale/missing output");
  var matches=Directory.GetFiles("Library/Bee","Player*-inputdata.json").Where(f=>File.ReadAllText(f).Contains(output.Replace('\\','/'))).ToArray();
  Require(matches.Length==1,"ambiguous/missing Bee input");ValidateBee(File.ReadAllText(matches[0]),output);
  File.WriteAllText(output+".bee.json",File.ReadAllText(matches[0]));
  // A publish marker is written by the official entry only after BuildReport success.
 }
 public static void Publish(BuildReport report){Require(report.summary.result==BuildResult.Succeeded&&report.summary.totalErrors==0,"BuildReport failed");ValidateProfile();NativeGate();Require(File.Exists(output+".bee.json"),"postflight absent");ValidateBee(File.ReadAllText(output+".bee.json"),output);File.WriteAllText(output+".release.json",JsonUtility.ToJson(new Receipt{profile=ProfilePath,profileSHA256=profileHash,unityConnectSHA256=connectHash,executableSHA256=Hash(output),utc=DateTime.UtcNow.ToString("o")},true));}
 [Serializable] class Receipt {public string profile,profileSHA256,unityConnectSHA256,executableSHA256,utc;}
}
