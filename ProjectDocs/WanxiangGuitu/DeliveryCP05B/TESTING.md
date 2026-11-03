# 复跑与输入边界

Unity6000.6.5f1及原依赖，固定Profile `Assets/BuildProfiles/WindowsRelease.asset`。本次隔离根 I:/WGCombat/CP05B-1103-A，B3最终工程为 B3/Cold/Project。不要复用失败的跨路径热Library；该尝试原样保留。所有输出使用新目录，不覆盖Evidence。

1. 从独立原型分支复制 Assets/Packages/ProjectSettings 到工程外新的Project；保护用户场景/PS，不在用户工程运行。按既有Invoke-Check.ps1所需现有B06依赖建立测试副本，不新增编排框架。
2. 文档 `Tests/CP05Probe.cs.txt` 复制为隔离 `Assets/CP05Probe.cs`；`Tests/CP05Editor.cs.txt` 复制为隔离Editor/B06LocalChecks/CP05Editor.cs。绝不加入产品工作树Assets。Editor `CP05Editor.Run` 启动真实训练和Play协程。
3. 既有 `DeliveryEncounterAI01/Invoke-Check.ps1 -Project <Project> -Output <fresh> -Method CP05Editor.Run -NonBatch`；保留实际command、desktop、exit、Unity日志和probe。固定测试调用真实Strike/UseSkill；初始fixture控制及焦点调用明确为API。
4. 同一隔离工程执行 `CP05Build.Run` 产生测试非开发Player，使用 `Invoke-Player.ps1 -Build <Release> -Output <fresh> -Probe`；`-Suite yaw` 为极小game-delta专项，不是正常帧率体验。Probe必须有非空已知状态语义回执，不能只看进程exit0。
5. 纯包前移出runtime Probe和引用它的Editor runner；执行CP05Build.Run。此Editor构建方法从原场景导出新的训练资源，不保存原场景，继承固定发行构建入口。源/输入两个Prefab哈希相同。纯包不带 `-cp05-probe`。
6. `Tools/AssemblyAudit.ps1` 核对纯包驱动排除及八类产品IL；`Tools/FinalAudit.py <new.json>` 只读核对开工2334项和精确源码合同；`Tools/CaptureAudit.py <new.json>` 独立检查黑帧。
7. `Tests/CP05ScopedPerf.cs.txt` 只在隔离Editor，通过原Invoke-Check入口执行CP05ScopedPerf.Run；原生Profiler作用域正/零/释放引用校准通过才发布数字。发布工具只生成新Evidence目录；原日志不修改。

源码合同审计是精确已知位置替换：Release只移除一段新增面向头和一次Solve适配调用后比对原整个方法；MeleeGeometry、AdvanceAttacks、Fire、Sight、AdventureProjectile整体相等。其它保护文件逐SHA核对，禁止宽泛白名单吞掉产品差异。

本批不执行新的整局存档/经济矩阵，不继承为PASS。真实输入/独立人工使用HUMAN_PLAYTEST；Player黑帧未定位前，不将截帧当作视觉通过。所有进程只在独立桌面启动；超时记录并普通关闭owned窗口，未强杀或关闭用户程序。
