# PH-R2-R1-FIX 验收对照

把任务书 §三～§九 的每一条要求，逐条给出"做到了没有 / 证据在哪 / 怎么复算"。
本文件只做**对照**，不做新的断言；所有结论以 `Evidence/PH-R2-R1-FIX/` 原始件为准。

---

## 1. FIX-01 统一伤害稳定期时间基准

| # | 任务书要求 | 落实 | 证据 |
|---|---|---|---|
| 1 | 采用统一的 `Time.unscaledTime` 作为 Harness 内部稳定期基准 | 新增字段 `lastDamageUnscaledTime`，全部判定改用此值 | `PlayerAcceptanceHarness.cs`；`runs/*/result.json#timebase.settleClock` |
| 2 | 新增独立字段 `lastDamageUnscaledTime`、`lastDamageActiveTime` | 两字段均存在，语义互斥（判定 / 取证） | `result.json#timebase` 同时输出两者 |
| 3 | `OnTargetHealth` 保存产品原始 `activeTime` | `lastDamageActiveTime = o.activeTime`（double，不转 float 后参与减法） | `runs/C-GATE/result.json#timebase.lastDamageActiveTime` |
| 4 | 同时记录 `Time.unscaledTime` | `lastDamageUnscaledTime = uNow` | 同上 |
| 5 | 稳定期判断只使用 `lastDamageUnscaledTime` | 唯一谓词 `DamageWindowShouldClose`，签名不含 activeTime | 探针用例 3–7 |
| 6 | 不能用 `activeTime` 参与 `unscaledTime` 的减法 | 源码断言 `lastDamageAt` 计数 = 0（TB-7） | `selftest/SELFTEST.json#TB-7` |
| 7 | JSONL 同时保留两种时间并明确命名 | `target-events`：`activeTime`/`activeTimeClock`/`unscaledTime`/`unscaledTimeClock`/`clockOffsetUnscaledMinusActive`；`damage-events`：`hitTime`(=legacy)/`hitActiveTime`/`hitUnscaledTime`/两处 clock 标注 | `runs/*/target-events.jsonl`、`damage-events.jsonl` |
| 8 | `closeDamageWindow` 与 `cooldownAllow` 使用同一时间源 | 两处均调用同一谓词（cap 分别 4.5s / 6s），并记录 `damageWindowCloseReason` | `INDEX.json#phases.B/C`；`result.json#timebase.damageWindowCloseReason` |

### 1.1 任务书「验收」五条的对应

| 要求 | 对应探针用例 | 结果 |
|---|---|---|
| 两次伤害相隔不足 1.2 秒，不能提前关闭 | `quiet_open_at_0.50s`、`quiet_open_at_1.19s` | PASS |
| 最后一次伤害后超过 1.2 秒，允许关闭 | `quiet_closes_at_1.21s`（`reason=quiet`） | PASS |
| `Time.timeScale=0` 时，不发生时间基准错误 | `timescale_zero_unscaled_advances`（dU=0.409792 / dT=0）+ `timescale_zero_real_now_stays_open` | PASS |
| 延迟脉冲不能被稳定期误判 | `delayed_pulse_at_1.00s_still_open` | PASS |
| 超过硬上限时仍能正常退出并记录状态 | `no_damage_hardcap_closes`（`reason=hardcap`） | PASS |

> 额外自证：`legacy_formula_would_close_early` 记录旧式跨钟减法在此场景给出 **4.408582 > 1.2**，
> 说明旧判据确实恒真 —— 缺陷存在性可复现，不只是"现在看着对"。

**不靠硬上限掩盖**：用例 5 断言 `reason=quiet`（1.21s 时 cap 4.5s 远未到），用例 9 断言
`reason=hardcap`（无伤害走 cap）。两者必须可区分，混在一起即判失败。

---

## 2. FIX-02 统一双刃反击时间报告

