# UX-PROGRESSION-03A 验收清单（ACCEPTANCE）

> 与 `IMPLEMENTATION_REPORT.md` 配套。状态图例：✅ 已通过 / ⚠️ 待执行 / ❌ 失败 / 🔒 冻结（不验收数值）

## A. 门禁
- [x] 基线包含 P1 (`ff81eb1cb`) 且 P1C (`4550348f1`) 为祖先
- [x] 实施分支 `feature/ux-progression-03a` 独立，未 merge/cherry-pick main/UX-02/03A/03A-R1

## B. 默认包（P-01 / P-02 / P-03 / P-04）
### B1 P-01 数值（12 项 T1/T2）
| 技能 | 字段 | 期望后值 | 源码 grep | 模型 MODEL_PASS |
|---|---|---|---|---|
| sword.triple | cd | 7 | ✅ | ✅ |
| sword.circle | cd/gap/power | 10/.30/.85 | ✅ | ✅ |
| spear.charge | cd/charge | 8/.60 | ✅ | ✅ |
| spear.sweep | cd/gap/power | 9/.24/.85 | ✅ | ✅ |
| staff.field | cd | 9 | ✅ | ✅ |
| staff.echo | gap/power | .22/.70 | ✅ | ✅ |
| bow.burst | gap/power | .18/.62 | ✅ | ✅ |
| bow.pierce | cd/power/charge | 10/1.35/.70 | ✅ | ✅ |
| gs.cleave | startup | .65 | ✅ | ✅ |
| gs.wave | startup/power | .60/1.30 | ✅ | ✅ |
| sc.reap | gap | .24 | ✅ | ✅ |

### B2 P-02 聚能 +1s
- [x] `WeaponSkillExpansion.TryCast` 对 8 旧扩展技能补 +1s（源码 ✅）
- [x] `AdventureCombat.SkillDuration` 旧扩展分支补 +1s（源码 ✅）
- [x] 槽0 既有 +1s 未被改动（回归 ✅）

### B3 P-03 回响 R-1 边界
- [x] 旧武器仅槽0 ×4、新武器技能 ×6 生效；普攻与旧扩展技能不适用（文案/枚举 ✅）
- [x] 未改动任何判定路径（攻击判定 0 变更）

### B4 P-04 UI（U-01…U-06）
- [x] U-01 回响描述补不适用说明
- [x] U-02 聚能「全部技能冷却 +1s」
- [x] U-03 技能窗 `AffixInfo`（回响适用/不适用、聚能 +1s、冷却读数）
- [x] U-04 槽0 描述「（含回响 +25%）」
- [x] U-05 T3 冻结文案
- [x] U-06 面板三行 + 巨剑前摇与代码同步

## C. 冻结排除项
- [x] T3（`twin.counter` / `sc.pull`）数值冻结 🔒（仅事件验收，不折算 η）
- [x] 9 条品质专属未实施（DESIGN_ONLY）
- [x] R-2 / R-3 / E-B / D-24 未实施

## D. 静态校验
- [x] Unity 批处理编译退出码 0，无 `error CS`
- [x] 平衡模型 12/12 MODEL_PASS，产物 SHA 与 R1 一致

## E. 真机 Player 验收（≥25 次）
- [ ] 25 次真实 `WanxiangGuitu.exe` + 注入输入运行
- 当前状态：**全部 `NOT_RUN`**（见 `Evidence/PLAYER_RUN_MATRIX.csv`）
- 执行方式：`python Evidence/Tools/player_acceptance_driver.py --unity <编辑器> --project <项目> --out Evidence --runs 25`
- 说明：Editor 冒烟测试 / 单元测试 / 离线模型 **均不是** PASS-PLAYER 的替代，必须真机构建运行

## F. 保护
- [x] 仅 8 个 `.cs` 文件变更；P1/P1C/v9/经济/掉落/随机流/用户文件/ProjectSettings/Packages 零偏差
