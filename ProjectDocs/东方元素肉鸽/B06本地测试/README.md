# 本地复跑

测试源码保存在 ProjectDocs 下，不参与游戏编译。不要复制到真实工程或使用玩家存档。当前已测副本是 C:/Users/guan/Documents/unitytest/MazeValidation，结果在 B06Validation。新的 prepare-isolated.ps1 新建副本流程本次 NOT_RUN；现有隔离副本与原工程运行源码已比对一致，并实际执行完整方法集。

PowerShell 示例（路径由调用者指定；三个输出路径应为本地测试专用）：

```powershell
$tools='D:/unity/BallMaze/BallMaze/ProjectDocs/东方元素肉鸽/B06本地测试'
& "$tools/prepare-isolated.ps1" -SourceProject 'D:/unity/BallMaze/BallMaze' -WorkProject 'C:/UnityChecks/B06Copy' -ArtifactsRoot 'C:/UnityChecks/B06Results' -IncludePlayerSmoke
& "$tools/run-release.ps1" -SourceProject 'D:/unity/BallMaze/BallMaze' -WorkProject 'C:/UnityChecks/B06Copy' -ArtifactsRoot 'C:/UnityChecks/B06Results' -UnityPath 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' -Methods @('B06DropCheck.Run','B06ForestCheck.Run','B06PhysicalCheck.Run','B06V8MigrationCheck.Run','B05LegacyMigrationCheck.Run','B05V7MigrationCheck.Run','B05ScenarioCheck.Run','B05FaultCheck.Run','B05LiveRegression.Run','T06RegContainerRuntimeCheck.Run','T06RegDualWeaponCheck.Run','T06RegWorkbenchCheck.Run','B05EditChecks.Run','B06BuildCheck.Run') -QuitMethods @('B05EditChecks.Run') -TimeoutSeconds 300
```

Windows 如本机执行策略禁止运行脚本，可用 powershell -NoProfile -ExecutionPolicy Bypass -File 指定本次进程，不修改系统执行策略。数组参数建议直接在 PowerShell 会话按示例调用。

run-release.ps1 每次写 invocation/results 的时间戳文件以及最新 results.json/csv/summary.txt。每个方法保存实际退出码、超时、启动异常、耗时和独立日志。任一失败/超时/异常时退出 1。退出 0 不表示人工作用或性能已验收；阅读每个断言标记与测试边界。同步 executeMethod 需要放入 QuitMethods；PlayMode 方法自己退出，不加 quit。

RunnerSelfTest 故意返回失败：0、7 和超时，汇总退出 1 才说明没有吞掉失败。它不启动 Unity。

原工程正常 AI 自动试玩入口 B06OriginalPlay.Run 使用 UNITY_TEST_ROOT 指定隔离目录。短样本中不关闭 AI、不改数值，原工程临时驱动已移出 Assets；人工试玩为 NOT_RUN。其默认策略不保证击杀或完成长路线。

IncludePlayerSmoke 仅给隔离构建加入 B06PlayerSmoke；它由 -b06-smoke-root <隔离目录> 启用，再次运行加 -b06-resume。两个进程都应记录 exit 0 和各自 B06_PLAYER_*_PASS。构建是测试产物，驱动不在原工程。不要把测试驱动或测试档作为正式玩家内容。
