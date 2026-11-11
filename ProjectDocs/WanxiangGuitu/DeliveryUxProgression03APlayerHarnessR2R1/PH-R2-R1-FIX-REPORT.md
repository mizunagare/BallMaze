# PH-R2-R1-FIX 报告

**批次**：PH-R2-R1-FIX（缺陷修正批次，非功能开发）
**仓库**：`mizunagare/BallMaze`
**HEAD**：`e9f9a142e80f0b4013338f70e5a5b6d1c3776826`
**分支**：`verify/ux-progression-03a-player-harness-r2-r1`
**构建**：`phr2r1-e32e240735e921f7c4aad220`，Harness `VERSION=3`
**结论**：**PASS**（范围：F-1 / F-1b / F-5 / F-2 + 定向 A–F）
**状态**：**未提交、未推送、未合并、未启动 03B，暂停待审**

---

## 1. 一句话结论

上一轮审计留下的四项缺陷全部修好并且**每一项都有可直接复算的证据**：
双时钟呈现（F-1）改为双钟分列 + 统一换算；稳定期判据（F-1b）改为单时钟并由
**真实 Player 内的 10 例时钟探针**直接断言；自检覆盖（F-5）做了 23 条逐条对账，
未覆盖项从 7 条降到 **0**；保护清单（F-2）从 219 行去重为 190，并补入缺失的 2 个 Unity 设置文件
= **192 个唯一文件**，同时新增构建前/后双快照闸门。

同时必须如实说明一件事：**本轮构建让 4 个 Unity 构建输入文件发生了字节变化**（一次性编辑器
schema 归一化），按任务书要求**没有用 `git checkout` 还原**，因此它们现在以 modified 状态留在工作区。
第 2、3 轮构建证明该变化不再重复（4/4 逐位相同），最终产物即由"零构建输入漂移"的构建产生。

---

## 2. 四项缺陷：根因 → 修法 → 证据

| ID | 缺陷 | 根因 | 修法 | 直接证据 | 状态 |
|---|---|---|---|---|---|
| **F-1** | 报告把 `hitTime`(Time.time) 与 `evadeSeenAt`(unscaledTime) 并列，制造"contact 早于 evade"的误读 | 两套时钟混排且未标注 | `DAMAGE_MODEL.md` §2.3/§2.3.1/§2.3.2 与 `ACCEPTANCE.md` §5 改为**双钟分列 + 换算列表 + 统一口径因果序列**；Harness 输出新增 `timebase` 区块与 `hitActiveTime`/`hitUnscaledTime` 显式字段 | `recompute/twin-timeline.json`（偏移 4.358567s，双路独立推导差 1e-6） | **已修正** |
| **F-1b** | `Time.unscaledTime - lastDamageAt`（后者是 `Time.timeAsDouble`）恒真 → 1.2s 稳定期形同虚设 | 跨时钟相减 | 新增 `lastDamageUnscaledTime` / `lastDamageActiveTime` 两个独立字段；**唯一判定函数** `DamageWindowShouldClose(nowUnscaled,lastDamageUnscaled,windowStartUnscaled,cap)` 的签名里根本不存在 activeTime 形参；`closeDamageWindow` 与 `cooldownAllow` 全部改用同一谓词；新增 `damageWindowCloseReason` 区分 `quiet`/`hardcap` | `runs/TIMEBASE/timebase-probe.json`（10 例）、自检 TB-0～TB-7 | **已修正 + 有直接自检** |
| **F-5** | 任务书 23 条 ≠ 实际 23 项自检，其中"时间源统一"实测不成立 | 从未做过逐条对账 | 新增 `SELFTEST_COVERAGE_MATRIX.md/.json`：23 条逐条映射，强制四分法；"时间源统一"升级为 8 项真实自检 | `SELFTEST_COVERAGE_MATRIX.json`：DIRECT 16（通过 16）/ PLAYER 6 / STATIC 2 / **NOT_COVERED 0** | **已对账** |
| **F-2** | 保护清单缺 `PC_RPAsset.asset`、`URPGlobalSettings.asset`，且无构建前快照 | 清单从未覆盖构建输入 | 清单去重 219→190，补 2 = **192**；新增 `preflight`/`postflight` 双清单（size/mtime/SHA256/worktree OID/HEAD OID/userEditPresent） | `protection/PROTECTED_SHA256.tsv`、`build/build-{pre,post}flight-manifest*.json` | **已修复** |

