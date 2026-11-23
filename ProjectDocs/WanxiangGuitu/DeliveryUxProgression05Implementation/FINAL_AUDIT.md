# UX-05 v10 最终独立审计

## R2_FINAL_CLOSURE 当前结论（2026-11-20）

**CONDITIONAL_PASS。F-01关闭；F-02仍未关闭。** 经负责人另行授权，本次补齐最终NoDefine/Release真实运行：两个构建分别启动、原生输入读取v10的128条历史、正常退出及新PID重启后再读，4条PASS；另有2条仪器中断保留。没有构建或产品代码修改。原159条Run分类、4142个历史文件及5404个既有索引项均不变。

Driver追溯涵盖Git可达/不可达对象、Builds、历史Evidence、工具/缓存源码、PDB、响应文件、日志及压缩归档。114条对应18个SHA均未恢复精确脚本；涉及31条R1 PASS的关联缺口继续保留。追溯完成不等于缺口关闭，不据此给整体PASS。

| 当前项目 | 判定 | 依据 |
|---|---|---|
| Git/产品/Schema/保护 | PASS | 保持接手源码与Index，未改真实存档或历史证据 |
| 最终NoDefine/Release运行 | PASS | 新矩阵4条正常运行，原生退出全0；真实历史页面及新PID重读 |
| 构建排除门禁 | PASS | 原最终三类SHA不变，纯构建无Harness/探针/UX_ACCEPTANCE，未注入 |
| ObjectiveHistory/迁移/Pending/双UI/D-20/D-23 | PASS（既有验证范围） | 原始证据重新哈希/关键状态复核，未重跑全矩阵；纯构建只补最小读取路径 |
| Driver归档来源 | CONDITIONAL_PASS | 114条未找回，不能精确复现；不改旧分类 |
| 整体 | CONDITIONAL_PASS | 仅F-01闭环，F-02等待负责人复审 |

详见 [收尾报告](R2_FINAL_CLOSURE.md)、[Driver恢复表](DRIVER_ARCHIVE_RECOVERY.csv)、[纯构建Run矩阵](NODEFINE_RELEASE_RUN_MATRIX.csv)、[新证据索引](EVIDENCE/R2/INDEX.json)。运行期间既存周期/失焦/退出保存导致主档SHA与revision变化，历史、committedRuns及非camp的Profile业务字段保持不变，不声称整档全程零变化。环境仍仅1280×720/DPI96。

以下为初次只读审计原文，保留当时发现与分类；其中“最终纯构建无对应Run”描述的是原159条历史集合，由本节新增证据更新，不再作为当前F-01状态。初审构建/Run对账表保持历史快照，不回写旧Run。

## 初审原文（历史快照）

**CONDITIONAL_PASS。** 只读审计完成。关键历史、迁移、回归及当前 Acceptance 双 UI 证据可复核，未发现本轮需要修代码的已证产品缺陷；整体最终发行验收仍有 F-01、F-02 两项证据条件，不能将 IMGUI-R2 PASS 扩大成整体 PASS。

审计日期：2026-11-20。本轮仅创建本报告、FINAL_RISK_REGISTER.md、FINAL_BUILD_IDENTITY.tsv、FINAL_RUN_RECONCILIATION.csv。没有执行会写入证据/result/INDEX的旧复算工具，改用进程内只读解析、哈希和断言；没有代码或存档修改，没有构建、Editor/Player或新Run。

## 最终状态

| 项目 | 判定 | 可证范围 |
|---|---|---|
| Git | PASS | 分支/HEAD符合任务，暂存区为空，既有未提交修改保留；远端独立实测 |
| Schema | PASS | 每条历史严格六字段；容器和旧覆盖标识属于既定设计；无新增槽位/地区收益字段 |
| 迁移 | PASS | v9到v10、八类故障恢复及含分页Pending夹具；原有字段投影一致；仅代表所列切点 |
| ObjectiveHistory | PASS | 历史构建的129次真实业务提交、128留存、永久去重、UTC冻结及冷读可复核；有受控导航边界 |
| IMGUI | PASS | 当前Acceptance A02，24次原生历程操作，七页/末条/关闭及无穿透 |
| uGUI | PASS | 同一存档查询，24次原生历程操作，与IMGUI的17对结果一致 |
| 构建 | CONDITIONAL_PASS | 最终三类构建身份/发行排除门禁通过；最终NoDefine/Release SHA无对应Player Run |
| 历史证据 | CONDITIONAL_PASS | 4142旧文件及全部5404索引项字节匹配；历史启动脚本身份与少量生命周期回执不完备 |
| 保护 | PASS | 差异在授权范围；本轮除四份交付外零既有文件字节变化，Git Index不变 |
| 整体 | CONDITIONAL_PASS | F-01、F-02需负责人复审；不是仅显示环境覆盖不足 |

