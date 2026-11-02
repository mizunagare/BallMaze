# CP04-BR 验收

整体 **BLOCKED**；七分项3 PASS（CPU仅有限测量）、3 NOT_RUN、1 UNRESOLVED。退出码、断言和整体验收分开，不以编排器0覆盖缺失。

|项|状态|证据|
|---|---|---|
|五文件逐字段/阶段审计|PASS|[阶段](Evidence/Raw/build-phase-analysis.json)、[字段](Evidence/Raw/field-differences.json)|
|构建输入行为等同性（必需）|UNRESOLVED|[构建报告](BUILD_INPUT_AUDIT.md)，native开关及最终数据等价未证明|
|Editor分配校准/真实Solve|PASS|[校准](Evidence/Raw/editor-allocation-analysis.json)，两版本各152作用域|
|非开发Player逐Solve字节|NOT_RUN|[原始控制](Evidence/Raw/FixedPlayers/PlayerProbe/probe.json)，不能采信0|
|GC Alloc完整要求|NOT_RUN|Editor有效，Player必需项未完成|
|CPU有限实测|PASS|[性能](PERFORMANCE.md)，不代表性能预算通过|
|基线Player/修复Player配对CPU与并发|NOT_RUN|基线missing-script，无完成回执|
|准确逐Solve查询次数|NOT_RUN|已知查询控制失败，未用静态估计冒充|
|本轮Editor功能|PASS|[presentation](Evidence/Raw/FixedEditorCore/presentation.json)，293PASS、exit0、未超时|
|本轮非开发验收Player功能|PASS|[presentation](Evidence/Raw/FixedPlayers/PlayerCore/presentation.json)，293PASS、exit0、未超时|
|纯发行构建/驱动剔除|PASS|[程序集](Evidence/Raw/assembly-audit.json)，纯发行0errors96warnings|
|原生输入|NOT_RUN|[脚本](NATIVE_INPUT.md)，无物理操作|
|人工体验|NOT_RUN|[空表](HUMAN_PLAYTEST.md)，无独立试玩者结果|
|冻结Aim/用户/旧证据|PASS|[保护](Evidence/Raw/protection-after.json)，2329+889，差异0|

上述明细是独立检查，不能与七分项或586功能断言混算。历史UNRESOLVED不追溯修改；自动化不是人工体验。
