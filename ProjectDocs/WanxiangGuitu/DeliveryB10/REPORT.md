# 《万象归途》B10 / B10-R1 黑猫猫族世界交付报告

> 首版实现与本地终验已完成；部分美术、原生/人工及既有根因仍开放，整体UNRESOLVED，等待固定SHA复审。输入冻结提交 `6cad42d535347e0d96ede0e40f3d6a889a846bab`；开始远端main `b474765dc9c28aaf7d2d267bc0362f828f1902b0`。最终交付链接以聊天中的远端核对SHA为准，不将文档提交冒充构建输入。

## 视觉依据与实际范围

最新用户主视觉为 [黑猫猫族世界概念](ArtBible/Concepts/Revisions/用户主要视觉参考_黑猫猫族世界.png)，原样复制、SHA256见同目录black-cat-primary-reference.json。它覆盖此前简化03/06的方向优先级；保留简洁UI阅读原则。15张概念PNG（原包9、历次修订5、最新用户图1）和03用户JPG均为设计参考，不是游戏成品。未将其他游戏角色、Logo、图标、地图或具体UI复制到产品。

STYLE_GUIDE v0.7提取约2.7～3头身、浅色口鼻/琥珀眼、黑毛红巾、皮革肩带铜扣、暖棕/森林绿/青蓝、职业工具与精英/Boss尺寸层级。原创代码制作并烘焙：5 Mesh、17 Material、14角色Prefab、47道具Prefab、4武器Prefab、47透明PNG、1图标边界数据，共135资源（276个文件含meta）。前后采用同一驱动、seed与分辨率；before是提交b474的场景，after保留用户现场场景/设置改动，所以不是逐像素相机一致或把所有画面差异归因于B10。资源不等于137个设计条目；同类部件复用、若干图标语义别名均如实记录。

- 主角及5设施猫：脸、耳、尾、背包、肩带、扣件、围裙、护目镜、账本和记录板实际接入。设施猫为静态视觉代理，靠近使用原设施业务；物资猫共用仓库，没有新商店、游走或对话AI。
- 敌人：盗匪/投掷手/猫爪菇/林灵/猎手/猞猁变体，陆Boss苔石肩铠枝角、水Boss晶蓝鬃鳍与水面显灵。沿用原攻击、伤害、掉落、徽章和唯一回执。显示名可变化，内部forest:warden/tide等ID不变。
- 材质/模型：圆润体积与倒角，钢Metallic .65/Smoothness .38、皮革Smoothness .20、布.07、水.42为首版参数。没有真实毛发纹理、面部骨骼或新软蒙皮，不能称与概念图绘画完成度一致。
- 动作：原创刚性分件绑定已有KayKit骨骼与CC0剪辑；Idle/Walk/Run/Attack/Hit/Death，Dodge仍程序化。攻击动画不决定伤害；没有改HP、移速、无敌帧或冷却。受控姿态激活、真实移动/伤害检查与正常AI实际战斗分开归档。
- UI：主菜单/存档/设置/HUD与7页管理uGUI使用共享字体、图标、深色面板、奶油选中与品质边框；拖放/旋转/主副武器、仓库、制造/配方/目标、药水、容器替换、待领取、保存调用原业务。旧PlayerInventory OnGUI对应分支停用。历史出征与结算面板仍保留原绘制、共享色板，未宣称所有旧面板全面迁移。
- 场景：标题可见实际猫族营地与清场远景；营地设施/物资、林冠/岩体、湖岸/遗迹/出口标记仅改表现。标题脸部树冠遮挡用实际截图发现并增加镜头断言。既有地形、深水碰撞、NavMesh、免费出口、森林开放探索与旧revision不变。

## 正式入口根因与边界

初始隔离入口回归实际打开ForestRuins后直接创建CombatSession/HUD，没有Title，exit1；旧正式Player也保留显式测试直入分支。B09无绕过参数的启动样本当时可显示菜单，因此不将用户现场猜为某登录服务问题（源码未发现该登录模块），也不说所有旧Player都必然无菜单。

本批Boot→目录/状态检查→Title→明确Continue/Read/New→Forest。普通Editor Play经playModeStartScene进入Boot；明确启动前隔离+-executeMethod仍有测试入口。正式Player剔除旧直入分支，旧参数在合法隔离根下也只到菜单，无合法测试隔离时提前拒绝。Session/保存增加授权门禁，菜单前不创建游戏HUD、新Run或写入新档。正式构建为Boot/Title/Forest三场景，不修改用户ForestRuins或ProjectSettings。

## 存档与业务

