# GAMEPLAY-UX02 原始证据索引

本轮624项发布证据：[原始与发布SHA256清单](manifest.json)。日志gzip保留原始上下文，失败/错误不删除；不发布用户覆盖层、缓存或构建二进制。

## 冻结输入、保护与资源

- [7份关键源码/两个构建全输入/五项用户文件绑定](final-bindings.json)、[开工用户SHA](user-before.json)、[合成根所有权](owner.json)。
- [资源缺失实验](resource-fault.json)、[Glow原/恢复/主工程SHA一致](resource-restored.json)。
- [54项资产与46个真实调用点](../resource-call-inventory.json)、[完整分层状态与Run身份](../SUMMARY.json)、[进程命令/exit/超时](../RUNS.csv)、[动作事件对照](../TIMELINES.csv)。
- [全部异常原上下文](log-analysis.json)、[工具语法](tool-syntax.json)。Search/JobTempAlloc仍UNRESOLVED，不能因exit0宣称干净引擎退出。

## 修复前后

- [Before7：111PASS/4FAIL](Before7/presentation.json)、[旧Damage事件](Before7/damage-events.jsonl.gz)、[旧逐帧时间线](Before7/attack-timeline.csv)、[旧执行源码](Before7/GUXCases.executed.cs.txt)。
- [After2：同115项全部PASS](After2/presentation.json)、[新Damage事件](After2/damage-events.jsonl.gz)、[新时间线](After2/attack-timeline.csv)。0.25与不足0.01的致死承伤来自真实连续Damage，没有改maxHP/Current。
- [扩展119项](AfterExpanded/presentation.json)：新增实体墙阻挡与真实未命中，真实碰撞开启。
- [MissingGlow 119项](MissingGlow/presentation.json)：既有Shader fallback、生成clip与自建Material销毁；共享材质另按所有权验证。
- [六招几何6534样本/36组矩形](BossGeometry/b07r1-rules.txt)、[原几何参数与采样CSV](BossGeometry/b07r1-geometry.csv)、[HUD数据](BossGeometry/b07r1-layout.csv)。这是数据/Show技术检查，不是实战或人工阅读验收。

## 必须保留的旧失败

- [首轮期限退出](Before/exception.txt)、[第二轮有界正常关闭回执](Before2/fixture-editor-close.json)：没有业务完成回执不能按exit0算PASS。
- [启动顺序诊断](FixtureState/presentation.json)：Start未完成后重新进入营地，不是表现根因。
- [Before3产品负例与夹具Collider错误](Before3/presentation.json)、[Before4编译失败](Before4/results.json)、[Before5 batch推进期限失败](Before5/exception.txt)。
- [Before6保留近距失败](Before6/presentation.json)、[After旧近距失败不删除](After/presentation.json)、[AfterTrace实际弹体](AfterTrace/projectile-events.jsonl.gz)。法杖近距CAMERA_SURFACE_BEHIND_MUZZLE样本未被6m对照关闭。
- 各目录均保留原Unity.log.gz、启动规格、实际退出码、命令、脚本与源码快照；根prepare-first-failure.txt记录更早A准备失败，A副本仍在工程外。

## 非开发Player与纯发行

- [验收构建原报告/97警告](AcceptanceBuild/build-report-messages.json)、[全部输入](AcceptanceBuild/build-inputs.json)、[驱动存在/无Editor引用PE与二进制哈希](AcceptanceBuild/pe-acceptance.json)。
- [运行时119项](Runtime/presentation.json)、[原Player日志](Runtime/Player.log.gz)、[实际exit0且未强杀](Runtime/GUXRuntime.exit.json)、[命令/超时](Runtime/results.json)、[Boot/Title/显式NewGame记录](Runtime/entry-audit.jsonl.gz)、[真实Damage](Runtime/damage-events.jsonl.gz)、[真实弹体](Runtime/projectile-events.jsonl.gz)、[实际时间线](Runtime/attack-timeline.csv)、[合成v9身份封装](Runtime/Game/ForestRuins/save.json)。
- Raw的“virtual”层级为沿用旧启动器标签，本批实际使用公开业务API夹具，未发送虚拟键鼠。上述均不证明原生输入或人工体验。
- [纯发行原报告/96警告](PureBuild/build-report-messages.json)、[全部输入](PureBuild/build-inputs.json)、[无GUX/旧驱动/UnityEditor引用PE与exe/核心程序集哈希](PureBuild/pe-exclusion.json)。

[报告](../REPORT.md) · [验收](../ACCEPTANCE.md) · [复跑](../TESTING.md) · [失败历史](../FAILURE_HISTORY.md)。原生U16、人工/正常AI冒险/完整性能等未执行层不由本批替代。推送不代表复审通过。
