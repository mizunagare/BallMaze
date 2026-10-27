# PLAYER-01：正式 Player 纵切验收与环境边界

**总体：NOT_RUN，正式 Player 完整冒险纵切未通过。** 本轮完成新的正式构建、六种正式标题状态与后台关闭验证，以及新执行的 Editor 支持回归。正式 Player 中继续/读取、设置操作、改键消费和完整冒险尚无安全可执行输入/驱动条件；没有用 Editor 的成功填补这些缺口。

[任务书及 BUILD-01 限定复审](Reviews/PLAYER01_TASK.md)已归档：短路径验证规避被接受，不是 Unity 导入器产品修复，91 条警告仍开放。本轮没有修改产品文件。

## 固定输入

- 开始本地/远端 main：`3839d4f581415f20251737bba5cc1c5a4afa56ff`，开工核对一致，没有回退。
- 产品源码输入：同上；构建期间不变。测试工具/Editor 专用确认测试冻结：`4a48a30c97c9ac92adc3d9bd493c496e687c6455`，该提交不修改 Assets/Packages/ProjectSettings。
- 最终提交为上述输入加本轮报告、结果和只读采集工具；完整 SHA 以交付消息/最终 Git 提交为准，避免报告自引用。
- 根：`D:/WGP01/1027-195130-818e8dee`。构建工程位于其 `B/20261027-195132-Short-84cce09c/Project`；全新 Library，不复制 ShaderCache。
- Unity `6000.6.5f1 (3ff58d469c8a)`，Windows64，URP/Core `17.6.0`，依赖锁未变。manifest SHA256 `0b0877e7b6b46e10165ba211d9f6d9178f1239f70237ae498ebee16f350fb67e`；lock SHA256 `0abcfda7c4723ebd8777c1355faefa45f6e42401f5d3a918d2194d71211cef88`。
- 原始清单 1152 文件；全部复制字节一致，收尾源文件哈希未变。相对 BUILD-01 的 1149 项新增本地 `_Recovery.meta`、`_Recovery/0.unity`、`_Recovery/0.unity.meta`，旧项无变化。用户覆盖层单列，未声称执行输入是干净 Git 树；未发布用户场景内容。

## 本轮真实执行分层

| 层 | 结果 | 不能据此宣称 |
|---|---|---|
| 新正式构建 | Succeeded，0 Error / 91 Warning / 4 Log；187.5767 秒，127361763 bytes；进程 exit0，无超时 | 所有警告解决、发行通过 |
| 正式 Player | 6 个新进程：Missing/Ready/Corrupt/Incompatible/Pending/Committed 的 Boot→Title、截图、真实目录指纹、title-quit、后台关闭均 PASS；均 exit0、无超时 | 点击过继续/读取/设置，进入过正式游戏，真实标题栏关闭或退出保存通过 |
| Editor 规则 | Input01Rules 26 项，本轮 PASS | 26 个玩家实验 |
| Editor 虚拟 InputSystem/uGUI | Input01Play 239 项、独立进程 Resume 11 项 PASS；同有效绑定、行为/提示、取消、保存失败重试和恢复 | 正式 Player 虚拟输入、原生键鼠或人工体验 |
| Editor 存档/事务 | B09Rules 四进程、B09Cases 三进程、确认期间集合变化测试 PASS | 正式 Player 中执行过相同 UI 或故障操作 |
| Editor Gather | Normal/Resume/FinalResume 三进程 PASS，实际采集、收费修复、撤离、结算、取材制造、再次森林出征和新进程身份一致 | 正式 Player 完整冒险纵切 |
| 原生/人工 | NOT_RUN；非活动桌面探针返回 NOT_RUN，零 SendInput，无切换/激活 | U16、物理标题栏关闭、人类可理解性通过 |
| 性能 | NOT_RUN；只记录硬件及标题时序 | 游戏负载 CPU/GPU、GC、显存或性能预算通过 |

顶层协调器 **27 PASS / 5 NOT_RUN / 0 FAIL**，构建另列；27 包含关闭命令、分析和准备动作，不是27次玩家实验。验收矩阵是 **2 PASS / 5 NOT_RUN**，未运行项不被计数较多的支持断言覆盖。原始结果见 [RESULTS.json](Evidence/RESULTS.json)、[逐次 CSV](Evidence/Run/results.csv)。没有继承前批运行结果。

## P01-01 构建与警告

复用 WanxiangBuild 原 Build 方法与 BuildOptions.None；BUILD-01 诊断包装只读取完整报告。目标资产路径217字符，正常 ComputeShader，包路径 DirectoryNotFound 为0。完整95条消息保留。

91条警告与 BUILD-01 最后短根构建**逐条多重集合相同**：仍存在91、消失0、新增0。86条 CS0618 来自 Player 编译代码中的旧API，不能归为纯Editor噪声；3条 CS0414未使用字段未修改；2条 Boot/Title旧序列化版本可能涉及初始化，六次标题观察不等于升级或消除风险。另将原始Editor导入/JobTempAlloc提示单独保存，未改写为这91条警告。[分类](Evidence/WARNING_REVIEW.json)。

| 产物 | 字节 | SHA256 |
|---|---:|---|
| WanxiangGuitu.exe | 667136 | `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a` |
| UnityPlayer.dll | 38692784 | `3bdc6e4cd1b5eb85e1562b1c6018949145cdedf50cf7aceab0d1518143f9aa7c` |
| Assembly-CSharp.dll | 498176 | `41ac100fc9c88bd2b8cad27ea01bf3b4304bed2482b9cc7d594b2263be707455` |

