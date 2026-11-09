# SKILL-STATE-01 验收表

> 判据在 [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) 中**先于任何 Player 运行**冻结，未事后调整。
> 状态定义：`PASS-PLAYER`（真实独立 Player 进程）／`PASS-STATIC`／`PASS-EDITOR`／
> `FAIL-PLAYER`／`NOT_RUN`／`INCOMPLETE`。跨 Run 事件不 join；null 时间与缺失事件不得计 PASS。

## 0. 批次门禁

| ID | 检查 | 判据 / 证据 | 结果 |
|---|---|---|---|
| A0-1 | R2 `protection.json` 矛盾核对 | `Evidence/Before/r2-protection-audit.json`：601 变更全在 R2 自身目录、历史目录 0、受保护 tree SHA 全同 | **PASS** |
| A0-2 | 矛盾定性 | `b1b2r1HistoryModified=true` 为宽松前缀误报；`protectedViolations=[]` / `PROTECTION_PASS` 正确 | **PASS** |
| A0-3 | R2 历史保护 | `28d9fc529…` 中 `protection.json` 与全部历史文件原文未改写，仅新增独立勘误 | **PASS** |
| A0-4 | 本批工具整改 | 精确尾斜杠前缀 + 排除自身目录 + 字段更名；实测 `historicalDeliveryModified=false` | **PASS** |
| A1-1 | 从最新开发分支 tip 建独立分支 | 基线 `28d9fc529ba3bc621f0f7e73a183a18fba69f867` → `fix/skill-state-01` | **PASS** |
| A1-2 | 远端 SHA 复核 | 开工与收尾 `git ls-remote`；main/B1/B2/R1/R2 均未移动 | **PASS**（见 `Evidence/After/remote-verification.json`） |
| A1-3 | 不合并 / 不强推 | `noAutoMergeMain=true`、`noForcePush=true` | **PASS** |
| A2-1 | 判据先于测试冻结 | `DESIGN_DECISIONS.md` 写入时间早于首个 Player run；含 C1–C5、TTL/life、修复门槛 | **PASS** |
| A3-1 | 静态审计 | `Evidence/Before/static-audit.json`：11 源码 SHA + **15/15** 冻结事实 | **PASS-STATIC** |
| A3-2 | 纯发行包干净 | 两次构建 `errors=0`、验证 Boot **0**；sidecar 只注入隔离副本 | **PASS-EDITOR** |
| A3-3 | 修复前二进制与 R2 一致 | `PureBuild1` EXE `001aeebf…` / Assembly `3763776a…` 与 R2 逐字一致 | **PASS** |

## 1. 修复前复现（先复现，后修复）

| ID | 检查 | 判据 / 实测 | 结果 |
|---|---|---|---|
| R-1 | 基线符阵链路 | `field-baseline`：1 spawn / 1 resolved / 1 field-created，同帧 | **PASS-PLAYER** |
| R-2 | 真实 UI 全局暂停 4s | `Time.time` 跨度 0.000、`fields` 1→1、恢复后 field-created=1 | **PASS-PLAYER** |
| R-3 | UI-only 2s（`<TTL`） | 跨度 2.006、`fields` 1→1、field-created=1 | **PASS-PLAYER** |
| **R-4** | **UI-only 4s（`>TTL`）负例** | 跨度 **4.006**、`fields` **1→0**、弹体暂停期存活、恢复后 `resolved=1` 但 **`field-created=0`** | **FAIL-PLAYER（负例成立）** |
| R-5 | 负例触发修复门槛 | `REPRODUCED_PRODUCT_DEFECT`、`productFixAuthorised=true` | **PASS** |
| R-6 | UI-only 定性 | 每个 case 标 `controlledStateInjection=true`；真实 UI 入口同时 `timeScale=0`，玩家菜单不可达 | **PASS** |

修复前矩阵：`Evidence/Before/skill-player-matrix-before.json`（12 PASS-PLAYER / 1 FAIL-PLAYER / 1 PARTIAL_OR_NOT_RUN）。
14 个原始 run 完整保存于 `Evidence/Before/Player-Runs-Before/`。

## 2. 最小修复边界

