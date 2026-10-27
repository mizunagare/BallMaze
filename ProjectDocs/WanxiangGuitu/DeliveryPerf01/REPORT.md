# PERF-01：性能基线与发行警告审计

## 范围、基线与复审归档

开工本地HEAD/远端main实读均为`6f2abca5f89fc80fc5d298623eda12f557654b78`，没有回退。PLAYER-02固定SHA复审归档于[Reviews](Reviews/PLAYER02_REVIEW_ARCHIVE.md)，附用户完整任务原文。其结论仅为交付方证据范围内的隔离非开发验收Player纵切有条件接受；复审方没有独立重建/运行，不是发行包完整冒险、原生输入或人工验收。

本批仅增加文档目录中的性能采样/分析工具，以及既有BUILD01包装器的可选`AcceptanceProfile Perf01`。默认Release和Player02入口不变；不改产品Assets、依赖、地图、经济、随机流或v9合同，不自动消除任何警告。最终交付提交SHA以核对远端后的交付块/固定链接为准，不能将开工输入SHA称为最终实现SHA。

## 测量方法与输入

工程外唯一根`D:/WGPF/1027-224456-e570002e`，重新短路径冷导入；复用BUILD01构建与PLAYER02独立进程/非活动桌面、合成集合、输入转发和退出回执。不使用UnityEditor作为性能Player运行驱动。临时采样代码只注入拥有者Acceptance副本，启用FrameTimingStats，BuildOptions.None。单独Release不注入任何测试类型/参数/源文件；PE类型/引用、143模块UTF8/UTF16扫描和源目录证据见[BuildProof](Evidence/Run-1027-224456/BuildProof)。每次运行关联产物、工具、输入集合及Profile/Run/region/seed/layout/装备/来源账/随机状态。

输入含用户ForestRuins/ProjectSettings/Recovery覆盖层，完整1152项哈希留证，**不是纯Git main场景的无条件复现证明**；不发布覆盖层正文。原始场景SHA256为`EBC46CE7104B6D6CE90B7F510A59A401D7CDF64AE8BABC85A7EBBF881C9D16D4`，ProjectSettings为`7D06EA8265EDAAF0A1A7402CFF1E94DA015450C58899438EBF4A5D97E37FD451`。

硬件i5-12400F（6核/12逻辑）、RTX3060、约48GB RAM、Windows11 Pro26200；驱动、设备、只读电源方案见[hardware](Evidence/Run-1027-224456/hardware.json)。实际Player确认NVIDIA/D3D11；WMI另列虚拟显示适配器，不能把其分辨率当作Player分辨率。WMI AdapterRAM溢出值不用作显存容量；SystemInfo的12113MB只为设备报告容量，不能当成可用/剩余显存。

测量固定1280×720窗口、PC、VSync0、targetFrameRate=-1、10秒预热；不为美化结果改帧率。Native host记录`inputDesktopActive=false`、SW_SHOWNOACTIVATE。Unity内部`isFocused=true`也保留，两者不能混为正在操作用户桌面。非独占硬件负载、D3D11后台呈现、合成构筑与临时观测代码均为限制。

Running输入为PLAYER02实际后继Run：seed592864411、generationVersion8、layoutRevision5；白色长枪等配置见完整快照/合成存档。Camp输入来自实际Committed边界。Loop输入由本批真实采集/拾取/渡口原子扣费产生，不编辑修复标志；后继Run种子由正常业务生成，不假称三次出征seed相同。Resume三次从同一实际后继集合新副本启动。

## 执行结果与性能数据

首轮完整队列为**15 PASS / 7 FAIL / 6 NOT_RUN**，原始结果、exit与Pass1冻结副本全部保留。7个失败包括3个后退出指纹工具错误及4个运行时驱动技能选择卡住；不是7个已确认产品缺陷。前置失败造成Loop/Resume各3个NOT_RUN，不做伪造回退。定向补跑另存recovery，不覆盖首轮。