仍为单一自动档、v9封装，兼容v1～v9。缺失、有效、损坏、不兼容、Pending/Committed及写入不确定分开展示。继续与读取保持同一Profile/Run/区域/seed/布局/随机流/装备ID/来源账/教程；不重抽奖励。新游戏需确认并沿用完整集合归档/staging/原子发布，取消和故障不覆盖旧档。

没有新经济字段或存档迁移。六种真实材料、B1渡口、B2目标、B3随机流、B4导航评分、双Boss徽章、教程与唯一结算继续原系统。草药/食用蘑菇/布料/卷轴/任务卷只有资源制作，无业务物品，CREATED；独立角色立绘CONCEPT_ONLY。模板条目没有删除来提高通过率。

## 验证口径

最终新All目录：`D:/WanxiangValidationRuns/B10R1ReadinessFinalAll/`下唯一运行。原有三个All和B10R1中间All均独立保留，不能继承PASS；首次失败见FAILURE_HISTORY和Evidence/FailureAttempts。实际结果如下；历史失败独立保留。

区分源码审查、受控规则/截图、Editor正常AI、无驱动非开发发行Player、显式驱动非开发验证Player、原生键鼠与人工试玩。验证Player中的uGUI回调不是原生点击。后台WM_CLOSE与游戏退出按钮也不等同真实标题栏路径根因已解决。

## 引用错误审计与最小修复

前一轮b538输入按进程为144 PASS/2预期FAIL，但日志独立门禁实际发现549次CatInventoryPresenter产品空引用，不能认定验收通过。原始完整结果与审计在Evidence/BeforeReadiness。根因为无Profile的旧规则场景打开背包时读取Profile.pending；已补“Profile缺失→真实未就绪提示/禁止数据操作→实际初始化后恢复页面”，不创建空档、不改库存、不catch吞异常。修复前新回归exit1，修复后7个定向步骤PASS且6份日志的引用错误为0。

编排器末尾新加B10.runtime-log-gate，实际扫描产品栈的NullReference/MissingReference/MissingComponent，即使测试exit0也返回FAIL。仍保留完整异常目录，不宣称该窄门禁覆盖所有可能错误。当前新完整All输入为6cad42d5，旧轮结果不继承。

## 已知限制

- UI01 D3D12 UNKNOWN、Editor青色帧根因UNRESOLVED；原生U16、独立人工可理解性/试玩NOT_RUN。没有新因果证据，不重复无效关闭实验或试探产品生命周期。
- 当前是原创程序化猫族首版，不是手工雕刻/毛发纹理/完整猫科软蒙皮的最终美术。NPC静态；营地/森林仍需后续人工审美反馈，不能凭自动截图认定“概念一致/玩家满意”。
- 未新增商店、任务系统、草药经济、后续区域或多存档槽。尚未完成的设计条目保留真实状态。
- 性能仅记录独立非活动桌面受控Player的实际计数；非冒险性能基准，缺失GC等标NOT_RUN。
- 历史中间All的故障注入用例遇到一个真实不可达候选，正确走备用布局却不满足其“第三次一定成功”的随机测试前提；未改地图或放宽断言，原seed未称修复。另一个中间Editor启动挂起进程按规则保留。最终All结果与这些历史失败分别记录，不能抹除。
- LFS本地对象与实际上传另附回执，账户剩余额度无账单能力，不能由fsck推断。两份用户文件哈希核对且不提交；日志脱敏，不上传真实档/分页、凭据、Library、Temp或构建二进制。

完成后暂停等待固定SHA复审，不自动开始B11；推送不等于复审通过。

## 最终实际结果（2026-10-26）

新完整All为 `20261026-202935-daf97cfa`，产品/执行输入 `6cad42d535347e0d96ede0e40f3d6a889a846bab`。**146 PASS、2个预期探针FAIL、0个非预期FAIL、3 NOT_RUN、2 UNRESOLVED**；编排器实际退出0，整体仍UNRESOLVED，不能当作发布或完整美术验收全通过。

