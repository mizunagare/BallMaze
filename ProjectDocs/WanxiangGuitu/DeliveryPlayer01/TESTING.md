# PLAYER-01 复跑与分层

Unity6000.6.5f1、现有锁和PowerShell7。本轮使用现有协调器Step/StartChild/FinishChild/SafePath/拥有者检查与旧Editor测试，未重建调度框架。不要操作真实存档、用户活动桌面或现有Unity。

```powershell
Set-Location D:/unity/WanxiangGuitu
$root = 'D:/WGP01/' + (Get-Date -Format 'MMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8)
New-Item -ItemType Directory $root | Out-Null
@{kind='PLAYER-01 isolated vertical-slice validation';source='D:/unity/WanxiangGuitu';head=(git rev-parse HEAD);root=$root;utc=[datetime]::UtcNow.ToString('o')} |
  ConvertTo-Json | Set-Content "$root/owner.json"
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONUTF8='1'
& $py -B ProjectDocs/WanxiangGuitu/DeliveryBuild01/audit_inputs.py --source D:/unity/WanxiangGuitu --out $root
& ProjectDocs/WanxiangGuitu/DeliveryBuild01/Invoke-Diagnostic.ps1 -Case Short -TestRoot "$root/B"
& ProjectDocs/WanxiangGuitu/DeliveryPlayer01/Invoke-Player01.ps1 -RunRoot $root
```

开工先核对远端main与任务授权基线；若已前进按任务书停止，不擅自重置。复审后的复跑要另行明确当前输入，不能把上述命令当作绕过版本检查的授权。

WorkerFrom默认是已审计的INPUT-01拥有者根；必须存在同来源owner及NativeProbe.dll。不存在时失败，不转到活动桌面。整个RunRoot/B/时间目录/Project必须通过BUILD-01包路径预算；本轮目标资产217字符。新机器需要提供本机对应的已审计worker根与Unity路径。

顺序：

1. 新正式构建，完整BuildReport检查与进程结束后才能继续。
2. Input01Rules → Play → Resume（Editor虚拟输入，新进程）。
3. B09Rules Run/Resume/Interrupt/Recover；B09Cases Run/Pending/Committed（Editor受控事务与恢复）。
4. U16Fixture生成**明确合成**合法继续档；P01Confirmation在另一合成目录验证集合变化拒绝。fixture初始物资/空遭遇仅用于UI，不冒充正常AI。
5. 沿原B4 Gather Normal/Resume/FinalResume，原敌人AI正常，三次独立Unity进程；只修改新副本中的Editor驱动目录并保留实际源码。
6. 六个正式Player标题进程，复制完整合成档集合，不改正例JSON；Corrupt/Incompatible是明确坏输入。都用显式存档根、D3D11、1280×720与已有只读入口审计/截图参数。
7. NativeProbe只在本次窗口做安全检查，非活动桌面返回NOT_RUN，无输入；关闭仅WM_CLOSE，真实退出另核对。绝不发送物理Esc或切换桌面。

每个Editor测试上限600秒，Gather调用420秒（内部360秒），标题等待90秒、关闭30秒。超时进程保留，依赖跳过；不强杀。原始命令、起止UTC、host/Unity/Player PID、退出码、超时、stdout/stderr及Unity日志保存于拥有者根。Gather Unity PID从原始UTP日志提取，与pwsh/worker host PID分开。

本批Editor确认测试只调用真实GameEntry方法，并在自己的合成档集合加入/移除并发哨兵；明确不是正式Player回调/原生操作。

元数据与只读发布：

```powershell
$b = Get-ChildItem "$root/B" -Directory | Select-Object -First 1
New-Item -ItemType Directory "$root/ProductIdentity" | Out-Null
& ProjectDocs/WanxiangGuitu/DeliveryBuild01/Inspect-Assembly.ps1 -AssemblyPath "$($b.FullName)/Results/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll" |
  ConvertTo-Json -Depth 6 | Set-Content "$root/ProductIdentity/assembly.json"
& $py -B ProjectDocs/WanxiangGuitu/DeliveryPlayer01/collect_player01.py --run $root --source D:/unity/WanxiangGuitu --evidence '<本次新证据发布目录>'
```

只在拥有进程结束后发布。只复制回执、原始日志、合成状态快照/指纹、执行测试源和截图，不复制Player二进制/Library或用户场景内容。源文件清单哈希包含用户覆盖层，独立记录；不要通过提交它们“统一输入”。

正式Player继续/设置/输入消费/完整冒险无可用运行驱动，保持NOT_RUN。现有Gather和虚拟输入都依赖UnityEditor，不能将-executeMethod传给正式Player冒称成立。后台WM_CLOSE、截图、规则断言和Editor机器人不能替代原生/人工，也不把一次标题启动称为性能基准。
