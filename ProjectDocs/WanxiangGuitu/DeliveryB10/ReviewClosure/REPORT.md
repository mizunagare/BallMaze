# B10-R1：第一阶段P0复审准备与玩家体验缺口

日期2026-10-26。**第一阶段仍开放，未通过独立复审。** 本次是实施方的源码/证据核对与已确认文档缺陷修复，不能冒充ChatGPT独立审核、原生UI、人工试玩或新一轮游戏回归。

## 版本与修改范围

- 本轮开始远端main、本地HEAD均为`9560b5bb68636fd7783810a6dc4bdead8ed934a3`，没有后续远端提交。
- 上轮产品/构建冻结输入`6cad42d535347e0d96ede0e40f3d6a889a846bab`，更早开工`b474765dc9c28aaf7d2d267bc0362f828f1902b0`。冻结输入→交付9560之间没有Assets/Packages/ProjectSettings提交变化。109个产品C#在当前工作区LF归一化后与冻结输入一致；这不表示新执行了构建。
- 两份用户未提交文件仍保留：ForestRuins SHA256 `ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4`，ProjectSettings SHA256 `7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451`。审计核对实际字节且拒绝其被暂存，不覆盖或夹带。
- 本轮不改产品C#、场景、包、存档字段、引擎/依赖或编排系统；仅更正README普通Play说明、补P0台账/滚动计划和可复跑只读检查。没有新增经济/武器/地图，没有发输入、启动游戏、改用户程序或访问真实玩家档。

## 已确认且已修复的文档缺陷

玩家问题：README同时说“打开ForestRuins并Play从营地开始”和末段“普通Play先进入标题”，会使用户把正常标题入口误认为错误。

实际实现：`Assets/CombatPrototype/Editor/FantasySceneMenu.cs:19`在普通Play设置Boot为playModeStartScene；`GameEntry.cs`只给明确隔离的Editor验证路径授权直入。没有新产品缺陷证据，因此不改入口代码。

先运行Audit.py，README合同项真实FAIL/exit1（其余11PASS）；再更正文案为Boot→Title→玩家选择，并把历史B08/B09批次停止语句标注为历史摘要；相同检查12PASS/exit0。保留[修复前](Evidence/before.json)、[修复后](Evidence/after.json)和实际退出回执。该RESOLVED只针对文档，不能用来关闭P0-02原生验收。

## P0未完成项台账

状态OPEN/IN_PROGRESS/BLOCKED/RESOLVED/NOT_APPLICABLE表示任务；PASS/FAIL/NOT_RUN/UNRESOLVED表示验证，两套枚举分开。

|ID|任务状态|当前验证/依据|关闭需要的证据|
|---|---|---|---|
|P0-01 固定SHA独立复审|BLOCKED|指定审核对话最近10轮读取成功，但对应复审回复仅content-reference，`BLOCKED_SOURCE_UNREADABLE`；实施方12项自查不算独立审核|审核方针对9560完整可读结论/附件与具体问题；不得猜测占位正文|
|P0-02 正式Player原生操作|BLOCKED|本轮NOT_RUN；[新环境检查](Evidence/environment.json)只有用户console1，未发现独占测试会话/VM或已授权远程租约|获准独立交互会话/测试机，真实输入送达+UI/业务变化；完整标题/继续/读取/新游戏/设置/正常退出/恢复。后台WM_CLOSE/回调不代替|
|P0-03 独立人工理解/试玩|BLOCKED|NOT_RUN；没有本轮独立试玩人员、无提示观察和记录|独立玩家完成关键循环，记录误解/停顿/误操作与提示介入；四武器试玩属于后续矩阵，不伪造|
|P0-04 D3D12 UNKNOWN|OPEN|UNRESOLVED；旧InputSystemShutdown→UNKNOWN→CodeReloadManager顺序保留，exit0不能说明干净关闭。现有样本无新因果栈|同标题栏关闭路径的有效异常上下文/符号栈或最小因果复现；没有新线索不追加关闭实验、不试探生命周期|
|P0-05 Editor青色帧|OPEN|UNRESOLVED；旧渲染/捕获异常与SW_HIDE导致的独立Player黑图是不同事项。历史稳定帧不能证明青色帧原因|异常原帧及相同帧号的相机/targetTexture/clearFlags/材质/渲染器可见性/场景生命周期/捕获方式时序；有明确线索再最小诊断|
|P0-06 Editor.Search内部异常|OPEN|UNRESOLVED；核对完整样本栈，SearchDatabase.EnumerateAll→GetDefaultSearchDatabase→SearchInit.IndexationOnStartup→EditorApplication.delayCall，无产品帧。73条为上轮异常目录计数，不是本轮新异常数|独立最小导入/搜索索引复现和搜索功能影响检查，关联具体引擎路径；不能将编辑器索引异常判成Player崩溃或完全无害|
|P0-07 角色/场景表现|OPEN|本轮源码/旧证据审计，不是新运行或审美通过。137条中15技术VERIFIED/111INTEGRATED/5CREATED/6CONCEPT_ONLY，资源路径本轮存在性核对通过|受影响局部表现的动态机位、动作/遮挡与概念映射、正式Player及人工评价。不要把程序化首版称为概念质感全部完成|
|P0-08 性能验收|OPEN|真实性能基准NOT_RUN；旧受控菜单/背包计数受驱动/截图/非活动桌面影响，GC和零Draw不推断性能优秀|目标硬件/画质/分辨率/负载与时段、主/渲染/GPU线程、GC/内存/Draw/材料等有效采样及预算；详见后续规范|

