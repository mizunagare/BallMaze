# UX-06 地区档案与复访引导

**结论：CONDITIONAL_PASS。产品实现、最终构建及本批针对性 Player 验证已完成，保持未暂存，等待负责人复审。** 历史异常退出的原生根因、逐操作完整前台元数据及人工体验仍有限制，未扩大为整体无条件 PASS。

## 实际改动 [S]

起点 `1c3fb90bf5902c147fda35252dc59e3b3a5f8872`；独立工作树 `WanxiangGuitu-UX06`，分支 `feature/ux-progression-06-region-records`。已跟踪产品修改只有 AdventureFlow.UI.cs、ObjectiveCatalog.cs；新增 RegionRecords.cs 与 AdventureFlow.RegionRecords.cs，以及必要 meta、Editor 测试/构建门禁与条件编译 Driver。逐路径大小、SHA 和新增/修改分类见 [FILES_CHANGED.tsv](FILES_CHANGED.tsv)。

营地“冒险历程”接入森林/遗迹/洞窟档案，两套 UI 共用只读投影、分页、状态和文案。森林读取真实首领计数/徽章，遗迹五项永久回执与洞窟首奖分组，区分待领取/已领取；最近目标使用已发布 Profile 的名称快照和确定性排序。历史跳转复用原地区筛选/分页。页面没有保存、结算、领取或发奖入口。无来源的地区终身指标显示“暂无可用记录”。修正森林唯一新武器来源的错误文案。[数据映射](DATA_MAPPING.md)

## 构建与输入 [B]

Unity 6000.6.5f1 / Windows64 Mono。最终 Acceptance BUILD11（0 errors / 115 warnings）、Release BUILD12_RELEASE（0 errors / 113 warnings）均取得真实 OS 退出码 0。源码、Driver 和 1516 项构建输入逐字节冻结，构建期间无漂移。产物完整 SHA/buildId 见 [BUILD_IDENTITY.tsv](BUILD_IDENTITY.tsv)。Release 实际 DLL 不含 UX06 Probe、旧验收 Harness、UX_ACCEPTANCE/UX06_ACCEPTANCE 以及 Editor 测试类型，见 [RELEASE_EXCLUSION.json](RELEASE_EXCLUSION.json)。本轮复用 BUILD12_RELEASE 完成两条纯 Release 实际运行，未重建；构建排除扫描与运行证据分别保留。

Unity 曾改写六项设置，现按负责人明确授权从已核验原件逐字节恢复；不是“构建从未产生变化”。[恢复核验](RECOVERY_20261124/RESTORATION_POSTVERIFICATION.json)（原 RESTORATION_RECEIPT 的 rows/proposedAction 为恢复前捕获内容，继续保留） 及原 AFTER_BUILD02/diff/STOP 保留。后续只在仓库外可写副本构建，实际打包输入服务均关闭，两个 URP 有效对象与批准基线相等，Graphics 引用未变。[有效输入分析](BUILD_INPUT_ANALYSIS.md)

## 测试与真实运行 [T/P/C]

- 最终源码 14 个独立投影/边界夹具通过；构造数据与真实出征分开，不因重复执行增加用例数。
- 最终同一 Acceptance/Driver 构建九局通过：F10/F11/F12、R07/R08/R09、C07/C08/C09，三地区各三局，独立 PID，同地区连续冷启动。真实移动、机关/宝箱、撤离、Pending/Committed 正常链产生记录；不是直接写历史制造 PASS。九局只证明这些功能，不证明留存或乐趣。[最终九局](FINAL_COHORT.json)
- 最终 UI 四条完整功能观察通过：真实记录 A03、容量、未知、新空档。57 次原生点击尝试，56 次状态变化；容量第20次点击未消费，原记录保留，第21次重试成功。覆盖双 UI 档案分页、三地区切换、历史跳转/筛选、七页历史导航、返回/关闭及点击穿透检查。四组相同地区/页码的 renderer 状态、Profile 一致；浏览窗口内 Profile/revision/RNG/攻防/save SHA 不变。[原生交互复算](NATIVE_UI_RECOMPUTATION.json)
- 补验前的 30 条 Run 保留原判定：原始 PASS 24、FAIL 6；其中 F07 的原始 PASS 遭 OS 异常退出，验收为 NOT_ACCEPTED，故进程条件满足的 PASS 为 23、NOT_ACCEPTED 为 7。23 中 UI-A02 仅承认已操作按钮和只读窗口，完整内容浏览不通过，不能用它替代 A03。阶段混合构建九局不替代最终同一构建九局。[逐 Run 矩阵](PLAYER_RUN_MATRIX.csv)

