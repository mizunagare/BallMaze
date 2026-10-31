# R1.1 复跑

所有 Output 必须全新。先复制 owned 隔离 P/Project，工程外合成存档，不覆盖旧根。

```powershell
$tools = 'H:/unity/WanxiangGuitu-CP03-R1/ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03'
$r11 = 'H:/unity/WanxiangGuitu-CP03-R1/ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03R11'
$py = 'C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py "$tools/SelfTest-R1.py" --output 'I:/WGCombat/CP03-R1-NEW/LegacySelfTestFinal' --original-root 'I:/WGCombat/CP03-1031-A'
& $py "$r11/SelfTest-R11.py" --output 'I:/WGCombat/CP03-R1-NEW/BindingSelfTestFinal'
```

预期各 exit0、50/33 PASS。原检查不删，分类用完整冻结 293 项结构的合成副本；这些 PASS 只测试工具，不是 Unity 通过。各负例核对报告、退出码和错误原因。

```powershell
& "$tools/Invoke-ReviewEditor.ps1" -Project 'I:/WGCombat/CP03-R1-NEW/P/Project' -Output 'I:/WGCombat/CP03-R1-NEW/Editor'
& "$tools/Invoke-Runtime.ps1" -Build 'I:/WGCombat/CP03-1031-A/AcceptanceBuild2/Release' -Output 'I:/WGCombat/CP03-R1-NEW/Runtime' -FixtureSave 'I:/WGCombat/CP03-1031-A/Final2/Game/ForestRuins/save.json'
```

正式包装器明确传 Editor/Runtime profile 及对应新冻结合同。真实进程预期 exit0，2 UR 保留使分类/宿主 exit2。外层 shell 使用 `exit $LASTEXITCODE`；不把 2 当游戏进程失败或把 0 当整体通过。原 Editor/Player 有界期限不改，不强杀。

独立只读分类必须有角色和合同，下面的 exit-code 必须取自该次真实进程回执，不能凭空填写：

```powershell
& $py "$tools/Receipt.py" --receipt 'I:/WGCombat/CP03-R1-NEW/Runtime/presentation.json' --output 'I:/WGCombat/CP03-R1-NEW/Reaudit' --profile Runtime --contract "$r11/Contracts/Runtime.json" --process-status PASS --exit-code 0
& $py "$r11/Verify-R11.py" 'I:/WGCombat/CP03-R1-NEW' --output 'I:/WGCombat/CP03-R1-NEW/consistency.json'
```

分类合法开放矩阵为 BLOCKED/2；错合同、错角色、缺合同为 INCOMPLETE/3。缺省参数保留只是为了生成结构化拒绝报告，无无合同通过路径。[新真实回执错误重审](Evidence/RealCrossContext/results.json)只读，不是另一次 Unity 执行。

一致性 35 检查核对 R1 Git 原字节、代码锚、原回执、CSV/Markdown、进程及输入/保护。性能、人工、原生和新构建不在本轮实测结论内。发布日志原始字节留 I 根，公开版本只遮盖凭据值，按 manifest 核对 Git 直接 blob 与 LFS 对象，不拿指针文本当日志。

验证器还需要 Before、RealCrossContext、保护及输入清单，结构见本轮证据；缺件不得继承旧 PASS。只核对本次已归档整轮时，可把验证器 root 指向 I:/WGCombat/CP03-R1-1031-B，另给全新 output；重新整轮则须生成相同结构后验证，不能只跑两条命令冒充完整回归。
