"""Summarize closed runtime cases without replacing missing CPU/GPU/GC metrics."""
import argparse,collections,csv,json,math,hashlib
from datetime import datetime,timedelta
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def quant(v,q):
 if not v:return None
 a=sorted(v);x=(len(a)-1)*q;i=int(x);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)
def stats(v,total):return dict(n=len(v),missing=total-len(v),p50=quant(v,.5),p95=quant(v,.95),p99=quant(v,.99),minimum=min(v) if v else None,maximum=max(v) if v else None,status='NOT_RUN' if not v else 'UNRESOLVED' if len(v)!=total else 'PASS')
def valid_system_value(column,value):return value>=0 if column=='cpu_machine_pct' or column.startswith('gpu_') else value>0
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False);root=a.root;runtime=root/'Runtime';attempts={}
 for d in (runtime/'Attempts').iterdir():
  if not (d/'owner.json').exists():continue
  o=load(d/'owner.json');caseName=Path(o['storage'].replace('\\','/')).name
  if caseName.lower() in attempts:raise RuntimeError('Ambiguous archived attempt identity '+caseName)
  attempts[caseName.lower()]=d
 cases=[];outliers=[]
 specs={'frame_interval_ms':('frame_interval_ms',1,True,False),'cpu_frame_ftm_ms':('ftm_cpu_ms',1,True,True),'cpu_main_ftm_ms':('ftm_main_ms',1,True,True),'cpu_render_ftm_ms':('ftm_render_ms',1,True,True),'gpu_ftm_ms':('ftm_gpu_ms',1,True,True),'cpu_main_recorder_ms':('pr_main_ns',.000001,True,False),'gc_alloc_recorder_bytes':('pr_gc_alloc_bytes',1,False,False),'draw_calls':('pr_draw_calls',1,False,False),'mono_used_bytes':('mono_used_bytes',1,True,False),'unity_allocated_bytes':('unity_allocated_bytes',1,True,False),'sampler_previous_us':('sampler_previous_us',1,False,False)}
 for d in sorted((runtime/'Cases').iterdir()):
  if not (d/'perf-config.json').exists():continue
  c=load(d/'perf-config.json');attempt=attempts.get(d.name.lower());ex=attempt/'runtime.Observe.exit.json' if attempt else None
  if not ex or not ex.exists():raise RuntimeError('Refuse collecting live/unknown-ended case '+str(d))
  result=load(d/'result-Observe.json') if (d/'result-Observe.json').exists() else {};receipt=load(d/'sample-receipt.json') if (d/'sample-receipt.json').exists() else {};header=load(d/'perf-header.json') if (d/'perf-header.json').exists() else {};cr=load(d/'case-result.json') if (d/'case-result.json').exists() else None
  f=d/'frames.csv';rows=list(csv.DictReader(f.open(encoding='utf-8-sig'))) if f.exists() else [];w=[x for x in rows if x['in_window']=='1'];n=len(w);metrics={}
  for label,(col,scale,positive,ftm) in specs.items():
   vals=[]
   for x in w:
    if col not in x or (ftm and x['ftm_new']!='1'):continue
    try:v=float(x[col])*scale
    except (ValueError,TypeError):continue
    if math.isfinite(v) and (v>0 if positive else v>=0):vals.append(v)
   metrics[label]=stats(vals,n)
   if vals:
    limit=metrics[label]['p99']
    for x in w:
     try:v=float(x.get(col,''))*scale
     except (ValueError,TypeError):continue
     if (not ftm or x['ftm_new']=='1') and v>limit:outliers.append(dict(case=d.name,metric=label,frame=x['frame'],realtime=x['realtime'],value=v,activity=x['activity']))
  # An allocation API returning zero for a known 64KiB test is unavailable, not zero allocations.
  metrics['sampler_allocation_bytes']=dict(status='NOT_RUN',reason='GC.GetAllocatedBytesForCurrentThread probe did not report a known allocation' if header.get('allocationProbe',0)<=0 else 'Self-allocation summary not requested; use raw column',probe=header.get('allocationProbe'))
  groups={}
  for activity in sorted(set(x['activity'] for x in w)):
   subset=[x for x in w if x['activity']==activity];groups[activity]=dict(rows=len(subset),observedSpanSeconds=float(subset[-1]['realtime'])-float(subset[0]['realtime']),cpuMain=stats([float(x['ftm_main_ms']) for x in subset if x['ftm_new']=='1' and float(x['ftm_main_ms'])>0],len(subset)),gpu=stats([float(x['ftm_gpu_ms']) for x in subset if x['ftm_new']=='1' and float(x['ftm_gpu_ms'])>0],len(subset)))
  ev=[json.loads(l) for l in (d/'perf-events.jsonl').read_text(encoding='utf-8-sig').splitlines()] if (d/'perf-events.jsonl').exists() else [];start=receipt.get('start',0);planned=c.get('seconds',0);within=[x for x in ev if start<=x['time']<=start+planned]
  defeats=[x for x in within if x['type']=='enemy-defeated'];targetTypes=[x['text'] for x in within if x['type']=='encounter-target'];domain=bool(result.get('status')=='PASS');full=bool(receipt.get('completed') and n and (c['scenario']=='Loop' or receipt['end']-start>=planned-.01));harness=bool(cr and cr['exitCode']==0 and cr['sidecarExited'] and cr['sidecarExit']==0)
  metricStatus='PASS' if domain and full and harness else 'NOT_RUN' if not n else 'FAIL'
  portable=runtime/'System'/d.name;sysroot=portable if portable.exists() else Path(c['systemOutput']) if c.get('systemOutput') else d;system=list(csv.DictReader((sysroot/'system-samples.csv').open(encoding='utf-8-sig'))) if (sysroot/'system-samples.csv').exists() else []
  # Keep system series separate: UTC intervals, exact owned PID, not CPU frame times.
  startEvent=next((x for x in ev if x['type']=='sample-start'),None)
  aligned=[]
  if startEvent:
   utcStart=datetime.fromisoformat(startEvent['utc'].replace('Z','+00:00'))-timedelta(seconds=startEvent['time']-start)
   utcEnd=utcStart+timedelta(seconds=min(planned,receipt.get('end',start)-start))
   aligned=[x for x in system if utcStart<=datetime.fromisoformat(x['utc'].replace('Z','+00:00'))<=utcEnd]
  systemMetrics={}
  for col in ['working_set_bytes','private_bytes','cpu_machine_pct','gpu_dedicated_bytes','gpu_shared_bytes']:
   vals=[float(x[col]) for x in aligned if valid_system_value(col,float(x[col]))];systemMetrics[col]=stats(vals,len(aligned))
  entry=[json.loads(l) for l in (d/'entry-audit.jsonl').read_text(encoding='utf-8-sig').splitlines()] if (d/'entry-audit.jsonl').exists() else []
  def stamp(x):return datetime.fromisoformat(x.replace('Z','+00:00'))
  launch=load(attempt/'runtime.Observe.command.json')['startUtc'];title=next((x for x in entry if x['phase']=='title-ready'),None);selected=next((x for x in entry if x['phase']=='continue-selected'),None);ready=next((x for x in entry if x['phase']=='game-ready'),None)
  req=next((x for x in ev if x['type']=='region-request'),None);done=next((x for x in ev if x['type']=='region-ready'),None)
  loading=dict(hostCommandStartToTitleSeconds=(stamp(title['utc'])-stamp(launch)).total_seconds() if title else None,continueSelectedToGameReadySeconds=(stamp(ready['utc'])-stamp(selected['utc'])).total_seconds() if ready and selected else None,successorInputRequestToReadySeconds=done['time']-req['time'] if req and done else None,pureRegionGenerationStatus='NOT_RUN',scope='Actual host-command/title/continue/game-ready edges; includes scheduling and input relay where noted, not isolated map generation or gameplay FPS',rawEntry=entry,rawLoadingEvents=[x for x in ev if x['type'] in ('loading-start','loading-ready','region-request','region-ready')])
  cases.append(dict(case=d.name,config=c,header=header,playerStatus=result.get('status','NOT_RUN'),terminal=result.get('terminal'),actualPlayerExitCode=load(ex).get('exitCode'),harnessStatus='PASS' if harness else 'FAIL',measurementStatus=metricStatus,window=receipt,rawRows=len(rows),windowRows=n,metrics=metrics,activities=groups,defeatsWithinWindow=defeats,targetTypes=targetTypes,gcCollections0Delta=int(w[-1]['gc0'])-int(w[0]['gc0']) if w else None,systemMetricsWindow=systemMetrics,systemRows=len(system),systemWindowRows=len(aligned),systemScope='Aligned by sample-start UTC corrected by monotonic offset; full lifetime raw series retained. Never a replacement for Unity CPU frame timings',loading=loading,fixtureHashFile=str(d/'fixture-before.json') if (d/'fixture-before.json').exists() else None,attempt=attempt.name if attempt else None))
 summary=dict(scope='Each run separately; missing metrics never substituted; partial/failure distributions retained; no hardware budget pass implied',cases=cases,counts=dict(collections.Counter(x['measurementStatus'] for x in cases)),metricDefinitions=str(Path(__file__).with_name('METRICS_POLICY.md')))
 (a.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 with (a.output/'summary.csv').open('w',encoding='utf-8-sig',newline='') as f:
  fields=['case','scenario','repetition','calibration','sampling','measurementStatus','playerStatus','harnessStatus','actualPlayerExitCode','windowRows','cpu_main_p50_ms','cpu_main_p95_ms','cpu_main_p99_ms','cpu_render_p95_ms','gpu_p95_ms','gpu_missing','gcCollections0Delta'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for x in cases:
   m=x['metrics'];writer.writerow(dict(case=x['case'],scenario=x['config']['scenario'],repetition=x['config'].get('repetition',0),calibration=x['config'].get('calibration',False),sampling=x['config'].get('sampling',True),measurementStatus=x['measurementStatus'],playerStatus=x['playerStatus'],harnessStatus=x['harnessStatus'],actualPlayerExitCode=x['actualPlayerExitCode'],windowRows=x['windowRows'],cpu_main_p50_ms=m['cpu_main_ftm_ms']['p50'],cpu_main_p95_ms=m['cpu_main_ftm_ms']['p95'],cpu_main_p99_ms=m['cpu_main_ftm_ms']['p99'],cpu_render_p95_ms=m['cpu_render_ftm_ms']['p95'],gpu_p95_ms=m['gpu_ftm_ms']['p95'],gpu_missing=m['gpu_ftm_ms']['missing'],gcCollections0Delta=x['gcCollections0Delta']))
 with (a.output/'outliers.csv').open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['case','metric','frame','realtime','value','activity']);writer.writeheader();writer.writerows(outliers)
 print(json.dumps(dict(cases=len(cases),counts=summary['counts'],outliers=len(outliers))))
if __name__=='__main__':main()
