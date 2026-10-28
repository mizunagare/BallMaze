# COMBAT02 验收

条目口径：17 PASS /1 历史预期 FAIL /4 NOT_RUN /7 UNRESOLVED。原始进程另外保留4次首次恢复链失败；不可用条目汇总掩盖这些exit1。本批不是整体发行/人工体验通过。

|ID|状态|验证层|证据与边界|
|---|---|---|---|
|C02-01|PASS|source|[UX02限定接受归档；不继承历史PASS](Evidence/../AUDIT_AND_MEASUREMENT.md)|
|C02-02|PASS|controlled-measurement|[684矩阵+8时序+24短战；81细边界另档](Evidence/Runs/Before/measurement.json)|
|C02-03|PASS|controlled-measurement|[同键684矩阵+8时序+24短战；81细边界另档](Evidence/Runs/After/measurement.json)|
|C02-04|PASS|offline-comparison|[20/20前后不变量](Evidence/Runs/Comparison/comparison.json)|
|C02-05|PASS|controlled-timing|[8实际动作；保留冷启动和帧波动](Evidence/Runs/After/timing.csv)|
|C02-06|PASS|enabled-enemy-AI-flat-arena|[前后24+24次敌死，每武器/体型n2，不是森林Boss胜率](Evidence/paired-duels-summary.json)|
|C02-07|PASS|controlled-actual-damage|[15/15品质追加段、多目标AoE与独立箭](Evidence/Runs/Contracts/contracts.csv)|
|C02-08|PASS|controlled-static-slope|[±10°实际坡碰撞，16/16命中；不是动态爬坡试玩](Evidence/Runs/Slope/matrix.csv)|
|C02-09|PASS|controlled-rules|[188/188，仅更新基础普攻预期为BasicPower](Evidence/Runs/LegacyAdapted/combat01.json)|
|C02-10|PASS|existing-regression|[输入/观测/B07Combat三个进程exit0](Evidence/Runs/Regression/results.csv)|
|C02-11|PASS|editor-normal-forest-AI|[Normal/Resume/FinalResume均exit0，采集渡口结算制造再次森林继续](Evidence/Runs/Regression/Normal-Gather/normal-results.txt)|
|C02-12|PASS|controlled-cross-process|[第二个隔离Run的4阶段通过，绝不覆盖首次失败](Evidence/Runs/RecoveryProbe-CommittedResume/results.csv)|
|C02-13|PASS|non-development-build|[None；0E94W；346.718秒](Evidence/Runs/Build/build-report-messages.json)|
|C02-14|PASS|assembly-metadata|[发行Assembly-CSharp不含本批Editor驱动类型名](Evidence/Runs/Build/build-hashes.json)|
|C02-15|PASS|source-binding|[所有源仓库C#与副本逐文件SHA一致，设置重序列化差异照录](Evidence/product-inputs.json)|
|C02-16|PASS|user-protection|[用户五项原件SHA不变，未暂存](Evidence/protected-after.json)|
|C02-17|PASS|controlled-visual|[同机位受控前后图存在；画面质量有限，非人工审美验收](Evidence/Runs/VisualAfter/controlled-release-1.png)|
|C02-H01|FAIL|retained-expected-history|[187P/1F；expected33 actual41.25；原样exit1保留](Evidence/Runs/LegacyOriginal/combat01.json)|
|N01|NOT_RUN|unexecuted|[原生U16](Evidence/../FAILURE_HISTORY.md)|
|N02|NOT_RUN|unexecuted|[独立人工试玩、可理解性与声音/物理输入感知](Evidence/../FAILURE_HISTORY.md)|
|N03|NOT_RUN|unexecuted|[最终发行Player实际战斗操作](Evidence/../FAILURE_HISTORY.md)|
|N04|NOT_RUN|unexecuted|[完整性能预算](Evidence/../FAILURE_HISTORY.md)|
|U01|UNRESOLVED|open|[UI01 D3D12 UNKNOWN](Evidence/../FAILURE_HISTORY.md)|
|U02|UNRESOLVED|open|[旧C15](Evidence/../FAILURE_HISTORY.md)|
|U03|UNRESOLVED|open|[Editor青色帧](Evidence/../FAILURE_HISTORY.md)|
|U04|UNRESOLVED|open|[Editor.Search](Evidence/../FAILURE_HISTORY.md)|
|U05|UNRESOLVED|open|[JobTempAlloc](Evidence/../FAILURE_HISTORY.md)|
|U06|UNRESOLVED|open|[旧Editor启动阻塞](Evidence/../FAILURE_HISTORY.md)|
|U07|UNRESOLVED|open|[首次附加B07恢复链前置查找失败；第二个不同Run通过不能确定原根因](Evidence/Runs/Recovery-Run/Unity.log.gz)|
