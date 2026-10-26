using System.Collections.Generic;using UnityEngine;
public sealed class HudIconCatalog {
 readonly Dictionary<string,Sprite> cache=new Dictionary<string,Sprite>();
 public Sprite Get(string key){if(string.IsNullOrEmpty(key))return null;if(cache.TryGetValue(key,out var value))return value;var texture=AdventureItems.Texture(key);value=texture==null?null:Sprite.Create(texture,PixelRect(key,texture),new Vector2(.5f,.5f),100);if(value!=null)value.name=key;cache[key]=value;return value;}
 static Rect PixelRect(string key,Texture2D texture){var uv=CatIconLayout.UV(key);return new Rect(Mathf.Round(uv.x*texture.width),Mathf.Round(uv.y*texture.height),Mathf.Round(uv.width*texture.width),Mathf.Round(uv.height*texture.height));}
 public void Dispose(){foreach(var v in cache.Values)if(v!=null)Object.Destroy(v);cache.Clear();}
}
