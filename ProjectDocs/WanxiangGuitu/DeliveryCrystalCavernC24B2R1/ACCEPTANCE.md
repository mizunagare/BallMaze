# CP06-C24-B2-R1 验收表

状态口径严格分层：`PASS-STATIC` / `PASS-MODEL` / `PASS-EDITOR` / `PASS-PLAYER` /
`NOT_RUN` / `INCOMPLETE` / `UNRESOLVED`。**不把多层结果汇总成无解释的 PASS**。

## 1. 验收明细

| ID | 要求 | 状态 | 证据 |
|---|---|---|---|
| R1-00-1 | 关联脚本只能对同一 Run 的原始事件 join | **PASS-STATIC + 自测** | `r1_correlate.py` 规则 R2；`r1-tool-selfcheck.json` 的 `cross_run_cannot_be_joined` |
| R1-00-2 | null 时间与缺失事件不能计入 PASS | **PASS-STATIC + 自测** | 规则 R3；`null_time_cannot_pass` / `missing_event_is_not_run` |
| R1-00-3 | 每项 check 列出输入行、表达式、结果 | **PASS-STATIC** | `c05-strict-checks.tsv`、`ring-player-checks.tsv`、`projection-cases.tsv` |
| R1-00-4 | B2 的 `c05-correlation.json` 与 10/10 声明原样保留 | **PASS-STATIC** | `b2-reevaluation.json` 的 `historicalFilesUntouched=true`；`git diff` 中无 B2 路径 |
| R1-00-5 | B1 的 C05 `INCOMPLETE` 原样保留 | **PASS-STATIC** | `b2-reevaluation.json` 的 `historicalStatusPreserved` |
| R1-01-1 | 同一 Run ID / PID / Build SHA 贯穿完整时间线 | **PASS-PLAYER** | `c05-strict-correlation.json`：18 事件、1 身份、0 null 时间 |
| R1-01-2 | Boss 初始 HP >50% 并进入 P1 前摇 | **PASS-PLAYER** | `warning` frame 2576，HP 195 > 180 |
| R1-01-3 | 前摇内经真实玩家攻击跨半血，不直接写 HP | **PASS-PLAYER** | `bossHealth` 事件含 `attackSource=AdventureCombat.Strike` 与调用栈；195→162 |
| R1-01-4 | 当前攻击按冻结 P1 参数释放 | **PASS-PLAYER** | `release` frame 2871：`phase=1 / Claw / 16` |
| R1-01-5 | 同次释放的玩家伤害有严格关联 HealthObservation | **PASS-PLAYER** | 同帧 2871、`correlationId` 相等；只读派生 join 键 |
| R1-01-6 | P1 Recovery 完整结束 | **PASS-PLAYER** | 独立 `recoveryEnd` frame 3208，`remaining=0` |
| R1-01-7 | Recovery 结束后才 Transition | **PASS-PLAYER** | `transitionBegin` frame 3209 > 3208 |
| R1-01-8 | Transition 后同一 Run 的下一招用 P2 参数 | **PASS-PLAYER** | `p2Release` frame 4067：`phase=2 / CrossLines / 20` |
| R1-01-9 | 同一 Run 关联总判定 | **PASS-PLAYER_SAME_RUN_C05（10/10）** | `c05-strict-correlation.json` |
| R1-02-1 | 内侧 / 外侧边缘接触 | **PASS-PLAYER** | `inner-edge` / `outer-edge`：`geometry=true`，HP 24→2 |
| R1-02-2 | 完全内侧 / 完全外侧安全 | **PASS-PLAYER** | `inner-safe` / `outer-safe`：`geometry=false`，HP 24→24 |
| R1-02-3 | 墙体遮挡：`geometry=true, clear=false`，HP 不变 | **PASS-PLAYER** | `wall`，HP 24→24 |
| R1-02-4 | 翻滚免疫：`evaded=true`，HP 不变 | **PASS-PLAYER** | `dodge`，HP 24→24 |
| R1-02-5 | 同一释放多帧只允许一次 Damage | **PASS-PLAYER** | 每样本 20–24 帧、`appliedCount<=1` |
| R1-02-6 | RingProbe 全字段原始记录 | **PASS-PLAYER** | 各 `ring-probes.jsonl` |
| R1-02-7 | 冻结参数未被事后调整 | **PASS-PLAYER** | 2.2 / 6.0 / 1.2 / 1e-4 / 22 逐样本一致 |
| R1-02-8 | 晶环矩阵总判定 | **RING_PLAYER_MATRIX_PASS（7/7）** | `ring-player-matrix.json` |
| R1-02-9 | 竖直带内 / 切线 / 带外、高度受击体 | **NOT_RUN** | 未构造可控高度受击体；B2 height 用例属 Editor/模型层 |
| R1-02-10 | `GameplayPaused` 冻结 / 顺延 | **NOT_RUN** | 未打开 UI 暂停面，无 pause-state 事件 |
| R1-02-11 | 死亡 / 离场 / Boss 死亡 / 卸载取消 | **NOT_RUN** | 未执行专门取消 run |
| R1-02-12 | 多 Collider 只允许一次 Damage | **NOT_RUN** | 所有样本 `bodyCount=1` |
| R1-02-13 | 原生键鼠 / 独立人工 / 纯包标题保护 | **NOT_RUN** | 本批未运行 |
| R1-03-1 | 晶环二维预警与竖直带信息差异的最小设计 | **DESIGN_ONLY / NOT_IMPLEMENTED** | `RING_WARNING_VISUAL_PROPOSAL.md` |
| R1-03-2 | 不改伤害 / 预警时长 / 命中逻辑 / 几何参数 | **PASS-STATIC** | 提案「明确不改动清单」；产品源码零修改 |
| R1-04-1 | C24 六项身份门禁 | **PASS-STATIC** | `projection-regression.json` 的 `identityGates` |
| R1-04-2 | alive/dead × collected/uncollected 四态 | **PASS-MODEL** | `aliveDeadCollectedCases` |
| R1-04-3 | 旧森林 / 遗迹 / C21 / C22 / C23 仍走通用分支 | **PASS-STATIC** | `oldLayouts.cases` |
| R1-04-4 | 查询不调用 Drop/Earn、不写存档、不推进 RNG | **PASS-STATIC** | `purity.projectWritesOnlyMaterialsAndOutGear` |
| R1-04-5 | 真实工厂对任意 uint 哈希逐位等价 | **PASS-MODEL** | `FACTORY_PAYLOAD_EQUIVALENT` + 源码归一化 |
| R1-04-6 | 未发现回归时不重跑全量旧地图评分矩阵 | **PASS-STATIC** | `fullOldMapScoringMatrixReRun=false` |
| R1-05-1 | 纯发行包不含任何验证驱动 | **PASS-EDITOR** | `PureBuild2`：`RuntimeInitializeOnLoads.json` 28 项 / 验证 0 |
| R1-05-2 | sidecar 驱动只注入隔离副本 | **PASS-EDITOR** | 各 `driver-injection.json` 的 `copyOnly=true` |
| R1-05-3 | Player 原始命令 / EXE SHA / Build SHA / PID / 日志 / 退出回执 | **PASS-PLAYER** | 各 `Evidence/Player/<run>/` |
| R1-05-4 | 用户文件 / 历史证据 / 真实存档保护 | **PROTECTION_PASS** | `protection.json`，违规 0 |
| R1-05-5 | 产品源码零修改（无 Player 证据显示产品缺陷） | **PASS-STATIC** | `git diff` 仅有 R1 新增文件；未提出最小修复 |
| R1-05-6 | 失败历史原样保留 | **PASS-STATIC** | `PureBuild1-DISCARDED/`、两次编译失败日志、A1/A2 失败 run、初始矩阵 |

