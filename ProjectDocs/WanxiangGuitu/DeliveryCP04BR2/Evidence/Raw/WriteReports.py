from pathlib import Path
import json
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04BR2');r=Path('I:/WGCombat/CP04BR2-1102-A')
(p/'.gitattributes').write_text('Evidence/** -text whitespace=cr-at-eol\nTests/** -text whitespace=cr-at-eol\n*.py -text whitespace=cr-at-eol\n*.ps1 -text whitespace=cr-at-eol\n')
(p/'.gitignore').write_text('__pycache__/\n*.pyc\n')
(p/'REPORT.md').write_text('''# CP04-BR2 专项调查交付

基准 `d8fede51ba719060c1d1f719295ce40bb21768d0`；独立分支 `verify/cp04-staff-acceptance-br2`。产品仍是 cc9 的 CombatAim 修复，main 仍为 `72db192a527bd256e2ba18cd7ab334d8334051da`。本文件所在最终提交为复审输入，完整 SHA 由提交后回执给出。不合并 main，不修改产品。

## 结果

|专项|状态|结论|
|---|---|---|
|本机 native 写回路径定位|PASS（限定样本）|匹配 PDB/二进制 + 原生反汇编 + 活体谓词对照，定位构建回调及 CrashReporting/EngineDiagnostics 桥接；未采集硬件写入断点调用栈|
|Bee Services 绑定|PASS|UnityConnect=true、CrashReporting=true、Insights=true；Analytics/PerformanceReporting=false，已按本轮目标输出路径筛选|
|实际外部发送/完整发行行为等同性|UNRESOLVED|标志和发送能力不能证明网络实际载荷、同意状态或所有条件下行为相同|
|Editor 分配来源|PASS|232/232作用域、校准通过，解释2516→4460B的1944B差额|
|非开发测试Player逐调用分配方法|PASS|原生Mono回调在两个独立进程各完成152作用域，正/零/释放引用校准通过|
|CPU数据汇总|PASS（测量整理）|分清单次Solve、整帧和并发；采样模式不同不作速度提升结论|
|实际性能预算验收|NOT_RUN|目标设备/帧率/画质/预算尚未确定，不自行设阈值|
|产品和历史保护|PASS|2329保护文件、889 CP04-B历史文件、848 BR历史文件均无差异；规范化Aim IL也相同|

上述8项为6 PASS（含限定范围）、1 UNRESOLVED、1 NOT_RUN。**不是整体游戏验收通过**。原生UI、人工试玩和历史引擎问题未关闭，旧BR状态不追溯改写。

## 新证据

Unity 6000.6.5f1 安装中有匹配的 Unity_x64.pdb（GUID/age与Unity.dll一致）。`OnEditorBuildStartedStatic` 调用 `UpdateServiceRequestingCoreStats`，根据服务的实际 GetEnabled 与 requiresCore 标志写回聚合 enabled。本样本旧Cloud开关为0，但CrashReporting的原生覆写 getter考虑Engine Diagnostics，返回1，因此请求Core Stats。不是产品CombatAim代码启用云服务。[UnityConnect](UNITYCONNECT.md)

当前1.5m的4460B中：物理API返回数组336B，剩余4124B由闭包、LINQ、排序/迭代相关分配组成。两套独立采集通道结果一致。新增安全检查及最终命中路径解释1944B增量，不删除安全检查来降低分配。[分配分析](ALLOCATION_ANALYSIS.md)

提出单次Solve内复用重叠结果、去LINQ及有界NonAlloc缓冲的量化方案；均**未实施、等待另行授权**。没有改变真实释放、碰撞、伤害、随机流、经济或存档。[性能提案](PERFORMANCE_PROPOSAL.md)

## 运行与边界

- Allocation6：Editor真实产品Solve/公共helper，232作用域完整；不是战斗或人工测试。
- MonoPlayer、MonoPlayerRepeat：BuildOptions.None、测试专用define，两个新进程各152作用域，实际Mono分配事件；不是未插桩纯发行性能。
- 两次纯发行构建均0错/96警告；测试Player构建0错/97警告。全部警告、失败导出、编译缺依赖和预启动占用保留。
- 纯发行程序集没有BR2驱动及UnityEditor引用；测试程序集含BR2MonoProbe和测试原生桥引用。所有CombatAim方法规范化IL与BR纯发行一致，非影子实现。
- 本批没有重新运行完整战斗/原生输入/人工试玩，也不继承旧293PASS为本批PASS。

[验收](ACCEPTANCE.md) · [失败历史](FAILURE_HISTORY.md) · [复跑](TESTING.md) · [证据索引](Evidence/INDEX.md)。交付后暂停等待独立复审。
''',encoding='utf8')
(p/'UNITYCONNECT.md').write_text('''# UnityConnect 原生路径与发行风险

## 本机二进制身份

Unity 6000.6.5f1（3ff58d469c8a），Unity.dll SHA256 `c9f8a6d5aabdfa71292fd8a8ca5c2a6d5a1cb995e6b07c850ae5da91d631f0dd`；PDB GUID `a5bae209-dbcf-4cf7-b0fe-243d461992a0`、age1，与PE记录严格匹配。[身份](Evidence/Raw/native-identity.json)

仅只读本机安装文件与自己的隔离进程。未附加调试器到用户程序、未打补丁或写原生内存。工具中的原生对象偏移/虚表仅适用于此二进制，不是通用Unity API；版本、模块范围与VirtualQuery检查失败应停止。原生getter使用本机Windows x64 ABI，不跨版本套用。

## 已定位路径

首选基址0x180000000（实际进程ASLR地址换算后核对）：

1. `UnityConnectSettings::OnEditorBuildStartedStatic`（VA 0x182721310）调用 `UpdateServiceRequestingCoreStats`（0x182722030）。
2. 后者遍历native服务列表，调用虚表+0x20的实际GetEnabled，并检查service+0x11的requiresCore标志；有服务请求时取true，否则才回退AnalyticsSettings.RequiresCoreStatsInBuild。
3. 比较并写入this+0x478，再进入`Object::SetDirty`。`SetEnabled`的同一字段地址和原生getter值交叉验证了字段含义。
4. 本轮只有CrashReporting getter返回1，其他五项返回0；CrashReporting requiresCore=1。Analytics managed回调列表为空，故不是该回退路径导致true。

[反汇编](Evidence/Raw/native-disassembly.json)、[原生符号](Evidence/Raw/native-symbols.txt)、[callee解析](Evidence/Raw/native-callees.txt)、[服务虚表映射](Evidence/Raw/native-services.txt)。这些是匹配二进制的静态路径与活体谓词对照；**未采集CPU硬件写入断点栈**，不宣称所有Unity版本或所有构建路径唯一如此。

## 为什么旧开关0仍返回1

干净副本打开时，聚合enabled为false，普通服务的原始enabled字节均0。但CrashReporting的GetEnabled不是BaseConnectSettings.GetEnabled：它还考虑Insights的ComputeEngineDiagnosticsEnabled及活动构建配置/平台条件。

ControlBuild构建前：Crash原生getter=1、旧原始enabled=0，其他getter=0，聚合native字段0。进入BuildPipeline后聚合字段变1，各服务getter不变。后续只读GetterAudit确认旧CloudReporting原生+0x68字段=0，EngineDiagnosticsSettings.enabled=true、canUploadReports=true。原始源配置中`InsightsSettings.m_EngineDiagnosticsEnabled: 1`，普通Insights.m_Enabled为0。

因此本样本驱动是**CrashReporting的EngineDiagnostics桥接请求**，不能把普通Insights.m_Enabled=0误当作关闭引擎诊断。初期“直接Insights base getter为true”的假设已被原始0读数否定；未掩盖该诊断修正。

[干净打开](Evidence/Raw/ConnectOpenControl/Connect/001.json)、[构建前](Evidence/Raw/ConnectControlBuild/Connect/001.json)、[构建首次写回](Evidence/Raw/ConnectControlBuild/Connect/002.json)、[只读getter审计](Evidence/Raw/ConnectGetterAudit/Connect/001.json)、[Crash反汇编](Evidence/Raw/native-service-disassembly.json)、[子调用符号](Evidence/Raw/native-crash-callees.txt)。

两次纯发行均使用原产品配置的新隔离副本；没有手工改m_Enabled、EngineDiagnostics或用户ProjectSettings。五文件原字节与前后SHA在各运行Stages中。普通Open没有执行BuildPipeline；源输入相同的Build才重算聚合开关。

## Bee绑定与潜在行为

|Bee字段|实际读取来源|本轮值|
|---|---|---|
|EnableUnityConnect|UnityEngine.Connect.UnityConnectSettings.enabled|true|
|EnableCrashReporting|UnityEditor.CrashReporting.CrashReportingSettings.canUploadReports|true|
|EnableInsights|UnityEditor.EngineDiagnostics.EngineDiagnosticsSettings.enabled|true|
|EnableAnalytics|UnityEngine.Analytics.Analytics.enabled|false|
|EnablePerformanceReporting|UnityEngine.Analytics.PerformanceReporting.enabled|false|

[托管IL](Evidence/Raw/bee-services-il.json)、[严格匹配本轮DestinationPath的Bee输入](Evidence/Raw/bee-services-current.json)。最初的宽泛cache枚举含旧轮输入，已明确标为不可用的归属证据，不能当成本轮新构建。

这证明发行构建保留引擎诊断/崩溃上传能力，不证明某次运行已经发送数据，也不等于完整Analytics SDK已启用。源配置包含engine-data.unity3d.com与engine-data.services.api.unity.com等诊断端点；未主动制造崩溃、上传项目/存档或执行网络载荷抓取。

Unity官方说明，6.2起新项目默认支持诊断数据，运行时数据可包括崩溃、ANR、错误及核心遥测；具体收集受项目/框架设置控制。[官方说明](https://docs.unity.com/en-us/cloud/developer-data-framework/built-for-unity-6)

**UNRESOLVED**：纯发行实际网络请求、载荷、项目绑定和同意状态在各种错误/联网条件下的行为未实测；不能由标志或当前没有日志推断无外部影响。若要改变诊断策略，应另行授权处理真实EngineDiagnostics/BuildProfile配置并配对验证；不建议手工恢复派生m_Enabled为0后宣称等同性。
''',encoding='utf8')
print('report/native docs written')
