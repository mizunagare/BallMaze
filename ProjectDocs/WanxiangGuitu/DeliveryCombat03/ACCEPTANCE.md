# COMBAT-03 验收表

范围是本批规则／实现，不是人工手感或最终平衡。逐行状态与历史标签分开统计；初始和历史FAIL不能被后续PASS覆盖。

| ID | 状态 | 项目与证据 |
|---|---|---|
| P01 | PASS | 四武器源码、时序、形状、品质及取消审计；DESIGN_AUDIT.md、WEAPON_DATA.md |
| P02 | PASS | Run/layout seed418、revision5、stream1、相同初始流／配置，96对命中／伤害不变；Evidence/FixedBefore、FixedAfter、Bindings/comparison.json |
| P03 | PASS | 三体型336样本矩阵、完整冻结基线与修复版；Evidence/BeforeVerified、After |
| P04 | PASS | 15品质分支；Evidence/Contracts/contracts.csv |
| P05 | PASS | 新回归58项，最终恢复后再跑58项；Evidence/AfterReadability、FinalReadability |
| P06 | PASS | 34范围／遮挡／扇形／重复Collider断言；Evidence/Area/area.json、area.csv |
| P07 | PASS | 188旧战斗断言：取消、无假伤害、冷却、暂停、换武器、卸载、临时对象有界；Evidence/Legacy |
| P08 | PASS | 各版本24场启用AI固定场地短战，普通／精英／波次Boss死亡与重复掉落／经验检查；Evidence/BeforeVerified/duels.csv、After/duels.csv |
| P09 | PASS | 输入、伤害观测、森林双Boss回归三进程；Evidence/Regression/results.json |
| P10 | PASS | 正常AI实际采集、修渡口、撤离、结算、存取制造、再次森林出征；Evidence/Regression/Normal-Gather/normal-results.txt |
| P11 | PASS | 同Profile／Run／区域／seed／布局／随机流／装备／来源账新进程恢复；Normal-Gather/process-result-Resume.json、process-result-FinalResume.json、b4-expected.json及storage-audit |
| P12 | PASS | 非开发Windows64构建，0错94警告，实际exit0；Evidence/Build/build-report-messages.json、results.json |
| P13 | PASS | 发行程序集PE元数据与哈希、已注入Editor驱动剔除；Evidence/Build/build-type-audit.json |
| P14 | PASS | 1280×720同机位真实Editor前后图，法杖／弓近战弧光移除；Evidence/VisualBefore、VisualAfter，非原生／人工验收 |
| P15 | PASS | 用户5文件、历史879文件逐项哈希不变；Evidence/Bindings/user-final.json、history-final.json |
| P16 | PASS | 106产品C#源／副本相同，静态限定3产品文件，无存档合同／经济／掉落／随机流／地图改动；source-copy.json、build-inputs.json，六项副本设置差异照录 |
| H01 | FAIL | HISTORICAL：COMBAT02原四exit1和aggregate FAIL继续保留，R1历史不覆写 |
| H02 | FAIL | EXPECTED_BEFORE：BeforeReadability36P/19F，实际exit1 |
| H03 | FAIL | INITIAL_TOOL：Before782样本内部期限，实际exit1 |
| H04 | FAIL | INITIAL_TOOL：Measure别名冲突，无依赖Unity启动；Bindings/sequence-first-failure.json |
| H05 | FAIL | INITIAL_TOOL：BeforePaired后置证据复制失败，子进程0／外层1；Bindings/sequence-copy-failure.json |
| N01 | NOT_RUN | 最终非开发Player实际战斗操作；本批只构建／静态发行元数据检查 |
| N02 | NOT_RUN | 原生键鼠U16，未用后台／虚拟输入冒充 |
| N03 | NOT_RUN | 独立人工试玩、可理解性与最终手感／平衡验收 |
| N04 | NOT_RUN | 真实性能基准；时序与DPS样本不是CPU／GPU性能测量 |
| U01 | UNRESOLVED | 历史D3D12 UNKNOWN根因，无新关闭实验 |
| U02 | UNRESOLVED | 历史Editor青色帧根因 |
| U03 | UNRESOLVED | Editor.Search内部异常，完整日志保留 |
| U04 | UNRESOLVED | JobTempAlloc警告，未过滤／试探修生命周期 |
| U05 | UNRESOLVED | 旧C15关闭确认根因，后续通过不抹去原失败 |

汇总：16 PASS / 5 FAIL / 4 NOT_RUN / 5 UNRESOLVED。这里的FAIL包括明确保留的历史、预期负例和初次工具失败；最终产品定向回归无新增非预期失败。不是整项目全绿，不自动关闭历史问题，也不等于独立复审通过。
