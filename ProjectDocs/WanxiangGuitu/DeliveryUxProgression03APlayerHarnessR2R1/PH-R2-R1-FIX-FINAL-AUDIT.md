# PH-R2-R1-FIX-FINAL：最终提交前独立审计报告

- 审计类型：**只读独立审计**（未修改产品源码 / 验收工具 / 设置文件 / 原始证据；未新增 Player Run；未执行 add / commit / push / merge / reset / checkout / restore / clean）
- 审计时间：2026-11-11 22:04 起
- 审计对象：PH-R2-R1-FIX 批次
- 结论：**CONDITIONAL_PASS**（见 §14；条件为 G-2 设置文件处置、FA-2 第 2 轮取证缺口、FA-3 悬空证据路径）

---

## 1. 基线身份

| 项 | 实测值 |
|---|---|
| HEAD | `e9f9a142e80f0b4013338f70e5a5b6d1c3776826` |
| HEAD tree | `20945471121d319c94f3b4f9ad4a5c3152bd899e` |
| 分支 | `verify/ux-progression-03a-player-harness-r2-r1` |
| 暂存区 | 空（`git diff --cached` 无输出） |
| sparse-checkout | 启用（cone 模式，`/Assets/`、`/ProjectSettings/`、部分 `ProjectDocs/`） |

### 1.1 构建产物身份（实测，非引用）

| 产物 | SHA256 | 备注 |
|---|---|---|
| Acceptance DLL | `db258d6e7f02b0b8d968527be8babb96fdfbe45958145a3ad25f39ec04ff2dfe` | FIX 批次身份主键 |
| NoDefine DLL | `f8b44e1e7471e354df9193a6607a680d8f1cf23e2f15c114a1c56e5d13f5b8e0` | 不含 Harness marker |
| Acceptance EXE | `b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436` | Launcher 桩，恒定 |
| NoDefine EXE | `b70442f90…2436` | 与 Acceptance 相同 |
| buildId | `phr2r1-e32e240735e921f7c4aad220` | `Builds/build-manifest.json` |
| Unity | `6000.6.5f1` | |

> **FA-1（重要，任务书输入错误）**：任务书 §2「最终 DLL」写的是 Acceptance `b3ce427c…1e91` / NoDefine `00373fe7…710e`。
> 经查这两个值是 **PH-R2-R1（FIX 前）**批次的 DLL，`buildId=phr2r1-318c660afbcaf218d04c469b`（见 `BUILD_IDENTITY.md` §2 与 §8.1 的显式区分）。
> FIX 批次因改动 Harness（单时钟判据 + v3 + 运行时探针）DLL 必然变化。
> **审计以实测 `db258d6e…` / `f8b44e1e…` 为准**；若按任务书字面值验收，会把正确的 FIX 产物误判为身份不符。

---

## 2. Git 工作区状态（A 阶段）

### 2.1 已跟踪文件修改：6 个，全部在预期范围内

| 文件 | +/− | 归属 |
|---|---|---|
| `Assets/CombatPrototype/Acceptance/PlayerAcceptanceHarness.cs` | +1112 / −84 | A 类：验收工具 |
| `player_acceptance_driver.py` | +1267 / −47 | A 类：验收工具 |
| `Assets/Settings/PC_RPAsset.asset` | +17 / −13 | G-2：Unity 设置（工具链写入） |
| `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset` | +17 / −1 | G-2：同上 |
| `ProjectSettings/GraphicsSettings.asset` | +15 / −0 | G-2：同上（纯新增） |
| `ProjectSettings/ProjectSettings.asset` | +4 / −3 | G-2：同上 |

### 2.2 其他检查

| 检查 | 结果 |
|---|---|
| 删除（D） | 0 |
| 重命名（R） | 0 |
| 产品逻辑源码修改 | **0**（192 保护清单中 188 未变，4 处变化全为上述设置文件） |
| 未跟踪条目 | 92 个顶层条目（详见 §12） |
| `git diff --check` | 1 处：`ProjectSettings.asset:800` 行尾空格（`Standalone: `，Unity 序列化产物） |
| LF/CRLF 告警 | `PlayerAcceptanceHarness.cs` 工作区为 LF，提交时将被转 CRLF（仓库 `.gitattributes` 行为，非本批引入） |

四个 Unity 设置文件保持 modified 状态，**未执行任何 checkout / restore / reset / clean**。

---

## 3. 时间判据源码审计（B 阶段）

### 3.1 单一判据函数

```csharp
internal static bool DamageWindowShouldClose(float nowUnscaled, float lastDamageUnscaled,
                                            float windowStartUnscaled, float hardCapSeconds)
{
    if (windowStartUnscaled < 0f) return true;                 // nothing armed
    bool quiet = lastDamageUnscaled >= 0f && (nowUnscaled - lastDamageUnscaled) > DamageQuietPeriodSeconds;
    bool capped = (nowUnscaled - windowStartUnscaled) > hardCapSeconds;
    return quiet || capped;
}

internal static string DamageWindowCloseReason(float nowUnscaled, float lastDamageUnscaled,
                                               float windowStartUnscaled, float hardCapSeconds)
{
    if (windowStartUnscaled < 0f) return "empty";
    if (lastDamageUnscaled >= 0f && (nowUnscaled - lastDamageUnscaled) > DamageQuietPeriodSeconds) return "quiet";
    if ((nowUnscaled - windowStartUnscaled) > hardCapSeconds) return "hardcap";
    return "";
}
```

| 要求 | 结论 | 证据 |
|---|---|---|
| 稳定期判断只用 unscaledTime | ✅ | 三形参全为 unscaled 语义，无 `activeTime` 形参 |
| 判定函数无 activeTime 参数 | ✅ | 签名本身使跨钟减法**类型层不可写** |
| quiet 与 hardcap 可区分 | ✅ | `DamageWindowCloseReason` 返回 `"quiet"` / `"hardcap"` / `""` |
| hardcap 不冒充 quiet | ✅ | 探针 `no_damage_hardcap_closes` 断言 `reason=="hardcap"` |
| 时间暂停时判定正确 | ✅ | `timeScale=0` 实测 dU=0.409792 / dT=0 |
| 延迟脉冲不被提前截断 | ✅ | `delayed_pulse_at_1.00s_still_open` |

