# PERF-02 测量能力与观测开销验证

## 基线与修改范围

开工本地/远端main实读均为`94dcc009ff971272fc46d8c5b323cbb3251619b5`。用户PERF01固定SHA复审原文及[限定结论](Reviews/PERF01_ARCHIVE.md)已归档：声明范围内有条件接受，不是性能达标/瓶颈定位/91警告修复，复审方没有独立Windows重跑。本批最终交付SHA由推送后远端核对的固定链接/交付块给出，不能把开工SHA当最终工具SHA。

只新增ProjectDocs内工具、文档、证据并增量更新开发计划，未修改旧PERF01证据或产品Assets、场景、ProjectSettings、包、v9合同和玩法。源输入1152项含用户ForestRuins/ProjectSettings/Recovery覆盖层，最终全部字节一致，覆盖层仅发哈希，不上传正文。不是纯Git场景的无条件复现。

唯一外部根`I:/WGP2/1028-080504-eef74f`；D盘开工约1.2GB空闲，因此改用I盘短路径，没有删除旧证据或用户程序。复用BUILD01冷导入/私有非活动桌面/资源保护与PLAYER02启动前隔离/输入/退出回执。三份全新Library的临时非开发验收包，BuildOptions.None：A/B各0 Error、116 Warning，C为0 Error、118 Warning，完整BuildReport及日志保留。原91条产品警告仍在；多出的25/27条来自临时驱动，不混入91项。

同i5-12400F、RTX3060、约48GB内存、Win11环境，实际运行均1280×720、PC、D3D11、VSync0、targetFrameRate=-1，10秒预热/60秒窗口。没有切API、降画质、修改系统/快捷键或激活桌面。`inputDesktopActive=false`与Unity内部focused=true均记录。采样不是物理键鼠或人工试玩；Application.Quit不等于标题栏关闭。设备、驱动、源码/工具/程序集/EXE SHA见原始证据。

## 实际执行与开销

三轮按ABC/BCA/CAB顺序，**9个独立窗口全部完成**；另有3个独立能力探针、2个有新线索的GPU定向诊断，共14个Player进程。真实OS退出均0、未超时、没有强杀；能力接口不可用仍如实判不可用，不从进程成功推导指标PASS。所有为Missing合成目录，只显示真实Title，不建立Profile/Run、不给物品、不改正例档。

- A无额外逐帧采样器/Recorder，FTM标志关闭，仅共同两次边界和原PLAYER02驱动。因此A内部CPU主/渲染/GPU/帧间隔分布NOT_RUN，不能为了填表添加Observer或用平均值伪造分布。边界Win32 CPU/工作集/私有内存、GC0、托管内存与帧数变化有效。
- B仅FTM/帧间隔/自身计时，预热前分配200000行numeric struct缓冲，结束后写CSV，3次均无溢出。没有完整Recorder/逐帧字符串/系统sidecar。
- C复用PERF01完整采样器、系统sidecar，窗口外做实际GPU身份与DXGI边界。C的CSV、字符串、Recorder与查询压力也是观测开销；自己的临时纹理只用于预热前/独立探针，释放明确归属资源，不触及产品生命周期。

每例P50/P95/P99、缺失、离群、内存和CPU时间见[逐进程表](Evidence/Run-1028-080504/Analysis/MEASUREMENTS.md)、[JSON](Evidence/Run-1028-080504/Analysis/summary.json)、[CSV](Evidence/Run-1028-080504/Analysis/summary.csv)。原始> P99的18892个指标/帧索引全部保留，不删除离群数据。

描述性结果：A每60秒GC0增量12～15，B为5～6，C为350～424。B自身采样P95约2.3～2.4微秒，C约45.7～56.8微秒。两者计时覆盖不同，B不含结束后CSV，C也不含全部独立sidecar成本；sidecar自身CPU累计未测量，NOT_RUN。大缓冲预分配改变堆/GC阈值，代码体积、FTM构建标志、系统负载也不同；不能从差值归因产品分配率或精确工具总成本。

进程CPU累计包含所有线程，可超过墙钟60秒；A约142266～151031ms，B约145719～148984ms，C约146344～155344ms。B主线程FTM P95为0.8444～0.8767ms，C为0.7993～1.0342ms，不呈稳定单调关系。不能据此声称C更快、更慢或性能达标。样本n=3、后台私有桌面且硬件非独占，没有目标预算；这不是无观测发行包的性能证明。

## GC能力

实际枚举GetAvailable名称/category/unit/句柄；记录Default和CollectOnlyOnCurrentThread、Valid/Running/Count/CurrentValue/LastValue。主线程零动作/每步65536字节payload各8步，分别同帧/下一帧/EndOfFrame；后台线程零动作和16×65536字节payload，线程ID、完成/join状态单列。zero-action仅指探针不主动分配，全游戏/日志仍可能分配。

