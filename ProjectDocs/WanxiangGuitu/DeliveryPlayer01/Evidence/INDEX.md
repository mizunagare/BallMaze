# PLAYER-01 证据索引

- [RESULTS.json](RESULTS.json)：P01-01～07矩阵、分层计数、六个正式标题分析、Gather身份/来源账/经济、保护文件与未运行边界。
- [WARNING_REVIEW.json](WARNING_REVIEW.json)：91条警告逐条与BUILD-01对比，Player相关风险与Editor诊断分开。
- [Build/RESULTS.json](Build/RESULTS.json)：新构建全消息计数、资产身份、输入及产物SHA；其Runs子目录有完整BuildReport消息、导入构建原日志、命令/退出/超时/复制清单。
- [ProductIdentity/assembly.json](ProductIdentity/assembly.json)、[测试类剔除](ProductIdentity/test-class-exclusion.json)：正式程序集SHA/MVID/元数据与Editor驱动不存在性。
- [Run/results.json](Run/results.json) / [CSV](Run/results.csv)：原编排结果，27 PASS/5 NOT_RUN包含准备/关闭/分析行，不是玩家实验数。
- `Run/Player-{Missing,Ready,Corrupt,Incompatible,Pending,Committed}/`：各自原始Player日志、截图、entry-audit、进程回执、关闭命令、前指纹及严格分析；状态/终局目录整个集合未改写。
- [正式缺档截图](Run/Player-Missing/title-player.png)、[有效档截图](Run/Player-Ready/title-player.png)、[Committed截图](Run/Player-Committed/title-player.png)：真正非开发Player，均仅标题，不是原生操作。
- [原生环境结果](Run/Player-Missing/native-environment.json)：NOT_RUN、未激活、未发输入。
- `Run/C/`：本轮Editor输入26/239/11、B09四进程事务故障/恢复、Pending/Committed三进程的原始日志、检查、身份、截图及退出回执。
- [确认变化结果](Run/Confirmation/confirmation-result.json)：Editor受控方法层，原档保留，不冒充正式Player UI。
- `Run/Gather/`：Normal/Resume/FinalResume原始日志、CSV轨迹、每阶段JSON检查点、储存定位审计、正常AI结果、每进程退出及实际Editor驱动源码。
- [第一Run检查点](Run/Gather/b4-checkpoint-1.json)、[后继Run检查点](Run/Gather/b4-checkpoint-2.json)、[业务完成记录](Run/Gather/normal-results.txt)：本次木4、修复木2/石1、入仓后取木2制造，最终仓库木0；Editor证据。
- `ReadOnlyAudit/`：本轮1152源文件SHA清单、版本/锁/保护哈希、只读历史包对照；不包含用户场景源内容。
- `ExecutedTools/`、`Run/environment.json`：实际入口与既有协调器/正常AI脚本快照、只读硬件/会话信息；不是性能基准或交互独占授权。
- `PUBLISHED_FILES.json`：发布文件字节与SHA256；PNG受LFS保存，原始日志不做换行归一化。

所有材料来自本轮拥有者根或明确标记的只读历史比较，完整外部Player产物/Library/合成存档保留原地不上传。没有用户真实存档、用户场景内容、凭据或缓存发布。正式Player完整游戏恢复、原生、人工及性能仍无通过证据。
