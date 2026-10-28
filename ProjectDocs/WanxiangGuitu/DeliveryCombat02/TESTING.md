# COMBAT02 复跑

只使用工程外唯一拥有者目录、合成档和闲置隔离副本。沿用DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly；主工程有用户Editor时不关闭、不编辑场景。先记录五项用户文件哈希。完整命令和实际exit/timeout见各Runs/*.command.json、*.exit.json、results.csv。

1. 固定远端main、源码、包和用户文件，准备副本。注入Tests/Combat02Bench.cs.txt到副本的Editor/B06LocalChecks；不得注入发行运行程序集。
2. 对开工代码运行Invoke-Combat02.ps1 -Project <isolated> -Output <new-root>/Before -Method Combat02Bench.Run；再以Boundary方法运行BeforeBoundary。没有基线不得先调参数。
3. 冻结DESIGN.md后仅同步获准C#到副本。用相同方法运行After、AfterBoundary、Contracts、Visual。角色/敌人位置和HP设置只属于受控合成测试，不冒充人工或正常AI。
4. Invoke-Remaining.ps1是本轮有序命令清单，复用既有Step/Worker和Invoke-Regression/Invoke-Checks，不建立第二套编排器。Before/After数据不得覆盖。WorkerPath可以显式传给Invoke-Combat02，指向既有NativeProbe.dll；路径不存在就失败。独立桌面只创建不激活，不发送原生按键、不抢用户桌面。
5. 历史Combat01原样运行先保留187/1；改为BasicPower的唯一基础伤害预期后再执行188。原文件不改，执行版本留档。其余断言不得削弱。
6. 使用原Invoke-Regression执行Input01/S2R1Observation/B07Combat和Normal/Resume/FinalResume；之后恢复该脚本暂存在Deferred的Editor文件。进程未结束则保留，不继续使用占用副本。
7. B07Rules.Run/Resume/PendingResume/CommittedResume使用显式共享合成根，各进程独立输出和退出回执。它会在受控测试中产生Pending/Committed，不能当玩家胜利。
8. 原Build01Audit.Run调用真实WanxiangBuild.Build，BuildOptions.None；归档所有警告和EXE/Assembly-CSharp哈希；检查Editor驱动不在Player DLL。
9. Slope方法在±10°真实Cube坡碰撞体上测试四武器普攻/技能，有限16行；它是静态受控命中测试，不冒称玩家动态爬坡体验。
10. python -B Verify-Comparison.py --root <owned-root>；python -B Collect-Evidence.py --run-root <owned-root> --repository <repo>。校验684相同case键、20条前后不变量、保护哈希、源码与副本差异。

本次根I:/WGCombat/C2-1028-2140。固定对照使用地图418、等级1、白装无词缀；普通/精英/波次Boss胶囊尺寸在每行记录。AI冒险用自己实际Run/seed，不与短战混算。时限：矩阵650秒、外部进程1200秒、原规则/AI沿用各自600/420秒；超时不强杀、不等于正常退出。

截图raw来自GameView，controlled来自同一运行相机的URP RenderRequest并临时映射overlay Canvas；两类原件均保留，不能冒充原生键鼠。原生U16、独立人工、完整性能继续NOT_RUN。

附加恢复诊断复跑：只在新的空合成根，把Evidence/B07Rules-diagnostic.cs.txt复制为副本Editor/B06LocalChecks/B07Rules.cs，并使用本批Tests中的Combat02RecoveryProbe。执行Combat02RecoveryProbe.Run；只有其exit0且expected文件存在，才依次执行B07Rules.Resume/PendingResume/CommittedResume（各独立Output，共享StorageRoot）。每一步保存expected前/后副本，失败立即把依赖步骤标NOT_RUN。历史旧驱动文件不修改，不把换Run的通过视作旧失败根因证明。
