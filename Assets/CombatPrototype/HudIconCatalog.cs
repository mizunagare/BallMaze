using System.Collections.Generic;using UnityEngine;
public sealed class HudIconCatalog {
 readonly Dictionary<string,Sprite> cache=new Dictionary<string,Sprite>();
 public Sprite Get(string key){if(string.IsNullOrEmpty(key))return null;if(cache.TryGetValue(key,out var value))return value;var texture=AdventureItems.Texture(key);value=texture==null?null:Sprite.Create(texture,new Rect(0,0,texture.width,texture.height),new Vector2(.5f,.5f),100);if(value!=null)value.name=key;cache[key]=value;return value;}
 public void Dispose(){foreach(var v in cache.Values)if(v!=null)Object.Destroy(v);cache.Clear();}
}
