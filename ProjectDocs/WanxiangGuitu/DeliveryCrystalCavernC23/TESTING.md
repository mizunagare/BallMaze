# 复跑说明

所有命令在独立工作树执行。不要对用户正在打开的 Unity 工程运行，不复制使用中的 Library，不覆盖任何旧输出。脚本内测试根固定为 `I:/WGCombat/C23-1106-A`，换机器复跑须逐项改为新的隔离根并记录差异。提交内存低于 3GB 不启动 Unity；超时不强杀。

1. 从交付提交创建干净隔离 Project，只复制 Assets/Packages/ProjectSettings，保留输入 SHA 清单。EditorProject 另建独立验证副本，不带 Library。生产源没有任何验收驱动。
2. 新固定 Prefab 已随提交保存，正式构建无需重新 Bake。需要重新制作时使用 `CrystalCavernAuthoring.BakeLake`，只在隔离副本调用。
3. 通过已有 `WanxiangBuild.ValidateBuild`（实际入口以构建 command.json 为准）及固定 `Assets/BuildProfiles/WindowsRelease.asset` 构建非开发 Windows64。运行 `Tools/Audit-Release.ps1 -Build <新构建目录名>` 核对实际 Bee、程序集和全包哈希。
4. Editor 验证把 `Tools/Driver.cs.txt` 和 `Tools/LakeDriver.cs.txt` 复制为验证工程中的 C# 文件，并复用 C22 的 `CavernValidationEditor.Begin` 入口。其精确源快照见 Evidence/Raw/EditorVerifiedInput。
5. `Tools/Run-Matrix.ps1 -Layer Editor -Tag <新唯一标签>` 顺序运行 14 个独立进程，失败立即停止，保留过程。`Invoke-Editor.ps1` 检查占用。
6. `Tools/Prepare-Player.ps1 -Build <构建名> -Observation <新副本名>` 复制纯包并编译隔离观测 sidecar，执行源文本随副本保存。`Tools/Run-Matrix.ps1 -Layer Player -Observation <新副本名> -Tag <新标签>` 运行对应 14 用例。
7. 追加 `Invoke-Player.ps1 -Mode lake` 连续样本，再 `-Mode warehouse -Seed <连续样本目录>`；`lake-routes`、`lake-nav-failure`、`hazard`、`death` 是单独证据。Editor 同名模式调用 `Invoke-Editor.ps1 -ValidationCopy -NonBatch -Method CavernValidationEditor.Begin -Mode ... -Seconds 600`。
8. `Invoke-Pure.ps1 -Exe <纯包EXE> -Output <新目录> -SeedPackage <合成档包目录>` 只记录纯包标题与退出；不点击游戏、不改变真实键位，不能称为原生操作验收。
9. Collect-Evidence 仅在所有进程退出后运行；已有归档目标会拒绝覆盖。检查 assertions.tsv + complete.txt + process.json；纯包使用 pure-runtime.json。进程 0 不自动等于语义通过。

精确启动命令、可执行路径、桌面/PID及原始退出证据都在 Evidence/Raw 中；完整 Unity 日志打包在 Evidence/Logs.zip，解压字节 SHA 对照 manifest.json。原始测试根及发行产物保留，原用户存档从未作为输入。

观测驱动使用 API 请求真实业务，并记录字符串/文件，会增加采样开销。本批未做可靠逐调用 GC/GPU 校准，不能用于最终性能预算。七武器固定靶、异常导航夹具、1HP 死亡夹具与正常 AI 连续过程分别标注，不互相冒充。