### 2.1 F-1b 的关键设计点：让错误无法复现

不是"改一行减号"，而是把判据收敛成一个签名受限的纯函数：

```csharp
internal static bool DamageWindowShouldClose(
        float nowUnscaled, float lastDamageUnscaled,
        float windowStartUnscaled, float hardCapSeconds)
```

- 参数里没有 `activeTime`，所以"拿产品钟减 Harness 钟"在类型层面就无法写出来；
- 返回原因由 `DamageWindowCloseReason(...)` 单独给出，`quiet` 与 `hardcap` 必须可区分，
  避免"靠 4.5s/6s 硬上限兜底"冒充满意；
- 源码静态断言（TB-7）：`lastDamageAt` 出现次数 **0**，可疑跨钟减法行 **0**。

### 2.2 F-1b 修复前后的判据差异

| 场景 | 旧式 `nowU − activeTime > 1.2` | 新式 `nowU − lastDamageUnscaled > 1.2` |
|---|---|---|
| 最后一次伤害后 0.05s | 4.3586 > 1.2 → **立即关闭**（错） | 0.05 → 保持开启（对） |
| 延迟脉冲在 1.00s 到达 | 窗口已关 → **命中被丢弃**（错） | 1.00 < 1.2 → 仍记录（对） |
| 最后一次伤害后 1.21s | 关闭 | 关闭，`reason=quiet` |

> 注意：PH-R2-R1 那批**实际没有漏计**（末次命中先于窗口评估点），所以这是"契约未实现"而非
> "数据错误"。本轮把它做成可断言的事实，而不是靠事后解释。

---

## 3. 构建身份与构建输入保护

### 3.1 产物身份

| 产物 | SHA256 |
|---|---|
| Acceptance **DLL** | `db258d6e7f02b0b8…`（完整值见 `Builds/build-manifest.json`） |
| NoDefine **DLL** | `f8b44e1e7471e354…` |
| Acceptance EXE（Launcher） | `b70442f90f50cd91…2436` |
| NoDefine EXE（Launcher） | `b70442f90f50cd91…2436`（与上者相同 → 再次说明身份必须锚在 DLL） |
| buildId | `phr2r1-e32e240735e921f7c4aad220` |
| define 泄漏 | **0** |

三次真实运行的 `loadedAssemblySha256`（Player 用 `Assembly.GetExecutingAssembly().Location` 自算）
= `dllSha256Before` = `expectedAssemblySha256` = `dllSha256After` = `db258d6e…`，**四方逐位一致**。

| Run | PID | exit | identityVerified | harness ver |
|---|---|---|---|---|
| TIMEBASE | 32072 | 0 | true | 3 |
| C-GATE | 9752 | 0 | true | 3 |
| STAFF-FIELD | 15308 | 0 | true | 3 |

### 3.2 构建输入闸门（3 轮）

| 轮次 | preflight | postflight | 结果 | 说明 |
|---|---|---|---|---|
| 1 | 16:42 | 16:43 | `CHANGED_BY_TOOLCHAIN`（0 未变 / 4 变化） | Unity 一次性归一化：URP prefilter 模式重算 + `scriptingDefineSymbols` `{}` → `Standalone:`。**构建前 4 个文件全部与 HEAD 一致**，不存在被覆盖的用户修改 |
| 2 | 16:45 | 16:47 | **PASS**（4 未变 / 0 变化） | 证明第 1 轮是一次性归一化，不是每构建必改写 |
| 3 | 16:49 | 16:51 | **PASS**（4 未变 / 0 变化） | **最终产物由此轮产生**：零构建输入漂移 |

第 1 轮差异完整留档：`build/build-input-diff.round1.patch`（169 行）。

**没有执行 `git checkout` / `restore` / `reset` / `clean`。** 4 个文件的归一化结果原样留在工作区，
`git status` 可见 —— 这是主动保留的可审计状态，不是遗漏。

### 3.3 保护面（192 唯一文件）

