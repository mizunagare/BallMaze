# COMBAT-01-R1 证据

本轮：[Run-1028-112303](Run-1028-112303/Analysis2/analysis.json)，开工SHA `be448f56cb629022047c5de35ca3bfb03eac7604`。最终SHA为本索引所在提交；推送不等于复审通过。

| 内容 | 路径 | 口径 |
|---|---|---|
| 31项独立核账 | [Analysis2/analysis.json](Run-1028-112303/Analysis2/analysis.json)、[checks.csv](Run-1028-112303/Analysis2/checks.csv) | 真实文件、句柄回执、输入与业务证据，不是退出码汇总 |
| 前摇与恢复时间线 | [startup-timeline.csv](Run-1028-112303/Analysis2/startup-timeline.csv) | 每行标PID，不跨进程混算模拟时间 |
| 两阶段与实际退出 | [Story1-stages.json](Run-1028-112303/Inputs/Story1-stages.json)、[Attempts](Run-1028-112303/Attempts/) | PID74944与75392，独立StorageAfter和实际native-exit回执 |
| F5前后与恢复观察 | [Story1](Run-1028-112303/Story1/) | actionId/Startup/pending、HP、弹体、冷却、库存/来源账；退出前不等待截图 |
| 新协议完整样本 | [Close2](Run-1028-112303/Close2/)、[Close3](Run-1028-112303/Close3/) | 独立窗口/进程/宿主观测，非原生标题栏 |
| 退出判据 | [Close3/Observer/timeline.jsonl](Run-1028-112303/Close3/Observer/timeline.jsonl)、[exit-observer.json](Run-1028-112303/Close3/Observer/exit-observer.json) | 先持有句柄再请求，独立记录PID缺席但不当退出证明 |
| 产品退出审计 | [entry-audit.jsonl](Run-1028-112303/Close3/entry-audit.jsonl)、[native-exit.json](Run-1028-112303/Close3/player.desktop-process.json.native-exit.json) | title-quit与实际子进程信号/退出码0双证据 |
| 工具初次失败 | [Close1](Run-1028-112303/Close1/) | net8缺失原stderr/退出码，后续Observer2另目录保留，不重写旧失败 |
| 188条新运行 | [Rules/combat01.json](Run-1028-112303/Rules/combat01.json)、[test-fork.json](Run-1028-112303/Rules/test-fork.json) | Editor batch受控，公开初始化接线；断言未删，不冒充Player |
| 构建/驱动边界 | [ProductIdentity](Run-1028-112303/ProductIdentity/)、[T](Run-1028-112303/T/) | 新验收0错133警告；143程序集，发行同SHA无驱动 |
| 全部警告 | [warning-inventory.json](Run-1028-112303/Inputs/warning-inventory.json) | 93既有产品/构建、40验收驱动；全部OPEN未过滤 |
| 纯发行复用身份 | [release-provenance.json](Run-1028-112303/Inputs/release-provenance.json)、[full-release-hashes.json](Run-1028-112303/Inputs/full-release-hashes.json) | 191文件一致；不是本轮重建声明 |
| 用户/产品保护 | [Inputs](Run-1028-112303/Inputs/) | 1152项产品和5项用户文件哈希，未复制用户场景内容 |
| 固定SHA旧失败原件 | [History](Run-1028-112303/History/) | 原COMBAT矩阵、C15/C16/额外启动失败，Git原字节与SHA |
| 原件清单 | [manifest.json](Run-1028-112303/manifest.json) | 280原件，发布与原始SHA；`.log.gz`无损解压 |

`python -B verify_evidence.py Evidence/Run-1028-112303`可在不依赖原I盘目录的环境复核发布字节、前摇真实保存、v9校验和、恢复和退出回执。必须先取得仓库LFS原件；不把Git LFS指针当PNG。它不是Windows重新运行或当前用户文件复查，原机完整审计另见audit_r1.py。

原生U16、人工、完整性能仍NOT_RUN，六项历史原因仍UNRESOLVED。新成功样本不能回写旧失败；完整条目见[验收](../ACCEPTANCE.md)。
