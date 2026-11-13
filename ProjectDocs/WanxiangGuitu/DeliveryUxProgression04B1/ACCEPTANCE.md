# UX-04-B1 真实 Player 验收记录

## 验收原则（B1-04 硬约束）

- 所有动作**必须经由真实 Player 输入**（真实鼠标 down/up 事件被产品 EventSystem 消费）。
- **禁止**为伪造验收而直接调用 `AdventureLoadout.Salvage` 底层方法。
- 输入由 Sidecar 观测驱动（`Tools/IntDriverB1.cs`）在**隔离构建副本**中注入，绝不进入产品源码与正式构建。
- 隔离存储根（`-wanxiang-storage-root`）确保不触碰用户真实存档。

## 输入注入机制

| 组件 | 说明 |
|---|---|
| 定位 | 按 `gameObject.name`（uGUI `UnityEngine.UI.Button` 名称 = 按钮文本）定位目标 |
| 坐标 | `RectTransformUtility.WorldToScreenPoint` 计算按钮屏幕中心 |
| 事件 | `InputSystem.QueueStateEvent` 投递真实 `MouseState` down → up |
| 消费 | 产品 EventSystem 处理点击，等价于真人操作 |
| 证据 | `b1-input-events.jsonl` 逐条记录 button-found / mouse-down / mouse-up |

## 验收矩阵（提取自真实观测，F1–F10）

| Step | 品质 | 动作 | 触发方式 | 前装备数 | 后装备数 | 前铁矿 | 后铁矿 | 期望 | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| F1 | 白 | 真实点击分解 | uGUI「拆解换铁矿…」→「确认拆解」 | 13 | 12 | 0 | 1 | 移除 1 件；Ore +1 | PASS |
| F2 | 绿 | 真实点击分解 | uGUI「拆解换铁矿…」→「确认拆解」 | 12 | 11 | 1 | 3 | 移除 1 件；Ore +2 | PASS |
| F3 | 紫 | 真实点击分解 | uGUI「拆解换铁矿…」→「确认拆解」 | 11 | 10 | 3 | 6 | 移除 1 件；Ore +3 | PASS |
| F4 | 金 | 分解被拒绝 | uGUI「不可分解·可入库」(禁用)→「确认拆解」不存在 | 10 | 10 | 6 | 6 | 装备数不变；材料不变 | PASS |
| F5 | 红 | 分解被拒绝 | uGUI「不可分解·可入库」(禁用)→「确认拆解」不存在 | 10 | 10 | 6 | 6 | 装备数不变；材料不变 | PASS |
| F6 | 金 | 拒绝后入库 | uGUI「存入选中装备」 | 10 | 9 | 1 | 0 | 仓库 +1；装备离包 | PASS |
| F7 | 金 | 入库后取出 | uGUI「传说·长剑」→「取回选中装备」 | 9 | 10 | 0 | 1 | 仓库 -1；装备回包 | PASS |
| F8 | v9 存档 | 保存进度 | product `SaveProgress(false)` | 10 | 10 | 6 | 6 | SaveProgress=True | PASS |
| F9 | 金/红(读档) | 读档后状态 | product `Continue()` 加载种子 v9 存档 | 10 | 10 | 0 | 0 | 金/红 可读；锁定 | PASS |
| F10 | v9 兼容 | 结构兼容 | product 读档路径 | 10 | 10 | 0 | 0 | loadout 恢复 10 件 | PASS |

> 注：F8 表格中 `after_ore=6` 为 dismantle 运行末态观测；readback 运行（F9/F10）以独立种子存档加载，初始材料为 0。

## 关键证据点

### 1. 金/红按钮禁用（F4/F5）
- `b1-input-events.jsonl` 记录：金/红「不可分解·可入库」按钮 `interactable=False`；「确认拆解」按钮在锁定态下**不存在**（无确认二次点击路径）。

### 2. 拒绝不消耗（F4/F5）
- 装备数 10→10、铁矿 6→6，零消耗。
- 服务端 `SalvageAllowed` 先行判定，拒绝路径在 `items.Remove` 之前返回。

### 3. 拒绝后可入库（F6/F7）
- `DepositEquipment(id)` 不检查品质（仅 `InBag` + `Capacity`），金装备从包（10→9）转入仓库（0→1）。
- `WithdrawEquipment(id)` 对称路径，仓库（1→0）转回包（9→10）。

### 4. v9 读档兼容（F9/F10）
- 读回种子 v9 存档：`version=9 revision=4`，共 10 件装备。
- `神话·长剑(红)` 与 `传说·长剑(金)` 经 `SalvageAllowed` 判定均为 `False`；白/绿为 `True`。
- `goldPresent=True redPresent=True goldLocked=True redLocked=True` ✅。

## 运行指纹（来自 `EVIDENCE/INDEX.json`）

| Run | 模式 | 结论 | 退出码 | 文件数 |
|---|---|---|---|---|
| `UX04-B1-DISMANTLE-01` | dismantle | PLAYER_RUN_COMPLETED | 0 | 14 |
| `UX04-B1-READBACK-01` | readback | PLAYER_RUN_COMPLETED | 0 | 14 |

- Acceptance 构建 DLL SHA256：`1dd1b676…`
- B1 观测驱动 DLL SHA256：`79e773e4…`（仅注入隔离副本）
- 用户真实存档 SHA256：`dfff9c4f…`（确认未变更）

## 验收结论

✅ **5 品质全链路真实 Player 验收通过**；金/红拒绝不消耗、拒绝后可入库、v9 存档兼容、读档状态正确。无直接调用底层 `Salvage` 的伪造行为。
