"""Closed-run analysis; A absent instrumentation remains missing, never zero."""
import argparse,collections,csv,json,math
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def quant(v,q):
 if not v:return None
 s=sorted(v);n=(len(s)-1)*q;i=int(n);return s[i]+(s[min(i+1,len(s)-1)]-s[i])*(n-i)
def stats(v,total):return dict(n=len(v),missing=total-len(v),p50=quant(v,.5),p95=quant(v,.95),p99=quant(v,.99),minimum=min(v) if v else None,maximum=max(v) if v else None,status='NOT_RUN' if not v else 'UNRESOLVED' if len(v)<total else 'PASS')
def lines(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines()] if p.exists() else []
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();assert (a.root/'matrix-complete.json').exists(),'No analysis during measurement';a.output.mkdir(exist_ok=False);results=[];probes=[];outliers=[]
 for case in sorted((a.root/'Runtime/Cases').iterdir()):
  c=load(case/'perf02-config.json');cr=load(case/'case-result.json') if (case/'case-result.json').exists() else {};r=load(case/'result-Observe.json') if (case/'result-Observe.json').exists() else {};ok=cr.get('launcherExit')==0 and r.get('status')=='PASS' and cr.get('sidecarStopped') and cr.get('sidecarExit') in (None,0)
  if c['scenario']=='Probe':
   samples=lines(case/'probe-samples.jsonl');worker=load(case/'probe-worker.json') if (case/'probe-worker.json').exists() else {};known=[s['threadAllocated'] for s in samples if s['phase']=='known-main-65536' and s['edge']=='same-frame'];apiReliable=bool(known) and all(x>=65536 for x in known) and worker.get('knownDelta',-1)>=worker.get('payload',1)
   allocationCounters=[]
   for s in samples:
    for v in s['counters']:
     if v['name'] in ('GC Alloc','GC Allocated In Frame','GC.Alloc'):allocationCounters.append(dict(phase=s['phase'],edge=s['edge'],frame=s['frame'],**v))
   supported=[v for v in allocationCounters if v['valid'] and v['count']>0 and v['unit']=='Bytes' and v['value']>0];gpuCandidates=[dict(phase=s['phase'],edge=s['edge'],frame=s['frame'],**v) for s in samples for v in s['counters'] if 'gpu' in v['name'].lower()]
   probes.append(dict(case=case.name,status='PASS' if ok and worker.get('done') and worker.get('joined') else 'FAIL',requestedMainPayload=65536,knownMainApiDeltas=known,worker=worker,threadAllocationApiStatus='PASS' if apiReliable else 'NOT_RUN / UNAVAILABLE',allocationRecorderStatus='UNRESOLVED' if supported else 'NOT_RUN / UNAVAILABLE',positiveAllocationRecorderSamples=supported,allAllocationCounterObservations=allocationCounters,gpuCounterCandidates=gpuCandidates,gpuRecorderStatus='OBSERVED / inspect names and units, not all GPU-named markers are GPU frame time' if any(v['valid'] and v['count']>0 and v['value']>0 for v in gpuCandidates) else 'NOT_RUN / UNAVAILABLE',scope='Positive counter alone is not byte-accurate probe correlation; zero-action is not whole game zero allocation'))
   continue
  begin=load(case/'boundary-start.json') if (case/'boundary-start.json').exists() else {};end=load(case/'boundary-end.json') if (case/'boundary-end.json').exists() else {};duration=end.get('time',0)-begin.get('time',0);raw=[];window=[];mapping={}
  if c['variant']=='B' and (case/'minimal-frames.csv').exists():raw=list(csv.DictReader((case/'minimal-frames.csv').open(encoding='utf-8-sig')));window=raw;mapping=dict(interval='interval_ms',main='main_ms',render='render_ms',gpu='gpu_ms',self='sampler_us')
  elif c['variant']=='C' and (case/'frames.csv').exists():raw=list(csv.DictReader((case/'frames.csv').open(encoding='utf-8-sig')));window=[x for x in raw if x['in_window']=='1'];mapping=dict(interval='frame_interval_ms',main='ftm_main_ms',render='ftm_render_ms',gpu='ftm_gpu_ms',self='sampler_previous_us')
  metrics={}
  for label in ('interval','main','render','gpu','self'):
   col=mapping.get(label);values=[]
   for row in window:
    if label in ('main','render','gpu') and row['ftm_new']!='1':continue
    value=float(row[col]);valid=value>=0 if label=='self' else value>0
    if math.isfinite(value) and valid:values.append(value)
   metrics[label]=stats(values,len(window))
   for row in window:
    value=float(row[col]);validFresh=label not in ('main','render','gpu') or row['ftm_new']=='1'
    if validFresh and metrics[label]['p99'] is not None and value>metrics[label]['p99']:outliers.append(dict(case=case.name,metric=label,frame=row['frame'],value=value))
  sameSettings=all(begin.get(x)==end.get(x) for x in ['variant','gpu','graphics','width','height','quality','vSync','limit']);overflow=load(case/'minimal-receipt.json')['overflow'] if (case/'minimal-receipt.json').exists() else False
  actualGpu=load(case/'unity-native-adapter.json') if (case/'unity-native-adapter.json').exists() else None;dxgi=load(case/'dxgi-start.json') if (case/'dxgi-start.json').exists() else None;matched=[x for x in dxgi['adapters'] if actualGpu and x.get('luid')==actualGpu.get('luid') and not x.get('error')] if dxgi else []
  pdh=lines(a.root/'Runtime/System'/case.name/'gpu-pdh.jsonl');validPdh=[]
  for s in pdh:
   for v in s.get('matching',[]):
    if v.get('Status')==0 and v.get('CookedValue',-1)>=0:validPdh.append(v)
  cpu=(end.get('cpuKernelMs',-1)+end.get('cpuUserMs',-1))-(begin.get('cpuKernelMs',-1)+begin.get('cpuUserMs',-1));status='PASS' if ok and duration>=c['seconds']-.01 and sameSettings and not overflow and begin.get('debug')==False else 'FAIL'
  results.append(dict(case=case.name,variant=c['variant'],repetition=c['repetition'],status=status,duration=duration,rawRows=len(raw),windowRows=len(window),metrics=metrics,ftmFresh=sum(x.get('ftm_new')=='1' for x in window),ftmRepeatedOrMissing=sum(x.get('ftm_new')!='1' for x in window),gpuNonpositiveNew=sum(x.get('ftm_new')=='1' and float(x[mapping['gpu']])<=0 for x in window),boundaryStart=begin,boundaryEnd=end,processCpuMs=cpu,gc0Delta=end.get('gc0',0)-begin.get('gc0',0),frameCountDelta=end.get('frame',0)-begin.get('frame',0),nativeGpuIdentity=actualGpu,dxgiActualAdapter=matched[0] if len(matched)==1 else None,dxgiStatus='PASS' if len(matched)==1 and matched[0]['localHr']>=0 and matched[0]['nonlocalHr']>=0 else 'NOT_RUN / UNAVAILABLE',pdhValidSampleCount=len(validPdh),pdhStatus='OBSERVED / validate LUID in raw list' if validPdh else 'NOT_RUN / UNAVAILABLE',scope='Instrumented temporary Player; A per-frame fields absent, not zero; common boundaries include their own bounded overhead'))
 out=dict(cases=results,probes=probes,counts=dict(collections.Counter(x['status'] for x in results)),scope='Measurement capability and bounded comparison, never performance budget/causal attribution or physical input pass')
 (a.output/'summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 with (a.output/'outliers.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=['case','metric','frame','value']);w.writeheader();w.writerows(outliers)
 with (a.output/'summary.csv').open('w',newline='',encoding='utf-8-sig') as f:
  fields=['case','variant','repetition','status','duration','processCpuMs','gc0Delta','windowRows','main_p95','render_p95','gpu_p95','gpu_missing'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for x in results:w.writerow({**{k:x[k] for k in fields[:8]},'main_p95':x['metrics']['main']['p95'],'render_p95':x['metrics']['render']['p95'],'gpu_p95':x['metrics']['gpu']['p95'],'gpu_missing':x['metrics']['gpu']['missing']})
 print(json.dumps(dict(cases=len(results),counts=out['counts'],probes=len(probes),outliers=len(outliers))))
if __name__=='__main__':main()