## Git实测和已有修改

- 仓库：mizunagare/BallMaze；分支：feature/ux-progression-05-objective-history。
- HEAD：`ae705b944b7d0fe851fbd395229dfc30ec636f5c`；父提交：`95caf234256613d4a6e4f89a8ab0dc09c397c6b2`。HEAD是B2基线，v10成果仍在未提交工作区，不能将HEAD SHA当产品DLL身份。
- 当前11个已跟踪修改、144个合并显示的未跟踪项/目录均为接手状态。11个修改文件为AdventureFlow.Objectives.cs、AdventureFlow.UI.cs、AdventureFlow.cs、AdventureRules.cs、AdventureState.cs、AdventureValidation.cs、CombatSaveSystem.Entry.cs、CombatSaveSystem.Location.cs、CombatSaveSystem.cs、GameEntry.cs、ObjectiveCatalog.cs。
- SaveSchemaMigration.cs及meta是既有新增实现；AGENTS.md、Assets/Resources.meta及其他历史交付/证据目录也是既有未跟踪内容，没有归因于本轮。
- 本轮 `git ls-remote --heads origin feature/ux-progression-05-objective-history feature/ux-progression-04-b2 main` 成功：UX-05远端分支不存在；B2=`ae705b944b7d0fe851fbd395229dfc30ec636f5c`；main=`72db192a527bd256e2ba18cd7ab334d8334051da`。不据此推断合并关系或授权推送。
- sparse-checkout已启用，包含Assets/Packages/ProjectSettings及既有文档路径；本轮未改配置。未fetch、reset、restore、add、commit、push或merge。

## 全量Run对账 [C]

按 EVIDENCE/R1/original-runs.csv 的Run ID集合分组，不能按当前CSV前68行切片。完整核验159条：任务指定68+79+最终3条共150条，另保留R2中间9条。Run ID/PID均匹配，无冲突。已读取Run目录1617个JSON、3754条JSONL记录，解析错误0；并另行解析关键共享隔离根的存档、分页、入口与访问日志。

| 分组 | 原始分类及数量 |
|---|---|
| 原始68 | PASS59；SUPPLEMENTAL_STOPPED1；FAIL_LAUNCH1；EXPECTED_NEGATIVE_BLOCKED1；FAIL2；PROCESS_CUT_WITNESSED2；OBSERVED_STARTUP_ONLY2 |
| R1新增79 | PASS43；FAIL_TIMEOUT4；PROCESS_CUT_WITNESSED11；INCOMPLETE_EVIDENCE5；FAIL15；EXPECTED_NEGATIVE_BLOCKED1 |
| R2全部12 | PASS4；FAIL2；FAIL_DRIVER1；PASS_INTERACTION_INCOMPLETE_EXIT3；INTERACTION_OBSERVED_AUTOSAVE_ACTIVE1；INCOMPLETE_INPUT_TOOL1 |

全矩阵保留106条原记录PASS及所有非PASS类别，不将其解释成最终产物通过率。43条R1新增PASS的原始status/PASS布尔、输入和结果均已读取；其中31条启动脚本仅能确认历史哈希，未找到匹配的当时脚本副本，不能声称43条驱动源码重现链均完整。

159份EXE身份有匹配产物；产品DLL为156份原路径匹配、3份在保留目录匹配。三份NoDefine旧路径已被后续构建复用，旧DLL在Preserved目录仍与原哈希一致，没有误报其历史运行使用了新DLL。[逐Run对账](FINAL_RUN_RECONCILIATION.csv)列出实际位置。

Driver哈希按真实含义区分：15条为sidecar DLL且当前字节匹配；24条为可匹配源码/启动脚本；6条为无Driver纯启动（N/A）；114条仅留历史启动脚本哈希，相关交付和构建区搜索未找到匹配源码。多数集成探针编入产品DLL，其执行代码的DLL哈希仍可验证，但不能代替外部启动脚本身份。

