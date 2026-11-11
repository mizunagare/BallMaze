# PH-R2-R1-FIX 修订说明（对 PH-R2-R1-FINAL-AUDIT 的增量附注）

**本文件不替代 `PH-R2-R1-FINAL-AUDIT.md`，只追加。**

| 项 | 值 |
|---|---|
| 被附注的报告 | `PH-R2-R1-FINAL-AUDIT.md` |
| 该报告 SHA256（生成时 = 现在） | `7c9c06f5bec3a542ece6102b29e1271612a8a797a970ab64669736db505eea3c` |
| 该报告最后修改时间 | 2026-11-11 16:08（本批未再写入） |
| 附注生效批次 | PH-R2-R1-FIX，构建 `phr2r1-e32e240735e921f7c4aad220` |
| 结论变化 | ~~CONDITIONAL_PASS~~ → **PASS**（解除条件已全部满足） |

原始报告中的 A（Git 工作区）、B（DLL 身份链）、C（双刃反击因果）、D（staff.field 四段）、
E（C-gate）、G（40 项复算）、H（保护文件/历史证据）等**结论均未被推翻**，本轮只处理它列出的
未关闭项与其自身的呈现缺陷。

---

## 1. 四项未关闭问题的处置

| 原编号 | 原等级 | 原描述 | 本轮处置 | 关闭状态 |
|---|---|---|---|---|
| **F-1** | 中 | `DAMAGE_MODEL` §2.3 / `ACCEPTANCE` §5 并列两种基准，制造"contact 早于 evade"误读 | 两文档改为双钟分列 + 换算表 + 统一口径因果序列；Harness 增 `timebase` 区块与 `hitActiveTime`/`hitUnscaledTime` | **CLOSED** |
| **F-1b** | 中低 | `PlayerAcceptanceHarness.cs:502/542` 用 `unscaledTime − lastDamageAt(Time.time)`，1.2s 稳定期恒真 | 引入 `lastDamageUnscaledTime`/`lastDamageActiveTime` 双字段；判据收敛为签名受限的 `DamageWindowShouldClose`（无 activeTime 形参）；`quiet`/`hardcap` 原因可区分；新增 8 项真实自检 | **CLOSED** |
| **F-5** | 中 | 任务书 23 条 ≠ 实际 23 项自检，7 条不在自检内，"时间源统一"实测不成立 | 新增 `SELFTEST_COVERAGE_MATRIX`，23 条逐条映射到真实证据，"时间源统一"升级为 DIRECT_TEST | **CLOSED** |
| **F-2** | 中低 | `PC_RPAsset.asset`、`URPGlobalSettings.asset` 不在保护清单，且无构建前逐文件 SHA | 清单 219 行去重为 190 + 补 2 = **192 唯一**；新增 preflight/postflight 双清单（含 git OID 与 userEdit 标记） | **CLOSED** |

## 2. 原报告中"低"等级项的现状

| 原编号 | 描述 | 现状 |
|---|---|---|
| F-3 | 实际 8 次 Player 启动，文档写"4 次" | 本批文档统一改为"真实运行次数 = 证据目录中 `run-manifest.json` 数量"，本轮为 3 次正向 + 2 次负向（ID-1 负向 + 超时/陈旧/错 SHA 另计），不再使用"4 次"这种口径 |
| F-4 | 17/124 证据被 `*.log` 忽略，入库需 `-f` | 未变，仍成立；`Evidence/PH-R2-R1-FIX` 同样受影响，已在 `EVIDENCE_INDEX.md` 标注 |
| F-6 | `Assets/Resources.meta` 13:53 前即存在 | 未变，本批未产生、未删除（风险 G-3） |

## 3. 本轮新发现（原报告不可能包含）

### 3.1 Unity 构建输入的一次性归一化（重要）

原报告 F-2 只指出"缺清单缺快照"。补上快照后暴露出更深的事实：

