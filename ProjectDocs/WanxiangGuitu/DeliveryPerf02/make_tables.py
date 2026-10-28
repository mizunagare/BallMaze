"""Descriptive current-run tables and PID/LUID/status-aware capability index."""
import argparse,collections,json,re,math
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines()]
def valid_pdh(v):
 value=v.get('CookedValue');return bool(v.get('actualAdapter') and v.get('Status')==0 and isinstance(value,(int,float)) and math.isfinite(value) and value>=0)
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args();s=load(a.root/'Analysis/summary.json');md='# PERF-02 逐进程结果\n\n同Title/Missing输入，1280×720/PC/D3D11，10秒预热、60秒窗口。所有程序退出/回执与原始记录另存；PASS只表示本次窗口完成，不是性能预算。A无逐帧数据，不能填0。B/C GPU只是有效子集，缺失不填CPU。\n\n|案例|窗口秒|进程CPU ms|GC0增量|CPU主P50/P95/P99 ms|渲染P50/P95/P99 ms|GPU有效P50/P95/P99 ms|GPU缺失/帧|自采样P95 us|\n|---|---|---|---|---|---|---|---|---|\n'
 def triple(v):return '/'.join('NOT_RUN' if v[k] is None else f'{v[k]:.4f}' for k in ('p50','p95','p99'))
 for c in s['cases']:
  m=c['metrics'];selfp=m['self']['p95'];md+=f"|{c['case']}|{c['duration']:.3f}|{c['processCpuMs']:.1f}|{c['gc0Delta']}|{triple(m['main'])}|{triple(m['render'])}|{triple(m['gpu'])}|{str(m['gpu']['missing'])+'/'+str(c['windowRows']) if c['windowRows'] else 'NOT_RUN'}|{selfp if selfp is not None else 'NOT_RUN'}|\n"
 md+='\nA/B/C共同边界的CPU时间含所有Player线程，不是主线程帧时间；进程CPU大于墙钟时间合理。B固定大缓冲与C字符串/CSV/Recorder/系统sidecar也影响堆和GC阈值，不能从C-B或B-A直接作因果。B自身计时不含结束后CSV写出；C自身计时不含全部独立sidecar成本。sidecar自身CPU累计未采集，NOT_RUN。\n\n|案例|工作集开始/结束 MiB|私有内存开始/结束 MiB|Mono使用开始/结束 bytes|帧数变化（非帧间隔分布）|\n|---|---|---|---|---|\n'
 for c in s['cases']:
  b,e=c['boundaryStart'],c['boundaryEnd'];md+=f"|{c['case']}|{b['workingSet']/1048576:.2f}/{e['workingSet']/1048576:.2f}|{b['privateBytes']/1048576:.2f}/{e['privateBytes']/1048576:.2f}|{b['monoUsed']}/{e['monoUsed']}|{c['frameCountDelta']}|\n"
 caps=[]
 for c in sorted((a.root/'Runtime/Cases').iterdir()):
  if not (c/'unity-native-adapter.json').exists():continue
  identity=load(c/'unity-native-adapter.json');uid=identity.get('luid');dxgi=load(c/'dxgi-start.json');matches=[r for r in dxgi['adapters'] if uid and r.get('luid')==uid];sys=a.root/'Runtime/System'/c.name;pdh=[];errors=[]
  diag=sys/'gpu-diagnostic-pdh.jsonl';normal=sys/'gpu-pdh.jsonl'
  for r in jl(diag if diag.exists() else normal):
   errors.extend(r.get('errors',[]) or ([r['error']] if r.get('error') else []))
   for v in r.get('targetSamples',r.get('matching',[])):
    if v is None:continue
    parts=re.search(r'luid_0x([a-f0-9]+)_0x([a-f0-9]+)',v['InstanceName'],re.I);actualUid=''.join(x.zfill(8).lower() for x in parts.groups()) if parts else None
    pdh.append(dict(actualAdapter=actualUid==uid,**v))
  valid=[r for r in pdh if valid_pdh(r)];wmi=jl(sys/'gpu-diagnostic-wmi.jsonl') if (sys/'gpu-diagnostic-wmi.jsonl').exists() else jl(sys/'gpu-wmi.jsonl') if (sys/'gpu-wmi.jsonl').exists() else []
  caps.append(dict(case=c.name,identity=identity,matchedDxgi=matches,dxgiStatus='PASS' if len(matches)==1 and matches[0]['localHr']==0 and matches[0]['nonlocalHr']==0 else 'UNRESOLVED',pdhTargetSamples=len(pdh),pdhActualAdapterValidSamples=valid,pdhInvalidOrOtherAdapterSamples=[r for r in pdh if r not in valid],pdhRawErrors=errors,wmiRows=wmi))
 gpuRecorder=[]
 for p in s['probes']:
  grouped=collections.defaultdict(list)
  for v in p['gpuCounterCandidates']:grouped[(v['name'],v['unit'])].append(v)
  for (name,unit),vs in grouped.items():gpuRecorder.append(dict(case=p['case'],name=name,unit=unit,events=len(vs),uniqueFrames=len({v['frame'] for v in vs}),positiveEvents=sum(v['valid'] and v['count']>0 and v['value']>0 for v in vs),nonpositiveOrUnavailable=sum(not(v['valid'] and v['count']>0 and v['value']>0) for v in vs),maximum=max(v['value'] for v in vs),scope='Phase checkpoints can repeat a frame; do not treat event count as independent frames or a 60s GPU recorder distribution'))
 (a.root/'Analysis/capabilities.json').write_text(json.dumps(dict(gpuMemory=caps,gpuRecorders=gpuRecorder,scope='All raw errors/status preserved. Current application usage and budget are distinct from capacity/free VRAM. A/B unique LUID probing NOT_RUN.'),ensure_ascii=False,indent=2),encoding='utf-8')
 md+='\n## 能力探针与GPU\n\n详见capabilities.json与probe原始行：GC分配Recorder及逐线程字节API在已知分配下不可用。GPU Frame Time有TimeNanoseconds正值子集；FrameTime.GPU未得到可靠正值。阶段检查点会重复同一帧，不冒称独立持续帧。DXGI在C按实际原生设备LUID匹配，local/nonlocal CurrentUsage为应用用量，Budget为OS应用预算，均不是设备剩余容量。A/B没有做该原生LUID查询，NOT_RUN。PDH有效目标与无效/外部适配器/退出附近样本、所有错误分开保留；WMI过滤和client查询均有本轮正例，不反推旧PERF01失败根因。\n'
 (a.root/'Analysis/MEASUREMENTS.md').write_text(md,encoding='utf-8');print('Tables',len(s['cases']),'GPU memory cases',len(caps),'Recorder groups',len(gpuRecorder))
if __name__=='__main__':main()
