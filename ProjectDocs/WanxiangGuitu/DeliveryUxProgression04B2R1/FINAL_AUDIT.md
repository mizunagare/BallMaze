# UX-04-B2-R1-FINAL 最终独立只读审计

## 最终结论

**CONDITIONAL_PASS**

C-01～C-07在本轮授权修复及既有证据的明确边界内有关闭依据；A03九个既有Player Run及99项原始检查记录一致，原复算23191 PASS / 0 FAIL / 20 INFO已从原件重新断言并逐行映射。**但历史可重现性和归档链不完整，不能给无条件PASS，也不授权暂存或提交。** 条件见第12节。

本次没有修改产品/原交付/历史证据，没有重建或新Player Run，没有执行git add/commit/push、merge main、reset/checkout/restore/clean或UX-05。只新增本报告、白名单及本轮审计附件，原INDEX不补写。

## 1. 完整HEAD、tree与分支

| 项目 | 实测值 |
|---|---|
| HEAD | `95caf234256613d4a6e4f89a8ab0dc09c397c6b2` |
| HEAD tree | `e46232da0b87c97c39174fe58737c394a773b649` |
| branch | `feature/ux-progression-04-b2` |
| 暂存区 | 空；cached stat/name-status均无条目 |
| diff --check | exitCode=0；仅有LF→CRLF提示，不是本轮写入 |

所有11条要求的Git命令均单独记录命令、exitCode及完整stdout/stderr，全部exit=0；完整diff不是以stat代替。见 [命令回执](<FINAL_AUDIT_EVIDENCE/20261116-1343/git/commands.json>)、[完整diff HEAD](<FINAL_AUDIT_EVIDENCE/20261116-1343/git/09.stdout.txt>)。

## 2. 工作区与时间基线分类

- 相对HEAD：仅5个tracked修改，均为M，无D/R；另3个新增B2源及其meta、原有Resources.meta、未跟踪交付/历史Evidence等。没有发现无关产品源码增删。
- **不能把11:07完整快照误称整个R1开始前状态**：当时已存在部分R1修改、meta和工具。09:57八源快照保留原B2未提交状态；11:07完整快照保留接手状态；本次再对当前文件实物核算。
- 相对09:57原B2八源：7个源有R1增量，只有B2AttackModel未变。相对11:07完整快照：只有3产品源+2 R1工具变化。这两个口径均成立，不能混为“整个R1仅改3源”。

| 分类 | 路径/结论 |
|---|---|
| A：B2新增源 | B2AttackModel、B2InventoryQuery、B2Collection（均在Assets/CombatPrototype） |
| B：B2原tracked修改 | AdventureLoadout、CampInventoryView、CampRuntime、CatInventoryPresenter、ContainerInventoryView |
| C：原B2之后R1源增量 | 上述B的5个 + B2Collection + B2InventoryQuery；C为A/B重叠标签 |
| R1接手后的3产品源 | AdventureLoadout、CatInventoryPresenter、ContainerInventoryView |
| R1接手后的2工具 | Tools/IntDriverR1.cs、Tools/run_r1_player.py |
| 新meta | 三个B2新源对应meta；11:07快照中已存在，本轮不重建GUID |
| 用户Unity项 | Resources.meta仍为原有未跟踪文件；PC_RPAsset及GraphicsSettings/ProjectSettings/URPProjectSettings与HEAD、11:07均一致，全部排除提交 |
| 文档/Evidence | 按正式产物与相关历史分列，不能git add整个未跟踪根目录 |

[三时点逐源hash与大小](<FINAL_AUDIT_EVIDENCE/20261116-1343/protection/SOURCE_TEMPORAL_CLASSIFICATION.json>)、[Unity项逐文件分类](<FINAL_AUDIT_EVIDENCE/20261116-1343/protection/UNITY_CHURN_CLASSIFICATION.json>)及各源B2→final diff均可复核。

## 3. C-01～C-07独立复核

