# PH-R2-R1-FINAL-AUDIT — 最终独立审计报告

| 项 | 值 |
|---|---|
| 审计对象 | PH-R2-R1 实施批次（含 PH-R1 / PH-R2 历史） |
| 审计方式 | **只读**（未修改源码、工具、证据、设置；未 add/commit/push；未 reset/checkout/restore/clean） |
| 审计时间 | 2026-11-11 16:04–16:20 (GMT+8) |
| 审计者 | 独立审计（本会话），不采信 PH-R2-R1 自述结论，全部数字从原始工件重算 |
| **最终结论** | **CONDITIONAL_PASS** |

---

## 1. 审计对象与完整 SHA

### 1.1 仓库基线

| 项 | 值 |
|---|---|
| HEAD | `e9f9a142e80f0b4013338f70e5a5b6d1c3776826` |
| HEAD tree | `20945471121d319c94f3b4f9ad4a5c3152bd899e` |
| 分支 | `verify/ux-progression-03a-player-harness-r2-r1` |
| 与 PH-R1 基线一致 | 是（未产生任何新 commit） |

### 1.2 构建产物（独立重算，非引用 manifest）

| 产物 | SHA256 | 与 manifest |
|---|---|---|
| Acceptance EXE | `b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436` | MATCH |
| Acceptance DLL | `b3ce427cdc3970b6412972f4c9de89442dd68f5debf572bcfebf8ad5e54a1e91` | MATCH |
| NoDefine EXE | `b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436` | MATCH |
| NoDefine DLL | `00373fe72161ba7e7c761983ef5865097584837c594a251f0f60a8f00e08710e` | MATCH |
| buildId（重算） | `phr2r1-318c660afbcaf218d04c469b` | MATCH |
| `Evidence/PH-R2-R1/build/build-manifest.json` | 与 `Builds/build-manifest.json` 逐字节相同 | 是 |

> 两个 EXE 同 SHA（Launcher 桩恒定）已被独立确认；**若以 EXE 作身份依据，新旧代码不可区分**。
> 本审计沿用 DLL 作身份主键。

### 1.3 交付文档（6 份）

| 文档 | SHA256 |
|---|---|
| REPORT.md | `f0fe681fc51bbc79413c0bbe8d17b48dbf469ede96b9bf09d61c6e6096658063` |
| ACCEPTANCE.md | `db6193ba94c0f8266ee302186ac0d5e89b52ebf7135526aad70d1892c64facd1` |
| TESTING.md | `85ad6e3c5cbb83cd78369c74662199a227fe01d3f772012a86ebf15d1ea46c2f` |
| BUILD_IDENTITY.md | `486d6ef386a98fe66966625ff471ff0f587afd03e4ace7d21b8b3f8800ae8c79` |
| DAMAGE_MODEL.md | `9fa9e5e1f6cd9e67af8c383db20f2558c20d2be34e403cc9f3db879df65520a9` |
| EVIDENCE_INDEX.md | `5943746e89a99020faf858a2e1e551f83a0490f5328561b093c2c2f2bbbf95fb` |

---

## 2. Git 工作区状态（A 阶段）

| 检查 | 期望 | 实测 | 判定 |
|---|---|---|---|
| HEAD 与基线一致 | `e9f9a142e…` | 一致 | ✓ |
| 分支正确 | `verify/…-r2-r1` | 一致 | ✓ |
| staged 为空 | 空 | `git diff --cached --stat` 无输出 | ✓ |
| tracked 修改仅 2 个验收工具文件 | 2 | 2 | ✓ |
| `git diff --check` | 无空白错误 | exit 0 | ✓ |
| 无删除 / 重命名 | 无 | `--diff-filter=DR` 空 | ✓ |
| 产品源码 / Prefab / 场景 / ProjectSettings / Packages 零修改 | 0 | `git diff HEAD -- ProjectSettings Packages` 空；其余路径无变更 | ✓ |
| 未跟踪文件全部枚举 | — | 91 项 | ✓ |

### 2.1 变更清单

```
M  Assets/CombatPrototype/Acceptance/PlayerAcceptanceHarness.cs   +861 −84
M  player_acceptance_driver.py                                   +786 −47
合计 +1647 −131
```

### 2.2 未跟踪项（91）