多数使用manifest.json，没有另名run-manifest.json。部分结果位于probe/result.json、包含输入的root/result.json或R2的verified-result.json；后者为宿主复算结果，原始产品状态在actions/outcomes/observer。对账保留实际路径和SHA，不补造文件名。六份纯启动退出码来自review-result，列为派生回执；另12条无原生宿主退出回执，其中CONTRACT-A02原分类PASS，其余为失败/停止/不完整尝试，不倒填退出0。每行audit_completeness_status只描述证据完备性，不改recorded_class。

## Schema和实际事务 [S]

AdventureState.cs的ObjectiveHistoryEntry仅声明六个字符串字段：

`runId / objectiveId / regionId / completedAtUtc / committedAtUtc / displayNameSnapshot`。

SettlementId为派生属性RunId+":terminal"；未新增持久化SettlementId、CompletionType或DefinitionVersion。Profile的objectiveHistory容器、objectiveHistoryLegacyUnknown覆盖标识和Pending plan中的同型镜像已列入原文件矩阵，不误计为每条历史的第七业务字段。未见新增技能槽、地区等级/收益、品质格位或D-24字段。

真实顺序为 AdventureFlow.LockOutcome → CaptureObjectives → CaptureCompletedObjective → AdventureRules.Plan → FreezeHistoryCandidate → Pending保存 → CommitSettlement → 同一候选Profile/committedRuns/收益发布 → 独立回读 → UI查询。核验源码：AdventureFlow.Objectives.cs、AdventureFlow.cs、AdventureRules.cs、CombatSaveSystem.cs、SaveSchemaMigration.cs和AdventureValidation.cs。

CompletedAtUtc在含成功撤离的终局达成点采样，不是首次打开第三个宝箱的时间；CommittedAtUtc是首次合格计划时间，不是实际落盘时间。Pending恢复/重试复用记录，不重新运行求值器生成历史。VerifyProfileWire以键白名单约束每项六字段；UTC要求28字符、7位小数、Z结尾。本审计使用原始存档字符串，不用二级摘要日期转换代替精确比较。

## 历史与存档关键路径 [P][C]

- CAPACITY-A02有387条宝箱接受/使用事件、129条撤离、129条默认槽事件、129条Pending冻结记录。主档校验正确；128条历史逐字段等于冻结序列第2至129项；committedRuns逐项等于全部129个Run ID。
- 第128/129条边界最旧项从e1d4120981c9482899f63c1ce465abf6变为4065e53c469e447bba62d62daf759e28；旧Run仍在committedRuns。
- R1-REPLAY-A01中旧Run被真实Plan入口拒绝；前后主档和现存夹具SHA均为 `17B41C690B3A53A8FDC04342F9F78B457D3A0D22F9368C2FEAB64646B1488845`。
- PENDING-STOP/RESUME、R1-SAVE-READBACK、R1-SAVE-STALE的冻结事件与最终存档六字段完全一致，Committed中对应Run只出现一次。读取受阻/过期世代后阻止再次确认，恢复后发布原计划；profileEqualsFrozenPlan原断言保留。
- CAPACITY-REOPEN冷进程及R2七页均为20×6+8。R2混合地区/并列UTC属于受控查询夹具，不是本轮再生成128次目标的证明。
- 容量链调用真实出征、宝箱Interact、撤离及提交业务，但使用RestorePosition受控导航和撤离timeScale=8。未见容量链直接写入历史集合；这是Mono业务结算证据，不宣称129局Windows原生按键行走。显示夹具和同Run冲突负例的数据投影不用于证明真实完成。
- 原收益、历史和committedRuns同一Committed候选发布；领取事务独立。永久去重不扫描最近128条。发布不确定时停在SettlementNeedsRead，不以SaveProgress=false推断磁盘未改变。

迁移复算：

