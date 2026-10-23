using UnityEngine;
// Designers can place additional instances; the active forest snapshot preserves their configuration.
public class ExtractionPoint:MonoBehaviour {
 public string entityId,label;public bool forest;
 [Min(1)]public float range=3;[Min(.1f)]public float duration=5;
 public ExtractionConfig Capture()=>new ExtractionConfig{id=entityId,label=label,position=transform.position,range=range,duration=duration};
 public void Configure(ExtractionConfig c,bool inForest){entityId=c.id;label=c.label;range=c.range;duration=c.duration;forest=inForest;transform.position=c.position;}
}
