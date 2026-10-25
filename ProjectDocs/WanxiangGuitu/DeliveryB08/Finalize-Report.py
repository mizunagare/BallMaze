"""Generate B08 acceptance from an ended final All without inheriting old PASS."""
import argparse
import collections
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--module', type=Path, required=True)
a = p.parse_args()
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
rows = read(a.run / 'results.json')
index = {r['name']: r for r in rows}
if index.get('report.finalized', {}).get('status') != 'PASS':
    raise ValueError('Ended final All required')
ev = a.module / 'Evidence/FinalAll'
proof = read(ev / 'frozen-product-proof.json')
summary = read(ev / 'review-summary.json')
build = read(ev / 'build-summary.json')
counts = dict(collections.Counter(r['status'] for r in rows))
unexpected = [r['name'] for r in rows if r['status'] == 'FAIL' and r['scope'] != 'harness-negative']
def status(names):
    values = [index.get(n, {}).get('status', 'NOT_RUN') for n in names]
    return next((v for v in ['FAIL', 'UNRESOLVED', 'NOT_RUN'] if v in values), 'PASS')
cases = [
 ('B08-01', '新增契约/旧档显式可选状态', ['B08Probe.Run', 'B08Rules.Run'], '受控规则；包括未完成禁止推进、错序设施、保存故障、只读帮助与图标'),
 ('B08-02', '真实采集拾取/账目/撤离取消/结算/取材制造', ['B08Rules.Run', 'B08Rules.Resume'], '受控NPC关闭；调用实际业务与真实倒计时，不是原生输入'),
 ('B08-03', '在途/营地/完成阶段跨进程继续', ['B08Rules.Resume', 'B08Rules.FinalResume', 'B08Rules.CompleteResume'], '独立Editor进程；Run/装备/来源账/随机/教程'),
 ('B08-04', '死亡/放弃重试、跳过后完整循环与继续', ['B08Recovery.Run', 'B08Recovery.Resume'], '受控业务；无补偿或教程奖励'),
 ('B08-04A', '营地真实移动/E交互、战斗时钟和五类冷却暂停', ['B08CampPause.Run'], '受控一秒时钟/真实控制器；不重置技能或制造物资'),
 ('B08-05', '40分辨率/缩放/帮助/错误/仓库布局', ['B08Visual.Run'], '实际渲染的受控夹具；边界/4标签/主目标/只读断言，不是人工可理解性'),
 ('B08-06', '首次正常冒险、制造、第二森林及继续', ['normal-ai.Tutorial.' + m for m in ['Normal', 'Resume', 'FinalResume']], '正常NPC AI+Editor领域机器人；实际移动/普攻/显示E目标/撤离'),
 ('B08-07', '最终非开发Player恢复教程完成的森林Run', ['B08-Player.B08-Tutorial.' + str(i) for i in [1, 2]], '显式隔离合成档；启动/后台WM_CLOSE/审计；不是原生UI'),
 ('REG-01', 'B1/B2/B3/路线评分规则与恢复', ['WGB1Check.Run', 'WGB1Check.Resume', 'WGB1Routes.Run', 'B2Rules.Run', 'B2Rules.Resume', 'B3StreamRules.Run', 'B3Checks.Run', 'B3Checks.Resume', 'RouteScoringRules.Run', 'RouteScoringRules.Resume'], '本轮实际重跑'),
 ('REG-02', '旧档、容器、双武器/冷却、仓库与配方', ['T06RegContainerRuntimeCheck.Run', 'T06RegContainerRuntimeCheck.Final', 'T06RegDualWeaponCheck.Run', 'T06RegWorkbenchCheck.Run', 'B05LegacyMigrationCheck.Run', 'B05V7MigrationCheck.Run', 'B06V8MigrationCheck.Run', 'WGLegacyForestCheck.Run'], '完整明细含其他历史用例，见results.json'),
 ('REG-03', 'Boss战斗/奖励/经济/新进程兼容', ['B07Rules.Run', 'B07Rules.Resume', 'B07Rules.PendingResume', 'B07Rules.CommittedResume', 'B07Combat.Run', 'B07Economy.Run'], '规则/真实物理受控；不冒称原生Boss战'),
 ('REG-04', '原五策略正常冒险与继续', ['normal-ai.' + s + '.' + m for s in ['Gather', 'Treasure', 'Bypass', 'Land', 'Lake'] for m in ['Normal', 'Resume', 'FinalResume']], '正常NPC；15个独立Editor进程'),
 ('BUILD', '非开发Windows64构建', ['WanxiangBuild.ValidateBuild'], 'BuildOptions.None；警告/源码/构建哈希单列')]
