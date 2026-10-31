# 复跑说明

以下为 PowerShell 示例；所有 Output 必须是未存在的新目录，不可复用 `CP03-1031-A` 原证据。Python 使用本机 Codex runtime。脚本和结果全部在文档目录；不要将驱动放入正式工程或发行 Assets。

```powershell
$tools = 'H:/unity/WanxiangGuitu-CP03-R1/ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03'
$py = 'C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py "$tools/SelfTest-R1.py" --output 'I:/WGCombat/CP03-R1-NEW/SelfTest' --original-root 'I:/WGCombat/CP03-1031-A'
& $py "$tools/Audit-Locked.py" 'H:/unity/WanxiangGuitu-CP03-R1' 'I:/WGCombat/CP03-1031-A' --output 'I:/WGCombat/CP03-R1-NEW/locked.json'
```

SelfTest 最终预期 exit0 / 50 PASS；其中负例 CLI 预期 exit1/2/3，不可吞掉。`Audit-Locked.py` 新接口必须给全新 --output；旧接口不再自动覆盖原 locked-contract.json。

只读重审历史矩阵：

```powershell
& $py "$tools/Receipt.py" --receipt 'I:/WGCombat/CP03-1031-A/Runtime2/presentation.json' --output 'I:/WGCombat/CP03-R1-NEW/Historical' --contract "$tools/Evidence/Runtime2/presentation.json" --exit-code 0
```

预期 exit2 / BLOCKED。`--exit-code` 必须来自真实原进程回执，不得凭进程消失或编排器状态填写。缺少进程退出码默认为不可确认，不产生 PASS。

先用原复制入口建立新的 owned CP03-R1 隔离工程，确认没有 Unity 占用、磁盘与提交内存足够；本轮复用旧冻结 CP03 Project 的完整独立副本（不修改旧副本）。复制结果与 [冻结产品输入](Evidence/frozen-build-product-binding.json)匹配后：

```powershell
& "$tools/Invoke-ReviewEditor.ps1" -Project 'I:/WGCombat/CP03-R1-NEW/P/Project' -Output 'I:/WGCombat/CP03-R1-NEW/Editor'
# 等 Editor 退出后再做只读详细观测
& "$tools/Invoke-ReviewEditor.ps1" -Project 'I:/WGCombat/CP03-R1-NEW/P/Project' -Output 'I:/WGCombat/CP03-R1-NEW/Diagnosis' -Diagnosis
& "$tools/Invoke-Runtime.ps1" -Build 'I:/WGCombat/CP03-1031-A/AcceptanceBuild2/Release' -Output 'I:/WGCombat/CP03-R1-NEW/Runtime' -FixtureSave 'I:/WGCombat/CP03-1031-A/Final2/Game/ForestRuins/save.json'
```

每次预期分类 exit2（Player/Editor 自身 exit0），不是全绿。外层 shell 须显式 `exit $LASTEXITCODE` 传播非零分类码。不可把所有非零判为产品失败，也不可把 BLOCKED 改 PASS。Editor 480 秒驱动期限、外层 1200 秒；Player 480 秒驱动期限、600 秒外层；不强杀，有占用则停止对应启动。

观测驱动保留原 293 断言/距离/相机/目标/Collider/Strike/UseSkill，仅在实际 Spawn 后缓存只读坐标/射线/速度/寿命，结束落盘。没有性能采样声明。正式 Player 重跑的是原 Nondevelopment 验收二进制，原 PE 检查/构建输入沿用且新哈希绑定，未新构建、未做纯发行原生 UI。正式产品 Git Assets 中没有本轮诊断驱动。

[证据发布工具](Publish-ReviewEvidence.py)仅发布新 owned root 的合成证据，跳过项目/缓存/二进制。原 I 盘日志不改；公开日志只遮盖凭据值，保留所有异常和行序，manifest 同时记录原/发布 SHA。没有通过过滤日志消除失败。
