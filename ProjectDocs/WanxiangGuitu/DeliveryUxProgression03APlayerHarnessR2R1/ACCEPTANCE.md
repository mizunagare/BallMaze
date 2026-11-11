# ACCEPTANCE — PH-R2-R1 验收判定

> 本文件回答：**"凭什么判这几项 PASS？"**
> 规则先行、证据在后：每条断言都给出可复核的字段路径，而不是"看起来对"。

---

## 1. 判定语义（先定义，再使用）

单次 Player Run 的 `finalStatus` 只可能是三种之一，由 Driver 在 Player 退出**之后**判定：

| 状态 | 触发条件 | 含义 |
|---|---|---|
| **PASS** | `exitCode==0` ∧ `¬timedOut` ∧ 身份全闭合 ∧ `marker` 正确 ∧ `result.pass==true` | 可采信 |
| **INCOMPLETE** | `exitCode==2` 或 `result.incomplete==true`（仅 `twin.counter`：第二次反击无 contact） | **不可采信，也不算失败**；保留全部原始证据，要求补测 |
| **FAIL** | 超时（即使 result.json 写 pass=true）/ 退出码非 0 / 身份不一致 / result 缺失或陈旧 / marker 不符 / `result.pass==false` | 不可采信，必须定位 |

判定顺序固定为：`超时 → 退出码 → INCOMPLETE → 身份 → marker → harness pass`。
**身份不一致的优先级高于"结果看起来正确"**——这是 R1-01 的核心纪律。

批次结论只允许：`PASS` / `CONDITIONAL_PASS` / `BLOCKED`。

---

## 2. 批次总览

| 阶段 | 内容 | 判定 | 关键证据 |
|---|---|---|---|
| **A** | 构建身份冒烟（Acceptance + NoDefine + marker + 四 SHA） | **PASS** | `build/acceptance-build.json`、`build/nodefine-build.json`、`build/build-manifest.json` |
| **B** | C-gate：`sword.triple` 真实战斗 | **PASS** | `runs/C-GATE/`、`recompute.json` (11/11) |
| **C** | 双刃反击：`twin.counter` 两次 contact | **PASS** | `runs/TWIN-COUNTER/`、`recompute.json` (18/18) |
| **D** | `staff.field` 逐段伤害 | **PASS** | `runs/STAFF-FIELD/`、`recompute.json` (11/11) |
| **E** | Harness 回归 18 项 + 身份 5 项 | **PASS** | `selftest/SELFTEST.json` (23/23) |

**批次结论：PASS**（范围限于本轮定向 A–E，不代表重跑 19 项全矩阵，见 §7）。

---

## 3. A — 构建身份冒烟

| 断言 | 实测 | 判定 |
|---|---|---|
| Acceptance 构建存在且可执行 | `Builds/WanxiangGuitu.Acceptance/WanxiangGuitu.exe` | ✓ |
| NoDefine 构建存在 | `Builds/WanxiangGuitu.AcceptanceNoDefine/WanxiangGuitu.exe` | ✓ |
| Acceptance DLL 含 Harness marker | `UX_ACCEPTANCE_HARNESS_v1` × 2（UTF-16LE） | ✓ |
| NoDefine DLL 不含 marker | 0 次（双编码扫描） | ✓ |
| Acceptance EXE SHA | `b70442f9…2436` | ✓ |
| Acceptance DLL SHA | `b3ce427c…1e91` | ✓ |
| NoDefine EXE SHA | `b70442f9…2436`（与 Acceptance 相同，**Launcher 恒定**） | ✓（不作为身份依据） |
| NoDefine DLL SHA | `00373fe7…710e` | ✓ |
| manifest 与实际产物一致 | `manifestReasons=[]` | ✓ |
| buildId 生成 | `phr2r1-318c660afbcaf218d04c469b` | ✓ |
| `UX_ACCEPTANCE` 泄漏到 ProjectSettings | 0 次 | ✓ |

---

## 4. B — C-gate（`sword.triple`，真实命中）

| 断言 | 实测 | 判定 |
|---|---|---|
| 真实目标存在并准备完成 | `target.prepared=true`，`c1:elite`，`initialHP=140` | ✓ |
| 真实伤害事件（非模拟） | `damage-events.jsonl` 3 条 + `target-events.jsonl` 3 条 | ✓ |
| HP 序列 | `140 → 118.55 → 97.10 → 75.65` | ✓ |
| 每段伤害 | `21.45` × 3（= 33 × 0.65） | ✓ |
| 逐段 expected 匹配 | 3/3 段 `|actual−expected| ≤ 0.05` | ✓ |
| 冷却 | `7.10633s`（期望 7.00，容差 −0.6/+1.5） | ✓ |
| 冷却期重按被拦 | `blockedDuringCooldown=true` | ✓ |
| DLL 身份闭合 | `loadedAssemblySha256 == dllSha256Before == expectedAssemblySha256` | ✓ |
| 退出码 / 超时 | `exitCode=0`，`timedOut=false` | ✓ |

