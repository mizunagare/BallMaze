using UnityEngine;
public partial class CombatSaveSystem {
 bool locationPrompt;SaveLocationResult locationResult;string oldLocation,newLocation;
 public void InitializeDefaultStorage(){
  var args=System.Environment.GetCommandLineArgs();int index=System.Array.IndexOf(args,"-wanxiang-storage-root");
  if(index>=0){if(index+1>=args.Length||!System.IO.Path.IsPathRooted(args[index+1])){locationResult=new SaveLocationResult{status=SaveLocationStatus.Blocked,message="隔离存档根路径必须是绝对路径。"};locationPrompt=true;session.Flow.MigrationFailed(locationResult.message);return;}string root=System.IO.Path.GetFullPath(args[index+1]);InitializeLocatedStorage(System.IO.Path.Combine(root,"Legacy","ForestRuins"),System.IO.Path.Combine(root,"WanxiangGuitu","ForestRuins"));}
  else InitializeLocatedStorage(SaveLocationMigration.LegacyDirectory,SaveLocationMigration.NewDirectory);
 }
 public void InitializeLocatedStorage(string legacy,string current){
  oldLocation=legacy;newLocation=current;locationResult=SaveLocationMigration.Resolve(legacy,current);
  if(locationResult.status==SaveLocationStatus.Ready){locationPrompt=false;InitializeStorage(current,true);return;}
  locationPrompt=true;session.Flow.MigrationFailed(locationResult.message);
 }
 void DrawLocationPrompt(){var matrix=CombatUI.Begin();int depth=GUI.depth;GUI.depth=-220;float x=CombatUI.Width/2-510,y=CombatUI.Height/2-230;CombatUI.Fill(new Rect(0,0,CombatUI.Width,CombatUI.Height),new Color(0,0,0,.95f));CombatUI.Panel(new Rect(x,y,1020,460));CombatUI.Text(new Rect(x+25,y+20,970,45),"万象归途 · 存档定位与恢复",28,CombatUI.Gold,true);CombatUI.Text(new Rect(x+25,y+85,970,260),locationResult.message,19);
  if(CombatUI.Button(new Rect(x+25,y+370,285,45),"重新检查（不创建空档）",!string.IsNullOrEmpty(oldLocation)&&!string.IsNullOrEmpty(newLocation)))InitializeLocatedStorage(oldLocation,newLocation);
  if(CombatUI.Button(new Rect(x+330,y+370,355,45),"明确继续新版，保留旧档",locationResult.status==SaveLocationStatus.Conflict&&locationResult.canUseNew)){try{SaveLocationMigration.ChooseNew(oldLocation,newLocation);InitializeLocatedStorage(oldLocation,newLocation);}catch(System.Exception e){locationResult.message=e.Message;}}
  if(CombatUI.Button(new Rect(x+710,y+370,285,45),"退出，保持现状"))Application.Quit();GUI.depth=depth;GUI.matrix=matrix;
 }
}
