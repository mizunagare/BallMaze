# CP03 独立复审整改基线

开工远端 main、本地 HEAD、指定基准均为 `72db192a527bd256e2ba18cd7ab334d8334051da`。独立分支 `fix/cp03-review-r1` 从该 SHA 创建，工作树在 H 盘；主工程用户覆盖层未复制到整改工作树，不推送 main、不合并。本报告所属整改提交由交付回复完整 SHA 绑定，不把输入 SHA 当最终 SHA。

主工程迁移至 `H:/unity/WanxiangGuitu`，原 D 路径仍为 Junction。用户修改 `ForestRuins.unity`、`ProjectSettings.asset`、`Assets/_Recovery.meta`、`Assets/_Recovery/` 原样保留。[保护前清单](Evidence/protected-before.json)、[保护后复核](Evidence/protected-after.json)覆盖 1,802 个文件（产品资源/依赖/设置/原 CP03 Evidence），全部 SHA256 未变，Git 状态一致。[产品差异](Evidence/product-diff.txt)为空。

## 输入与运行

- 唯一新合成根：`I:/WGCombat/CP03-R1-1031-A`，不接触真实存档。[owner](Evidence/owner.json)。
- 隔离工程从旧 CP03 的 `P/Project` 完整复制至新根；无原工程/旧副本写入。[复制日志](Evidence/project-copy.log.gz)。
- [冻结构建输入绑定](Evidence/frozen-build-product-binding.json)：排除 Editor/验收驱动后 1,147 个实际产品输入与原 AcceptanceBuild2 清单逐字节一致（数量以文件为准）。
- [初始工作树字节比较](Evidence/input-binding.json)、[Git 原字节比较](Evidence/input-binding-with-git.json)、[Git 指针比较](Evidence/product-canonical-binding.json)均保留原始差异，不能把差异当 0。Git LFS 指针不等于资源内容；CRLF/BOM 与旧冻结输入不同，工作树语义比较另列。
- [工作树规范化比较](Evidence/worktree-canonical-binding.json)剩 5 个设置差异；[设置来源](Evidence/settings-provenance.json)证明它们与旧工程及冻结构建输入一致，是既有隔离构建配置，不是本轮改动，也不是用户设置覆盖层。最终冻结输入绑定为 0 差异。
- 非开发 Player 使用原不可变 `AcceptanceBuild2/Release` 重新运行；[exe/UnityPlayer/程序集哈希](Evidence/input-binding.json)保留。没有声称本轮新构建、纯发行原生验收或新性能对照。
- Editor 使用 Unity 6000.6.5f1，原受控公开战斗 API 矩阵；正常 Player 从 Boot/Title 受控 Continue 载入原合成检查点，非原生点击。检查点原样复制 [回执](Evidence/RuntimeFinal/fixture-copy.json)。

历史 [CP03 报告](../DeliveryCombatPresentation03/REPORT.md)、[Runtime2 原进程结果](../DeliveryCombatPresentation03/Evidence/Runtime2/results.json)、[Runtime2 原断言](../DeliveryCombatPresentation03/Evidence/Runtime2/presentation.json)不修改。
