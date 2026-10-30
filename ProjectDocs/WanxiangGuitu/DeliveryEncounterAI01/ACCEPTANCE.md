# 验收对照（限定自动化范围，独立复审待定）

| 项目 | 状态 | 新证据与边界 |
|---|---|---|
| 当前AI职责、状态、参数和实际缺陷 | PASS | BASELINE、DESIGN、STATE_MAP；EnemyBrain不存在，不虚构封位系统 |
| 修复前真实负例及失败保留 | PASS | BeforeRepro2、LateBeforeRepro及所有首修失败；不是离线模型 |
| 枪口遮挡、重定位、释放时再验证 | PASS | FinalRepro，实际侧移后发射、非法发射0；动态遮挡取消且不退冷却 |
| 普通/远程/精英/Boss有限错峰 | PASS（受控） | 19断言；720条件记录，360输入配对；预测窗不是全局免伤 |
| 两近战、多近战+远程、双Boss各自遭遇 | PASS（受控） | FinalBeforeMatrix/FinalMatrix，10组合四档；Warden+近战诊断不是自然同POI |
| 两Boss自然同场或相邻压力 | NOT_RUN | 现有布局分区，不改变地图凑测试 |
| 可见预警反应、正常移动与早闪对照 | PASS（有限） | 公共Telegraph/Remaining反应，真实Damage；策略/窗口并非全排列，不能推断人工手感 |
| 实际guard、POI警戒、追击与回家 | PASS（有限） | EncaiGuard13断言；不把guard关闭的局部矩阵当成该证明 |
| 暂停、禁用、死亡、场景弹体清理 | PASS（有限） | 定向/guard/战斗时序及Boss恢复回归；非全回调穷举 |
| 护甲、XP、武器、瞄准/碰撞 | PASS | 新数学85、Damage42、AIM132、时序188、区域34；源合同锁定 |
| v9、B1、来源账、唯一结算、Boss记录/奖励、RNG | PASS | 新17回归进程实际exit0，含跨进程Running/Pending/Committed；旧日志不覆盖 |
| 正常AI采集—修复—撤离—制造—再出征—恢复 | PASS | Normal三进程，实际材料5、修复一次、结算/取材制造、新森林Run |
| 纯发行构建与无观测驱动 | PASS | Build Options=None，0E96W，PE检查及输入绑定；完整警告未筛选 |
| 纯发行Player实际业务/原生键鼠 | NOT_RUN | 本批未执行，不继承PLAYER02或BAL02的历史PASS |
| 原生U16 | NOT_RUN | 没有安全独立交互环境，本轮不抢桌面 |
| 人工理解、趣味与最终难度 | NOT_RUN | 未安排独立玩家，自动化不冒充人工 |
| 全部Nav失败/抖动计数、所有生命周期组合 | NOT_RUN | 有有限导航测试和状态/位置原始轨迹，缺少全面计数，不填0 |
| 完整性能基准 | NOT_RUN | 新查询分配风险未实测，不以零采样宣称优秀 |
| 用户文件与锁定合同保护 | PASS | 5文件SHA不变，14源不变，4源与构建输入一致；无CI/依赖/进度结构变更 |
| D3D12 UNKNOWN、旧C15、青色帧、Search等历史根因 | UNRESOLVED | 无新因果证据，不擅自关闭 |

结构化断言524PASS/0FAIL；另有17相关回归进程、18矩阵进程和3正常AI进程完成，不能相加为独立人工样本。历史复现/技术/编排FAIL在FAILURE_HISTORY逐一保留；前后59个真实死亡与109个删失不是被剔除的坏样本。

本表的PASS仅指列明测试层级与有限合同。推送和构建不代表独立复审或整个玩家体验验收通过。