> C-gate 的含义：**若这里拿不到真实伤害，后续一律不得 PASS**。本批已通过，后续判定有效。

---

## 5. C — 双刃反击（`twin.counter`，消费一次）

> **修订（PH-R2-R1-FIX-02）**：原表第 3、8 行的"7.187345"与"9.497s"分别取自两套时钟（见
> `DAMAGE_MODEL.md` §2.3.1）。因果链本身成立，但并列呈现会被误读为"contact 早于 evade"。
> 下表改为**统一 `Time.unscaledTime` 口径**（换算偏移 4.358567s，双路独立推导）。

任务书 §4 的 11 条，逐条给出证据来源（统一时钟）：

| # | 条件 | 证据字段 | 统一时钟实测 |
|---|---|---|---|
| 1 | 真实敌人攻击 | `t3.evadeSeen=true` | ✓ |
| 2 | 玩家真实翻滚 | `t3.dodgeRollObserved=true` | ✓（翻滚帧 703/717） |
| 3 | 无敌窗口成功拒绝攻击 | `evadeSeenAt`（原生 unscaled） | **7.187** |
| 4 | actual-evaded-attack 被观察到 | `evadeSeenAt > 0` 且 `observations[stage=actual-evaded-attack]` 存在 | ✓ |
| 5 | 第一次反击真实 contact | `damage-events` hitId=1，`skillPhase="counter"` | **7.803**（+0.616s ≤ 0.85 强化窗） |
| 6 | 第一次 empowered=true | `t3.counterEmpowered=true` | ✓ |
| 7 | 第一次伤害 1.8× | `59.39999 = 33 × 1.8` | ✓ |
| 8 | 技能冷却结束 | 第二次 F 按下距第一次 **9.500s**（cd 9.5s）；两次 contact 间隔 9.497s | ✓ |
| 9 | 第二次反击真实 contact | `secondCounterContactSeen=true`，hitId=2 | **17.301** |
| 10 | 第二次 empowered=false | `t3.secondCounterEmpowered=false` | ✓ |
| 11 | 第二次未获新强化状态 | 第 2 次伤害回落到 `21.45 = 33 × 0.65`（基线，非 1.8×） | ✓ |

严格判定式（Harness 实际代码）：

```csharp
bool ok = evadeSeen && dodgeRollObserved && counterContactSeen && counterEmpowered
          && secondCounterContactSeen && !secondCounterEmpowered;
```

- 任务书给定的 5 项式 `evadeSeen && counterContactSeen && counterEmpowered && secondCounterContactSeen && !secondCounterEmpowered` **被完整包含**；
- 额外要求 `dodgeRollObserved`（更严格，非放宽）；
- 若 `secondCounterContactSeen==false` → `incompleteReason` 落盘 + `Application.Quit(2)` → Driver 记 **INCOMPLETE**，绝不映射为 PASS；
- 本批未修改产品冷却、未触碰 `consumedEvade` / 强化状态字段。

**本批实际拿到第二次真实 contact**（统一时钟 17.301s，伤害 21.45），因此不是"因 INCOMPLETE 而跳过"，而是真正验证了"只消费一次"。

PH-R2-R1-FIX 未重跑本场景（修复不触碰其判定路径），改为在**冻结原始事件**上按统一时钟复算，见
`Evidence/PH-R2-R1-FIX/recompute/twin-timeline.json` 与 `INDEX.json#phases.F`。

---

## 6. D — `staff.field` 逐段伤害

见 `DAMAGE_MODEL.md` §2.2。摘要：

| 段 | ratio | expected | actual | 判定 |
|---|---|---|---|---|
| 1 | 0.65 | 21.45 | 21.45 | ✓ |
| 2 | 0.40 | 13.20 | 13.20 | ✓ |
| 3 | 0.40 | 13.20 | 13.20 | ✓ |
| 4 | 0.40 | 13.20 | 13.20 | ✓ |
| 总 | — | 61.05 | 61.05 | ✓ |

`result.json` 中 `expectedHitRatios=[0.65,0.4,0.4,0.4]`、`expectedTotal=61.05`，逐段断言由
`recompute.json` 独立复算（11/11）。

---

## 7. 范围与不适用范围（必须与结论一起读）

| 项 | 本批 | 说明 |
|---|---|---|
| 定向 Run | 3 个（C-GATE / TWIN-COUNTER / STAFF-FIELD） | 任务书 §7 明确"不再执行全部 19 项" |
| 自检 Run | 5 个（positive / stale / wrongsha / timeout / wrongdllsha） | 均为工具行为验证，非产品验收 |
| 19 项矩阵 | **未重跑** | 产品源码零改动（`git diff` 仅 2 个验收工具文件）→ PH-R2 的 19 PASS 结果在新 DLL 下不被推翻，但也**不被本批重新背书** |
| 03B | 未启动 | 任务书 §10 |

因此本批 PASS 的正确读法是：**"R1-01/02/03/04 三个缺陷已修复且可复现验证；定向范围内 PASS"**，
而不是"整套 UX-PROGRESSION-03A 重新通过验收"。
