# 万象归途：交付 A 实施与验证报告

日期：2026-10-23。仓库 `https://github.com/mizunagare/BallMaze`，目标分支 `main`。开始本地/远端与审阅基线均为 **4f5a501f35c2e8a265e8fd72bbd6c08fbed7c02b**，最初工作区干净，没有待保留的用户未提交修改。未 reset、未重写历史、未新建仓库、未启用 CI。

代码交付提交为 **152ae5642d63759cf5ccba1e27cdb25768c2843e**。最终报告提交由本文件的 Git 历史定位，最终完整SHA及推送后远端核对在交付回复提供（提交不能内含自身SHA）。其他信息见 DELIVERY.json。报告/证据提交仅补文档，不另改已验证产品代码。源码/构建对应由 Evidence/source-manifest.json、构建哈希和结果记录交叉定位。

## 核验与增量范围

实际 Unity **6000.6.5f1 / 3ff58d469c8a**，URP **17.6.0**、Input System **1.20.0**、uGUI **2.6.0**，包与引擎未升级。基线已有分页 v9、森林第一阶段、装备容器/双武器/词缀/营地200件仓库/六材料/29高级配方/来源账/唯一结算，直接复用。v1～v8 兼容链保留，不为路径迁移虚增版本。

| 项目 | 实际处理与证据 | 结果 |
| --- | --- | --- |
| R01 合法空遭遇 | WorldReady 依赖生成/事件/波次初始化与稳定实体集合一致性，零长度与null分开；保存入口不再要求敌人数>0；已击败敌人作为死亡实例保留 | PASS |
| R01 完整流程 | 零敌人出征/采集拾取/保存/独立进程继续/撤离/重复提交/回营存取制造再出征；资源/事件不重置；主动放弃与清空据点恢复 | PASS |
| R02 警戒追击 | 感知11米仅用于发现；Engaged驱动追击，受击即时同据点警报；保留敌人离巢24米/玩家离巢31米返巢及再发现；无回血/刷新掉落 | PASS |
| R02 正常AI | 原工程正常伤害速度，绕行、圈外箭击/组警报、11米外追击、追击存取、越界返巢/返回存取、再发现、实际击杀与采集撤离 | PASS |
| R03 通行 | 生成时出生点安全投影，恢复只验证不改种子；地点、出口实际交互范围、全部出生点导航验证；20种子CharacterController实际碰撞通行，AI停用 | PASS（通行探针） |
| R03 恢复边界 | 两次失败后成功、三次后seed1备用、全失败回营；恢复导航失败阻止覆盖，重试同Run/同种子；森林坠落回当前入口 | PASS（受控） |
| R04 分页/发布 | 分页权限/写入失败、主档发布前/后中断、备份引用页缺失、主坏备好、双坏拒绝、持久终局恢复；不删除任何引用页 | PASS（受控） |
| 改名迁移 | v8/v9×营地/在途/Pending/Committed；整套主备页+档案、复制/发布中断与重试、旧目录不变、冲突明确选择、重复启动身份/收益不增长 | PASS（受控） |
| 保留系统 | 四武器、V/各冷却、六词缀/20武器品质技能效果、网格旋转交换/容器换装、仓库与待领取、六材料、29配方链、药水Q/冷却、v1～v8兼容 | PASS（各定向回归） |

规则不重设计：撤离无需清场；本局战利品穿戴不变来源；入场非消耗品保护；已用药水/材料不因死亡恢复；H仍接唯一撤离结算入口；原波次测试保留。没有添加交付 B 的新森林玩法。

## 品牌与清理

Product Name/游戏级营地与结算标题/有效Editor菜单统一万象归途；构建名WanxiangGuitu.exe，Company Name仍DefaultCompany。工程已安全改为 **D:/unity/WanxiangGuitu**，旧位置仅残留空隐藏.vs目录；Hub需添加新路径。CombatPrototype、业务类、ForestRuins场景及存档game ID不搬迁/替换。

[清理明细](CLEANUP.md)列出删除的46个旧示例文件/meta，扫描唯一外部引用已移除；没有共享资源需要迁出。当前RPG测试/夹具/许可证全部保留。另修复共享模板中11条失效GUID及5个额外空脚本测试组件，保留有效后处理/SSAO与原GUID；并修正删除后残留templateDefaultScene路径。共享SampleSceneProfile仍被渲染资产使用，保留。云项目/平台包兼容标识不改名。

## 存档与定位

[完整说明](SAVE_LOCATION_MIGRATION.md)。Windows旧 `LocalLow/DefaultCompany/BallMaze/ForestRuins`，新 `LocalLow/DefaultCompany/万象归途/ForestRuins`，由当前用户persistentDataPath解析。迁移先只读校验全套，复制staging、逐文件SHA256及源未变化校验、Flush、再发布。旧目录保留，不仅复制save.json。新旧独立档不覆盖不拼接；明确选择继续新版或退出/修复重试。失败不初始化空档，主备引用页缺失不偷删页通过校验。定位层不发奖、不重开局。

## 实际运行与测试类别

