# REPORT — PH-R2-R1：构建身份与验收语义修订

| 项 | 值 |
|---|---|
| 项目 | 万象归途（BallMaze） |
| 修订 | PH-R2-R1（承接 PH-R2 / PH-R2-FINAL） |
| 分支 | `verify/ux-progression-03a-player-harness-r2-r1` |
| 基线提交 | `e9f9a142e80f0b4013338f70e5a5b6d1c3776826`（未提交任何新 commit） |
| 批次结论 | **PASS**（范围：定向 A–E，见 §7 与 §8） |
| 生成时间 | 2026-11-11 |
| 状态 | 已完成，**未提交 / 未推送 / 未合并 main / 未启动 03B**，等待独立复审 |

---

## 0. 一句话结论

PH-R2-FINAL 认定的三个技术缺陷（DLL 身份未进链、反击消费一次断言过松、Staff.field 用统一倍率）
全部修复，并用**真实 Player 运行**证明：

- 4 次运行的 `loadedAssemblySha256`（Player 自算）与 `dllSha256Before` 与 `expectedAssemblySha256` **三方逐位一致**（`b3ce427c…1e91`），且与 EXE Launcher 的 `b70442f9…2436` 明确区分；
- 双刃反击**真实取得第二次 contact** 且 `empowered=false`、伤害回落到 0.65×（不是靠缩短冷却绕开）；
- `staff.field` 逐段 `21.45 / 13.20 / 13.20 / 13.20`（0.65 + 0.40×3）全部命中，总伤 61.05；
- 23 项自检 + 40 项独立复算全部通过；190/190 保护文件、311/311 历史证据零改动。

---

## 1. 修改的文件

`git diff --numstat HEAD` 只有 **2 个受跟踪文件**变更：

| 文件 | + | − | 性质 |
|---|---|---|---|
| `Assets/CombatPrototype/Acceptance/PlayerAcceptanceHarness.cs` | 861 | 84 | 验收工具（`#if UX_ACCEPTANCE` 隔离） |
| `player_acceptance_driver.py` | 786 | 47 | 验收驱动脚本（仓库根，非产品代码） |
| **合计** | **1647** | **131** | |

未跟踪（新增）：

| 路径 | 说明 |
|---|---|
| `Evidence/PH-R2-R1/` | 本批证据，124 个文件 |
| `ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/` | 本批 6 份文档 |
| `Assets/Resources.meta` | **Unity 编辑器自动生成的文件夹 meta**（该文件夹内容早已入库，仅 meta 缺失），非人工编辑 |

`git status --porcelain=v2` 原文：`Evidence/PH-R2-R1/protection/GIT_STATUS_porcelain_v2.txt`
`git diff --stat HEAD` 原文：`Evidence/PH-R2-R1/protection/GIT_DIFF_STAT.txt`

---

## 2. 是否存在产品源码修改

**没有。**

| 判定 | 依据 |
|---|---|
| 无产品 `.cs` 变更 | `git diff --name-status HEAD` 仅上表 2 个文件，均在验收工具范畴 |
| 武器数值未动 | `WeaponSkillExpansion.cs`、`NewWeaponCombat.cs` 不在 diff |
| 冷却未动 | 同上；本批所有冷却读数来自产品常量（7 / 9 / 9.5） |
| 存档格式未动 | `CombatSaveData.cs`、`CombatSaveSystem*.cs`、`SaveLocationMigration.cs` 未在 diff |
| 经济 / 掉落 / 随机流未动 | 相关文件未在 diff；v9 存档与掉落表零改动 |
| ProjectSettings / Packages 未动 | 曾出现 Unity 构建自动改写的 4 个设置文件，已在收尾**全部 `git checkout` 还原**（见 §9 G-2） |
| define 未泄漏 | `ProjectSettings.asset` 中 `UX_ACCEPTANCE` 出现 **0** 次，`scriptingDefineSymbols: {}` |

