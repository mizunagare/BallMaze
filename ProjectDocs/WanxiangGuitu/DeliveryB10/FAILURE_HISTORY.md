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