| 故障点 | 故障/恢复Run后缀 | 核验 |
|---|---|---|
| 归档前 | A3 / A3-RECOVERY | 原源/归档相符，恢复成功 |
| 分页写前 | P3 / P3-RECOVERY | 同上 |
| 分页写后 | Q3 / Q3-RECOVERY | 同上 |
| 候选写前 | C3 / C3-RECOVERY | 同上 |
| 候选校验错误 | CHECKSUM / CHECKSUM-RECOVERY | 候选拒绝，后续恢复 |
| 原子替换前 | REPLACE / REPLACE-RECOVERY | 未提前发布，后续恢复 |
| 原子替换后 | AFTER2 / AFTER2-RECOVERY | 新版可读，未自动Commit旧Pending |
| 回执丢失 | RECEIPT2 / RECEIPT2-RECOVERY | 持久结果读回，重复读取复用 |

每例归档4个文件：主档、备份、外置分页、关联事务；共复算32个文件条目。八例原v9源及备份保留，全部SHA/大小正确；新版历史为空且覆盖未知，旧ActiveRun/Settlement.plan原有字段投影无差异，Pending仍为0，页引用匹配。ImportV9读取验证后的归档，初始化空历史后发布，未调用Evaluator或Plan倒填。标题是显式迁移入口，Location/Entry协调独立根和写闸。

PAGED-RESTORE-A01等旧客户端恢复结果保留。锁竞争两个PID运行区间重叠，第二端title-ready=Blocked；v9正常命名空间为Missing，强制放入v9空间的v10内容为Incompatible，前后业务文件指纹一致。通用探针原始FAIL仍为FAIL，只作为负例拒绝证据，不重新分类成PASS。

## 双UI与实际修复 [S][P][C]

AdventureFlow.UI.cs的QueryHistory同时由DrawHistory与RebuildHistoryUgui调用，过滤及双UTC/稳定身份排序后生成新数组，不重排底层历史或写档。相对R2接手源码快照仅该UI文件变化：非活动旧uGUI canvas不再每帧清除historyOpen；IMGUI打开时透明raycast遮罩阻挡底层uGUI，关闭后取消。旧文件保存在UX05-IMGUI-R2/EVIDENCE/AdventureFlow.UI.before.cs.txt，可直接比较实际diff。

| 最终Run | PID | IMGUI/uGUI消费操作 | 前台验证 | 查询对数 | 退出 |
|---|---:|---|---:|---:|---:|
| MIXED-A06 | 28720 | 20 / 20 | 43 | 15 | 0 |
| EMPTY-A03 | 23248 | 2 / 2 | 6 | 1 | 0 |
| UNKNOWN-A03 | 32476 | 2 / 2 | 6 | 1 | 0 |
| 合计 | 3个独立进程 | 24 / 24 | 55 | 17 | 全0 |

已重新核对全部actions/outcomes、50对原生MouseDown/Up、滚动位置和状态。前台PID/HWND归属正确，坐标基于ClientToScreen/DPI事实。48次指成功消费的历程操作，不是GUI.Event.Use计数；55次还含继续、背包关闭和退出。六字段、排序、分页逐项相等；查询/切换/筛选期间Profile和主档SHA不变，关闭后无Preparing并恢复Camp输入上下文。

重新打开[IMGUI末条截图](UX05-IMGUI-R2/EVIDENCE/MIXED-A06/observer/screen-0009.png)和[uGUI末条截图](UX05-IMGUI-R2/EVIDENCE/MIXED-A06/observer/screen-0033.png)，均显示第7页“守誓”及相同Run身份。此为审计Agent图像核对，不冒充负责人[M]人工体验。

退出另走既存SaveBeforeExit：三份主档revision各加1，payload仅改变revision及camp.events/randomStateJson/resources；历史、committedRuns、收益不变，退出前主档成为完整备份，130个关联文件不变。因此UI只读成立，但不能写成整次进程从启动到退出主档SHA零变化。

已验证环境仅1280×720、DPI96。其他分辨率/DPI未验证，是已知非阻断覆盖限制：当前55次身份/坐标守卫、完整分页和17对业务结果均通过，查询层不随显示环境分叉；不能仅由CanvasScaler存在推定其他环境通过。

## 回归、构建及证据转用边界

P1C三地区的原run-summary、事件、完成文件、退出及各自v10主档相符，各有地区目标历史且Committed。R1十四个唯一UX-03技能场景的identityVerified/entryAuthorized/pass/damageVerdict均真、failed均假，并有keyEvents；loadedAssemblySha与manifest匹配。B1金红拒绝分解、B2收藏/错误ID拒绝/只读预览与实际替换匹配，有原始事件及代码断言。

