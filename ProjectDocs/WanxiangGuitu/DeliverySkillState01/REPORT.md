# SKILL-STATE-01 交付报告

> 批次：`SKILL-STATE-01`（主计划第 6 节 + 本批用户追加的 5 项审计）
> 分支：`fix/skill-state-01`，基线 `28d9fc529ba3bc621f0f7e73a183a18fba69f867`（R2 tip）
> 顺序：**R2 保护核对 → 冻结判据 → 静态审计 → 真实 Player 复现 → 仅负例成立后最小修复 → 同链复验 → 交付**
> 交付后暂停等待复审；`CP06-INTEGRATION-01` / `UX-PROGRESSION-01` 未启动。

---

## 1. 完整 SHA 与分支状态

| 对象 | 完整 SHA | 状态 |
|---|---|---|
| `main` | `72db192a527bd256e2ba18cd7ab334d8334051da` | 未移动 |
| `fix/cp06-crystal-warden-b1` | `a013c15aae15e17af6a7596a022f01f56a745c34` | 未变 |
| `fix/cp06-crystal-warden-b2` | `98924a34b6df817aa5a979b50439a4515881744b` | 未变 |
| `fix/cp06-crystal-warden-b2-r1` | `c388e9b7ecf9b5619a65fac81227eba68f61b832` | 未变 |
| `fix/cp06-crystal-warden-b2-r2`（基线） | `28d9fc529ba3bc621f0f7e73a183a18fba69f867` | 开工未前进、收尾未变 |
| 本批交付 / 复核提交 | 见 [remote-verification.json](Evidence/After/remote-verification.json) 与交付回复 | 推送后 `git ls-remote` 复核 |

未强推、未合并 `main`、未覆盖旧分支；开工与收尾均重新核对远端完整 SHA。

## 2. 第一项：R2 保护哈希矛盾核对

用户指出的矛盾：`DeliveryCrystalCavernC24B2R2/Evidence/After/protection.json` 中
`b1b2r1HistoryModified=true` 但 `protectedViolations=[]`、`verdict=PROTECTION_PASS`。

**结论：这是汇总工具判据的假阳性，不是历史被修改。** 详见
[PROTECTION_AUDIT_R2.md](PROTECTION_AUDIT_R2.md) 与
[Evidence/Before/r2-protection-audit.json](Evidence/Before/r2-protection-audit.json)。

| 检查 | 结果 |
|---|---|
| R1 tip → R2 tip 全部变更 | **601** |
| 其中 R2 自身目录 `DeliveryCrystalCavernC24B2R2/` | **601（100%）** |
| B1 / B2 / R1 / 原 B 历史目录变更 | **0** |
| `ProjectSettings/` / `Packages/` / `.unity` / `.asset` / `Assets/` | **0** |
| 受保护目录的 tree object SHA（R1 tip vs R2 tip） | **全部相同** |
| 宽松前缀 `DeliveryCrystalCavernC24B` 命中 | 601，其中属于历史目录 **0** |

根因：R2 的 `finalize_evidence.py` 用**无尾斜杠**的前缀
`"ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B"` 计算
`b1b2r1HistoryModified`，该前缀同时匹配本批自身的 `…C24B2R2/`；而
`PROTECTED_PREFIXES` 使用带尾斜杠的精确前缀，所以 `protectedViolations=[]` 与
`PROTECTION_PASS` 是**正确**的，`b1b2r1HistoryModified=true` 是**字段名/判据误报**。

处置：**R2 已提交的 `protection.json` 与全部历史文件原样保留、未改写**；本批新增独立勘误；
本批自己的汇总工具改为精确前缀 + 显式排除自身目录 + 字段名
`historicalDeliveryModified`（实测为 `false`）。

## 3. 冻结判据与静态审计

[DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) 在**任何 Player 运行之前**冻结：五类合同 C1–C5、
阈值（`fields TTL=3.0s`、`projectile life=2.5s`、暂停 2s/4s）、UI-only 受控注入定义、
修复门槛与禁止边界。

