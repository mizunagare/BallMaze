using System;using System.IO;using UnityEngine;
// Isolated acceptance build only. Explicit synthetic root and opt-in required.
public sealed class GUXPlayer:MonoBehaviour {
 string root;float deadline;bool started,requested;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]static void Install(){var a=Environment.GetCommandLineArgs();if(Array.IndexOf(a,"-gux-acceptance")<0)return;var r=ValidationStorage.Root(a,true);if(r==null||!File.Exists(Path.Combine(r,"gux-owner.json")))throw new Exception("owned acceptance root required");var g=new GameObject("GUX isolated acceptance driver");DontDestroyOnLoad(g);g.AddComponent<GUXPlayer>().root=r;}
 void Start(){deadline=Time.realtimeSinceStartup+240;}
 void Update(){try{if(Time.realtimeSinceStartup>deadline)throw new Exception("GUX bounded runtime deadline");if(!started){if(!requested&&GameEntry.Instance!=null&&!GameEntry.Loading){GameEntry.Instance.AskNew();if(!GameEntry.Instance.ConfirmNew())throw new Exception("controlled explicit newgame rejected: "+GameEntry.Error);requested=true;}var s=FindFirstObjectByType<CombatSession>();if(s==null||s.hero==null||!s.Saves.IsInitialized)return;GUXCases.Begin(s,root,"nondevelopment-acceptance-player; virtual input, controlled fixtures; Boot/Title and explicit controlled NewGame callback; NOT native click");started=true;}GUXCases.Tick();if(GUXCases.Done){enabled=false;Application.Quit(GUXCases.ExitCode);}}catch(Exception e){File.WriteAllText(root+"/exception.txt",e.ToString());enabled=false;Application.Quit(1);}}
}


