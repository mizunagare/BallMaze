# WORLD-01 证据索引

- 发布校核：1107个原件清单文件逐字节/LFS oid一致，152个LFS文件；不含用户场景内容。
- [分层状态](status.json)、[六样本矩阵](seed-matrix.csv)、[原件/发布哈希清单](manifest.json)、[暂存与LFS核对](publication-check.json)。
- Before/feedback.json 与 After/feedback.json：真实运行反馈负例/修复后正例，含活Boss、预计核心及只读状态，不是原生点击截图。
- Samples/418-A、418-A2：编译/Safe Mode清理、实际进程结果、夹具升级暂停deadline，历史不删除。
- Samples/{418-A3,418-B,419-A,419-B,420-A,420-B}/Shared/content-nav.json：请求/实际seed、版本、完整布局、每实体/边NavMesh路径和真实长度；route-evaluations.json 为当前世界分项评分。
- 各 Shared/ordinary-combat.csv、after-exploration.json、transitions.jsonl、cycle-*.json、expected.json 和阶段主备档：实际普通敌攻击、采集拾取/地面、来源余额、恢复/结算/制造/后继Run。320断言与520导航行是不同计量，不能相加成成功率。
- PoiShared：真实祭坛选择、解除暂停后重复拒绝、新进程 Used/身份/随机流检查；不是直接设置Used。
- Death(-Store)、Fault(-Store)、Missing/Corrupt(-Store)、RecoveryMatrix(-Store)、Overflow(-Store)、BossEconomy(-Store)：实际旧规则新运行，恢复矩阵33条，受控Boss奖励与满包/死亡/重复收益，层级不冒充正常AI胜利。
- Boundary-Store/matrix.csv 与 Boundary/comparison.json：81剑枪距离边界样本，历史最终几何/命中元组只读对照零差异。WeaponContracts-Store 为15品质/多目标样本；RangedArea-Store/area.json 为34弓杖检查。
- Regression/results.json 与 Normal-Gather：输入、观测、Boss六攻击/四武器，以及正常AI三阶段真实轨迹、结算/制造和新进程证据。正常AI图片是该层级截图，不是独立人工。
- Build：输出根准备失败，构建未开始。Build02-Store/build-report-messages.json：完整96警告；Build03-Store：增量输入复验2警告，不代表修复。Build03/build-inputs.json 与 input-check.json 前后1375文件一致；release-inspection.json 是真实EXE/程序集哈希与只读PE边界。
- Bindings：开工/冻结/输入绑定、所有用户及历史保护SHA256、每次方法/退出码/超时、工具失败。完整日志gzip，原文件保留；不删除警告或异常。
- Tools/CompilerCleanup：仅隔离失败Editor的精确Safe Mode退出工具源与记录；未激活桌面、未强杀、不是U16或Player退出验收。

源码审计表和实际状态图见上级目录。纯发行/验收Player游戏、原生、人工、性能及未专测提示分支仍NOT_RUN，旧引擎/关闭根因仍UNRESOLVED。固定Git发布不代表独立复审通过。
