# PERF-02 失败历史与限定诊断

原PERF01所有失败/补跑/校准原样保留，不覆写。本批所有失败与后续结果独立归档。

1. 初次A构建启动前，Host owner.source使用正斜杠，复用的SafePath返回反斜杠，严格拥有者比较拒绝，未启动Unity。只规范化隔离owner路径后在新构建目录重试；不放宽拥有者验证。
2. 外部.NET DXGI校准首次Add-Type因较新.NET签名将ref对应in的CS9191诊断视为编译错误。原始校准源码/错误回执保留；外部校准使用.NET的in签名，实际Unity Mono引用仍用ref签名。没有过滤编译日志或降低诊断。外部pwsh的CurrentUsage不当作Player结果。
3. 能力探针已知分配API返回0：后台线程16×64KiB payload确实执行完成，但GetAllocatedBytesForCurrentThread仍0；不是零分配通过。实际同帧/跨帧/main/current-thread/all-thread recorder的Valid/Count/单位另存，不用堆或进程增长代替分配字节。
4. PDH Get-Counter -ErrorAction Stop遇到部分无效样本会整体抛异常；先完整保留这一实验，不因该错误声称所有目标PID样本不可用。若继续诊断，必须保留所有原始Status/错误，并仅对确实有效的目标样本下结论；不能删错误或虚构0。

后续一次保留全部状态/错误的单样本诊断、一次双样本诊断均独立归档，不替换九个稳态窗口。初检只看退出附近尾部的无效样本；全量复核发现首部有效目标PID样本，纠正“整轮不可用”的过度概括。单样本已可读正值，不把双样本试验说成必须等待两个样本才能使用的根因修复。WMI本轮过滤与client筛选均有正例，无法反推PERF01历史失败的唯一根因。

5. 首个PE类型断言失败：旧metadata reader对空namespace输出`.Perf02Minimal`，初版精确比较`Perf02Minimal`没有去除前导分隔点。保存初始失败及三份完整PE原件；只规范化空namespace点，A/B/C类型集合预期不变，重审通过。不改运行时、构建或放宽类型边界。

完整矩阵、后续诊断、实际退出码和超时记录以Evidence原始目录及REPORT为准；没有强杀，没有把技术中断记成死亡或正常退出。产品/依赖/真实档未因这些工具问题修改。
