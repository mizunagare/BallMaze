# PERF-02 采样前冻结口径

基线94dcc009ff971272fc46d8c5b323cbb3251619b5，只有ProjectDocs中新工具/证据；用户产品输入1152项单独冻结，原档不访问。I盘新短路径、全新Library，Unity6000.6.5f1/Mono/D3D11，原画质/分辨率不变。所有构建为BuildOptions.None临时验收包，不是无驱动发行包。复用PLAYER02私有非活动桌面和退出/指纹机制，不原生输入、不强杀。

## A/B/C

相同Missing合成输入、Title不操作、不创建Run；1280×720/PC/原VSync和帧率，预热10秒、窗口60秒，各3独立进程，以ABC、BCA、CAB顺序轮换（有失败就保留）。构建完成后才测量，不与编译同时运行。

- A：不注入逐帧采样器、不创建额外Recorder，FTM构建标志关闭。只有相同PLAYER02输入/退出驱动与两个共同边界快照；不能为了填表再加入逐帧Observer。A内部CPU/GPU/帧间隔分布NOT_RUN；可比较窗口帧数、代0集合变化、Windows真实进程CPU时间、工作集/私有内存和托管内存边界。
- B：仅FTM、帧间隔、固定numeric struct缓冲、探针自身耗时，窗口内不串行化/写CSV/查找对象/额外GC recorder/系统sidecar。缓冲在预热前分配，结束后写盘；记录容量与溢出，不动态扩容掩盖丢样。FTM构建启用。
- C：PERF01完整采样器原文及独立系统sidecar；新增PDH/WMI可用性日志；C在窗口外查询DXGI和实际Unity设备LUID。记录这些配置差异，不能将差值简单称因果；完整Recorder/CSV/系统探针的压力也属于被观察对象。

共同边界是两次固定成本观测：UTC/单调时钟、frameCount、GC0、Mono/Unity内存、Win32 GetProcessTimes/GetProcessMemoryInfo。不用Mono返回0的进程内存实现，不把进程/托管堆增量当作GC分配字节。A没有逐帧数据是设计边界，不从均值伪造逐帧分布。

## 能力探针

C独立Probe进程，不与A/B/C稳态窗口混算。枚举GetAvailable名称/category/unit/Valid；显式尝试实际可用GC/GPU项及Memory GC Alloc/GC Allocated In Frame/Internal GC.Alloc，默认和current-thread两种选项分别留证。每个主线程zero-action/64KiB payload步骤记录同帧/下一帧/EndOfFrame；后台线程零动作与16×64KiB payload、线程ID及前后帧单列。全游戏继续分配，zero-action只指探针不主动分配，不能当作全进程零分配。对象头/对齐不是payload，不能用大小差推断字节精确；观测对象/日志本身也有分配。

Recorder无效/Count0、时间覆盖不到、单位非Bytes、已知分配仍0分别记录。API在已知正分配下失败时，其zero结果不能证明零分配。不可用用NOT_RUN/UNAVAILABLE；不把Windows工作集或Mono堆变化当成GC分配替代。

## GPU与显存

FTM保留timestamp、是否新值、非正/缺失、原始CPU主/渲染/GPU值和约4帧延迟；不CPU填GPU。Recorder名称/单位/Count/Valid原样保存。PDH按真实PID筛选，保留所有实例名及Status/原始值、LUID；WMI无过滤全查询后按PID匹配，与旧过滤失败单列。错误不变0。DXGI query在拥有者进程内，local/nonlocal CurrentUsage与OS应用预算、设备capacity分别报告，预算余量不是整张显卡的剩余显存。

多个同名RTX逻辑适配器时，C用自己2×2临时纹理取得D3D11设备→IDXGI adapter LUID；不释放借用的Unity原生纹理，只释放新取得的COM引用。只在预热前/能力探针做此读查询，自己的纹理随后Destroy；不改产品生命周期或关闭逻辑。若LUID/计数器对应不唯一或HRESULT失败，保持UNAVAILABLE/UNRESOLVED。

## 统计与证据

P50/P95/P99用线性插值，各进程单列；记录n、缺失/重复/nonpositive、min/max与>P99帧索引。无效/超出窗口/失败/溢出全部保留。不同API、线程、版本、构建、窗口不可混合为一个分布。没有硬件预算，不宣称性能达标；没有原生UI/独立人员仍NOT_RUN。91警告只读最多3类别（对象枚举排序、First身份、CS0414字段），全部仍OPEN；场景版本不再扩展审查或重存。
