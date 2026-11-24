import pathlib,json,csv,hashlib
D=pathlib.Path(__file__).resolve().parent
if (D/'RELEASE_RUNTIME/SUMMARY.json').exists():
    raise SystemExit('Historical pre-Release document generator stopped; use release_update_docs.py for the current report. No files changed.')
def put(name,value):(D/name).write_text(value.strip()+'\n',encoding='utf-8')
if not (D/'RISK_AT_SETTINGS_GATE_20261123.md').exists():
    (D/'RISK_AT_SETTINGS_GATE_20261123.md').write_bytes((D/'RISK_REGISTER.md').read_bytes())
put('REPORT.md','''# UX-06 地区档案与复访引导

**结论：CONDITIONAL_PASS。产品实现、最终构建及本批针对性 Player 验证已完成，保持未暂存，等待负责人复审。** 历史异常退出的原生根因、逐操作完整前台元数据及人工体验仍有限制，未扩大为整体无条件 PASS。

## 实际改动 [S]

起点 `1c3fb90bf5902c147fda35252dc59e3b3a5f8872`；独立工作树 `WanxiangGuitu-UX06`，分支 `feature/ux-progression-06-region-records`。已跟踪产品修改只有 AdventureFlow.UI.cs、ObjectiveCatalog.cs；新增 RegionRecords.cs 与 AdventureFlow.RegionRecords.cs，以及必要 meta、Editor 测试/构建门禁与条件编译 Driver。逐路径大小、SHA 和新增/修改分类见 [FILES_CHANGED.tsv](FILES_CHANGED.tsv)。

营地“冒险历程”接入森林/遗迹/洞窟档案，两套 UI 共用只读投影、分页、状态和文案。森林读取真实首领计数/徽章，遗迹五项永久回执与洞窟首奖分组，区分待领取/已领取；最近目标使用已发布 Profile 的名称快照和确定性排序。历史跳转复用原地区筛选/分页。页面没有保存、结算、领取或发奖入口。无来源的地区终身指标显示“暂无可用记录”。修正森林唯一新武器来源的错误文案。[数据映射](DATA_MAPPING.md)

## 构建与输入 [B]

Unity 6000.6.5f1 / Windows64 Mono。最终 Acceptance BUILD11（0 errors / 115 warnings）、Release BUILD12_RELEASE（0 errors / 113 warnings）均取得真实 OS 退出码 0。源码、Driver 和 1516 项构建输入逐字节冻结，构建期间无漂移。产物完整 SHA/buildId 见 [BUILD_IDENTITY.tsv](BUILD_IDENTITY.tsv)。Release 实际 DLL 不含 UX06 Probe、旧验收 Harness、UX_ACCEPTANCE/UX06_ACCEPTANCE 以及 Editor 测试类型，见 [RELEASE_EXCLUSION.json](RELEASE_EXCLUSION.json)。本批没有新增纯 Release Player 运行，不将构建排除扫描冒充运行验收。

Unity 曾改写六项设置，现按负责人明确授权从已核验原件逐字节恢复；不是“构建从未产生变化”。[恢复核验](RECOVERY_20261124/RESTORATION_POSTVERIFICATION.json)（原 RESTORATION_RECEIPT 的 rows/proposedAction 为恢复前捕获内容，继续保留） 及原 AFTER_BUILD02/diff/STOP 保留。后续只在仓库外可写副本构建，实际打包输入服务均关闭，两个 URP 有效对象与批准基线相等，Graphics 引用未变。[有效输入分析](BUILD_INPUT_ANALYSIS.md)

## 测试与真实运行 [T/P/C]

- 最终源码 14 个独立投影/边界夹具通过；构造数据与真实出征分开，不因重复执行增加用例数。
- 最终同一 Acceptance/Driver 构建九局通过：F10/F11/F12、R07/R08/R09、C07/C08/C09，三地区各三局，独立 PID，同地区连续冷启动。真实移动、机关/宝箱、撤离、Pending/Committed 正常链产生记录；不是直接写历史制造 PASS。九局只证明这些功能，不证明留存或乐趣。[最终九局](FINAL_COHORT.json)
- 最终 UI 四条完整功能观察通过：真实记录 A03、容量、未知、新空档。57 次原生点击尝试，56 次状态变化；容量第20次点击未消费，原记录保留，第21次重试成功。覆盖双 UI 档案分页、三地区切换、历史跳转/筛选、七页历史导航、返回/关闭及点击穿透检查。四组相同地区/页码的 renderer 状态、Profile 一致；浏览窗口内 Profile/revision/RNG/攻防/save SHA 不变。[原生交互复算](NATIVE_UI_RECOMPUTATION.json)
- 全部 30 条 Run 保留原判定：原始 PASS 24、FAIL 6；其中 F07 的原始 PASS 遭 OS 异常退出，验收为 NOT_ACCEPTED，故进程条件满足的 PASS 为 23、NOT_ACCEPTED 为 7。23 中 UI-A02 仅承认已操作按钮和只读窗口，完整内容浏览不通过，不能用它替代 A03。阶段混合构建九局不替代最终同一构建九局。[逐 Run 矩阵](PLAYER_RUN_MATRIX.csv)

原失败、BUILD01 包缓存失败、BUILD02 准备构建/null退出码、BUILD04_RELEASE 门禁拒绝及所有中断/失败不删除、不回写。细节见 [风险](RISK_REGISTER.md) 与 [复现](TESTING.md)。

## 保护与停止状态 [C]

[最终保护](FINAL_PROTECTION.json) 与 [201 行指纹](PROTECTION_SHA256.tsv)：原 UX-05 HEAD/分支/index/status/AGENTS 未变；本工作树两项已授权 tracked diff，暂存区为空。六设置当前为原基线，Packages/锁文件及非授权既有产品源码无变化；Schema、迁移、结算、奖励、经济、掉落、RNG、D-20/D-23 未改。只使用明确隔离根，没有读取或修改真实用户存档。复用 UI 样本的原 UX-05 源文件逐字节仍一致，不重开旧证据审计。

UX-05 继续 CONDITIONAL_PASS，F-02 继续 OWNER_ACCEPTED_HISTORICAL_LIMITATION。本批没有 add/commit/push/merge，没有操作 main，没有重写 UX-05 证据。下一步仅为负责人复审本批实现和遗留限制。
''')
put('ACCEPTANCE.md','''# UX-06 实际验收

结论 CONDITIONAL_PASS，证据层级不互相替代。原始失败仍在矩阵中。

|项目|结果/证据|
|---|---|
|新空档与旧未知、五项遗迹/洞窟分组、永久回执三状态、名称快照/排序/128说明|[T] 14个夹具通过；最终 BUILD11/FIXTURE_RESULT.json、BUILD12_RELEASE/FIXTURE_RESULT.json；相同14项只计一次|
|只读已发布来源|[S] QueryRegionRecord 独立 InspectReadOnly；保存失败/待核对/结算待确认无入口；[P/C]九局 Pending 快照无新历史、Committed 回读才有，冻结行一致；没有专门新增故障注入Run|
|三地区连续与跨进程|[P/C]最终同一构建九局各3通过，FINAL_COHORT.json 与原始Run事件；首领击杀/洞窟首奖分组的正值状态主要为夹具证据，九局不是首领战专项|
|双UI档案、三地区、返回/关闭、历史跳转|[P/C]UI-REAL-A03 20次原生点击；三页遗迹与两页森林/洞窟实际浏览，4组renderer状态配对；uGUI与IMGUI共用同一投影/分页逻辑|
|七页历史/筛选/覆盖|[P/C]UI-CAPACITY-A01 25次尝试，1次未消费保留并重试成功。uGUI全128条7页、IMGUI森林126条7页；筛选重置、类型空匹配、跳转重置类型；没有逐一滚读全部离屏行|
|空/未知历史|[P/C]UI-EMPTY-A01与UI-UNKNOWN-A01各6次原生点击，两UI正确区分，新档正常创建；旧样本来源为既有隔离UI工件副本|
|浏览只读/D-23|[P/C]最终4个UI观察窗口前后及逐操作Profile/revision/RNG/攻防相等，主档SHA相等；材料/配方/回执包含在完整Profile比较内；退出时正常保存位于窗口之外|
|1280×720 DPI96|[P]容量Run有完整Win32客户端/DPI/前台PID样本；A02亦有历史样本。其他最终UI Run有截图、产品focus gate和原生输入窗口，但没有逐操作完整Win32样本，不扩大为全部操作均已完成此前台元数据审计|
|构建保护|[B/C]BUILD11/BUILD12_RELEASE真OS退出0，冻结输入无漂移、URP有效设置相等、打包Services均false；六文件授权恢复记录保留|
|发行工具排除|[B/C]实际Release DLL双编码标识扫描+原条件编译/Editor隔离；无验收Probe/Harness/define标识；本批未运行Release Player|
|Schema/冻结规则/原UX05|[S/C]保护指纹与diff通过；非授权战斗/技能/经济源码未改，不把静态保护说成重新完成UX03全套Player回归|

最终4条UI的57次尝试不等于57条独立测试。全批30条Run不等于30条全部通过。UI-A02仅部分功能范围，F07探针PASS但异常退出均单独限制。

人工手感、乐趣、长期留存、其他分辨率/DPI、本批未实际触发的首领正值纪念/所有收藏正值组合属未验证或夹具证据，不能转写为真实Player通过。
''')
put('RISK_REGISTER.md','''# UX-06 当前风险与历史处置

结论 CONDITIONAL_PASS；旧状态见 RISK_AT_SETTINGS_GATE_20261123.md / REPORT_AT_SETTINGS_GATE_20261123.md，不修改旧 STOP 和原始失败。

|编号|当前状态|事实、处置与限制|
|---|---|---|
|UX06-G01|CLOSED_BY_OWNER_AUTHORIZED_RECOVERY|Unity曾改写六设置，依批准方案核验后原字节恢复；后续独立副本构建、导入/有效/打包快照及Services门禁通过，不接受新的有效配置。原漂移/失败记录保留。|
|UX06-B01|CLOSED_FOR_FINAL_BUILD|BUILD01失败、BUILD02准备结果/null退出码、BUILD04拒绝保留；BUILD11与BUILD12_RELEASE冻结输入与真OS退出0为最终依据。|
|UX06-P01|OPEN_HISTORICAL_NATIVE_EXIT|F07业务记录成功但OS退出0xc000041d，旧探针误作PASS，不能接受为运行通过。确切原生根因未证实。Driver改为Update后延迟退出、启动器核对真实退出码，并串行运行；最终九局与4条完整UI退出0。不得声称历史异常根因已消除；该项不是负责人已接受的F-02。|
|UX06-U01|KNOWN_INPUT_ATTEMPT_LIMITATION|容量第20次IMGUI点击未消费，重新观察/前台采样后第21次成功；首次不算通过。其余最终原生点击有实际状态变化。A03/未知/空档缺少完整逐操作Win32前台元数据，保留为证据粒度限制。|
|UX06-U02|KNOWN_COVERAGE_LIMITATION|1280×720 DPI96已实测；其他环境未验证。历史7页导航已验证但未逐个滚读全部离屏行。人工体验/长期留存未验证。|
|UX06-U03|RESOLVED_WITH_PAGED_RECORDS|A02的档案滚轮/拖动未展现全部内容，原PASS只限只读/已操作按钮。产品改为双UI共同显式分页，A03完整浏览复测；旧截图/分类保留。|
|UX06-T01|CLOSED_FOR_REQUIRED_SCOPE|最终同一构建3地区各3局通过。正值首领纪念/洞窟首奖/全部收藏组合的细分状态为构造夹具验证，不称其全部来自九局真实触发。|
|UX06-D01|DATA_GAP_NONBLOCKING|无充分地区出征/撤离账本/终身最高，UI中文提示暂无可用记录，不添加字段，不推测永久收益。|
|UX06-R01|NOT_RUN_RELEASE_PLAYER|纯Release构建与工具排除通过；本批真实Player使用Acceptance Mono产物，不扩大发行运行结论。|
|F-02|OWNER_ACCEPTED_HISTORICAL_LIMITATION|UX05历史Driver无法位级重现为负责人既有接受结论；不再追查，不改旧Run判定或UX05 CONDITIONAL_PASS。|

F01为驱动寻路/碰撞绕行不足；F02移动停止，焦点竞争可疑但原始焦点证据不足，不能确认唯一根因；F03到危险撤离点实际死亡，正常没有成功历史，后续驱动选择安全出口，不修改敌人/HP/战斗；F08与C04为前台信号未送达的出征前失败。后续新Run通过不回写这些原FAIL。

UI-A01只读比较失败与前台/自动保存时序有关；新观察在正常自动保存后取基线，测试构建临时延长间隔并恢复，产品存档逻辑不改。独立UI复算工具最初错误假设每Run都有完整Win32元数据而报文件缺失；修正工具读取实际存在材料，并将缺失明确列为METADATA_PARTIAL，而非伪造样本或把缺失改判为已验证。
''')
print('Final documentation written; no product or index mutations')