| ID | 检查 | 结果 |
|---|---|---|
| F-1 | 仅修改 `WeaponSkillExpansion.cs` 一处产品文件 | **PASS**（`git diff` 确认） |
| F-2 | 改动仅 3 处：`effectiveTime` 字段+注释、`LateUpdate` 判定、`Release` 登记 | **PASS** |
| F-3 | TTL 仍 3 秒（未改成 30 秒） | **PASS** |
| F-4 | 未清空已释放弹体，`life=2.5s` / `speed` 未改 | **PASS** |
| F-5 | 自然销毁 / 死亡 / 卸载后有界清理（TTL + `OnDisable().fields.Clear()`） | **PASS** |
| F-6 | 未改伤害、技能次数、冷却、瞄准、护甲、经验、经济 | **PASS** |
| F-7 | 未改 v9 存档格式与 `CombatSaveData` | **PASS** |
| F-8 | 未新增技能、未重构技能系统、未升级依赖、未新增 CI | **PASS** |
| F-9 | 其余 8 个受保护产品源码 `UNCHANGED` | **PASS** |

## 3. C1 法杖余烬符阵：弹体命中与延迟生成（修复后）

| ID | 判据 | 证据 | 结果 |
|---|---|---|---|
| C1-1 | 一次释放恰好 1 个弹体 + 1 条 `fields` 登记 | `skill-events.jsonl` spawn=1，`case-summary.fieldsAtPauseStart=1` | **PASS-PLAYER** |
| C1-2 | `resolved` 且非遮挡 → 恰好 1 次 `field-created` + 1 个 `SkillImpactField` | 4 组暂停矩阵全部 1:1 | **PASS-PLAYER** |
| C1-3 | `resolved-blocked-origin` 不生成符阵 | 静态审计 P-5 + 无反向样本（未单独构造遮挡 case） | **PASS-STATIC** |
| C1-4 | 符阵位置/伤害/半径保持产品原值 | 源码 diff 未涉及 `SkillImpactField.Spawn` 参数 | **PASS-STATIC** |
| C1-5 | 不暂停基线 `life=2.5s < TTL=3s` → 有符阵 | `field-baseline` field-created=1 | **PASS-PLAYER** |

## 4. C2 弓蓄力：开始 / 持续 / 释放 / 取消

| ID | 判据 | 实测 | 结果 |
|---|---|---|---|
| C2-1 | `Startup→Charging→charge-locked→Release→Recovery→complete` | `bow-charge` 事件序列完整 | **PASS-PLAYER** |
| C2-2 | `ChargeFraction` ∈[0,1]、按住不超 1s 锁定 | 观测 `ChargeFraction≈0.373`，`Charging` 阶段明确 | **PASS-PLAYER** |
| C2-3 | 锁定后生成 `SkillPiercingProjectile` | `pierce-spawn=1`、`pierce-flight=16`、`complete=1` | **PASS-PLAYER** |
| C2-4 | 取消发 `cancel`、`Phase=Cancelled`，无后续 pierce / 伤害 | `bow-charge-cancel`：`cancel=1`、`pierce-spawn=0`、`release=0`（取消前已 `charge-locked` 属真实时序） | **PASS-PLAYER** |
| C2-5 | 不改 `charge=1` 上限、`1+.85f` 系数、贯穿 3 目标 | 源码 diff 未涉及 | **PASS-STATIC** |

## 5. C3 生命周期

| ID | 场景 | 实测 | 结果 |
|---|---|---|---|
| C3-1 | 真实 UI 全局暂停 | `SetDetails` → `timeScale=0`、`Time.time` 冻结、`fields` 1→1、恢复后正常释放 | **PASS-PLAYER** |
| C3-2 | UI-only 暂停 | 受控注入、明确标注不可达；修复后 4s 仍 1→1 | **PASS-PLAYER（受控）** |
| C3-3 | 死亡 | `resolved=0, field-created=0`，弹体销毁，无补发伤害，`dead=true` | **PASS-PLAYER** |
| C3-4 | 闪避 | `CancelSequence` 取消 active；**已释放**弹体仍 `resolved=1 + field-created=1` | **PASS-PLAYER** |
| C3-5 | 切换武器 / 技能槽 | 同上（换到 Sword / 槽位 2）；`fields` 未被无差别清空 | **PASS-PLAYER** |
| C3-6 | 场景卸载 | `ReturnToTitle` 后 `fieldCreatedCount=0, projectiles=0, fields=0` | **PASS-PLAYER** |
| C3-7 | 自然到期后 `fields` 有界清理 | `after-expiry` 报 `fields=0` | **PASS-PLAYER** |

## 6. C4 时间一致性

