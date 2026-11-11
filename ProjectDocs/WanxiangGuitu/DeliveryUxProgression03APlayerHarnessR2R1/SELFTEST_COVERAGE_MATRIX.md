# SELFTEST_COVERAGE_MATRIX — 自检覆盖范围对账（PH-R2-R1-FIX-03）

> 本文件回答一个问题：**“原任务书 §8 的 23 条要求，究竟哪几条是自动化自检真正断言过的？”**

> 结论先说：31 项自检里 **16 条要求**有直接自动化断言，**6 条**只有真实 Player 原始证据，
> **2 条**只有静态审计，**0 条**完全未覆盖。PLAYER_EVIDENCE / STATIC_AUDIT **不计入自检 PASS**。

## 1. 统计

| 指标 | 数值 |
|---|---|
| 自检总项数 | **31**（原始 18 + 身份 5 + 时间基准 8） |
| 自检是否全通过 | **是** |
| 需求条目 | 23（R10 拆成 R10a/R10b，共 24 行） |
| DIRECT_TEST | **16**（通过 16） |
| PLAYER_EVIDENCE | **6** |
| STATIC_AUDIT | **2** |
| NOT_COVERED | **0** |

## 2. 逐条对账

| ID | 要求 | testId | 证据路径 | 验证方式 | 状态 | 类型 | 局限 |
|---|---|---|---|---|---|---|---|
| R01 | 交付构建包含 harness 标记 | `#1` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#1` | 工具断言：Acceptance 输出目录的 DLL/EXE 字节中含 UX_ACCEPTANCE_HARNESS_v1 | PASS | **DIRECT_TEST** | 只证明该构建含标记，不证明标记指向的代码路径一定被执行 |
| R02 | NoDefine（出货等价）构建不含标记 | `#2` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#2` | 工具断言：NoDefine 输出目录的 DLL/EXE 不含标记 | PASS | **DIRECT_TEST** | — |
| R03 | KeyDown / KeyUp 事件成对记录 | `#5, #6` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#5,#6` | 真实 Player 运行后断言 keyEvents 中 down / up 各至少 1 条 | PASS | **DIRECT_TEST** | 只断言存在性，不校验字符级配对顺序 |
| R04 | Run 隔离（每次运行独立根目录） | `#17` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#17` | 断言自检期间产生 >=4 个独立 SELFTEST* 运行目录 | PASS | **DIRECT_TEST** | — |
| R05 | 旧 result.json 被拒绝 | `#13` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#13` | 预置 1 小时前的 result.json 并缩短超时，工具必须拒绝并报 stale | PASS | **DIRECT_TEST** | — |
| R06 | 错误 buildSha 被拒绝 | `#14` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#14` | 传入 DEADBEEFWRONG 作为 buildSha，工具必须 FAIL | PASS | **DIRECT_TEST** | — |
| R07 | 超时被拒绝且日志保留 | `#15, #16` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#15,#16` | 6s 硬超时 → FAIL（绝不为 PASS），且 stdout/stderr/player.log 均存在 | PASS | **DIRECT_TEST** | — |
| R08 | 默认 AppData 存档目录未被写入 | `#18` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#18` | 批次前后对 default + legacy 两个存档目录做指纹比对 | PASS | **DIRECT_TEST** | 指纹覆盖文件名/大小/内容；不覆盖 NTFS ACL 等元数据 |
| R09 | 时间源统一（settle 判定只用单一时钟） | `TB-0, TB-1, TB-2, TB-3, TB-4, TB-5, TB-6, TB-7` | `Evidence/PH-R2-R1-FIX/runs/TIMEBASE/timebase-probe.json` | 真实 Player 内运行时钟探针（含 Time.timeScale=0、跨时钟偏移、延迟脉冲、硬上限），并对源码做静态断言（不存在 unscaledTime - activeTime 减法） | PASS | **DIRECT_TEST** | 本项为 FIX-01 新增；PH-R2-R1 阶段该要求为 NOT_COVERED（审计 F-5） |
| R10a | CharacterController 位置同步（代码检查） | `STATIC-CC` | `Assets/CombatPrototype/Acceptance/PlayerAcceptanceHarness.cs` | 静态审计：RepositionTargetAdjacentToHero 在写入 transform.position 后执行 cc.enabled=false/true 强制重同步 | PASS | **STATIC_AUDIT** | 只证明代码路径存在，不构成自动化断言 |
| R10b | CharacterController 位置同步（运行时证据） | `RUN-C-GATE, RUN-STAFF-FIELD` | `Evidence/PH-R2-R1-FIX/runs/C-GATE/damage-events.jsonl` | 真实命中发生在目标被重定位到攻击范围内之后（3 段 / 4 段全部命中） | PASS | **PLAYER_EVIDENCE** | 间接证据：以“真实命中发生”推断位置同步生效，无独立同步断言 |
| R11 | 真实目标身份（非伪造敌人） | `#10, RUN-C-GATE` | `Evidence/PH-R2-R1-FIX/runs/C-GATE/result.json` | result.json target.prepared/entityId/archetype/initialHP 与 target-events.jsonl 的 targetId 一致 | PASS | **PLAYER_EVIDENCE** | — |
| R12 | 真实伤害（数值符合冻结模型） | `RUN-C-GATE, RUN-STAFF-FIELD, Evidence/PH-R2-R1-FIX/INDEX.json#phases.B` | `Evidence/PH-R2-R1-FIX/runs/STAFF-FIELD/damage-events.jsonl` | 逐段比对 actualDamage 与 frozen ratio x AP：21.45/13.20/13.20/13.20；C-gate 21.45x3 | PASS | **PLAYER_EVIDENCE** | 工具侧 #10 只断言“捕获到真实伤害”，数值一致性由本行原始事件独立复算 |
| R13 | 强化消费只发生一次（双刃反击） | `RUN-TWIN(frozen)` | `Evidence/PH-R2-R1/runs/TWIN-COUNTER/damage-events.jsonl` | 两次真实 contact：首击 1.8x=59.40 empowered=true；次击 0.65x=21.45 secondCounterEmpowered=false | PASS | **PLAYER_EVIDENCE** | 本批未重跑（修复不触碰其判定路径）；由 F 阶段回归在冻结原始事件上复核 |
| R14 | 牵引完成（soul_pull pull-start） | `RUN-R14(frozen)` | `Evidence/Runs/R14-20261111-120707/result.json` | t3.pullStartSeen=true，峰值位移 0.730588m，期间 HP 不变 | PASS | **PLAYER_EVIDENCE** | 属于 PH-R2 19 项矩阵，不在本批测试范围；证据产生于 PH-R2 DLL，未在 FIX DLL 下重新取证 |
| R15 | 峰值位移（原始位置数据） | `RUN-R14(frozen)` | `Evidence/Runs/R14-20261111-120707/result.json` | t3.pullPeakDisplacement=0.730588（产品口径 0.731m） | PASS | **PLAYER_EVIDENCE** | 同上：PH-R2 DLL 证据，本批未重跑 |
| R16 | 原始数据聚合可追溯到原始事件 | `#23, RECOMPUTE` | `Evidence/PH-R2-R1-FIX/runs/STAFF-FIELD/recompute.json` | 从 damage-events.jsonl / target-events.jsonl 重算段倍率、HP 链、总伤害，并与 result.json 交叉比对 | PASS | **DIRECT_TEST** | — |
| R17 | Define 清理（ProjectSettings 无泄漏） | `STATIC-DEFINE` | `ProjectSettings/ProjectSettings.asset` | 构建链结束后 ProjectSettings.asset 中 UX_ACCEPTANCE 出现次数 = 0，且 NoDefine DLL 不含标记（#2） | PASS | **STATIC_AUDIT** | 静态文本计数；不排除被其它文件间接引用 |
| R18 | AppData 指纹（批次级零变化） | `#18` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#18` | 批次前后 AppData default + legacy 目录指纹一致 | PASS | **DIRECT_TEST** | — |
| R19 | 错误 DLL SHA 被拒绝（真实 Player） | `#19` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST-wrongdllsha-*/run-manifest.json` | Driver 传全零期望 DLL SHA；Player 自算真实 SHA → identityVerified=false → 退出码 1 | PASS | **DIRECT_TEST** | — |
| R20 | Player 内部 SHA 不一致被拒绝 | `#20` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#20` | 篡改 loadedAssemblySha256 + identityVerified=false，verify_run_identity 必须返回原因 | PASS | **DIRECT_TEST** | 纯函数级负向测试，非独立进程 |
| R21 | 构建前后 DLL 变化被拒绝 | `#21` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#21` | 篡改 dllShaAfter，verify_run_identity 必须返回原因 | PASS | **DIRECT_TEST** | — |
| R22 | manifest 与实际 DLL 不一致被拒绝 | `#22` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json#22` | 篡改 manifest.acceptanceDllSha256，verify_manifest 必须返回原因 | PASS | **DIRECT_TEST** | — |
| R23 | run-manifest 记录退出码 / 身份 / 终态 | `#23` | `Evidence/PH-R2-R1-FIX/selftest/SELFTEST-positive-*/run-manifest.json` | 断言 exitCode==0、timedOut==false、finalStatus==PASS、identityVerified==true、resultJsonSha256 与实际文件一致 | PASS | **DIRECT_TEST** | — |

