# INPUT-01：键鼠重绑定、设置与统一提示

开始本地/远端main：`a5e770064eedb8bfc478e54d54732b991f454658`。产品/执行测试冻结：`f16bdcaee45553c9d53d525bdceecdd2e2238a1a`。最终文档/证据SHA由交付消息提供，避免自引用。按用户提供的[固定复审](../Reviews/S2R2_a5e77006_REVIEW_AND_INPUT01_TASK.md)归档，S2-R2三个已验证P2限定关闭，保留原战斗/统计成果，不再改MatrixEvidence。审核包3996清单文件大小/哈希一致，接收结论不是我方再次运行审核方测试。

## 实际实现与入口

- 标题 → 设置 → **操作 / 键位**；游戏中通过原帮助按钮或有效帮助键 → **操作 / 键位**，共用同一编辑器。19个稳定动作ID，主键＋可选别名；旧Tab/B/C和R的上下文语义保留。
- 草稿、有效快照与磁盘分开；可捕获单键/离散鼠标、取消、恢复默认草稿、应用。冲突近行提示并拒绝，不偷换另一动作。方向仅键盘；Esc、右键镜头/拖放、F2/F3/F5/F9、1/2/3和N保留，管理界面左键保留点击。
- 实际ThirdPersonHero、AdventureCombat、Inventory、InteractionResolver等消费者统一读PlayerInput，继续调用原业务方法；没有改变伤害、速度、无敌、冷却、AI、地图、掉落、制造、撤离或唯一结算。
- 快捷栏主键帽、出口/最近交互、路线/帮助按钮、教程、营地提示和旧OnGUI/武器页均使用有效快照。别名完整列在设置/帮助中，快捷键帽使用主键以防长名裁切。保留可见鼠标入口，不更改Snipaste或系统快捷键。
- 捕获、焦点、设备和场景变化清理触发/按住状态；关闭帧不穿透。输入门禁与原业务门禁相接，营地/嵌套帮助恢复进入前时钟和光标，不无条件设为1。鼠标快捷键不抢UI点击，旋转等管理鼠标快捷键仍可用。

核心源码：PlayerBindings.cs（定义/默认/冲突）、PlayerInput.cs（控件快照/上下文/提示）、InputSettingsPanel.cs（共享uGUI草稿与捕获）、GamePreferences.cs（独立设置发布）。完整[动作映射](INPUT_ACTIONS.md)列明消费者、显示与保留键。旧UI主要仅替换键位文案；原装备/来源账/结算和随机流算法不重写。

## 本轮真实验证

|层级|实际结果|限定|
|---|---|---|
|Unity产品规则|26断言PASS|默认/旧v1设置、冲突/保留/别名/鼠标/坏文件/写盘失败/重试；不是26次游戏|
|实际虚拟输入与uGUI|239断言PASS|InputSystem事件经产品消费者；含四武器默认/自定义、捕获取消、实际UI应用失败/重试、拾取/单次修复、帮助/路线/角色、管理阻断及布局；大量断言是同一场景中的布局元素|
|真正新进程标题继续|11断言PASS|从Title Canvas虚拟点击设置/返回/继续，由GameEntry恢复；同Profile/Run/区域/seed/布局/装备ID/库存/来源账/渡口回执/随机流。不是同MonoBehaviour重读JSON|
|本批受影响All|35 PASS / 2预期探针FAIL / 92 NOT_RUN / 2 UNRESOLVED|0非预期FAIL；两个负探针为exit7和诊断超时，不能当产品失败或丢弃；92包含未选旧套件，不等于92个输入缺陷|
|既有回归|B09设置、B08营地、UI01、B1、B2、B3均PASS|本轮独立执行；旧35/58汇总、26战斗、100规则/20通行未无差别重跑，不继承旧PASS|
|正常AI|Gather Normal/Resume/FinalResume均exit0|实际采集木6、修渡口一次、撤离、入库、取材制造、再次森林出征、第三进程继续；该机器人含领域命令，不是原生玩家|
|正式非开发Player|Missing/Ready均Boot→Title；实际截图/入口审计；后台关闭exit0，无超时|未点击继续前没有Gameplay Session，存档指纹保持。后台WM_CLOSE不是标题栏点击或U16|
|原生/独立人工/完整性能|NOT_RUN|本轮只读发现用户活动控制台，无已授权独占会话或可用独立测试机；没有抢占桌面或要求用户守候|

