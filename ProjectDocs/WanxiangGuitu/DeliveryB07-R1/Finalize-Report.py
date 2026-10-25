"""Use existing B07 result derivation, append R1-specific acceptance without inheriting PASS."""
import argparse,collections,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--module',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB07/Finalize-Report.py'),'--run',str(a.run),'--module',str(a.module)],check=True)
rows=json.loads((a.run/'results.json').read_text(encoding='utf-8-sig'));index={r['name']:r for r in rows}
cases=[('V01','新显示契约、旧独立OnGUI停用','B07ReadabilityProbe.Run'),('V02','6534点几何等价、六攻击原数值、36布局矩形、随机只读','B07ReadabilityRules.Run'),('V03','38张实际相机受控截图、双Boss/缩放/坡地、像素检查与生命周期','B07ReadabilityVisual.Run'),('V04','相机遮挡契约','B07OcclusionProbe.Run'),('V05','身体/枝冠淡化与恢复、材质清理、HP/控制器/随机不变','B07ActorOcclusion.Run'),('D02','Editor短暂青色帧内部原因','render.first-frame-root-cause')]
table=['','## B07-R1 专项结果','','| 编号 | 检查 | 状态 |','|---|---|---|']
for code,label,method in cases:table.append('| '+code+' | '+label+' | '+index.get(method,{}).get('status','NOT_RUN')+' |')
table+=['','受控显示验证停用NPC，仅验证渲染/相机/几何与规则，不是正常AI战斗。正常AI与最终Player结果仍使用前表的独立进程行。','',
 '稳定帧截图通过不证明短暂青色帧根因已定位，也不代表最终Player原生UI或人工体验通过。',
 '所有首次失败、诊断入口错误、元数据路径错误及修复结果见 [失败历史](FAILURE_HISTORY.md)。','']
path=a.module/'ACCEPTANCE.md';text=path.read_text(encoding='utf8').replace('# B07 验收表','# B07-R1 验收表');path.write_text(text+'\n'.join(table),encoding='utf8')
path=a.module/'REPORT.md';text=path.read_text(encoding='utf8').replace('状态：IN_PROGRESS，最终结果尚未填写。','状态：实现与本轮自动化证据交付，待复审；原生UI与人工理解未执行，已知引擎诊断未关闭。')
text+='\n'+ '\n'.join(table)+'\n最终All运行输入之后只修改报告及证据工具。产品、规则与正常AI代码均按冻结输入核对，构建输入与用户场景/设置差异明确列出。\n'
path.write_text(text,encoding='utf8')
print(json.dumps(dict(counts=dict(collections.Counter(r['status'] for r in rows)),readability={method:index.get(method,{}).get('status','NOT_RUN') for _,_,method in cases})))
