# UX-06 当前风险与历史处置

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
|UX06-R01|CLOSED_FOR_REACHABLE_UGUI_SCOPE|BUILD12_RELEASE两条真实运行退出0，三地区uGUI及冷启动验证完成；不重建、不注入探针，IMGUI另列未执行。|
|F-02|OWNER_ACCEPTED_HISTORICAL_LIMITATION|UX05历史Driver无法位级重现为负责人既有接受结论；不再追查，不改旧Run判定或UX05 CONDITIONAL_PASS。|

F01为驱动寻路/碰撞绕行不足；F02移动停止，焦点竞争可疑但原始焦点证据不足，不能确认唯一根因；F03到危险撤离点实际死亡，正常没有成功历史，后续驱动选择安全出口，不修改敌人/HP/战斗；F08与C04为前台信号未送达的出征前失败。后续新Run通过不回写这些原FAIL。

UI-A01只读比较失败与前台/自动保存时序有关；新观察在正常自动保存后取基线，测试构建临时延长间隔并恢复，产品存档逻辑不改。独立UI复算工具最初错误假设每Run都有完整Win32元数据而报文件缺失；修正工具读取实际存在材料，并将缺失明确列为METADATA_PARTIAL，而非伪造样本或把缺失改判为已验证。

## Release 补验后的现行限制

- UX06-P01继续OPEN_HISTORICAL_NATIVE_EXIT：F07为旧BUILD09关闭阶段原生崩溃；最终BUILD11/12身份不同，本轮两个Release退出0，原生根因仍未知，不能声明修复或已被负责人接受。原始PASS/验收NOT_ACCEPTED不变。
- UX06-R02 = NOT_RUN_NO_PRODUCT_ENTRY：纯Release无正式IMGUI renderer选择入口，既有IMGUI只在Acceptance切换；未为补验修改产品。需要负责人接受本批纯Release覆盖限制，不能把uGUI通过扩大到双UI。
- UX06-R03 = VISIBLE_INPUT_LIMITATION：30次原生输入中6次无预期可见确认，原图与输入均保留，不归因产品故障。使用正常Alt+F4取得两次退出0；不声称已验证标题菜单退出路径。
- UX06-R04 = OBSERVABILITY_LIMITATION：本轮只读观察磁盘、可见UI及OS进程，未观测Release实时UI状态、内存revision/RNG。自动保存导致主档字节/revision变化；浏览窗口业务事实未变，仅既有资源捕获数组顺序变化。冷启动camp事件与随机状态会重建，全部非camp永久字段及128条历史一致，不把有限比较描述为全部存档/实时随机流冻结。
- 其他分辨率/DPI、人工手感、长期留存和九局之外的首领/全部收藏正值组合仍按既有未覆盖范围报告。

本批仍CONDITIONAL_PASS；可供只读提交准备审查，尚无暂存/提交授权。F-02继续OWNER_ACCEPTED_HISTORICAL_LIMITATION，与上述UX06限制分别登记。

## UX06-SOURCE01：外部启动器来源缺口（提交候选审查新增）

OPEN / DATA_GAP / OWNER_REVIEW_PENDING。仅本批现存文件与源码ZIP核对后，9条早期Run未找到SHA 0f99646d3b8a074049399e35460b7ac4d4d874b2758a40c13a3847a7401e8a75 对应的精确外部启动器源码，包含F01/F02/F03的FAIL以及F04/F05/F06/R01/R02/R03的阶段PASS。不是运行Driver缺失，不用当前源码补填历史身份；最终同构建九局及两条Release来源完整。保留历史判定，不套用UX05 F-02接受状态，不宣称穷尽恢复可能性，不自动扩大验收。

## 本次交付授权的有限处理

28条JPEG派生引用已修正，正式记录于DELIVERY_CONTROL/REFERENCE_RESOLUTION.tsv；七处格式例外仅限登记路径/原SHA/行号，获准原样保留。240个完整路径属性已追加，未扩展LFS或持久配置。外置1463项及修正前54项控制副本均本地解包核验通过，未外部签收。上述只关闭已授权的材料处理动作；UX06-SOURCE01、F07、Release IMGUI、人工体验和其他显示环境限制仍OPEN/待复审，不记为负责人已接受。F-02状态只适用于原UX05历史限制。
