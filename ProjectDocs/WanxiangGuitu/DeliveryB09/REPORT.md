# B09：正式入口、存档管理、角色动作与场景呈现

状态：B09 实现和本轮可运行自动验证完成，提交固定 SHA 复审；原生与人工验收仍开放，不代表全部发布验收通过。

开始本地与远端 main：`c401dfbe6da944d980ae5045c7b52a09fd65193c`。最终 SHA 在交付提交及远端核对后提供。

## 实际能力与实现

- 新增 Title 场景，正式 Windows 构建先进入标题。五个真实入口：继续、新游戏、读取、设置、退出。标题使用独立森林远景、uGUI 与真实 EventSystem，不先建立 CombatSession。
- 仍是单一自动存档集合，没有多个档案槽。读取页明确说明。目录、格式、兼容和新游戏事务见 SAVE_COMPATIBILITY.md。
- 目录摘要检查只读（中断的新游戏事务由独立日志恢复），分别报告缺失、有效主档、备份恢复、版本不兼容、损坏、未发布临时写入及新旧目录冲突。选择之后再次检查完整集合指纹，失败保留原集合。
- 新游戏必须二次确认：重置角色、Run、随身物品、仓库、配方、徽章及教程；保留独立设置和完整旧集合归档。候选以现有 v9 保存器写 staging，再发布，既有结算和来源账不改写。
- 通过现有 HUD 的“标题”按钮保存并返回；保存失败留在游戏，不用返回菜单绕过结算。继续待确认结算仍走原确认/发布流程。
- 设置仅包含已实现的主音量、相机灵敏度、HUD 比例、窗口/全屏与两档分辨率；固定键位仅说明，不伪装提供重绑定。
- Editor 默认编辑场景仍是 ForestRuins，现有测试继续显式打开它。正式 Build Settings 与构建代码均为 Title、ForestRuins 两场景。`-wanxiang-test-gameplay` 必须同时具有有效隔离根，仅作为明确受控的回归入口；根参数本身不能跳过标题。

## 动画资源与状态机

实际审计现有 Knight：6 个 SkinnedMeshRenderer、246 个骨骼引用、0 Animator；Legacy Animation 的全部所用剪辑绑定均能解析。现有 KayKit Adventurers CC0 资源，未下载新第三方素材，许可保留 Assets/FantasyArt/Licenses 和原素材许可说明。

复用 Idle、Walking_A、Running_A、武器攻击、Hit_A、Death_A 剪辑。Dodge 明确为既有程序化翻滚，并非骨骼翻滚剪辑。按真实水平位移取走/跑及步频；攻击/受击采样按原动作窗口映射，不决定伤害。营地静止冻结姿态，实际营地移动以营地移动时钟采样；战斗仍按缩放时间。暂停不推进技能、无敌帧或战斗。主角死亡动画可在终局世界暂停时以独立表现时间播放一次并停住，不阻断终局、不推进战斗冷却；营地静止和普通暂停仍冻结动作。

## 场景现状与范围

既有营地是 18×18 地面，镜头远处可见另一块森林平台。历史稳定截图可直接看到左上角独立地块；本轮早期审计截图有青色帧，不能据此判断地形已改善。新实现增加无碰撞连续表面与确定性的远景树木，按区域隐藏无关地块的 Renderer；森林延伸地表并替换灰色边界墙的可视部分，保留原碰撞、导航和旧布局。没有改地形版本、POI、湖水阻挡、资源、出口配置或奖励生成。实际截图还发现出口三米高不透明光柱位于出生点正后方，遮住主角；将这一个纯视觉标记改为头顶上方短柱、降低底板饱和度，保留范围/时间/费用/修复启用状态及碰撞导航。此几何遮挡不等同于 Editor 青色帧根因。

## 用户文件保护

不提交或覆盖用户修改的 ForestRuins.unity 与 ProjectSettings.asset。起始原始 SHA256：

- ForestRuins.unity：`EBC46CE7104B6D6CE90B7F510A59A401D7CDF64AE8BABC85A7EBBF881C9D16D4`
- ProjectSettings.asset：`7D06EA8265EDAAF0A1A7402CFF1E94DA015450C58899438EBF4A5D97E37FD451`

测试副本包含用户当前场景，须在输入清单中明确；不冒称干净 Git 场景。

## 验证与限制