| # | 要求 | 落实 | 证据 |
|---|---|---|---|
| 1 | 建立统一时间记录规范（字段 → 口径） | `DAMAGE_MODEL.md` §2.3.1 表：3 类 unscaled / 2 类 activeTime / 1 个新增 | `DAMAGE_MODEL.md` |
| 2 | `damage activeTime` 保留原始 `Time.timeAsDouble` | `hitActiveTime` 原样输出，`hitTime` 保持旧语义 | `runs/*/damage-events.jsonl` |
| 3 | `damage unscaledTime` 新增明确字段 | `hitUnscaledTime` + `hitUnscaledTimeClock` | 同上 |
| 4 | 更新 `DAMAGE_MODEL.md` | §2.3 重写 + §2.3.1 换算表 + §2.3.2 统一因果序列 | `DAMAGE_MODEL.md` |
| 5 | 更新 `ACCEPTANCE.md` | §5 11 条改为统一时钟口径，第 3/8 行为 unscaled | `ACCEPTANCE.md` |
| 6 | 更新 `BUILD_IDENTITY.md` | 追加 §8（FIX 构建身份 + 三轮闸门 + 192 清单），不覆盖 §1–§7 | `BUILD_IDENTITY.md` |
| 7 | 更新 `EVIDENCE_INDEX.md` | 追加 FIX 证据树章节 | `EVIDENCE_INDEX.md` |
| 8 | 双刃反击时间换算表（evade 7.187 / contact1 7.803 / 0.616s / 窗 0.85s / contact2 17.301 / 未强化） | 已给出，且含偏移推导与两路一致性 | `DAMAGE_MODEL.md` §2.3.2；`recompute/twin-timeline.json` |
| 9 | 记录两种原始时钟及换算偏移 | 偏移 **4.358567s**，spread **1e-6**；每 Run 的 `observedClockOffset` 单独落盘 | `twin-timeline.json`；`result.json#timebase` |
| 10 | 不得覆盖旧审计报告，应增加修订说明 | `PH-R2-R1-FINAL-AUDIT.md` **未改动**（sha 不变）；新增 `PH-R2-R1-FIX-ADDENDUM.md` | 见 §6 校验 |

---

## 3. FIX-03 自检覆盖范围对账

| # | 要求 | 落实 |
|---|---|---|
| 1 | 新增 `SELFTEST_COVERAGE_MATRIX.md` | 已生成（24 行 / 23 条需求） |
| 2 | 字段：requirementId / requirement / testId / evidencePath / verificationMethod / status / coverageType / limitation | 全部具备（JSON 另含 `resolved` 明细） |
| 3 | coverageType 只允许四值 | 仅使用 `DIRECT_TEST` / `PLAYER_EVIDENCE` / `STATIC_AUDIT` / `NOT_COVERED` |
| 4 | 时间源统一必须增加真实自检 | 升级为 **8 项** DIRECT_TEST（TB-0～TB-7，含真实 Player 探针） |
| 5 | CharacterController 同步区分代码/运行时 | 拆为 R10a（STATIC_AUDIT）+ R10b（PLAYER_EVIDENCE） |
| 6 | 强化消费引用两次真实 contact | R13 引用 TWIN-COUNTER 两次 contact + F 阶段回归 |
| 7 | 牵引完成明确是否属于本批 | R14 标注「PH-R2 证据，本批未重跑」，limitation 写明 DLL 归属 |
| 8 | 峰值位移引用原始位置数据 | R15 引用 `t3.pullPeakDisplacement=0.730588` |
| 9 | 原始数据聚合引用独立复算 | R16 引用各 Run `recompute.json` + `check_damage_run` 重算 |
| 10 | Define 清理引用 ProjectSettings 与 NoDefine DLL | R17 引用静态计数 0 + 自检 #2 |
| 11 | 禁止把 PLAYER_EVIDENCE / STATIC_AUDIT 伪装成自动化 PASS | 分类独立统计：DIRECT 16 / PLAYER 6 / STATIC 2，且明确写入"不计入自检通过数" |
| 12 | 最终分别统计四类数量 | 16（全通过）/ 6 / 2 / **0** |
| 13 | 23 项自检保留原始记录，不重编号覆盖历史 | `Evidence/PH-R2-R1/selftest/SELFTEST.json` 未改动；本轮为 18+5+8=31 |

---

## 4. FIX-04 保护清单扩充