### 3.2 全部时钟调用点穷举

Harness 内 `Time.*` 统计：`unscaledTime` 70 处 / `timeScale` 7 处 / `timeAsDouble` 6 处 / `time` 6 处 / `frameCount` 1 处。

`Time.time` 的 6 处出现全部**非判定路径**：
- 4 处为注释与 JSON 标签字符串（`"Time.timeAsDouble (CombatHealth.activeTime)"`）；
- 2 处为探针**刻意对照测量**（`tbT0 = Time.time;`、`float dT = Time.time - tbT0;`），目的是证明 `timeScale=0` 时 scaled 钟冻结。

`Time.timeAsDouble` 的 6 处全部为取证标签或数据原样透传，无参与比较。

### 3.3 唯一的跨钟减法（已声明，非判定）

`PlayerAcceptanceHarness.cs:1358`

```csharp
["observedClockOffset"] = (lastDamageActiveTime > 0d && lastDamageUnscaledTime > 0f)
    ? (double)lastDamageUnscaledTime - lastDamageActiveTime : 0d,
```

仅用于**报告输出**（展示两钟偏移），不参与任何 `if` 判定。属可接受的可审计取证字段。

### 3.4 决策点全部核对

| 位置 | 传入 now | 传入 last | 传入 start | hardcap |
|---|---|---|---|---|
| `closeDamageWindow` (L544) | `Time.unscaledTime` | `lastDamageUnscaledTime` | `damageWindowStart` | 4.5s |
| `cooldownAllow` (L585) | `Time.unscaledTime` | `lastDamageUnscaledTime` | `damageWindowStart` | 6.0s |
| `TbCase` (L1449) | 参数 | 参数 | 参数 | 参数 |

> **观察 O-4**：hardcap 存在两个不同值（4.5s / 6.0s，按阶段不同），文档 §2.3 未并列声明两个上限。不影响正确性，但读者需注意"hardcap"并非单一常数。

### 3.5 10 项 in-Player 探针原始输出

`Evidence/PH-R2-R1-FIX/timebase-probe.json`（`runId=TIMEBASE`，`buildId=phr2r1-e32e…`，`identityVerified=true`，`settleClock=Time.unscaledTime`，`allOk=true`，caseCount=10）

| # | 用例 | ok | closed | reason |
|---|---|---|---|---|
| 1 | `timescale_zero_unscaled_advances` | ✅ | — | dUnscaled=**0.409792**，dScaled=**0** |
| 2 | `timescale_zero_real_now_stays_open` | ✅ | false | `""` |
| 3 | `quiet_open_at_0.50s` | ✅ | false | `""` |
| 4 | `quiet_open_at_1.19s` | ✅ | false | `""` |
| 5 | `quiet_closes_at_1.21s` | ✅ | true | `quiet` |
| 6 | `delayed_pulse_at_1.00s_still_open` | ✅ | false | `""` |
| 7 | `cross_clock_offset_does_not_close` | ✅ | false | `""` |
| 8 | `no_damage_hardcap_stays_open` | ✅ | false | `""` |
| 9 | `no_damage_hardcap_closes` | ✅ | true | `hardcap` |
| 10 | `legacy_formula_would_close_early` | ✅ | — | legacyValue=**4.408582** > 1.2 |

**缺陷存在性反证**：`legacyValue=4.408582` 说明旧式跨钟公式在 t=+0.05s 就会判定"已静默 4.41s"，远超 1.2s 阈值 → 窗口被错误立即关闭。修复后同刻判定为 `closed=false`。修复有效性成立。

### 3.6 B 阶段结论

**无隐性跨钟计算。** 判定路径、探针、报告三者的时钟边界清晰且可类型层保证。

---

## 4. 双时钟文档审计（C 阶段）

### 4.1 文档矩阵

| 文档 | 双钟关键词 | 职责 | 结论 |
|---|---|---|---|
| `DAMAGE_MODEL.md` | 完整 | §2.3 双钟分列 + §2.3.1 定义与偏移 + §2.3.2 统一因果序列 | ✅ 达标 |
| `ACCEPTANCE.md` | 1 处 | 引用"统一时钟 17.301s" | ✅ 达标 |
| `BUILD_IDENTITY.md` | 0 处 | 构建身份，**不涉及时钟** | ✅ 合理豁免 |
| `EVIDENCE_INDEX.md` | 1 处 | 证据树导航 | ✅ 达标 |
| `PH-R2-R1-FINAL-AUDIT.md` | — | 原始审计报告 | ✅ **未被覆盖**（sha `7c9c06f5bec3a542ece6102b29e1271612a8a797a970ab64669736db505eea3c` 与 FIX 前一致） |

### 4.2 换算公式与偏移推导（可复算）

`§2.3.1` 给出两条**相互独立**的推导路径：

| 路径 | 事件 | unscaledTime | activeTime | 偏移 |
|---|---|---|---|---|
| 1 | 技能 start（首次施放） | `skillStarts[0]` = 7.520294 | `observations[1].time` = 3.161727 | **4.358567** |
| 2 | actual-evaded-attack | `t3.evadeSeenAt` = 7.187345 | `observations[0].time` = 2.828779 | **4.358566** |

审计独立核验：上述 4 个锚点值**全部真实存在于** `Evidence/PH-R2-R1/runs/TWIN-COUNTER/result.json`（字段路径分别为 `.skillStarts[0]`、`.observations[1].time`、`.t3.evadeSeenAt`、`.observations[0].time`），两条路径互差 1e-6。

文档明确声明：`换算常数为本 Run 专用；不同进程启动时刻不同，不可跨 Run 复用`。

### 4.3 双刃反击因果链复核