## 3. 与 PH-R2-R1 阶段的差异（F-5 的修复点）

| 项 | PH-R2-R1 | PH-R2-R1-FIX |
|---|---|---|
| 23 条是否一一对应 | 否：任务书 23 条 ≠ 实际 23 项自检，7 条不在自检内 | 是：本表逐条映射，未覆盖项显式标注 |
| “时间源统一” | **NOT_COVERED**（实测不成立，见审计 F-5） | **DIRECT_TEST**：TB-0～TB-7，真实 Player 内探针 + 源码静态断言 |
| CharacterController 同步 | 混在“真实伤害”里笼统叙述 | 拆成 R10a（代码）/ R10b（运行时）两类证据 |
| 强化消费 | 仅引用一次 | 引用两次真实 contact + F 阶段冻结证据回归 |
| 牵引完成 / 峰值位移 | 未标明是否属于本批 | 显式标注“PH-R2 证据、本批未重跑” |
| 原始数据聚合 | 未映射 | R16 → 独立复算 + `recompute.json` |
| Define 清理 | 未映射 | R17 → ProjectSettings 计数 0 + NoDefine DLL 无标记 |

## 4. 复现方式

```bash
cd /i/unity/WanxiangGuitu
# 原始自检输出（31 项）
python -c "import json;d=json.load(open('Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json'));[print(('PASS' if c['ok'] else 'FAIL'),c['check']) for c in d['checks']]"
# 本表重建（只读原始自检输出）
python Evidence/PH-R2-R1-FIX/recompute/build_coverage_matrix.py
```