Harness 自身处于 `#if UX_ACCEPTANCE` 之内：NoDefine（出货等价）构建的 DLL 中
`UX_ACCEPTANCE_HARNESS_v1` 出现 **0** 次（双编码扫描），SHA 为 `00373fe7…710e` 且与 Acceptance
DLL `b3ce427c…1e91` 不同 —— 出货构建不包含任何验收代码。

---

## 3. DLL SHA 身份链（R1-01）

### 3.1 清单

`Builds/build-manifest.json`（`schemaVersion=1`）—— 逐项见 `BUILD_IDENTITY.md` §2。

| 产物 | SHA256 |
|---|---|
| Acceptance EXE（Launcher） | `b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436` |
| **Acceptance DLL** | `b3ce427cdc3970b6412972f4c9de89442dd68f5debf572bcfebf8ad5e54a1e91` |
| NoDefine EXE（Launcher） | `b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436` |
| **NoDefine DLL** | `00373fe72161ba7e7c761983ef5865097584837c594a251f0f60a8f00e08710e` |
| buildId | `phr2r1-318c660afbcaf218d04c469b` |

> 两个 EXE 的 SHA **完全相同**（Launcher 桩恒定），这正是 PH-R2 身份链失效的根因。
> 本批把所有身份判定主键换成 DLL；EXE 仅作辅助记录。

### 3.2 三方闭合（4 次运行，逐位一致）

```json
// runs/C-GATE/run-manifest.json（节选）
"dllSha256Before": "b3ce427c…1e91",
"dllSha256After":  "b3ce427c…1e91",
"loadedAssemblyPath": "…\\WanxiangGuitu.Acceptance\\WanxiangGuitu_Data\\Managed\\Assembly-CSharp.dll",
"loadedAssemblySha256": "b3ce427c…1e91",     // Player 自己算的
"expectedAssemblySha256": "b3ce427c…1e91",
"identityVerified": true, "identityReasons": []
```

`loadedAssemblySha256` 由 `Assembly.GetExecutingAssembly().Location` → 打开实际文件 → 流式 SHA256 得到，
**不是**命令行回写。负向证明见下条。

### 3.3 负向证明（真实 Player，非 mock）

自检 ID-1 传入全零 `--expected-dll-sha`：

| 字段 | 值 |
|---|---|
| `loadedAssemblySha256`（Player 实算） | `b3ce427c…1e91` |
| `expectedAssemblySha256` | `0000…0000` |
| `identityVerified` | **false** |
| `exitCode` / `finalStatus` | `1` / **FAIL** |

若 Player 只是回写参数，这里会是"全零 + verified=true"。实测相反 → 自算是真的。

### 3.4 运行前后一致性

每个 Run 都在 Player 退出后重算 EXE/DLL SHA，并与启动前比对；
不一致即 FAIL（自检 ID-3 用篡改值验证了该分支）。

---

## 4. 双刃反击"消费一次"验证（R1-02）

严格判定式（代码原文）：

```csharp
bool ok = evadeSeen && dodgeRollObserved && counterContactSeen && counterEmpowered
          && secondCounterContactSeen && !secondCounterEmpowered;
// 第二次无 contact → incompleteReason 落盘 + Application.Quit(2) → INCOMPLETE
```

任务书 §4 的 11 条逐条证据见 `ACCEPTANCE.md` §5。关键实测：

| 事实 | 值 |
|---|---|
| 敌人攻击被无敌窗拒绝 | `evadeSeen=true`，`evadeSeenAt=7.187345` |
| 真实翻滚 | `dodgeRollObserved=true` |
| 第 1 次反击 contact | `hitId=1`，`counterEmpowered=true`，伤害 `59.39999 = 33 × 1.8` |
| 冷却结束 | 两次 contact 间隔 `9.497s`（`twin.counter` cd 9.5s） |
| 第 2 次反击 contact | `secondCounterContactSeen=true`，`hitTime=12.941937` |
| 第 2 次未强化 | `secondCounterEmpowered=false`，伤害 `21.45 = 33 × 0.65` |

**本批是"真的拿到了第二次 contact"**，不是以 INCOMPLETE 规避。未修改产品冷却，
未触碰 `consumedEvade` / 强化状态；全部经由真实输入 + 真实战斗事件。