MVID `90845514-e7c5-4307-b975-7e8bf2947399`；[身份与方法元数据](Evidence/ProductIdentity/assembly.json)。本轮正式程序集不含 Build01Audit、P01Confirmation、Input01Rules/Play、WGNormalAICheck、WGA1NormalResume、B09Rules、U16Fixture；[排除检查](Evidence/ProductIdentity/test-class-exclusion.json)。P01Confirmation在发布构建之后仅注入隔离Editor，没有塞进Player。

## P01-02/04：正式入口通过的部分与未执行的部分

六例均从正式非开发 EXE 启动，1280×720、D3D11，启动前提供显式存档根和日志路径。缺档不创建Run；坏档/未来版本不覆盖；Pending/Committed标题显示真实结算阶段；有效档显示可继续及源Profile/Run身份。未选择进入游戏，CombatSession对象数始终0。所有存档集合前后指纹相同。

关闭是只向本次拥有的窗口发送 WM_CLOSE；实际退出码、退出时间、未超时、title-quit及崩溃标记均核对。**标题未进入业务会话，没有宣称获得在途退出保存审计**。这是标题生命周期验证，不是物理标题栏点击或游戏内正常退出存档验收。

正式Player的继续/读取、确认期间变化、设置打开/取消/应用、改键后实际行为和提示尚未执行，因此 P01-02、P01-04 整项 NOT_RUN。Editor 控制层另外真实通过239/11项和确认变化检查，不能代替它们。未向正式Player注入测试DLL、虚拟设备驱动或运行时业务回调后门。

## P01-03：Gather支持证据与正式Player阻断

源码证实现有 Gather 在 `Editor/A1ValidationDrivers` 中注入 `UnityEditor` 类，启动命令使用 `-executeMethod`；GameEntry 在正式程序集剔除 EditorValidationEntry/ExplicitGameplay 绕过。不能把这条流程照搬到正式EXE并称原路径成立。因此正式Player完整纵切 NOT_RUN，未编造一次失败战斗或将未启动算作死亡。

本轮仍复跑现有 Gather 支持链，三个实际Unity PID为 **57252、53872、36320**，各进程exit0/无超时。使用旧策略原始初始配置：白弓/剑、合成携带材料及真实配方药水；不冻结敌人、不改角色属性、不出征后传送。领域操作和虚拟移动仍明确属于Editor机器人。

- Profile：`ac18e7670db74368930cfc55bc60ccfb`。
- 第一Run：`e002a58644db47ca81c7e5f2f0dea16e`，seed `1071009358`。
- 后继森林Run：`60df7a206df947dc85c9f565b079cae4`，seed `2003299434`；同Profile、确实创建新Run。
- 本次木材采集4；收费渡口木2/石1扣费一次，剩余新增木2；真实结算入仓后取木2用于制造，最后仓库木0。未沿用 INPUT-01 的历史木6口径。
- 实际制造新增装备ID：`1e32e31c12604910bea56bcf87794298`。检查点同时保存入场剩余/新增来源账、地面掉落、实体/装备ID、布局/随机流、仓库/配方与修复回执。
- 第二进程核对第一Run状态后实际撤离、重复提交无重复奖励、制造再出征；第三进程核对后继Run状态。见 [正常AI原日志](Evidence/Run/Gather/normal-results.txt)、[第一检查点](Evidence/Run/Gather/b4-checkpoint-1.json)、[第二检查点](Evidence/Run/Gather/b4-checkpoint-2.json)。

这些结果验证现有业务支持链，不能关闭“正式Player从标题完整冒险”的缺口。

## P01-05：受控故障与恢复

本项按任务书允许的受控层记 PASS：新执行的 B09Rules 包含候选保存before-publish失败、归档后故障回滚、发布后回调核对、真正新进程归档中断恢复；B09Cases通过真实放弃/结算代码生成Pending/Committed并分别启动新进程核对Profile及结算完整身份；Gather用非零真实收益验证重复提交不改变Profile。没有为了得出结果直接改最终JSON字段。

新增Editor确认回归：在真实合法继续档的完整集合上AskNew，加入专用合成并发变化哨兵后ConfirmNew明确拒绝，save.json字节保留且没有创建业务对象，移除哨兵后原指纹恢复。不是正式Player点击测试。[结果](Evidence/Run/Confirmation/confirmation-result.json)。

正式Player坏档及不兼容档只读保护另有新证据。真实玩家目录未作为测试输入或核查对象；依据为启动前显式隔离、产品路径分支与定位审计，没有额外访问真实目录来“证明未变”，也不宣称有系统调用级全盘访问追踪。

## P01-06/07与开放项

非活动测试桌面不是获授权独占的交互环境。既有worker在缺档Player上返回“非前台/不可见，不激活、不发送输入”，没有物理Esc、全局快捷键或用户桌面操作。还缺安全交互测试环境和独立人员。CPU/GPU帧时间、GC、游戏内存/显存、负载采样均未执行；CIM硬件信息和0.84–1.32秒Boot→标题记录只用于入口诊断，不能作为性能基准。

保留：D3D12 UNKNOWN、Editor青色帧、Editor.Search、JobTempAlloc根因 UNRESOLVED；原生U16、独立人工、完整性能 NOT_RUN。没有重复无新线索关闭实验，没有改生命周期消异常。

## 用户文件与交付

ForestRuins SHA256 `ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4`；ProjectSettings SHA256 `7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451`。源1152文件字节不变，新增Recovery保持未提交。已有Unity进程及其他用户程序未关闭；本次拥有进程已退出，保留进程清单为空。

仅提交本批测试/文档、证据属性与计划状态链接；产品、包、v9、经济、地图与输入系统无修改。完整证据见 [索引](Evidence/INDEX.md)，复跑见 [TESTING](TESTING.md)。最终暂停，等待固定SHA复审，不自动开始下一批，也不宣称纵切或发行验收完全通过。
