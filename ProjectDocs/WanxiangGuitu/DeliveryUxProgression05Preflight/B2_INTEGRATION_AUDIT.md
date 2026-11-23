# UX04-close A1–A9：B2 集成兼容性只读审计

**判断：在三个固定对象组成的完整历史树中，未发现必须修复才可进入下一轮隔离验证的源码、谱系或 Unity 导入域冲突；不构成集成发布放行。** 仍未验证固定目标树的干净 Unity 导入/编译、真实旧档迁移和两套 UI 的完整真实运行。三项新增 GUID 在仓库全树确实重复，但第二份均在非导入证据目录，不能说“全树零重复”，也不能当作 Unity 导入冲突。未合并、未 checkout/fetch、未改索引/分支/Git、未运行 Player/Unity、未写存档；审计只新增本文。

证据标识：[S] 固定 Git 对象的源码/树/元数据；[E] 已归档真实运行（只对其已知构建和场景有效）；[C] 本次离线复算；[D] 合同或设计要求；[H] 未验证。构建回执属于证据链记录，不是 Player 运行本身。

## 固定对象

| 角色 | commit | tree |
|---|---|---|
| main | 72db192a527bd256e2ba18cd7ab334d8334051da | 91222637ddf806fd543da93f95259503b0041d33 |
| UX04 / B1 | 95caf234256613d4a6e4f89a8ab0dc09c397c6b2 | e46232da0b87c97c39174fe58737c394a773b649 |
| UX04 / B2 | ae705b944b7d0fe851fbd395229dfc30ec636f5c | 64ded86dbabd22ff2e668445055d87fc7b102116 |

[S] 用实际对象与现有 origin 跟踪分支核对均一致；远端查询由上游已复核，本轮没有 fetch。B2 唯一父提交是 B1，B1 唯一父提交是 UX03 e18dc50cadba3b8f78deae83ff051360116cd；main 是两功能分支的祖先，main/B2 的 merge-base 即 main，左右独有提交计数 0/74。对该 main 不存在双边分叉；**不能把 B2 单提交直接搬到 main 当作完整 UX04**，那会跳过 B1 及其前序功能与合同。此处只是谱系判断，未执行集成。

## A1–A9