最终逐例资格、三次独立窗口、CPU主/渲染/GPU P50/P95/P99、缺失数、GC、内存、加载、活动切片与Title ON/OFF对照见[逐窗口数据](Evidence/Run-1027-224456/AnalysisFinal/MEASUREMENTS.md)、[完整JSON](Evidence/Run-1027-224456/AnalysisFinal/summary.json)、[CSV](Evidence/Run-1027-224456/AnalysisFinal/summary.csv)。[accepted-runs](Evidence/Run-1027-224456/AnalysisFinal/accepted-runs.json)明确列出最终24个8×3窗口与3个额外Title对照，校准/前置/失败不算正式重复。

定向补跑13项PASS，真实Loop×3及Resume×3的独立只读核对全部PASS：确实创建新森林Run，恢复同一后继Profile/Run/区域/seed/layout/streams/gear/ledger。全部37个原始案例的**测量资格**为27 PASS/8 FAIL/2 NOT_RUN；这里的8包含2个短校准的工具资格失败，2个NOT_RUN为不设性能窗口的渡口准备（一成一败），与首轮28个编排行的15/7/6是不同层级。没有通过分类把失败准备改称业务成功。

可复核的CPU主线程FTM P95三次范围（ms）：标题0.933～1.298、营地2.740～3.767、移动4.085～4.689、采集5.384～5.597、普通战斗4.094～4.821、精英/首领4.432～5.086、循环5.158～5.501、恢复4.652～4.758。逐例P50/P99和所有原始离群值同时公开；这些是临时观测包的描述性数据，不能按此给发行包作预算结论。

CPU FrameTiming主/渲染、Profiler主线程、GPU、帧间隔、系统CPU占用分别保存；不以帧间隔替代CPU，不以CPU填补GPU。FTM约4帧回传延迟，重复timestamp/非正值保留在raw但不塞入有效分布。GPU表是有效子集，完整覆盖未取得；`missing`含无新FTM记录与非正计时。DrawCalls为可用Recorder；没有GC Allocated In Frame和Render Thread Recorder时分别NOT_RUN，渲染时间另取明确标识的FTM，不冒充该Recorder可用。

Windows精确PID系统sidecar提供实际工作集/私有内存与CPU时间序列；Mono进程API零值视不可用。GC.CollectionCount仅代0（当前Mono最大代0）计增量，不将三个代相加重复计数。已知64KiB分配探针仍返回0，所以自分配字节/Release每帧GC Alloc不能测量，明确NOT_RUN；不是“零GC”。可用的Mono使用量、Unity分配总量和GC集合事件单列。

GC集合数较高，但逐帧字符串/CSV及虚拟驱动自身也产生分配；缺乏有效分配字节计数时，不能从总GC次数把压力归因于产品。Title ON自采样耗时P50约29.7～38.2微秒、OFF约23.1～30.3微秒；该计时不覆盖全部系统sidecar/驱动/引擎探针开销，也不能将相减值直接当作产品原本耗时。

GPU进程专用/共享内存计数器未取得有效实例，错误与有限3次查询保留，不用设备总容量代替可用显存。纯区域生成耗时未单独剖分；实际host启动→标题、Continue选择→game-ready、出征请求→后继就绪边沿单独记录，后者包含UI输入/业务等待，不能冒充纯生成计时。

120秒普通/精英首领窗口包括接近、真实攻击、击败、恢复与遭遇耗尽后的观察，实际事件和活动分布逐例列出。没有持续补怪或修改BossHP/AI；因此不能称为120秒连续高强度战斗性能。Loop为真实撤离→Pending→Committed→确认→取材制造→再次森林出征的可变时段，不冒充180秒稳态负载。Resume为标题预热后的加载与观察30秒。

采样器自身耗时保留；同V3产物Title额外采集ON/OFF各3次。OFF仍含基础CSV、驱动、sidecar和FrameTimingStats构建，不能给出完整采样开销上限或自动扣除工具成本。没有目标硬件预算，**不宣称性能达标或平衡完成**。本批没有源码调用栈层面的已确认瓶颈；过期对象查找API/热路径只属后续剖析候选，不从静态警告数量推导每帧调用次数或因果。