五次探针中已知主/后台分配实际完成，但`GC.GetAllocatedBytesForCurrentThread`已知正分配仍返回0；`GC Allocated In Frame`、`GC Alloc`、Internal `GC.Alloc`默认及current-thread Recorder均无效、Count0。结论：**所测试的非开发6000.6.5f1 Mono接口在本环境不能可靠给出逐帧/逐线程分配字节，NOT_RUN/UNAVAILABLE**。不是零分配通过，也不是所有Unity平台/开发包都不支持。

GC Used/Reserved Memory属于堆量，不当作分配字节；Windows工作集/私有内存只是独立交叉观测，不替代GC Alloc。GC0确有变化，但工具自身分配无法剥离，不能称为产品已确认GC瓶颈。

## GPU时间、适配器与显存

FTM在B/C均取得有效GPU子集；重复timestamp、无新值、非正值保持原始缺失，不CPU填GPU。`GPU Frame Time` Recorder取得TimeNanoseconds正值子集；`FrameTime.GPU`虽句柄可用，却没有可靠正值，不能把0解释为无GPU工作。Probe检查点会重复同一帧，不冒充持续60秒独立帧分布；API可能共享引擎后端，不能当成独立硬件验证。**完整逐帧GPU覆盖仍UNRESOLVED**。

本机枚举出多个同名RTX3060逻辑适配器及软件适配器，不能靠名字或WMI的溢出AdapterRAM猜测实例。C从自己临时2×2纹理的实际D3D11设备取得IDXGI adapter LUID，均为`000000000001253a`；按该LUID匹配查询，不释放借用的Unity纹理指针，只释放新取得的COM引用。A/B没有做该原生LUID查询，NOT_RUN，不能声称A/B也已独立确认同一逻辑适配器。

C的3个窗口及5次探针均取得匹配的DXGI node0 local/nonlocal CurrentUsage与预算，独立字段保留设备容量。CurrentUsage是当前应用段用量，Budget是OS分配给应用的预算，**不是整张卡的剩余/可用显存**。定义依据：[Microsoft QueryVideoMemoryInfo](https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgiadapter3-queryvideomemoryinfo)，接口边界以本轮实际HRESULT/身份为准。

初版sidecar的PDH ErrorAction Stop在批次含无效样本时整体抛错，原始日志完整保留。随后一次Continue单样本、一次双样本的定向诊断保留所有样本状态/错误。单样本已取得实际LUID有效样本11条，双样本12条；退出附近无效值及软件适配器的合法零用量分开记录，均不冒充实际GPU零用量。额外诊断不替换9个窗口，也不称已修复原窗口的PDH时间序列。

WMI过滤查询和无过滤后client PID筛选均有当前正例。顺序查询的缓存/时间不同，不要求逐字节相等，不反推PERF01历史失败根因；尾部抽查不可代表整轮。能力及所有GPU候选详见[capabilities](Evidence/Run-1028-080504/Analysis/capabilities.json)。动态计数器在进程退出前后可能无效，这些原始错误不吞掉；整个设备真正剩余显存、A/B唯一LUID和完整GPU覆盖仍未取得。

## 警告、失败与保护

最多3类只读语义审查：枚举/排序72条关联诊断、First身份14条、CS0414字段3条，共89条；剩余2个场景版本警告保持旧结论，不继续扩第4类或重存用户场景。详见[SEMANTIC_REVIEW](SEMANTIC_REVIEW.md)、源码SHA/行列/上下文JSON。所有91条仍OPEN，中18/低37/信息36，不机械换API，不用静态警告数推断每帧调用或已确认瓶颈。

保留初次owner斜杠拒绝、外部.NET校准签名失败、初次PE空namespace点的断言失败、PDH部分样本失败及所有重试；见[FAILURE_HISTORY](FAILURE_HISTORY.md)。PE只是类型边界：A无额外采样器，B只有Minimal，C才有Full/Probe/DXGI；三个包均无UnityEditor引用，仍全部是临时带驱动验收包。

所有拥有者进程结束后才分析/归档；首次5项数学测试保留，最终新增无效0/合法0/错误适配器/非有限值检查，共7项通过。1152项产品源输入全部未变，未上传用户场景/设置正文、真实档、Player二进制或Library。原生U16/独立人工/预算仍NOT_RUN；D3D12 UNKNOWN、Editor青色帧、Search、JobTempAlloc根因仍UNRESOLVED，本轮没有重做无新线索关闭实验。

交付仅表示测量能力已核实并准确界定；等待固定SHA独立复审，不自动清零警告、优化产品或进入新地图/新批次。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md)
