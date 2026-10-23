using System.Linq;
using UnityEngine;
public partial class AdventureFlow {
 public ExtractionConfig waveExit=new ExtractionConfig{id="exit:wave",label="波次撤离装置",position=new Vector3(0,.1f,-10)};
 public ExtractionConfig CurrentExit { get {var layout=GetComponent<ForestRegionRuntime>()?.Layout;if(layout==null){waveExit.duration=extractionDuration;return waveExit;}var configs=Object.FindObjectsByType<ExtractionPoint>(FindObjectsSortMode.None).Where(p=>p.forest&&p.gameObject.scene==gameObject.scene).Select(p=>p.Capture()).ToArray();if(configs.Length==0)configs=layout.exits;if(ActiveRun!=null&&ActiveRun.phase==RunPhase.Extracting&&!string.IsNullOrEmpty(ActiveRun.exitId))return configs.FirstOrDefault(e=>e.id==ActiveRun.exitId);return configs.OrderBy(e=>Vector3.Distance(e.position,session.hero.transform.position)).FirstOrDefault();} }
}
