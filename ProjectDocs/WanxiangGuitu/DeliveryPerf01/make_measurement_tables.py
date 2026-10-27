"""Make an explicit final selection table without discarding first failures or missing fields."""
import argparse,collections,json
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('--analysis',type=Path,required=True);a=p.parse_args();data=json.loads((a.analysis/'summary.json').read_text(encoding='utf-8'));cases=data['cases'];selected=[]
 for scenario in ['Title','Camp','Movement','Gather','Combat','Boss','Loop','Resume']:
  for n in range(1,4):
   cand=[x for x in cases if x['config']['scenario']==scenario and x['config'].get('repetition')==n and not x['config'].get('calibration') and x['config'].get('sampling',True) and x['measurementStatus']=='PASS']
   if len(cand)!=1:raise ValueError(f'Expected one eligible current-batch sample {scenario} R{n}, got {len(cand)}; do not hide ambiguity')
   x=cand[0];h=x['header'];assert h['debug']==False and h['width']==1280 and h['height']==720 and h['ftmEnabled']==True
   selected.append(x)
 off=[]
 for n in range(1,4):
  cand=[x for x in cases if x['config']['scenario']=='Title' and x['config'].get('repetition')==n and not x['config'].get('sampling',True) and x['measurementStatus']=='PASS']
  if len(cand)!=1:raise ValueError('Missing or ambiguous sampling-off repetition')
  off.append(cand[0])
 md='# 本轮逐窗口性能分布\n\n仅下列24个完整业务/采样/编排窗口作为8×3基线；另有3个Title关闭额外采集对照。首轮失败、校准与前置准备全部保留在summary.json/CSV和原始数据，不拿替换窗口抹掉失败。P50/P95/P99单位ms，缺失值不填补；GPU只为有效子集分布，缺失数见JSON。不是硬件性能预算通过。\n\n|场景/重复/案例|CPU主P50/P95/P99|CPU渲染P50/P95/P99|GPU有效子集P50/P95/P99|GPU缺失/窗口帧|GC0次数|\n|---|---|---|---|---|---|\n'
 def fm(s):
  return '/'.join('NOT_RUN' if s[k] is None else f'{s[k]:.3f}' for k in ['p50','p95','p99'])
 for x in selected:
  m=x['metrics'];md+=f"|{x['config']['scenario']} R{x['config']['repetition']} `{x['case']}`|{fm(m['cpu_main_ftm_ms'])}|{fm(m['cpu_render_ftm_ms'])}|{fm(m['gpu_ftm_ms'])}|{m['gpu_ftm_ms']['missing']}/{x['windowRows']}|{x['gcCollections0Delta']}|\n"
 md+='\n## 活动、加载与内存\n\n详见每例summary.json：活动切片、实际击败事件、目标、原始窗口起止、GC0、Windows系统样本及内存P50/P95/P99、DrawCalls、Mono/Unity内存、采样器自身耗时。FTM/ProfilerRecorder不同定义分别保留。主/渲染帧时与帧间隔不混用。加载边沿包含应用调度与输入转发，纯区域生成耗时NOT_RUN。\n\n|案例|启动命令→标题秒|继续选择→游戏就绪秒|后继出征请求→就绪秒|工作集P95 MiB|私有内存P95 MiB|实际击败数|\n|---|---|---|---|---|---|---|\n'
 def num(v):return 'NOT_RUN' if v is None else f'{v:.3f}'
 for x in selected:
  l=x['loading'];sm=x['systemMetricsWindow'];ws=sm['working_set_bytes']['p95'];pr=sm['private_bytes']['p95']
  md+=f"|{x['case']}|{num(l['hostCommandStartToTitleSeconds'])}|{num(l['continueSelectedToGameReadySeconds'])}|{num(l['successorInputRequestToReadySeconds'])}|{num(ws/1048576 if ws else None)}|{num(pr/1048576 if pr else None)}|{len(x['defeatsWithinWindow'])}|\n"
 md+='\n## Title关闭额外采集对照\n\n同一V3产物、同60秒/10秒预热、独立进程。OFF仅关闭Recorder/FTM捕获，仍有基础CSV/驱动/系统sidecar/FrameTimingStats构建标志；不同时间系统负载未独占，不从差异推导完整工具开销或因果结论。\n\n|重复|ON帧间隔P50/P95/P99|OFF帧间隔P50/P95/P99|ON采样器自身us P50/P95/P99|OFF自身us P50/P95/P99|\n|---|---|---|---|---|\n'
 for n in range(1,4):
  on=next(x for x in selected if x['config']['scenario']=='Title' and x['config']['repetition']==n);o=off[n-1]
  md+=f"|{n}|{fm(on['metrics']['frame_interval_ms'])}|{fm(o['metrics']['frame_interval_ms'])}|{fm(on['metrics']['sampler_previous_us'])}|{fm(o['metrics']['sampler_previous_us'])}|\n"
 md+='\n没有删除超过P99的帧；outliers.csv保存每个异常帧索引/原值/活动，原始CSV含窗口前后及失败数据。零计时/不可用分配不当作优秀性能。\n'
 (a.analysis/'MEASUREMENTS.md').write_text(md,encoding='utf-8');(a.analysis/'accepted-runs.json').write_text(json.dumps(dict(status='PASS',scope='8x3 current-batch completed mixed workload windows, not performance budget/native/human acceptance',selected=[x['case'] for x in selected],samplingOff=[x['case'] for x in off],allMeasurementsByStatus=dict(collections.Counter(x['measurementStatus'] for x in cases)),allRawCases=len(cases)),indent=2),encoding='utf-8')
 print(json.dumps(dict(selected=len(selected),off=len(off),allCases=len(cases),allMeasurementStatuses=dict(collections.Counter(x['measurementStatus'] for x in cases)))))
if __name__=='__main__':main()