---

## 5. Staff.field 逐段伤害验证（R1-03）

`expectedHitRatios = {0.65, 0.40, 0.40, 0.40}`，逐段比对（不是只比总数）：

| 段 | 期望（33×ratio） | 实测 | HP before → after |
|---|---|---|---|
| 1 | 21.45 | **21.45** | 140.00 → 118.55 |
| 2 | 13.20 | **13.20** | 118.55 → 105.35 |
| 3 | 13.20 | **13.20** | 105.35 → 92.15 |
| 4 | 13.20 | **13.20** | 92.15 → 78.95 |
| 总 | 61.05 | **61.05**（ratio 1.000） | |

旧模型（统一 0.65 → `expectedTotal=85.80`）会在这里直接失败；新模型同时满足"逐段正确"与"总数正确"，
且能区分 0.65 与 0.40 两种倍率。详见 `DAMAGE_MODEL.md` §2.2 的反证表。

---

## 6. 定向 Player Run 结果（R1-04）

| Run | 场景 | 进程 | 起止 | 退出码 | 超时 | 身份 | 结论 |
|---|---|---|---|---|---|---|---|
| C-GATE | `sword.triple` | 10600 | 15:35:46–15:36:01 | 0 | 否 | 闭合 | **PASS** |
| TWIN-COUNTER | `twin.counter` | 5256 | 15:36:01–15:36:20 | 0 | 否 | 闭合 | **PASS** |
| STAFF-FIELD | `staff.field` | 31932 | 15:36:20–15:36:37 | 0 | 否 | 闭合 | **PASS** |

- 每个 Run 均有独立 `run-manifest.json`（Driver 在 Player 退出后写），记录
  `exitCode / timedOut / buildId / exeSha256Before|After / dllSha256Before|After /
  loadedAssemblySha256 / identityVerified / resultJsonSha256 / finalStatus`；
- 超时一律 FAIL（自检 "timeout produces FAIL (never PASS)" 实测：`exitCode=1, timedOut=true`，日志完整保留）；
- 每个 Run 使用隔离存储根（`runs/<RUN>/WanxiangGuitu/ForestRuins/save.json`），不写 AppData。

---

## 7. Harness 自测结果

`Evidence/PH-R2-R1/selftest/SELFTEST.json`：**23/23 PASS**（原有 18 + 身份 5）。

| 组 | 内容 | 结果 |
|---|---|---|
| 原有 18 | marker/NoDefine 隔离、C-gate 真实伤害、按键与技能事件、陈旧 result 拒收、错误 buildSha 拒收、超时 FAIL、日志保留、Run 隔离、AppData 保护 | 18/18 |
| 新增 5 | ID-1 错误 DLL SHA（真实 Player 拒绝）、ID-2 Player 内部 SHA 不一致、ID-3 运行中 DLL 变化、ID-4 manifest 与实际 DLL 不符、ID-5 run-manifest 退出码/身份/finalStatus 正确 | 5/5 |

另有 **独立复算 40 项**（`RECOMPUTE.json`，纯读，不启动 Player）：
C-GATE 11/11、TWIN-COUNTER 18/18、STAFF-FIELD 11/11。

---

## 8. AppData 与历史证据保护结果

| 对象 | 期望 | 实测 |
|---|---|---|
| AppData 默认存档 `…\LocalLow\DefaultCompany\万象归途` | 未变 | 未变（前后指纹一致） |
| AppData 旧版存档 `…\LocalLow\BallMaze\ForestRuins` | 未变 | 未变 |
| 受保护文件（任务书 219 行 / 190 唯一路径） | 零改动 | **190/190 MATCH**（原始字节 + git blob OID 双判） |
| PH-R1/PH-R2 历史证据（311 份，含 `Evidence/INDEX.json`、`PLAYER_RUN_MATRIX.csv`、`Runs/R01..R19`、`Evidence/PH-R2/**`） | 零改动 | **311/311 一致** |
| `UX_ACCEPTANCE` 泄漏到 ProjectSettings | 0 | 0 |

