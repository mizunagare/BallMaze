"""Audit existing matrix evidence; preserves original inputs and incomplete attempts."""
import argparse,csv,json
from pathlib import Path
from MatrixEvidence import summarize
p=argparse.ArgumentParser();p.add_argument('--matrix',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--plan',type=Path);p.add_argument('--legacy-audit',action='store_true');a=p.parse_args()
root=a.matrix.resolve(strict=True)
if not a.matrix.is_absolute() or not (root/'owner.json').exists() or a.output.exists() or a.output.resolve().is_relative_to(root):raise ValueError('Owned matrix and fresh output outside input required')
try:plan=json.loads((a.plan or (root/'selected-plan.json' if (root/'selected-plan.json').exists() else Path(__file__).with_name('MATRIX_INPUTS.json'))).read_text(encoding='utf-8-sig'))
except (ValueError,OSError) as e:plan={'cases':[],'invalidPlan':str(e)}
result=summarize(root,plan,a.legacy_audit);a.output.mkdir(parents=True)
(a.output/'matrix-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (a.output/'matrix-results.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['case','attempt','block','run','started','departed','businessOutcome','toolStatus','completeness','seconds','damage','issues'])
 for r in result['rows']:w.writerow([r['input']['id'],r.get('attemptId'),r.get('blockId'),r.get('run'),r['started'],r['departed'],r['businessOutcome'],r['status'],r['measurementCompleteness'],r.get('elapsedSeconds'),r.get('damageTaken'),json.dumps(r['issues'])])
print(json.dumps({k:result[k] for k in ('status','planned','started','knownTerminal','unknown','counts')}));raise SystemExit(0 if result['status']=='PASS' else 2 if result['status']=='NOT_RUN' else 1)