| 口径 | 结果 |
|---|---|
| 清单规模 | 219 行 → 去重 29 → 190 唯一 → +2 = **192** |
| 相对 FIX 起点 | **188 未变**，4 变化（全部为上述 4 个构建输入），缺失 0 |
| 变化文件是否有用户改动风险 | 均为 `userEditPresent=false`（构建前 = HEAD 内容） |
| 历史证据（PH-R1/PH-R2/PH-R2-R1/FINAL-AUDIT/Runs/INDEX/矩阵） | **1340/1340 逐位一致，0 变化** |
| AppData（default + legacy） | 批次前后指纹一致 |

---

## 4. A — 时间基准（真实 Player 内探针）

`runs/TIMEBASE/timebase-probe.json`，`allOk=true`，10 例全过。

| # | 用例 | 输入 | 期望 | 实测 | 结果 |
|---|---|---|---|---|---|
| 1 | timeScale=0：unscaled 前进而 scaled 冻结 | 真实等待 0.41s | `dU>0.30 ∧ |dT|<0.05` | `dU=0.409792`，`dT=0` | PASS |
| 2 | timeScale=0 时真实时刻窗口仍开启 | 真实 elapsed 0.41s | 不关闭 | `closed=false` | PASS |
| 3 | 两次伤害相隔 0.50s 不得关闭 | last=u, now=u+0.50 | 不关闭 | `closed=false` | PASS |
| 4 | 相隔 1.19s 不得关闭 | now=u+1.19 | 不关闭 | `closed=false` | PASS |
| 5 | 超过 1.2s 允许关闭 | now=u+1.21 | 关闭且 `reason=quiet` | `closed=true`,`quiet` | PASS |
| 6 | 延迟脉冲 1.00s 不被误判 | now=u+1.00 | 不关闭（命中保留） | `closed=false` | PASS |
| 7 | 产品钟偏移（−4.36s）不得缩短静默期 | now=u+0.05 | 不关闭 | `closed=false` | PASS |
| 8 | 无伤害时硬上限前保持开启 | now=w+1.00 | 不关闭 | `closed=false` | PASS |
| 9 | 硬上限到期必须退出且标记 | now=w+4.60 | 关闭且 `reason=hardcap` | `closed=true`,`hardcap` | PASS |
| 10 | 旧式跨钟减法确实会误判（缺陷存在性证明） | `nowU−activeTime=4.408582` | >1.2 → 旧式会关 | `ok=true` | PASS |

用例 5/9 显式断言 `reason`，因此**不可能**出现"硬上限冒充静默期"的通过。

## 5. B — C-gate（`sword.triple`）

| 段 | HP before | HP after | actual | expected | 比率 |
|---|---|---|---|---|---|
| 1 | 140.00 | 118.55 | 21.45 | 21.45 | 0.650 |
| 2 | 118.55 | 97.10 | 21.45 | 21.45 | 0.650 |
| 3 | 97.10 | 75.65 | 21.45 | 21.45 | 0.650 |

总伤害 64.35；`cooldownMeasured=7.108136`（期望 7.0，容差 ±0.6/+1.5）；冷却期再施放被拒绝
（`blockedDuringCooldown=true`）。

## 6. C — Staff.field（逐段）

| 段 | ratio | expected | actual | 判定 |
|---|---|---|---|---|
| 1 | 0.65 | 21.45 | **21.45** | PASS |
| 2 | 0.40 | 13.20 | **13.20** | PASS |
| 3 | 0.40 | 13.20 | **13.20** | PASS |
| 4 | 0.40 | 13.20 | **13.20** | PASS |
| 总 | — | 61.05 | **61.05** | PASS |

HP 链 140 → 118.55 → 105.35 → 92.15 → 78.95 连续；`cooldownMeasured=9.105258`；
`expectedHitRatios=[0.65,0.4,0.4,0.4]`。**不是只看总数**：每段独立比对，且 0.65 与 0.40 可区分。

## 7. D — 构建保护与身份

`INDEX.json#phases.D`：`gate=PASS`，`unchanged=4`，`changed=0`，`manifestReasons=[]`，
Acceptance marker `true` / NoDefine marker `false`。

## 8. E — 自检 31/31