| 量 | 实测 | 审计复算 |
|---|---|---|
| evadeSeenAt（unscaled） | 7.187345 | — |
| contact#1（activeTime） | 3.444509 | +4.358567 = **7.803076**（文档 7.803075，差 1e-6，见 FA-4） |
| Δ（contact#1 − evade） | — | **0.615731 s** ≤ 0.85s 强化窗 → 强化成立 |
| contact#1 伤害 | 59.39999 | 33 × 1.8 = 59.40 ✅ `counterEmpowered=true` |
| contact#2（activeTime） | 12.941937 | +4.358567 = **17.300504**（文档 17.300503） |
| contact#2 伤害 | 21.45 | 33 × 0.65 = 21.45 ✅ `secondCounterEmpowered=false` |
| 两次接触间隔 | — | 9.497 s ≈ twin.counter 冷却 9.5s ✅ |

**"contact 早于 evade" 的原始悖论已消解**：3.444509（产品钟）与 7.187345（Harness 钟）分属两钟，统一后 contact 发生在 evade 之后 0.616s，与"闪避成功 → 0.85s 强化窗 → 反击命中"的因果顺序一致。

### 4.4 原始时间字段未被覆盖

`target-events.jsonl` / `observations.time` 保留 `activeTime` 原值；`damage-events.jsonl` 同时输出 `hitActiveTime` 与 `hitUnscaledTime` 并各自标注 `*Clock` 字段；帧号 `frame` 保留。换算值只出现在文档列，不写回原始文件。

---

## 5. 23 项覆盖矩阵审计（D 阶段）

`Evidence/PH-R2-R1-FIX/SELFTEST_COVERAGE_MATRIX.json`

| 检查 | 结果 |
|---|---|
| 需求数 / 行数 | 23 / **24**（R10 按 FIX-03 拆为 R10a 代码路径 + R10b 运行时证据，需求计数仍为 23） |
| requirementId 唯一性 | 24/24 唯一，无重复 |
| coverageType 合法性 | 全部属于 {DIRECT_TEST, PLAYER_EVIDENCE, STATIC_AUDIT, NOT_COVERED}，非法值 0 |
| testId 或证据路径 | 24/24 具备（见 FA-3 的一处路径悬空） |
| 验证方式 | 24/24 有 `verificationMethod` |
| 直接测试与间接证据是否混淆 | 未混淆：`STATIC_AUDIT`/`PLAYER_EVIDENCE` 行的 `resolved.ok` 为 `null` 并标注 `note="referenced evidence"`，未冒充自动化断言 |
| NOT_COVERED 是否被判 PASS | 0 项 NOT_COVERED，不存在该项误判 |
| 统计可独立复算 | `{DIRECT:16, PLAYER:6, STATIC:2, NOT_COVERED:0}` 与逐行计数一致 |

**统计口径声明（已遵守）**：16 项 DIRECT_TEST 是唯一可称"自动化断言通过"的层级；PLAYER_EVIDENCE（6）与 STATIC_AUDIT（2）**不得**与 16 相加表述为"24 项自动化 PASS"。本报告不使用该表述。

各行的 `limitation` 字段如实声明了局限，其中：
- `R13`：本批未重跑，由冻结原始事件复核；
- `R14`/`R15`：属 PH-R2 19 项矩阵，证据产生于 **PH-R2 DLL**，未在 FIX DLL 下重新取证（与 G-1/G-4 一致）；
- `R01`/`R03`/`R08`/`R10a`/`R10b`/`R12`/`R17`/`R20`：均给出单项局限说明。

---

## 6. 31 项自检审计（D 阶段续）

`Evidence/PH-R2-R1-FIX/selftest/SELFTEST.json`：`count=31`、`allPassed=true`、逐项 `ok=true` **31/31**。

审计**未采信 `allPassed` 字段**，逐项回溯原始产物：

| 组 | 编号 | 数量 | 原始证据 | 结论 |
|---|---|---|---|---|
| 原始 | #1–#18 | 18 | marker 双编码扫描、EXE/DLL SHA、C-GATE run、artifacts、stale/wrongsha/timeout 负向 run、isolation、AppData 指纹 | 18/18 |
| 身份 | #19–#23 | 5 | `SELFTEST-wrongdllsha` / `wrongsha` / `stale` / `positive` run-manifest | 5/5 |
| 时间基准 | #24–#31 | 8 | `SELFTEST-timebase` run + `timebase-probe.json` | 8/8 |

### 6.1 负向用例原始运行状态（关键）

| 用例 | exitCode | timedOut | identityVerified | finalStatus | 是否如期拒绝 |
|---|---|---|---|---|---|
| `SELFTEST-positive-165256` | 0 | false | true | **PASS** | — |
| `SELFTEST-timebase-165256` | 0 | false | true | **PASS** | — |
| `SELFTEST-stale-165256` | 1 | **true** | false | FAIL | ✅（见 FA-8） |
| `SELFTEST-timeout-165256` | 1 | true | false | FAIL | ✅ 超时绝不 PASS |
| `SELFTEST-wrongsha-165256` | 0 | false | true | **FAIL** | ✅ buildSha 不符被拒（进程本身正常退出） |
| `SELFTEST-wrongdllsha-165256` | 1 | false | false | FAIL | ✅ 期望 DLL SHA 不符被拒 |

`wrongsha` 用例尤其重要：进程 `exit=0`、`identityVerified=true`，仍被判 FAIL —— 证明校验不依赖进程退出码。

> **FA-8（信息级）**：`stale` 用例 `timedOut=true`，其 FAIL 由"陈旧拒绝"与"短超时"共同造成。`SELFTEST.json#13` 的 detail 已显式记录拒绝理由为 `result.json is stale (modified before this run started)`，因此"陈旧拒绝"这一断言仍成立，但该用例不是单因闭环。

---

## 7. 192 个保护文件审计（E 阶段）

`Evidence/PH-R2-R1-FIX/protection/PROTECTED_SHA256.tsv`（193 行 = 1 表头 + 192 数据行）

