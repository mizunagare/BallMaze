# B4：森林多路线与完整冒险循环

授权及开始基线：`89806fd41db84f2d331efb41e6f2f3c1e8d5cc0c`，仓库 `mizunagare/BallMaze`，分支 main。开工与发布前分别读取远端；没有 reset、force push 或重写历史。用户的 `ProjectSettings/ProjectSettings.asset` 改动保留且不提交。Unity 6000.6.5f1 和依赖不升级，未启用 CI。

## 玩家入口与实现

仍使用 ForestRuins **测试场景**。营地选择制造目标和探索目标，出征选择森林探索；路线详情展开当前图与建议。路线显示地点、经过地点、近似距离、基准风险、实际剩余采集节点/箱子/敌人/地面堆数及材料种类。耗尽的地点不再作为收益目的地，但可能作为通路显示。建议不会移动、开箱、拾取或撤离，也不消耗玩法随机流。

新布局 revision 4 / generationVersion 6 / contentRevision B06-B4。七个 POI ID、42 个资源 ID、11 个遭遇 ID 和三个出口 ID 保留。连通骨架加局部 seed 决定的湖岸连接及交叉边，包含可绕过精英与需经过精英的不同湖岸组合。相同版本和 seed 生成相同数据；地图局部随机不读取奖励或表现状态。资源与遭遇布置避让路线，岩石保留道路廊道。导航构建检查全部路线边及资源接近路径，原地点/出口/遭遇检查继续保留。

复用原有三次尝试及固定备用布局，不无限重试、不悄悄换 seed。记录 requestedSeed、实际 seed、attempt、fallback 和每次失败原因；成功备用布局不冒充原 seed 成功。revision 4 的验证器同步检查重试记录与七地点标识。旧 revision 1/2/3 从保存快照恢复，保持原路线、种子与奖励语义；不迁移重抽。旧资源模板选择顺序不变，新 revision 4 按稳定实体 ID 选择模板以避免对象枚举顺序变化。

存档封装继续v9，新增字段仅属于新布局；旧revision不要求新重试数组，缺字段不改变其布局、启用标志或随机语义。既有兼容路径与历史夹具仍由FullRegression运行，不新增存档路径迁移或物品来源推断。

五类地点奖励、遗迹装备边界、B3 随机流、B1 原子扣费/回执和唯一结算不重做。正常 AI 暴露了已开宝箱碰撞体挡住自身内嵌掉落的问题：现在仅允许该已开箱忽略其自身包含的掉落遮挡，仍检查其他阻挡体；掉落位置、数量、随机结果和旧保存位置不变，不自动领取。

## 验证口径

最终完整 All `20261024-132834-3bcdc2ee` 实际完成：**77 PASS、2 预期故障探针 FAIL、19 NOT_RUN、1 UNRESOLVED，0 非预期失败**。协调器实际 exit0、无遗留进程。40项受控规则、9项正常AI、1项92张受控截图检查通过；其余PASS包括工具与编排，不能称为77个游戏场景。19 NOT_RUN包括17原生相关、1人工、1未配置ProcDump；UNKNOWN仍UNRESOLVED。逐项见 [ACCEPTANCE](ACCEPTANCE.md)。

正式非开发 Windows 构建（BuildOptions.None）成功：0错误、69警告、114040972字节，46.8334099秒。警告主要为既有及新增调用使用Unity 6.6弃用的FindObjectsByType/FindObjectsSortMode API，未借此升级依赖或扩大改造；全部警告保存在构建日志ZIP。

构建SHA256：`WanxiangGuitu.exe` 为 `001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A`；产品代码 `Assembly-CSharp.dll` 为 `D04EBB84BE5535DB4F6F147D3D4FD194A9D55B61A9055F7F03B1C4631CB4B50E`。仅比较exe不足以证明产品代码一致，完整构建文件清单单独发布。