[Evidence/Before/static-audit.json](Evidence/Before/static-audit.json)：11 个产品源码 SHA256 +
**15/15** 冻结控制流事实全部命中，结论 `PASS-STATIC`，明确标注
`productVerdict = NOT_DECIDED_BY_STATIC_AUDIT`（静态推导不判产品 FAIL，也不授权改码）。

## 4. 先复现：修复前真实 Player 负例

沿用 R1 的 `build_driver.py` / `run_player.py`（哈希未改，不依赖 `pwsh`），
干净纯发行包 `PureBuild1`：EXE `001aeebf…`、Assembly `3763776a…` 与 **R2 纯包逐字一致**，
`errors=0`、验证 Boot **0**，sidecar 只注入隔离副本。

`Evidence/Before/Player-Runs-Before/` 保留 **14 个独立真实 Player run** 的全部原始证据。
核心矩阵（修复前，`Evidence/Before/skill-player-matrix-before.json`）：

| case | `Time.time` 跨度 | `fields` 起→止 | 弹体暂停期 | resolved | **field-created** | 判定 |
|---|---|---|---|---|---|---|
| `field-baseline` | — | 0→0 | — | 1 | **1** | PASS-PLAYER |
| `field-global-pause-4s`（真实 UI，`timeScale=0`） | **0.000** | 1→1 | 存活 | 1 | **1** | PASS-PLAYER |
| `field-ui-only-2s`（受控注入，`<TTL`） | 2.006 | 1→1 | 存活 | 1 | **1** | PASS-PLAYER |
| **`field-ui-only-4s`（受控注入，`>TTL`）** | **4.006** | **1→0** | **存活** | **1** | **0** | **FAIL-PLAYER** |

负例完全成立：`GameplayPaused=true && timeScale=1` 时 `Time.time` 继续推进而弹体被
`AdventureProjectile.Update()` 冻结；3 秒后 `fields` 记录按 `Time.time >= expires`
被删除，恢复后弹体真实命中（`resolved=1`）却无法生成符阵（`field-created=0`）。
修复前总判定 `REPRODUCED_PRODUCT_DEFECT`，`productFixAuthorised=true`。

**UI-only 可达性事实**：真实 UI 入口 `SetDetails` 打开面板时**同时**置 `HudPanelOpen=true`
与 `Time.timeScale=0`（R2 已实测）。因此该状态在玩家正常菜单中**不可达**；本批通过 sidecar
设置公开字段 `HudPanelOpen` 作为 **CONTROLLED_STATE_INJECTION** 验证产品已支持的状态合同，
绝不写成「玩家正常菜单已复现」。

## 5. 最小产品修复

仅在 `Assets/CombatPrototype/WeaponSkillExpansion.cs` 做 **3 处**改动
（SHA `1fce49f5…` → `4f8bc464…`）：

```csharp
// 1) 新增字段：只在弹体时钟推进时推进的有效玩法时钟
float effectiveTime;

// 2) LateUpdate：与 AdventureProjectile.Update() 的暂停条件互补
if(hero!=null&&!hero.GameplayPaused&&Time.timeScale>0)effectiveTime+=Time.deltaTime;
expired.Clear();foreach(var pair in fields)if(effectiveTime>=pair.Value.expires)expired.Add(pair.Key);...

// 3) Release：登记改用同一时钟（TTL 仍为 3）
if(c.def.mechanism=="impact-field")fields[c.id]=new PendingField{cast=c,expires=effectiveTime+3};
```

| 约束 | 遵守情况 |
|---|---|
| TTL 数值 | **仍 3 秒**，未改成 30 秒 |
| 已释放弹体 | **未清空**、life/speed 未改 |
| 自然销毁 / 死亡 / 卸载 | 仍由 TTL + `OnDisable` 的 `fields.Clear()` 有界清理 |
| 伤害 / 次数 / 冷却 / 瞄准 / 护甲 / 经验 / 经济 | 未改 |
| v9 存档格式 / `CombatSaveData` | 未改 |
| 其它 8 个受保护产品源码 | `git diff` 全部 `UNCHANGED` |
| 新技能 / 技能系统重构 / 依赖 / CI | 均无 |

