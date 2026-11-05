# R5 证据索引

冻结基准 8a4ce422f97174160662e8f9acb7982e9d68502b。隔离验证根 I:/WGCombat/C1R5-1105-A。原始两套发行包在 I:/WGCombat/C1R3-1105-A 的 ProjectA-Build/Release、ProjectB-Build/Release。发布证据清单为每件文件保留原始 SHA256、发布 SHA256、大小和脱敏标记。日志及跟踪 JSONL 使用 gzip，PNG 保留原始字节。[证据清单](manifest.json)

## 原生配置写回

- [原生写回报告及两文件完整配置](../NATIVE_SETTINGS_AUDIT.md) · [符号化调用栈](Audit/symbolized-writebacks.json) · [符号身份](Audit/pdb-identity.json)
- [冷导入进程回执](NativeProject-Import/process.json) · [导入写回记录](NativeProject-Import/writes.jsonl.gz) · [构建进程回执](NativeProject-Build/process.json) · [构建写回记录](NativeProject-Build/writes.jsonl.gz)
- [构建摘要](Audit/traced-build.summary.txt) · [Bee 输入](Audit/traced-build.bee.json) · [发行回执](Audit/traced-build.release.json) · [完整日志](NativeProject-Build/Unity.log.gz)

## 运行画面

| 轮次 | A 营地和标题 | A 遗迹 | B 营地和标题 | B 遗迹 | 同机位 A/B |
| --- | --- | --- | --- | --- | --- |
| 1 探索 | [原图、TSV、进程](Frames-A-camp-1/) | [原图、TSV、进程](Frames-A-ruins-1/) | [原图、TSV、进程](Frames-B-camp-1/) | [原图、TSV、进程](Frames-B-ruins-1/) | [拼图](RenderComparison1/montage.png) · [差异数据](RenderComparison1/pixel-metrics.json) |
| 2 固定条件 | [原图、TSV、进程](Frames-A-camp-2/) | [原图、TSV、进程](Frames-A-ruins-2/) | [原图、TSV、进程](Frames-B-camp-2/) | [原图、TSV、进程](Frames-B-ruins-2/) | [拼图](RenderComparison2/montage.png) · [差异数据](RenderComparison2/pixel-metrics.json) |
| 3 同包控制 | [原图、TSV、进程](Frames-A-camp-3/) | [原图、TSV、进程](Frames-A-ruins-3/) | [原图、TSV、进程](Frames-B-camp-3/) | [原图、TSV、进程](Frames-B-ruins-3/) | [拼图](RenderComparison3/montage.png) · [差异数据](RenderComparison3/pixel-metrics.json) |

- [A/A、B/B 和四组 A/B 复跑矩阵](Audit/repeatability.json)
- [无取证驱动纯 A 截图](PureBootA/title-player.png) · [纯 A 回执](PureBootA/pure-runtime.json) · [无取证驱动纯 B 截图](PureBootB/title-player.png) · [纯 B 回执](PureBootB/pure-runtime.json)
- [保护文件与历史证据](Audit/protected-inputs.json) · [发行哈希与 Bee 核对](Audit/release-protection.json) · [五项运行时差异及三项辅助文件差异](Audit/release-differences.json)

## 复跑

使用全新的本机隔离验证根。原生跟踪以冷工程运行 Invoke-NativeEditor.ps1 的 Import，再运行 Build，使用 Trace-Native.py 和 Trace-Native.js 附加到隔离 Editor，随后用 Symbolize.py 对 exact-match PDB 解符号。构建输入清单与进程启动参数保存在各阶段证据目录。Verify-Evidence.py 检查 PDB 身份、纯包和取证副本哈希、两包 Bee 设置及历史保护文件。

跨场景用各纯包副本的程序集作编译引用，将 RenderProbe.cs.txt 编译成 C1R5RenderProbe.dll 并仅在两份取证副本的 ScriptingAssemblies.json、RuntimeInitializeOnLoads.json 注册。Invoke-Render.ps1 按同一输入分别运行 A/B 营地和遗迹，重复两次取最终同包控制。各进程 fixture.json 保留合成档来源与哈希，Player.command.json 保留实际进程参数。Compare-Frames.py 生成每轮像素指标与差分图，Compare-Repeatability.py 比较最终四份取证进程样本。不得在原始发行目录附加驱动。 [取证工具](../Tools/)

[验收表](../ACCEPTANCE.md) · [失败历史](../FAILURE_HISTORY.md)
