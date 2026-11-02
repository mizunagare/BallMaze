# CP04-BR2 验收

专项调查交付完成，不宣称整体发行风险或性能验收通过。8项：6 PASS（限定测量/定位范围）、1 UNRESOLVED、1 NOT_RUN。

|项|状态|证据/边界|
|---|---|---|
|本机native写路径及触发服务定位|PASS|[身份](Evidence/Raw/native-identity.json)、[反汇编](Evidence/Raw/native-disassembly.json)、[原生getter](Evidence/Raw/ConnectControlBuild/Connect/001.json)；没有硬件写栈|
|Bee三项及Analytics区别|PASS|[明确DestinationPath](Evidence/Raw/bee-services-current.json)、[消费IL](Evidence/Raw/bee-services-il.json)|
|实际外部发送、同意及完整发行行为|UNRESOLVED|未抓取运行时请求/载荷，不从标志推断无影响|
|Editor分配来源和增量|PASS|[232作用域](Evidence/Raw/Allocation6/scoped-events.json)、[分解](Evidence/Raw/allocation6-analysis.json)|
|非开发测试Player方法有效性|PASS|[进程A](Evidence/Raw/MonoPlayer/mono-probe.json)、[进程B](Evidence/Raw/MonoPlayerRepeat/mono-probe.json)，各152作用域且独立校准|
|分层CPU汇总/量化提案|PASS|[数据](Evidence/Raw/cpu-current.json)、[提案](PERFORMANCE_PROPOSAL.md)；不是性能达标或优化已实现|
|性能预算验收|NOT_RUN|未获目标硬件、目标帧率、负载和预算，不自行设阈值|
|源输入/用户/历史保护|PASS|[2329+889+848保护](Evidence/Raw/protection-and-il.json)，Aim源码和规范化IL均一致|

新执行记录：Editor Allocation5 224/224、Allocation6 232/232；两个Player各152；离线工具自测12PASS。采样作用域不是游戏功能用例，不能与历史293PASS混算。

两次纯发行0errors/96warnings，非开发测试构建0errors/97warnings；[原始build](Evidence/Raw/ConnectBuild/build.json)、[control build](Evidence/Raw/ConnectControlBuild/build.json)、[probe build](Evidence/Raw/MonoBuild/probe-build.json)。纯发行无BR2驱动/原生桥引用，probe明确含测试驱动，见[桥依赖](Evidence/Raw/native-bridge-audit.json)。

未执行：无采集器纯发行逐Solve测量、完整并发战斗新基准、GPU专项、原生输入、人工体验。历史BR构建等同性、D3D12 UNKNOWN、Editor问题及所有旧失败不因本轮定位而被改写。产品优化方案待单独授权，本轮没有实施。