| 路径 | 数量 | 说明 |
|---|---|---|
| `Evidence/Runs/*` | 85 | PH-R1/PH-R2 的补充运行目录（历史证据，未提交） |
| `Evidence/PH-R2-R1/` | 1 | 本批证据（125 文件） |
| `Evidence/PH-R2/` | 1 | PH-R2 批次证据（历史） |
| `Evidence/PH-R2-FINAL-AUDIT/` | 1 | PH-R2-FINAL 审计产物（历史） |
| `ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2/` | 1 | PH-R2 交付（历史） |
| `ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/` | 1 | 本批交付（6 文档 + 本报告） |
| `Assets/Resources.meta` | 1 | Unity 生成的文件夹 meta，**13:53 前即存在**，非本批产生 |

---

## 3. 两个工具文件 Diff 的范围一致性

### 3.1 `PlayerAcceptanceHarness.cs`（26 个 hunk，+861/−84）

文件首行 `#if UX_ACCEPTANCE`、末行 `#endif` 完整，全部改动位于验收工具内部。按功能归类：

| 区段 | 内容 | 是否属于 R1 范围 |
|---|---|---|
| 字段区 | `loadedAssemblyPath/loadedAssemblySha256/loadedAssemblyName/expectedDllSha/identityVerified/identityNote/expectedHitRatios/incompleteReason/secondCounterContactSeen` | R1-01/02/03 ✓ |
| `ParseArgs` | `--build-id / --expected-exe-sha / --expected-dll-sha` | R1-01 ✓ |
| 新增 `ResolveAssemblyIdentity()` | 自算 DLL SHA，失败即 `identityVerified=false` | R1-01 ✓ |
| `RecordDamageHit` | 逐段 `expectedHitRatios[hitIndex] * AP`；`damageWindowClosed` 守卫 | R1-03 ✓ |
| `ComputeExpectedModel` | `Staff\|1` 非均匀 4 段；`expectedTotal=(0.65+0.40×3)×…` | R1-03 ✓ |
| `FinalizeDamageForensics` | 非均匀分支逐段核对（含 overkill 归零、`Convert.ToSingle`） | R1-03 ✓ |
| `T3VerdictOk` | 严格 6 项（含 `dodgeRollObserved`），缺第二次 contact → `incompleteReason` | R1-02 ✓ |
| `Finish` / `WriteResult` | `pass &&= identityVerified && !incomplete`；`Application.Quit(2)` 表 INCOMPLETE；result.json 增身份与 ratio 字段 | R1-01/02/04 ✓ |

无任何改动落在产品战斗逻辑、数值表、存档、Prefab、场景。

### 3.2 `player_acceptance_driver.py`（+786/−47）

`compute_build_id` / `load_build_manifest` / `verify_manifest` / `build_identity_snapshot` /
`generate_build_manifest` / `verify_run_identity` / `run_one`（前后 SHA + `run-manifest.json`）/
`selftest`（ID-1..ID-5）/ `run_r1`（A–E）/ `recompute_r1`。全部属 R1-01/04/05，无产品侧副作用。

---

## 4. DLL 身份链（B 阶段）

### 4.1 闭合关系（3 个定向 Run + 1 个自检正向 Run）

| Run | pid | loadedAssemblyPath 属 Acceptance 目录 | loadedAssemblySha256 | expected | dllBefore | dllAfter | identityVerified | exit | timedOut |
|---|---|---|---|---|---|---|---|---|---|
| C-GATE | 10600 | 是 | `b3ce427c…1e91` | 同 | 同 | 同 | true | 0 | false |
| TWIN-COUNTER | 5256 | 是 | `b3ce427c…1e91` | 同 | 同 | 同 | true | 0 | false |
| STAFF-FIELD | 31932 | 是 | `b3ce427c…1e91` | 同 | 同 | 同 | true | 0 | false |
| SELFTEST-positive | — | 是 | `b3ce427c…1e91` | 同 | 同 | 同 | true | 0 | false |

四元等式 `loadedAssemblySha256 == expectedAssemblySha256 == dllSha256Before == dllSha256After`
在 4/4 运行成立（1e0 精度，逐字符）。`run-manifest.resultJsonSha256` 与 `result.json` 实际哈希 4/4 一致。

### 4.2 "Player 自己算" 的独立证明

`selftest/SELFTEST-wrongdllsha-153637/`（真实 Player 启动，非 mock）：

