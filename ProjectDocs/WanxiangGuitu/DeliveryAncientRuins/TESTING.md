# 本机复跑

Unity6000.6.5f1、现有URP17.6/Input1.20/uGUI2.6，禁止升级、CI、真实档、关闭用户程序或强杀。先检查可提交内存≥3GB（Editor重型构建门槛5GB）及该实验工程无占用。使用全新输出目录，历史I:/WGCombat/C1-1105-A各目录不可重用覆盖。

1. 新独立worktree取固定交付SHA。游戏隔离副本只复制获准产品Assets/Packages及明确冻结的测试配置；不复制Library。已有本机实验工程路径写在Tools/Invoke-Editor.ps1；其他机器须明确改为自己的隔离路径并记录差异。不要导入MapMagic到产品。运行时复跑使用仓库保存资源，不需插件。重新作者生成仅在另外独立安装合法免费MapMagic的项目中使用Tests/C1Authoring.cs.txt，新的空资产输出，不能覆盖已冻结输出或供应商源码。
2. 将Tests/C1Probe.cs.txt、C1Metrics.cs.txt复制到隔离Assets顶层为.cs；C1Editor/C1Rules复制到Assets/Editor。依赖UI01Before来自DeliveryUI01/Tests/UI01Before.cs.txt；旧B3StreamRules来自DeliveryB3/Tests，B07Economy来自DeliveryB07/Tests，均仅放隔离Editor目录。本轮执行原样快照也保存在Evidence/*/ExecutedTools，不把驱动放正式产品Assets。
3. 先执行编译/规则：pwsh -File Tools/Invoke-Editor.ps1 -Method C1Rules.Run -Output I:/WGCombat/C1-1105-A/Rerun-Rules-<新编号>。编译失败不要启动交互式Editor造成安全模式占用。
4. 然后C1Editor.Explore/Boss/Elite/Death/Fault和Sword/Spear/Staff/Bow/Twin/Great/Scythe，-NonBatch。每次独立Editor进程，读取process.json和probe.json全部行。三区Gate用历史3ce934提交的独立副本复跑，不修改最终DefaultStage来伪造历史。
5. WanxiangBuild.ValidateBuild调用正式固定Privacy Profile，-Seconds 900。非开发测试包仍包含驱动，必须如此标注。Tools/Invoke-Player.ps1 -Exe <该包exe> -Output <全新根> -Mode explore / combat-0/1/2/3/11/12/13 / elite / boss / death / fault，调用正式运行时代码，非Editor替代。
6. 正常产品SaveProgress生成SeedPackage（含ground-loot页）；-SeedPackage <原样包> 配合C1Editor.Resume/Player resume运行，禁止修改payload。resume-frontier只验证原stage3逻辑，BossResume使用Boss实际胜利样本。测试脚本读取签名/身份，不篡改最终存档。prepare-camp是显式合成装备设置，仍走真实存取、拾取、装备与保存，不当赚取证明。
7. 本轮Tools/Invoke-Matrix、Invoke-WeaponMatrix、Invoke-FinalWeapons保留所有尝试的编排。不要盲目重跑已有输出名；复制脚本并更换唯一输出名。它们可能汇总完成而存在FAIL，必须运行Analyse.py并检查每个真实进程和语义。当前有效选择见Evidence/validation-summary-final.json，绝不删除旧FAIL。
8. 纯包：隔离Editor关闭后，将全部C1运行时/Editor工具（含.meta）移到工程外已验证目录，保留哈希。WanxiangBuild.ValidateBuild重构建。pwsh -File Tools/AssemblyAudit.ps1 -TestBuild <测试包Release> -ReleaseBuild <纯包Release> -Output <新文件>。必须用外部pwsh实际退出，不读取未由本地脚本设置的LASTEXITCODE。
9. Tools/Invoke-Pure.ps1用真实CampPackage、全新隔离根启动无测试参数的纯包，观察正式entry-audit标题状态、实际退出及存档前后哈希；后台关闭不是原生菜单交互。实际原生与人工协议见NATIVE_HUMAN.md。
10. 旧流/经济仅受控规则：B3StreamRules.Run四组PASS标记与B07Economy.Run两组标记及真实exit0。旧夹具含合成填包和直接Damage，只验证旧业务，不能混入C1真实战斗。

Tools/Audit.py核对2413保护文件、199供应商文件、核心Git与Windows原字节及全部产品输入；Tools/Analyse.py校验语义/进程/存档checksum并生成当前与历史明细；Tools/Publish.py只压缩及隐私脱敏发布，不改源证据，manifest保留源/发布SHA。Build的exe、程序集及全部数据文件共同绑定；不得只用相同通用Player启动器exe SHA判断内容。

本轮有效技术运行：915条当前PASS、0 FAIL；先行Gate52条另列。所有首次失败、重试、编译器错误、超时和工具错误均保留。GC/GPU未经校准、完整性能预算、原生/人工不得写PASS。隔离配置与模板差异未获完整等同性证明，复跑必须记录实际配置，不能静默覆盖用户设置。
