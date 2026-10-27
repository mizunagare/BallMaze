# PLAYER-02 证据索引

本批运行根原件：`D:/WGP02/1027-205135-23e14979`；Git中仅日志、回执、合成状态/哈希、执行测试源与截图。未上传Player二进制、缓存、用户场景或真实存档。

## 汇总与输入

- [尝试JSON](Run-1027-205135/RESULTS.json) / [CSV](Run-1027-205135/RESULTS.csv)：37尝试，31 PASS、6 FAIL；1失败为预启动拒绝，实际Player为31 exit0、5 exit1，超时0。不是37次冒险。
- [验收矩阵](Run-1027-205135/ACCEPTANCE_RESULTS.json)：6 PASS、3 NOT_RUN、4 UNRESOLVED。
- [1152项原始输入](Run-1027-205135/ReadOnlyAudit/source-files.json)、[最终保护](Run-1027-205135/FINAL_INPUT_PROTECTION.json)、[存档定位](Run-1027-205135/STORAGE_BOUNDARY.json)。包含用户覆盖层哈希而不包含其内容；非纯main场景。
- [最终运行源冻结](Run-1027-205135/ProductIdentity/tool-freeze.json)、[worker2源码](Run-1027-205135/ProductIdentity/Worker2Source)、[worker2哈希](Run-1027-205135/ProductIdentity/worker2.json)、[中途远端核对](Run-1027-205135/ProductIdentity/git-midrun.json)。发布器后续只读增补与运行时冻结分别记录。
- [逐文件字节manifest](Run-1027-205135/manifest.json)，Evidence禁用文本换行转换；PNG沿用仓库LFS。

## 最终非开发验收Player（215148-Short-e48dddda）

|阶段|原始回执、日志、快照与完整合成集合|
|---|---|
|Setup 64检查|[215926-Setup-2cb1c7](Run-1027-205135/Attempts/215926-Setup-2cb1c7)|
|Main 49检查|[215937-Main-03104d](Run-1027-205135/Attempts/215937-Main-03104d)|
|Pending故障/重试 12检查|[220035-Pending-19eb2e](Run-1027-205135/Attempts/220035-Pending-19eb2e)|
|Committed 5检查|[220045-Committed-59efaf](Run-1027-205135/Attempts/220045-Committed-59efaf)|
|取材/制造/再出征 33检查|[220053-Manufacture-06448c](Run-1027-205135/Attempts/220053-Manufacture-06448c)|
|后继Run新进程 5检查|[220103-Successor-bb698c](Run-1027-205135/Attempts/220103-Successor-bb698c)|
|最终启动器恢复复测|[220554-Successor-165570](Run-1027-205135/Attempts/220554-Successor-165570)|

每个目录都有实际命令、exe/DLL哈希、PID/非活动桌面、原始Player日志、实际exit/timeout、输入投递与语义回执、StorageAfter。投递成功不是语义成功。退出为测试器Application.Quit，不是原生标题栏关闭。

- [教程实机图](Run-1027-205135/Attempts/215937-Main-03104d/StorageAfter/tutorial-bindings.png)
- [真实Pending结算图](Run-1027-205135/Attempts/215937-Main-03104d/StorageAfter/Main-pending.png)
- [制造并再次出征图](Run-1027-205135/Attempts/220053-Manufacture-06448c/StorageAfter/Manufacture-successor.png)
- [Story5账目23项](Run-1027-205135/ProductIdentity/story5-business.json)、[Story4独立样本](Run-1027-205135/ProductIdentity/story4-business.json)。不能混用两个样本的数量/种子。
- [最终八类存档/设置观察](Run-1027-205135/Supporting/Catalog-220148-2a8df2e2/results.json)，之前一轮八类观察也保留在Supporting。目录输入哈希前后不变；Pending/Committed复制的是实际运行边界的完整合成集合，未改正例JSON。

## 构建、支持回归与失败

- [发行构建](Run-1027-205135/Build-R/RESULTS.json)：全新Library、0错误91警告；[PE剔除证明](Run-1027-205135/ProductIdentity/proof-Release.json)。
- [6次验收构建](Run-1027-205135/Build-T/RESULTS.json)：最终0错误114警告；[驱动存在/无Editor依赖](Run-1027-205135/ProductIdentity/proof-Acceptance.json)。每次完整BuildReport及原始导入日志均保留。
- [逐条警告变化](Run-1027-205135/WARNING_REVIEW.json)：发行91条与PLAYER-01全部相同，验收23条为驱动新增。
- [现有Input01Rules重跑](Run-1027-205135/Supporting/Rules-215552-c2aec349)：26检查，仅Editor支持层。
- [本轮10项预检](Run-1027-205135/Supporting/Preflight-20261027-213810-58859066)：命令/非零拒绝探针保留。预检原件另在Preflight与Supporting实际命名目录。
- [失败说明](../FAILURE_HISTORY.md)，六次尝试及工具扫描/枚举初始FAIL都保留。没有将Editor、截图或后台输入重标为原生U16。

- [发行143模块全扫描](Run-1027-205135/ProductIdentity/all-modules-Release.json)：所有测试标识均不存在；[验收143模块](Run-1027-205135/ProductIdentity/all-modules-Acceptance.json)仅Assembly-CSharp检出。与PE类型、引用、场景及源输入共同核对。
