# Evidence 索引（INDEX）

> 所有哈希为 SHA256（节选前 16 位）。模型产物与 R1 冻结运行逐字节一致。

## A. 平衡模型产物（`build_balance_model.py --out .`）
| 文件 | SHA256(前16) | 说明 |
|---|---|---|
| SKILL_VALUE_MODEL.csv | `50ef984e8f45de41` | 7 普攻 + 4 槽0 + 14 扩展 = 25 行模型读数 |
| BEFORE_AFTER_MATRIX.csv | `0ff88ed648b1f4d3` | 14 技能 + 10 词缀 + 9 品质 + 7 构筑 = 40 行前后对照 |
| SENSITIVITY.csv | `126de53ab4660abf` | N/H 敏感度（162 行，cap/H 为理论假设） |
| FOCUS_SYMMETRY_IMPACT.csv | `e272bb711fbdbb74` | 聚能 E-A +1s 对 8 旧扩展技能影响（8 行） |
| MODEL_SUMMARY.csv | `193c645f5f26a815` | 统计摘要（27 行） |
| Tools/model-run.json | `8943b509bd805c6d` | 参数源 + 产物 SHA + 统计 |

模型统计：`total=14, t1=1, t2=11, t3=2`；`b_lt1_all=8, b_lt1_t3=2, b_lt1_t12=6`；**`model_pass=12, model_fail=0`**；`focus_pass=8, focus_fail=0`；身份误差 ≈ 1.1e-16。
参数源 SHA（`dee5a726…`）与 R1 冻结运行一致 → 模型脚本字节级未偏移。

## B. 真机验收
| 文件 | 状态 |
|---|---|
| PLAYER_RUN_MATRIX.csv | 25 行规划用例，全部 `NOT_RUN`（T3 两行 `T3_FROZEN`） |
| Tools/player_acceptance_harness.cs | 参考 C# 注入器（在 `Evidence/Tools`，不编入游戏） |
| Tools/player_acceptance_driver.py | 构建 + 串行运行 + 汇总编排器 |

## C. 实施代码最终 blob SHA（8 文件，与冻结 PROPOSALS 一致）
| 文件 | git blob SHA256(前16) |
|---|---|
| WeaponSkillExpansion.cs | `5707e9c343f8008c` |
| GreatswordCombat.cs | `21d584fba6caac8b` |
| ScytheCombat.cs | `690e4ea1962f60cf` |
| AdventureCombat.cs | `35f4cd043b11b080` |
| NewWeaponCombat.cs | `00ea5ca3e90fbb36` |
| WeaponTraits.cs | `9c7e6370e0b92839` |
| SkillTradeoffs.cs | `6cf6de8eee8e826c` |
| WeaponSkillPanel.cs | `cff30102e0083096` |

## D. 参考基线 SHA
| 引用 | SHA(前16) |
|---|---|
| 实施基线与分支起点 `design/ux-progression-02` | `1dba0462…` |
| 冻结规格来源 `design/ux-progression-03a-r1` | `600c3dba…` |
| P1 集成点 | `ff81eb1cb` |
| P1C 集成点 | `4550348f1` |

## E. 保护声明
`git diff --stat 1dba0462 HEAD` 仅含上述 8 个 `.cs`（32 增 / 23 删）。P1/P1C/v9/经济/掉落/随机流/用户文件/ProjectSettings/Packages/Resources **零偏差**。
（`Assets/Resources.meta` 为本次 Unity 编译副产物，未纳入提交。）
