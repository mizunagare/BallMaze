using System;using System.Linq;using System.Text;using System.Security.Cryptography;using UnityEngine;
// Append-only stable IDs. Legacy 0..10 and the original weighted pool are untouched.
public static class NewWeaponRegistry {
 public const int EnabledCount=1;
 public static bool Is(GearType type)=>(int)type>=11&&(int)type<11+EnabledCount;
 public static bool Valid(GearType type)=>(int)type>=0&&((int)type<=10||Is(type));
 public static bool Weapon(GearType type)=>(int)type>=0&&(int)type<4||Is(type);
 public static bool Ranged(GearType type)=>type==GearType.Staff||type==GearType.Bow;
 public static string Id(GearType t)=>Is(t)?new[]{"weapon_twin_blades"}[(int)t-11]:AdventureCatalog.GearIds[(int)t];
 public static string Name(GearType t)=>new[]{"双刃"}[(int)t-11];
 public static string Icon(GearType t)=>new[]{"twin_blades"}[(int)t-11];
 public static string Hash(string value){using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(value))).Replace("-","").ToLowerInvariant();}
 public static uint Number(string value)=>Convert.ToUInt32(Hash(value).Substring(0,8),16);
 public static GearItem Create(GearType type,GearQuality quality,string source=null){if(!Is(type)||(int)quality<0||(int)quality>4)throw new ArgumentException("Unsupported new weapon definition");string key=source??Guid.NewGuid().ToString("N");var item=new GearItem{id=Hash("NW1/id/"+key).Substring(0,32),type=type,quality=quality,definitionId=Id(type)};item.FreezeNewStats();int count=quality==GearQuality.White?0:quality<GearQuality.Gold?1:2;item.affixes=Enumerable.Range(0,WeaponTraits.Names.Length).OrderBy(i=>Number("NW1/affix/"+key+"/"+i)).Take(count).ToArray();return item;}
}