73个产品C#源码与隔离副本在CRLF规范化后全部一致。777个源输入逐项记录原始哈希；运行结束后隔离副本有6个设置资产差异：PC_RPAsset的预过滤派生字段、URPGlobalSettings的运行时列表、GraphicsSettings序列化新增字段、UnityConnectSettings的m_Enabled、ProjectSettings中文字转义及EditorBuildSettings的BOM。它们发生于隔离Unity导入/构建序列化，未回写源工程、未升级包；差异文件与哈希全部保留，**不声称777文件或设置与源码逐字节相同**。源用户ProjectSettings原始SHA256始终为 `7D06EA8265EDAAF0A1A7402CFF1E94DA015450C58899438EBF4A5D97E37FD451`。哈希清单是运行后的副本快照，不伪称逐时刻的构建输入采样。

正式Player四组×两进程均exit0、无超时、退出审计和保存修订/校验通过；仅证明后台Owned-window WM_CLOSE路径。它使用合成在途夹具；三条完整冒险由Editor中的正常NPC AI领域驱动验证，不能互相冒充。

最终 All 结果见 ACCEPTANCE 与独立完整运行证据；先前定向结果不继承为新 PASS。正常 NPC AI 的玩家由领域 bot 操作，未冻结敌人、未增改战斗属性、出征后未瞬移；它不是原生键鼠验收。物理通行专项关闭 NPC 并忽略其动态碰撞，仅用于受控通行检查，单独标记。

三策略各运行三个独立进程：出征并完成目标后在途保存；新进程恢复后撤离、确认唯一结算、取材制造并再次进入森林；第三进程恢复新森林。核对 Profile/Run/区域/seed/布局、随机流、装备 ID、世界实体、未拾取掉落、材料来源账、仓库和配方。Gather 实际采集并修复渡口；Treasure 实际寻宝并使用免费入口；Bypass 绕西侧到免费祭坛，核对精英未被触发、仍存活。结算摘要只发布合成断言，完整 plan 不入库。

## 保留的失败

| 独立运行 | 实际结果与处理 |
|---|---|
| 125540-723510f5 | 原产品 30 seed 拓扑相同，新增回归 FAIL；保留修复前证据 |
| 130006-d98f3e0e | 新测试驱动 CS0165 编译失败，修正测试变量初始化；不是产品运行通过 |
| 130207-55b62b97 | 初次拓扑/导航定向通过，不替代最终 All |
| 130804-aad66d42 | Gather/Bypass 完成；Treasure 在箱内晶石拾取阶段领域期限失败，进程 exit1、非外部超时；依赖阶段 NOT_RUN |
| 131056-eceb600a | 旧布局与状态查询专项通过 |
| 131515-78eb20cf | 新拾取回归复现 OPENED_CHEST_BLOCKS_OWN_EMBEDDED_LOOT CrystalShard |
| 131643-d2003aa4 | 拾取等通过；物理测试对“必须每个请求零重试”的过严断言失败。保留实际原因，改为任务允许的有界重试并分列请求/实际 seed；同步稳定新版本模板选择 |
| 132328-d1b1d7cc | 修复后专项及 Treasure 三进程通过；不作为最终 All 的继承结果 |

全部完整时间戳目录位于 Evidence/Attempts，原日志保留、发布副本脱敏。后来增加仓库/配方恢复断言，最终 All 的实际 ExecutedDrivers 单独记录哈希，避免把旧驱动当新断言证据。

首次提交的封装校验发现31份历史源码快照被Git行尾规范化，且PowerShell在断言失败后仍继续提交。后续独立提交重新按限定-text属性收录原始字节，46份快照全部按索引哈希通过；不重写历史，不改变产品或测试结果。初次失败及路径清单保留在[publication-check.json](Evidence/Provenance/publication-check.json)。

## 未完成与边界

原生 U16、人工可理解性 **NOT_RUN**；D3D12 UNKNOWN 根因 **UNRESOLVED**。历史 UI-01 的 65 PASS / 2 预期探针 FAIL / 20 NOT_RUN / 1 UNRESOLVED 不改写。后台 WM_CLOSE、正常 AI、受控截图和编译通过均不能替代原生 UI 或真实标题栏退出验收。

B4 不开发 B07 双 Boss、徽章或后续地图。ForestRuins 仍是测试森林；路线图是可通行的建议网络，开放地形并非强制走廊。随机组合数量及导航覆盖有界，不声称穷尽所有整数 seed。推送完成不代表 ChatGPT 复审通过。
