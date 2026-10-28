# UX-02 证据索引

开工`da118c245a04f32909ce4c83b45e239ce2e0d2df`。本批固定本机拥有者根`I:/WGCombat/U2-1028-1959`；原始文件、保留的编译失败进程与完整二进制在本机，不上传项目缓存或用户覆盖层内容。

## 最终结果

- [分层汇总](FINAL_SUMMARY.json)：最终UX60 PASS、配方/经济89 PASS、新进程5 PASS；原战斗188 PASS；正常AI三进程；最终非开发构建0错误94警告。各层不相加为“全局通过率”。
- [最终UX规则](FinalRun-1028/FinalRulesR4/ux02.json)、[配方89项](FinalRun-1028/FinalExtrasRunR4/ux02.json)、[新进程5项](FinalRun-1028/FinalExtrasResumeR4/ux02.json)。对应目录有实际命令、时间、进程/桌面句柄回执、退出码、日志。
- [原188断言](FinalRun-1028/CombatBatchFinal/combat01.json)；[既有受影响回归与正常AI协调器](FinalRun-1028/AffectedFinal/results.json)；[三进程正常AI](FinalRun-1028/AffectedFinal/Normal-Gather/)含轨迹、期望身份、结算与制造结果。另有Regression目录的B07经济、B3、UI01和Input01结果。
- [最终构建与全部消息](FinalRun-1028/FinalBuildR4/build-report-messages.json)；[完整191文件哈希](FinalRun-1028/r4-release-files.json)；[运行时源码/保护身份](FinalRun-1028/r4-identity-proof.json)。EXE启动器可相同，程序集SHA以FINAL_SUMMARY为准。
- [用户五项保护](FinalRun-1028/protected-final.json)；[原始冻结全1154项输入](FinalRun-1028/final-frozen-inputs.json)、[导入后实际副本对应](FinalRun-1028/r4-runtime-inputs.json)。URP/Graphics/UnityConnect副本自动变化和中文同义转义明确记录，主工程未写回；运行时C#一致。真实玩家档未访问、未计算哈希。

## 同机位对照（受控渲染，不是原生输入）

|模块|修复前|修复后|
|---|---|---|
|制作1280|[旧版](FinalRun-1028/Before2/controlled-craft-1280.png)|[新版](FinalRun-1028/FinalRulesR4/controlled-craft-1280.png)|
|容器1280|[旧版](FinalRun-1028/Before2/controlled-containers-1280.png)|[新版](FinalRun-1028/FinalRulesR4/controlled-containers-1280.png)|
|容器1920|[旧版](FinalRun-1028/Before2/controlled-containers-1920.png)|[新版](FinalRun-1028/FinalRulesR4/controlled-containers-1920.png)|
|制作1920/HUD150%|未作同条件旧版断言|[新条件](FinalRun-1028/FinalRulesR4/controlled-craft-1920-ui150.png)|
|陆地Boss死亡结束|[旧版](FinalRun-1028/Before2/controlled-death-end-boss_warden.png)|[新版](FinalRun-1028/FinalRulesR4/controlled-death-end-boss_warden.png)|
|湖中Boss死亡结束|[旧版](FinalRun-1028/Before2/controlled-death-end-boss_tide.png)|[新版](FinalRun-1028/FinalRulesR4/controlled-death-end-boss_tide.png)|

各目录还保留普通/远程/精英/波次Boss的death-start/death-end。camera位置和seed固定，测试显式关闭AI并受控Damage，仅验证模型/生命周期，不是讨伐胜利证据。

原始ScreenCapture的`craft-*.png`等青色帧亦保留，不能作视觉PASS。`controlled-*.png`由实际运行时URP RenderRequest取得，临时将活动overlay映射到相机后恢复。没有原生录屏、独立人工记录或完整最终Player原生业务验收，均NOT_RUN。

## 历史与完整性

- [初始快照](Run-1028/)保留早期归档；[最终归档清单](FinalRun-1028/collection-manifest.json)列原件SHA、发布件SHA及许可token脱敏数。脱敏不删除异常/失败；本机原始日志仍保留，gzip无损保存脱敏后的完整日志。
- Before/Before2/After1/Normal-Gather/Regression/FinalRulesR2等失败与阻断全部保留；参考[失败历史](../FAILURE_HISTORY.md)。初始Normal-Gather仍是保留进程的快照，不被后来正常AI成功替换。
- [本批修改的实际运行时源码快照](Sources/)；只包含本批C#，不含用户场景或项目设置原文。
- 旧C15、D3D12、青色帧、Search、JobTempAlloc和旧Editor启动问题不关闭。用户UX01发行包、Fresh/Continue模板和协议均未改动。
