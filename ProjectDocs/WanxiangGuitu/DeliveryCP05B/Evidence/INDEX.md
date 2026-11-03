# 原始证据索引

原件 I:/WGCombat/CP05B-1103-A，未覆盖。仓库日志gzip镜像，manifest记录source/published SHA及脱敏；截图不裁切。构建二进制留本机，仓库完整文件清单可验证。

- [B1清单](B1/manifest.json)、[纯包文件哈希](B1/release-files.json)、B1_CHECKPOINT：Build4/Smoke4/Editor2及更早失败。
- [B2清单](B2/manifest.json)、[纯包哈希](B2/release-files.json)、B2_CHECKPOINT：Editor1、Player1缺失回执、Player2、纯包SmokeRelease。
- [B3清单](B3/manifest.json)、[最终Editor](B3/EditorFinal/probe.json)、[最终Player](B3/PlayerFinal/probe.json)、[实际Player进程](B3/PlayerFinal/runtime.json)。相应目录下projectile/damage/melee-trace.jsonl.gz和probe-progress.jsonl.gz保存原始实际事件。
- [实际转角旧FAIL](B3/YawBeforePlayer/probe.json)、[修复后](B3/YawAfterPlayer/probe.json)；YawBeforeBuild保留执行时旧AdventureCombat源码快照。
- [镜头旧FAIL](B3/CameraJumpBefore/camera-jump.json)、[After](B3/CameraJumpAfter/camera-jump.json)。
- [热缓存脚本缺失](B3/AssetAudit3/asset-audit.json)、[冷副本对照](B3/ColdAssetAudit/asset-audit.json)、[四份源码一致](B3/type-cache-source-pair.json)。
- [逐查询GC原始Profiler](B3/ScopedPerfEditor/scoped-perf.json)、[样本统计](B3/ScopedPerfEditor/summary.json)。
- [纯构建摘要](B3/build-summary.txt)、[Release marker](B3/release-marker.json)、[实际Bee](B3/bee.json)、[所有产物SHA](B3/release-files.json)、[纯包启动/关闭](B3/SmokeRelease/runtime.json)。完整96条构建警告在ReleaseBuild/Unity.log.gz。
- [纯包驱动排除/IL](B3/assembly-audit.json)、[B2同类对照](B3/assembly-b2.json)、[产品输入对应](B3/source-parity.json)、[最终保护](B3/protection-final.json)。
- [图像核验](B3/capture-audit.json)：Player全黑帧保留在PlayerFinal及B2 Player2；不得冒充有效画面。
- [对照GIF清单](B3/ComparisonEditor/manifest.json)：camera/staff/bow/sword/spear，**受控Editor短序列**，原分辨率帧在EditorFinal/clip-*；无声音/原生输入/人工。不是持续Player录像。

人工记录空白见HUMAN_PLAYTEST.md。NOT_RUN、UNRESOLVED及全部失败见ACCEPTANCE与FAILURE_HISTORY；镜像没有将任何旧结果改成PASS。
