# CP06-INTEGRATION-02 · 验收（INT02-01 ～ INT02-06）

> 验收基于**全部独立隔离的真实 Player run**，计数唯一来源 [RUN_LEDGER.csv](RUN_LEDGER.csv)：
> **32 个 Run = 17 PASS + 15 FAIL**（`phase=R0` 24 个：13 PASS / 11 FAIL；R1-02 新增 8 个：4 PASS / 4 FAIL）。
> 全部历史 FAIL / NOT_RUN 保留原判不改写；旧统计（14/12/12）的勘误见 [ERRATA.md](ERRATA.md)。
> 「SKIP」= 该步骤在候选中按设计不适用（有源码级依据），其余步骤仍真实执行。

## INT02-01 候选纯发行构建身份 —— **PASS**

| 验收点 | 结果 | 证据 |
|---|---|---|
| 候选 SHA | `2964ad7413d2644f23c12a8c82e1d439e2884a01` | `git log`（tip 提交 `2964ad741`） |
| 纯发行构建（Dev/Profiler/Debug=0） | PASS | `WindowsRelease.asset` + release sidecar |
| 可执行 SHA256 确定性 | `001aeebf…`（与历史 C22/C24B 纯构建一致） | [PLAYABLE_CANDIDATE_BUILD.md](PLAYABLE_CANDIDATE_BUILD.md) |
| 隐私门禁（Bee 唯一匹配/遥测全禁） | PASS | 同上 §4 |
| 纯构建零验证注入 | PASS | 同上 §5 |

## INT02-02 三地区各一条真实完整出征循环 —— **PASS（遗迹采集 SKIP）**

| 地区 | run | 循环完整性 | 战斗 | 采集 | 撤离结算 | 再出征 |
|---|---|---|---|---|---|---|
| 森林 | forest-loop-7 | PASS | 45→0 击杀 33 伤害 | Wood 4（拾取/拒重） | Extracted+commit+ack | 新 runId |
| 古代遗迹 | ruins-loop-3 | PASS | c1:guard 60→0 | **SKIP**（无矿脉，源码依据） | Extracted+commit+ack | 新 runId |
| 水晶洞窟 | cavern-loop-1 | PASS | watcher 60→0 | Ore 6（拾取/拒重） | Extracted+commit+ack | 新 runId |

全部经真实业务入口，无场景直载 / teleport 伪造循环（摆位仅限位姿）。

## INT02-03 跨地区状态切换 + 跨进程在途恢复 —— **PASS**

| 验收点 | 结果 | 证据 run |
|---|---|---|
| forest→ruins→cavern 连续切换，状态无串扰 | PASS（44 断言） | cross-region-chain-1 |
| 每区独立 runId / 区域身份 | PASS | 同上 |
| 进程 1 中途存档、进程 2 真实 Continue() 恢复同一 run | PASS（runId/region/instance/seed 全一致） | xproc-1 + xproc-2 |
| 跨进程存档字节一致 | PASS（SHA256 清单 diff 为空） | xproc-2/storage-copy-manifest-* |
| Boss 真实交战 + 合法撤离 | PASS | cavern-boss-1 |

## INT02-04 七武器与八技能真实输入组合 —— **PASS**

| 验收点 | 结果 | 证据 run |
|---|---|---|
| 7 武器 select+Strike+released | PASS×7 | weapon-smoke-2 |
| 8 技能双槽真实施放（两地区） | PASS | skill-smoke-3 |
| 弓蓄力（Phase=Charging） | PASS×2 地区 | skill-smoke-3 |
| 法杖符阵真实弹体 spawn | PASS×2 地区 | skill-smoke-3 |
| 技能共享冷却为真实产品行为（历史 FAIL 保留） | FAIL→PASS（驱动等待冷却） | skill-smoke-1→3 |
| **弓蓄势贯矢真实松键自然释放**（半蓄力 + 满蓄力） | **PASS×2 发**（56 断言 0 FAIL） | **bow-pierce-natural-8** |
| **弹体贯穿合同**（单发命中多目标、同目标不重复、≤3 目标上限） | **PASS**（chain=2：`enemy:2`+`enemy:4`，perProjectileRepeats=0） | **bow-pierce-natural-8** |
| **弹体生命周期 + 真实冷却** | **PASS**（两发均销毁；release 后 remaining=10.17s，冷却期施放被拒） | **bow-pierce-natural-8** |
| 弓手动取消（历史证据，保留不改写） | PASS（历史） | skill-smoke-3 |

## INT02-05 奖励→制造→结算→回营→再次出征 —— **PASS**

| 验收点 | 结果 | 证据 |
|---|---|---|
| 双地区采集（Wood4+Stone5+Ore3+Crystal4） | PASS | reward-loop-2 |
| 仓库原子入账（final==carried，四种材料） | PASS | reward-warehouse-* |
| 重复提交拒绝 | PASS | reward-no-duplicate-commit |
| **真实制造白品剑**（原子扣料） | PASS（items 8→9） | reward-craft-sword-white |
| 再次出征新 runId | PASS | reward-redeploy |

## INT02-06 失败路径与用户文件保护 —— **PASS**

| 验收点 | 结果 | 证据 |
|---|---|---|
| 远离出口撤离被合法拒绝 | PASS（refused=True） | fail-paths-2 |
| 真实致死→Death 结局→commit→区域卸载 | PASS | fail-paths-2 |
| 死亡结算确认（ack）后恢复再出征 | PASS（新 runId） | fail-paths-2 |
| 存档隔离（不经 AppData） | PASS（全部 32 个 run） | fail-isolated-save |
| 用户文件零改动 | PASS（git 仅新增本交付目录） | REPORT.md §4 |

## R1 追加验收项 —— **PASS**

| 验收点 | 结果 | 证据 |
|---|---|---|
| 24 个原始 Run 唯一分类、互相矛盾的三处统计（14/12/12）已勘误 | PASS（24 = 13 + 11，runId 唯一 24） | [RUN_LEDGER.csv](RUN_LEDGER.csv)、[ERRATA.md](ERRATA.md) |
| 构建/工具尝试与 Player Run 分离 | PASS（20 条 0 计入 Player Run） | [NON_RUN_ATTEMPTS.csv](NON_RUN_ATTEMPTS.csv) |
| 森林 Run ID 来源可追溯 | PASS（**DIRECT**：`int-events.jsonl:2 productRunId=2582537b…`） | [FOREST_RUN_ID_PROVENANCE.md](FOREST_RUN_ID_PROVENANCE.md) |
| 弓蓄势贯矢自然释放（真实输入、非 API 调用） | PASS（`cancelDelta=0`，两发各唯一 release/spawn） | bow-pierce-natural-8 |
| 计数跨文档一致（REPORT / ACCEPTANCE / INDEX / CURRENT_STATUS / 账本） | PASS（四处均为 32 = 17 + 15；R0 子集 13 + 11） | 本文件各节 + `Evidence/INDEX.md` |

## 限制（不因本批关闭）

- 遗迹无矿脉（产品事实，SKIP）：待产品侧决策是否给遗迹提供资源。
- 人工试玩 / 观感 / 最终打击感：`NOT_RUN`（与历史口径一致）。
- 弓蓄力自然释放已通过（半蓄力 + 满蓄力）；仍未覆盖「蓄力过程中被敌人打断/中断」的组合路径，
  以及人类玩家的主观手感评估。
