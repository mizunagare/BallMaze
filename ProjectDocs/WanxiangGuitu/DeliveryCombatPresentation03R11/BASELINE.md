# CP03-R1.1 基线

独立分支 `fix/cp03-review-r1.1` 从 R1 `42cfd3d8f3abd4861cd672dbb8f440fae48e4b65` 创建。开工远端 main 为 `72db192a527bd256e2ba18cd7ab334d8334051da`；本机 Git 两次网络失败后，通过 GitHub 只读 GET 核对：[main](Evidence/remote-main-api.json)、[R1](Evidence/remote-r1-api.json)。未 reset、force push、合并或推送 main。

主工程 `H:/unity/WanxiangGuitu` 的用户场景、ProjectSettings、Recovery 保留；整改工作树 `H:/unity/WanxiangGuitu-CP03-R1` 切到 R1.1，R1 引用保持 42cfd3d8。唯一新合成根 `I:/WGCombat/CP03-R1-1031-B`，复制新的隔离工程，不写旧副本。[复制日志](Evidence/project-copy.log.gz)。

[合同来源](Contracts/PROVENANCE.json)为 R1 Git 对象的完整原字节副本，各 293 项；旧 Evidence 不修改。真实 Editor 用原 CP03Editor/CP03Cases，非开发 Player 重跑原 AcceptanceBuild2/Release；无本轮新构建或纯发行原生验收声明。

[2,664 个文件保护复核](Evidence/protected-after.json)包含主工程用户文件及旧 CP03/R1 交付和证据，SHA 全部不变，用户 Git 状态一致。[产品 diff](Evidence/product-diff.txt)为空。[1,147 项冻结输入和二进制哈希](Evidence/input-binding.json)与旧受控构建一致。用户场景覆盖层未进入测试。

最终 SHA 由本报告所属提交及交付回复绑定，不以基准代替最终 SHA。历史 [R1 报告](../DeliveryCombatPresentation03R1/REPORT.md)保持原样。