- 第 1 次构建（16:42）使 4 个文件**同时**变化：`PC_RPAsset.asset`（URP prefilter 模式重算，30 行）、
  `UniversalRenderPipelineGlobalSettings.asset`（18 行）、`ProjectSettings.asset`
  （`scriptingDefineSymbols: {}` → `Standalone:`，+ unicode 转义）、`GraphicsSettings.asset`（+15 行）。
- 4 个文件在构建前**均与 HEAD 逐字节一致**（`userEditPresent=false`），因此不存在"覆盖用户修改"。
- 第 2、3 次构建前后 4/4 **逐位相同** → 该变化是编辑器 schema 归一化，不是每次构建都改写。

**处置**：按任务书要求**未用 `git checkout` 还原**。代价是工作区保留 4 个 modified 文件；
收益是"零变化"不再依赖事后恢复，而是由第 3 轮构建的可重复性证明。

### 3.2 第一版时钟探针的用例数据错误

第一版把静默期用例的 `damageWindowStart` 设为评估点前 10s，导致 4.5s 硬上限先触发，
4 例返回 `reason=hardcap` 而判 FAIL。**判据本身行为正确，是测试输入错**。
修正为 `startU = u` 并增加 `expectReason` 断言（`""` / `quiet` / `hardcap`）后 10/10 通过。
失败原始证据保留于 `Evidence/PH-R2-R1-FIX/failed/TIMEBASE-probe-data-error/`。

> 这条记录的意义：如果当时用"放宽断言"或"提高上限"让它变绿，就会掩盖"硬上限冒充静默期"的真实风险。
> 现在用例 5 必须 `reason=quiet`、用例 9 必须 `reason=hardcap`，两者不可互换。

## 4. 原报告风险登记表的更新

| 原 ID | 原等级 | 更新 |
|---|---|---|
| R1（DLL SHA 未进身份链） | 高 | PH-R2-R1 已修；本批再次四方一致 → **CLOSED** |
| R2（`build-manifest.json` 不存在） | 中 | 已存在并在本批重建（第 3 轮产物）→ **CLOSED** |
| R5（sparse-checkout 导致 466 文件未检出） | 中 | 本批 `PROTECTED_RECHECK` 用 `git hash-object` 取 worktree OID + `rev-parse HEAD:<path>` 取索引侧 OID，绕开未检出问题 → **降为低** |
| R6（exitCode 仅在 INDEX） | 中 | 已改为逐 Run `run-manifest.json` → **CLOSED** |
| F-1 / F-1b / F-2 / F-5 | 中 / 中低 | 见 §1 → **CLOSED** |
| 新增 G-1…G-4 | — | 见 `PH-R2-R1-FIX-REPORT.md` §11 |

## 5. 结论变更依据

原报告给出的解除条件是：
> 修 F-1（报告记账）、F-1b（统一判据时钟）、F-5（表述对账）、F-2（扩充清单+设置快照），
> 再跑一次定向 A–E 即可转 PASS。

本轮四项全部执行，并跑了 A–F（A/B/C/D/E + 双刃反击冻结回归）：

| 解除条件 | 是否满足 |
|---|---|
| F-1 报告记账 | ✅ 两份文档重写 + 换算表 |
| F-1b 统一判据时钟 | ✅ 单谓词 + 10 例探针 + 8 项自检 |
| F-5 表述对账 | ✅ 23 条逐条映射，NOT_COVERED 0 |
| F-2 扩充清单 + 设置快照 | ✅ 192 唯一 + 三轮闸门 |
| 定向 A–E 通过 | ✅ 全通过，自检 31/31，保护 188/192 未变（4 个为构建输入，已披露），历史 1340/1340 |

→ **CONDITIONAL_PASS 解除，结论更新为 PASS。**

遗留的 G-1…G-4 均为"范围外/待负责人决策"性质，不构成对已验收结论的反证。
