using System;using System.IO;using UnityEngine;
// Isolated acceptance build only. Explicit synthetic root and opt-in required.
public sealed class UXTechPlayer:MonoBehaviour {
 string root;float deadline;bool started,requested;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]static void Install(){var a=Environment.GetCommandLineArgs();if(Array.IndexOf(a,"-uxtech-acceptance")<0)return;var r=ValidationStorage.Root(a,true);if(r==null||!File.Exists(Path.Combine(r,"uxtech-owner.json")))throw new Exception("owned acceptance root required");var g=new GameObject("UXTech isolated acceptance driver");DontDestroyOnLoad(g);g.AddComponent<UXTechPlayer>().root=r;}
 void Start(){deadline=Time.realtimeSinceStartup+240;}
 void Update(){try{if(Time.realtimeSinceStartup>deadline)throw new Exception("UXTech bounded runtime deadline");if(!started){if(!requested&&GameEntry.Instance!=null&&!GameEntry.Loading){GameEntry.Instance.AskNew();if(!GameEntry.Instance.ConfirmNew())throw new Exception("controlled explicit newgame rejected: "+GameEntry.Error);requested=true;}var s=FindFirstObjectByType<CombatSession>();if(s==null||s.hero==null||!s.Saves.IsInitialized)return;UXTechCases.Begin(s,root,"nondevelopment-acceptance-player; virtual input, controlled fixtures; Boot/Title and explicit controlled NewGame callback; NOT native click");started=true;}UXTechCases.Tick();if(UXTechCases.Done){enabled=false;Application.Quit(UXTechCases.ExitCode);}}catch(Exception e){File.WriteAllText(root+"/exception.txt",e.ToString());enabled=false;Application.Quit(1);}}
}