## 6. 复验：修复后真实 Player

`PureBuild2`：`errors=0`、验证 Boot 0，EXE 不变、Assembly SHA `53d42b11…`
（唯一变量即上述源码）。`Observed2` 重新编译注入驱动，**14 个 case 全部独立重跑**。

| case | `Time.time` 跨度 | `fields` 起→止 | resolved | **field-created** | 判定 |
|---|---|---|---|---|---|
| `field-baseline` | — | 0→0 | 1 | **1** | PASS-PLAYER |
| `field-global-pause-4s` | 0.000 | 1→1 | 1 | **1** | PASS-PLAYER |
| `field-ui-only-2s` | 2.006 | 1→1 | 1 | **1** | PASS-PLAYER |
| **`field-ui-only-4s`** | **4.004** | **1→1** | **1** | **1** | **PASS-PLAYER** |

`Evidence/After/skill-player-matrix.json`：`PRODUCT_FIX_VERIFIED`；
前后对比中**唯一**状态变化的 case 是 `field-ui-only-4s`（FAIL-PLAYER → PASS-PLAYER），
其余 12 项保持 PASS-PLAYER 无回归。

## 7. 五类合同的验证结果

| 合同 | 结论 | 关键实测 |
|---|---|---|
| **1. 法杖余烬符阵弹体命中与延迟生成** | `PASS-PLAYER` | 每组恰好 1 `spawn`、1 `resolved`、1 `field-created`；`field-created` 与 `resolved` 同帧；实体遮挡路径 (`resolved-blocked-origin`) 不生成符阵；`staff.field` 伤害/半径/位置参数未改 |
| **2. 弓蓄力开始/持续/释放/取消** | `PASS-PLAYER` | `start→windup→Charging(ChargeFraction≈0.373)→charge-locked→release→pierce-spawn→pierce-flight×16→complete`；`bow-charge-cancel` 发出 `cancel`、`Phase=Cancelled`、零 `pierce-spawn`、零后续 `release`（取消前已 `charge-locked` 属真实时序，未产生弹体或伤害） |
| **3. UI 暂停 / 死亡 / 闪避 / 切换武器 / 场景卸载生命周期** | `PASS-PLAYER` | 切槽(→2)/换武器(→Sword)/闪避后**已释放**弹体仍 `resolved=1 + field-created=1`（`CancelSequence` 不清 `fields`）；死亡与卸载后 `resolved=0, field-created=0`，无补发伤害；卸载后 `projectiles=0, fields=0`；自然到期后 `fields=0` 有界清理 |
| **4. 已释放弹体 / pending 记录 / 后续效果时间一致性** | 修复后 `PASS-PLAYER` | 修复前 UI-only 4s 记录先过期（1→0）而弹体存活；修复后两者共用有效玩法时钟（1→1），恢复后一次真实命中只生成一次符阵；`SkillImpactField` 脉冲计时与暂停条件一并纳入静态审计 |
| **5. 新进程恢复的技能状态与存档合同** | `PASS-PLAYER` | 写档进程与读档进程 **PID 不同、runId 不同**（修复前 33704 / 8624；修复后 32048），共享同一存档根目录；读档后 `selected=0`（CP06-A 明示设计限制）、`fields=0`、弹体/符阵/贯矢弹全 0、`busy=False`、`skillRemaining≈9.47–9.55` 对存档 `9.64–9.65`（读档后自然递减）、无自动释放、无跨 Run join |

## 8. 证据分层与未覆盖项