| 项 | 状态 | 核查结果 |
|---|---|---|
| **A1 未提交依赖** | 静态未见 | [S] B2 的三个新源/三个 meta 和五个修改源全部在提交对象；调用所需的 B1 门禁、容器、保存、战斗常量均在父链或 B2。工作区未跟踪的 Assets/Resources.meta 与既有证据目录不是这次结论输入；已跟踪 Assets/Packages/ProjectSettings 对 B2 无工作区差异。[H] 未在新干净工作区做 Unity 编译。 |
| **A2 文件重叠** | 已枚举 | [S] 比较 main→B1 与 B1→B2 的全路径交集，恰为 [AdventureLoadout.cs](<Assets/CombatPrototype/AdventureLoadout.cs>)、[CatInventoryPresenter.cs](<Assets/CombatPrototype/CatInventoryPresenter.cs>)、[ContainerInventoryView.cs](<Assets/CombatPrototype/ContainerInventoryView.cs>)；即 B1 单提交的三个产品文件。UX03 合同提交自身的九条产品路径与该 B2 增量交集为零。重叠在单祖先线上，属语义复核而非双边文本冲突；见下表。 |
| **A3 命名冲突** | 静态未见 | [S] 在 B2 完整 Assets/Packages 树定位新增顶层 B2AttackModel/B2AttackSnapshot/B2AttackEvaluation/B2EquipRole、B2Collection、B2Category/B2ItemStatus/B2SortKey/B2FilterSpec/B2FilterTabs/B2FilterState/B2InventoryQuery/B2SortView，未发现第二份产品定义；CatInventoryPresenter 的多处声明是既有 partial。ProjectDocs 历史 C# 快照不属于导入域；[H] 不替代真实编译诊断。 |
| **A4 Unity GUID** | 导入域无冲突；全树有发现 | [S][C] 仓库全树 B2 有七组重复（四组继承，三组新脚本与审计副本同 GUID）；B2 的 Assets/Packages 导入域按 guid 声明扫描无一重复，三组新 GUID 各恰有一个导入命中，Unity 场景/Prefab/asset 不引用这三组。详见 GUID 小节。不要将证据副本复制到 Assets 或 Packages。 |
| **A5 B1 金红不可分解** | 保留 | [D] 金/红不可分解但可按常规入库。[S] [AdventureLoadout.cs:354–391](<Assets/CombatPrototype/AdventureLoadout.cs#L354-L391>) 的 SalvageAllowed 要求 quality < Gold；Salvage 先拒绝金红，后判收藏/容量，移除装备和发矿只在成功后。两 UI 的直接调用点均入 Salvage；B2Collection.CanQuickDismantle 不能放宽 B1。DepositEquipment 不按品质拒绝。[E] B1 真实点击和读回证据见下。 |
| **A6 UX03 技能、攻击力、窗口合同** | 窗口/技能代码未变；攻击等价有界 | [S] UX03 的 AdventureCombat、GreatswordCombat、NewWeaponCombat、ScytheCombat、SkillTradeoffs、WeaponSkillExpansion、WeaponSkillPanel 对 B2 均不变。BeginAttack/SlotWindow 共用 AttackWindow（基础长矛节拍系数 1.30），技能窗/分段取实际 Motor 或技能定义，面板非第二套推导；回响适用性、聚能 +25%/+1s 与专属提示没有被 B2 改写。B2 将装备攻击移入 B2AttackModel：正常合法装备按 ID 取首项、排除 worn/overflow，盘内/主武器攻击加 Rig、Bag；备用正常不计。英雄仍是 base+装备+进度，长矛普通攻击再乘 1.25。[E][C] 历史 Mono 攻击位级对比见下。[H] 非法/损坏装备、完整 UX03 七武器运行未重测；装备防御改为 float foreach 累加，不能据攻击证据声称防御也位等价。 |
| **A7 B2 读档是否要求新增字段** | 不要求 | [S] [CombatSaveData.cs](<Assets/CombatPrototype/CombatSaveData.cs>)、[CombatSaveSystem.cs](<Assets/CombatPrototype/CombatSaveSystem.cs>)、[AdventureState.cs](<Assets/CombatPrototype/AdventureState.cs>)、[AdventureItems.cs](<Assets/CombatPrototype/AdventureItems.cs>) 在 B1→B2 无变化。读取仍走既有 envelope/校验/迁移；B2 用已存在的 GearItem.id、definitionId、quality、位置及装备状态。收藏是静态进程内 HashSet，筛选/排序选择和预览投影是内存态；没有保存 DTO、版本或迁移分支新增。uGUI/IMGUI 用同一内存查询，视图排序不是物理整理。 |
| **A8 旧档行为** | 历史与静态覆盖；用户档未验证 | [S] 既有加载、校验、旧版升级及默认化路径没有 B2 改动；冷进程收藏为空，不会从档内补读；同进程收藏按 ID 跨容器，非“每次读档必清空”。来源缺失仍可显示“来源未标注”。[E] B1 样本 v9 保留金红，早期 B2 隔离 v9 读回恢复 19 件、AP 33，并观察到从收藏 3 件到新进程 0 件；这不是目标用户旧档、也不是当前 B2 构建的端到端读档。[H] 未试真实旧档、所有历史版本、损坏主档/备份回退、写回及逆向迁移。 |
| **A9 完整树 PreviewAdd/Replace** | 静态接通；历史有界 | [S] 完整树有两 API、两 UI 入口、共享 ProjectEquipment/CanPlaceState/PlaceState；预览克隆且不写档，失败保留原状态，Apply 重新校验，显式 Replace 不猜被换 ID，Add 不驱逐旧件。槽/容器/盘位依法拒绝（如容器仅支持显式 Replace 且走既有存档事务），重复/空装备 ID 直接拒绝；与旧 UI 的 Compare 便捷入口不同，那个旧名字实际是 Add 查询而非自动 Replace。[E][C] 已归档 uGUI 六场景和 Float Gate 见下。[H] 未用固定整树重新构建/运行；历史证据不宣称终版 IMGUI、所有 Add 模式、容器提交和所有旧档全覆盖。 |

## 产品文件级矩阵

[S] 范围为 B1→B2 全部 11 条 Assets 路径（5 M + 6 A）；另有 1,663 条 Evidence 和 288 条 ProjectDocs 路径，均为新增，不是产品编译输入。无 Packages/ProjectSettings/场景/Prefab/原有 meta 改动。“重叠”以 main→B1 与 B1→B2 实际改动路径交集为准，blob 为 Git 对象前缀。

| 文件 | 变更 | B1→B2 blob | 与 main→B1 重叠 | 职责/复核点 |
|---|:---:|---|:---:|---|
| [AdventureLoadout.cs](<Assets/CombatPrototype/AdventureLoadout.cs>) | M | 1f57bf2a3→0ebb937c6 | 是 | 攻击/防御、纯预览/提交、分解权威门禁、整理 |
| [B2AttackModel.cs](<Assets/CombatPrototype/B2AttackModel.cs>) | A | —→dc551cf2c | 否 | 攻击模型、预览输入输出 |
| [B2AttackModel.cs.meta](<Assets/CombatPrototype/B2AttackModel.cs.meta>) | A | —→be22e5f23 | 否 | 脚本 GUID，见 A4 |
| [B2Collection.cs](<Assets/CombatPrototype/B2Collection.cs>) | A | —→981f7ebe8 | 否 | 会话收藏与分解/整理保护 |
| [B2Collection.cs.meta](<Assets/CombatPrototype/B2Collection.cs.meta>) | A | —→f71b727d0 | 否 | 脚本 GUID，见 A4 |
| [B2InventoryQuery.cs](<Assets/CombatPrototype/B2InventoryQuery.cs>) | A | —→1bf9fbaa7 | 否 | 查询、显示过滤及排序状态 |
| [B2InventoryQuery.cs.meta](<Assets/CombatPrototype/B2InventoryQuery.cs.meta>) | A | —→487ee033d | 否 | 脚本 GUID，见 A4 |
| [CampInventoryView.cs](<Assets/CombatPrototype/CampInventoryView.cs>) | M | 0ef47fa79→949dc1397 | 否 | 营地仓库列表查询 |
| [CampRuntime.cs](<Assets/CombatPrototype/CampRuntime.cs>) | M | ad52353cb→9556e4c37 | 否 | 仓库整理收藏保护、入库失败提示 |
| [CatInventoryPresenter.cs](<Assets/CombatPrototype/CatInventoryPresenter.cs>) | M | 5f1a8d7e5→68a45dd20 | 是 | uGUI 查询/收藏/预览与 B1 按钮门禁 |
| [ContainerInventoryView.cs](<Assets/CombatPrototype/ContainerInventoryView.cs>) | M | b605c1694→52e3ed5b5 | 是 | IMGUI 查询/收藏/预览与 B1 按钮门禁 |

## GUID 全树核查

[S][C] 对每个固定对象列出全部跟踪 .meta，再扫描所有以 guid: 开头且符合 32 十六进制字符的声明；转小写按值分组，最后单独限制 Assets/Packages 导入域。声明数不是文件数（有文本内多条声明），重复数按 GUID 组计。

| 树 | 全树 .meta 文件 | 全树 GUID 声明 | 全树重复组 | 导入域声明 / 重复组 |
|---|---:|---:|---:|---:|
| main | 586 | 599 | 4 | 587 / 0 |
| B1 | 758 | 771 | 4 | 759 / 0 |
| B2 | 764 | 777 | 7 | 762 / 0 |

B2 新增的同值组各两条，第二条位于 ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SUPPORTING_CURRENT（非导入域）。继承组 9ed16455a60fb9d418f3f53d14126018、5e5a34d08f09a3f419e9376f8a55623a、46eb43271f8b9e34caf397ded5aaf2d6、cc9a73f0eebda2d4a99d71abd3126caa 各三条，均在 DeliveryPlayer01/Evidence/Run/Gather 的三个 ExecutedDrivers 快照。

| GUID | 导入 Meta | 非导入快照 |
|---|---|---|
| f2e7d10e4f9a42788f9c15e6e4dd7e1e | [B2AttackModel.cs.meta](<Assets/CombatPrototype/B2AttackModel.cs.meta>) | [SUPPORTING_CURRENT/B2AttackModel.cs.meta](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SUPPORTING_CURRENT/B2AttackModel.cs.meta>) |
| c189b5d478364a7a81ca99738a8e0fa1 | [B2Collection.cs.meta](<Assets/CombatPrototype/B2Collection.cs.meta>) | [SUPPORTING_CURRENT/B2Collection.cs.meta](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SUPPORTING_CURRENT/B2Collection.cs.meta>) |
| bd256a15e7e944038fdb3180e0f08a8f | [B2InventoryQuery.cs.meta](<Assets/CombatPrototype/B2InventoryQuery.cs.meta>) | [SUPPORTING_CURRENT/B2InventoryQuery.cs.meta](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/SUPPORTING_CURRENT/B2InventoryQuery.cs.meta>) |

## 真实历史证据与复算边界

- **B1 [E][C]：** [分解原始观测](<Evidence/Runs04B1/UX04-B1-DISMANTLE-01/b1-observations.jsonl>) seq 5–17：白绿紫 13→12→11→10 件，铁矿 0→1→3→6（+1/+2/+3）；金红各自仍持有，矿不变；金件入库 0→1 并取回 1→0。[读回原始观测](<Evidence/Runs04B1/UX04-B1-READBACK-01/b1-observations.jsonl>) seq 12–14 两者均在档且 SalvageAllowed=False。支持历史 B1，不等于在 ae705b944 上重新点击。
- **早期 B2 [E]：** [READBACK](<Evidence/Runs04B2/UX04-B2-READBACK-FINAL/b2-observations.jsonl>)、[FAVSEED](<Evidence/Runs04B2/UX04-B2-FAVSEED-FINAL/b2-observations.jsonl>)、[RESTART](<Evidence/Runs04B2/UX04-B2-RESTART-FINAL/b2-observations.jsonl>) 三个历史运行属于产品 DLL 875cfea8… 构建。收藏种子 token 71ca8e6428fd，重启 token 9dea6a7f0eac，观测为 0 件且 tokenChanged=True；这是跨进程证据，不是进程内换档清除规则。
- **R2FIX [E]：** UI-A07 六个归档 run 共 641 checks、0 failed（96+96+80+186+94+89），四组可行、两组正确拒绝；均为 Mono 非 Editor。同一历史产品 DLL ab3d5ba4…、EXE b70442f9…、UI 驱动 0c44b9c6…；以 [accessory/run-manifest.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/run-manifest.json>) 和原始结果定位。[历史构建回执](<Evidence/Runs04B2R2FIX/FINAL-A02/_product/receipt/b2-product-build.json>) 记录 B1 为 baseline、隔离 Player 替换受控 Assembly-CSharp。三份新增 .cs 的 B2 blob SHA-256 与回执逐一相符（6e45644e… / 8ec17262… / 91f0036b…）；这建立了局部源身份关联，不能当作固定提交全部输入的干净 Unity 构建证明。
- **R2FIX [C]：** 从六份原始 result 的 before/after 本次复算单精度 base+loadout+progression 和 AP 差值；[accessory/result.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/result.json>) 61.5→73.5 / +12；[arms/result.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-arms/result.json>) 57.4500007629→65.8499984741 / +8.3999977112；[main/result.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-main/result.json>) 48→83 / +35；[board-insufficient/result.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-board-insufficient/result.json>) 240→240 / 0；[legal-swap/result.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-legal-swap/result.json>) 57.5→69.5 / +12；[illegal-swap/result.json](<Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/result.json>) 54.6500015259→同值 / 0。这里只复算已归档字段，非重演点击或完整几何 Oracle。
- **攻击位级 [E][C]：** [FINAL-A02 Float Gate 原始结果](<Evidence/Runs04B2R2FIX/FINAL-A02/UX04B2R2FIX-FLOAT-FINAL-001/result.json>) 7 组（顺/逆序、多物品、正值 Rig/Bag、相加顺序、重复输入），逐项比较 oldBits/newBits 得 24/24 相同。这是限定样本。静态发现 Defense 的旧 LINQ Sum 与新 float foreach 的累加精度不可默认等同；若防御也要求严格位级兼容，应单列门禁。

## 后续门槛（本轮不执行）

1. [H] 在获准后对固定集成候选做干净 Unity 导入/编译，记录 commit/tree、Assets GUID 域、Unity/程序集及 Player 哈希；不得带入工作区未跟踪资产或 ProjectDocs 快照。
2. [H] 在隔离副本上复验 UX03 七武器技能/窗口、B1 金红双 UI 与旧档读回；如合同要求，补装备防御位级用例。用有代表性的旧档及坏档/备份情形核验，不触及用户原档。
3. [H] 同一候选 build 覆盖 uGUI/IMGUI 的 Add/Replace、取消/容量不足/失效后提交、容器与主/备用槽；校验预览不改状态、仅成功提交才发生约定持久化。
