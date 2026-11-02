# CP04-BR 证据索引

所有新运行独立保存。发布压缩不是覆盖原件；[manifest](Raw/manifest.json) 记录源文件及发布SHA、大小、脱敏标记。原件根 `I:/WGCombat/CP04BR-1102-A`。原始Profiler data/raw均gzip归档；原始二进制不上传，逐文件哈希清单可核对。

- [保护前清单](Raw/protected-before.json)、[历史清单](Raw/history-before.json)、[保护后](Raw/protection-after.json)。2329+889差异0，Aim完全一致。
- [冷打开](Raw/FixedOpen2/results.json)、[冷build](Raw/FixedBuildAudit/build.json)、[暖纯发行](Raw/FixedWarmPureBuild/build.json)、[修复验收build](Raw/FixedAcceptanceBuild/build.json)、[基线验收build](Raw/BaselineAcceptanceBuild/build.json)。每目录Stages含5文件原字节，Unity.log.gz含完整构建日志。
- [字段diff](Raw/field-differences.diff)、[阶段分析](Raw/build-phase-analysis.json)、[Bee实际services](Raw/bee-services.json)、[IL消费者](Raw/connect-consumer-field.json)、[只读包源码索引](Raw/package-source-audit.json)。
- [程序集剔除/IL](Raw/assembly-audit.json)、[二进制哈希](Raw/binary-manifests.json)、[冷暖对比](Raw/build-comparison.json)。
- [Fixed Editor逐作用域原数据](Raw/FixedScoped/scoped-events.json)、[Baseline](Raw/BaselineScoped/scoped-events.json)、[原Profiler fixed](Raw/FixedScoped/scoped-profiler.data.gz)、[原Profiler baseline](Raw/BaselineScoped/scoped-profiler.data.gz)。各目录command/desktop/exit/Unity.log.gz。
- [配对GC分布](Raw/editor-allocation-analysis.json)、[工具自测10项](Raw/allocation-tool-selftests.json)、[Player测量](Raw/FixedPlayers/PlayerProbe/probe.json)、[Player分析](Raw/player-performance-analysis.json)。
- [本轮Editor293断言](Raw/FixedEditorCore/presentation.json)、[真实进程](Raw/FixedEditorCore/CP03Editor.Run.exit.json)、[Player293断言](Raw/FixedPlayers/PlayerCore/presentation.json)、[Player真实进程](Raw/FixedPlayers/PlayerCore/CP04BRPlayerCore.exit.json)。
- [早期Profiler失败](Raw/FixedEditorProbe/profiler.raw.gz)、[reader失败](Raw/profiler-reader-failure.json)、[基线15分钟失败](Raw/BaselineEditorProbe/exception.txt)、[编译失败窗口](Raw/scoped-window-inventory.json)、[基线Player中断](Raw/BaselinePlayers/PlayerProbe/interruption.json)。不因普通关闭exit0改成PASS。
- [硬件](Raw/hardware.json)、[原生空表](Templates/native-input.csv)、[人工空表](Templates/human-playtest.csv)。空白表不是已执行结果。

旧 CP04-B 原数据仍在原交付目录，本批只读，不重复发布成新结果。所有分类与 [ACCEPTANCE](../ACCEPTANCE.md) 对齐。

- [最终文件核验](FINAL_FILE_CHECK.json)：对8619工具/证据输入，817项Raw发布文件及2329+889保护文件差异0；后续仅此传输归档文档。
- [LFS/Git首次失败与重试](PUSH_HISTORY.json)：与产品断言分别记录。

