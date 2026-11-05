using System;
using UnityEngine;

// Saved editor outputs only. The Player never calls MapMagic or an Editor API.
public enum RuinsModule { Block, Column, Arch, Stair, Altar, Door, Chest, Roof, Rune }
public sealed class RuinsAssets : ScriptableObject {
 public const string Version="C1-BAKED-1";
 public string assetVersion=Version;
 public int authoringSeed=424242;
 public GameObject terrain;
 public GameObject[] modules;
 public GameObject Module(RuinsModule type){
  if(assetVersion!=Version||terrain==null||modules==null||modules.Length!=9||modules[(int)type]==null)
   throw new InvalidOperationException("遗迹保存资源版本或模块缺失，未创建替代白盒。");
  return modules[(int)type];
 }
 public static RuinsAssets Load(){var a=Resources.Load<RuinsAssets>("AncientRuins/Set");if(a==null)throw new InvalidOperationException("缺少烘焙遗迹资源。");a.Module(RuinsModule.Block);return a;}
}