| 字段 | 值 |
|---|---|
| 传入期望 | `0000…0000`（64 个 0） |
| Player 实算 | `b3ce427cdc3970b6412972f4c9de89442dd68f5debf572bcfebf8ad5e54a1e91` |
| `identityVerified` | **false** |
| `identityReasons` | `["Player identityVerified is not true","Player expectedAssemblySha256 mismatch"]` |
| exitCode / finalStatus | `1` / **FAIL** |

若为"命令行回写"，实算值会是全零且 verified=true。实测相反 → 自算成立；错误时退出非 0 成立。
Driver 侧独立拒绝由 ID-3（运行前后 DLL 变化）、ID-4（manifest 与实际不符）与
`SELFTEST-wrongsha`（buildSha 不符、exit=0 仍判 FAIL）共同覆盖。

---

## 5. 双刃反击因果链（C 阶段，最高优先级）

### 5.1 疑点

报告表格并列了 `hitTime=3.444509`（第 1 次 contact）与 `evadeSeenAt=7.187345`，
**表面呈现"contact 早于 evade"**，因果倒置。

### 5.2 根因：同一 result.json 内存在两套时钟

| 字段 | 时钟来源 | 代码位置 |
|---|---|---|
| `keyEvents[].time`、`skillStarts[]`、`skillCompletes[]`、`casts[].at`、`t3.evadeSeenAt`、日志前缀 | `Time.unscaledTime` | `Log()` L195、L205、L210、L475 等 |
| `damage-events.jsonl.hitTime`、`target-events.jsonl.activeTime`、`observations[].time` | `Time.timeAsDouble` | `CombatHealth.cs:26` |

### 5.3 转换公式（由两个**互不相同**的事件流各自推导，非拟合）

```
offset = Time.unscaledTime − Time.time          // 本次运行
```

| 事件 | Time.time | unscaledTime | offset |
|---|---|---|---|
| actual-evaded-attack | 2.828779 | 7.187345 | **4.358566** |
| skill start | 3.161727 | 7.520294 | **4.358567** |

两者相差 `1.0e-6 s`（浮点精度），**独立同源验证通过**。
第 3 对（contact 3.444509 vs 日志 7.803，日志仅 3 位小数）反推 4.358491，与上一致（舍入误差内）。

### 5.4 统一到 `unscaledTime` 后的完整因果链

| 序 | 事件 | 时刻 | 与前一步间隔 | 证据 |
|---|---|---|---|---|
| 1 | 敌人攻击电报 → 翻滚按下 (Space) | 7.088 | — | `keyEvents` frame 703 |
| 2 | 翻滚抬起，`IsRolling=True IsInvulnerable=True` | 7.152 | +0.064 | `harness.log` + frame 717 |
| 3 | **actual-evaded-attack（无敌窗拒绝）** | **7.187** | +0.035 | `harness.log` OBS；`t3.evadeSeenAt` |
| 4 | 反击按下 (F) | 7.515 | +0.328 | `casts[2]` frame 815 |
| 5 | 技能 start | 7.520 | +0.005 | `skillStarts[0]` |
| 6 | **第 1 次 contact，empowered=True，59.40** | **7.803** | **+0.616（≤0.85 窗）** | `observations.contact` + `harness.log` FORENSIC |
| 7 | 技能 complete | 8.047 | +0.244 | `skillCompletes[0]` |
| 8 | 第 2 次反击按下 (F) | 17.015 | +9.500（= cd 9.5） | `casts[3]` frame 3647 |
| 9 | **第 2 次 contact，empowered=False，21.45** | **17.301** | +0.286 | `harness.log` OBS counter2 |

**第一段反击发生在 evade 之后 0.616s，处于产品 `ConsumeEvade` 的 0.85s 强化窗内**
（`NewWeaponCombat.cs:20`：`Time.time-evadeAt>.85f` 则拒绝），且该 `empowered` 由产品在 contact 时给出，
非 Harness 推断（`NewWeaponCombat.cs:44`：`bool empowered=counter&&owner.ConsumeEvade();`）。

### 5.5 第三重（无时钟）印证：帧号

| 事实 | 帧号 |
|---|---|
| Space down / up（翻滚） | 703 / 717 |
| F down / up（第 1 次反击） | 815 / 904 |
| **hit#1** | **903** ∈ [815, 904] ✓ |
| F down / up（第 2 次反击） | 3647 / 3733 |
| **hit#2** | **3732** ∈ [3647, 3733] ✓ |
| 翻滚帧 717 < hit#1 帧 903 | 翻滚严格在命中之前 ✓ |

