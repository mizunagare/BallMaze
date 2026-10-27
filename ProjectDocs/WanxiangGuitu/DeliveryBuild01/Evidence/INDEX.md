# BUILD-01 证据索引

- [FINAL_AUDIT.json](FINAL_AUDIT.json)：固定输入、源文件保护、全复制清单、包身份与产物对比、未运行边界。
- [RESULTS.json](RESULTS.json) / [CSV](RESULTS.csv)：本批全部独立运行，不继承历史 PASS；质量与取证退出码分开。
- `Runs/20261027-173924-Long-086d18f4/`：工具初次编译失败、原执行诊断源；ReadOnlyAudit 对三份旧工程只读文件/包审计，完整源文件 SHA 清单。
- `Runs/20261027-174115-Long-7b1262fc/`：251 字符额外对照，目标正常但其他包路径可失败。
- `Runs/20261027-174542-Long-383ac3cb/`：260 字符新工程基线复现，完整 97 条 BuildReport 消息与导入调用栈。
- `Runs/20261027-175029-Short-85699e2d/`：第一份短工程，完整 95 条消息，0 Error。
- `Runs/20261027-175503-Repeat-d42b8bc9/`：工具冻结后的短根独立重复；完整复制清单与实际执行工具快照。
- `Runs/Preflight-*/`：两轮 10 项预检，259/260/261、不同 Unity 输入、实际拒绝与目录未创建检查；保留预期非零退出原文。
- `AssemblyIdentity/`：旧构建与本批构建的 MVID、PE 时间戳、2278 方法签名与 IL 指纹；不把静态指纹当作实际游戏运行。
- `PUBLISHED_FILES.json`：发布证据字节数与 SHA256。原始日志不换行归一化（.gitattributes -text）。

每个构建 Runs 中含 owner、input-hashes、results JSON/CSV、完整命令、UTC/真实退出/超时/桌面进程回执、原始导入构建日志、asset-before/after、完整 build-report-messages、import-exception-context、BuildSummary、product-hashes。只发布测试根材料，不发布存档、Player/Library、凭据或用户工程副本。

原始二进制和 LastBuild.buildreport 保留在各自工程外拥有者根，不纳入 Git；其目标位置可从 owner/report 精确定位。历史 INPUT-01 证据仍在原目录，未重写。

本批证据类别是只读源码/文件审计、受控 Editor 导入/构建、离线工具规则。没有正式 Player 实际运行、原生 UI、人工或性能验收证据；相应项 NOT_RUN。历史引擎开放项保持 UNRESOLVED。
