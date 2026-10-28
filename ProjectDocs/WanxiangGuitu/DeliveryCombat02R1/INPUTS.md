# 冻结输入与重放边界

开工main/本地均为fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a，未发现后续提交。用户提供的复审认为COMBAT02剑枪改动仅在有限测量范围有条件接受，整批仍FAIL；本轮不自行认定独立复审通过。

|输入|值/来源|重放精度|
|---|---|---|
|原命令|Recovery-Run/B07Rules.Run.command.json；Unity6000.6.5f1，B07Rules.Run，非batch|保留原模式、600秒外层/360秒方法时限，替换工程外根/PID/桌面标识|
|原测试源|DeliveryCombat02/Evidence/B07Rules-before-diagnostic.cs.txt|按原字节SHA冻结，新增观察器单独记录；全部Need/Single表达式未变|
|原产品输入|前批product-inputs.json的358项，含115个C#|本轮源仓库逐项SHA一致；115个C#与副本一致，实际Editor产品DLL也与原C2缓存DLL一致|
|场景/设置/Recovery|5项开工SHA|源文件前后相同；未暂存或覆盖|
|原请求/接受seed|975140455/975140455；layout revision5、bossVersion1、generationVersion8、contentRevision B06-B4-R1、targetWave5|来自原b07-save后续加载后的存档，不冒称失败瞬间；通过已有Editor验证seed入口重放|
|原Run|7679a97700ea4e8ea8626431676475d9；ForestRuins；区域实例末尾:ForestRuins:1|保留身份作为证据，新进程新建真实合成Run，未伪造原Guid|
|原40次请求|1～40，原b07-nav.csv记录80个Boss路径，39个不同接受seed|本轮每次同时记录requested/accepted、attempt、fallback、failure列表；不补写旧缺失字段|
|预期Boss|boss:warden/Warden、boss:tide/Tide|稳定身份/语义不变；进程内EntityId和场景句柄按真实新实例记录|
|缺失状态|原故障瞬间内存/帧序、完整Unity全局随机初态、句柄、精确首帧耗时、未落盘状态|不能精确字节重放；本轮是同原seed和同产品/夹具操作的近似重放与因果对照|

原后续三次依赖加载会更新b07-save；因此original-save-metadata.json明确标记为事后资料，不作为故障瞬间快照。原始审计却已保留实际路径切换和读取顺序，为本轮复现提供独立历史佐证。

本轮根I:/WGCombat/R1-1028-A仅编译失败历史，B为业务诊断与修复对照。每个进程均有新合成存档，启动前显式-wanxiang-storage-root；默认启动写入的是该隔离根下WanxiangGuitu/ForestRuins，不是真实玩家默认目录。

原127个受保护发布文件/旧aggregate及59个原始源证据均哈希相同；旧4个exit1和旧aggregate-status.json仍保持原值。复制到本批OriginalReference只为查阅，不修改原件。

观察器前版对null Run的JsonUtility输出可能包含默认结构；判定使用AtCamp/Tracking及有效runId，不把空runId对象当真实Run。后版增补hasActiveRun存在标志及空路径保护，均为只读元数据改进，不作为产品状态修改。

最终普通夹具去除诊断和固定seed，另外保留batch显式初始化合同。旧共享准备脚本的原字节在Bindings/Invoke-Rules-before.ps1，当前只增加Stable注入映射，原历史B07源和运行输入不覆盖。普通中间版3次、最终版3次非batch及1次batch分别归档，不混入同seed3+3因果对照。