帧号单调、与任何时钟无关，独立确认"命中属于按下窗口之内、且在翻滚之后"。

### 5.6 结论

- 因果链**成立且可证**：攻击→翻滚→无敌拒绝→强化→第 1 次 contact(1.8×)→冷却 9.500s→第 2 次 contact(0.65×)→未再强化。
- 第二次反击是**真实 contact**（帧 3732 + `secondCounterContactSeen=true`），非"无 contact 记为消费成功"。
- **但报告表格未声明基准差异，构成呈现缺陷（F-1）**，必须修正后才能作为对外证据。

---

## 6. Staff.field 四段伤害（D 阶段）

| # | hitId | HP before → after | actual | 期望 33×ratio | result.json 一致 | 判定 |
|---|---|---|---|---|---|---|
| 1 | 1 | 140.00 → 118.55 | 21.45 | 21.45 (0.65) | 是 | ✓ |
| 2 | 2 | 118.55 → 105.35 | 13.20 | 13.20 (0.40) | 是 | ✓ |
| 3 | 3 | 105.35 → 92.15 | 13.20 | 13.20 (0.40) | 是 | ✓ |
| 4 | 4 | 92.15 → 78.95 | 13.20 | 13.20 (0.40) | 是 | ✓ |
| 总 | — | 140 → 78.95 | **61.05** | **61.05** | 是 | ✓ |

10 项独立检查：

| 检查 | 结果 |
|---|---|
| hitId 唯一且 1..N | ✓ [1,2,3,4] |
| 事件顺序（hitTime 严格递增） | ✓ 2.1399 < 2.3920 < 2.9959 < 3.5973 |
| targetId 一致 | ✓ `c1:elite` |
| HP 前后连续（自 initialHP=140 起） | ✓ 无断点（容差 1e-4） |
| actualDamage == HP 差值 | ✓ 4/4（容差 0.05） |
| expectedDamage 与阶段倍率一致 | ✓ 4/4，**逐段**而非总数 |
| 无重复事件 | ✓ (hitId,time,damage) 唯一 |
| result.json 与 JSONL 一致 | ✓ 4/4 逐字段（1e-6） |
| `target-events.jsonl` 与 `damage-events.jsonl` 一致 | ✓ 4/4（applied/before） |
| 总伤害正确 | ✓ 61.05 = 140−78.95（0.00001 级） |

**未使用"总数 61.05 通过即算过"的宽松判定**：第 2–4 段若按 0.65 记期望（21.45）会立刻失败，
本审计亦独立验证了该反例。

---

## 7. C-gate 独立复算（E 阶段）

| 项 | 期望 | 实测 | 判定 |
|---|---|---|---|
| HP 序列 | 140 → 118.55 → 97.10 → 75.65 | 完全一致 | ✓ |
| 每段伤害 | 33 × 0.65 = 21.45 | 21.45 / 21.45 / 21.45 | ✓ |
| 总伤 | 64.35 | 64.35（= 140−75.65） | ✓ |
| 三次真实命中 | 3 条 damage-events | 3 条（+3 条 target-events） | ✓ |
| 冷却实测 | ≈7.1s | **7.10633s** | ✓（容差 −0.6/+1.5） |
| 冷却期重按被拒 | `blockedDuringCooldown=true` 且 starts 不增 | cast@6.97 被拦，`skillStarts` 仍为 1 | ✓ |
| 冷却后允许再施放 | starts ≥ 2 | 6.062722 → 13.16905 | ✓ |
| DLL 身份完整 | 四元等式 | 成立 | ✓ |
| 退出码记录 | 0 / 非超时 | 0 / false | ✓ |

---

## 8. Harness 自检审计（F 阶段）

`selftest/SELFTEST.json`：`allPassed=true`，23 项。逐项均有原始证据（Run 目录或构建产物）。

