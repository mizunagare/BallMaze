"""Expected exit2 is startup safety rejection, never a normal gameplay exit PASS."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args()
process=json.loads((a.root/'process.json').read_text(encoding='utf-8-sig'));log=(a.root/'player.log').read_text(encoding='utf-8-sig',errors='replace')
checks={'expectedExit2':process['exitCode']==2,'noTimeout':not process['timedOut'],'noForce':not process['forcedTermination'],
 'preSceneRejectionMarker':'B09_ISOLATION_REJECTED' in log,'noSaveAudit':not (a.root/'storage-audit.jsonl').exists(),
 'noTitleAudit':not (a.root/'entry-audit.jsonl').exists(),'noSaveCollection':not (a.root/'WanxiangGuitu').exists()}
out={'status':'PASS' if all(checks.values()) else 'FAIL','scope':'Final Player rejected explicit RELATIVE root before scene initialization; expected exit2, NOT normal gameplay/exit acceptance. Missing-root case tested only by pure parser, not launched.', 'checks':checks,'process':process}
(a.root/'b09-rejection-analysis.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');print(json.dumps(out));raise SystemExit(0 if all(checks.values()) else 1)
