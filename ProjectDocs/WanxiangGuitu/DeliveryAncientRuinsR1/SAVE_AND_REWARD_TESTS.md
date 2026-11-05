# 存档与奖励复跑

使用 Unity 6000.6.5f1 与仓库固定 Windows64 Release Profile。隔离工程位于 I:/WGCombat/CP06C1-1104-A/Validation/Project。命令从本交付目录运行。以下命令中 Output 使用 I:/WGCombat/C1R1-1105-A 下的全新目录。实际启动环境与完整参数在各运行目录的 command 和 process 回执中。

1. 将 Tests 中的 C1Probe、C1R1Cases、C1Metrics 放入隔离工程的 Assets 顶层，将 C1Rules、C1Editor 放入隔离 Assets/Editor。Editor 驱动复用上一批的 UI01Before 辅助类。
2. 用 Tools/Invoke-Editor.ps1 -Method C1Rules.Run -Output <新目录> 做批量编译和规则测试。正式模式为 C1Editor.Rewards、Fault、Boss、Death、Assist、FrontierResume、ResumeRewards、ResumeBoss、MatrixSword/Spear/Staff/Bow/Twin/Great/Scythe，使用 -NonBatch。
3. 用相同脚本执行 WanxiangBuild.ValidateBuild，再用 Tools/Invoke-Player.ps1 -Exe <测试包 exe> -Output <新目录> -Mode rewards/fault/boss/death/assist/resume-frontier/resume-rewards/resume-boss/matrix-0/1/2/3/11/12/13。非开发测试包包含脚本驱动。
4. ResumeRewards 和 ResumeBoss 使用上个进程由真实 SaveProgress 写出的 SeedPackage，参数为 -SeedPackage <该目录>。复制时逐文件核对哈希，包括同一保存批次的地面战利品页。ResumeFrontier 读取前批原始三区合成存档的副本。
5. 在隔离工程关闭后，把本批测试脚本和对应 .meta 移出工程，重做 WanxiangBuild.ValidateBuild。通过 Tools/AssemblyAudit.ps1 对照测试包与纯发行包。纯包运行用 Tools/Invoke-Pure.ps1 与独立合成存档，记录标题、退出和存档前后哈希。后台关闭与真实键鼠分列。
6. 保留每轮进程退出状态、语义回执与原始日志。Tools/Summarize.py 从原始数据提取统计、Boss 时间和构建回执。Tools/Publish.py 只压缩与脱敏，不覆盖来源。

满包夹具通过真实 AdventureLoadout.Add 填入合成白剑，容量验证、领取、恢复、撤离和结算均调用产品事务。武器矩阵用明确标注的受控高生命目标固定碰撞条件，移动和命中调用产品系统。该夹具不作为难度或实战平衡证据。标准 Boss 和死亡案例使用实际战斗及正常生命变化。
