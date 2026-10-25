# B09 验收对照

只认All5独立运行：`B09DisplayVerified/20261026-001243-cd1430ec`，输入`6ec68a88bc171af1c7e5926642b17899ab20f8ec`。实现交付待复审，原生/人工与既有根因仍开放。下表按需求拆分，不与编排138/2/7/2相加计数。

| 要求 | 状态 | 实际范围/证据 |
| --- | --- | --- |
| 正式Player默认主菜单、五入口、没有旧HUD/Session抢先初始化 | PASS | 6个非开发Title状态；真实截图+title-ready/rendered/quit审计；非原生点击 |
| 缺失、有效、损坏、不兼容、Pending、Committed按钮状态 | PASS | FinalAll/B09Diagnostics/B09-Title-*，PNG实际复核 |
| Backup、旧版本、未确定tmp、冲突与阻断分类 | PASS | B09Rules与A1规则；这些额外类别未逐一拍最终Player图 |
| 新游戏二次确认/取消不写档/重复请求锁 | PASS | B09Visual真实uGUI回调与GameEntry门禁；不是键鼠 |
| 候选写入失败/归档故障/发布后回调核对 | PASS | B09Rules.Run，完整集合不混入新Profile |
| 中断后新进程恢复、重复恢复 | PASS | B09Rules.Interrupt/Recover；受控中断边界，不是断电/强杀 |
| 单一自动档真实列表，读取前目标变化拒绝 | PASS | SaveCatalog+B09Visual；无虚构槽位，失效快照不偷偷读新目标 |
| Continue/读取同Profile、Run、布局、随机流、ID、来源账、教程 | PASS | Entry三进程检查点+2个受控Player继续；菜单按钮原生路径未运行 |
| v1～v9兼容、旧在途、分页与结算唯一性 | PASS | B05Legacy/V7、B06V8、LegacyForest、B07/B08/B09规则；默认值/保护链保留 |
| B1费用/回执、B2目标、B3随机流、B4导航与评分 | PASS | 本轮全规则与Gather/Treasure/Bypass三组正常AI |
| 双Boss/徽章/首次与重复奖励、双武器/冷却/仓库/制造/教程 | PASS | 本轮既有规则＋Land/Lake/Tutorial/Entry正常NPC AI |
| 实际初始骨骼与剪辑审计、资源许可 | PASS | 6 Skinned、246骨骼引用、Legacy曲线全部解析；现有KayKit CC0，无新下载 |
| Idle/Walk/Run/Attack/Hit/Death基本动作 | PASS | B09Visual实际采样、真实位移/伤害驱动夹具；无Animator/Avatar完整重定向声明 |
| Dodge动作 | PASS | 原HeroDodge驱动程序化翻滚，不是骨骼翻滚剪辑 |
| 武器动作映射与原战斗窗口/命中、翻滚无敌帧 | PASS | 源码映射＋四武器/战斗/冷却回归；动画不决定伤害 |
| 营地/暂停时钟、死亡视觉不阻断结果与复活 | PASS | B08CampPause、B09Visual死亡0.2秒及完成后图/确认回营；保存错误优先 |
| 无滑步/足锁定及所有视角四武器手感 | NOT_RUN | 无脚掌IK；未用静态图代替人工/原生动态验收 |
| 营地与森林延景、当前镜头无独立平台拼接 | PASS | B08稳定基线与B09实际营地/森林图；表现层无碰撞，不扩大可走范围 |
| 导航、资源、出口、Boss/旧布局不受装饰影响 | PASS | 本轮B4/R1与正常AI；未改地形revision/旧存档数据 |
| 任意相机下环境/标记无遮挡 | NOT_RUN | 入口标记有头盔局部投影重叠；不宣称全视角已验收 |
| 菜单4分辨率、HUD缩放/旧UI组合不越界 | PASS | B09 12张菜单页及Bounds断言；原UI92图/B08夹具。OS DPI和原生点击不在此PASS内 |
| 实际设置及集合外持久化 | PASS | B09Preferences；音量/灵敏度/HUD/窗口分辨率；没有按键重绑定假选项 |
| 非开发Windows构建与测试驱动剔除 | PASS | BuildReport 0错误87警告，元数据/哈希；不是原生UI证明 |
| 正式启动根安全保护 | PASS | 纯解析6负例＋API门禁；2个相对根Player自动exit2；不启动缺根负向Player |
| 正向Player关闭/保存/新进程恢复 | PASS | Title6及gameplay2均exit0无超时；WM_CLOSE不是标题栏鼠标 |
| 完整All与失败传播/隔离 | PASS | 协调exit0、0非预期FAIL，2预期探针FAIL原样保留，无挂起进程 |
| 用户场景/ProjectSettings保护、未提交内容不夹带 | PASS | user-input-proof及staged-byte-proof；源文件原SHA256不变 |
| 源码与测试/运行输入可追溯 | PASS | 94产品C#、70注入规则、63正常驱动来源与831构建输入逐一哈希；6项副本差异不隐藏 |
| 干净Git场景/设置完全相同构建验证 | NOT_RUN | 当前测试副本含受保护用户场景，不能声称clean-clone一致 |
| 原生U16/B09按钮与标题栏键鼠 | NOT_RUN | 未激活测试桌面有渲染不等于有安全原生输入环境 |
| 人工可理解性与试玩 | NOT_RUN | 没有独立人员；不拿截图/Editor bot代替 |
| D3D12 UNKNOWN根因 | UNRESOLVED | 旧证据保持，不用D3D11/后台WM_CLOSE通过替代 |
| Editor青色帧根因 | UNRESOLVED | 稳定帧与SW_HIDE捕获修正均不是该根因证明 |

[完整结果](Evidence/FinalAll/results.json) · [证据索引](Evidence/INDEX.md) · [失败历史](FAILURE_HISTORY.md)。本轮没有多槽系统，槽位独立/删除/覆盖验收不适用，不标作已实现PASS。