| # | 自检项 | 原始证据 | 判定 |
|---|---|---|---|
| 1 | marker 存在 | Acceptance DLL（UTF-16LE 命中 2 次） | ✓ |
| 2 | NoDefine 无 marker | NoDefine DLL（0 次） | ✓ |
| 3 | EXE SHA 与 manifest 一致 | manifest + 实算 | ✓ |
| 4 | C-gate 正向 Run PASS（含身份/新鲜度） | `SELFTEST-positive-*/` | ✓ |
| 5 | KeyDown 记录 | `keyEvents` | ✓ |
| 6 | KeyUp 记录 | `keyEvents` | ✓ |
| 7 | skill start | `skillStarts` | ✓ |
| 8 | skill complete | `skillCompletes` | ✓ |
| 9 | 入口经公共 API 授权 | `entryAuthorized=true` | ✓ |
| 10 | C-gate 真实伤害 | `damage-events.jsonl` + `target.prepared` | ✓ |
| 11 | damage-events 落盘 | 文件存在 | ✓ |
| 12 | target-events 落盘 | 文件存在 | ✓ |
| 13 | 陈旧 result 被拒 | `SELFTEST-stale-*/`（预置 1h 前 result） | ✓ |
| 14 | 错误 buildSha 被拒 | `SELFTEST-wrongsha-*/`（exit=0 仍 FAIL） | ✓ |
| 15 | 超时判 FAIL | `SELFTEST-timeout-*/`（timedOut=true） | ✓ |
| 16 | 超时保留日志 | stdout/stderr/player.log 均在 | ✓ |
| 17 | Run 根隔离 | 5 个独立目录 | ✓ |
| 18 | AppData 未被写 | default+legacy 指纹一致 | ✓ |
| 19 | 错误 DLL SHA 被拒（真实 Player） | `SELFTEST-wrongdllsha-*/` | ✓ |
| 20 | Player 内部 SHA 不一致被拒 | 篡改 `loadedAssemblySha256` → 非空 | ✓ |
| 21 | 运行前后 DLL 变化被拒 | 篡改 `dllShaAfter` → 非空 | ✓ |
| 22 | manifest 与实际 DLL 不符被拒 | 篡改 `acceptanceDllSha256` → 非空 | ✓ |
| 23 | run-manifest 退出码/身份/状态 | `run-manifest.json` 5 字段核对 | ✓ |

### 8.1 与任务书 §8 清单的对账（重要）

任务书列出的 23 个条目与实际 23 项自检**并非一一对应**。差异项：

| 任务书条目 | 实际情况 | 判定 |
|---|---|---|
| 9 时间源统一 | **不存在此项自检**；且实测**不成立**（见 §5.2、F-1、F-1b） | ✗ |
| 10 CharacterController 位置同步 | 非自检项；属 PH-R2 的实现修复（`cc.enabled` 重同步），效果由 §10「真实目标/真实命中」间接覆盖 | 间接 |
| 13 强化消费 | 非自检项；由 TWIN-COUNTER 运行覆盖（`T3VerdictOk`） | 覆盖于 B/C 阶段 |
| 14 牵引完成 | PH-R2 #14 场景，**本批未运行** | 不在本批 |
| 15 峰值位移 | 同上 | 不在本批 |
| 16 原始数据聚合 | 非自检项；由 `recompute` 模式覆盖（40 项） | 覆盖于 G 阶段 |
| 17 Define 清理 | 非自检项；由 A 阶段 `defineLeakCount=0` 与 NoDefine marker 扫描覆盖 | 覆盖于 A/B 阶段 |

因此"23/23 通过"只能表述为"**本批定义的 23 项自检全部通过**"，
不能读作"任务书 §8 的 23 条断言全部成立"。

---

## 9. 40 项独立复算（G 阶段）

不采信 `RECOMPUTE.json` 的 `ok` 字段，按原始 JSONL/result.json 重新实现谓词：

| Run | 我的复算 | RECOMPUTE.json 声称 | 一致性 |
|---|---|---|---|
| C-GATE | 11/11 | 11/11 | 一致 |
| STAFF-FIELD | 11/11 | 11/11 | 一致 |
| TWIN-COUNTER | 18/18 | 18/18 | 一致 |
| **合计** | **40/40** | 40/40 | 一致 |

另独立重算的非 40 项内事实：4 个产物 SHA、buildId、3 次身份四元等式、
`resultJsonSha256` 4/4、190 保护文件、311 历史证据 — 全部一致。
因此"40/40 有可复现输入"成立。

---

## 10. 190 个保护文件（H 阶段）

| 项 | 值 |
|---|---|
| manifest 行数 | 219 |
| 唯一路径 | 190 |
| 重复行 | 29 个路径重复（共 58 行 → 29 组重复） |
| MATCH | **190/190** |
| CHANGED | 0 |
| 缺失 | 0 |
| 越界路径 | 0（全部在仓库内） |