## 91条发行警告

新Release：0 Error /91 Warning /4 Log，完整warning文本集合与PLAYER02一致。逐条[WARNINGS.md](Evidence/Run-1027-224456/WarningAudit/WARNINGS.md)、[JSON](Evidence/Run-1027-224456/WarningAudit/warnings.json)、[CSV](Evidence/Run-1027-224456/WarningAudit/warnings.csv)记录ID、原文、文件/行/列、API、源码/文本SHA、Player调用路径、替代建议、风险、潜在行为改变和回归。

- 86条CS0618：36条排序枚举附加诊断、34条普通FindObjectsByType、2条保留inactive的重载、14条FindFirstObjectByType；对应50处API调用与36条枚举提示，不能说86次实际查询。First→Any可能改变身份选择；inactive参数和稳定ID/scene过滤须保留，未经授权不机械迁移。
- 3条CS0414：PlayerInventory.nearest/nearestEvent只有声明及null赋值，交互已由InteractionResolver负责；ThirdPersonHero.nextAttack只有0重置，实际冷却AdventureCombat.attackAt。private非序列化字段；未发现字面名称反射读取，不将静态搜索当作所有动态反射的证明。当前无已确认运行损害；以后清理仍需交互/冷却回归。
- 2条场景版本：Boot.unity与Title.unity的GameObject fileID1000缺serializedVersion，按legacy1读取低于最小6；Transform版本2是不同块。当前冷导入/标题可运行，但有将来序列化迁移风险。原场景未重存，不操作用户ForestRuins来消警告。

风险分布：**阻断0 /高0 /中18 /低37 /信息36**，均仍OPEN，审计完成不等于缺陷关闭。信息级枚举与对应API关联，不抹掉API本身风险。没有确认需立即修改产品的高风险缺陷，后续迁移应另行授权。

所有临时采样构建警告另存BuildReport，不混入91条；V3/V4均0错误120警告。导入期JobTempAlloc15条、native-target-extension20条、assembly-hint-path20条为五次构建日志索引，不混入BuildReport91。完整原日志保留；Search/UNKNOWN在这些样本未出现不能推导历史根因已解决。运行时URP后处理shader不可用另列[runtime-diagnostics](Evidence/Run-1027-224456/runtime-diagnostics.json)，不删日志，不临时切换渲染设置伪造更好性能。

## 失败、保护与开放项

见[FAILURE_HISTORY](FAILURE_HISTORY.md)。后退出文件占用通过sidecar输出分离解决；升级模态只在临时驱动中通过真实Digit1输入处理。原PLAYER02驱动未改，原失败日志/截图、V1～V4源码与所有尝试完整保留；没有强杀超时进程，测试结束后再做分析和压缩。

用户原始文件及1152项产品输入最终逐项比对，证据见source-protection；仅提交获准ProjectDocs工具/证据，不提交场景、设置、Recovery、二进制或Library。没有新游戏玩法测试被旧PASS顶替；本轮实际采集、战斗、扣费、结算、制造、出征和恢复证据与历史规则矩阵分开，未重跑的全旧存档/四武器/原生矩阵不宣称通过。

保留D3D12 UNKNOWN、Editor青色帧、Editor.Search、JobTempAlloc根因UNRESOLVED；原生U16/独立人工/性能预算验收NOT_RUN。后台虚拟输入、Application.Quit和受控截图不替代标题栏关闭/人工试玩。完整无观测发行包游戏性能、纯地图生成、GC Alloc/可用显存、因果热点仍待后续工具或获准实验；本批交付后暂停等待固定SHA独立复审，不自动优化警告或进入新批次。

[验收表](ACCEPTANCE.md) · [复跑](TESTING.md) · [冻结口径](METRICS_POLICY.md) · [证据索引](Evidence/INDEX.md)
