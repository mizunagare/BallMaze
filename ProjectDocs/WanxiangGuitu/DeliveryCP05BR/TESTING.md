# 复跑说明

本批沿用原Invoke-Check.ps1和StartChild/FinishChild、NativeProbe私有桌面，不新建CI或替代编排框架。工具只在文档目录，实际执行时复制至工程外隔离Project；产品分支Assets无改动。

1. 从b27bda44复制Assets/Packages/ProjectSettings到新的工程外Project，不复制跨路径热Library。开工记录源/用户工程全部SHA。复制既有B06测试依赖，保持UI01Before等入口完整。
2. 将Tests/CP05BRProbe.cs.txt复制为隔离Assets/CP05BRProbe.cs，CP05BREditor.cs.txt复制到隔离Editor/B06LocalChecks。复用先前BR2AllocationNative.dll，先核对DLL SHA；缺失/接口不可用必须NOT_RUN或阻断，不能返回0当零分配。
3. 原Invoke-Check `-Project <Project> -Output <fresh> -Method CP05BREditor.Run -NonBatch`。输出实际Editor命令/退出、Profiler raw、原生样本和Frame。最终EditorFinal为有效输入；前两轮失败必须保留。
4. 原Invoke-Check `-Method CP05Build.Run` 构建含诊断驱动的非开发包，再执行本目录 `Invoke-Measure.ps1 -Build <FinalTestBuild/Release> -Output <fresh> -Probe`。默认不活动桌面显示；`-HiddenControl`仅作明确负例，`-Graphics d3d11`只改变对照启动，不写用户GraphicsSettings。
5. 新运行器依次验证真实进程、校准/必需工作负载、实际画面；会生成measurement-receipt及render-receipt。HiddenControl的视觉FAIL是原始结论，期望负例识别另行记录。不得以运行器0替代这些报告。
6. `Analyse.py <run> <fresh analysis.json> --stress` 验证24校准、各16次方法、60个普通区间、至少240个密集区间/4秒、双敌真实水平移动和实际弹体。定向query与局部帧区间分开，不是整帧性能。
7. `SelfTest.py <EditorFinal> <fresh> --stress` 为13项合成工具自测；`RenderSelfTest.py <PlayerFinal> <fresh>`为7项真实CLI分类/退出码检查，不计作人工或游戏玩法PASS。保留派生输入与实际stdout/stderr。
8. 纯包前移出runtime Probe和引用它的Editor runner，保留执行快照；原CP05Build.Run构建PureBuild。Cecil类型/PInvoke排除、8类型IL比较、实际测试包负例、所有文件SHA、Profile及Bee实际五字段分别核对。Native桥不放Assets/Plugins或发行目录。
9. 普通纯包Smoke只传训练/隔离/窗口参数，无-br驱动，无自动按键。正常WM_CLOSE后必须观察真实exit/log；这不是人工退出验收。用户现场测试使用Launch-Playable.ps1及空白记录表。

采样输入包含场景/相机/目标实际坐标、帧号、真实攻击/碰撞观察、材质计数、编译输入与运行二进制SHA。所有输出目录必须新建；日志不得覆盖。构建副本Unity写回单独记录，不能覆盖源/用户工程。
