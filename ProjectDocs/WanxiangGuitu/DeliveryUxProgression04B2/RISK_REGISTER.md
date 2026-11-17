# UX-04-B2 · RISK_REGISTER

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

| ID | 风险 | 状态 | 事实/缓解 | 标记 |
|---|---|---|---|---|
| R-01 | 等价重构改变实时攻击力（D-24 回退） | **已消除** | `Attack`/`Defense` 委托同一纯函数；黄金矩阵 24 行逐位相等 + `G0 liveMatch=True` | [S][E] |
| R-02 | 出现第二套业务逻辑 | **已消除** | 实时属性、预览、比较、黄金矩阵共用 `B2AttackModel.ComputeAttack`；sidecar 内的 `LegacyAttack` 是独立测试 oracle，非产品逻辑 | [S] |
| R-03 | 预览修改实际装备/存档 | **已消除** | 全部在 `Clone()` 副本；`G7-preview readOnly=True`；无 `SaveProgress` 调用 | [S][E] |
| R-04 | 装备系数被改（0.5 / 0.35 / 1.25 / Power） | **已消除** | 相关文件零变化；Player 实测 66 / 46.2 / 85 | [S][E] |
| R-05 | IMGUI 与 uGUI 整数 filter 语义分歧 | **已消除** | 单一 `B2FilterState` + 单一 `SpecForTab` + 单一 `Matches`；两路径 8/8 页签一致 | [S][E] |
| R-06 | 新增来源/地区字段或改写 origin 校验 | **已消除** | 来源仅用 `origin`+`originRunId`；`AdventureState`/`AdventureFlow.Supplies`/`AdventureValidation` 零变化 | [S] |
| R-07 | 收藏被持久化 / Schema 迁移 | **已消除** | 普通进程内 `HashSet<string>`；跨进程实证 token 改变且 0 件收藏 | [S][E] |
| R-08 | 收藏装备被快速分解 | **已消除** | `Salvage` 单点门禁；`canQuickDismantle=False stillOwned=True ore=0` | [S][E] |
| R-09 | 批量整理误删收藏 | **已缓解** | `SortBag`/`SortWarehouse` 前置 `BatchPreservesFavourites` + 数量校验；二者本就只重排 | [S][D] |
| R-10 | 收藏阻断正常入库/取出/穿戴 | **已消除** | 收藏不参与任何存取/穿戴判定；金装备 deposit/withdraw PASS | [S][E] |
| R-11 | 重复件被自动合并/删除 | **已消除** | `DuplicateHints` 只计数、只显示「仅提示，不合并」 | [S] |
| R-12 | 破坏性操作缺二次确认 | **已消除** | IMGUI 新增两段式，uGUI 既有两段式保留并叠加收藏门禁 | [S][E] |
| R-13 | 容量 200 被改 / 容器结构被改 | **已消除** | 常量与两处校验零变化；`CapacityLine` 明确区分 96/48/200 | [S][E] |
| R-14 | 仓满静默失败 | **已消除** | 逐分支明确原因；Player 实测「永久仓库已满（200/200 件）…装备未移动」 | [S][E] |
| R-15 | 热键/PlayerAction 被改 | **已消除** | `PlayerBindings.cs`/`PlayerInput.cs` 零变化；新增能力只用页面按钮 | [S] |
| R-16 | 重做 UI 布局 | **已消除** | 新增内容写入既有 `Rect`；仅 IMGUI 顶部同一行内拆分为标题+容量行 | [S] |
| R-17 | B1 金红门禁被覆盖 | **已消除** | `SalvageAllowed` 未改且仍为第一道门；`uGUI-B1-Gold/Red` PASS | [S][E] |
| R-18 | 构建过程修改 ProjectSettings / 场景 / Prefab | **已避免** | 采用全源码 Roslyn 重编译 + 隔离副本；未运行 Unity batchmode；终检 `git status` 为空 | [S] |
| R-19 | 用户真实存档被写入 | **已避免** | 每次 Run 全新 `-wanxiang-storage-root`；原始 Acceptance 构建 DLL 未变 | [S] |
| R-20 | sidecar 污染正式构建 | **已避免** | 驱动 DLL 只注入 gitignored 隔离副本；原 `Builds/WanxiangGuitu.Acceptance` 未注入 | [S] |
| R-21 | 验收伪造成立 | **已避免** | 所有被测动作经真实鼠标事件（uGUI: InputSystem；IMGUI: 原生 OS）；未直接调用底层方法冒充动作 | [S][E] |
| R-22 | 失败证据被覆盖/删除 | **已避免** | `UGUI-01` FAIL 原样保留；全部 18 个运行目录未删除；修正后使用新 Run ID | [S][E] |
| R-23 | IMGUI 输入无法被验收 | **已解决（有过程记录）** | InputSystem 事件不到达 IMGUI `Event.current`；改用 `user32.dll` 原生 OS 鼠标，`IMGUI-FINAL` 8/8 页签状态正确；不确定的 `IMGUI-01/02/03` 如实标记 | [S][E] |
| R-24 | 黄金矩阵过于平凡（结果全相同） | **已排除** | 数值覆盖 8/19/43/78/132、33→157、85、99、79.2、39、66、46.2；备用/Overflow/Worn 恒 0 但均逐位比较 | [C][E] |

## 遗留风险与未验证假设 [H]

| ID | 遗留项 | 影响 | 建议 |
|---|---|---|---|
| H-01 | 仅验证 1280×720 / D3D12 窗口 | IMGUI 原生点击坐标依赖 `CombatUI.Scale` 与窗口客户区原点 | 未来批次补高 DPI / 其他分辨率回归 |
| H-02 | 仓满由 `CampRuntime.Restore` 预置（准备阶段），非 200 次真实点击 | 仓满「拒存」动作本身是真实点击，但填满过程是准备 | 如需端到端可补长链路 Run |
| H-03 | 批量整理保护未做「故意构造缺件」的故障注入 | 保护为源码不变量，未实测拒绝分支 | 未来批次补负向注入测试 |
| H-04 | `Board` 预览为「假设放置成功」，实际需 `CanPlace` | 预览可能高估可达 Δ | 在 UI 上标注或补 `CanPlace` 联动 |
| H-05 | 未运行 Unity `BuildPlayer` 做二进制对照 | 全源码 Roslyn 重编译依据 Unity Bee `.rsp` | 若允许临时写 ProjectSettings，可补一次官方构建对照 |
| H-06 | 未穷举所有 affix / 容器组合 | 等价性由共享表达式结构保证 | 可扩矩阵，非阻断 |
| H-07 | `B2FilterState` 为进程内静态，重启回默认 spec | 与「会话内」语义一致，未专门断言 | 未来批次可补跨进程 spec 断言 |
| H-08 | 本轮未提交 / 未推送 / 未合并 main | 按停止条件刻意保持 | 待负责人复审后决定 |

## 结论 [D]

所有**阻断级**风险（R-01~R-24）均已通过源码事实或真实 Player 证据消除；剩余为 H-01~H-08 的非阻断遗留假设，不影响 B2-01~B2-05 功能验收结论。