| 条件 | 从源码及原件得出的结论 | 判定 |
|---|---|---|
| C-01 | 收藏为Ordinal ID全局集合，不按容器/品质/类型共享。SortBag仅InBag before/after，SortWarehouse仅stored；Deposit/Withdraw保留ID不清收藏。Salvage所有拒绝先返回，消费成功才NotifyGearDestroyed；Prune存活集合含loadout、warehouse及pending.item.id。A03无不同活装备错误共享ID的观测。 | PASS（关闭依据成立） |
| C-02 | 两UI产品调用DisplayOrder/Apply，先过滤再新列表排序；None保留输入顺序，AttackDesc/QualityDesc/TypeAsc以Ordinal ID次级排序。实际排序目录行位置改变，网格空间位置刻意不重排。底层ID/顺序/Main/Reserve/Worn/Overflow不写入。四种排序、实际uGUI行序/按钮/滚轮与真实切UI一致性有原始依据。 | PASS |
| C-03 | 原顶部和底部调用是重复同一B2Controls；当前Draw只实际调用底部一次。原热键来源不变；A03两条Win32 down/up链own/window/foreground PID=2520，保留条None→AttackDesc，旧位置无效，截图标题无遮挡。 | PASS |
| C-04 | 扫描Assets/Packages/ProjectSettings/Library PackageCache共10446个meta、10445个不同GUID；三新GUID各仅一处，互异且不撞其余10442个唯一GUID；Player输入manifest集合相同。原资产meta763项对完整快照零缺失/零变更。 | PASS |
| C-05 | Strength0/3先真实出征进入ActiveRun，再通过RestoreProgress恢复rank；实际bonus0/15、装备8、base25、AP33/48、Main预览157/172；角色页与既有IMGUI HUD目视确认。未发现直接写最终AttackPower。默认uGUI无数字攻击字段，不冒充数值HUD。 | PASS |
| C-06 | Preview复制GearItem与候选、仅局部主备ID，未发现写真实装备/库存/容器/存档/随机状态路径。8种角色×9项canonical前后相同，144个前后FNV独立重算；随后真实选中并设为主武器成功。**不等于所有替换数值/容量可行性正确。** | PASS（仅九项只读及可用性） |
| C-07 | 逐15条before/action/after状态及输入核对完整收藏链；入库/取回同ID、源消失/目的唯一/守恒，收藏保留；失败分解不变；取消后确认分解矿石+1、装备消失；同profile/同装备复制隔离存档，新PID收藏3→0。API守卫测试与真实输入分列。 | PASS |

[源码逐调用点及行号](<FINAL_AUDIT_EVIDENCE/20261116-1343/source/SOURCE_REVIEW.md>)、[扩大GUID扫描](<FINAL_AUDIT_EVIDENCE/20261116-1343/protection/GUID_RECHECK.json>)、[Player原始依据](<FINAL_AUDIT_EVIDENCE/20261116-1343/player/PLAYER_REVIEW.md>)。上述为既有记录独立审查，非本轮重跑。

## 4. 九个最终Player Run

统一buildId：`ux04b2r1-6f876c60-b70442f9-5a2654de`。每项都查实际result、manifest、command、input、state和observation；九个物理目录独立，runId/模式/PID绑定一致，exitCode均0。

| RunId后缀（前缀UX04B2R1-A03-） | PID | 原检查PASS/总数 |
|---|---:|---:|
| sort-ugui | 4372 | 22/22 |
| sort-imgui | 2520 | 11/11 |
| strength0 | 32228 | 15/15 |
| strength3 | 14380 | 15/15 |
| preview9 | 3156 | 10/10 |
| guid | 14532 | 3/3 |
| golden | 32172 | 2/2 |
| collection | 2120 | 20/20 |
| restart | 7324 | 1/1 |
| 合计 | 9个独立PID | 99/99 |

184条文件/二进制哈希核验无异常；九目录166件文件另有独立目录指纹。[逐Run审计JSON](<FINAL_AUDIT_EVIDENCE/20261116-1343/player/PLAYER_REVIEW.json>)包含完整SHA256、文件大小与行号，而非仅9/9汇总。

## 5. 99项检查的证明级别

99项原PASS均有对应同名原始observation，不是凭summary计数。独立分级为 **51项重算、18项目视佐证、30项仅原始记录**，不得把99个driver自报PASS说成99项都被独立重新执行证明。API守卫记录的部分参数、截图存在性与完整Player过程真实性有其固有限制；结合本轮源码审查，不新增测试补洞。

[逐99项CSV](<FINAL_AUDIT_EVIDENCE/20261116-1343/player/CHECKS_99.csv>)给每项result/observation/state原始行、独立级别与依据。只读模式本来不产生装备变化时，部分state-changes文件可以为空，行为变化由对应raw observation/输入记录核对，不伪称每个文件都有状态行。

