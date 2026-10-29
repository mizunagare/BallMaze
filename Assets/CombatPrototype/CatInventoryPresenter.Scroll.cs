using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public sealed partial class CatInventoryPresenter {
 readonly Dictionary<string,float> scrollPositions=new Dictionary<string,float>();
 readonly Dictionary<string,float> lastListPositions=new Dictionary<string,float>();
 readonly Dictionary<ScrollRect,string> liveScrolls=new Dictionary<ScrollRect,string>();
 string ScrollKey(string name)=>bag.CurrentPage+"|"+CampInventoryView.Section+"|"+name+"|"+filter+"|"+craftCategory+"|"+onlyCraftable+"|"+(craftSearch??"").Trim();
 static string ListKey(string key){var parts=key.Split('|');return parts[0]+"|"+parts[1]+"|"+parts[2];}
 void CaptureScrolls(){foreach(var pair in liveScrolls)if(pair.Key!=null&&pair.Key.content!=null){float position=Mathf.Max(0,pair.Key.content.anchoredPosition.y);scrollPositions[pair.Value]=position;lastListPositions[ListKey(pair.Value)]=position;}liveScrolls.Clear();}
 RectTransform Scroll(Transform parent,string name,float x,float y,float w,float h,float height){var content=CatUI.Scroll(parent,name,x,y,w,h,height);var view=content.GetComponentInParent<ScrollRect>();string key=ScrollKey(name);liveScrolls[view]=key;float offset=scrollPositions.TryGetValue(key,out var old)?old:lastListPositions.TryGetValue(ListKey(key),out var previous)?previous:0;view.StopMovement();content.anchoredPosition=new Vector2(0,Mathf.Clamp(float.IsNaN(offset)||float.IsInfinity(offset)?0:offset,0,Mathf.Max(0,height-h)));return content;}
 void RestoreScrolls(){Canvas.ForceUpdateCanvases();foreach(var pair in liveScrolls){var view=pair.Key;view.StopMovement();var p=view.content.anchoredPosition;p.y=Mathf.Clamp(p.y,0,Mathf.Max(0,view.content.rect.height-view.viewport.rect.height));view.content.anchoredPosition=p;}}
}
