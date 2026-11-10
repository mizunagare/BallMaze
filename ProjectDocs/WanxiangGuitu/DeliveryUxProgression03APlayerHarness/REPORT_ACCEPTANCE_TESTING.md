# REPORT / ACCEPTANCE / TESTING — UX-PROGRESSION-03A 真实 Player 验收（PH-R1）

批次：UX-PROGRESSION-03A-PH-R1
基线：`feature/ux-progression-03a` @ `679815fc0a47a8aa19b54e1d5c1ae88d7a9fd50b`
分支：`verify/ux-progression-03a-player-harness`
Unity：6000.6.5f1 ｜ Acceptance EXE SHA256：`b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436`
产品源码改动：**零**

## 总结论

| 阶段 | 结果 |
|------|------|
| A 工具自测 | **15/15 PASS**（详见 TOOL_SELF_TEST.md） |
| B 3 小样本 | **3/3 PASS**（SAMPLE01/03/10，实测冷却 7.116/8.107/9.107） |
| C 完整 25 项矩阵 | **19 PASS / 0 FAIL / 6 NOT_RUN**（首次批 18/1/6，#18 观测盲区经工具修复后复跑通过；首批 R01-R19 目录保留未覆盖） |

AppData 保护：整批测试前后默认存档目录指纹零变化（default_save/legacy_save 均 true）。

## C 阶段实测证据（每行均来自真实 Player 运行的 result.json）

### 12 项技能（行 1-12）——真实启动/释放/结束/实际冷却
全部 PASS。实测冷却 vs 期望（两次 skill-start 事件间隔，unscaled）：
sword.triple 7.109/7、sword.circle 10.107/10、spear.charge 8.111/8（蓄力 .60s 真实按住）、
spear.sweep 9.106/9、staff.field 9.105/9、staff.echo 9.106/9、bow.burst 9.106/9、
bow.pierce 10.108/10（蓄力 .70s）、twin.volley 7.107/7、gs.cleave 9.109/9、
gs.wave 10.107/10、sc.reap 8.108/8。
（偏差恒为 ~0.107s = harness 第二次注入的 +0.1s 等待余量，非产品偏差。）
每行冷却期内探针重铸均被拦截（blockedDuringCooldown=true）。

### T3 冻结（行 13-14）——仅事件验收
- #13 twin.counter（双刃反击）：真实施放，start/complete 事件观测通过，0.85s 强化窗/
  1.8 倍数值保持冻结。
- #14 sc.pull（灵魂牵引）：真实施放，start/complete 观测通过；`--expect-zero-damage`
  断言 0 伤害通过（damages=0）。

### 聚能 +1s（行 15-17）
focus+sword.circle 11.106/11、focus+spear.charge 9.107/9、focus+bow.pierce 11.109/11 ——
E-A 对称补齐在真实 Player 中逐行验证。

### 回响边界（行 18-19）——运行时描述断言
- #18 echo+sword.slot0：PASS。`combat.SkillDescription` 真实输出
  「周围 5 米造成 200% 攻击伤害（含回响 +25%）」（area 4→5 米，词缀真实生效）。
  槽 0 基础技能经公开 LastAttackId/LastAttackPhase 状态取证（该路径无 Observed 事件）。
- #19 echo+spear.charge.exp：PASS。扩展技能描述不含「含回响 +25%」（R-1 边界：旧扩展
  技能描述不标注回响）。

### NOT_RUN 6 行（#20-#25，诚实理由，不伪造 PASS）
- #20/#21（echo.panel/focus.panel）、#22（gs.cleave.startup）、#23（gs.wave.power）、
  #24（sc.reap.gap）：断言对象是屏幕渲染面板文本（AffixInfo/SkillTradeoffs），无头
  Player 无法可靠读取；其运行时数据来源已被真实运行覆盖（#18/#19 回响标注、#15-#17
  聚能 +1s、#10-#12 数值）。
- #25 regression.P1：旧槽 0 技能语义需产品负责人确认映射（本批不做产品改动）；四把旧
  武器真实技能回归已由 #1-#8 全部通过覆盖；v9/经济/掉落/随机流/ProjectSettings/Packages
  由零改动承诺保证（git diff 可证）。

## 证据清单

- `Evidence/PLAYER_RUN_MATRIX.csv` —— 最终批次逐行状态（冻结列保留，新增 status/reason）
- `Evidence/INDEX.json` —— 全部 Run、AppData 保护、自测结果
- `Evidence/Runs/<run_id>/` —— 每 Run：result.json（runId/processId/buildSha/entryAuthorized/
  cooldownMeasured/skillStarts/skillCompletes/observations/keyEvents/damages）、harness.log
  （逐行实时落盘）、player.log、stdout/stderr、entry-audit.jsonl
- `Builds/acceptance_manifest.json`、`Builds/acc_build_chain.log` —— 构建链证据
- 首批失败保留：`Evidence/Runs/R01..R19`（第一批，含 #18 FAIL）与本批
  `R01-20261110-174744` 等时间戳目录并存，历史未覆盖

## 禁止修改清单核对

产品源码零修改：8 个已实施 C# 文件、技能数值、伤害、攻击判定、冷却规则、v9/v10、
经济、掉落、随机流、用户场景、ProjectSettings、Packages、真实存档全部未动。
本批新增/修改仅：`Assets/CombatPrototype/Acceptance/`（harness）、
`Assets/CombatPrototype/Editor/AcceptanceBuild.cs`、`player_acceptance_driver.py`、
`AcceptanceBuildRunner.sh`、ProjectDocs 交付文档。

## 暂停声明

已推送独立验证分支并核对完整 SHA；产品分支、设计分支、P1/P1C、main 均未移动。
**暂停等待复审：不合 main，不进入 03B。**