| 层级 | 结论 |
|---|---|
| `PASS-PLAYER` | 修复前 12/14、修复后 13/14；共 **28 个独立真实 Player run**（各含 EXE/Build/驱动 SHA、PID、runId、命令行、日志、原生退出回执、原始事件/帧/断言） |
| `PASS-STATIC` / `PASS-MODEL` | 15/15 冻结事实、11 个源码哈希、确定性阈值复算 |
| `PASS-EDITOR` | 两次纯发行包构建门禁 `result=Succeeded, errors=0`；未重跑 B2 Editor 几何契约 |
| **`NOT_RUN`** | ① `GameplayPaused=true && timeScale>0` 的玩家正常菜单路径（产品 UI 同时冻结 timeScale，不可达）；② `field-natural-expire` 的「射空无命中」子项（移除夹具后弹体扫到 arena 地面几何，属正常产品命中，未伪造）；③ 原生键鼠 / 独立人工 / 纯包标题保护 / 全量七武器矩阵 |

`field-natural-expire` 判为 `PARTIAL_OR_NOT_RUN`，**不把部分覆盖汇总成无解释的 PASS**。
所有 `NOT_RUN` 项与夹具原因见 [TESTING.md](TESTING.md) 第 5 节。

## 9. 失败与修正历史（全部保留）

| 记录 | 说明 |
|---|---|
| `Evidence/Runs/DriverBuild1/driver-compile-failed-1.log` | 首版驱动在 `try/catch` 中用 `yield return`（CS1626）；改用 R1/R2 stack 驱动模式 |
| `Evidence/After/skill-player-matrix-initial.json` / `skill-player-checks-initial.tsv` | 分析器首版把合法 `time=0` 当 null、把加载期 2 帧算进暂停窗口、把夹具造成的正常命中判产品 FAIL；**原始判定保留** |
| `Evidence/Before/Player-Runs-Before/` | 修复前 14 个 run 完整原始证据，未被修复后 run 覆盖 |
| B1 / B2 / R1 / R2 历史报告、失败与原始证据 | 一律未改写 |

以上修正只作用于工具 / sidecar / 分析器，**未事后调整判据、容差、半径或 TTL**；
产品负例在修复前的任一版本判定中始终为 `FAIL-PLAYER`。

## 10. 保护核验

`Evidence/After/protection.json`：`PROTECTION_PASS`，`protectedViolations=[]`（0 违规）；
480 个变更 = 479 个本批交付文件 + **1 个授权产品源码**；
`historicalDeliveryModified=false`、`projectSettingsModified=false`、
`dependenciesModified=false`、`userSceneModified=false`、
`productChangesAreOnlyAuthorisedFile=true`。
`Evidence/After/hash-manifest.json` 覆盖 **513** 个文件；`player-runs.json` 记录 28 个 run。
未升级依赖、未新增 CI、未 force push、未自动合并 `main`。

## 11. 交付物与复审建议

`ProjectDocs/WanxiangGuitu/DeliverySkillState01/`：
`PROTECTION_AUDIT_R2.md`、`DESIGN_DECISIONS.md`、`REPORT.md`、`ACCEPTANCE.md`、
`TESTING.md`、`Evidence/INDEX.md`，以及 `Before/`（R2 勘误、静态审计、修复前矩阵与
14 个 run）、`After/`（修复后矩阵、保护、构建身份、Player 清单、远端复核、全量哈希）、
`Player/`（修复后 14 个 run）、`Runs/`（两次纯包构建、两次驱动编译注入）、`Tools/`（8 个可复跑工具 + 驱动源码）。

复审建议重点：
1. `ACCEPTANCE.md` 中 UI-only 为**受控状态注入**、玩家菜单不可达的定性是否接受；
2. `field-natural-expire` 的 `NOT_RUN` 子项是否需要另批改进夹具；
3. 最小修复把 pending 到期时钟由 `Time.time` 换成有效玩法时钟，是否影响其它依赖
   `fields` 的边缘路径（本批已覆盖切槽/换武器/闪避/死亡/卸载/自然到期）。