原失败、BUILD01 包缓存失败、BUILD02 准备构建/null退出码、BUILD04_RELEASE 门禁拒绝及所有中断/失败不删除、不回写。细节见 [风险](RISK_REGISTER.md) 与 [复现](TESTING.md)。

## 保护与停止状态 [C]

[最终保护](FINAL_PROTECTION.json) 与 [201 行指纹](PROTECTION_SHA256.tsv)：原 UX-05 HEAD/分支/index/status/AGENTS 未变；实施阶段本工作树两项已授权 tracked diff（本次另有已批准的根属性变更），暂存区为空。六设置当前为原基线，Packages/锁文件及非授权既有产品源码无变化；Schema、迁移、结算、奖励、经济、掉落、RNG、D-20/D-23 未改。只使用明确隔离根，没有读取或修改真实用户存档。复用 UI 样本的原 UX-05 源文件逐字节仍一致，不重开旧证据审计。

UX-05 继续 CONDITIONAL_PASS，F-02 继续 OWNER_ACCEPTED_HISTORICAL_LIMITATION。本批没有 add/commit/push/merge，没有操作 main，没有重写 UX-05 证据。下一步仅为负责人复审本批实现和遗留限制。

## 纯 Release 补验与历史退出关联（2026-11-24）

结论仍为 **CONDITIONAL_PASS**。复用 BUILD12_RELEASE，产品源码、1516项冻结构建输入与产物原始字节未变，本轮未构建、未注入验收工具。新增两条 Run，九局及原57次点击矩阵未重跑。

|Run ID|PID|buildId|实际退出码|实际覆盖|
|---|---|---|---|---|
|UX06-RELEASE-CORE-R01-20261124|912|UX06-7a4fa23741a53c83|0|正式标题继续游戏；128条历史；三地区uGUI档案、森林近期快照、洞窟复访；遗迹/洞窟历史跳转及返回|
|UX06-RELEASE-COLD-R02-20261124|3236|UX06-7a4fa23741a53c83|0|同根冷启动再次读取；128条和森林126/遗迹1/洞窟1一致；三地区uGUI浏览、洞窟跳转及返回|

EXE SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；产品 DLL SHA256 `7a4fa23741a53c8361b546fb9054e504a65b868edd0e453938004fc840d6e18f`。外部原生输入源码及SHA、启动参数、原始PNG/JPEG、按键/点击、进程观察器均逐Run归档。正常退出使用 Windows Alt+F4，原有 quit/before-exit/save 审计与干净关闭日志匹配真实OS退出0，不是强制结束，也不宣称已验证标题菜单退出按钮。

新根来自本批已登记容量隔离样本的132文件逐字节副本，不访问原UX05或真实用户目录；[来源指纹](RELEASE_RUNTIME/SAMPLE_COPY.json)。原样本SHA/大小/mtime及此前1176项原始证据均未变；[结束保护](RELEASE_RUNTIME/PROTECTION_AFTER.json)。

**纯浏览磁盘结论有边界：** 既有自动保存没有关闭。R01 revision 655→667，R02 695→705；主档原始SHA确实变化。逐字段检查表明，各自浏览窗口内仅revision、保存时间、校验和和营地resources数组顺序变化。84个唯一实体的完整值映射一致；保留历史、全部其他Profile字段、材料、配方、回执及累计账本一致。原捕获使用 FindObjectsSortMode.None，比较仅规范化这个已证实的数组顺序，没有改写存档或忽略其他字段。每Run的 PERSISTED_BROWSE_COMPARISON.json 与原始快照可复算。

跨进程历史和全部非camp的Profile字段一致。camp.randomStateJson、camp.events在启动间有差异，不能声称完整检查点或实时RNG跨启动相等。源码依据是既有 ApplyCamp 调用 session.Restart、选择性恢复营地，不走 RestoreWorld；本轮没有改变该路径。[跨启动差异](RELEASE_RUNTIME/COLD_PROFILE_DIFFERENCES.json)。Release实时UI状态、内部revision及RNG未被探针观测，磁盘事实不能替代这些内部断言。

**纯 Release IMGUI = NOT_RUN_NO_PRODUCT_ENTRY。** CombatSession.Awake始终创建PlayerHudPresenter；本批唯一关闭该组件的renderer切换在UX06_ACCEPTANCE探针内，Release不含此入口。没有通过注入或改造产物完成切换，既有Acceptance IMGUI结论保留，但不升级为纯Release IMGUI通过。

