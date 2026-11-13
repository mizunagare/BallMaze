# UX-04-B1 实施报告 · 高品质装备不可分解

| 项 | 值 |
|---|---|
| 批次编号 | UX-04-B1 |
| 功能主题 | 高品质装备不可分解（`高品不可分解`） |
| 产品基线 commit | `e18dc50cadba3b8f78deae83ff051360690116cd` |
| 源分支 | `feature/ux-progression-03` |
| 实施分支 | `feature/ux-progression-04`（独立创建，未回退 main，未覆盖 UX-03 成果） |
| 授权依据 | D-16 = B-1（白/绿/紫可分解；金/红禁分解）；D-24 维持现状 |
| 实施状态 | ✅ 完成，等待复审（未提交 / 未推送 / 未合并 main / 未启动 UX-05） |

---

## 一、正式授权（D-16 = B-1）

- **白 (White) / 绿 (Green) / 紫 (Purple)**：允许分解，保持原有逻辑不变。
- **金 (Gold) / 红 (Red)**：**禁止分解**；界面明确禁用拆解按钮并提示「不可分解 · 可入库」。
- **D-24 维持现状**：攻击力叠加规则、武器伤害、掉落率、宝箱概率等均未改动。
- 规则以 `GearQuality.Gold` 为唯一阈值（枚举值：White=0, Green=1, Purple=2, Gold=3, Red=4），即 `quality < Gold` 方可分解。

## 二、实施基线确认

| 检查项 | 结果 |
|---|---|
| HEAD commit | `e18dc50…` 与产品基线一致（已确认本地=远程） |
| 远程分支 `feature/ux-progression-03` | 与本地匹配 |
| 新分支 `feature/ux-progression-04` | 已从基线独立创建，仅含 3 个 B1 批准文件改动 |
| UX-03 成果 | 完整保留，未被覆盖（原 Acceptance 包未注入 B1 驱动） |

## 三、B1-01 存储路径审查（8 项硬门禁）

| # | 审查项 | 结论 |
|---|---|---|
| 1 | 金/红能否进入普通容器 | ✅ 能。`InBag` 定义为 `!board && !overflow && !worn`，品质不参与判定 |
| 2 | 容量限制 | ✅ `DepositEquipment` 仅检查 `InBag` 与 `CampRuntime.Capacity`，与品质无关 |
| 3 | Overflow（迁移暂存）处理 | ✅ 完整保留，提供「取回背包」路径，不影响品质 |
| 4 | 既有金/红存档读取兼容 | ✅ `ValidateCurrentItem` 用 `quality<5` 校验，金/红均可读取 |
| 5 | 穿戴拒绝（worn）装备能否入库 | ✅ 不能（worn 非 B1 范畴），但 worn 装备本就不属于临时状态，存在产品解锁路径 |
| 6 | 存取是否改变属性 | ✅ 不改变（存取为对称路径，仅移动归属） |
| 7 | 是否存在不可入库状态 | ✅ 仅 `worn/board/overflow/Carried` 受业务逻辑约束，均为临时态且有产品解锁路径 |
| 8 | 是否存在不可分解/不可处理状态 | ✅ 入场保护（`ProtectedEntry`）与 B1 锁定均为**产品内显式可识别态**，非脏状态 |

> **门禁结论**：未发现「不可入库 / 不可分解 / 不可处理」的脏装备状态 → **B1-01 释放**，可继续 B1-02 / B1-03。

## 四、B1-02 分解规则（服务端单点门禁）

- 在 `AdventureLoadout.Salvage` 入口处设置**唯一服务端判定** `SalvageAllowed(item) => item!=null && item.quality < GearQuality.Gold;`
- 金/红被拒绝时：**先判定后改状态**，绝不消耗装备或材料，仅 `NotifyMessage("传说/神话品质不可分解 · 可入库")` 后返回。
- **所有分解入口统一收敛到 `Salvage` 方法**：IMGUI（ContainerInventoryView）与 uGUI（CatInventoryPresenter）均经同一判定。
- 拒绝**不影响**制造 / 拾取 / 分解返还数量 / 经济参数。

## 五、B1-03 UI 提示

- 金/红行显示「**不可分解 · 可入库**」，明细文案「传说/神话品质 · 不可分解 · 可入库」。
- 拆解按钮 `interactable = false`（uGUI）或按钮不渲染（IMGUI），**无纯 UI 隐藏绕过**。
- 不新增弹窗流程、不改变布局；白/绿/紫 UI 完全不变。
- 「可入库」仅在 `InCamp && 仓库未满` 时方显示相关入口，避免误导。

## 六、B1-04 真实 Player 验收

- 通过**真实鼠标输入注入**（`InputSystem.QueueStateEvent` + 按 `gameObject.name` 定位按钮屏幕中心）驱动产品 EventSystem 点击，**禁止直接调用 `Salvage` 底层方法伪造验收**。
- 5 品质全链路验证（详见 `ACCEPTANCE.md` / `PLAYER_RUN_MATRIX.csv`）：
  - 白/绿/紫：真实点击分解成功，装备 -1、铁矿按 `quality+1` 增加；
  - 金/红：拆解按钮禁用，真实点击被拒绝，装备数、材料数均不变；
  - 金：拒绝后可入库（仓库 +1），入库后可取回（仓库 -1）；
  - v9 读档：金/红可读且锁定，白/绿仍允许分解。

## 七、保护域（禁止改动项）

仅 3 个文件因 B1 批准而变更，其余 21 项保护域文件 SHA256 经 `git diff --quiet HEAD` 确认未变（`PROTECTION_SHA256.tsv`）。详见 `DISASSEMBLY_RULES.md` 保护清单与 `TESTING.md` 保护核验。

## 八、交付物清单

`ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B1/`

| 文件 | 内容 |
|---|---|
| `REPORT.md` | 本报告 |
| `ACCEPTANCE.md` | 真实 Player 验收记录（含输入事件证据） |
| `TESTING.md` | 测试方法论、构建链、保护核验 |
| `DISASSEMBLY_RULES.md` | 分解规则规格与保护域 |
| `STORAGE_COMPATIBILITY.md` | 存储兼容性审查（B1-01） |
| `PLAYER_RUN_MATRIX.csv` | 真实点击 10 步验收矩阵 F1–F10 |
| `EVIDENCE/INDEX.json` | 2 次运行 / 2 PASS / 28 文件 / 哈希自洽 |
| `PROTECTION_SHA256.tsv` | 24 项保护域 SHA256 与变更标记 |

> 注：所有失败运行均按规「原样保留」；本次 2 次运行均 PASS，无失败历史需保留。
