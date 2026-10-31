# CP03-R1.2 基线

独立分支 `fix/cp03-review-r1.2` 从 `00a8d740b824f9eb97c892da5195385517446e60` 创建。开工通过 GitHub 只读 GET 核对：[main](Evidence/remote-main.json)为 `72db192a527bd256e2ba18cd7ab334d8334051da`，[R1.1](Evidence/remote-r11.json)为指定基准。R1 引用仍为 `42cfd3d8f3abd4861cd672dbb8f440fae48e4b65`，不合并、不改旧提交、不推送 main。

唯一新合成根 `I:/WGCombat/CP03-R1-1031-C`，从旧隔离工程复制全新 P/Project，[日志](Evidence/project-copy.log.gz)。主工程 `H:/unity/WanxiangGuitu` 的场景、设置、Recovery 保留；整改工作树 `H:/unity/WanxiangGuitu-CP03-R1` 切至新分支。

[保护前](Evidence/protected-before.json)/[后](Evidence/protected-after.json)覆盖 3,476 项用户文件及旧 CP03/R1/R1.1 交付和证据，全 SHA 不变，用户 Git 状态一致。旧 50/33 脚本也不改，在新目录复制适配证据输入的副本。[空产品 diff](Evidence/product-diff.txt)覆盖 Assets/Packages/ProjectSettings。

非开发 Player 复用原 CP03 AcceptanceBuild2 重新运行；无新构建或纯发行原生验收声明。[1,147 项冻结输入和 exe/UnityPlayer/程序集哈希](Evidence/input-binding.json)一致。角色合同继续使用 R1.1 不变快照与 R1 固定 SHA，没有更换合同或缩小断言集合。

最终完整 SHA 由本报告所属提交及交付回复绑定，不把制定基准当最终 SHA。