lines = ['# B08 验收表', '', '结果仅来自本次最终完整All；历史失败保留，未执行不继承。', '',
         '| 编号 | 检查 | 状态 | 证据类型 |', '|---|---|---|---|']
for number, label, methods, scope in cases:
    lines.append('| ' + ' | '.join([number, label, status(methods), scope + '；`' + '`, `'.join(methods) + '`']) + ' |')
lines += ['| U16 | 最终Player原生键鼠与标题栏关闭 | NOT_RUN | 无安全独立交互环境；后台关闭不可替代 |',
          '| HUMAN | 独立人工可理解性 | NOT_RUN | 未安排，不用截图/机器人冒充 |',
          '| UNKNOWN | D3D12 UNKNOWN根因 | UNRESOLVED | 无新因果证据，不重复实验或改生命周期 |',
          '| RENDER | 既有Editor青色帧内部原因 | UNRESOLVED | 40%像素阈值只是大面积纯青帧检测；不能证明局部渲染无异常 |', '',
          '## All实际状态行', '', json.dumps(counts, ensure_ascii=False), '',
          '非预期FAIL：' + (', '.join(unexpected) or '0') + '。标准负探针FAIL单独保留。协调器exit0不等于全部验收通过。', '',
          '[完整命令/时间/退出码/超时](Evidence/FinalAll/results.json) · [失败历史](FAILURE_HISTORY.md) · [证据索引](Evidence/INDEX.md)', '']
(a.module / 'ACCEPTANCE.md').write_text('\n'.join(lines), encoding='utf8')
body = (a.module / 'REPORT.md').read_text(encoding='utf8').split('<!-- FINAL_VALIDATION -->')[0]
body = body.replace('状态：IN_PROGRESS；不得将定向结果当最终完整 All。', '状态：本轮实现与证据交付，等待复审。原生UI、人工理解与已知诊断保持开放。')
body = body.replace('最终数据、构建哈希和全部失败待新完整All完成后填写。', '最终数据与失败历史见下节及验收表。')
section = ['<!-- FINAL_VALIDATION -->', '## 最终实际验证', '',
           '运行目录：`' + str(a.run) + '`。冻结输入：`' + proof['commit'] + '`。', '',
           '源码核对：产品' + str(proof['count']) + '份、注入测试' + str(len(proof['injectedTests'])) + '份、正常AI执行驱动' + str(len(proof['normalDrivers'])) + '份。', '',
           'All状态行：`' + json.dumps(counts, ensure_ascii=False) + '`；非预期FAIL ' + str(len(unexpected)) + '。', '',
           '```text', build['summary'].strip(), '```', '',
           '正常AI进程：' + str(len(summary['normalProcesses'])) + '；最终Player进程：' + str(len(summary['playerProcesses'])) + '，各自真实退出码/超时/审计独立列出，不相互替代。', '',
           '实际首次教学路线、材料收益、首局/后继Run与教程阶段见review-summary.json。测试无自动授予教程物品；白武器使用既有木2石1矿2配方。', '',
           '产品与执行测试冻结后只增加报告及证据后处理工具。最终完整交付SHA由本报告所在提交和交付消息给出。', '',
           '森林入口的部分受控截图有青色立柱/底座遮挡角色，与ForestRegionRuntime既有入口撤离标记的位置和形状相符；本轮未修改这些几何。不能把它直接当作引擎异常，也不能用布局断言或40%阈值宣称所有画面无遮挡。既有大面积青色帧内部根因仍单独UNRESOLVED。', '',
           '[验收](ACCEPTANCE.md) · [失败历史](FAILURE_HISTORY.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md)', '']
(a.module / 'REPORT.md').write_text(body + '\n'.join(section), encoding='utf8')
print(json.dumps(dict(counts=counts, unexpected=unexpected, b08=summary['b08Methods'])))
