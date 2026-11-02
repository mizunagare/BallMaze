# 复跑与证据层级

所有输出新建于工程外I:/WGCombat/CP04B-*，不能使用用户工程或真实存档。源产品从main72db192a构造，仅替换获准CombatAim，既有隔离Editor辅助目录/Library必须独立拷贝。Tests/*.cs.txt仅复制到隔离工程；CP03Cases及CP04B运行时驱动用UNITY_EDITOR或CP04B_ACCEPTANCE宏，不能直接拷入产品。

Editor继承既有DeliveryEncounterAI01/Invoke-Check.ps1入口，方法：CP04BEditor.Run（38）、CameraWall（2）、Boundary（6）、Lifecycle、Death、Perf，以及CP03Editor.Run（四武器293）。每轮执行副本与命令见原始目录。编译错误/异常/超时不以exit0掩盖；不强杀，不抢桌面，不修改用户快捷键。

构建由隔离Editor的CP04BBuild.Acceptance/Pure执行：Acceptance显式extraScriptingDefines=CP04B_ACCEPTANCE；Pure调用原WanxiangBuild.Build且不含该宏。两者BuildOptions.None，最后使用AcceptanceBuildShippingInput/PureBuildShippingInput。先Inspect-Build.ps1分别核对类型及引用。27次实际运行的来源链见AssessmentFinal。

```powershell
$d='H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04B'
& "$d/Invoke-Players.ps1" -Root 'I:/WGCombat/CP04B-NEW' -Build 'I:/WGCombat/CP04B-1102-A/AcceptanceBuildShippingInput/Release' -Fixture 'I:/WGCombat/CP03-1031-A/Final2/Game/ForestRuins/save.json'
```

Player先通过真实Boot/Title受控Continue读取原合成检查点逐字节副本，不注入奖励，不改最终存档；显式-cp04b-acceptance与owner文件双重保护。主批Historical/Matrix/Wall/Boundary/Lifecycle/Death/Perf，含真实攻击、发射、碰撞及Damage。驱动受控禁用fixture AI以隔离几何，不冒称正常AI或原生输入。Windows独立非活动desktop不激活。

```powershell
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py "$d/Assess.py" 'I:/WGCombat/CP04B-1102-A' 'H:/unity/WanxiangGuitu-CP04' --output 'I:/WGCombat/CP04B-1102-A/NewAssessment'
```

当前预期最终exit2/BLOCKED：174PASS、1UR、3NR。根因是隔离输入等同性仍待核查和分配/原生/人工证据缺项，不能仅按进程0宣布完成。AssessmentFirst只覆盖早期功能检查，后发现的输入差异和缺项由AssessmentFinal显式纳入，旧结果保留。

完整复跑还需要首次BeforeMatrix、逐阶段保护清单、计数克隆、元数据与输入差异文件；不能跳过这些依赖让报告全绿。初始嵌套布局主批的真实路径见Evidence/AssessmentDelivery/run-paths.json；复跑器已修复且有两套控制，不能假装旧运行发生在平铺路径。
