using System;using UnityEngine;

// Authored alpha bounds, loaded once. No texture readback, save writes or random queries in UI.
public static class CatIconLayout {
 [Serializable]public class Entry{public string key;public float x,y,width,height;}
 [Serializable]public class Data{public Entry[] entries;}
 static Data data;
 public static Rect UV(string key){if(data==null){var text=Resources.Load<TextAsset>("CatWorld/Icons/Bounds");data=text==null?new Data{entries=new Entry[0]}:JsonUtility.FromJson<Data>(text.text);}foreach(var e in data.entries)if(e.key==key)return new Rect(e.x,e.y,e.width,e.height);return new Rect(0,0,1,1);}
}
