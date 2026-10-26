# B10 失败与中间尝试（实施中）

不以最后PASS覆盖早期失败。原始运行均在工程外隔离目录，发布前需使用既有脱敏工具归档，不上传完整存档/缓存。

| 运行/尝试 | 实际结果 | 判断/后续 |
| --- | --- | --- |
| B10Before/20261026-095151-6e594ed6 | exit1，ForestRuins直接创建Session与HUD | P0实际入口回归暴露问题；后续Boot授权门禁修复 |
| ZIP首轮导入 | 文件名默认解码不匹配白名单，未写图 | 重解码文件名后原样复制9张；载荷与原包SHA保留 |
| 概念02/03 | 用户要求继续优化，非定稿 | 保留版本与提示词；04厚实材质后改为猫族方向 |
| B10CatBefore/20261026-120551-ac9a878f | exit1，测试超时 | 批处理跳过存档Start初始化，未实际执行猫族断言；属测试入口问题，不冒称产品回归已经触发 |
| B10CatBake/20261026-121122-dad268a4 | 3 PASS（准备/生成/渲染） | 猫族Prefab实际出现；不是整批验收 |
| B10CatUI1/20261026-122042-8c76c5d3 | 定向执行通过，图标人工检查发现暗头像 | 保留首轮图，后续摄影环境和专用图标shader修正，不把图标初稿标VERIFIED |
| B10CatUI2/20261026-122715-0630403d | 5 PASS（含七页面和B09动作受控检查） | 图片头像仍暗，继续修正；操作均受控非原生 |
| B10CatUI3/20261026-123457-b04e9a97 | 1 FAIL /3 PASS /1 NOT_RUN | 测试按重复按钮名选错材料行；实际交易有效但断言目标错误。加入稳定控件ID，保留失败，不归咎保存系统 |
| B10CatUI4/20261026-124219-93f8c7e0 | 5 PASS | 真实uGUI回调的主武器/旋转拖放、存取、制造、保存失败回滚重试、纯查询和新进程身份/来源账检查通过；仍非完整All/原生UI/人工理解 |

本表未列出的后续尝试须继续追加。尚未完成的最终All、发布构建、原生和人工项目不得据此标PASS。

| B10PlayerControl1 | 独立桌面名称被现有安全白名单拒绝，未启动Unity | 保留启动器错误；入口增加同一WGTest格式校验，不归咎游戏 |
| B10PlayerControl2 | read/new页面未渲染，exit3；pending退出0 | 非活动桌面18帧不足0.15秒；产品页切换改为事件刷新/旧回调拒绝，驱动加真实时间等待，保留失败 |
| B10PlayerControl3 | new/pending通过；read不变量失败，continue未运行 | 新发现测试夹具路径竞态：规则驱动在存档Start完成前换目录，生成的指定fixture仍为旧营地快照；修复等待初始化并断言实际写盘hasActiveRun。未放宽Player不变量 |
| B10CatUI5截图命名 | 规则Run共用默认隔离根，后续名为camp的截图实际为在途森林 | 保留原图并明确阶段；后续视觉驱动独立存档根，不将该图当营地证据 |

## 后续独立失败与修复，不继承通过