| 检查 | 结果 |
|---|---|
| 数据行数 | 192 |
| 唯一路径 | **192**（重复 0） |
| 缺失文件 | 0 |
| 越界路径（绝对路径 / `..` / `.git`） | 0 |
| 空 SHA | 0 |
| SHA 格式错误 | 0 |
| **当前 SHA 独立重算一致** | **192/192** |
| **`git rev-parse HEAD:<path>` 一致** | **192/192** |
| **`git hash-object` (worktree) 一致** | **192/192** |
| 相对 FIX 起点变化 | **4**，且全部为构建输入 |

### 7.1 构成

| 类别 | 数量 |
|---|---|
| `WeaponSkillBalance` | 159 |
| `ProjectSettings` | 28 |
| `unity-settings (FIX-04 addition)` | 2 |
| `Packages` | 2 |
| `SaveV9Progression` | 1 |

### 7.2 新增两文件已纳入

| 文件 | 在清单 | 起点 SHA ≠ 当前 |
|---|---|---|
| `Assets/Settings/PC_RPAsset.asset` | ✅ | ✅ |
| `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset` | ✅ | ✅ |

### 7.3 219 → 190 去重独立复算

以 `Evidence/PH-R2/PROTECTED_SHA256.tsv`（220 行 = 1 表头 + **219** 行）为源独立复算：

| 检查 | 结果 |
|---|---|
| 源行数 | 219 |
| 唯一路径 | **190** |
| 重复行数 | **29** |
| 被重复的路径数 | 29 |
| **同路径不同 SHA 冲突** | **0**（说明 29 个重复是同一文件的重复登记，去重无损） |
| 源唯一集 − FIX 清单 | **0**（无遗漏） |
| FIX 清单 − 源唯一集 | 2（恰为 FIX-04 新增的两个设置文件） |

**去重正确，未丢任何受保护文件。**

---

## 8. 三轮构建保护审计（F 阶段）

### 8.1 四文件 SHA 链（逐位）

| 文件 | R1 pre | R1 post | R3 pre | R3 post | 当前工作区 |
|---|---|---|---|---|---|
| `PC_RPAsset.asset` | `92cc0975` | `98a1b54e` | `98a1b54e` | `98a1b54e` | `98a1b54e` |
| `URPGlobalSettings.asset` | `f074f700` | `cbbf7836` | `cbbf7836` | `cbbf7836` | `cbbf7836` |
| `ProjectSettings.asset` | `34cf824f` | `c28e9061` | `c28e9061` | `c28e9061` | `c28e9061` |
| `GraphicsSettings.asset` | `674353be` | `d1288ed7` | `d1288ed7` | `d1288ed7` | `d1288ed7` |

### 8.2 闸门判定

| 检查 | 结果 |
|---|---|
| R1 pre 的 worktree OID == HEAD OID（4/4） | ✅ 构建前与 HEAD 一致 |
| R1 pre `userEditPresent` | 4/4 = **false**（构建前无人工改动） |
| R1 pre → R1 post 变化数 | **4**（一次性归一化，`CHANGED_BY_TOOLCHAIN`） |
| **R1 post == R3 pre（逐位）** | ✅ → **间接证明第 2 轮零漂移** |
| R3 pre == R3 post（逐位） | ✅ 第 3 轮零漂移 |
| R3 post == 当前工作区 | ✅ 最终产物输入即当前磁盘状态 |
| 是否存在构建后 checkout/restore | **否**（4 文件以 modified 留工作区） |

### 8.3 round1 patch 一致性

`build/build-input-diff.round1.patch`（169 行）与当前 `git diff HEAD -- <四文件>`（169 行）逐行一致（仅 `index` 行不同）。**工具链改动自第 1 轮起未被再次触碰。**

### 8.4 第 3 轮产物归属

`Builds/build-manifest.json` `builtAt=2026-11-11T16:52:15`；R3 postflight 时间 `16:51`，三段 A–F 运行 `16:52:20` 起 —— 时间与输入状态均闭合，A–F 使用的 `db258d6e…` 确由零漂移的第 3 轮产出。

> **FA-2（中低，取证缺口）**：`build/` 仅存 **round1** 与 **最终轮** 两套 preflight/postflight（非 round1 那套被最终轮覆盖），**第 2 轮无任何独立文件留痕**（无 pre/post manifest、无构建日志、无 diff），仅有 `INDEX.json#buildInputGate.rounds[1]` 的汇总声明 `unchanged:4, changed:0`。
> 依任务书规则「如果构建前 SHA 缺失，不得推断为零变化」，**不可径行采信第 2 轮的汇总声明**。
> 但 `R1 post == R3 pre` 的逐位等式成立（R2 的输入态 = R1 输出态，R2 的输出态 = R3 输入态），构成对"第 2 轮零漂移"的**有效间接证明**。因此该缺口影响的是"逐轮留痕完整性"，不影响结论真假。

> **FA-6（低）**：R3 preflight 的 `userEditPresent` 4/4 为 `true`。该字段语义实为"工作区 OID 与 HEAD OID 不同"，而非"存在人为编辑"。R1 时两者一致故为 false，R2 起承载 R1 归一化故为 true。字段命名易被误读为"用户改过设置"，建议后续改名为 `differsFromHead`。

---

## 9. 四个 Unity 设置文件语义审查（G 阶段）

### 9.1 `ProjectSettings/ProjectSettings.asset`（+4 / −3）

| 变更 | 前 → 后 | 分类 |
|---|---|---|
| `productName` | `万象归途` → `"\u4E07\u8C61\u5F52\u9014"` | **SERIALIZATION_ONLY**（同一字符串的 Unicode 转义） |
| `metroApplicationDescription` | 同上 | **SERIALIZATION_ONLY** |
| `scriptingDefineSymbols` | `{}` → `{Standalone: ""}` | **DEFAULT_NORMALIZATION**（显式空 define，等价于无 define） |

`UX_ACCEPTANCE` 泄漏计数 **0**，与 `IDENT` 断言一致。

### 9.2 `ProjectSettings/GraphicsSettings.asset`（+15 / −0）