| 分组 | 数量 | 结果 |
|---|---|---|
| 原始自检（保留、未重编号） | 18 | 18/18 |
| 身份自检（R1-01/R1-04） | 5 | 5/5 |
| **时间基准自检（FIX-01 新增）** | **8**（TB-0～TB-7） | **8/8** |

其中 TB-3 的真实数据：`dU=0.41333`，`dScaled=0`；TB-6 给出旧式值 `4.408582 > 1.2`；
TB-7 源码断言 `lastDamageAt=0 / suspiciousLines=0`。

覆盖对账见 `SELFTEST_COVERAGE_MATRIX.md`：**DIRECT_TEST 16 条全部通过**，
PLAYER_EVIDENCE 6 条、STATIC_AUDIT 2 条**不计入自检通过数**，NOT_COVERED **0**。

## 9. F — 双刃反击冻结回归（不重跑）

修复不触碰 `twin.counter` 判定路径，因此按任务书用**冻结的 PH-R2-R1 原始事件**复核，`allOk=true`：

| 序号 | 事件 | 统一 `unscaledTime` |
|---|---|---|
| 1 | evade（i-frames 生效，强化开启） | **7.187** |
| 2 | 反击 F 按下 | 7.515 |
| 3 | **第一次 contact** | **7.803**（+0.616s ≤ 0.85s 强化窗）→ 59.40 = 33×1.8 |
| 4 | 反击 complete | 8.047 |
| 5 | 第二次 F 按下 | 17.015（距首次 **9.500s**） |
| 6 | **第二次 contact** | **17.301** → 21.45 = 33×0.65，未强化 |

换算偏移 **4.358567s**，由"skill start"与"actual-evaded-attack"两条独立事件流各推一次，差 **1e-6s**；
帧号 703/717（翻滚）< 903（命中#1）∈[815,904]，3732（命中#2）∈[3647,3733] 提供无时钟印证。
数据：`recompute/twin-timeline.json`。

## 10. 失败历史（保留）

`failed/TIMEBASE-probe-data-error/` —— 第一版探针的**测试用例数据错误**：静默期用例把
`damageWindowStart` 设为评估点前 10s，导致 4.5s 硬上限先触发，4 例返回 `reason=hardcap`。
判据本身行为正确，是输入数据错。修正为 `startU=u` 并增加 `expectReason` 断言后全过。
完整原始证据 + `FAILURE_NOTE.json` 保留，未删除。

## 11. 未关闭风险

| ID | 等级 | 内容 |
|---|---|---|
| G-1 | 低 | 19 项完整矩阵未在 FIX DLL 下重跑（任务书限定只做 A–F 定向） |
| G-2 | 中低 | 4 个 Unity 构建输入文件被一次性归一化，按规则**未还原**；提交时是否纳入需负责人决定 |
| G-3 | 低 | `Assets/Resources.meta` 仍未跟踪（非本批产生，未删除） |
| G-4 | 低 | R14/R15（牵引完成、峰值位移）证据来自 PH-R2 DLL，本批未重新取证 |

## 12. 停止状态

- 未 `git add` / `commit` / `push`；未合并 `main`；未启动 `UX-PROGRESSION-03B`。
- 未修改产品源码：`git diff --name-status HEAD` 仅 `PlayerAcceptanceHarness.cs` 与 `player_acceptance_driver.py`。
- 未删除任何历史证据；`Evidence/PH-R2-R1-FINAL-AUDIT` 与旧报告原样保留。

## 13. 复现

```bash
cd /i/unity/WanxiangGuitu

# 构建输入闸门（只读；不构建时也可单独跑，用于确认当前状态）
python player_acceptance_driver.py preflight
python player_acceptance_driver.py postflight      # 期望 GATE=PASS

# 定向批次 A–F（真实 Player，约 100s）
python player_acceptance_driver.py fix

# 覆盖对账 / 保护面 / 历史证据（纯读，不启 Player）
python Evidence/PH-R2-R1-FIX/recompute/build_coverage_matrix.py
python Evidence/PH-R2-R1-FIX/recompute/recheck_protection.py
python Evidence/PH-R2-R1-FIX/recompute/recheck_history.py
```
