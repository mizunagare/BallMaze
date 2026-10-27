# PLAYER-02 交付报告

本批限定结论：**隔离的非开发 Windows Player 自动化冒险纵切 PASS**；不是原生 U16、人工体验、完整性能或独立复审通过。没有产品玩法、v9 数据结构或依赖变更。

## 输入与构建边界

- 开工本地及远端 main：`428c41fa4f82e7a95c3163319384cad668b5ef6b`。开工后再次读取远端仍相同；没有回退、合并或强推。
- 最终运行时源冻结：`0453761799e0a14c0c303d1ab327ce6df15da3be`；后续只整理只读报告/发布器和证据。实际执行源及原始 SHA256 另存各构建的 `ExecutedTools/`、`runtime-injection.json`；不把构建 owner 中的当时 HEAD 当成未提交驱动的唯一身份。
- 产品输入为该基线的源码**加开工时用户工作区覆盖层**。1152 个 Assets/Packages/ProjectSettings 文件保持原始字节；用户场景、设置和 Recovery 文件未提交。故这些实机证据不是“纯 Git main 场景”的无条件复现证明，复跑须核对输入清单；不上传用户覆盖层内容。
- Unity 6000.6.5f1、URP17.6.0、Input System1.20.0、uGUI2.6.0 未升级；所有构建新短路径工程、新 Library，URT 目标路径217字符。允许已有全局下载/编译缓存，不宣称整机冷缓存。
- 1次干净发行构建：0 Error / 91 Warning / 4 Log；6次临时验收构建均成功，前5次108警告，最终114警告。发行91条与 PLAYER-01 逐条一致（86 CS0618、3 CS0414、2场景序列化版本）；最终额外23条均来自临时驱动。没有抑制警告。原始导入 JobTempAlloc 等诊断独立保留。

## 实际实现

[依赖审计](BOUNDARY_AUDIT.md)列出旧 Gather 的 Editor、直接业务调用与替代路径。`PlayerAcceptanceDriver.cs.txt` 仅在明确 Acceptance 变体的拥有者副本内成为运行时代码；默认 Release 不注入。正常 Boot→Title，选择前断言没有 CombatSession，不使用测试直入游戏开关。

uGUI使用虚拟 Keyboard/Mouse、EventSystem与真实射线目标；旧出征/结算 IMGUI 使用独立工具向精确拥有的非活动桌面窗口发送 WM_MOUSEMOVE/DOWN/UP。工具仅回执“投递”，驱动另等原按钮造成的业务变化。不调用 onClick/业务回调，不反射、不传送、不冻结AI、不改属性/奖励、不改正例存档JSON。导航只读规划，移动、普攻、拾取与H交互都经过正式消费者。所有进度定位在进程启动参数中明确指定。

新工具复用现有 Step/StartChild/FinishChild。Step仅增加默认false的可选非活动窗口显示参数；旧调用不变。工具不能切换/激活桌面或移动全局鼠标；无法确认非活动桌面时拒绝投递。驱动结束用Application.Quit，**不是标题栏关闭验收**。

## 最终实际链与账目

最终验收包 `215148-Short-e48dddda`，Story5六个独立进程：Setup / Main / Pending / Committed / Manufacture / Successor。全部实际exit0、无超时；检查数分别64/49/12/5/33/5。这些断言不是168次冒险。另以最终启动器再恢复一次后继Run通过。

- 主菜单设置改为Forward=UpArrow、Dodge=Z、Inventory=I；取消/冲突、虚拟Esc捕获取消、真实.tmp目录写入失败、重试应用、默认草稿取消、新进程恢复均覆盖。
- 正常新游戏/装备UI选择初始长枪，准备按钮出征；实际移动和资源伤害、地面掉落、E拾取、H渡口修复、开始/取消/重新撤离到Pending。敌人AI保持原状；这是一条自动化采集策略，不是三策略或武器平衡验收。
- 真实采集：木4、石3、矿4；渡口扣木2石1；结算入仓木2石2矿4。取木2石1矿2制造一把白剑，仓库余木0石1矿2，新装备ID `dcb785744d974ac1a321aaf392d6b667`。未拾取地面物不计入收益；提交失败未入仓。
- Profile `c9823e54fb6844ccb209617a26904f40`；首Run `4552c0ce9f3541cca673c96cfcc007dc`；后继森林Run `b290a184e10d4fb5ae2c9f9a7282c14e`。新进程核对region、seed、布局、随机流、装备ID、来源账；23项独立只读账目核对通过。
- 第一轮完整链Story4也保留，采集木5石6矿5，结算木3石5矿5，制造后余木1石4矿3。它是另一实际样本，不能混用数量或当成同种子对照实验。
- Pending退出后以“读取所示自动档”恢复；真实save.json.tmp目录故障使提交失败且原档/Profile不变，移除自己的空故障目录后原按钮重试Commit一次。Committed两次继续不重复发奖。仓库UI取材、制造、确认后继森林出征，再次独立进程继续成功。

## 结果与限制

P02-01～06共6 PASS；原生U16/独立人工/完整性能3 NOT_RUN；四项历史引擎问题4 UNRESOLVED。见[验收表](ACCEPTANCE.md)。没有声称全部玩家验收全绿。

总尝试37：31 PASS、6 FAIL（5次Player exit1技术失败、1次启动器拒绝而未启动Player）；无超时。全部原始失败保留，最终受影响六进程与八类目录均通过。7次构建通过；10项短路径预检、26项现有Editor输入规则通过，后者不替代Player结果。[失败历史](FAILURE_HISTORY.md)另列检查器UTF16对齐与只读账目枚举错误，不能把汇总器exit0当作这些历史失败消失。

所有实机均D3D11、1280×720、非活动私有桌面。虚拟输入、合成窗口消息、截图、Application.Quit不构成物理键鼠/人工/真实标题栏关闭证据。未重新验证全部历史地图/武器/Boss矩阵或v1～v9迁移矩阵；本批产品源码/存档合同零变更，相关输入规则与实际v9链另有本轮结果。首次Worker试验的原始源码哈希未单独冻结；其二进制、命令及失败回执仍留在外部拥有者根，最终Worker2源/哈希完整归档。

发行包PE检查未包含PlayerAcceptanceDriver、-p02-mode/-p02-expect及测试场景；验收包检出驱动，两者均无UnityEditor程序集引用。默认构建仍Boot/Title/ForestRuins。发行包本身没有驱动，**未执行它的原生完整冒险**。

[原始证据索引](Evidence/INDEX.md) · [复跑](TESTING.md) · [输入/构建/运行结果](Evidence/Run-1027-205135/RESULTS.json)。完成后暂停等待固定SHA独立复审，不自动开始新批次。