## 6. 23191项独立复算及黄金矩阵

本轮另写oracle，**没有执行/导入原recompute_r1.py来充当独立审计**。原23,211行均逐条映射到本轮从raw/asset/manifest/输入新计算的结论：

- 原检查定义的复核结果：**23191 PASS / 0 FAIL / 20 INFO**，未映射0。
- 数值/排序/指纹/SHA等原PASS映射15298；另外7893条结构/回执/存在性/来源检查从原件重断言。原PASS/expected/actual不是新oracle结论输入。
- 新oracle总断言23196 PASS / 0 FAIL /20 INFO，比原定义多5条计数交叉检查；6个原语自测和2个静态风险示例另列，不混入原统计。
- INFO保持：9条初始化前boot无raw、4条额外排序点击无structured publishedIds、7条非Main替换后数值非本项验收目标；绝不转PASS。
- 九run共163 observation、154 raw；3个Main评估、8种preview9的72项前后相同/144个FNV、157条manifest文件SHA、36个资产SHA均核对。

[最终组合汇总](<FINAL_AUDIT_EVIDENCE/20261116-1343/recompute/A03_COMBINED_SUMMARY.json>)、[完整逐原行映射](<FINAL_AUDIT_EVIDENCE/20261116-1343/recompute/A03_COMPLETE_ORIGINAL_CHECK_MAPPING.csv>)、[补充报告](<FINAL_AUDIT_EVIDENCE/20261116-1343/recompute/RECOMPUTE_REVIEW_A03_SUPPLEMENT.md>)。首轮仅覆盖15303断言的阶段报告仍保留，不能把其旧覆盖边界当最终结果。

原B2黄金矩阵独立从原始装备/资产与HEAD旧表达式重建：**Attack21/21及Defense21/21逐位一致**；AP/BP21/21在历史文本精度内一致（历史未存其原始bits，不能宣称AP/BP逐位实测）。6个B2最终manifest通过，74份其所列文件SHA/bytes匹配；加6份manifest即INDEX的80项。

container-bonus行独立为Active8+容器6=Attack14，bits1096810496；AP39，bits1109131264。旧审计曾双计的文字修正声明保留于原B2 FINAL_AUDIT第114行，但**首次45不匹配及当时修正脚本/输出不可取得**，本轮正确计算不等于补回该历史原始链。[黄金逐位CSV](<FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.csv>)、[历史检索](<FINAL_AUDIT_EVIDENCE/20261116-1343/golden/history_search.json>)。

## 7. 构建身份与166源文件

| 身份 | 实测SHA256 |
|---|---|
| R1产品Assembly-CSharp.dll（Player与Evidence归档一致） | `6f876c6090ce57e498359bf93fb812583f848d3064612c10940f24f83c389db7` |
| EXE | `b70442f90f50cd91f7af7bf2272602645fc5d02c4d3156fb221fc27c328d2436` |
| A03 Driver DLL（当前Builds live） | `5a2654dead65d59485ad4810dc44a8746609a8546e7c93c068fa8867e55da384` |
| 当前Driver源及实际执行源 | `d2b52f1f6e179ff4637c07f6ac43150b53803a09ba37d2415e317779b9c26d10` |
| 重编前Acceptance产品DLL | `1dd1b676ada592f273ea2c53ee4dcc7ba0a870cc48c724feffc3ddb19d597f49` |

166个Assets源清单逐个实物SHA无漂移；响应文件实际投入153个不同C#源，13个Editor源不属于Assembly-CSharp编译投入，不能把166误说成全部编进产品DLL。响应文件、日志、Roslyn实际hash也核验，149 defines/336 references。

这是带 **UX_ACCEPTANCE** 的产品C#重编，包含既有条件编译验收代码；不是shipping/release无验收标记包，更不是新Unity BuildPipeline资产重构建。独立sidecar与产品DLL、重编前Acceptance DLL是不同身份。既有验收脚本无请求场景不运行其case，不把sidecar注入和完整release构建混淆。336引用路径列于rsp，但历史未逐一归档所有引用内容，不能扩大为完整位可复现构建。

[构建身份逐项重算](<FINAL_AUDIT_EVIDENCE/20261116-1343/build/BUILD_IDENTITY_RECALCULATED.json>)；编译exit0不是Player PASS，本结论另有原始Run证据。

## 8. 11609项保护快照实物审计

