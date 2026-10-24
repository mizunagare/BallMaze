"""Generate acceptance tables from the final ended All, never from earlier PASSes."""
import argparse
import collections
import csv
import io
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
    raise ValueError('Final All has not ended')
evidence = a.module / 'Evidence/FinalAll'
if not (evidence / 'frozen-product-proof.json').is_file():
    raise ValueError('Publish and seal final input first')
counts = dict(collections.Counter(r['status'] for r in rows))
unexpected = [r['name'] for r in rows if r['status'] == 'FAIL' and r['scope'] != 'harness-negative']
def status(names):
    values = [index.get(name, {}).get('status', 'NOT_RUN') for name in names]
    for value in ['FAIL', 'UNRESOLVED', 'NOT_RUN']:
        if value in values:
            return value
    return 'PASS'

cases = [
 ('S01', 'Editor隔离固定种子仅使用一次、全局随机状态不变', ['B07SeedReplay.Run'], 'Editor专用测试入口；正式Player不含入口'),
 ('B01', '非开发Windows64构建', ['WanxiangBuild.ValidateBuild'], 'BuildOptions.None；完整警告另存'),
 ('C01', '定义、固定种子、合法导航、首次/重复、原子故障', ['B07Rules.Run'], '受控规则/物理导航'),
 ('C02', '六攻击命中/闪避/越界、四武器普攻和主动技能', ['B07Combat.Run'], '受控真实伤害/物理'),
 ('C03', '逐攻击前摇中断、恢复时钟、冲锋抗硬直但受伤', ['B07Interruptions.Run'], '受控真实伤害；不宣称胜利'),
 ('C04', '两个seed×两首领×满血/半血，攻击及脱战返巢', ['B07Liveness.Run'], '8组受控AI，不是正常冒险'),
 ('C05', '满包保留地面装备、整理拾取、穿戴不保护、死亡后重复收益', ['B07Economy.Run'], '受控经济/真实死亡提交'),
 ('P01', 'Running/Pending/Committed新进程恢复、实际对象及防重复', ['B07Rules.Resume', 'B07Rules.PendingResume', 'B07Rules.CommittedResume'], '三个独立Editor进程'),
 ('N01', '陆地Boss采集/制作/战斗/撤离/入仓/再制造/再次出征/继续', ['normal-ai.Land.' + x for x in ['Normal', 'Resume', 'FinalResume']], '正常NPC AI与领域机器人；不是原生输入'),
 ('N02', '湖中Boss同一完整循环与免费出口', ['normal-ai.Lake.' + x for x in ['Normal', 'Resume', 'FinalResume']], '正常NPC AI与领域机器人；不是原生输入'),
 ('N03', '采集、遗迹、绕行三种既有策略', ['normal-ai.' + s + '.' + m for s in ['Gather', 'Treasure', 'Bypass'] for m in ['Normal', 'Resume', 'FinalResume']], '9个正常AI进程'),
 ('R01', 'B1费用/回执、B2目标、B3随机流、R1路线评分', ['WGB1Check.Run', 'WGB1Check.Resume', 'WGB1Routes.Run', 'B2Rules.Run', 'B2Rules.Resume', 'B3StreamRules.Run', 'B3Checks.Run', 'B3Checks.Resume', 'RouteScoringRules.Run', 'RouteScoringRules.Resume'], '本轮重新执行，非继承'),
 ('R02', '旧档迁移、旧森林、合法空状态与恢复', ['B05LegacyMigrationCheck.Run', 'B05V7MigrationCheck.Run', 'B06V8MigrationCheck.Run', 'WGLegacyForestCheck.Run', 'WGA1Check.Empty', 'WGA1Check.Recovery'], '合成旧档/历史夹具'),
 ('P02', 'B07实际冒险派生存档在正式Player保存与新进程继续', ['B07-Player.B07-' + s + '.' + str(n) for s in ['Land', 'Lake'] for n in [1, 2]], '非开发Player；后台WM_CLOSE；非原生战斗'),
]
lines = ['# B07 验收表', '', '以下全部取自最终新 All；历史失败单独保留，不拼接旧 PASS。', '',
         '| 编号 | 检查 | 状态 | 实际证据类型 |', '|---|---|---|---|']
for number, label, names, scope in cases:
    lines.append(f'| {number} | {label} | {status(names)} | {scope}；`' + '`, `'.join(names) + '` |')
for number, label, state, scope in [
 ('U01', '最终Player的原生鼠标键盘U16', 'NOT_RUN', '无安全独立交互环境，不以截图/WM_CLOSE替代'),
 ('U02', '独立人工可理解性与原工程人工试玩', 'NOT_RUN', '未安排，不以机器人替代'),
 ('U03', '最终Player原生Boss战', 'NOT_RUN', '最终Player仅启动/退出/恢复，Boss实战来自隔离Editor正常AI'),
 ('D01', 'D3D12 UNKNOWN根因', index.get('shutdown.root-cause', {}).get('status', 'NOT_RUN'), '沿用UNRESOLVED，不作无新线索实验')]:
    lines.append(f'| {number} | {label} | {state} | {scope} |')