本轮结果以 Evidence/FinalAll 的独立 All5 为准，不继承旧轮 PASS。原生 UI 与人工试玩分别 NOT_RUN；UI-01 D3D12 UNKNOWN 和 Editor 青色帧根因仍 UNRESOLVED。受控按钮调用与 Editor 正常 NPC AI 不是原生键鼠。推送不代表复审通过。B09 后暂停，不开始 B10。

营地延景与森林外圈属于表现层：不扩大营地可走范围、不去掉原森林边界碰撞。当前复用程序化低多边形场景，未实现脚掌 IK 或完整 Humanoid 重定向；精准足锁定、原生操控与人工场景可理解性不以静态截图宣称通过。

实际复核发现旧结算大面板会完全遮住死亡动作。仅在主角死亡剪辑播放且终局已安全记录、无保存错误的短暂阶段降低结算背景透明度；文字、按钮和唯一提交入口不变且立即可用。动画结束恢复原面板；保存错误不透明遮罩优先。增加0.2秒动作和完成后结算两张实际渲染图，不延迟终局或保存。

## 实际入口与关键源码

正式构建的 `WanxiangGuitu.exe` 默认进入 `Assets/CombatPrototype/Title.unity`；只有用户选择继续或确认新游戏才转入 ForestRuins。工程编辑默认仍为 ForestRuins，想检查菜单时在隔离副本打开 Title 场景。Editor 安全退出只显示提示，不关闭编辑器。HUD 右上角“标题”保存成功后返回；失败留在当前游戏。

- GameEntry / TitleMenu：正式启动边界、可见操作、读取前再核对、重复请求锁与过渡遮罩。
- SaveCatalog / NewProfileTransaction / CombatSaveSystem.Entry：真实单档目录信息、完整集合归档与原子新档发布，复用原保存器。
- GamePreferences：集合外设置，不新增虚假按键重绑定、画质档或存档槽。
- FantasyActorVisual：现有骨骼与 Legacy 剪辑采样，移动步频取实际位移，攻击不决定命中。
- ScenePresentation / ForestRegionRuntime：无碰撞延景与出口标记表现，不扩地图、不改地形 revision/导航/生成/奖励。

## 已复核的呈现边界

最终输入的受控图像已查看读取/设置/新游戏确认、营地、森林、走/跑/攻击/翻滚/受击/死亡及结果面板。12张菜单页覆盖1280×720、1920×1080、2560×1440与3440×1440；控件边界有断言。Editor截图底部“编辑器中请使用停止 Play”来自主动验证安全退出，正式 Player 的标题截图另列，不能将它说成 Player 错误。

营地当前视角不再暴露独立森林平台及18×18方形地面边缘。出口高标记不再包住角色身体，但入口相机下仍有头盔局部投影重叠；这项保留为表现限制，不能宣称任意视角无遮挡。未做营地导航范围扩张、森林新布局、精细足锁定、脚掌IK或大型美术重建。四武器业务回归与剪辑映射有证据，但没有四武器所有相机角度的人工动作手感验收。

死亡结果在动作短暂播放时仍可立即确认并保存，完成后恢复通常背景。截图是受控真实渲染，不能证明原生操控、帧间手感或人工可理解性。

## 最终实际验证（All5）

- 开始本地/远端 main：`c401dfbe6da944d980ae5045c7b52a09fd65193c`。
- 最终完整运行输入：`6ec68a88bc171af1c7e5926642b17899ab20f8ec`；产品 C# 自 `b432ac0dee324278abd7a96d415603106dfd93e8` 后未改变。其后只补报告与证据发布，最终交付完整 SHA 在推送后核对的回复中提供，避免报告自引用 SHA。
- 工程外唯一根：`D:/WanxiangValidationRuns/B09DisplayVerified/20261026-001243-cd1430ec`，本地2026-10-26 00:12～00:53左右，协调进程真实退出码0。
- 原编排行 **138 PASS / 2 FAIL / 7 NOT_RUN / 2 UNRESOLVED**。2 FAIL 为预期非零/超时探针（exit7及有界超时），**0非预期FAIL**；不能将 exit0 或这个计数说成全部验收通过。挂起测试进程列表为空。
- 82条受控规则入口记录、21个正常 NPC AI / Editor玩家bot进程、2条受控视觉任务通过；正常AI覆盖 Gather、Treasure、Bypass、Land、Lake、Tutorial、Entry，每组正常/恢复/最终恢复三进程。Entry从真实Title的uGUI回调进入，真实采集拾取、撤离取消/重启、结算、入仓、取材制造和第二次森林出征；新Run确实不同，最终继续字段精确相同。
- 最终非开发 **D3D11** Player：6种标题状态（Missing/Ready/Corrupt/Incompatible/Pending/Committed）均实际渲染、存档集合字节未变、无CombatSession提前初始化、后台WM_CLOSE退出码0/无超时/无强杀/有title-quit审计。另2个显式gameplay入口进程完成退出保存与同局恢复，均exit0。它们不是菜单按钮原生点击或最终Player完整bot冒险。
- 2个显式相对根拒绝进程均自动exit2、无超时、无强杀、`normalCloseFallback=false`，无标题/保存审计或新档集合；这是安全错误退出，不能计作正常游戏退出。
- 12张菜单/读取/设置尺寸图＋确认、营地、森林与动作/结算等共22张受控B09图；另6张真实最终Player标题图，共28张B09图。既有92张UI夹具与B08/B07显示回归独立保留。原生UI及人工理解不从这些图推定。