- 新增引用错误门禁实际扫描117日志，**0产品引用错误**；此前549次CatInventoryPresenter空引用已修复。完整审计剩73条Editor.Search内部索引异常，原始上下文完整保留，不归因于Player或称已定位根因。
- 7策略×3进程＝21正常AI/恢复步骤PASS：采集、寻宝、绕精英、陆Boss、湖Boss、教程、标题入口。正常属性、合成起始物资，测试Input System设备驱动；敌人正常AI、实际攻击/采集/掉落/制造/结算，非Windows原生或人工试玩。
- 无驱动非开发发行Player：Missing/Ready/Corrupt/Incompatible/Pending/Committed/LegacyFlag/Uncertain八类先显示Title，8/8 PASS；后台WM_CLOSE退出回执与无存档变更检查不代表真实标题栏关闭根因解决。
- 独立显式驱动的非开发验证Player：15/15步骤，read/continue/new/pending均实际退出0、无超时；entry-audit中的quit请求/回执、storage-audit、校验和及修订13→14的新进程同Run继续通过。实际菜单/背包/角色/营地准备/工作台回调与截图，**不是原生点击**。返回标题前先保存，不能混称仍在冒险时点击标题栏X的保存测试。
- 正式构建：Unity6000.6.5f1，Windows64、非开发、Boot/Title/ForestRuins，0错误88警告；全部日志/警告行及BuildReport总数分别保留。公司DefaultCompany、产品万象归途；引擎与包不升级。
- 109产品C#在LF归一化后与运行副本一致，276猫族文件与输入逐字节一致；1143构建输入原始SHA完整记录。6处原始差异涉及Unity导入/预过滤、图形序列化、云连接隔离和换行/Unicode表示；不声称所有原始文件逐字节相同，用户两份文件源哈希不变且未提交。

[完整结果/CSV/轨迹与日志](Evidence/FinalAll/) · [构建与源码审计](Evidence/FinalAudit/) · [最终聚合JSON](Evidence/FinalAudit/closure-summary.json)

### 资产统计与覆盖

15概念PNG+03用户JPG；135实际Unity资源、276文件（含meta）；137设计条目：**15 VERIFIED（限定技术导入/引用/实际运行，不是人工认可）、111 INTEGRATED、5 CREATED、6 CONCEPT_ONLY、0 BLOCKED**。有实际制作/路径131/137=95.6%，实际接入126/137=92.0%，技术逐项VERIFIED15/137=10.9%；不把概念映射100%冒充游戏完成率。

VERIFIED：WX-UI-001～009、WX-UI-201～203、WX-CHR-001/002/013。每项来源、类型、大小/SHA、导入、使用位置和实际证据见ASSET_CATALOG、ASSET_INVENTORY与RUNTIME_VERIFICATION。其余不因一张截图或文件存在自动通过。

CONCEPT_ONLY：独立角色立绘、灌木草丛、遗迹门框/台阶、药水使用专用特效、撤离成功专用特效。CREATED：草药、食用蘑菇、布料、卷轴、任务卷的模型/图标，当前无相应业务物品。NPC静态且物资猫复用仓库，无新商店；刚性部件+既有骨骼，翻滚程序化；历史出征/结算尚非全面uGUI重写。完整概念质感、比例与人工审美仍未完成，不能宣称所有B10美术要求已终验。

### 实际性能观测（非性能验收）

|用例|Unity实时到TitleReady|纹理运行内存bytes|材质对象|主线程采样均值|Draw均值/状态|GC|
|---|---|---|---|---|---|---|
|Case-new|3.772s|328297|85|0.203ms|0 (NOT_RUN)|NOT_RUN|
|Case-pending|3.485s|262761|580|0.216ms|0 (NOT_RUN)|NOT_RUN|
|Case-read|5.250s|43263093|585|9.927ms|1860 (PASS)|NOT_RUN|

上述是在返回标题前后的受控非活动桌面用例采样，含驱动/截图/资源卸载时序，不是进程完整启动成本、GPU显存峰值、森林帧预算或平衡完成。0 Draw为计数不可用NOT_RUN，不是优化通过；GC无有效计数NOT_RUN。

### 构建哈希

- `Build/Release/WanxiangGuitu.exe`：SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`，667136 bytes。
- `Build/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll`：SHA256 `aebce6a6157a3fe2e75a932a5d71ffb85a0b03f4807ef6377b1f8053670e0cb4`，475648 bytes。

用户ForestRuins SHA256 `ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4`；ProjectSettings SHA256 `7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451`，开工至终验一致，不进入提交。

### 正常AI的首轮结算样本

|策略|保留材料（皮/晶/核/木/石/矿）|保留新装备数|损失装备数|
|---|---|---|---|
|Gather|0,0,0,3,0,0|0|0|
|Treasure|6,9,0,6,0,3|3|0|
|Bypass|0,0,0,5,0,0|0|0|
|Land|10,5,2,7,0,0|2|0|
|Lake|11,6,2,8,0,0|3|0|

这些是Synthetic SettlementSummaries的首个Pending捕获，不能把该文件status=0写成已提交；实际Commit/ACK、入仓、取材制造与再次森林出征由21进程的后继轨迹/恢复断言核对。未拾取的地面物品不提前计入本表。

6个原始输入差异的字段摘要与品牌语义一致性见[审计](Evidence/FinalAudit/input-differences-summary.json)，产品名称只是UTF8/转义形式不同，CompanyName均DefaultCompany，用户源设置未改。
