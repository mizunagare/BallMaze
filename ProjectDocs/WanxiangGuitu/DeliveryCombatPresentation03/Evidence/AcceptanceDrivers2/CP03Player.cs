using System;using System.IO;using UnityEngine;
// Isolated acceptance build only. Explicit synthetic root and opt-in required.
public sealed class CP03Player:MonoBehaviour {
 string root;float deadline;bool started,requested;
 [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]static void Install(){var a=Environment.GetCommandLineArgs();if(Array.IndexOf(a,"-cp03-acceptance")<0)return;var r=ValidationStorage.Root(a,true);if(r==null||!File.Exists(Path.Combine(r,"cp03-owner.json")))throw new Exception("owned acceptance root required");var g=new GameObject("CP03 isolated acceptance driver");DontDestroyOnLoad(g);g.AddComponent<CP03Player>().root=r;}
 void Start(){deadline=Time.realtimeSinceStartup+480;}
 void Update(){try{if(Time.realtimeSinceStartup>deadline)throw new Exception("CP03 bounded runtime deadline");if(!started){if(!requested&&GameEntry.Instance!=null&&!GameEntry.Loading){if(!GameEntry.Instance.Info.canContinue||!GameEntry.Instance.Continue())throw new Exception("controlled immutable fixture Continue rejected: "+GameEntry.Error);requested=true;}var s=FindFirstObjectByType<CombatSession>();if(s==null||s.hero==null||!s.Saves.IsInitialized)return;CP03Cases.Begin(s,root,"nondevelopment-acceptance-player; controlled public combat APIs, fixed fixtures; no synthetic input or injected Damage; Boot/Title and explicit controlled Continue from immutable synthetic checkpoint; NOT native click");started=true;}CP03Cases.Tick();if(CP03Cases.Done){enabled=false;Application.Quit(CP03Cases.ExitCode);}}catch(Exception e){File.WriteAllText(root+"/exception.txt",e.ToString());enabled=false;Application.Quit(1);}}
}