**纯新增，0 删除 0 改写。** 新增字段全部为默认值：`m_GraphicsStateCollection: {fileID: 0}`、`m_CollectionStartupAction: 0`、`m_TraceSendToEditor: 1`、`m_WarmupAsync: 1`、`m_WarmupProgressivelyLimit: -1`、`m_DefaultLightBaker: 0`、`m_ShaderBuildSettings{...: []}` 等。

| 判定项 | 结果 |
|---|---|
| 渲染管线资源引用 | **未变**（`m_CustomRenderPipeline: {fileID: 0}` 未动） |
| URP Global Settings 引用 | **未变**（`m_RenderPipelineGlobalSettingsMap` guid `18dc0cd2…` 未动） |
| Graphics API / Color Space | 未涉及 |
| 光照、阴影、后处理既有值 | 未改写（纯新增行） |

分类：**DEFAULT_NORMALIZATION**（Unity 6000.6 schema 升级补齐新字段默认值）。

### 9.3 `Assets/Settings/PC_RPAsset.asset`（+17 / −13）

**这是四个文件中唯一含"既有值被改写"的文件。** 改写集中在 URP shader 预过滤（variant stripping）开关：

| 字段 | 前 → 后 |
|---|---|
| `m_PrefilteringModeAdditionalLight` | 4 → 0 |
| `m_PrefilteringModeAdditionalLightShadows` | 0 → 2 |
| `m_PrefilteringModeForwardPlus` | 1 → 2 |
| `m_PrefilteringModeScreenSpaceOcclusion` | 1 → 2 |
| `m_PrefilteringModeScreenSpaceReflection` | 1 → 0 |
| `m_PrefilterWriteRenderingLayers` | 0 → 1 |
| `m_PrefilterAlphaOutput` | 0 → 1 |
| `m_PrefilterDBufferMRT3` | 0 → 1 |
| `m_PrefilterSoftShadowsQuality{Low,Medium,High}` | 0 → 1（三项） |
| `m_PrefilterScreenSpaceIrradiance` | 0 → 1 |
| `m_PrefilterBicubicLightmapSampling` | 0 → 1 |

新增字段：`m_ShadowSmallMeshScreenPercentages`、`m_PrefilterPointSamplingUpsampling: 1`、`m_Light2DPrefilteringMode: 0`、`m_Light2DKeptVariantCombos: []`。

**机械分类：EFFECTIVE_CONFIGURATION_CHANGE** —— 这些不是顺序或空字段规范化，而是控制系统保留哪些 shader keyword 的有效配置值。

**实证降级依据**：Player 日志中「shader 被剥离」的可观测面**在 FIX 前后完全一致**：

| 批次 | 每 Run 剥离告警数 | 具体 shader |
|---|---|---|
| `Evidence/Runs/R01…`（PH-R2） | 4 | GaussianDoF / BokehDoF / PaniniProjection |
| `Evidence/Runs/R10…`（PH-R2） | 4 | 同上 |
| `Evidence/PH-R2-R1/runs/*`（3 Run） | 4 / 4 / 4 | 同上 |
| `Evidence/PH-R2-R1-FIX/runs/*`（3 Run） | 4 / 4 / 4 | 同上 |

**新增剥离 0 项**，三代一致。据此将本文件降级为 **DEFAULT_NORMALIZATION（URP 版本驱动的默认值重算）**，并保留残余风险：预过滤只被观测到 DoF/Panini 三项，其余 keyword 的保留集合未做逐项 A/B 比对。

### 9.4 `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset`（+17 / −1）

`m_RuntimeSettings.m_List` 由 `[]` 变为 16 条 rid 引用。

审计核实：这 16 个 rid **本就已在该资产中定义**（`RefIds` 区），且原本已被 `m_Settings.m_SettingsList` 引用；本次仅新增"运行时注册"。对象类型：

`UniversalRendererResources`、`UniversalRenderPipelineRuntimeShaders`、`UniversalRenderPipelineRuntimeTextures`、`URPDefaultVolumeProfileSettings`、`ShaderStrippingSetting`、`RenderGraphGlobalSettings`、`RenderGraphUtilsResources`、`URPReflectionProbeSettings`、`ScreenSpaceAmbientOcclusionBlueNoiseResources`、`ScreenSpaceAmbientOcclusionCoreResources`、`UniversalRenderPipelineRuntimeXRResources`、`MipGenRenderPipelineRuntimeResources`、`ScreenSpaceReflectionPersistentResources`、`UniversalRenderPipelineRuntimeTerrainShaders`、`LightmapSamplingSettings`、`VrsRenderPipelineRuntimeResources`。

分类：**EFFECTIVE_CONFIGURATION_CHANGE**（运行时资源注册由空变为 16 项）。`m_AssetVersion` 仍为 `11`，未升版；无缺失资源报错；3 次 Player Run 渲染与战斗逻辑均正常。

### 9.5 分类汇总

| 文件 | 分类 | 风险保留 |
|---|---|---|
| `ProjectSettings.asset` | SERIALIZATION_ONLY + DEFAULT_NORMALIZATION | 低 |
| `GraphicsSettings.asset` | DEFAULT_NORMALIZATION（纯新增） | 低 |
| `PC_RPAsset.asset` | DEFAULT_NORMALIZATION（机械属 EFFECTIVE，经剥离面实证降级） | **低—中**（未逐 keyword A/B） |
| `URPGlobalSettings.asset` | **EFFECTIVE_CONFIGURATION_CHANGE** | **中**（运行时注册变更，未见故障） |

**未做任何还原。** 依任务书要求，`EFFECTIVE_CONFIGURATION_CHANGE` 必须保留风险并交负责人决定（见 §12 / §13 G-2）。

---

## 10. 1340 个历史证据保护（H 阶段）

`Evidence/PH-R2-R1-FIX/protection/HISTORY_RECHECK.json`

