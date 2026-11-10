# UX-PROGRESSION-03A 测试方法论（TESTING）

本文件记录默认包如何逐层验证，以及各层能/不能证明什么。

## 层级与工具
| 层 | 目标 | 工具 / 证据 | 能证明 | 不能证明 |
|---|---|---|---|---|
| **L0 源码一致性** | 代码 == 冻结 PROPOSALS | `git grep` 逐字段核对 `BEFORE_AFTER_MATRIX.csv` | 实现与规格逐字一致 | 运行期行为 |
| **L1 编译** | C# 可编译 | 真实 Unity 批处理（`6000.6.5f1`，-nographics -batchmode -quit） | 语法/类型/引用正确 | 数值平衡、玩法体验 |
| **L2 平衡模型** | 冻结后 B/η 落入目标带 | `Evidence/Tools/build_balance_model.py` | T1/T2 12/12 MODEL_PASS（离线） | 真实战斗 DPS/实测 |
| **L3 规则/文案** | 回响边界、UI 文案 | 源码 grep + `ACCEPTANCE.md` B3/B4 | 文本/枚举正确 | 玩家感知 |
| **L4 真机验收** | 真实运行期行为 | `player_acceptance_harness.cs` + `player_acceptance_driver.py` | PASS-PLAYER 真机闸门 | —（最高权威） |

## 本会话已执行
1. **L1 编译**：真实编辑器退出码 0，无 `error CS`（编译在全部代码已改状态下进行，等价于校验最终集成）。
2. **L2 模型**：`python build_balance_model.py --out .` → `model_pass=12 / model_fail=0`，全部产物 SHA 与 R1 冻结运行逐字节一致（`parameterSourceSHA256=dee5a726…`）。
3. **L0/L3**：8 个 `.cs` 全部字段经 grep 核对，与 `BEFORE_AFTER_MATRIX.csv` 后值一致；回响边界与 U-01…U-06 文案/枚举到位。

## 本会话未执行（诚实声明）
- **L4 真机验收**：未构建并串行运行 25 个独立 `WanxiangGuitu.exe`。原因：构建+串行 25 次超出本次执行边界；且任务明确要求真机构建 + `InputSystem.QueueStateEvent` 注入，不可由编辑器/单测/模型替代。
- 已交付完整可运行工具链与 25 行 `PLAYER_RUN_MATRIX.csv`（`NOT_RUN`），在评审方环境一键翻转。

## 关键约束
- **T3 不折算 η**：`twin.counter` / `sc.pull` 数值冻结，仅以专属事件验收；不计入 T1/T2 通过率。
- **攻击判定 0 变更**：P-03 仅澄清回响适用边界（文案/枚举），未触碰任何判定路径。
- **保护**：所有验证仅在 `Assets/CombatPrototype` 的 8 个文件内；其余工程资产零偏差。

## 复现命令
```bash
# L1 编译
"/c/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" -batchmode -nographics \
  -projectPath "I:/unity/WanxiangGuitu" -logFile build.log -quit

# L2 模型
python Evidence/Tools/build_balance_model.py --out .

# L4 真机（评审方环境）
python Evidence/Tools/player_acceptance_driver.py \
  --unity "C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" \
  --project "I:/unity/WanxiangGuitu" --out Evidence --runs 25
```
