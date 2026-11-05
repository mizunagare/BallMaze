# R2 原始证据索引

隔离原始目录为 I:/WGCombat/C1R2-1105-A。发布文件的源与发布 SHA256 见 [清单](manifest.json)，大日志、存档和逐帧轨迹按原有流程压缩，个人路径与许可标识脱敏。纯包与验证包的完整文件哈希见 [构建文件](build-files.json)。

| 事项 | 证据 |
| --- | --- |
| 进程和断言 | [案例汇总](Derived/case-summary.json)、[启动关联](Audit/launches.json) |
| 特殊待领、拆解和已领跨进程 | [R2Salvage](R2Salvage/)、[已领遗镰](LoadClaimed-R2Salvage/)、[已领首奖](LoadClaimed-R2ResumeBoss/) |
| 普通装备品质和物料 | [White](White/)、[WhiteRetry](WhiteRetry/)、[Green](Green/)、[R2Boss](R2Boss/)、[R2ResumeBoss](R2ResumeBoss/) |
| 两阶段首领、实际命中及规避 | [R2Boss](R2Boss/)、[R2Death](R2Death/)、[EditorPhase2](EditorPhase2/)、[时间](Derived/boss-timing.json) |
| 五区真实路线与敌人位移 | [R2Rewards](R2Rewards/)、[敌人位置样本](Audit/enemy-movement.json) |
| 武器、遮挡、辅助、暂停及切换 | [七武器](Derived/weapon-matrix.json)、[R2Assist](R2Assist/)、[法杖墙](R2WallStaff/)、[弓墙](R2WallBow/)、Guardian 各目录 |
| 跨进程真实 v9 恢复 | [封装与地面页](Audit/v9-snapshots.json)、LoadPhase1Injured、LoadPhase2、LoadElite、LoadPending、LoadCommitted |
| 冻结构建和原历史完整性 | [源与发布证据](Audit/frozen-history.json)、[保护核对](product-protection.json) |
| 新验证构建及纯包 | [VerificationBuild](VerificationBuild/)、[VerificationBuild2](VerificationBuild2/)、[纯包启动](R2PureBoot/pure-runtime.json)、[程序集核查](assembly-equivalence.json)、[第二构建程序集核查](assembly-equivalence2.json) |
| 配置输入等同性 | [隔离与仓库差异](lab-input-differences.json) |

复跑沿用独立隔离 Unity 工程，先确认占用、可提交内存和存储隔离，再在隔离 Assets 顶层安装 Tests 的 C1Probe、C1R1Cases、C1R2Cases、C1Metrics 及 Editor 的 C1Editor。Tools/Invoke-Editor.ps1 调用 WanxiangBuild.ValidateBuild 生成非开发验证包。Tools/Invoke-Player.ps1 逐次使用新目录，模式、实参及合成档来源见各目录 command 和 seed-copy。使用归档的实际 SeedPackage，禁止改写保存内容。完成后恢复隔离工程原驱动。冻结纯包使用 Tools/Invoke-Pure.ps1。

历史来源审计可通过 Tools/Audit.py 输入 R1 原始目录、R1 固定文档目录和 R2 原始目录复跑。Tools/Summarize.py 与 Tools/Publish.py 从实际回执生成索引和发布副本。
