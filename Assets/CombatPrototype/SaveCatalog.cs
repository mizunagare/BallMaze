using System;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;

public enum SaveAvailability { Missing, Ready, Backup, Legacy, Conflict, Corrupt, Incompatible, Uncertain, Blocked }
public sealed class SaveInfo {
 public SaveAvailability status;public bool canContinue;public string reason,path,stamp,profileId,runId,phase,region,savedAt;public int version,level;public long revision;public float health;
 public string Summary=>canContinue?$"等级 {level} · 生命 {health:0}\n{region} · {phase}\n修订 {revision} · {(string.IsNullOrEmpty(savedAt)?"未记录保存时间":savedAt)}\n{reason}":reason;
}
// One autosave collection, never a fictional slot list. Inspection does not migrate/write.
public static class SaveCatalog {
 public static string Fingerprint(string folder){folder=Path.GetFullPath(folder);ValidationStorage.RejectLinks(folder);if(File.Exists(folder))throw new IOException("存档位置被文件占用");if(!Directory.Exists(folder))return "missing";var files=new System.Collections.Generic.List<string>();var pending=new System.Collections.Generic.Stack<string>();pending.Push(folder);while(pending.Count>0)foreach(var f in Directory.EnumerateFileSystemEntries(pending.Pop())){ValidationStorage.RejectLinks(f);if(Directory.Exists(f))pending.Push(f);else files.Add(f);}long total=0;var sb=new StringBuilder();foreach(var f in files.OrderBy(x=>x,StringComparer.Ordinal)){total+=new FileInfo(f).Length;if(total>256L*1024*1024)throw new IOException("存档集合超过管理预算，未自动操作");sb.Append(f.Substring(folder.Length)).Append(':').Append(Hash(File.ReadAllBytes(f))).Append('\n');}return Hash(Encoding.UTF8.GetBytes(sb.ToString()));}
 public static string Hash(byte[] bytes){using(var h=SHA256.Create())return BitConverter.ToString(h.ComputeHash(bytes)).Replace("-","");}
 public static SaveInfo Inspect(string folder){var result=new SaveInfo{path=folder,status=SaveAvailability.Missing,reason="尚无自动保存档；新游戏需要确认。"};try{result.stamp=Fingerprint(folder);string primary=Path.Combine(folder,"save.json"),backup=primary+".bak";Exception error=null;CombatSaveData d=null;string chosen=null;
  if(File.Exists(primary)){try{d=CombatSaveSystem.InspectReadOnly(primary);chosen=primary;}catch(NotSupportedException e){result.status=SaveAvailability.Incompatible;result.reason=e.Message;return result;}catch(Exception e){error=e;}}
  if(d==null&&File.Exists(backup))try{d=CombatSaveSystem.InspectReadOnly(backup);chosen=backup;}catch(Exception e){error=e;}
  if(d==null){if(error!=null){result.status=error is NotSupportedException?SaveAvailability.Incompatible:SaveAvailability.Corrupt;result.reason="主档/备份不可恢复，原文件保留："+error.Message;}else if(Directory.Exists(folder)&&Directory.EnumerateFileSystemEntries(folder).Any()){result.status=SaveAvailability.Uncertain;result.reason="目录有内容但没有有效主档或备份；未创建空档。";}return result;}
  var envelope=JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(chosen));var world=d.sourceVersion>=7?(d.hasActiveRun?d.activeRun.checkpoint:d.profile.camp):d;
  result.canContinue=true;result.version=d.sourceVersion;result.revision=d.revision;result.savedAt=envelope.savedAtUtc;result.profileId=d.profile?.profileId;result.runId=d.hasActiveRun?d.activeRun.runId:null;result.level=world?.level??1;result.health=world?.health??100;result.region=d.hasActiveRun?(d.activeRun.mode==AdventureMode.ForestExploration?"ForestRuins · 森林测试区":"波次测试区"):"营地";result.phase=d.hasSettlement?(d.settlement.status==SettlementStatus.Pending?"结算待确认":d.settlement.acknowledged?"营地":"结算已保存，待回营"):d.hasActiveRun?(d.activeRun.phase==RunPhase.Extracting?"撤离引导中":"在途冒险"):"营地";
  if(d.sourceVersion<=6){result.region="旧版波次场景";result.phase="旧版在途进度（继续时迁移）";}
  result.status=chosen==primary?SaveAvailability.Ready:SaveAvailability.Backup;result.reason=chosen==primary?"当前只有一个自动保存档。":"主档缺失或损坏，将恢复完整备份；原文件保留。";
  if(File.Exists(primary+".tmp")){result.status=SaveAvailability.Uncertain;result.reason="发现未发布的临时写入；继续仅恢复最后有效修订，不提交临时奖励。";}
 }catch(Exception e){result.status=SaveAvailability.Blocked;result.canContinue=false;result.reason="存档检查受阻："+e.Message;}return result;}
 public static SaveInfo InspectLocations(string legacy,string current){var info=Inspect(current);try{bool old=Directory.Exists(legacy)&&Directory.EnumerateFileSystemEntries(legacy).Any();bool next=Directory.Exists(current)&&Directory.EnumerateFileSystemEntries(current).Any()||File.Exists(current);if(!old)return info;if(!next){var prior=Inspect(legacy);prior.stamp=Fingerprint(current);if(prior.canContinue){prior.status=SaveAvailability.Legacy;prior.reason="旧目录有有效自动档；继续时按原迁移器迁移完整集合，保留旧目录。";}return prior;}
  if(!SaveLocationMigration.ChoiceMatches(legacy,current)){info.status=SaveAvailability.Conflict;info.canContinue=false;info.reason="新旧目录同时存在且未确认选择。请在读取页明确选择新版；不会覆盖或合并。";}
 }catch(Exception e){info.status=SaveAvailability.Blocked;info.canContinue=false;info.reason=e.Message;}return info;}
}
