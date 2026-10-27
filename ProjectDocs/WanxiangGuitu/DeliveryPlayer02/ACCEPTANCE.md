# PLAYER-02 验收表

范围为临时非开发正式运行时验收包，非Editor替代。独立复审未由开发者判定通过。

|编号|本轮状态|依据/边界|
|---|---|---|
|P02-01|PASS|RuntimeInitialize组件，无UnityEditor依赖；文档源仅注入隔离验收工程。|
|P02-02|PASS|正式验收Player八类标题/设置输入、并发确认拒绝；输入集合只读核对。|
|P02-03|PASS|UpArrow/Z/I真实消费；HUD、帮助、教程、取消/冲突/默认草稿、写入失败与设备/焦点恢复。|
|P02-04|PASS|Story5六进程完整业务链；真实输入/碰撞/采集/拾取/收费撤离/结算/仓库/制造/后继森林。|
|P02-05|PASS|Pending与Committed恢复、提交写入失败/重试、重复恢复及后继Run身份/布局/随机流/来源账。|
|P02-06|PASS|发行0错91警告，最终验收0错114警告；独立PE类型/引用/字符串与场景输入证明。|
|原生U16|NOT_RUN|无安全独立原生交互环境；虚拟设备与PostMessage均不替代原生键鼠。|
|独立人工理解/试玩|NOT_RUN|没有独立试玩人员，不以自动化代替。|
|完整性能基准|NOT_RUN|未做固定负载CPU/GPU/GC/显存等测量。|
|D3D12 UNKNOWN|UNRESOLVED|保留历史状态，本批未开展无新线索实验。|
|Editor青色帧|UNRESOLVED|保留历史状态，本批未开展无新线索实验。|
|Editor.Search|UNRESOLVED|保留历史状态，本批未开展无新线索实验。|
|JobTempAlloc|UNRESOLVED|保留历史状态，本批未开展无新线索实验。|

- 原始31 PASS/6 FAIL为尝试计数（其中1次预启动拒绝），不能当作37次冒险；历史失败保留。P02矩阵6 PASS、3 NOT_RUN、4 UNRESOLVED与尝试计数分别报告。
- 最终Story5六个业务进程全部PASS；最终八类目录PASS且输入集合不变。既有规则为独立Editor支持层，不冒充Player。
- 旧存档版本全面迁移、完整Boss/地图矩阵、本轮业务死亡、发行包原生操作未新执行，不继承旧PASS。产品零变更及输入清单不等于这些矩阵已重新执行。
- 保存失败是合成根中的真实文件系统障碍；正例业务档均由游戏运行时生成，坏档/99版本为明确负例，禁止用于冒险成功证明。

证据：[逐项机器结果](Evidence/Run-1027-205135/ACCEPTANCE_RESULTS.json)、[实际进程CSV](Evidence/Run-1027-205135/RESULTS.csv)、[最终账目](Evidence/Run-1027-205135/ProductIdentity/story5-business.json)、[发行排除](Evidence/Run-1027-205135/ProductIdentity/proof-Release.json)。
