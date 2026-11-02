# UnityConnect 原生路径与发行风险

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

字段+0x68的含义另由命名为SetEnableCloudDiagnosticsReporting的本机setter写入指令确认，非仅凭字段位置猜测：[字段证明](Evidence/Raw/native-cloud-field-proof.json)。本批没有调用该setter。