| ID | 判据 | 修复前 | 修复后 | 结果 |
|---|---|---|---|---|
| C4-1 | 冻结阈值 TTL=3s / life=2.5s / 暂停 2s 与 4s | 一致 | 一致 | **PASS-MODEL** |
| C4-2 | 弹体恢复后存活且经历有效玩法时间 ≥TTL 时，首次真实命中仍须生成符阵 | **FAIL**（1→0、field-created=0） | **PASS**（1→1、field-created=1） | **PASS-PLAYER（修复后）** |
| C4-3 | `field-created` 与 `resolved` 同一 Run / 同帧；一次 release 最多 1 符阵 | 成立 | 成立 | **PASS-PLAYER** |
| C4-4 | 后续 `SkillImpactField` 脉冲时钟一并审查 | 静态审计 P-15 | 未改产品 | **PASS-STATIC** |
| C4-5 | 不通过延长 TTL / 清空弹体 / 禁用暂停规避 | 修复方案核查 | 见 F-3/F-4 | **PASS** |

## 7. C5 新进程恢复与存档合同

| ID | 判据 | 实测 | 结果 |
|---|---|---|---|
| C5-1 | v9 字段集合不变，仅 `weaponSkillCooldown` 持久化 | 源码 diff 未涉及存档 | **PASS-STATIC** |
| C5-2 | 读档后 `Selected` 回槽 0（CP06-A 明示设计限制） | `selected=0`（写档时为 1） | **PASS-PLAYER** |
| C5-3 | 无 `fields` / 弹体 / 符阵 / 贯矢弹 / active 残留 | 全部 0，`busy=False` | **PASS-PLAYER** |
| C5-4 | `SkillRemaining` 与存档一致 | 修复前 9.545 vs 9.645；修复后 9.474 vs 9.647（读档后自然递减） | **PASS-PLAYER** |
| C5-5 | 不自动释放技能、不补发伤害 | `noAutoRelease=True`、`fieldCreatedCount=0` | **PASS-PLAYER** |
| C5-6 | 真正的新进程、事件不跨 Run join | 修复前 PID 33704 / 8624；修复后写档与读档 PID 不同、runId 不同 | **PASS-PLAYER** |

## 8. 保护、证据与总判定

| ID | 检查 | 结果 |
|---|---|---|
| P-1 | `PROTECTION_PASS`，`protectedViolations=[]` | **PASS**（`Evidence/After/protection.json`） |
| P-2 | 480 变更 = 479 交付文件 + 1 授权产品文件；`historicalDeliveryModified=false` | **PASS** |
| P-3 | 场景 / `ProjectSettings` / 依赖 / 真实存档 / 历史证据零改动 | **PASS** |
| P-4 | 28 个 Player run（14 修复前 + 14 修复后），全量 SHA256 清单 513 文件 | **PASS** |
| P-5 | 失败历史保留（CS1626 编译失败、分析器初始错误判定、修复前全部 run） | **PASS** |
| P-6 | 复跑说明与证据索引齐全 | **PASS**（`TESTING.md` / `Evidence/INDEX.md`） |
| P-7 | 推送后远端完整 SHA 复核、暂停等待复审 | **PASS**（`remote-verification.json`） |

**总判定：**

| 阶段 | 判定 |
|---|---|
| 修复前 | `REPRODUCED_PRODUCT_DEFECT`（唯一产品负例 `field-ui-only-4s`） |
| 修复后 | **`PRODUCT_FIX_VERIFIED`**（13/14 `PASS-PLAYER`，1 项 `PARTIAL_OR_NOT_RUN`） |
| 前后对比 | 唯一变化 `field-ui-only-4s`：FAIL-PLAYER → PASS-PLAYER；12 项保持 PASS 无回归 |

## 9. 明确未覆盖（`NOT_RUN`），复审时请重点确认

| 项 | 原因 | 建议 |
|---|---|---|
| `GameplayPaused=true && timeScale>0` 的玩家正常菜单路径 | 产品 `SetDetails` 同时冻结 timeScale，该组合不可达；本批仅为受控状态注入 | 若产品后续开放此类 UI，需另批复测 |
| `field-natural-expire` 的「射空无命中」子项 | 移除夹具目标后弹体仍扫到 arena 地面几何，产生正常 `resolved` + 符阵；夹具未能制造空域飞行 | 另批设计空域夹具后补测 |
| 原生键鼠 / 独立人工试玩 | 本批为观测 Player + sidecar 业务入口 | 按 `TESTING.md` 补跑 |
| 纯包标题保护 / 全量七武器矩阵 / B2 Editor 几何契约 | 本批仅定向审计技能状态 | 不重复历史批次 |

> 上述 `NOT_RUN` 项**不得**由本批复审改写为 PASS；`field-natural-expire` 保持
> `PARTIAL_OR_NOT_RUN`，不把部分覆盖汇总成无解释的 PASS。
