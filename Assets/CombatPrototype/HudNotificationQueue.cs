using System.Collections.Generic;using UnityEngine;
public sealed class HudNotificationQueue {
 string info;float until;readonly Dictionary<MaterialKind,int> pickups=new Dictionary<MaterialKind,int>();
 public string IconKey {get;private set;}="help";
 public void SetIcon(string icon){IconKey=icon;}
 public void Clear(){info=null;until=0;pickups.Clear();IconKey="help";}
 public void Message(string value){pickups.Clear();info=value;until=Time.unscaledTime+3;IconKey="help";}
 public void Pickup(MaterialKind kind,int count){if(Time.unscaledTime>=until)pickups.Clear();pickups.TryGetValue(kind,out int n);pickups[kind]=n+count;info=null;until=Time.unscaledTime+2.5f;IconKey="bag";}
 public string Text{get{if(Time.unscaledTime>=until)return "";if(info!=null)return info;var parts=new List<string>();foreach(var p in pickups)parts.Add(PlayerInventory.Label(p.Key)+" +"+p.Value);return string.Join("   ",parts);}}
}
