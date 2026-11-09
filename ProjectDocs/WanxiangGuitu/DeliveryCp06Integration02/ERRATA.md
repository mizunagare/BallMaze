# ERRATA · CP06-INTEGRATION-02 统计矛盾勘误（R1-01 / R1-02）

> 本文件**只修正统计分类**，不改写任何原始证据、原始断言、原始日志或历史结论。
> 唯一权威来源：[RUN_LEDGER.csv](RUN_LEDGER.csv)（由 `Evidence/Tools/r1_ledger.py`
> 从 `Evidence/Player/<run>/` 原始文件机械生成，非人工录入）。
> 生成结果：[Evidence/Tools/r1-ledger-summary.json](Evidence/Tools/r1-ledger-summary.json)。

## 0. 两个口径（必须先读）

账本按 `phase` 列分成两段，两者互不覆盖：

| phase | 含义 | rows | PASS | FAIL |
|---|---|---|---|---|
| `R0` | R1 开工前就存在的 24 个原始 Player Run（R1-01 的核对对象） | 24 | 13 | 11 |
| `R1-02` | 本轮为「弓蓄势贯矢自然释放」新增的 8 个 Player Run | 8 | 4 | 4 |
| **合计** | **全部独立 Player Run** | **32** | **17** | **15** |

**R1-01 的结论（24 = 13 PASS + 11 FAIL）不变**，它对应 `phase=R0` 子集；
R1-02 追加的是**新证据**，不是对旧 24 个 Run 的重新分类。任何文档引用计数必须同时
说明口径（R0 / 全部）。

## 1. 最终值（单一来源，闭合校验通过）

| 项目 | R0 子集 | 全部（含 R1-02） |
|---|---|---|
| 独立 Player Run 总数 | **24** | **32** |
| 驱动 runId 唯一数 | **24**（无重复、无漏项） | **32**（无重复、无漏项） |
| `finalVerdict = PASS` | **13** | **17** |
| `finalVerdict = FAIL` | **11** | **15** |
| `finalVerdict = SKIP / NOT_RUN / INCOMPLETE` | **0**（遗迹采集步骤为 SKIP，但该 Run 整体判 PASS） | **0** |
| `isHistorical = yes`（被后续同类 Run 取代） | **13**（= 11 个 FAIL + 2 个被取代的 PASS：forest-loop-6、reward-loop-1） | **20**（= 15 个 FAIL + 5 个被取代的 PASS：forest-loop-6、reward-loop-1、bow-pierce-natural-4/-6/-7） |
| 分类合计 | 13 + 11 = **24** ✅ | 17 + 15 = **32** ✅ |

分类维度（互斥，全部 32；括号内为 R0 子集）：

| category | 计数 | 含义 |
|---|---|---|
| `ACCEPTED` | 16（12） | 通过，且为本模式的最终采信 Run |
| `ACCEPTED_SCENARIO_ONLY` | 1（1） | reward-loop-1：场景通过，但 `crafted=False`，**不代表制造成功** |
| `DRIVER_ERROR` | 8（4） | 验证驱动自身缺陷（R1-02 新增 4 个：bow-pierce-natural-1/-2/-3/-5） |
| `PRECONDITION_ERROR` | 5（5） | 摆位/前置条件不满足 |
| `PRODUCT_LEGAL_REFUSAL` | 2（2） | 产品按合同合法拒绝，非缺陷 |
| `PRODUCT_FAILURE` | **0（0）** | 候选产品缺陷：**零** |

## 2. 被勘误的旧声明（原文保留）