D-20有129次实际出征后slot=0事件，没有新增长期槽位字段。D-23在Mono比较三地区及forest:hunts-complete四组、各256个固定掉落输入，攻击/防御/背包与仓库材料/配方均不变；原比较断言通过。各组完整数值未另存，本轮核验原Mono断言及源码，不用Python double冒充Unity float复算。

最终三类构建EXE/DLL与记录匹配，完整构建原退出码0，Release发布回执EXE SHA匹配。NoDefine/Release对UTF8/UTF16查Harness/Probe/UX_ACCEPTANCE等标记均为0，RuntimeInitializeOnLoads无验收启动项，无sidecar。[构建身份](FINAL_BUILD_IDENTITY.tsv)保留50行，早期失败构建没有删除。早期R1 NoDefine-A01和Release-A01仍有UX_ACCEPTANCE字符串，与后来改编译守卫再构建A03的历史吻合，不能把早期“all markers absent”摘要扩为最终严格门禁。

**F-01：最终纯发行运行证据未闭环。** 最终NoDefine DLL `E17F31F475A990E4183E4F07F56F9710532317C8F18FA1CC7492E956F5AADB78`、Release DLL `18D7C9FD00BD4C40926C6E6B52B9032C59D0D0F3FAE7B9B411965C7AC3A7188C` 在159条中无对应Player Run。当前原生UI在Acceptance观察副本，旧纯发行启动/回归来自较早DLL。源码差异小和既有测试降低风险，但仍是[D]跨构建转用，不是[P]最终纯发行已运行。无需盲目重跑全部历史矩阵，最小补证/风险接受需负责人裁决。

**F-02：部分历史Driver来源不能精确重现。** 114条仅留历史启动脚本哈希，其中31条属于R1的43条新增PASS；相关交付/构建区没有匹配源码。产品DLL可验证不等于外部Driver和输入生成方式全部可重现。保留原分类/哈希，不用当前脚本覆盖证据。

## 历史完整性与保护 [C]

- 原4142个历史文件及当前5404个索引项逐文件重算SHA256/大小，0差异；原68行逐字段不变，R2接手147行分类未覆盖。
- 原保护清单601项：590项保持基线字节，11项差异均为先前授权实施文件。相对R2接手1504项源码/配置快照仅AdventureFlow.UI.cs变化；没有发现其他非授权产品修改。ProjectSettings、Packages无未授权差异；迁移源及meta是既有授权新增。
- 读取2083条storage-audit，所记录路径全部在Evidence隔离根。本轮只访问源码、构建和隔离证据，未访问真实用户存档，也不为证明保护而读取真实档。历史日志不是全系统文件访问追踪，结论限定在记录入口/访问点。
- 本轮审计前6928个既有源码/配置/交付文件的路径、大小、SHA组合摘要为 `3C2DB543885D55E78F914652E2716BD97B73AA4A725A36957858AB275D329252`。排除四个新交付后末次再次匹配；Git Index SHA256保持 `5A03EB17D73F6F02167F382787C1AE7BBA4EC8BCC1FD1E71532C363DE4BB1FC1`。未清洗原始日志或历史FAIL。
- 个别二级review JSON自动转换UTC后省略末尾0，例如P1C forest摘要；原始存档仍是合法28字符。本轮精确比较使用payload和冻结事件，不以摘要代替原始字段。

## 方法、交付与停止

执行只读git branch/rev-parse/status/diff/ls-remote/sparse-checkout；Python标准库csv/json/hashlib逐行解析及SHA256复算；比较完整六字段、冻结尾部/committedRuns关联、UTC排序和17对查询；核对32个归档条目、源文件与分页引用；扫描程序集字节及启动表。没有调用会重写旧result/INDEX的工具。

对账表逐Run列原分类、原结果路径和SHA、PID/退出来源、EXE/DLL/Driver身份、隔离根、输入路径及替代文件名；缺失值不倒填。CSV/TSV列数、唯一Run ID、计数和内部引用已检查。

交付：[最终风险](FINAL_RISK_REGISTER.md)、[构建身份](FINAL_BUILD_IDENTITY.tsv)、[逐Run对账](FINAL_RUN_RECONCILIATION.csv)。原REPORT/ACCEPTANCE及证据索引不改。审计已停止，等待负责人复审F-01/F-02，不自动提交、推送、合并、发布或启动UX-06。
