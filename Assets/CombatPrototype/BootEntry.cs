using System.Collections;using UnityEngine;using UnityEngine.SceneManagement;
// The shipping scene contains no combat objects or automatic save creation.
public sealed class BootEntry:MonoBehaviour {
 IEnumerator Start(){if(GameEntry.LaunchRejected)yield break;if(!Application.isEditor&&System.Array.IndexOf(System.Environment.GetCommandLineArgs(),"-wanxiang-test-gameplay")>=0)Debug.LogWarning("B10_LEGACY_GAMEPLAY_FLAG_IGNORED: 正式版本始终先显示开始界面。");Time.timeScale=0;Cursor.lockState=CursorLockMode.None;Cursor.visible=true;GameEntry.BeginBoot();yield return null;yield return SceneManager.LoadSceneAsync(GameEntry.TitlePath);}
 void OnGUI(){if(GameEntry.LaunchRejected)return;var matrix=GUI.matrix;var color=GUI.color;GUI.matrix=Matrix4x4.identity;GUI.color=new Color(.10f,.20f,.17f);GUI.DrawTexture(new Rect(0,0,Screen.width,Screen.height),Texture2D.whiteTexture);GUI.color=Color.white;GUI.Label(new Rect(Screen.width*.5f-120,Screen.height*.5f-20,300,60),"万象归途\n正在准备开始界面…");GUI.color=color;GUI.matrix=matrix;}
}
public sealed class GameSceneRedirect:MonoBehaviour {
 IEnumerator Start(){yield return null;yield return SceneManager.LoadSceneAsync(GameEntry.BootPath);Destroy(gameObject);}
}