不是只检查TSV自身：逐项读取外部PRECHANGE清单、完整workspace快照及当前文件，核路径集合、存在、baseline/current/snapshot SHA、baseline/current/snapshot大小和授权范围。**11609/11609、TSV路径唯一11609、集合相等、丢失0、未授权变更0**。

仅3产品源+2工具为AUTHORIZED_R1_EDIT；所有其它原始文件实物不变。B1/UX-03、v9/v10/v11、数值资产/成本/返还/概率/随机算法/尺寸/Boss/P1/P1C、Packages/ProjectSettings、场景/Prefab保护成立。授权文件内部的D-24委托重构及R1局部变化又由源码审查、原B2快照diff和黄金计算交叉核对。

[逐11609行含大小的重算TSV](<FINAL_AUDIT_EVIDENCE/20261116-1343/protection/PROTECTION_RECALCULATED.tsv>)、[独立摘要](<FINAL_AUDIT_EVIDENCE/20261116-1343/protection/summary.json>)。Windows extended path用于长路径，只读，不复制/恢复原件。

本轮只读入口另捕获12649个既有文件SHA/bytes；[只读闭环](<FINAL_AUDIT_EVIDENCE/20261116-1343/READONLY_CLOSURE.json>)复核本轮原件零变更/缺失。仅新增本轮输出不计作原件更改。

## 9. 历史失败与归档链

[历史逐路径hash/缺失表](<FINAL_AUDIT_EVIDENCE/20261116-1343/history/HISTORY_PATH_HASH_MISSING.json>)核查全部18个B2和27个R1运行manifest；原B2 INDEX的80项及4回执匹配，R1 INDEX的550个路径/hash关系匹配。

- B2 UGUI-01 exit3原FAIL保留；IMGUI-01/02/03仍是无有效IMGUI状态变化的诊断，不因COMPLETED字段晋升验收PASS。
- A01 sort-imgui原FAIL、foreground=false及未发原生输入保留；A02自动9/9与人工HUD不足同时保留；A03最终9/9仍独立记录。
- 旧recompute-A01的31 FAIL、schema2的10 FAIL保留，不以A02/A03覆盖；A01/A02 Driver归档实物存在且hash一致。
- 原INDEX/历史元数据 **supersededBy显式字段为0**。本轮新增[审计推导关系](<FINAL_AUDIT_EVIDENCE/20261116-1343/SUPERSESSION_AUDIT.json>)明确限定覆盖范围，不冒充原始字段，也不改历史FAIL。

| Driver历史身份 | 当前可取得性 |
|---|---|
| B2 827877e4… / 2f18b8eb… / 3ba56e19… | 历史二进制不可取得；不可宣称可重新验证这些版本 |
| B2 final b7a46b0a… | 只在Builds live，hash匹配，无Evidence归档 |
| R1早期408df57e… | 只在旧Builds live，hash匹配，无归档 |
| R1 A01 d47dcfb8… / A02 e222298a… | Evidence归档可取得且匹配 |
| R1 A03 5a2654de… | 只在Builds live，hash匹配，无Evidence归档 |

旧B2保护表还存在39条对今日raw文件hash差异：32条仅LF/CRLF表示差异，7条为已授权R1源增量。旧表原件本身未变，不能称其“今日所有raw hash一致”；当前11609新快照的实物核验独立通过。

## 10. 文档、INDEX与CSV完整性

DeliveryUxProgression04B2、DeliveryUxProgression04B2R1及PreImplementationAudit均读取实际文档、JSON、CSV和路径，不以报告计数替代。历史审查13472个引用核查关系不是13472份独立文件；无断裂Markdown路径。13项设计组合/通配表达式非字面文件路径，160项无先验hash只能登记存在及当前hash，不能倒推历史从未被改写。

R1 27次CSV身份字段与各manifest逐一一致；原文件INDEX 550关系hash均匹配，原B2 80项并非全部历史。旧“全部完成”必须结合旧CONDITIONAL_PASS及本轮R1边界阅读，不能把旧文案直接变成本次结论。[完整历史/文档报告](<FINAL_AUDIT_EVIDENCE/20261116-1343/history/HISTORY_REVIEW.md>)。

原INDEX原样保留，不更新以包含本轮附件；本轮使用独立[AUDIT_INDEX](<FINAL_AUDIT_EVIDENCE/20261116-1343/AUDIT_INDEX.json>)记录新增报告/附件SHA。

