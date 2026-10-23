using UnityEngine;
// Designers can place additional instances; the active forest snapshot preserves their configuration.
public class ExtractionPoint:MonoBehaviour {
 public string entityId,label;public bool forest;
 [Min(1)]public float range=3;[Min(.1f)]public float duration=5;
 ExtractionConfig config;Renderer[] repairVisuals;
 public ExtractionConfig Capture(){var c=config==null?new ExtractionConfig():AdventureData.Clone(config);c.id=entityId;c.label=label;c.position=transform.position;c.range=range;c.duration=duration;return c;}
 public void Configure(ExtractionConfig c,bool inForest){config=AdventureData.Clone(c);entityId=c.id;label=c.label;range=c.range;duration=c.duration;forest=inForest;transform.position=c.position;}
 public void SetRepairVisuals(Renderer[] renderers){repairVisuals=renderers;RefreshRepairVisuals();}
 public void SetRepair(bool repaired,string receipt){config.repaired=repaired;config.repairReceipt=receipt;RefreshRepairVisuals();}
 void OnGUI(){if(!forest||config==null||!config.repairRequired||Camera.main==null)return;var hero=Object.FindFirstObjectByType<ThirdPersonHero>();if(hero==null||hero.GameplayPaused||Vector3.Distance(hero.transform.position,transform.position)>18)return;var p=Camera.main.WorldToScreenPoint(transform.position+Vector3.up*2);if(p.z<=0)return;CombatChineseUI.Apply();GUI.Box(new Rect(p.x-120,Screen.height-p.y,240,28),label+(config.repaired?" · 已修复":" · 待修复"));}
 void RefreshRepairVisuals(){if(repairVisuals==null)return;foreach(var r in repairVisuals){r.enabled=config.repaired;r.transform.localRotation=config.repaired?Quaternion.identity:Quaternion.Euler(0,0,25);}}
}
