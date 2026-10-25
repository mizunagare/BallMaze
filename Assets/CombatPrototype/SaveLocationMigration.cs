using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;
using UnityEngine;
public enum SaveLocationStatus { Ready, Conflict, Blocked }
public class SaveLocationResult {public SaveLocationStatus status;public string directory,message;public bool canUseNew;public string legacyFingerprint,currentFingerprint;}
// Storage relocation only. No game rule, ownership or settlement planning is performed here.
public static class SaveLocationMigration {
 [Serializable] class Entry {public string path,hash;}
 [Serializable] class Receipt {public string source,sourceFingerprint;public Entry[] files;}
 const string ReceiptName="wanxiang-migration.json",ChoiceName="wanxiang-choice.json";
 public static string LegacyDirectory=>Path.Combine(Path.GetDirectoryName(Application.persistentDataPath),"BallMaze","ForestRuins");
 public static string NewDirectory=>Path.Combine(Application.persistentDataPath,"ForestRuins");
 static string Digest(byte[] data){using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(data)).Replace("-","");}
 static void NoLinks(string path)=>ValidationStorage.RejectLinks(path);
 static bool Evidence(string path)=>Directory.Exists(path)&&Directory.EnumerateFileSystemEntries(path).Any()||File.Exists(path);
 static Entry[] Manifest(string directory){
  NoLinks(directory);
  if(!Directory.Exists(directory))throw new IOException("存档目录不存在");var list=new List<Entry>();
  var pending=new Stack<string>();pending.Push(directory);var files=new List<string>();while(pending.Count>0){foreach(string item in Directory.EnumerateFileSystemEntries(pending.Pop())){if((File.GetAttributes(item)&FileAttributes.ReparsePoint)!=0)throw new IOException("存档包含链接，未自动迁移");if(Directory.Exists(item))pending.Push(item);else files.Add(item);}}
  foreach(string file in files.OrderBy(p=>p,StringComparer.Ordinal)){
   string relative=file.Substring(directory.TrimEnd(Path.DirectorySeparatorChar).Length+1);if(relative.EndsWith(".tmp",StringComparison.OrdinalIgnoreCase)||relative==ReceiptName||relative==ChoiceName)continue;
   list.Add(new Entry{path=relative,hash=Digest(File.ReadAllBytes(file))});
  }return list.ToArray();
 }
 static string Fingerprint(Entry[] entries)=>Digest(Encoding.UTF8.GetBytes(string.Join("\n",entries.Select(e=>e.path+":"+e.hash))));
 public static string CollectionFingerprint(string directory)=>Fingerprint(Manifest(directory));
 public static bool ChoiceMatches(string legacy,string current){foreach(var name in new[]{ReceiptName,ChoiceName}){var p=Path.Combine(current,name);if(!File.Exists(p))continue;var r=JsonUtility.FromJson<Receipt>(File.ReadAllText(p));if(r!=null&&r.source==Path.GetFullPath(legacy)&&r.sourceFingerprint==CollectionFingerprint(legacy))return true;}return false;}
 public static CombatSaveData ValidateRecoverable(string directory){
  Exception first=null;CombatSaveData valid=null;
  foreach(string name in new[]{"save.json","save.json.bak"}){string file=Path.Combine(directory,name);if(!File.Exists(file))continue;try{var d=CombatSaveSystem.InspectReadOnly(file);if(valid==null)valid=d;}catch(Exception e){first=e;}}
  if(valid==null)throw new InvalidDataException("主档与备份没有完整可恢复的存档",first);
  // Retained v9 migration archives own their referenced pages too. Historical raw archives
  // may intentionally contain old invalid anchors, so verify bytes/checksum/pages, not new rules.
  foreach(string file in Directory.GetFiles(directory,"*.json").Where(f=>Path.GetFileName(f).StartsWith("save-",StringComparison.Ordinal))){
   var envelope=JsonUtility.FromJson<CombatSaveEnvelope>(File.ReadAllText(file,Encoding.UTF8));if(envelope==null||string.IsNullOrEmpty(envelope.payload)||Digest(Encoding.UTF8.GetBytes(envelope.payload))!=envelope.checksum)throw new InvalidDataException("迁移档案校验失败："+Path.GetFileName(file));
   if(envelope.version>=9)GroundLootStore.Unpack(JsonUtility.FromJson<CombatSaveData>(envelope.payload),directory);
  }return valid;
 }
 public static CombatSaveData ValidateMigrationSet(string directory){
  bool primary=false;try{if(File.Exists(Path.Combine(directory,"save.json"))){CombatSaveSystem.InspectReadOnly(Path.Combine(directory,"save.json"));primary=true;}}catch{}
  if(primary&&File.Exists(Path.Combine(directory,"save.json.bak"))){try{CombatSaveSystem.InspectReadOnly(Path.Combine(directory,"save.json.bak"));}catch(Exception e){throw new InvalidDataException("主档可用但备份／引用页不完整，迁移停止；原集合保留。",e);}}
  return ValidateRecoverable(directory);
 }
 static SaveLocationResult Ready(string path,string message)=>new SaveLocationResult{status=SaveLocationStatus.Ready,directory=path,message=message,canUseNew=true};
 public static SaveLocationResult Resolve(string legacy,string current,Action<string> hook=null){
  legacy=Path.GetFullPath(legacy);current=Path.GetFullPath(current);
  try {
   if(string.Equals(legacy,current,StringComparison.OrdinalIgnoreCase)||current.StartsWith(legacy.TrimEnd(Path.DirectorySeparatorChar)+Path.DirectorySeparatorChar,StringComparison.OrdinalIgnoreCase))throw new IOException("迁移源与目标必须分离");
   NoLinks(legacy);NoLinks(current);
   bool old=Evidence(legacy),next=Evidence(current);if(!old&&!next)return Ready(current,"没有旧档，准备新档。");
   if(next){bool valid=false;string reason="";try{ValidateRecoverable(current);valid=true;}catch(Exception e){reason=e.Message;}
    if(!old){if(!valid)throw new InvalidDataException(reason);return Ready(current,"继续万象归途存档。");}
    string receipt=Path.Combine(current,ReceiptName),choice=Path.Combine(current,ChoiceName);string fingerprint=Fingerprint(Manifest(legacy));
    foreach(string marker in new[]{receipt,choice})if(File.Exists(marker)){var r=JsonUtility.FromJson<Receipt>(File.ReadAllText(marker));if(r!=null&&r.source==legacy&&r.sourceFingerprint==fingerprint){if(!valid)throw new InvalidDataException(reason);return Ready(current,"继续已迁移／已选择的新档；旧目录保留。");}}
    return new SaveLocationResult{status=SaveLocationStatus.Conflict,directory=current,canUseNew=valid,legacyFingerprint=fingerprint,currentFingerprint=valid?Fingerprint(Manifest(current)):null,message="新旧目录都有档案，未覆盖、未合并。"+(valid?"可明确选择继续新版，旧目录完整保留。":"新版无法恢复："+reason)+"\n旧："+legacy+"\n新："+current};
   }
   ValidateMigrationSet(legacy);var before=Manifest(legacy);string fingerprintBefore=Fingerprint(before);string stage=current+".migration-staging";
   if(Directory.Exists(stage)){Directory.Move(stage,stage+".interrupted-"+Guid.NewGuid().ToString("N"));}
   Directory.CreateDirectory(stage);hook?.Invoke("before-copy");
   foreach(var file in before){string target=Path.Combine(stage,file.path);Directory.CreateDirectory(Path.GetDirectoryName(target));byte[] bytes=File.ReadAllBytes(Path.Combine(legacy,file.path));using(var stream=new FileStream(target,FileMode.CreateNew,FileAccess.Write,FileShare.None)){stream.Write(bytes,0,bytes.Length);stream.Flush(true);}}
   hook?.Invoke("after-copy");if(Fingerprint(Manifest(stage))!=fingerprintBefore||Fingerprint(Manifest(legacy))!=fingerprintBefore)throw new IOException("迁移中源档变化或复制校验失败");ValidateMigrationSet(stage);
   WriteReceipt(Path.Combine(stage,ReceiptName),new Receipt{source=legacy,sourceFingerprint=fingerprintBefore,files=before});hook?.Invoke("before-publish");
   NoLinks(current);if(File.Exists(current))throw new IOException("迁移目标为文件，停止覆盖");
   if(Directory.Exists(current)){if(Directory.EnumerateFileSystemEntries(current).Any())throw new IOException("迁移目标出现内容，停止覆盖");Directory.Delete(current,false);} // OS rejects a nonempty race; never recursive.
Directory.Move(stage,current);hook?.Invoke("after-publish");return Ready(current,"旧档及分页完整迁移；旧目录保留。");
  }catch(Exception e){return new SaveLocationResult{status=SaveLocationStatus.Blocked,directory=current,message="存档定位／迁移受阻，未初始化空档："+e.Message+"\n旧："+legacy+"\n新："+current};}
 }
 static void WriteReceipt(string path,Receipt receipt){byte[] b=Encoding.UTF8.GetBytes(JsonUtility.ToJson(receipt,true));string temp=path+".tmp";using(var stream=new FileStream(temp,FileMode.Create,FileAccess.Write,FileShare.None)){stream.Write(b,0,b.Length);stream.Flush(true);}if(File.Exists(path))throw new IOException("迁移确认文件已存在，未覆盖");File.Move(temp,path);}
 [NonSerialized] public static Action<string> ChoiceValidationHook;
 public static void ChooseNew(string legacy,string current,SaveLocationResult expected=null){
  legacy=Path.GetFullPath(legacy);current=Path.GetFullPath(current);NoLinks(legacy);NoLinks(current);ValidateRecoverable(current);
  string oldHash=Fingerprint(Manifest(legacy)),newHash=Fingerprint(Manifest(current));
  if(expected!=null&&(expected.status!=SaveLocationStatus.Conflict||expected.legacyFingerprint!=oldHash||expected.currentFingerprint!=newHash))throw new IOException("确认期间集合变化，请重新检查后再次选择");
  string path=Path.Combine(current,ChoiceName),temp=path+"."+Guid.NewGuid().ToString("N")+".tmp";
  byte[] bytes=Encoding.UTF8.GetBytes(JsonUtility.ToJson(new Receipt{source=legacy,sourceFingerprint=oldHash,files=new Entry[0]},true));
  using(var stream=new FileStream(temp,FileMode.CreateNew,FileAccess.Write,FileShare.None)){stream.Write(bytes,0,bytes.Length);stream.Flush(true);}
  ChoiceValidationHook?.Invoke("before-choice-publish");NoLinks(legacy);NoLinks(current);ValidateRecoverable(current);
  if(Fingerprint(Manifest(legacy))!=oldHash||Fingerprint(Manifest(current))!=newHash)throw new IOException("确认写入前集合变化，保留上一确认");
  if(File.Exists(path))File.Replace(temp,path,path+".previous");else File.Move(temp,path);
  ChoiceValidationHook?.Invoke("after-choice-publish");
 }
}
