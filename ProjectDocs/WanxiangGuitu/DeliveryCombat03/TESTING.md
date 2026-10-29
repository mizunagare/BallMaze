# COMBAT-03 复跑

Unity6000.6.5f1，既有依赖不升级。使用新建 I:/WGCombat/<唯一名>，写 owner.json，保存远端完整SHA、git status、用户文件及历史证据哈希。禁止真实存档、关闭用户程序、激活用户桌面或强杀超时进程。不要复用本轮已有输出目录。

1. 沿用 DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly，SourceProject指当前工程、WorkProject指唯一根/P/Project，ArtifactsRoot指唯一根/Prepare。不要启动用户主工程；先检查Unity进程冲突。继承原启动前 -wanxiang-storage-root 与 Worker 隔离传输。
2. 所有测试 .cs.txt 只注入副本 Editor/B06LocalChecks，不放产品 Assets。使用本目录 Invoke-Measure.ps1 -Project <clone> -Output <new>/phase -Method <method>；它复用 DeliveryCombat02/Invoke-Combat02.ps1 与原 Step/Worker，而非新建编排框架。Worker默认依赖现有独立NativeProbe.dll；缺失应传入既有脚本支持的WorkerPath或记BLOCKED，不能退回用户桌面。
3. 基线只在闲置副本恢复开工85b8badc的三个产品C#。对Combat03Readability.Run先保留负例；Combat03Bench.Run测三种体型、四武器普攻／技能、重复Collider／遮挡／高低差和24场短战。main不回退。Before最初过大网格的失败留档；不要求复跑工具的已知超大负例以消耗时间。最终有限网格是源码中明确列出的.75/3/6/12米与左右30度、正面。
4. 同步当前三个产品C#后运行AfterReadability与After，再跑Combat03Bench.Contracts、Combat03Area.Run。Readability按品质检查5/7/9箭、侧球、真实范围与独立方向／身份、查询随机状态不变；Area分别验证直击、仅AoE、重叠、边界、遮挡、扇形多目标及Collider重复对照。范围单位与目标碰撞体尺寸须一起看。
5. 严格固定矩阵用Combat03Fixed.Run：通过既有Editor专用SetNextSeedForValidation(418)在实际Depart前指定种子，不直接改Run／奖励／最终存档。FixedBefore与FixedAfter各96样本；identity.json保留真实Run身份与完整初始流。Compare.py核对seed、流、装备配置与每个条件键，不以两次独立Run的GUID不同冒充恢复不一致。
6. 运行原COMBAT01规则的本轮执行副本：仅沿用已确认的枪BasicPower预期修正，其余断言不动。执行UX02BatchEntry.Combat；归档实际执行源，不能覆盖原DeliveryCombat01文件。再复用DeliveryCombat01/Invoke-Regression.ps1运行输入／观测／Boss与正常AI三进程，恢复其仅在副本内暂移的Deferred文件。前一依赖失败不能把后续标PASS。
7. 注入原Build01Audit，执行非开发Build01Audit.Run，保留完整build-report-messages.json和所有警告。Inspect-Build.ps1只读扫描真实Release各DLL的PE元数据与SHA，不加载产品代码，不冒充Player运行验收。
8. Combat03Bench.Visual对四武器同位置／相机／1280×720分别输出raw和controlled URP RenderRequest图。前后都是真实Editor，不是森林正常AI／原生键鼠／人工。恢复最终源后再执行FinalReadability，确认没有把基线产品留在副本。
9. python -B Compare.py <root>生成对照；python -B Collect.py <root> <repo>只发布本批拥有者根的证据。日志压缩并仅脱敏凭据值；源日志SHA与发布SHA分别记录。不得改旧aggregate、原输入和失败。

Run-Sequence.ps1、Run-EvidenceCompletion.ps1、Run-FixedPair.ps1记录本轮有依赖的调用顺序；它们假设已经准备相应基线副本与拥有者根，可参数化Project/RunRoot。完整命令、实际exit、timeout、各次输入副本在Evidence。内部测量650秒／外部1200秒，其他原规则／AI沿用原时限；超时诊断且不强杀，占用则停止复用。不可用的原生环境记NOT_RUN。

本轮原工具只固定布局418的尝试与严格固定Run418的尝试明确分开。短战每武器／体型仅n=2，不保证随机掉落初态一致，不作收益或平衡等价断言。基础属性、品质分支与临时位置/HP设置属于受控夹具，不冒充真实玩家胜利。

保护限制：本机运行输入包含用户未提交场景／设置，仅有哈希、不擅自上传；固定GitSHA不能单独重现这些本机差异。源与构建副本六个设置资产不同，见build-inputs，不要写成所有输入字节一致。编排器0、构建0或截图可见均不替代对应业务断言。
