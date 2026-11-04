using System;using UnityEngine;
// Version 1 is frozen. Future balance changes require a new version and retain this reader.
public static class NewWeaponDropRules {
 public const int Version=1, MaximumPerDeath=1;public const double OrdinaryChance=.03,EliteChance=.08;
 public static double Chance(EnemyArchetype type)=>type==EnemyArchetype.Elite?EliteChance:type==EnemyArchetype.Melee||type==EnemyArchetype.Ranged?OrdinaryChance:0;
 public static int Weight(int typeIndex)=>typeIndex>=0&&typeIndex<3?1:0;
 public static GearQuality Quality(double roll)=>roll<.005?GearQuality.Red:roll<.04?GearQuality.Gold:roll<.18?GearQuality.Purple:roll<.55?GearQuality.Green:GearQuality.White;
 public static int Choose(uint roll,int count){if(count<1||count>3)throw new ArgumentOutOfRangeException(nameof(count));int total=0;for(int i=0;i<count;i++)total+=Weight(i);int ticket=(int)(roll%(uint)total);for(int i=0;i<count;i++){ticket-=Weight(i);if(ticket<0)return i;}throw new InvalidOperationException("New drop weight invariant");}
 public static string Stamp(string old)=>"NWD1:"+NewWeaponRegistry.EnabledCount+"|"+old;
 public static bool Read(string text,out int count){count=0;if(string.IsNullOrEmpty(text))return false;int bar=text.IndexOf('|');if(bar<0)return false;string prefix=text.Substring(0,bar),old=text.Substring(bar+1);if(old!="B06-B4-R1"&&old!="B06-B4"&&old!="B06-B2")return false;if(prefix.Length==6&&prefix.StartsWith("NWD1:",StringComparison.Ordinal))count=prefix[5]-'0';else if(prefix.Length==3&&prefix.StartsWith("NW",StringComparison.Ordinal))count=prefix[2]-'0';else return false;return count>=1&&count<=Math.Min(3,NewWeaponRegistry.EnabledCount);}
}
