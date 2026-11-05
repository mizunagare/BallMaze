# C1 分项验收

37 PASS / 0 FAIL / 6 NOT_RUN / 4 UNRESOLVED。待独立复审，不宣称整体验收完成。

当前35个实际运行案例：915 PASS（Editor规则33、受控Editor441、非开发测试Player441），0 FAIL。先行三区Gate另26+26 PASS。逐步重复断言不是独立玩法数；辅助旧规则标记、构建与保护审计不混入915。过程65条probe/rules历史FAIL及其他编译/基线/超时失败完整保留，见失败历史。

|ID|范围|状态|证据|
|---|---|---|---|
|A01|07e476基线、独立分支、未合并main|PASS|[REPORT.md](REPORT.md)|
|A02|2413项用户/原产品文件原始哈希不变|PASS|[Evidence/final-protection.json](Evidence/final-protection.json)|
|A03|CombatAim/CP05/七武器核心原始Windows字节与Git内容保持|PASS|[Evidence/final-protection.json](Evidence/final-protection.json)|
|A04|199项MapMagic供应商源码未改|PASS|[Evidence/final-protection.json](Evidence/final-protection.json)|
|A05|用户Scene/ProjectSettings、依赖及CI未修改|PASS|[Evidence/final-protection.json](Evidence/final-protection.json)|
|A06|先三地区Editor 26条断言|PASS|[Evidence/FrontierEditor3/probe.json](Evidence/FrontierEditor3/probe.json)|
|A07|先三地区非开发Player 26条断言|PASS|[Evidence/FrontierPlayer1/probe.json](Evidence/FrontierPlayer1/probe.json)|
|A08|四块257保存地形、免费核心只用于编辑器|PASS|[Evidence/Authoring2/authoring.json](Evidence/Authoring2/authoring.json)|
|A09|九类自有模块、四猫族变体和原有石像接入|PASS|[ASSET_CATALOG.md](ASSET_CATALOG.md)|
|A10|五区Editor实际CC行走/相机净空50条断言|PASS|[Evidence/FullEditorFinal1/probe.json](Evidence/FullEditorFinal1/probe.json)|
|A11|五区非开发Player实际CC行走/截图50条断言|PASS|[Evidence/FullPlayer1/probe.json](Evidence/FullPlayer1/probe.json)|
|A12|机关、门双向开关、占用保护与真实导航|PASS|[Evidence/FullPlayer1/probe.json](Evidence/FullPlayer1/probe.json)|
|A13|碑文开密室、封石实际CapsuleCast阻挡|PASS|[Evidence/FullPlayer1/probe.json](Evidence/FullPlayer1/probe.json)|
|A14|真实宝箱落地、拾取与重复请求不加奖|PASS|[Evidence/FullPlayer1/probe.json](Evidence/FullPlayer1/probe.json)|
|A15|精英实际AI、实际攻击与死亡|PASS|[Evidence/ElitePlayer2/probe.json](Evidence/ElitePlayer2/probe.json)|
|A16|新Boss两阶段及不同真实攻击释放/战斗|PASS|[Evidence/BossPlayer1/probe.json](Evidence/BossPlayer1/probe.json)|
|A17|Boss真实材料拾取、地面紫装、重复掉落不变/旧流不变|PASS|[Evidence/BossPlayer1/probe.json](Evidence/BossPlayer1/probe.json)|
|A18|七武器Editor/Player身份、普攻/当前技能及真实击败|PASS|[Evidence/validation-summary-final.json](Evidence/validation-summary-final.json)|
|A19|七武器走廊与大厅真实通行、保留墙体|PASS|[Evidence/validation-summary-final.json](Evidence/validation-summary-final.json)|
|A20|法杖/弓走廊真实Spawn与墙体首次接触|PASS|[Evidence/WeaponPlayerStaff2/probe.json](Evidence/WeaponPlayerStaff2/probe.json)|
|A21|暂停/恢复状态稳定|PASS|[Evidence/FullPlayer1/probe.json](Evidence/FullPlayer1/probe.json)|
|A22|真实Boss致死、结算、重开|PASS|[Evidence/DeathPlayer2/probe.json](Evidence/DeathPlayer2/probe.json)|
|A23|Running跨进程Run/地形/流/实体/装备/来源账恢复|PASS|[Evidence/ResumePlayer1/probe.json](Evidence/ResumePlayer1/probe.json)|
|A24|Boss击败后战利品跨进程恢复及结算|PASS|[Evidence/BossResumePlayer1/probe.json](Evidence/BossResumePlayer1/probe.json)|
|A25|连续三次正常读取、掉落唯一且仅一活动区域|PASS|[Evidence/ResumePlayer1/probe.json](Evidence/ResumePlayer1/probe.json)|
|A26|撤离取消/重启、Pending/Commit两次、确认入仓再出征|PASS|[Evidence/ResumePlayer1/probe.json](Evidence/ResumePlayer1/probe.json)|
|A27|本批中间stage3逻辑区域/事件/遭遇不扩展|PASS|[Evidence/FrontierResumePlayer1/probe.json](Evidence/FrontierResumePlayer1/probe.json)|
|A28|发布前失败回滚重试、发布后故障确认完整状态/修订|PASS|[Evidence/FaultPlayer1/probe.json](Evidence/FaultPlayer1/probe.json)|
|A29|旧B3四组流隔离与旧B07受控经济两组标记|PASS|[TESTING.md](TESTING.md)|
|A30|30个重复seed规则、JSON规范化/非法新地图拒绝|PASS|[Evidence/RulesFull10/rules.json](Evidence/RulesFull10/rules.json)|
|A31|回营后活动Terrain=0、NavMeshData=0（非泄漏归因）|PASS|[Evidence/ResumePlayer1/map-memory.jsonl.gz](Evidence/ResumePlayer1/map-memory.jsonl.gz)|
|A32|纯发行Windows非开发构建0错104警告|PASS|[Evidence/PureBuild1/release.summary.txt](Evidence/PureBuild1/release.summary.txt)|
|A33|四测试包与纯包审计所列38项关键产品类型IL一致，纯包无C1/原测试驱动及Editor引用|PASS|[Evidence/assembly-final-4.json](Evidence/assembly-final-4.json)|
|A34|固定Privacy Profile与Bee五服务逐项false|PASS|[Evidence/build-services-final.json](Evidence/build-services-final.json)|
|A35|纯包实际标题启动/可继续、未自动入游戏、实际退出0且合成档字节不变|PASS|[Evidence/PureRuntime1/pure-runtime.json](Evidence/PureRuntime1/pure-runtime.json)|
|A36|CPU/DrawCalls原始有效采样和硬件记录（仅测量非预算通过）|PASS|[PERFORMANCE.md](PERFORMANCE.md)|
|A37|独立剑前摇自动面向、法杖真实软锁定释放与Damage、石柱目标排除和RNG只读|PASS|[辅助Player](Evidence/AssistPlayer1/probe.json)|
|N01|可靠GC逐调用/整帧分配测量|NOT_RUN|[PERFORMANCE.md](PERFORMANCE.md)|
|N02|本游戏GPU负载校准及显存测量|NOT_RUN|[PERFORMANCE.md](PERFORMANCE.md)|
|N03|性能预算与长时间/多敌完整战斗基准|NOT_RUN|[PERFORMANCE.md](PERFORMANCE.md)|
|N04|物理键鼠及原生U16|NOT_RUN|[NATIVE_HUMAN.md](NATIVE_HUMAN.md)|
|N05|独立人工美术/理解/手感/最终平衡|NOT_RUN|[NATIVE_HUMAN.md](NATIVE_HUMAN.md)|
|N06|本轮v1–v8完整迁移矩阵|NOT_RUN|[SAVE_COMPATIBILITY.md](SAVE_COMPATIBILITY.md)|
|U01|原生内存漂移完整归因|UNRESOLVED|[PERFORMANCE.md](PERFORMANCE.md)|
|U02|JobTempAlloc原生释放根因|UNRESOLVED|[FAILURE_HISTORY.md](FAILURE_HISTORY.md)|
|U03|MapMagic三个版本标签供应商维护原因|UNRESOLVED|[ASSET_CATALOG.md](ASSET_CATALOG.md)|
|U04|隔离副本四处设置差异的来源阶段及完整构建输入等同性|UNRESOLVED|[Evidence/isolated-settings-differences.json](Evidence/isolated-settings-differences.json)|

历史UI-01 D3D12 UNKNOWN、Editor青色帧及旧黑帧/C15根因、Editor.Search内部异常、外部诊断发送路径仍沿用原UNRESOLVED；原生U16、独立人工理解/试玩仍NOT_RUN。本轮成功截图、退出或Bee全关闭不自动关闭这些历史事项。

A27仅中间原型逻辑兼容，不声称本批迭代前后的地形/相机净空逐值相同。A29为原有受控规则夹具，其直接Damage/合成填包不作为C1真实战斗证明。七武器实际战斗来自A18，无注入Damage/覆盖HP。Boss所有招式的命中/边界组合及所有机位未穷举，不能推导最终平衡或人工体验通过。