|运行|原始结果|处理与边界|
|---|---|---|
|B10FinalAll/20261026-135427-520bf6c7|141 PASS /3 FAIL /3 NOT_RUN /2 UNRESOLVED|2预期探针，1非预期B07ActorOcclusion；中间风格/混合输入，不是最终验收|
|B10FinalStyleAll/20261026-142010-4feb7543|140 PASS /4 FAIL /3 NOT_RUN /2 UNRESOLVED|2预期探针，另有遮挡与跑步截图断言；同时仍使用后来发现缺面的旧图标|
|B10AcceptedFinalAll/20261026-151656-538b2fe4|140 PASS /5 FAIL /3 NOT_RUN /2 UNRESOLVED|名字不代表验收。2预期探针，非预期B05拾取、B07遮挡、B08营地E；各自保留，不能因正常AI21进程与构建成功忽略|
|B10IconProbe2|MissingComponent CanvasRenderer真实失败|ItemGraphic添加必要CanvasRenderer，保留首次图标暗/空白图|
|B10IconAlphaBefore|portrait/hero/potion/sword四项alpha覆盖失败|显式更新已持久Mesh顶点/法线/索引/包围盒并UploadMeshData，保留GUID。CopySerialized热更新路径产生碎片，未称Unity引擎根因已定位|
|B10IconUploadFix|烘焙与alpha42通过，但动作截图FAIL|保留失败；视觉测试从Editor回调位移改为游戏帧的真实CC移动；净空、实际速度和Run状态断言保持|
|B10FinalMotionGate|B09Visual/B10Comparison与准备3 PASS|不替代全量All；动作、伤害、翻滚与死亡由真实逻辑驱动，敌人关闭仅限受控截图|
|B10RemainingRegressionGates/20261026-153522-fce53f58|3 PASS|旧遮挡测试在LateUpdate绑定前采集旧骨架Renderer，日志证实这些Renderer后来enabled=false；改为绑定后采集当前可见Mesh，Fade/恢复/HP/碰撞/RNG断言不降。B05显式同步物理并选择实际净空近点，真实PickUp和来源账仍须通过；原偶发失败的唯一根因未证明|
|B08CampPause旧驱动|在固定一秒内每Editor update移动.005，位移量依机器负载不确定，并未等初始存档完成|新增等待初始化、限定本次测量总移动.2m并记录E目标/教程阶段；冷却冻结、实际移动、真实交互断言保留。后续独立结果另记|
|ExactBefore Cast|旧版近战模型不可见，保留原图及失败|不伪造一个通过的before。新的清晰取景驱动检查实际LOS与冠层包围盒，不改变生命或物品|

最新用户概念覆盖简化03方向；此前的通过仅属于对应输入，不延伸为新风格通过。新B10-R1材质、图标和正式构建均需要重新运行。

B10R1FinalArtGate首次B08修订在batchmode等待Saves.IsInitialized，但现有CombatSaveSystem.Start明确在batchmode跳过；这是新测试修订的入口错误，会在自身120秒上限失败，不强杀或更改运行中副本。源测试改为只在非batchmode等Start，batchmode继续用原显式隔离初始化。失败另存，不归咎游戏。

B10R1EntryFinalGate：B08营地E/冷却、B10多分辨率与真实动作、规则/新进程恢复、五类敌人取景共6 PASS。照片检查仍发现标题Hero脸部被前景树冠遮挡；这不是业务断言通过即可忽略的美术问题。已记录原图，标题专用树木改为营地清场外的远景，加入四分辨率镜头到脸部遮挡断言。不会移动游戏森林的树、碰撞或导航。

B10R1FullAll/20261026-191956-921964b9启动于799bd556，随后因上述真实取景问题修改了产品ScenePresentation和比较驱动；该轮保留为中间尝试，即使规则通过，也不能作为最终同源构建与整批验收。最终必须在产品冻结后另开新All，不能由定向通过替代。

B10R1FullAll中间轮已结束：{'PASS': 127, 'FAIL': 4, 'NOT_RUN': 19, 'UNRESOLVED': 2}；失败步骤[{'name': 'probe.nonzero', 'exit': 7, 'timeout': False}, {'name': 'probe.timeout', 'exit': None, 'timeout': True}, {'name': 'WGDeliveryACheck.Run', 'exit': 1, 'timeout': False}, {'name': 'normal-ai.Bypass.FinalResume', 'exit': 1, 'timeout': False}]。Bypass.FinalResume的Unity启动停在Successfully changed project path，未进入游戏恢复断言；超时保留PID30340（记录时仍响应，CPU低），没有强杀、没有根因归因或重分类正常退出。独立最终FrozenAll同阶段已通过，不继承本中间轮结果；旧轮后续跳过/失败逐项保留。