| 位置 | 旧值（原文） | 核对依据 | 最终值 | 修订原因 |
|---|---|---|---|---|
| `REPORT.md` §3.2 标题 | 「### 3.2 保留的失败历史（**14** 个 FAIL run，不改写）」 | 24 个 run 的 `complete.txt` + `assertions.tsv` + `Player.exit.json` | **11** | “14”无法由任何文件组合复算得出：该表格实际只列出 11 个 FAIL Run（forest-loop ～ -5 共 5、ruins-loop/-2 共 2、weapon-smoke-1、skill-smoke-1、skill-smoke-2、fail-paths-1 共 4），另列了 1 个 PASS Run（reward-loop-1）。属早期 Run 数量变化后正文未同步的算术漂移。 |
| `Evidence/INDEX.md` §1 标题 | 「## 1. 通过的关键 run（9 个模式，**12** 个 run）」 | 同上 | **13** | 该表含 12 行，其中 reward-loop-1 属“场景 PASS”，而行内文风暗示其为采信 Run；同时该表**漏掉**了 forest-loop-6（`complete.txt=PASS`、exit 0、29 PASS/0 FAIL），后者被误放进 §2 的失败表。 |
| `Evidence/INDEX.md` §2 标题 | 「## 2. 保留的失败历史（**12** 个 FAIL run，原样保留不改写）」 | 同上 | **11** | 该表 12 行中，forest-loop-6 的判定字段自己写着「PASS（英雄随后死亡为合法战果）」——它被放进失败表仅是排版归类错误，不是 FAIL。去掉它后为 11。 |
| `CURRENT_STATUS.md` §2c | 「24 个独立真实 Player run，**12 个通过、12 个历史 FAIL** 原样保留」 | 同上 | **13 通过 / 11 FAIL**（其中 13 个为历史尝试） | 沿用 INDEX 的 12/12 派生值；与 REPORT 的 14 亦互相矛盾。三处文档必须统一到 RUN_LEDGER。 |

三份文档此前的三组数字（14 / 12 / 12）互不相容，且都不等于任何可复算的组合；
本批统一为 **24 = 13 PASS + 11 FAIL**。

## 3. 差异定位（逐 Run）

| run | 旧归类位置 | complete.txt | exit | 断言 PASS/FAIL/SKIP | 正确判定 |
|---|---|---|---|---|---|
| forest-loop-6 | INDEX §2「失败历史」 | PASS | 0 | 29 / 0 / 0 | **PASS**（历史尝试，已被 forest-loop-7 取代） |
| forest-loop-7 | INDEX §1 | PASS | 0 | 29 / 0 / 0 | PASS（采信） |
| reward-loop-1 | INDEX §1（列在通过区） | PASS | 0 | 37 / 0 / 0 | **PASS（场景）**，`crafted=False` 如实保留；**不是**制造成功证据 |
| reward-loop-2 | INDEX §1 | PASS | 0 | 62 / 0 / 0 | PASS（采信，制造真实发生） |
| 其余 11 个 FAIL | INDEX §2 | FAIL | 2 | 含 ≥1 FAIL | FAIL（原样保留） |

REPORT §3.2 中把 `reward-loop-1` 写成「（非 FAIL，但 crafted=False）」一行，是 14 这个
数字的主要来源之一；本批将其移出失败集合，改记 `ACCEPTED_SCENARIO_ONLY`。

## 4. 未改动项（明确声明）

- 未删除、未移动、未重命名任何 `Evidence/Player/<run>/` 目录。
- 未修改任何 `assertions.tsv`、`complete.txt`、`failure.txt`、`Player.log`、`int-events.jsonl`。
- 未把任何 FAIL 改写成 PASS；未把 reward-loop-1 的 `crafted=False` 改写成 True。
- 未重跑三地区完整循环；未重建 Player。
- 历史结论（各根因分析）保持原文，仅在 REPORT §3 增加指向本账本的计数引用。

## 5. R1-02 追加的 8 个 Run（口径扩展，非重新分类）

R1-02 要求「真实松开输入自然释放」弓蓄势贯矢，因此新增 8 个独立 Player Run。
每一次都**单独计数一次**（含全部失败尝试，不删除、不合并）：