[完整JSON](Evidence/FinalAll/results.json) · [CSV](Evidence/FinalAll/results.csv) · [派生摘要](Evidence/FinalAll/b09-summary.json) · [逐项验收](ACCEPTANCE.md) · [证据索引](Evidence/INDEX.md)。

## 构建、源码与实际日志

Unity6000.6.5f1，URP17.6.0/Input System1.20.0/uGUI2.6.0未升级；Windows64非开发构建成功，**0错误/87警告**，总计114158204字节。全部警告保留在Build日志及build-warning-lines.json，172条带warning的原始行不等同于87条BuildReport计数；主要为现存/本轮Unity查询API弃用警告，没有隐藏或升级依赖来消除它们。

- WanxiangGuitu.exe SHA256：`001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A`。
- Assembly-CSharp.dll SHA256：`9ecf52f02121f8951f104e64f86096d8717afd001e96d8cdb384d67d6c0cdcce`；静态元数据检查所需运行类存在，Editor验证驱动/中断钩子剔除。元数据检查不是UI验收。
- 94份产品C#与冻结输入一致；70份注入规则及63份正常AI驱动均找到冻结提交来源。831份源资产/包/设置有逐文件哈希，最终副本6项差异完整列出：Assets/Settings/PC_RPAsset.asset、UniversalRenderPipelineGlobalSettings.asset，以及ProjectSettings下EditorBuildSettings.asset、GraphicsSettings.asset、ProjectSettings.asset、UnityConnectSettings.asset。它们是既有隔离设置/本轮Editor导入与测试的副本变化，不能声称所有构建输入逐字相同。
- 特别是测试副本采用受保护的用户当前场景，原ProjectSettings也有隔离副本差异；用户文件本身哈希未变且不提交。**没有执行干净Git场景/设置的逐字一致验收**，不能据当前源码匹配就忽略这些输入差异。
- 独立完整日志清点发现73个异常起点，均分类为Editor.Search内部调用栈；原上下文、完整脱敏日志保留。不是“exit0所以日志干净”，也没有据此归因产品。历史Editor截图内存分配崩溃另留原日志，资源门槛只是防护，不证明根因已解。

本地正式包保留在上述运行根的 `Build/Release/WanxiangGuitu.exe`，未覆盖源工程Builds目录。测试/复跑必须显式传隔离根，不用真实玩家档。

## 捕获漏检、修复前后与开放项

All4原计数为138/2/7/2，但6个隐藏窗口标题PNG全黑，旧校验漏检；其视觉PASS已被独立6项FAIL复审撤回。新校验增加空白帧断言，同一旧二进制在未激活测试桌面里由SW_HIDE改为SW_SHOWNOACTIVATE后取得有效画面。最终All5重新执行全部步骤，并实际查看6张标题图；没有修改产品生命周期、绘制假画面或激活桌面。失败、对照和最终结果分开，见[失败历史](FAILURE_HISTORY.md)。这不解释Editor青色帧或D3D12 UNKNOWN。

继续开放：D3D12 UNKNOWN与Editor青色帧根因UNRESOLVED；原生U16、B09菜单原生键鼠/标题栏操作、人工可理解性/动作手感NOT_RUN。默认D3D12路径本轮没有重做无新线索关闭实验。精确足锁定、所有武器/相机角度的动作与遮挡验收未完成；入口标记仍可能投影重叠头盔，错误文案仍可带底层英文诊断，属于后续体验复核内容。没有新增多存档槽、归档恢复UI或完整骨骼翻滚。

B09交付后暂停等待ChatGPT固定SHA复审；推送不是复审通过，不开始B10或后续元素地图。历史UI-01的65/2/20/1及其环境边界记录不重写。