中间FullAll的WGDeliveryACheck失败具体记录：请求seed1440702505，测试主动注入前两次Build失败；第三候选seed+2实际Nav校验报“资源互动不可达：node:24”，产品按原规则成功采用seed1备用布局。测试同时要求generationAttempt==2且非fallback，因此exit1。这一fixture未固定自然生成前提，故障注入与真实候选失败叠加；未通过改地图/扩常数/删除物品使其通过，也未改断言。最终FrozenAll在另一自动生成种子下同项PASS，**不代表原seed第三候选被修复**；原失败与完整日志继续保留，随机夹具脆弱性作为已知限制。

中间Bypass.FinalResume外层exit1、timedOut=false；内层明确打印“Timed-out isolated Editor still active”，校验抛“Normal AI process/guard validation failed”。区分外层字段与内层超时，不把其写成exit0或完成恢复。原始进程仍保留；启动挂起根因UNRESOLVED，不猜测GPU、存档损坏或游戏生命周期。

## 退出码未暴露的真实UI错误（必须修复，不认定冻结轮通过）

B10R1FrozenAll/20261026-192415-aa0d1bf5按进程计144 PASS/2预期FAIL/3 NOT_RUN/2 UNRESOLVED、21正常AI、8标题和独立验证Player15 PASS，但独立日志审计发现622异常起始行：73来自Editor.Search，另549全部为**CatInventoryPresenter.LateUpdate第15行的产品空引用**（药水547、双武器2）。因此该轮不能以exit0或0非预期进程FAIL认定通过。新日志门禁对该原始目录实际返回FAIL、549 findings，不移除日志。

根因：旧规则夹具使用无Profile的LegacyHarness并打开背包，新增UI的刷新键直接读取s.Flow.Profile.pending.Length。修复是在数据未就绪时显示明确原因和返回入口、禁用数据操作、不创建Profile或改物品；真正完成InitializeStorage后恢复原正常页面。不是catch异常或隐藏错误日志。

B10InventoryReadiness.Run先在旧产品执行：B10R1ReadinessBefore/20261026-202117-c10e49ab exit1，捕获真实空引用。后续B10R1ReadinessAfter独立副本的同一测试、原药水、原双武器规则已通过；其余规则和最终新All另外记录，不继承前一轮PASS。

编排器末尾新增轻量B10.runtime-log-gate，扫描实际规则、正常AI、构建、正式标题和受控Player日志中带产品源码栈的NullReference/MissingReference/MissingComponent；不吞日志、不改已有测试语义，不把未覆盖的其他异常推导为“全部干净”。完整异常目录仍保留，Editor.Search不被直接归咎游戏。

资产目录后处理脚本新增逐项SHA时曾出现缩进错误（Build-AssetInventory.py第53行），当次没有覆盖旧目录数据；已修正并实际重跑成功，当前137条/276文件。该工具错误不计作游戏运行PASS，也不更改旧失败。

最终6cad新All实际结束：146 PASS/2预期探针FAIL/3 NOT_RUN/2 UNRESOLVED；0非预期命令失败，新增门禁117日志0引用错误。原549次UI空引用已关闭；73 Editor.Search内部索引异常未定位。当前结果不改此前过程失败、随机fixture候选失败或启动挂起，也不关闭原生/人工与D3D12/青色帧事项。

最终结算样本表的临时报表命令首轮因f-string括号语法错误返回非零，未写入文件；已纠正重跑，不计作游戏验证失败或PASS，未修改原始结算数据。

提交证据校验首轮FAIL：42份已脱敏B4诊断.log受Git忽略规则影响未暂存，0字节不匹配、0受保护文件被暂存。保留staged-byte-check-before-log-add.json；仅补入这42份既有脱敏诊断后重新核对，不重新运行或改写原始日志。

## 第一阶段P0复核：入口文档矛盾

9560输入的README仍写打开ForestRuins并Play直接从营地开始，与FantasySceneMenu.cs:19及文末Boot入口说明冲突。新只读Audit.py先11PASS/1FAIL、exit1；只更正文档和历史批次提示后同脚本12PASS、exit0。见ReviewClosure/Evidence/before.json、after.json及退出回执；不是产品故障修复或新一轮游戏回归。P0独立审核、原生/人工及引擎根因仍开放，旧失败与All计数不改。