两Run共30次外部输入记录，24次取得相应可见结果/正常退出确认，6次未取得预期可见确认（R01返回标题/释放鼠标/Tab/窗口X尝试、R02关闭历史）。这些尝试原样保留，不推定为产品缺陷、不计为输入消费通过；[逐输入可见结果](RELEASE_RUNTIME/INPUT_VISIBLE_REVIEW.tsv)。最终Alt+F4退出0；没有触发新原生异常。

历史F07属于BUILD09，DLL `5bfa8d0e278367d62d763fa9bd8f349cb8e882f3386e6f91764bd816a2150649`，与最终BUILD11/12 DLL及Driver不同。BUILD09与BUILD11的EXE和UnityPlayer.dll相同，不能因产品DLL变化排除引擎层共因；Release的引擎二进制不同，[引擎关联SHA](RELEASE_RUNTIME/ENGINE_CORRELATION.json)。日志在Input System Shutdown之后记录Crash!!!，OS退出3221226525（0xc000041d）。只能确定退出阶段，不能确定原生根因。原始PASS、验收NOT_ACCEPTED不变，不宣称修复。最终BUILD11的C04退出1为未收到前台信号的驱动主动失败，非同类崩溃；其余非零退出与证据见[完整关联表](RELEASE_RUNTIME/EXIT_CORRELATION.csv)。最终BUILD11/12未观察到该原生崩溃，不等于证明不存在。

原30行的身份与判定逐字段不变，追加2条限定uGUI范围的Release PASS后，总32条：原始PASS26/FAIL6，进程验收PASS25/NOT_ACCEPTED7；UI-A02的局部结论仍不扩大。F-02保持OWNER_ACCEPTED_HISTORICAL_LIMITATION。

**提交准备状态：CONDITIONAL_READONLY_READY。** 固定源码/构建身份、运行证据与保护材料已足够开展只读提交候选审查；仍需负责人确认接受纯Release IMGUI不可达、历史原生崩溃根因不明及未覆盖人工/显示环境限制。不是无条件验收收口，不构成暂存/提交授权。该补验阶段当时未生成提交白名单；后续现行交付状态见下节。

提交候选只读审查发现：UX06早期F01/F02/F03/F04/F05/F06/R01/R02/R03的外部启动器SHA 0f99646d3b8a074049399e35460b7ac4d4d874b2758a40c13a3847a7401e8a75 在本批现存归档中未找到精确源码，涉及6条阶段PASS。32条运行Driver/原生输入源码与构建对应，最终九局和两条Release启动器来源完整。此为新增UX06来源DATA_GAP，未被负责人接受，不适用UX05 F-02；不改变原始Run判定。

## 现行交付前置收口（负责人本次授权）

以上实施/Release补验结论和旧风险均保留；本节为现行交付状态。整体仍CONDITIONAL_PASS，不因材料收口升级。

已封存修正前54份控制原件及身份；28条JPEG引用逐项改正，六次未确认输入及原32条Run判定、截图均未改。文档生成器已防止缺图回退退出JSON，并在本次交付冻结后拒绝旧聚合再生，避免覆盖现行材料。九条早期外部启动器来源缺口已正式登记OPEN，未套用F-02。

根.gitattributes精确追加240完整路径的-text，原有规则和10项LFS保持；两文件七处行尾空格按[精确范围](DELIVERY_CONTROL/FORMAT_EXCEPTION_APPROVAL.tsv)获准原样保留，未批准其他位置或内容。未运行clean或暂存，实际pointer/对象/索引验收均NOT_RUN。

原1463项已封装为 `UX06_RAW_EVIDENCE_1463.zip`，SHA256 `75d8306d0990ee688173fb968e565364bf7f170220a8ec8b730171f05c30b24b`；新增54份修正前控制副本另封装为 `UX06_PRECORRECTION_CONTROL_54.zip`，SHA256 `2b7df2827d0033788719caece44f79bcbd98c7832788def7a173aae6f13bf507`。两包在全新目录逐路径、大小、SHA核验通过，原件与首次解包失败目录均保留。[包身份与实际本地保存/接收位置](DELIVERY_CONTROL/PACKAGE_RECEIPTS.json)、[独立接收校验](DELIVERY_CONTROL/PACKAGE_VERIFICATION.json)。这只证明本地验证，**不宣称已完成外部传输或签收**。

正式交付元数据及不依赖本机审查目录的核验方式见[交付路由](DELIVERY_CONTROL/DELIVERY_ROUTE.md)。当前原始Run事实保持；本次变化仅为授权派生文档/工具、属性、当前索引和控制材料。最终候选以本轮重新生成的SUBMIT_WHITELIST及逐路径SHA表为准，不预设480/481。材料完成后保持空暂存，等待对最终固定集合的暂存授权；F07、启动器缺口、Release IMGUI、人工/显示环境仍供负责人裁决，未自动接受。
