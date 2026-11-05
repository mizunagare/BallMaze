# R6 证据索引

验证根 I:/WGCombat/C1R6-1105-A。两份原始发行包留在 I:/WGCombat/C1R3-1105-A 下的 ProjectA-Build/Release 和 ProjectB-Build/Release。所有原图保留字节。发布清单逐项给出本地原始和仓库发布 SHA256，日志和较大的指标用 gzip。PDB、包二进制和合成存档正文只留隔离盘。[证据清单](manifest.json) · [保护核验](protection.json)

- [七机位示例对照图](ComparisonFinal/montage.png) · [全量 1,330 对数据](ComparisonFinal/metrics.json.gz) · [分布与逐帧记录](ComparisonFinal/summary.json) · [差分图目录](ComparisonFinal/)
- [基础批次](batch.jsonl.gz) · [阴影独立批次](isolated.jsonl.gz) · [诊断 A 遗迹](Frames-A-ruins-isolated-1/) · [诊断 B 遗迹](Frames-B-ruins-isolated-1/)
- [GraphicsSettings 序列化对象](graphics-payload.json) · [原生 A](Frames-A-camp-native2/native-readback.jsonl.gz) · [原生 B](Frames-B-camp-native2/native-readback.jsonl.gz) · [原生偏移与默认](native-offset-evidence.txt) · [渲染资源](render-object-hashes.json)
- [无驱动纯 A 标题](PureBootA/title-player.png) · [无驱动纯 A 回执](PureBootA/pure-runtime.json) · [无驱动纯 B 标题](PureBootB/title-player.png) · [无驱动纯 B 回执](PureBootB/pure-runtime.json)
- [R5 历史证据](https://github.com/mizunagare/BallMaze/blob/f21f807fb39f38653d7d3a5d9a3e3371936fedbe/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR5/Evidence/INDEX.md)

| 轮次 | A 标题与营地 | A 遗迹五区 | B 标题与营地 | B 遗迹五区 |
| --- | --- | --- | --- | --- |
| 01 | [截图、帧号、状态](Frames-A-camp-01/) | [截图、帧号、状态](Frames-A-ruins-01/) | [截图、帧号、状态](Frames-B-camp-01/) | [截图、帧号、状态](Frames-B-ruins-01/) |
| 02 | [截图、帧号、状态](Frames-A-camp-02/) | [截图、帧号、状态](Frames-A-ruins-02/) | [截图、帧号、状态](Frames-B-camp-02/) | [截图、帧号、状态](Frames-B-ruins-02/) |
| 03 | [截图、帧号、状态](Frames-A-camp-03/) | [截图、帧号、状态](Frames-A-ruins-03/) | [截图、帧号、状态](Frames-B-camp-03/) | [截图、帧号、状态](Frames-B-ruins-03/) |
| 04 | [截图、帧号、状态](Frames-A-camp-04/) | [截图、帧号、状态](Frames-A-ruins-04/) | [截图、帧号、状态](Frames-B-camp-04/) | [截图、帧号、状态](Frames-B-ruins-04/) |
| 05 | [截图、帧号、状态](Frames-A-camp-05/) | [截图、帧号、状态](Frames-A-ruins-05/) | [截图、帧号、状态](Frames-B-camp-05/) | [截图、帧号、状态](Frames-B-ruins-05/) |
| 06 | [截图、帧号、状态](Frames-A-camp-06/) | [截图、帧号、状态](Frames-A-ruins-06/) | [截图、帧号、状态](Frames-B-camp-06/) | [截图、帧号、状态](Frames-B-ruins-06/) |
| 07 | [截图、帧号、状态](Frames-A-camp-07/) | [截图、帧号、状态](Frames-A-ruins-07/) | [截图、帧号、状态](Frames-B-camp-07/) | [截图、帧号、状态](Frames-B-ruins-07/) |
| 08 | [截图、帧号、状态](Frames-A-camp-08/) | [截图、帧号、状态](Frames-A-ruins-08/) | [截图、帧号、状态](Frames-B-camp-08/) | [截图、帧号、状态](Frames-B-ruins-08/) |
| 09 | [截图、帧号、状态](Frames-A-camp-09/) | [截图、帧号、状态](Frames-A-ruins-09/) | [截图、帧号、状态](Frames-B-camp-09/) | [截图、帧号、状态](Frames-B-ruins-09/) |
| 10 | [截图、帧号、状态](Frames-A-camp-10/) | [截图、帧号、状态](Frames-A-ruins-10/) | [截图、帧号、状态](Frames-B-camp-10/) | [截图、帧号、状态](Frames-B-ruins-10/) |

## 复跑

从冻结包复制到新的隔离根，按原包 Managed 引用编译 RenderProbe.cs.txt 和 DiagnosticProbe.cs.txt 为 C1R6RenderProbe.dll，分别加入 RenderA/B 和 DiagnosticA/B 副本。编译引用包括 mscorlib、netstandard、System、System.Core、Assembly-CSharp、Unity.RenderPipelines.Core.Runtime，以及 UnityEngine 的 Core、ImageConversion、ScreenCapture、Animation、ParticleSystem、Physics 和 UI 模块。仅在副本的 ScriptingAssemblies.json 注册程序集，在 RuntimeInitializeOnLoads.json 注册 C1R6.RenderProbe.Run，loadTypes=0。不要改动原包。

使用 Invoke-Render.ps1 的 Label 和 Mode 逐个交错执行 A/B，Attempt 为 01–10。阴影诊断另用 Intervention 与 DiagnosticCopy 参数，Attempt 为 isolated-1 和 isolated-2。Compare-Captures.py 接收隔离根与 ComparisonFinal 输出子目录，使用 NumPy 2.3.5 和 Pillow 13.0.0。启动跟踪前对照 Player PDB GUID 和 age，先启动 Native-Graphics.py 监视指定新运行目录，再以 Invoke-Render.ps1 启动拥有的独立桌面进程。Read-Graphics.py 使用 UnityPy 1.25.0 对原始纯包读出 PSO 载荷。原图和原始日志保留，证据发布由 Publish.py 生成双哈希清单。[取证工具](../Tools/) · [失败历史](../FAILURE_HISTORY.md)
