# 原始证据索引

原件根 `I:/WGCombat/CP05BR-1103-A`，所有失败及历史黑帧保留。[manifest](manifest.json)记录原件/发布SHA、日志gzip、脱敏及已知GBK元数据转UTF8。原始文件均未修改。

- [渲染对照](render-comparison.json)；[原B3显示重跑](LegacyShownD12/probe.json)与LegacyHiddenD12：旧B3同一包，完整显示157/0/1及隐藏相机前缀。
- PlayerShownD12/PlayerHiddenD12/PlayerShownD11/PlayerRepeatD12：同诊断包的API/显示条件对照，窗口/相机/PNG及视觉回执。
- Editor1/Editor2：场景重名、掉落空引用、Profiler警告、实际退出/清理和执行时源码。
- Editor3/EditorStress：保留中间采样；不当作最终双敌负载通过。
- [EditorFinal](EditorFinal/br-probe.json)、[Unity Profiler原始作用域](EditorFinal/unity-profiler.json)、[独立分析](EditorFinal/analysis.json)：最终1116记录及472作用域交叉验证。
- [PlayerFinal](PlayerFinal/analysis.json)、[独立重复](PlayerFinalRepeat/analysis.json)、[最终门禁](PlayerGated/measurement-receipt.json)、[视觉回执](PlayerGated/render-receipt.json)：最终2172/2215/2223记录。实际runtime、desktop-process、command、exit独立保存。
- [13项采样自测](FinalSelfTests/selftests.json)；[7项视觉CLI自测](RenderSelfTests/selftests.json)。较早ToolSelfTests/StressSelfTests仍保留，不继承作本轮通过。
- [纯构建日志](PureBuild/Unity.log.gz)、[摘要](PureBuild/release.summary.txt)、[Profile marker](PureBuild/release.release.json)、[实际Bee](PureBuild/release.bee.json)：纯发行构建和全部警告；[所有产物SHA](release-files.json)、[发行身份](release-identity.json)。
- PureSmoke：READY/实际可见窗口库存/普通关闭与真实exit；不等于物理操作。
- [纯包类型/PInvoke与IL](assembly-release-final.json)；[真实测试包拒绝负例](assembly-driver-negative.json)。
- [开工哈希](protected-before.json)、[最终保护](protection-final-2.json)：2347项源/用户保护与隔离写回；原CP05B历史无diff。
- hardware.json、scope-contract.json、final-run-summary.json、window-tool-capability.json：硬件、采样条件、最终分层结果及窗口工具阻断。

Frame是原始PNG，不是概念图或合成图；测试Player、纯发行、Editor、原生输入与人工状态分别见报告，未执行项不可互相替代。