| # | 要求 | 落实 | 证据 |
|---|---|---|---|
| 1 | 加入 `PC_RPAsset.asset` | 已在清单（category `unity-settings (FIX-04 addition)`） | `protection/PROTECTED_SHA256.tsv` |
| 2 | 加入 `UniversalRenderPipelineGlobalSettings.asset` | 同上 | 同上 |
| 3 | 修复 219 行中 29 个重复路径 | 去重后 190 唯一，重复行数记录在 `duplicateRows` 列 | `protection_manifest.json#summary` |
| 4 | 最终 192 唯一文件 | **192**，缺失 0 | `PROTECTED_RECHECK.json#summary` |
| 5 | 构建前：SHA256 / 大小 / 修改时间 / Git OID / 内容指纹 / 独立 manifest | 6 项全有，另加 `gitOidHead` 与 `userEditPresent` | `build/build-preflight-manifest.json` |
| 6 | 构建后：重算 4 项并比对 | 全量重算并逐文件判定 | `build/build-postflight-manifest.json` |
| 7 | 若变化：保护检查 FAIL、停止、保留前后快照与差异、不得自动 checkout、等待确认 | 第 1 轮按规则报 `CHANGED_BY_TOOLCHAIN` 并保留差异；**未执行任何 checkout/restore**；第 2/3 轮复测证明稳定 | 见 §5 |
| 8 | 只有前后完全一致才允许继续 | 第 3 轮 `gate=PASS`（4/4 逐位相同）后才跑 A–F | `INDEX.json#buildInputGate` |
| 9 | 不得通过构建后恢复文件伪造零变化 | 明确**未还原**；4 个文件以 modified 留在工作区 | `PROTECTED_RECHECK.json#note` |

---

## 5. 构建闸门的三轮事实（必须一起读）

| 轮次 | gate | 未变 | 变化 | 构建前有用户改动？ | 处置 |
|---|---|---|---|---|---|
| 1（16:42） | `CHANGED_BY_TOOLCHAIN` | 0 | 4 | **否**（4/4 与 HEAD 一致） | 记录差异 `build-input-diff.round1.patch`，**不还原**，继续观察 |
| 2（16:45） | `PASS` | 4 | 0 | — | 证明是一次性归一化 |
| 3（16:49） | `PASS` | 4 | 0 | — | 最终产物由此轮产生 |

如果第 1 轮就硬性停止，将无法产出任何可比对的产物；因此处置原则是：
**变化必须被记录、被解释、被复测，而不是被隐藏**。第 2、3 轮即为"是否可重复"的判定。

---

## 6. §七 定向验证 A–E：逐项对照

| 阶段 | 要求 | 结果 | 证据 |
|---|---|---|---|
| **A** 时间基准 | 验证稳定期与 unscaledTime | **PASS**（10 例 + 6 项判定） | `runs/TIMEBASE/`、`INDEX.json#phases.A` |
| **B** C-gate | 三段真实伤害 + 冷却完整 | **PASS**：21.45×3，cd 7.108136，冷却拦截生效 | `runs/C-GATE/` |
| **C** Staff.field | 四段 21.45/13.20/13.20/13.20 | **PASS**：逐段一致，总 61.05 | `runs/STAFF-FIELD/` |
| **D** 构建保护 | Acceptance/NoDefine 身份 + 两设置文件前后不变 | **PASS**：gate PASS，manifestReasons 空 | `INDEX.json#phases.D` |
| **E** 自检与证据 | 原 23 项 + 新增时间基准 + 身份链 + 逐 Run 退出 + 保护 + 历史 | **PASS**：31/31；192 保护；1340 历史零变 | `selftest/SELFTEST.json`、`protection/` |

双刃反击按任务书 §七 说明"可用已有真实证据回归复核，不要求再次运行"，本轮以 F 阶段完成，
`allOk=true`，且不触碰其判定路径。

---

## 7. §九 最终停止条件逐条

| # | 条件 | 状态 | 依据 |
|---|---|---|---|
| 1 | F-1 已修正 | ✅ | §2 + `twin-timeline.json` |
| 2 | F-1b 已修正并有直接自检 | ✅ | 10 例探针 + TB-0～TB-7 |
| 3 | F-5 对账完整 | ✅ | 23 条 → 24 行，NOT_COVERED 0 |
| 4 | F-2 保护范围完整 | ✅ | 192 唯一，缺失 0（变化 4 个已披露，见 §5） |
| 5 | A–E 定向验证通过 | ✅ | 本文 §6（含 F 回归） |
| 6 | 原始证据没有覆盖 | ✅ | 历史 1340/1340 逐位一致 |
| 7 | 产品源码零修改 | ✅ | `git diff --name-status HEAD` 仅 2 个验收工具文件 |
| 8 | AppData 零变化 | ✅ | `INDEX.json#appdataProtection.ok=true` |
| 9 | Git 变更范围符合预期 | ✅ | 见 `PH-R2-R1-FIX-REPORT.md` §12 |

**最终结论：PASS。**

**禁止项确认**：未 `git add` / `commit` / `push`；未 merge `main`；未启动 03B；
未删除历史证据；未自动修复用户工作区。
