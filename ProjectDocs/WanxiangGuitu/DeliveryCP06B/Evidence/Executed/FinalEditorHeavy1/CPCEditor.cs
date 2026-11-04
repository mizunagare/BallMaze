using System;using System.IO;using UnityEditor;using UnityEditor.SceneManagement;using UnityEngine;
public static class CPCEditor {
 static EditorWindow view;static bool started,formal;static string root;static double deadline;
 public static void Run(){Begin(false);}public static void Formal(){Begin(true);}
 static void Begin(bool f){formal=f;root=ValidationStorage.Root(Environment.GetCommandLineArgs(),true);deadline=EditorApplication.timeSinceStartup+300;view=UI01Before.Size(1280,720);EditorSceneManager.playModeStartScene=null;EditorSceneManager.OpenScene(GameEntry.TitlePath);EditorApplication.update+=Tick;EditorApplication.EnterPlaymode();}
 static void Tick(){try{EditorApplication.QueuePlayerLoopUpdate();view?.Repaint();if(EditorApplication.timeSinceStartup>deadline)throw new Exception("CP05C bounded Editor deadline");if(!EditorApplication.isPlaying)return;if(!started){if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!=GameEntry.TitlePath)return;if(!formal)CP05Training.StartIsolated();var g=new GameObject("CP05C Editor controlled probe");UnityEngine.Object.DontDestroyOnLoad(g);g.AddComponent<CPCProbe>().formal=formal;started=true;}if(CPCProbe.Done){EditorApplication.update-=Tick;EditorApplication.Exit(CPCProbe.Code);}}catch(Exception e){File.WriteAllText(root+"/exception.txt",e.ToString());EditorApplication.update-=Tick;EditorApplication.Exit(1);}}
}
