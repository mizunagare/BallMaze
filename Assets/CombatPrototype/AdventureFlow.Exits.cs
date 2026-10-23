using System;
using System.Linq;
using UnityEngine;
public partial class AdventureFlow {
 public ExtractionConfig waveExit=new ExtractionConfig{id="exit:wave",label="波次撤离装置",position=new Vector3(0,.1f,-10)};
 public ExtractionConfig[] ExitConfigs(){var layout=GetComponent<ForestRegionRuntime>()?.Layout;if(layout==null){waveExit.duration=extractionDuration;return new[]{waveExit};}var configs=UnityEngine.Object.FindObjectsByType<ExtractionPoint>(FindObjectsSortMode.None).Where(p=>p.forest&&p.gameObject.scene==gameObject.scene).Select(p=>p.Capture()).ToArray();return configs.Length==0?layout.exits:configs;}
 public ExtractionConfig CurrentExit {get{var configs=ExitConfigs();if(ActiveRun!=null&&ActiveRun.phase==RunPhase.Extracting&&!string.IsNullOrEmpty(ActiveRun.exitId))return configs.FirstOrDefault(e=>e.id==ActiveRun.exitId);var ordered=configs.OrderBy(e=>Vector3.Distance(e.position,session.hero.transform.position)).ThenBy(e=>e.id,StringComparer.Ordinal).ToArray();var nearest=ordered.FirstOrDefault();if(nearest!=null&&nearest.repairRequired&&!nearest.repaired&&(session.hero.Inventory.Count(MaterialKind.Wood)<nearest.repairWood||session.hero.Inventory.Count(MaterialKind.Stone)<nearest.repairStone)){var usable=ordered.FirstOrDefault(e=>(!e.repairRequired||e.repaired)&&Vector3.Distance(e.position,session.hero.transform.position)<=e.range);if(usable!=null)return usable;}return nearest;}}
 public string ExitInteractionText {
  get{var e=CurrentExit;if(e==null)return "出口不存在，请重试读取。";if(!e.repairRequired)return "H "+e.label+"撤离（无需清场）";if(e.repaired)return "已修复 · H 开始渡口撤离（E 与附近物品按距离互动）";
   int w=session.hero.Inventory.Count(MaterialKind.Wood),s=session.hero.Inventory.Count(MaterialKind.Stone);
   return $"{e.label} · {(w>=e.repairWood&&s>=e.repairStone?"可修复":"未修复")}\n木材 需{e.repairWood} / 持有{w} / 缺{Mathf.Max(0,e.repairWood-w)}；石头 需{e.repairStone} / 持有{s} / 缺{Mathf.Max(0,e.repairStone-s)}\nH 修复（仅本次冒险有效）；修复后再次互动撤离；E 按最近对象互动";
  }
 }
 string RepairKey(ExtractionConfig e)=>ActiveRun.runId+":"+ActiveRun.regionInstanceId+":"+e.id;
 public string RepairReason(string exitId){
  if(!Enabled||ActiveRun==null||ActiveRun.phase!=RunPhase.Running||requested.HasValue||Frozen||session.hero.Health.Dead)return "当前状态不能修复渡口。";
  var e=ExitConfigs().FirstOrDefault(x=>x.id==exitId);if(e==null||!e.repairRequired)return "该出口无需修复。";
  if(Vector3.Distance(session.hero.transform.position,e.position)>e.range)return "请靠近指定渡口再修复。";
  if(session.hero.GameplayPaused||session.hero.Progression.PendingChoices>0||session.hero.Dodge.IsRolling)return "请先结束面板、技能选择或翻滚。";
  if(e.repaired)return "渡口已经修复，无需再次付费。";
  if(session.hero.Inventory.Count(MaterialKind.Wood)<e.repairWood||session.hero.Inventory.Count(MaterialKind.Stone)<e.repairStone)return "随身材料不足，未扣费；仍可使用普通出口。";
  return "";
 }
 void SetExitRepair(string id,bool repaired,string receipt){var p=UnityEngine.Object.FindObjectsByType<ExtractionPoint>(FindObjectsSortMode.None).Single(p=>p.forest&&p.gameObject.scene==gameObject.scene&&p.entityId==id);p.SetRepair(repaired,receipt);}
 // One synchronous checkpoint publishes inventory, provenance and receipt. A false save
 // may mean a post-publication callback failed; inspect disk before deciding to roll back.
 public bool RepairExit(string exitId){
  string reason=RepairReason(exitId);if(reason!=""){session.hero.Inventory.NotifyMessage(reason);return false;}
  var e=ExitConfigs().Single(x=>x.id==exitId);var bag=session.hero.Inventory;
  var before=AdventureData.Clone(ActiveRun);var live=session.Saves.CaptureLegacy();long revision=Revision;string receipt=RepairKey(e);
  if(e.repairWood>0&&!bag.TryRemove(MaterialKind.Wood,e.repairWood))return false;
  if(e.repairStone>0&&!bag.TryRemove(MaterialKind.Stone,e.repairStone))throw new InvalidOperationException("修复预检与扣费不一致");
  SetExitRepair(exitId,true,receipt);
  bool saved=session.Saves.SaveProgress(false);
  if(!saved){
   try{
    var disk=CombatSaveSystem.InspectReadOnly(session.Saves.SavePath);
    var persisted=disk.activeRun?.checkpoint?.forest?.exits?.FirstOrDefault(x=>x.id==exitId);
    if(disk.activeRun?.runId==before.runId&&disk.revision==revision+1&&persisted?.repairReceipt==receipt&&persisted.repaired){session.Flow.Restore(disk);saved=true;}
    else if(disk.revision!=revision||disk.activeRun?.runId!=before.runId)throw new InvalidOperationException("存档修订与修复操作不一致");
   }catch(Exception ex){MigrationFailed("渡口保存结果待核对，请重试读取完整存档；暂不退款或再次扣费："+ex.Message);return false;}
   if(!saved){ActiveRun=before;Applying=true;try{bag.RestoreInventory(live.materials,live.potions,live.potionAssigned,live.potionCooldown);}finally{Applying=false;}SetExitRepair(exitId,false,e.repairReceipt);}
  }
  session.hero.Inventory.NotifyMessage(saved?"渡口修复已保存；再次按 E / H 开始撤离。":"修复未保存，材料与来源账已恢复，可重试。");return saved;
 }
 public bool InteractExit(){var e=CurrentExit;return e!=null&&e.repairRequired&&!e.repaired?RepairExit(e.id):BeginExtraction();}
}