| 检查 | 结果 |
|---|---|
| 条目数 / 唯一路径 | 1340 / 1340（重复 0） |
| 物理可见文件 | **1340/1340**（无需回退 Git 对象库） |
| **逐文件 SHA256 独立重算一致** | **1340/1340** |
| 基线来源 | `pre_change_snapshot.json`（`generatedAt=2026-11-11T16:37:15`，构建开始前 5 分钟） |
| recheck 条目不在起点快照 | 0 |
| `preSha256` 与起点快照不一致 | 0 |

### 10.1 分区

| 区域 | 文件数 | 变化 |
|---|---|---|
| `Evidence/PH-R2` | 15 | 0 |
| `Evidence/PH-R2-R1` | 125 | 0 |
| `Evidence/PH-R2-FINAL-AUDIT` | 47 | 0 |
| `Evidence/Runs` | 1151 | 0 |
| `Evidence/INDEX.json` | 1 | 0 |
| `Evidence/PLAYER_RUN_MATRIX.csv` | 1 | 0 |
| **合计** | **1340** | **0** |

覆盖对象包含：PH-R1/PH-R2 原始证据、PH-R2-FINAL-AUDIT 审计证据、PH-R2-R1 原始证据与其 `recompute.json`、原始 Player Run、原始 `result.json`、历史 INDEX、失败原因记录。

### 10.2 稀疏检出说明

sparse-checkout 为启用状态，但 1340 份历史证据**全部在文件系统物理可见**（均为工作区未跟踪文件），故本次采用**物理字节**口径而非 Git 对象库口径，判据强度更高。

> **FA-9（结构性，信息级）**：1340 份历史证据中仅 **2 份**（`Evidence/INDEX.json`、`Evidence/PLAYER_RUN_MATRIX.csv`）被 Git 跟踪，其余 **1338 份未跟踪**。
> 因此"零变化"的基线是**同会话快照文件**而非 Git 树。该口径在本次审计中成立（快照生成于构建前、1340/1340 逐字节吻合），但**该历史证据树本身尚未纳入版本控制**，需在提交策略中一并处置（见 §12）。

---

## 11. 210 份 FIX 证据审计（I 阶段）

`Evidence/PH-R2-R1-FIX/INDEX.json`：`evidenceFileCount=210`，`evidenceFiles` 数组 210 条。

| 检查 | 结果 |
|---|---|
| INDEX 条目数 | 210（唯一 210，重复 0） |
| 磁盘文件数（除 `INDEX.json`） | 210 |
| INDEX − 磁盘 | 0 |
| 磁盘 − INDEX | 0 |
| **逐文件 SHA256 一致** | **210/210** |
| **逐文件大小一致** | **210/210** |

### 11.1 目录构成

| 目录 | 文件数 | 内容 |
|---|---|---|
| `selftest/` | 148 | 12 组正/负向 Run（positive / stale / timeout / wrongsha / wrongdllsha / timebase × 2 轮）+ `SELFTEST.json` + `console.log` |
| `runs/` | 36 | C-GATE / STAFF-FIELD / TIMEBASE 各 12 件 |
| `failed/` | 9 | 首版错误探针（`TIMEBASE-probe-data-error`） |
| `build/` | 5 | round1 patch + 两套 pre/postflight |
| `protection/` | 5 | TSV / manifest / recheck / 历史复核 / 起点快照 |
| `recompute/` | 5 | 4 个复算脚本 + `twin-timeline.json` |
| 根 | 2 | `SELFTEST_COVERAGE_MATRIX.json`、`timebase-probe.json` |
| **合计** | **210** | |

### 11.2 关键证据抽查

| 项目 | 位置 | 结论 |
|---|---|---|
| 10 项时间探针 | `timebase-probe.json` | 10/10 ok，参数与原始输出完整 |
| C-gate 原始数据 | `runs/C-GATE/damage-events.jsonl` | 3 段 × 21.45，HP 链连续（见 §11.3） |
| Staff.field 四段 | `runs/STAFF-FIELD/damage-events.jsonl` | 21.45 / 13.20×3 = 61.05（见 §11.3） |
| 31 项自检 | `selftest/SELFTEST.json` | 31/31 ok |
| 192 项保护清单 | `protection/PROTECTED_SHA256.tsv` | 192/192 |
| 三轮构建记录 | `build/` | round1 + 最终轮（第 2 轮缺，FA-2） |
| **失败探针原始目录** | `failed/TIMEBASE-probe-data-error/`（9 件，含 `FAILURE_NOTE.json`） | **完整保留，未被覆盖** |
| 复算数据 | `recompute/*.py` | 4 个脚本可执行 |

### 11.3 审计方独立复算（不采信批次内复算）

**C-gate**（`runs/C-GATE/damage-events.jsonl`，3 段）

| # | HP before | HP after | damage | 期望 33×0.65 |
|---|---|---|---|---|
| 1 | 140 | 118.55 | 21.45 | 21.45 ✅ |
| 2 | 118.55 | 97.10001 | 21.45 | 21.45 ✅ |
| 3 | 97.10001 | 75.65001 | 21.45 | 21.45 ✅ |

合计 **64.35**；`cooldownMeasured=7.108136`，两次 skillStart 间隔 `7.108139`；`blockedDuringCooldown=true`；三段时钟偏移**恒为 4.300357**（单钟记录一致性佐证）。

**Staff.field**（`runs/STAFF-FIELD/damage-events.jsonl`，4 段）

| # | HP before | HP after | damage | 期望（ratio × 33） |
|---|---|---|---|---|
| 1 | 140 | 118.55 | 21.45 | 0.65 × 33 = 21.45 ✅ |
| 2 | 118.55 | 105.35 | 13.20 | 0.40 × 33 = 13.20 ✅ |
| 3 | 105.35 | 92.15001 | 13.20 | 13.20 ✅ |
| 4 | 92.15001 | 78.95001 | 13.20 | 13.20 ✅ |

合计 **61.05**，四段逐段等于 `ratio × AP`，HP 链连续（`before[i] == after[i-1]`）。偏移恒为 4.323052/4.323053。