## 2. 未解决 / 待复审重点

| 项 | 状态 | 复审建议 |
|---|---|---|
| R1-02 的竖直带高度样本 | `NOT_RUN` | 具备可控高度受击体的驱动后补跑；不得用 B2 Editor 结果冒充 Player |
| R1-02 的暂停与取消路径 | `NOT_RUN` | 需 UI 暂停面与取消场景的专门 run |
| R1-02 的多 Collider | `NOT_RUN` | 附加第二个 enabled 非 trigger 胶囊后补跑 |
| R1-03 可视化 | `DESIGN_ONLY` | 复审批准后才实现，且需独立 PASS-PLAYER 截帧验证 |
| 分析工具断言修正 | 已解释 | 初始 `4/7` 与修正后 `7/7` 两份结果均保留，请确认语义理解 |

## 3. 边界声明

- 本批**没有**重跑 B2 的 Unity Editor 几何契约；`PASS-EDITOR` 仅指本批纯包构建门禁。
- 本批**没有**把静态控制流、确定性模型或 Editor 运行冒充观测 Player。
- `pwsh` 缺失，历史编排链未运行；本批改用 `run_player.py` 等价独立启动，两者结果不混写。
- `PASS-PLAYER_SAME_RUN_C05` 与 `RING_PLAYER_MATRIX_PASS` 是**两个独立结论**，未合并成单一 PASS。