lines += ['', '## 本轮 All 状态行统计', '', json.dumps(counts, ensure_ascii=False), '',
          '非预期失败：' + (', '.join(unexpected) or '0') + '。两个标准负探针单列，不改写为PASS。', '',
          '协调器成功结束只表示编排完成且无非预期失败，不等于原生UI、人工理解或发布验收通过。', '',
          '完整命令、时间、退出码、超时与原始分类：[FinalAll/results.json](Evidence/FinalAll/results.json)。',
          '输入/构建/截图：[证据索引](Evidence/INDEX.md)。历史：[失败记录](FAILURE_HISTORY.md)。', '',
          '首次奖励“已领取”字段表示已生成首奖一次，不表示自动拾取或已入仓；徽章永久，物质战利品仍可因失败损失。',
          '两首领任意顺序；双首领纪念标记不开放未经授权的后续地图。', '']
(a.module / 'ACCEPTANCE.md').write_text('\n'.join(lines), encoding='utf-8')

combat = list(csv.DictReader((a.run / 'Rules/b07-hits.csv').read_text(encoding='utf-8-sig').splitlines()))
out = io.StringIO(newline='')
writer = csv.DictWriter(out, fieldnames=['attack', 'variant', 'before', 'after', 'status', 'scope'])
writer.writeheader()
for row in combat:
    hit = int(row['variant']) == 0
    valid = float(row['after']) < float(row['before']) if hit else float(row['after']) == float(row['before'])
    writer.writerow(dict(attack=row['attack'], variant=['hit', 'dodge', 'outside'][int(row['variant'])], before=row['before'], after=row['after'], status='PASS' if valid else 'FAIL', scope='controlled physics, not native/normal victory'))
(evidence / 'combat-case-results.csv').write_text(out.getvalue(), encoding='utf-8')

summary = read(evidence / 'review-summary.json')
proof = read(evidence / 'frozen-product-proof.json')
build = read(evidence / 'build-summary.json')
section = ['<!-- FINAL_VALIDATION -->', '## 最终实际验证', '',
           '完整 All 运行目录：`' + str(a.run) + '`。', '',
           '冻结输入：`' + proof['commit'] + '`；产品脚本 ' + str(proof['count']) +
           ' 个、注入测试 ' + str(len(proof['injectedTests'])) + ' 个、执行正常AI驱动 ' + str(len(proof['normalDrivers'])) + ' 个分别核对。', '',
           '状态行：`' + json.dumps(counts, ensure_ascii=False) + '`；非预期FAIL：' + str(len(unexpected)) + '。', '',
           '非开发 Windows64 构建（BuildOptions.None）：', '', '```text', build['summary'].strip(), '```', '',
           '正常 AI 证据是隔离Editor中的正常NPC+领域机器人。没有冻结NPC、覆盖生命或直接写胜利字段。正式Player另有启动/退出/恢复证据，不把两类互相冒充。', '',
           '| 策略 | 首领真实释放数（最大记录） | 结算保留材料（皮/晶/核心/木/石/矿） | 保留装备 |', '|---|---:|---|---|']
for name, info in summary['adventures'].items():
    if 'keptMaterials' not in info:
        section.append('| ' + name + ' | NOT_RUN | 不完整；见失败行 | NOT_RUN |')
        continue
    m = info['keptMaterials']
    section.append('| ' + name + ' | ' + str(info['maxObservedReleases']) + ' | ' + '/'.join(str(m[k]) for k in ['MonsterHide', 'CrystalShard', 'BossCore', 'Wood', 'Stone', 'Ore']) + ' | ' + str(len(info['keptGear'])) + '件保留装备（品质详见summary） |')
section += ['', '合成初始物资、制造与实际选用武器见 TESTING。采木后实际制作白弓，主战仍用原选中的白弓；不把这条验证称作装备搭配平衡完成。生命超过100可来自实际升级选择，不是覆盖生命。', '',
            '12次Player进程的实际退出码、超时、强杀标记和审计见 `review-summary.json` 与各cell的process/analysis/storage-audit；仅在该轮全部实际执行时才称12次。', '',
            '最终交付SHA由本报告所在Git提交及交付消息给出；完整运行输入之后仅提交报告/证据工具，不改变产品或测试执行源码。', '']
report = a.module / 'REPORT.md'
body = report.read_text(encoding='utf-8').split('<!-- FINAL_VALIDATION -->')[0]
body = body.replace('状态：IN_PROGRESS。本文先记录实现口径；最终结果以新的完整 All 和证据索引为准。',
                    '状态：实现与自动化证据交付，待复审。原生UI、人工理解及UNKNOWN保持开放；不宣称发布验收通过。')
body = body.replace('待最终完整 All 结束后填写汇总。', '最终数据见下节及验收表。')
report.write_text(body.rstrip() + '\n\n' + '\n'.join(section), encoding='utf-8')
print(json.dumps(dict(counts=counts, unexpectedFailures=unexpected, combatCases=len(combat))))
