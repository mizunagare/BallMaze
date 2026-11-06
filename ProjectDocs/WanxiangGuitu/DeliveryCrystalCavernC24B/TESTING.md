# 复跑与证据边界

Unity 6000.6.5f1；不升级依赖。根目录 `I:/WGCombat/C24-1106-A`。每次输出必须为新目录，禁止覆盖现有结果。启动前检查可提交内存 >=3 GB；超时保留进程，不强杀。所有存档为该根目录下合成数据。

## 非开发测试 Player

1. `Tools/Prepare-Player.ps1 -Build Phase2PureBuild1 -Observation <新名称>`。只复制纯包，再将 Driver.cs.txt 编译为 sidecar 并注册到**副本**。
2. `Tools/Invoke-Player.ps1 -Output I:/WGCombat/C24-1106-A/<新运行> -Mode <模式> -Observation <同名称>`。
3. 恢复模式加 `-Seed <来源运行目录>`，Copy-TestSeed 仅复制该目录中合成存档及预期数据，记录哈希。
4. 核对 `process.json`、原生 `Player.exit.json`、断言及实际业务轨迹，不能仅用编排退出码。

模式：`weapon-0/1/2/3/11/12/13`；`weapon-clear-0` / `weapon-block-0` 等五种近战；`pair-p1-Claw-hit/evade`、`pair-p1-Volley-hit/evade`、同类 p2；`pair-p2-CrossLines-hit/evade`；`pair-p2-HollowRing-hit/inner/outer`。招式配对只在启动前设置受控位置；P2 通过真实剑攻击达到阈值，随后恢复真实 AI。规避用正常移动/翻滚。不是正常出征或原生输入。

`route-three` 检查 dormant/challenged 的 C24 单独贡献与全部既有精英贡献；`route-dead` 用既有死亡合成存档恢复。第一次错误要求整条湖岸风险为零的运行保留。

奖励已完成，不为增加数量重跑：`reward-before`、`reward-after`、`reward-restore`、`reward-camp`，以及源代码中的 pending/claim/salvage/normal-repeat/normal-bank-restore 模式。每轮实际执行版本见 `Evidence/Runs/ExecutedDrivers/`；不要假定最新驱动等于旧运行驱动。

## Editor 与纯包

Editor 使用隔离 Project，在单独验证目录放 Driver.cs.txt 的 C# 副本，使用现有 `C24ValidationEditor.Begin`，`Invoke-Editor.ps1 -NonBatch`。不要用 batchmode 的 CombatSaveSystem.Start 提前退出路径。生产构建前不包含该驱动，原冻结构建已经完成。

纯包检查使用 `Invoke-Pure.ps1 -Exe <冻结包exe> -Output <新目录> -SeedPackage <合成存档子目录>`。该工具在独立桌面检查标题渲染、没有自动入局、合成存档未变和真实退出；背景关闭消息不代表原生键鼠操作。

## 只读审核

`Audit-Combat-Matrix.py` 读取当前 A1 原始输入；默认必须创建新审核目录，复跑时改输出名，不能覆盖 CombatMatrixAudit1。严格比较的 8 个 FAIL 不得通过改浮点容差转为 PASS。

`Audit-Windup-New.py` 仅使用 A2/B2；原 malformed A1/B1 为负例，保留拒绝结果。半血前摇顺序保持 INCOMPLETE。

`Archive-Evidence.py` 按 SHA 复制，已存在不同内容即拒绝；归档 manifest 名称首次已使用，后续必须新名称。`Summarize-Runs.py` 统计所有原始尝试，含重复夹具断言，不能替代逐项 ACCEPTANCE。
