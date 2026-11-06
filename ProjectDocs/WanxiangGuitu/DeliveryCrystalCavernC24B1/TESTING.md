# 复跑说明

使用 PowerShell 7（`pwsh`），不是 Windows PowerShell 5.1。Unity 6000.6.5f1；Python 为 Codex runtime 的 Python。所有脚本固定独立根目录 `I:/WGCombat/C24B1-1107-A`，已存在输出拒绝覆盖。复跑先换新隔离根和新证据目录，不删除旧目录。

## 层级与入口

- 无驱动发行构建：干净隔离工程，仅产品源码、固定 WindowsRelease Profile，调用既有发行构建入口。实际调用保存在 `Evidence/Runs/PureBuild1/Editor.command.json`，BuildReport摘要及Bee、release回执见其 `BuildReceipts`。**先构建纯包，后导入测试驱动**。
- 非开发观测 Player：`Prepare-Player.ps1 -Root <root> -Build PureBuild1 -Observation <fresh>`，复制发行包并仅在副本加入 CavernValidationDriver。`Invoke-Player.ps1` 的具体参数参考每个 `Player.command.json` / `Player.launch-spec.json`。
- Editor：在隔离 Project 中复制 `Tools/Driver.cs.txt` 到验证目录，再用 `Invoke-Editor.ps1 -Method C24ValidationEditor.Begin -NonBatch -Mode <mode> -Output <fresh>`。不得把该驱动加入后续纯包。
- 模式：`b1-first-before`、`b1-first-after`、`b1-name-cavern`、`b1-name-forest`、`b1-ring-inner/outer/band/safe`。旧首奖状态由 Copy-TestSeed 的合法隔离源拷贝，具体来源和SHA见各fixture.json；不是直接编辑存档造状态。
- 评分：隔离参考源码从 `37b25bb...` 导出，用 `Extract-Reference.py` 解析Unicode路径和本地LFS内容。两端同档案，真实Continue/LoadProgress后暂停，`ScoreDriver.cs.txt`只读Evaluate和Ranked。`Compare-Scores.py`保留原位置比较失败；`Compare-Scores-Identity.py`读取同批输入按稳定ID核对，不采样新输入。
- 纯包启动：`Invoke-Pure.ps1 -Exe <newPure>/WanxiangGuitu.exe -Output <fresh> -SeedPackage <isolated save>`。该测试只证明标题、合成档保护和实际退出；后台WM_CLOSE不是原生键鼠验收。
- 独立审核：`Audit-Notices.py`、`Protect.py`、`Archive-Evidence.py`。归档拒绝覆盖不同内容，复跑必须使用新manifest名。

首次失败见 FAILURE_HISTORY。进程exitCode与断言、设计开放项分开判断；取证成功不意味着产品设计口径已通过。C02/C04/C05及完整奖励链不重跑。