| run | complete | exit | 断言 PASS/FAIL/SKIP | 判定 | category | 被谁取代 |
|---|---|---|---|---|---|---|
| bow-pierce-natural-1 | FAIL | 2 | 32 / 5 / 0 | FAIL | `DRIVER_ERROR` | natural-8 |
| bow-pierce-natural-2 | FAIL | 2 | 20 / 1 / 0 | FAIL | `DRIVER_ERROR` | natural-8 |
| bow-pierce-natural-3 | FAIL | 2 | 40 / 1 / 0 | FAIL | `DRIVER_ERROR` | natural-8 |
| bow-pierce-natural-4 | PASS | 0 | 55 / 0 / 1 | PASS | `ACCEPTED` | natural-8 |
| bow-pierce-natural-5 | FAIL | 2 | 56 / 1 / 0 | FAIL | `DRIVER_ERROR` | natural-8 |
| bow-pierce-natural-6 | PASS | 0 | 55 / 0 / 0 | PASS | `ACCEPTED` | natural-8 |
| bow-pierce-natural-7 | PASS | 0 | 55 / 0 / 0 | PASS | `ACCEPTED` | natural-8 |
| **bow-pierce-natural-8** | **PASS** | **0** | **56 / 0 / 0** | **PASS** | `ACCEPTED` | — （采信） |

四项 `DRIVER_ERROR` 的根因（均为驱动缺陷，**不是**产品缺陷）：

1. natural-1：驱动用敌人自身 Y 取射击点，把英雄放到地形以下（`pierce-spawn y=-3.44`），
   弹体立即撞击地面；且冷却断言被放在 5s 飞行等待之后，11s 冷却被读成 0。
2. natural-2：驱动断言弓 Muzzle 位于胸口（+0.6m），实际产品弓弦源高度约 +0.30m。
3. natural-3：第二次施放前未重新 `PlayerInput.Focus(true)`，11s 冷却后按键不再产生 Down 边沿。
4. natural-5：生命周期等待未考虑产品在 `Time.timeScale==0` 时**按设计冻结弹体**
   （升级选卡/死亡 Freeze），因此等待超时；同时重复命中用了跨弹体全局计数。

## 6. 本轮发现的技术性口径问题（已修正，附证据）

| 问题 | 影响 | 处理 | 依据 |
|---|---|---|---|
| bow-pierce-natural-1～-6 的 `run-summary.json` 由旧 schema 写出，**没有 `exitCode` 字段**，`verdict` 只有 `DRIVER_FAILED` / `OBSERVATION_COMPLETE` | 账本初版把这 6 个 Run 误判为 `INCOMPLETE`（R1-02 出现 `INCOMPLETE:2`） | `r1_ledger.py` 增加 `exit_code_of()`：`run-summary.json` 缺失时回退读取启动器写出的 `Player.exit.json`（同为原始证据） | natural-4/-6 的 `Player.exit.json` 均为 `exitCode=0, forcedTermination=false, timedOut=false` |
| 早期 6 个 Run 的 `pid` 同样不在 `run-summary.json` | 账本 `pid` 列为空 | 同步回退读取 `Player.exit.json.pid` | 同上 |
| `cast2Window` 在命中到达前关闭 | natural-6 出现误导性 `cast2DistinctTargets=0[]` | 将窗口关闭移到命中/伤害断言之后 | natural-7/-8 该字段为 `1[enemy:2]` / `2[enemy:2/enemy:4]` |
| 产品在升级选卡时冻结弹体（`Time.timeScale=0`） | natural-5/-7 的生命周期等待只能以「产品冻结」收尾 | 驱动改用产品自身 `HeroProgression.SelectChoice` 完成选卡后继续等待 | natural-8 有 `lifecycle-end`（冻结，remaining=1）与 `lifecycle-end-resumed`（remaining=0）两条事件 |

以上修正均**不涉及产品源码**，仅改验证驱动与账本生成器；旧 Run 的原始文件一律未改写。