证据：`protection/B_protected_recheck.json`、`protection/PROTECTED_SHA256.tsv`、
`protection/history_recheck.json`、`INDEX.json → appdataProtection`。

### 8.1 关于"范围"

本批**没有**重跑 19 项矩阵（任务书 §7 明确要求只做定向 A–E）。
因此本批 PASS 的正确读法是"三个缺陷已修复并可在真实 Player 中复现验证"，
不能读作"19 项全矩阵重新背书"。由于产品源码零改动，PH-R2 的 19 PASS 结论不被推翻，
但**新 DLL 下的全矩阵运行仍未发生**——这是下一轮（如需）的显式待办，不是本批的隐含承诺。

---

## 9. 未关闭问题

| # | 问题 | 等级 | 说明 / 处置 |
|---|---|---|---|
| G-1 | 19 项全矩阵未在新 DLL 下重跑 | 中 | 任务书 §7 限定范围；产品源码零改动、定向 Run 与全部复算通过，风险可控。若复审要求全量背书，需追加一轮完整矩阵（约 19 × 20s + 构建） |
| G-2 | Unity 构建会自动改写 4 个设置文件 | 低 | 实测构建后 `ProjectSettings.asset`、`GraphicsSettings.asset`、`PC_RPAsset.asset`、`UniversalRenderPipelineGlobalSettings.asset` 被编辑器序列化改写（Unicode 转义、空 define 块）。已在收尾 `git checkout` 全部还原，还原后重算：保护面 190/190、产物 SHA 不变。**构建期间这些文件确实处于被改写状态**，但未提交、也未参与任何判定 |
| G-3 | `Assets/Resources.meta` 未跟踪 | 低 | Unity 为已入库的 `Assets/Resources/` 文件夹生成缺失的 meta。未删除（删除会导致编辑器再次生成并可能引起 GUID 抖动），也未提交。建议负责人决定是否随下次提交纳入 |
| G-4 | EXE Launcher SHA 恒定 | 低（已缓解） | 两个构建 EXE 同 SHA，`buildId` 已改为由两个 DLL 主导；审阅者若只看 EXE 仍可能误判，故文档与本报告一律以 DLL 为准 |
| G-5 | 反编译型审查不可用 | 低 | 本批未做 IL 级验证（无 ildasm 工件）。Harness 产品隔离由 marker 双编码扫描 + NoDefine DLL SHA 差异支撑 |
| G-6 | sparse-checkout 仍生效 | 低（沿用） | PH-R1 的 466 个证据文件为 `skip-worktree`，物理未检出，历史复核口径为"快照 SHA 一致"而非"文件可读"。PH-R2-FINAL 的 R5 风险未在本批消除（不在本批授权范围） |
| G-7 | 冷却/时序为实测值，非恒定 | 信息 | 7.10633 / 9.106946 / 9.497 每次会有毫秒级抖动，判定使用容差 −0.6/+1.5，不做逐位相等断言 |

---

## 10. 停止状态

- 未提交（`git status` 仅 2 个已知文件变更 + 未跟踪证据/文档）
- 未推送
- 未合并 main
- 未启动 UX-PROGRESSION-03B
- 未开始其他功能开发

等待负责人独立复审。复审通过后方可进入提交审批。

---

## 附：文件清单

| 文档 | 内容 |
|---|---|
| `REPORT.md` | 本文件：结论、10 项必答、未关闭问题 |
| `ACCEPTANCE.md` | A–E 逐项判定、状态语义、11 条反击条件映射 |
| `TESTING.md` | 环境、命令、23 项自检明细、40 项复算、可重复性 |
| `BUILD_IDENTITY.md` | manifest、buildId 构造、三方闭合、负向证明、NoDefine 隔离 |
| `DAMAGE_MODEL.md` | 逐段倍率、三个 Run 的数值表、12 项校验维度、判定公式 |
| `EVIDENCE_INDEX.md` | 目录结构、关键文件指纹、四条证据链、复核命令 |