逐项比对"期望 SHA（13:53 基线）"与"当前实际 SHA"，并额外以 `git hash-object`
比对 HEAD blob OID，双判一致。

---

## 11. 311 份历史证据（H 阶段）

| 项 | 值 |
|---|---|
| 快照条目 | 311（14:56:19 采集） |
| 一致 | **311/311** |
| 变更 / 缺失 | 0 / 0 |

分布：`Evidence/Runs` 247、`Evidence/PH-R2-FINAL-AUDIT` 47、`Evidence/PH-R2` 15、
`Evidence/INDEX.json` 1、`Evidence/PLAYER_RUN_MATRIX.csv` 1。

含 PH-R1 的原始 `INDEX.json`、`PLAYER_RUN_MATRIX.csv`、`R01..R19` 运行目录与
PH-R2 的失败历史，均未被覆盖或重分类。

---

## 12. Unity 设置文件还原审计（I 阶段）

### 12.1 被构建改写的 4 个文件

| 文件 | 是否在 190 保护清单 | 13:53 逐文件 SHA 快照 | 当前 vs HEAD |
|---|---|---|---|
| `ProjectSettings/ProjectSettings.asset` | 是 | 有（`B_protected_files.json`，SHA 与 HEAD 一致） | 干净 |
| `ProjectSettings/GraphicsSettings.asset` | 是 | 有（同上） | 干净 |
| `Assets/Settings/PC_RPAsset.asset` | **否** | **无** | 干净 |
| `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset` | **否** | **无** | 干净 |

### 12.2 是否存在覆盖用户修改

| 证据 | 内容 | 等级 |
|---|---|---|
| `Evidence/PH-R2-FINAL-AUDIT/A06_diff_name_status.txt`（13:53，构建前） | `git diff HEAD` 仅 2 个工具文件 → 4 个设置文件当时**处于 HEAD 状态，无用户未提交修改** | B（间接、时点明确） |
| `B_protected_files.json`（13:53） | 其中 2 个文件的逐文件 SHA 与 HEAD 及当前完全一致 | A（逐文件 SHA） |
| 当前 `git status`（16:05） | 4 个文件对 HEAD 干净 | A |
| 构建日志 | 记录构建成功，未记录设置内容 | — |

**结论：无用户修改被覆盖。** 但除 2 个文件外，**没有构建前的逐文件 SHA 快照**，
故对 `PC_RPAsset.asset` 与 `URPGlobalSettings.asset` 只能给出 B 级证据，
不能声称"已用 SHA 逐位证明未被覆盖"。本审计未执行任何 checkout/restore（按任务书要求）。

---

## 13. 124 份证据完整性（J 阶段）

| 检查 | 结果 |
|---|---|
| 磁盘文件数 | 125（含 `INDEX.json` 自身） |
| `INDEX.json` 列出的文件 | 124（已声明排除自身，避免自引用） |
| 列出但缺失 | 0 |
| 磁盘上有、清单未列 | 仅 `INDEX.json`（符合约定） |
| SHA / 大小漂移 | 0 |
| 空文件 | 16：8 个 `stderr.txt`（无 stderr）+ 8 个 `ForestRuins.entry.lock`（锁文件）；均为预期 |
| 内容重复 | 1 组：8 份 `stdout.txt` 完全相同（Player 同一启动横幅）；无异常 |
| 4 个负向运行证据完整 | ✓ stale / timeout / wrongsha / wrongdllsha 均含 run-manifest、player.log、harness.log、stdout、stderr |
| 3 个定向 Run 完整 | ✓ result / run-manifest / damage-events / target-events / player.log / harness.log / stdout / stderr / recompute |
| 原始与派生区分 | 原始 106 / 派生 18（`INDEX.json`、`RECOMPUTE.json`、3×`recompute.json`、3×build、3×protection、4×GIT_*） |
| 派生可追溯 | ✓ `recompute.sourceArtifacts` 3 文件哈希全对；`run-manifest.resultJsonSha256` 3/3 对；`INDEX.recompute.sha256` 对 |

---

## 14. 最终提交白名单（K 阶段）

> 只生成清单，**未执行 `git add`**。

### A. 验收工具修改（2）

```
Assets/CombatPrototype/Acceptance/PlayerAcceptanceHarness.cs
player_acceptance_driver.py
```

### B. 交付文档（7）

