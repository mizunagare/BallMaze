# 失败、工具问题与历史边界

不把后续PASS回写到首次失败文件；不将历史引擎问题关闭。完整原始日志、退出、语义行、命令和发布SHA见Evidence/manifest.json。

|尝试|真实结果/问题|处理与边界|
|---|---|---|
|B1Before|1 PASS/4 FAIL；缺新类型/定义/识别|实现前负例，保留before.json|
|B1Editor1|夹具未等技能面板Start，Sequence异常|等待真实UI创建，未造装备成功|
|B1Editor2|42 PASS/7 FAIL；准备末尾Focus屏障导致同帧请求拒绝|等待屏障结束，保留原49行|
|StorageEditor1 / DropEditor1|掉落复核误用原存档测试输出根，覆盖一份PASS汇总；原54行progress和SeedPackage仍在；掉落夹具又因未等Saves完整初始化而异常|明确承认目录污染；不把被覆盖汇总当最终证据。原失败仍在，存档在StorageEditor2/3新根、掉落在DropData2及Channel独立新根重跑。历史交付文件未改|
|MigrationEditor1|旧Time.time门槛在营地暂停下超时，exit1|新增标题/正常出征适配，复用原迁移规则；V1..V8随后实际执行。首轮合成目录另有snapshot记录；原日志不覆盖|
|CancelBefore1|5 PASS/1 FAIL：新动作取消后动画仍为Attack|仅新动作取消同步现有CancelAttack；CancelAfter1 6 PASS|
|pre-final-source-match.json|隔离副本漏同步镰刀小修复|拦截构建，保留mismatch；attempt2重新核对|
|new-run-pair-editor1.json|同材料两堆FindObjects枚举顺序不同，比较器误报|保留FAIL；按完整内容与数量多重集合严格比较，未改数据/容差，12项自测含丢失/重复/品质/词缀/随机流负例|
|NearPlayer1|首额外样本请求拒绝后读取空Aim导致异常|保留原数据；补就绪日志和空值保护，不改产品|
|NearPlayer2/3|首.35m样本无发射；其余样本通过；ready日志证明首角色在发射前已死亡|固定步进曾作用于训练重建等待。改为正常重建、立即暂停夹具AI、确认真实新角色健康后才固定步进。不复活/改HP、不降低命中断言。NearEditor4/Player4严格40项通过|
|StatsBeforeEditor1|18 PASS/8 FAIL：Frenzy/Reach、地波与牵引回响遗漏|仅新策略读取既有属性、统一新普攻时钟/触及和实际范围。StatsAfterEditor1 26 PASS；保留负例|
|LegacySavePlayerLatest4|实际exit1，旧CP6保存测试未初始化；候选档已写、newgame事务aborted，旧集合未替换|全新LSR4与LRR4复核通过，原失败/候选/事务保留。没有可靠错误来源回执，根因仍UNRESOLVED，不擅自修改新档事务。缺失SeedPackage还使随后的编排停止，未执行项由新根继续|
|工具只读审计初次命令|误用不存在的WeaponSkillCatalog.cs文件路径；真实类型在WeaponSkillExpansion.cs|工具错误，不归为产品缺陷；后续精确IL审计，不伪造原始文件证据|

旧B1～CP06-A、CP03/CP04、关闭失败、黑帧和引擎异常原始报告均保留。本轮部分Unity Editor日志再出现Editor.Search内部ArgumentOutOfRangeException、退出时JobTempAlloc/MemoryLeaks；没有因进程退出或稳定截图就关闭根因。原生U16、独立人工试玩、最终平衡和完整性能预算仍未执行。

迁移规则中既有强制死亡刺激只用于存档故障/保护规则测试，不当作武器命中或正常战斗证明。新武器和法杖专用命中均经真实物理与原伤害入口。

收尾额外保留：PlayerPerformanceLatest4的分配校准失败（零控制48B），因此Player性能NOT_RUN；功能37 PASS不能覆盖校准。DeliveryAudit首命令把合成数据目录当作进程输出目录而报缺少exit回执（工具exit1）；显式绑定8个数据/进程目录后45项通过，未改任何原回执。原终端错误存在会话，未伪造独立旧错误日志。