- **干净隔离导入/编译：PASS。** 使用只复制Assets/Packages/ProjectSettings、不带Library的全新副本，交付脚本完整执行19个方法，退出码0，无超时。最后修正模板默认场景/当前说明后复跑资源审计与正式构建；不改玩法代码。
- **非开发Windows构建：PASS。** BuildOptions.None，ForestRuins唯一入口；正式Release不含WGPlayerFlow。见最终BuildSummary与构建SHA256。首次干净构建有旧API警告，不能写成“全程无警告”。
- **正式产品默认启动：PASS（启动/隔离定位）。** 无运行测试驱动，非batch启动，在显式隔离根创建v9营地档。隐藏窗口没有可用MainWindowHandle，CloseMainWindow返回false，测试工具最终主动终止进程（exit=-1）；这不计为正常退出验收。
- **新进程恢复：PASS（受控）。** 单独非开发PlayerVariant只增加验证驱动，三进程exit0/无超时。验证同Run零世界、页面、采集/事件、引导撤离、重复提交、入库取出制造/装备存取、再出征、Pending死亡与主动放弃恢复。该驱动会定位主角/注入致死伤害，不冒充正常AI。
- **正常AI原工程自动试玩：PASS。** 实际种子418（请求1153043384；测试LayoutFactory固定418，非随机种子抽样），generation3/contentB06-A1；弓主武器/剑备用，携入石1矿2，正常生命/伤害/速度，AI全启用，出征后无传送。真实箭击、追击返巢、击杀、攻击树拾取木3、5秒撤离、木3入仓、取料制造、再出征，记录和四张原始截图在Evidence/NormalAI。
- **冻结AI通行：PASS。** 20种子，地点+出口范围+出生点；仅通行，不等于战斗或人工试玩。
- **人工操作试玩：NOT_RUN。** 长时平衡、所有种子/四武器完整收益路线、交付B的三条完整路线、断电/真实磁盘满/ACL损坏场景均NOT_RUN；已有故障注入不冒充真实断电或物理磁盘故障。

实际入口与复跑参数见 [TESTING.md](TESTING.md)。Windows测试构建在本机隔离目录，未提交二进制、Library/Temp、原始许可日志或真实玩家档。

## 失败记录与复测

最终交付矩阵无未解决产品FAIL，但曾实际失败，保留Earlier-runs与断言摘要：

1. 共享模板资源审计FAIL（11条失效GUID），定向清理无效组件/弃用资源，资源审计复测PASS；未屏蔽检查。
2. 首次正常AI驱动等待使用Time.time，结算暂停使等待超时；第二次末尾日志访问已销毁目标导致工具异常。改成Editor实时时钟/先结束日志，第三次完整ALL_PASS、exit0。它们是测试工具修复，不用未完成尝试代替完整冒险。
3. 补跑旧容器Final时缺container-v2别名夹具；用仓库现有v2原始载荷提供别名，断言未削弱，完整复跑PASS。
4. 新药水检查初次拷贝时机晚导致类未导入；重新启动导入后PASS，交付脚本在首次导入前准备全部源码。

原始日志可能含Unity内部SearchDatabase/JobTemp分配警告；不把它们隐藏，也不将进程exit0自动等同于所有界面/性能均无缺陷。断言、退出码与截图一起看。

## 已知限制与下一批

分页无垃圾回收/总磁盘配额，历史档与中断staging会增长；磁盘/权限问题会阻止保存而非丢物品。旧新冲突界面仅能明确继续新版或退出修复，不提供自动合并/反向覆盖。战斗瞬时弹体/前摇不续播仍是原兼容规则。正常AI仅一条固定布局有收益路线，不等于全地图平衡。

交付 B **仅规划、未实现**：B1渡口修复与扣费幂等、B2地点收益/配方目标、B3五类随机流隔离、B4正常AI三条有收益路线和100规则/20通行。B06完成再进入B07双Boss/徽章，B08天气陷阱等。不因本轮测试通过宣称整批森林完成。

推送完成仅代表可复审；尚未通过ChatGPT复审。

## 仓库证据索引

- Evidence/final-runs.json：19方法完整退出码/耗时/超时、最终2项复测和独立验证构建；final-assertions.txt为断言与原日志哈希。
- Evidence/final-player-process-results.json、final-player-assertions.txt：3个进程实际结果。
- Evidence/NormalAI/：原工程正常AI的元数据、逐步记录、CSV与4张真实运行截图。
- Evidence/BuildSummary.txt、build-artifacts.json：非开发正式/验证构建区分与文件哈希。
- Evidence/source-manifest.json：产品输入文件SHA256、C#与构建副本比较（全部一致）；记录Unity导入/构建自动序列化设置差异，不宣称原始文件逐字节完全不变。
- Evidence/earlier-runs.json、assertions.txt：较早通过/失败与后续修复记录。
- cleanup-scan.json、CLEANUP.md：删除前引用扫描与完整删除/保留清单。

本机最后正式程序位于 C:/Users/guan/Documents/unitytest/WanxiangDeliveryA/ReproResults/Release/WanxiangGuitu.exe。仅编译警告/自动生成的本地设置不作为升级或夹带修改提交。

## A1 复审更正（2026-10-23）

固定提交deaf0258的正常AI命令缺少启动隔离参数，后续切换InitializeStorage不能证明默认Start此前未访问玩家目录。因此历史“始终不使用真实玩家数据”的正常AI启动口径撤回：历史是否实际触及玩家目录 **未核实**；没有证据确认损坏，也不能确认绝对安全。旧PASS仅保留为当时后段玩法断言结果，不继承为A1启动隔离PASS。A1修复、首次到退出路径记录和本轮重跑结果见 ../DeliveryA1/REPORT.md。19方法与受控Player的旧记录仍是历史结果，不代替本轮运行。