各组覆盖有交集，不把26＋239＋11或All行数相加称独立玩家实验。受控输入夹具停用敌人和设置初始物资单列；正常AI始终与之分开。参考[逐项验收](ACCEPTANCE.md)、[复跑](TESTING.md)、[失败历史](FAILURE_HISTORY.md)、[证据](Evidence/INDEX.md)。

## 构建产物与未关闭的质量问题

Unity6000.6.5f1，Windows64，BuildOptions.None。最终BuildReport **Succeeded，2 Error、91 Warning**，127363354字节，耗时1分39.710秒；真实Editor进程exit0。不能称零错误构建。只读读取同一LastBuild.buildreport得到97条消息（2错误、91警告、4日志），完整归档，未更改原计数。

两条Error均为：`Host type is not matching any asset type at Path Packages/com.unity.render-pipelines.core/Editor/Lighting/ProbeVolume/RenderingLayerMask/TraceRenderingLayerMask.urtshader.`，分别在Build player和Preprocess Player阶段。初始导入日志还记录PackageCache中的USS/UXML/URT文件DirectoryNotFoundException；已归档具体路径和栈。当前不能证明根因或运行影响，**构建质量UNRESOLVED，I14不作完全通过**。不升级/删包、不改生命周期、不重跑无新线索的关闭实验以制造零错误。

产物身份（未提交构建二进制）：

|产物|SHA256|
|---|---|
|WanxiangGuitu.exe|`001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`|
|UnityPlayer.dll|`3bdc6e4cd1b5eb85e1562b1c6018949145cdedf50cf7aceab0d1518143f9aa7c`|
|Assembly-CSharp.dll|`bd39592d1cad68a1fca56b0f092cb02cc0c629cbcd6604eb3fbb4eea82072552`|

实际Player程序集不含Input01Rules/Input01Play/Input01DeviceFocus/临时BuildReport审计类型。后者只读诊断在构建完成后注入隔离Editor，第一次辅助脚本字段类型编译错误及修正结果单独保留，不冒充发布构建编译错误，也不覆盖原All。

## 首选项、v9与用户文件保护

- GamePreferences仍version1，可选bindingVersion=1/inputBindings；老文件缺字段默认。原音量/灵敏度/HUD/窗口字段保留，坏设置有可见警告，读取不自动覆写，主动应用备份原文件。未知JSON元数据按JsonUtility原能力忽略，不宣称支持未来设置。
- 设置沿原preferences.json父目录定位；新游戏独立保留偏好。未加进Profile/Run或v9封装，不提升进度版本。真正新进程恢复全部指定身份和检查点；永久奖励/材料来源账没有因改键重建。
- 原用户ForestRuins.unity：`ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4`；原ProjectSettings.asset：`7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451`，收尾字节均不变，未纳入提交。
- 隔离场景原字节相同。隔离ProjectSettings被Unity将productName/metroApplicationDescription两行改为等价的引号Unicode转义，因此克隆哈希不同，不能称所有输入字节相同；源码31文件规范化文本与冻结Git一致。实际测试包含保护的用户场景副本，Git没有发布该用户改动；公共固定提交单独复跑时须记录场景输入差异。

## 开放项与交付边界

I01～I13的有限自动化适用项PASS；I14构建质量UNRESOLVED；I15原生/人工NOT_RUN。另保留D3D12 UNKNOWN、Editor青色帧、Search及JobTempAlloc根因UNRESOLVED，完整性能NOT_RUN。原始日志可见Search异常和JobTempAlloc警告，不以exit0冒称干净退出。

实现已交付，不代表INPUT-01、阶段2、发行或人工体验获独立复审认可。提交推送后重新核对远端完整SHA；交付后暂停，不启动新地图或下一阶段。
