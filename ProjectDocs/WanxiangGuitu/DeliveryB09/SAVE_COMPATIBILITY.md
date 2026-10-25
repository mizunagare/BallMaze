# B09 存档模型与失败处理

## 现状

当前仍为一个 v9 自动保存封装：主档 save.json、备份 save.json.bak、ground-loot 分页、迁移与恢复档案。ProfileState、RunState、SettlementRecord 共处一个完整封装，沿用修订号、校验和与原子写入。没有新增槽位索引，没有改变存档版本。v1～v9 继续由原 ReadChecked/LoadProgress 迁移与恢复。

默认 Company Name 不变，旧位置为 DefaultCompany/BallMaze/ForestRuins，新位置为 DefaultCompany/万象归途/ForestRuins。测试严格使用启动参数指定的隔离根：Legacy/ForestRuins 与 WanxiangGuitu/ForestRuins。本轮不读取真实目录。

## 状态边界

- 营地：Profile 与营地检查点，不创建 Run。
- 在途/引导：恢复同一 Run、区域、seed、布局、随机流、来源账及教程。
- Pending：继续原待确认结算，不提前提交。
- Committed 未 acknowledged：恢复已保存结果，仍由原回营确认入口处理。
- 损坏且无有效备份：不可继续，保留原文件。
- 不支持的版本：不可继续，不回退成空档。
- 有效备份：可恢复完整备份；目录与页由原保存器校验。
- 未发布 tmp：明确标出不确定写入，只允许读取最后有效修订。
- 新旧目录都有集合：必须明确选择；不合并，复用 A1 选择回执。

## 新游戏事务（不是 Restart 的别名）

明确确认全部重置后，对当前和旧目录重新计算指纹；进入场景前复核。以独占 entry.lock 防并发，候选保存到同级 GUID staging；使用原保存器写完整候选，校验 v9、独立 Profile ID、无 Run/结算。先写并落盘事务 journal，原集合整体移动到 GUID archive，再发布 staging，核对实际 Profile ID 与完整集合指纹，最后记录 committed。

发布前失败不替换旧集合；原集合已经归档但未发布时，只有指纹匹配且目标不存在才原样恢复。已经发布但回调失败时，先核对实际新集合；不盲目回滚或再次创建。状态不明则保留候选、归档与 journal，阻止自动覆盖。归档包含备份和所有分页，不只复制 save.json。旧位置保持；明确新游戏时为新集合建立原迁移器选择回执。设置在集合外，保留。

新档不混入旧仓库/配方/徽章/教程；旧档归档可离线恢复，但本轮没有伪造“档案槽”浏览或一键恢复归档 UI。失败时不会将候选内存进度自动写回旧位置。

## 合成验证

测试新游戏 staging/归档/发布故障、发布后回调故障、进程边界恢复、读取失效快照、状态分类、集合指纹与旧版本回归。全部使用工程外唯一根。Editor-only 的 EntryInterruption 是受控事务边界试件，非崩溃/强杀；正式程序集剔除。日志和断言与真实 Player 背景关闭/恢复分开记录。