结构化台账见[OPEN_ITEMS.json](OPEN_ITEMS.json)。没有自动关闭历史问题，第一阶段不要求强行解决所有引擎问题，但也不能自动认定满足独立审核退出条件。

## 异常证据与影响边界

Editor.Search完整异常块与源日志SHA在after.json的`Editor-Search-sample-call-chain`。异常之后同日志仍出现真实采集等业务记录，上轮流程完成的证据也存在；这只说明该样本没有立即阻断该流程，不能证明搜索/导入无影响。未调用Search API的产品代码不能凭此被定责；本轮不删除索引、清Library、禁日志或升级引擎。

UNKNOWN样本原路径/上下文/SHA在after.json，旧退出审计和转储/ProcDump校准仍引用[UI01调查](../../DeliveryUI01/CLOSE_INVESTIGATION.md)、[环境边界](../../DeliveryUI01/ENVIRONMENT_BOUNDARY_REPORT.md)。只重读旧证据，没有新启动/退出实验。取前三份日志不等于统计所有异常或新增因果证明。

青色帧复核：[逐帧路径、SHA与只读像素观测](Evidence/cyan-frame-observation.json)。本轮只读检查B09 Evidence中114张名称含b09-/camp/Camp且不在BeforeBlankCapture的历史PNG，没有发现单一RGB占98%以上的帧。这不是完整异常帧集合，不覆盖瞬时渲染，不证明根因已解决；不应据此改材质/相机/生命周期。现有稳定帧断言与黑图捕获修复均不代替上述时序数据。

## 角色和场景的实际缺口

主参考仍为用户黑猫概念板、STYLE_GUIDE v0.7。当前刚性猫部件绑定既有KayKit骨骼，翻滚程序化，NPC静态代理；没有完整软蒙皮/面尾新骨骼。营地/森林仍简化几何与表现延景，资源路径存在与技术导入不意味着材质/比例/叙事层次达到概念图。部分历史准备/结算仍OnGUI而非全量uGUI。6个概念项和5个仅资源项保留，不借本轮复审擅自实现新经济或全面翻修。

## 本轮结果与后续门槛

|层次|本轮结果|
|---|---|
|只读源码/证据合同|修复前11PASS/1FAIL；修复后12PASS，exit1→0|
|环境发现|实际执行，quser退出0；只发现用户会话，不能授予交互租约|
|产品规则/Editor正常AI/新进程恢复|NOT_RUN，本轮未改产品；不继承上轮PASS|
|非开发构建/Player/退出审计|NOT_RUN，本轮无新二进制或退出码|
|原生UI/人工试玩/真实性能基准|NOT_RUN；阻塞和缺失指标独立列明|
|UNKNOWN/青色帧/Search根因|UNRESOLVED，不以文档改成PASS|

上轮146PASS/2预期探针FAIL/3NOT_RUN/2UNRESOLVED、88构建警告、21正常AI、8发行标题和15受控Player步骤继续保留为**历史输入6cad的结果**；当前检查没有将它们加到12PASS。目录中的验收行与All汇总有不同统计粒度，不将73 Search异常再伪造为2个汇总项之一。

本轮没有存档格式/行为变化，v9及v1～v9兼容没有被新运行证明也没有被改写。未重建则新构建警告/性能均NOT_RUN。必要回归在出现可复现产品修复后，按影响范围使用既有隔离入口执行。

下一步：取得可读固定SHA复审；具备安全交互环境与独立试玩者后完成真实体验记录；仅有新线索才诊断历史引擎问题。阶段2的100seed/20通行/四武器矩阵已记入[计划](../../STAGE2_VALIDATION_SPEC.md)，没有开工。最终文档提交/推送不表示第一阶段退出或独立审核通过。