```
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/REPORT.md
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/ACCEPTANCE.md
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/TESTING.md
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/BUILD_IDENTITY.md
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/DAMAGE_MODEL.md
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/EVIDENCE_INDEX.md
ProjectDocs/WanxiangGuitu/DeliveryUxProgression03APlayerHarnessR2R1/PH-R2-R1-FINAL-AUDIT.md   ← 本报告
```

### C. 正式证据（125 = 124 + INDEX.json）

```
Evidence/PH-R2-R1/**            （全部）
```

**注意**：其中 **17 个 `*.log` 文件被仓库 `.gitignore` 规则 `*.log` 忽略**
（6× player.log、6× harness.log、console.log 等），常规 `git add` 会被静默跳过。
若要完整归档日志，需 `git add -f` 或为 `Evidence/**/runs/**/*.log` 增加例外规则——
**这是负责人的决策项，本审计不代为执行**。

### D. 必须保留的失败历史（不得删除、不得覆盖）

| 路径 | 性质 |
|---|---|
| `Evidence/PH-R2-R1/selftest/SELFTEST-stale-153637/` | 负向：陈旧结果 |
| `Evidence/PH-R2-R1/selftest/SELFTEST-timeout-153637/` | 负向：超时 |
| `Evidence/PH-R2-R1/selftest/SELFTEST-wrongsha-153637/` | 负向：buildSha 不符 |
| `Evidence/PH-R2-R1/selftest/SELFTEST-wrongdllsha-153637/` | 负向：DLL SHA 不符 |
| `Evidence/Runs/*`（85 个未跟踪目录） | PH-R1/PH-R2 历史运行（含失败） |
| `Evidence/PH-R2/`、`Evidence/PH-R2-FINAL-AUDIT/` | 前序批次证据与审计产物 |

### E. 不允许提交

| 路径 | 原因 |
|---|---|
| `Builds/**` | 构建产物，已被 `.gitignore` 忽略（可复核，不入库） |
| `Library/**` | Unity 缓存，已忽略 |
| `__pycache__/**` | Python 缓存；当前**不存在**，若出现必须排除 |
| `Assets/Resources.meta` | Unity 生成；未被忽略，需负责人决定"纳入"或"删除"（本审计不处置） |
| `*.log`（17 个） | 见 C 的注意项，默认不随常规提交 |
| `Evidence/PH-R2-R1/**/*.tmp`、`*.bak` 之外的临时物 | 无（已核查） |

---

## 15. 未关闭风险

| # | 风险 | 等级 | 事实 | 建议 |
|---|---|---|---|---|
| **F-1** | 报告时间基准混用，造成"第 1 次 contact 早于 evade"的表面倒置 | **中** | `DAMAGE_MODEL.md` §2.3 与 `ACCEPTANCE.md` §5 把 `hitTime`（`Time.time`）与 `evadeSeenAt`（`unscaledTime`）并列，未声明 4.3586s 偏移 | 报告必须补"统一到 unscaledTime"的换算表（本报告 §5.4 已给出），或直接改用 `unscaledTime` 记账 |
| **F-1b** | `closeDamageWindow` 与 `cooldownAllow` 的"1.2s 稳定期"判据时钟混用，**恒为真** | **中低** | `PlayerAcceptanceHarness.cs:502`、`:542`：`Time.unscaledTime − lastDamageAt`，`lastDamageAt` 来自 `activeTime`（`Time.time`） | 改为同基准（都用 `activeTime` 或都用 `unscaledTime`）。本批实际由 4.5s / 6s 上限兜底（末次命中 7.922s，finalize 15.229s），**未造成漏计**；若未来技能脉冲跨度 > 上限会静默漏计 |
| **F-2** | 190 保护清单未覆盖 2 个会被 Unity 构建改写的文件 | **中低** | `Assets/Settings/PC_RPAsset.asset`、`.../UniversalRenderPipelineGlobalSettings.asset` 不在 219 行清单内；本批被构建改写后已还原 | 扩充保护清单；对设置文件建立构建前逐文件 SHA 快照 |
| **F-3** | "4 次真实 Player Run" 口径与实际不符 | 低 | 实际 8 次启动：3 定向 + 1 自检正向 = 4 次 PASS；另有 4 次负向（stale/timeout/wrongsha/wrongdllsha） | 文档统一为"4 次正向 + 4 次负向" |
| **F-4** | 17/124 证据文件被 `*.log` 忽略 | 低 | `git check-ignore` 命中；PH-R1 证据同样无 `.log` 入库（仓库既有约定） | 明确"日志是否入库"策略；若入库需 `-f` 或规则例外 |
| **F-5** | 任务书 §8 的 23 条与实际 23 项自检不一致 | **中** | 7 项（时间源统一、CC 位置同步、强化消费、牵引完成、峰值位移、原始数据聚合、Define 清理）不在自检内；其中"时间源统一"实测不成立 | 以本报告 §8.1 的对账表为准；不要宣称"任务书 23 条全部通过" |
| **F-6** | `Assets/Resources.meta` 未跟踪且未被忽略 | 低 | 13:53 前即存在（非本批产生） | 负责人决定纳入或删除；不随工具提交 |
| **F-7** | PH-R1 证据仍为 sparse-checkout（`skip-worktree`） | 低（沿用） | 466 个文件物理未检出；历史复核口径为"快照 SHA 一致" | 若需逐文件物理复核，需先 `git sparse-checkout` 调整（本轮禁止） |
| **F-8** | 全矩阵未在新 DLL 下重跑 | 中 | 本批仅定向 3 行；产品源码零改动 | 如需对外声称"19 项在新构建下通过"，须另开批次 |