> **FA-3（低，悬空证据路径）**：覆盖矩阵 `R16` 行的 `evidencePath` 为 `Evidence/PH-R2-R1-FIX/runs/STAFF-FIELD/recompute.json`，该文件**不存在**；该行 `resolved` 数组亦自述 `note: "evidence path missing"`，但整行 `status` 仍为 `PASS`（因 `#23` 子项通过）。
> 复算数据实际位于 `runs/STAFF-FIELD/result.json#damageForensics`（含逐段 `expectedDamage`）与 `damage-events.jsonl`。审计方已据原始事件独立复算 61.05 通过（见上表），**结论不受影响**，但该证据指针需修正，否则第三方按图索骥会扑空。
> 注：`Evidence/PH-R2-R1/runs/TWIN-COUNTER/recompute.json` 确实存在，疑似 FIX 批次沿用了旧路径命名而未生成对应文件。

> **FA-7（低）**：`INDEX.json` 的 `evidenceFiles` 条目仅含 `path` / `size` / `sha256`，**无**任务书要求的"文件类型 / 对应测试 / 原始或派生属性"三个字段。这些分类信息存在于 `EVIDENCE_INDEX.md`（人类可读），未进入机器可校验的清单。属可增强项。

> **FA-5（低）**：`INDEX.json` 顶层 `buildSha256` 的值为 **EXE** SHA（`b70442f9…`），而 EXE 恒定不变、不能作身份主键。真正的身份主键在 `build.acceptanceDllSha256`。字段命名易导致误读。

---

## 12. 最终提交白名单（J 阶段）

**未执行 `git add`。以下仅为清单。**

### A. 验收工具（2 个，modified）

| 文件 |
|---|
| `Assets/CombatPrototype/Acceptance/PlayerAcceptanceHarness.cs` |
| `player_acceptance_driver.py` |

### B. FIX 正式交付文档（11 个，全部未跟踪）

| 文件 | 状态 |
|---|---|
| `REPORT.md` | 本批更新 |
| `ACCEPTANCE.md` | 本批更新（双钟表述） |
| `TESTING.md` | 本批更新 |
| `BUILD_IDENTITY.md` | 本批追加 §8 |
| `DAMAGE_MODEL.md` | 本批追加 §2.3 / §2.3.1 / §2.3.2 |
| `EVIDENCE_INDEX.md` | 本批追加 §6 |
| `SELFTEST_COVERAGE_MATRIX.md` | 新增 |
| `PH-R2-R1-FIX-REPORT.md` | 新增 |
| `PH-R2-R1-FIX-ACCEPTANCE.md` | 新增 |
| `PH-R2-R1-FIX-ADDENDUM.md` | 新增 |
| `PH-R2-R1-FINAL-AUDIT.md` | **历史审计报告，内容未变**（sha `7c9c06f5…`） |

> 整个 `DeliveryUxProgression03APlayerHarnessR2R1/` 目录在 Git 中尚未跟踪，故 11 个文件均需首次入库。

### C. FIX 正式证据（210 个 + INDEX.json = 211 个）

`Evidence/PH-R2-R1-FIX/**`（`selftest/` 148、`runs/` 36、`failed/` 9、`build/` 5、`protection/` 5、`recompute/` 5、根 2，加 `INDEX.json`）

> `*.log` 受 `.gitignore` 约束，入库需 `git add -f`（共 17 份日志类证据）。

### D. 必须保留的失败证据（不得删除、不得覆盖）

| 路径 |
|---|
| `Evidence/PH-R2-R1-FIX/failed/TIMEBASE-probe-data-error/FAILURE_NOTE.json` |
| `Evidence/PH-R2-R1-FIX/failed/TIMEBASE-probe-data-error/{result.json,timebase-probe.json,harness.log,player.log,run-manifest.json,entry-audit.jsonl,stdout.txt,stderr.txt}` |

### E. 不允许提交 / 需单独决策

| 项 | 处置 | 理由 |
|---|---|---|
| `ProjectSettings/ProjectSettings.asset` | **单独决策** | SERIALIZATION_ONLY + DEFAULT_NORMALIZATION，低风险；若排除则每次构建重现 dirty |
| `ProjectSettings/GraphicsSettings.asset` | **单独决策** | 纯新增默认字段，低风险 |
| `Assets/Settings/PC_RPAsset.asset` | **单独决策** | 机械属 EFFECTIVE_CONFIGURATION_CHANGE，经剥离面实证为等价；残余风险低—中 |
| `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset` | **单独决策（风险最高）** | 运行时资源注册由空变 16 项，属真实配置变更，未见故障 |
| `Assets/Resources.meta` | **单独决策（G-3）** | 未跟踪的合法 Unity 文件夹 meta（guid `5c997356…`）；`Assets/Resources/` 已跟踪 199 个文件但其父级 meta 缺失，长期存在 GUID 漂移隐患 |
| `Library/` | **排除** | `.gitignore:17` 已忽略 |
| `Builds/` | **排除** | `.gitignore:21` 已忽略 |
| `__pycache__` | **不存在** | 全仓库无命中 |
| 临时日志（`/tmp/*.log` 等） | **排除** | 仓库外 |
| `Evidence/PH-R2`、`Evidence/PH-R2-R1`、`Evidence/PH-R2-FINAL-AUDIT`、`Evidence/Runs`（1338 份） | **需负责人决定是否同批入库** | 全部未跟踪；FIX 证据引用这些历史产物，若不入库则引用悬空（FA-9） |
| `ProjectDocs/…/DeliveryUxProgression03APlayerHarnessR2/`（4 份） | **需负责人决定** | 上一批次文档目录，同样未跟踪 |

**禁止 `git add .`。**

---

## 13. 未关闭风险

