using System;using System.IO;using UnityEngine;using UnityEditor;using UnityEditor.SceneManagement;
public static class CP05Build {
 public static void Run(){try{
  string root=ValidationStorage.Root(Environment.GetCommandLineArgs(),true);EditorSceneManager.OpenScene(GameEntry.ForestPath);var session=UnityEngine.Object.FindFirstObjectByType<CombatSession>();if(session==null)throw new Exception("No original session");
  Directory.CreateDirectory("Assets/CombatPrototype/Resources/CP05Training");AssetDatabase.Refresh();PrefabUtility.SaveAsPrefabAsset(session.hero.gameObject,"Assets/CombatPrototype/Resources/CP05Training/Hero.prefab");PrefabUtility.SaveAsPrefabAsset(session.enemies[0].gameObject,"Assets/CombatPrototype/Resources/CP05Training/Enemy.prefab");AssetDatabase.SaveAssets();Environment.SetEnvironmentVariable("UNITY_TEST_ROOT",root);WanxiangBuild.ValidateBuild();
 }catch(Exception e){Debug.LogException(e);EditorApplication.Exit(1);}}
}