---

## 16. 最终审计结论

### **CONDITIONAL_PASS**

**支撑 PASS 的部分（证据链完整、可独立复算）**

1. 身份链闭合：4/4 运行的 `loadedAssemblySha256`（Player 自算）= `expectedAssemblySha256` = `dllSha256Before` = `dllSha256After` = `b3ce427c…1e91`；错误期望时 `identityVerified=false`、exit 1、Driver 判 FAIL。
2. 双刃反击因果链成立：统一时钟后 evade 7.187 → contact 7.803（+0.616s，≤0.85 窗，1.8×=59.40）→ 冷却 9.500s → contact 17.301（0.65×=21.45，未再强化）；帧号 903/3732 提供无时钟印证。
3. `staff.field` 四段逐段正确（21.45/13.20/13.20/13.20，总 61.05），10 项结构检查全过。
4. C-gate 三段 21.45、HP 序列一致、冷却 7.10633s、冷却期拦截生效。
5. 40/40 复算独立重现；190/190 保护文件、311/311 历史证据零改动；产品源码修改 0。
6. 23 项自检全部有原始证据。

**不能判 PASS 的部分**

- **F-1**：交付报告的时间表混用两套时钟，制造了"contact 早于 evade"的误导性呈现——这是对外证据的可审计性缺陷，必须修正。
- **F-1b**：验收工具中存在时钟混用的判据（`closeDamageWindow` / `cooldownAllow` 的 1.2s 稳定期恒真），本批侥幸由时间上限兜底未致漏计，属真实代码缺陷。
- **F-5**：任务书 §8 的 23 条与实际自检不对应，其中"时间源统一"不成立；"23/23"不可外推为任务书 23 条全通过。
- **F-2**：保护清单有 2 个文件盲区，且这 2 个文件缺构建前逐文件 SHA 快照（证据等级 B）。

**结论口径**：数据结论（伤害、身份、消费一次、保护面）**成立且可复现**；
但交付物存在 1 项呈现缺陷、1 项工具逻辑缺陷、1 项统计口径缺陷与 1 项保护面盲区，
在修正并复审前不予 PASS。

**解除条件**：修正 F-1（报告换算/记账）、F-1b（统一判据时钟）、F-5（对账表述）、
F-2（扩充清单 + 设置文件快照），再跑一次定向 A–E 即可转 PASS。

---

## 17. 审计执行边界声明

- 本轮**未**修改任何产品源码、验收工具、原始证据、ProjectSettings、Packages。
- **未**执行 `git add` / `commit` / `push` / `merge`，**未**执行 `reset` / `checkout` / `restore` / `clean`。
- **未**新增 Player Run，**未**覆盖历史证据，**未**删除失败记录。
- 本报告为唯一新增文件（`ProjectDocs/.../DeliveryUxProgression03APlayerHarnessR2R1/PH-R2-R1-FINAL-AUDIT.md`）。
- 审计中所有数字均由原始工件重算；未采信 `INDEX.json`、`RECOMPUTE.json`、`SELFTEST.json` 的自述 `ok/pass` 字段作为结论依据。