| 编号 | 风险 | 等级 | 状态 |
|---|---|---|---|
| **G-1** | 19 项完整矩阵未在 FIX DLL（`db258d6e…`）下重跑；A–F 仅覆盖 3 个定向 Run | 中 | **未关闭**（FIX 仅改动 Harness 判定路径，但回归面确实小于完整矩阵） |
| **G-2** | 四个 Unity 设置文件 modified，其中 `URPGlobalSettings.asset` 为 EFFECTIVE_CONFIGURATION_CHANGE | 中 | **未关闭**，待负责人决定提交或排除 |
| **G-3** | `Assets/Resources.meta` 未跟踪 | 中低 | **未关闭** |
| **G-4** | R14/R15 历史证据产生于 **PH-R2 DLL**，未在 FIX DLL 下重新取证 | 中低 | **未关闭**（覆盖矩阵已如实标注 `limitation`） |
| **FA-1** | 任务书 §2「最终 DLL」引用 FIX 前的 `b3ce427c…` / `00373fe7…` | 中 | 已记录，本报告以实测 `db258d6e…` / `f8b44e1e…` 为准 |
| **FA-2** | 第 2 轮构建无独立 preflight/postflight 留痕，仅 INDEX 汇总声明 | 中低 | 已由 `R1post == R3pre` 间接闭合；留痕完整性仍缺 |
| **FA-3** | R16 `evidencePath` 指向不存在的 `recompute.json`，该行仍判 PASS | 低 | 数据在 `result.json#damageForensics`，审计方已独立复算 |
| **FA-4** | §2.3.2 实用常数 4.358566，§2.3.1 公示 4.358567，致 7.803075/7.803076 差 1e-6 | 低 | 记录 |
| **FA-5** | `INDEX.json#buildSha256` 实为 EXE SHA，非构建身份主键 | 低 | 记录 |
| **FA-6** | `userEditPresent` 字段名为"与 HEAD 不同"，易误读为人为编辑 | 低 | 记录 |
| **FA-7** | `INDEX.evidenceFiles` 缺"类型/对应测试/原始或派生"字段 | 低 | 记录 |
| **FA-8** | `stale` 用例 FAIL 由陈旧拒绝 + 短超时共同造成 | 信息 | 拒绝理由已显式记录 |
| **FA-9** | 1340 历史证据中 1338 份未纳入 Git，保护基线为同会话快照 | 信息 | 记录，影响提交策略 |
| **O-4** | hardcap 存在 4.5s / 6.0s 两个值，文档未并列声明 | 信息 | 记录 |

**未删除任何上述限制。未将 PH-R2 / PH-R2-R1 DLL 下的结果表述为 FIX DLL 下的完整矩阵回归。**

---

## 14. 最终结论

### 14.1 已独立验证为真（PASS）

1. HEAD / tree / 分支与任务书一致；暂存区空；无删除、无重命名。
2. 时间判据仅用 `Time.unscaledTime`，判定函数签名不含 `activeTime`，跨钟减法在类型层不可写；唯一的跨钟减法为声明式取证字段。
3. 10/10 in-Player 探针通过；`dU=0.409792` / `dT=0`；旧式公式反证值 `4.408582 > 1.2` 成立。
4. 双钟文档分层清晰，偏移由两条独立事件流互证（4.358567 / 4.358566），并声明不可跨 Run 复用；双刃反击因果链 7.187 → 7.803（Δ 0.616 ≤ 0.85）→ 17.301 完整可复算。
5. 23 需求 → 24 行，`{DIRECT:16 pass 16, PLAYER:6, STATIC:2, NOT_COVERED:0}`，无混淆、无 NOT_COVERED 误判。
6. 31/31 自检逐项回溯原始产物成立；负向用例确被拒绝（含 `exit=0` 仍判 FAIL 的强校验）。
7. 192 个唯一保护文件：192/192 当前 SHA、192/192 HEAD blob OID、192/192 worktree blob OID 全部一致；219→190 去重独立复算无损。
8. 三轮构建链路闭合：`R1pre == HEAD`、`R1pre→R1post` 变化 4、`R1post == R3pre`、`R3pre == R3post == 工作区`；round1 patch 与当前 diff 逐行一致；**全程无 checkout/restore**。
9. 1340/1340 历史证据逐字节一致；210/210 FIX 证据 SHA 与大小一致；失败探针 9 件完整保留。
10. 产品逻辑源码修改 **0**；原始审计报告 `PH-R2-R1-FINAL-AUDIT.md` **未被覆盖**。
11. 未提交、未推送、未合并 main、未启动 03B。

### 14.2 未满足 / 需决定

- **G-2**：两个设置文件属 EFFECTIVE_CONFIGURATION_CHANGE（`URPGlobalSettings` 中风险、`PC_RPAsset` 低—中），必须由负责人决定入库或排除，审计方未还原。
- **FA-2**：第 2 轮构建留痕缺失（间接证明成立，逐轮取证不完整）。
- **FA-3**：R16 证据指针悬空（数据可用，指针需修正）。
- **G-1 / G-3 / G-4**：矩阵回归面、`Resources.meta`、PH-R2 DLL 历史证据，均维持原状未关闭。

### 14.3 判定

> ## **CONDITIONAL_PASS**
>
> 全部功能性主张（时间基准修复、双钟报告、覆盖矩阵、自检、保护清单、历史证据、证据完整性、产物身份）均经独立复算成立，未发现数据造假、未发现跨钟残留、未发现构建后还原或用户文件被覆盖。
>
> 但存在**四项需负责人裁决或补记的条件**：G-2 设置文件提交决策（含一项真实的运行时注册变更）、FA-2 第 2 轮构建留痕缺口、FA-3 悬空证据指针、G-3 `Resources.meta` 归属。在这些条件未确认前，不予 PASS。

---

## 附：审计方法与可复现性

- 所有 SHA256 均由审计方独立重算，未采信任何 `INDEX` / `SELFTEST` / `HISTORY_RECHECK` 的汇总结论；上述文件仅作为“待验证声明”使用。
- Git 侧双口径：`git rev-parse HEAD:<path>`（索引）与 `git hash-object`（worktree）。
- 历史证据采用物理字节口径（1340 份全部可见），并对基线做溯源校验（`pre_change_snapshot.json`，生成于 16:37:15，早于构建 16:42）。
- 全程只读：未修改产品源码、验收工具、设置文件、原始证据；未新增 Player Run；未执行 `git add/commit/push/merge/reset/checkout/restore/clean`。