## 11. 最终提交白名单冻结

冻结的是**候选白名单**，不是git add授权：[逐路径文本](<SUBMIT_WHITELIST.txt>)、[类别/SHA/bytes/未来逐条命令CSV](<FINAL_AUDIT_EVIDENCE/20261116-1343/SUBMIT_WHITELIST.csv>)、[类别统计与排除规则](<FINAL_AUDIT_EVIDENCE/20261116-1343/WHITELIST_SUMMARY.json>)。

| 类别 | 精确范围 |
|---|---|
| A | 3个B2新增源 |
| B | 5个B2原tracked修改源 |
| C | 7个相对原B2的R1源增量；与A/B重叠，不重复提交同一路径 |
| D | 3个新meta；所有其它meta不纳入 |
| E | 逐项正式B2/R1文档、可复核工具、基线源证据及本轮审计产物；PreImplementationAudit仅为历史设计输入 |
| F | 原B2六最终Run、R1 A03正式Run、必要构建身份/源回执与实物归档 |
| G | 相关历史失败/诊断/被替代Run及旧失败复算；包括但不限于41份最低不可丢弃原件 |

清单中每个payload路径必须实际存在、逐项hash；不使用目录通配做暂存。自引用CSV/summary/index使用显式meta策略，不虚构自身hash；AUDIT_INDEX可核CSV、summary、报告及字面清单。

**明确排除**：Builds、Library、Assets/Resources.meta、四个Unity设置项（PC_RPAsset、GraphicsSettings、ProjectSettings、URPProjectSettings）、其它ProjectSettings、Packages、场景/Prefab、运行_roots、临时/无关日志、无关历史Evidence/旧交付、用户已有修改。保留Player.log与正式编译回执日志属于原始证据，不作为“临时日志”删除。PDB/ref DLL等中间产物不纳入。

仓库sparse-checkout=true且non-cone；正式目录不在当前sparse规则内，ignore关系另记录。**只有未来另获明确授权后**，才能按冻结清单逐条使用 `git add --sparse -f -- <单一路径>`；禁止git add .或直接加根目录。本轮未执行任何暂存命令。新增/移动二进制等条件若被后续批准，须重新审计并冻结清单，不自动扩展本清单。

## 12. 未关闭条件与风险

| ID | 未关闭事项 | 负责人复审所需决策；本轮不修复 |
|---|---|---|
| CND-01 | 三个旧B2 Driver已不可取得；B2 final/早期R1/A03 Driver仅Builds live，未形成可提交Evidence归档 | 接受历史不可重现例外，或另授权归档现存实物并重新核hash/冻结；不得声称恢复了缺失旧版本 |
| CND-02 | 原历史缺supersededBy显式字段 | 审核接受本轮新推导关系的范围；如需回填原索引必须另行授权，不能追认为历史已有 |
| CND-03 | 旧container-bonus双计首次失败/修正脚本输出缺失 | 接受仅保留文字修正声明的限制，引用本轮独立正确结果，不伪造原始修正链 |
| R-01 | 容器replacement preview未卸旧同类worn，first-worn可能沿用旧加成；feasible不保证实际容量/装备可行性 | 原有非本轮修复范围风险；C06只读关闭不能消除它 |
| R-02 | Inventory缺完整原始字段；只独立重算所提供canonical的UTF16 FNV与前后相等 | 不宣称九类状态全部canonical均从独立raw重建 |
| R-03 | 21行黄金矩阵不覆盖全部浮点累加组合 | 纯Python发现三Active值在double→float与逐步float模型下可差1 ULP；未核历史Mono Sum IL，不能称实际Player已回归或系数规则改变。见[边界](<FINAL_AUDIT_EVIDENCE/20261116-1343/golden/ROUNDING_BOUNDARY.md>) |
| R-04 | 既有证据是Acceptance壳+产品C#重编+sidecar，不是release/完整Unity资产构建 | 当前hash身份可核；不能以此代替未经授权的release重构建或全部平台/分辨率测试 |

## 13. 最终停止

**CONDITIONAL_PASS**：七项本轮关闭依据与当前A03数值/只读/输入证据复核成立，保护快照成立；历史归档和可重现性条件未关闭，保持独立登记。不把这些问题自行修复、补跑或改写原结论。

本轮完成只读审计与候选提交白名单冻结后暂停，等待负责人复审。没有提交、推送、合并或后续功能开发。
