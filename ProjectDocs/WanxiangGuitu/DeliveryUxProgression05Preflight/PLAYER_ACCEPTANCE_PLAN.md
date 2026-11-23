# UX-05 Player 验收任务书

**[D] NOT_RUN。** 负责人已裁决，D-19、D-20、D-23 均为 A／APPROVED。本文件规定获独立授权后的执行与取证。实施入口见 [任务书](IMPLEMENTATION_TASKBOOK.md)。

## 每项共用规则

- 每个用例及输入变体使用 Run ID `UX05-{build12}-{UTCbatch}-{case}-{variant}-{attempt}-{phase}`。phase 用 INIT/WRITE/KILL/REOPEN/P1/P2 等明确阶段，另记 parentRunId。重试使用新 attempt。REOPEN 与父运行共用专属根，独立克隆复验另开根。MULTI 使用同根双 PID、独立 Run ID 和共同 pairId。
- 全部输入使用合成夹具或获批脱敏冻结副本，只以显式 `-wanxiang-storage-root` 启动。保存根解析、只读源的 SHA-256/mtime、目标初始指纹和保护清单。操作系统路径审计核对无生产目录 I/O。故障观察点和真实操作分别记录，通过真实输入触发玩法。不得通过设 HP、成功标志或奖励直接完成。
- 所有行的 **F** 包含主、滚动备、可达分页、归档、临时文件、关联文件和必要事务状态的相对路径、存在性、长度、SHA-256、mtime。另记录原始源保护指纹、外壳版本与 revision、payload checksum 和原字节哈希、规范语义差分、profile/run/checkpoint/settlement 键及奖励 ID。在注入前后、进程退出与重开后保留。只读场景从动作窗口排除或明确分离正常 autosave。
- 每个 Run 目录必须有 `manifest.json`（commit/tree、buildId、Unity/backend、DLL/EXE/驱动 SHA、驱动源码和编译参数、命令、PID、退出码、根和输入标识）、`fingerprints.json`（F）、`input.jsonl`、`events.jsonl`、`player.log`、`result.json`，以及下表的专项文件。按 Run ID 汇总原始文件的路径、哈希、长度和结果。未经运行标 NOT_RUN。失败的原始文件保留，后续新 Run 记录替代关系。人工体验单列。
- 跨重启历史需求已确认。Schema 和历史专项须待最小变更与隔离 Player 授权后执行。MIGRATE 的零迁移变体为未获迁移授权或只读路径的控制组。DEFAULT/REOPEN 另验证现行 v9 对照。保留所有通用回归。验收失败时停止放行，保全可恢复世代。

## 用例与断言

| case（进入 Run ID） | 输入及操作 | 原始指纹 | 预期结果 | 失败条件 | 专项证据文件 | 保护范围 |
|---|---|---|---|---|---|---|
| V9READ | 原始 v9 营地、在途、Pending、已提交未确认/已确认；有页/无页 | F + 源版本、四个快照路径、装备/技能/来源/随机流 | 读入正确来源与原业务状态；只读浏览及首次加载证据分开 | 隐式升级、错误降级、字段丢失或误发奖 | readback.json | 原版 v9、v6 验证链、主备与技能状态 |
| DEFAULT | 缺候选字段的合法 v9；合法校验但目标版字段缺失或非法 | F + 字段存在图及 plan 镜像 | 旧源显式默认无记录或空且覆盖未知；非法目标拒绝 | 伪造达成、目标静默补坏字段或旧档拒读 | defaults.json | 保留原字段和值、旧 Pending |
| MIGRATE | 有效 v9 各状态及完整主备页；同一请求发两次；零 Schema 独立变体 | F + 归档清单、父/目标、发布次数、允许字段差分 | D-19 直达唯一目标，目标世代只发布一次；零 Schema 路线仍为 v9 且无迁移写 | 有中间版、第二次发布、原始归档不全、语义越界或计奖 | migration.json | 全部旧业务字段、几何、随机、原档 |
| REOPEN | 两次关闭后以新 PID 重开同一隔离根，再从已冻结副本重开；另测正常 autosave | F + PID、锁生命周期、目标发布及确认次数 | 同版读取和再次请求无迁移写；正常保存按原约定另增 revision | 回执/备份重复、重开重迁、串根或遗留锁 | reopen.json | 父/子世代与已提交记录 |
| SETTLE | 旧/新 Pending 与 Committed、确认回营、同键重放；达成、失败、证据不足 | F + run/settlement 键、plan、奖励和记录集合 | 旧计划不补历史；新获批记录与奖励同次生效，重试和确认不重复 | 放奖与回执分离、重复或历史裁剪后可重放 | settlement.json | 旧结算、库存、教程、奖励 |
| CUT | 归档前后、页和主档半写、Flush 后、替换前后及确认前后杀进程 | F + 故障点前后原始快照和未决事务 | 匹配父可重试，匹配子只补确认，未知冻结 | 提升 tmp、损坏主备、丢页、重复奖励或人工未知被自动续写 | fault.json | 唯一好档、历史归档、页与事务 |
| REPLACE | 模拟原子替换明确失败和完成后抛错；父指纹在发布前变化 | F + 原始异常、系统返回及磁盘父子指纹 | 分别确认未发、已发或拒绝过期父；只以实际磁盘判定 | 布尔值直接决定重写，跨卷复制假装原子，旧父覆盖新世代 | fault.json | 原子性、父代、备份 |
| BAD | 截断 JSON、payload 与 checksum 不符、重新加校验但非法结构、未来版、缺页或页篡改 | F + 损坏部位、哈希、诊断码 | 分别诊断语法、校验、不兼容、结构、缺页；按恢复规则拒绝破坏性写入 | 自动初始化、静默降版或接受不完整页面 | diagnosis.json | 源/备证据、未知版、引用闭包 |
| BAK | 主坏备好、主好备旧、双坏、仅 tmp、完整归档和缺页归档各一；归档同名不同指纹 | F + 归档与还原逐文件对照、恢复来源 | 原版在克隆中加载完整可验证集合；保留唯一好备，坏集冻结；归档不可覆盖 | 混页、覆盖备份、未披露数据缺失或拿 tmp 恢复 | recovery.json | 原档、全部关联文件、版本及事务 |
| MULTI | 同专用根 P1 持锁，P2 争用；P1 强杀后重开；失效父和旧版尝试共根 | F + 两 PID、pairId、锁与父 generation | 仅一写者，旧父失配，旧版使用独立根并不能打开新世代写入 | 双写、旧父覆盖、未释放锁或凭时间戳抢锁 | concurrency.json | 所有写入口及代际隔离 |
| DOWN | 原版 v9 对目标版隔离副本；从迁前归档另克隆还原 | F + 新旧集合及还原时差 | 旧端不得静默回退覆盖；旧快照可开启且报告快照后进度损失 | 编辑版本伪造兼容、覆盖新集合或称无损降级 | recovery.json | 新旧完整集合 |
| UX03 | 剑/矛/杖/弓/双刃/大剑/镰刀，各走普攻和 1/2 两技能的真实释放 | F + 输入、蓄力/释放/命中时间、冷却、AP 位模式 | 七武器逐一满足 UX-03 合同，窗口取实际运行值 | 漏武器/技能、伤害/节拍变化或以面板代替实际输入 | combat.json | 武器、技能机制、时间窗、D-24 |
| P1C | 森林、遗迹、洞窟各进区→目标交互→挑战/战斗→撤离→结算→重启；失败反例 | F + 地区/目标/实体键、事件链、结局及奖励 | 符合三地区原挑战合同，可回读，失败不伪造目标成功 | 跳过真实触发、奖励循环或任一地区缺证据 | regions-loop.json | 地图条件、挑战、奖励、随机 |
| B1 | 金红各尝试分解与正常入库；白绿紫正对照；覆盖 uGUI/IMGUI | F + 装备 ID、资源增量、存档/随机变化 | 金红拒绝且仍能入库；白绿紫按既有返还 | 误分解、伤及入库、资源或 ID 异常 | inventory.json | B1 权威门禁和经济 |
| B2 | 双 UI 收藏/过滤/排序与 Add/Replace 六场景，取消、容量不足和失效后提交；重启收藏 | F + 九域、装备 ID、AP、RNG、保存事件 | 预览纯读，合法提交与预测一致，无猜替换 ID；收藏同进程保留、新进程清空 | 预览写盘、错误移除、收藏被持久化或排序改存储 | inventory.json | B2 收藏、替换、装备和 D-24 |
| SKILL | 选择当局槽后结束，原进程新出发及冷进程后新出发；旧/新武器各组 | F + 实际 1/2 输入、选择状态和字段差分 | D-20 每局默认且合同相同；无新增索引、每武器配置或临时数值字段 | 跨局恢复选择、写新字段或技能行为漂移 | skill-defaults.json | 既有 skills/offers/weaponSkillCooldown 语义 |
| REGION | 三地区已有/未知指标及多次往返展示；同种子配对对照含第五次撤离检查 | F + 指标来源、前后资源、经济/进度变化 | D-23 按现有 ProfileState 投影，缺项 DATA_GAP；不开写入和奖励路径 | 自造零值、地区字段、永久攻防、掉落/材料、配方或任何隐性收益 | region-projection.json | 只读、原经济、战斗、解锁及掉落 |
| ISOLATE | 允许的合成/脱敏副本；未指定根、非法根、重解析点与尝试越界的负例 | F + 根解析、允许路径、受保护原始夹具 SHA/mtime | 仅在明确隔离根运行；拒绝非法路径且无生产目录 I/O | 回退真实路径、原始夹具或保护文件变化 | isolation.json | 真实存档、历史证据与项目保护范围 |

P1C 闭环口径见 [历史验收](../DeliveryUxProgression01P1C/ACCEPTANCE.md)，UX-03 七武器与窗口按 [既有合同](../DeliveryUxProgression03/IMPLEMENTATION_SPEC.md)，B1/B2 历史基线见 [集成审计](B2_INTEGRATION_AUDIT.md)。迁移与恢复的父/子判据见 [备份恢复](BACKUP_RECOVERY.md)。历史证据仅作为对照输入。

## 跨重启目标历史专项

**NOT_RUN。** 使用上文 F 和通用证据要求，每行按 OH 编号和变体生成唯一测试 Run ID，另记录产品局 runId、profileId、settlementId。所有用例各有专属隔离根，跨进程子运行在明确指定的同一根重开并使用不同测试 Run ID。OH08、OH10 每个注入点用独立夹具和根。全程对照历史、奖励、库存、committedRuns、页引用及读写事件。

| case | 操作与输入 | 预期与失败条件 | 专项证据 |
|---|---|---|---|
| OH01 | 用真实输入完成目录目标并撤离，再提交；打开历史并独立领取已有待领项 | Pending 隐藏。Committed 后同局只一条，七项展示字段匹配。领取不改条目。提前显示、漏记、错误身份或新增奖励均失败 | objective-events.jsonl、history-diff.json、reward-diff.json |
| OH02 | 条件满足后死亡、放弃或结算保存失败；另测证据不足及无目录目标的波次挑战 | 非合格结局与未发布的提交均不显示成功。明确保存失败后可按原计划重试，只有提交成功才显示。虚假成功、提前奖励或重算均失败 | objective-events.jsonl、fault.json、history-diff.json |
| OH03 | 同一终局连续提交、读回后再提交、确认回营及领取；同卡另开一局完成 | 相同 RunId + SettlementId + ObjectiveId 只出现一次且既有奖励一次。不同 RunId 的同目标各有一项。重放、重复发奖或按卡片而非局去重均失败 | replay.json、reward-diff.json |
| OH04 | 成功提交并退出，冷进程以同一根继续 | 时间与身份不变，结果仍可查，打开页面无额外写入。仅缓存可见或跨进程重记失败 | reopen.json、history-view.json |
| OH05 | 多次出征，含成功、不满足条件及失败，再回营翻页 | 最近结算被替换后仍可查先前已提交项。无失败项，筛选翻页无写入。历史被清空或变成当局回执失败 | campaign-runs.json、history-view.json |
| OH06 | 森林、遗迹、洞窟混合，含同时间、首领、机关链、通用挑战及空筛选 | 地区/类型组合、首领／特殊分类、既定降序和分页稳定。未知与空分离，森林通用挑战不冒充首领击杀。漏项、重复分页或显示未完成失败 | query-cases.json、history-view.json |
| OH07 | 隔离近满夹具，真实提交第 128、129 项，回拨时钟另测并重放被淘汰局 | 只淘汰最早已提交项，最多 128 条，排序可重复，committedRuns 不裁剪，奖励和旧键不可重放。越界、时钟倒退改留存或过大封套被错误发布均失败 | retention.json、envelope-size.json、replay.json |
| OH08 | v9 含页和相关事务，分别在归档、暂存、原子替换和确认边界中断 | 重开选择完整父或子，已发只补确认，未知冻写。零倒填、零重复迁移和奖励。丢页、提升 tmp、覆盖唯一好备失败 | migration-fault.json、archive-manifest.json |
| OH09 | 原始 v9 营地、在途、Pending、Committed 夹具读及明确迁移 | 原始 v9 可读，迁移默认显式空和旧未知，旧业务不变。旧历史伪造或兼容失败 | v9-read.json、schema-diff.json |
| OH10 | 比对新 Pending 固定候选、提交前失败、已发布未确认与旧 Pending 迁入 | 恢复 Pending 不展示候选且固定身份、UTC 和显示快照，随后成功提交一次。恢复 Committed 同项同时间；旧计划不重算。漏记、重复或奖励变化失败 | recovery.json、objective-events.jsonl、reward-diff.json |
| OH11 | 两次新进程读已迁 v10 档，重复相同升级请求；正常 autosave 单列 | 不二次发布、不多一份备份或条目，指纹无非预期变化。升级标记、revision 或记录重复即失败 | reopen.json、generation-diff.json |
| OH12 | 模拟完整用户存档集合的获准脱敏夹具，封存新版后从迁前全量归档克隆到独立旧根 | 原版能加载主备、页、关联文件和必要事务，哈希逐项匹配，告知快照后的进度损失。缺页、改真实存档、覆盖新版或混世代失败 | archive-manifest.json、restore-compare.json、v9-read.json |
| OH13 | 用 127 条已提交夹具，通过实际目标结算写第 128 条。另读有 129 条的非法 v10 夹具 | 合法序列保留原 127 条和新增项。非法目标档被拒绝且不静默裁剪。任何误删均失败 | retention.json、schema-diff.json |
| OH14 | 以 128 条启动，真实完成第 129 条，制造与最早提交不同的最早 UTC。分别在替换前和已发布未确认点中断 | 替换前无删除，确认后仅最早提交项淘汰。UTC、回拨、筛选及重放不得影响被淘汰项。除合法新局的正常结算差分，其他累计数据逐项相同 | generation-diff.json、retention.json、protected-counters.json |
| OH15 | 完全相同三元键重复提交。同一 ObjectiveId 换合法 Run 和终局重做。对相同 Run 注入不同 ObjectiveId 与实际卡片冲突的验证夹具 | 相同键只一项。同目标跨 Run 各一项。不同目标的键可区分，但相同 Run 不得绕过单卡片与结算合同。非法候选不得发布或发奖 | identity-cases.json、objective-events.jsonl、reward-diff.json |
| OH16 | 多页历史包含同 CompletedAtUtc、不同 CommittedAtUtc、双时间相同与时钟回拨。反复筛选、冷启和翻页 | 按两个 UTC 降序、三元键 ordinal 升序。跨页稳定，持久提交位置及指纹不变。第二排序键为冻结的计划时间 | query-cases.json、history-view.json |
| OH17 | 用含历史快照的 v10 夹具，跨两个批准的目录变体读取，替换当前目标显示名称并测试旧 ID 退役 | 旧记录显示完成时名称，分类按稳定 ID 兼容映射。退役条目仍可分类，未知合法 ID 分类不猜补。新完成的同 ID 采用新名称。重开不回填、改写或合并旧记录 | catalog-variants.json、history-view.json、history-diff.json |
| OH18 | 提交、回放、领取及重放领取；将历史条目裁剪后重放原终局，同时保留地区缺口 | 历史与结算及领取各走自己的判定。裁剪不删 committedRuns、领取键或地区累计。显示历史不补 DATA_GAP。任何复领、误记或额外写入均失败 | replay.json、reward-diff.json、protected-counters.json |
| OH19 | 相同达成时刻的候选延迟确认，首个 Pending 前后、计划就绪后、首次提交失败后和重新启动分别取证 | 达成时采 CompletedAtUtc。首个 Pending 保存前计划形成时采 CommittedAtUtc。两者对同一候选只采一次，延迟、失败或重启不改值。savedAtUtc 与文件时间无参与。与 OH10 共享恢复夹具、独立时间断言 | clock-samples.json、pending-fingerprint.json |
| OH20 | 第 129 条已确认且旧记录已裁剪、最近 SettlementRecord 又被替换后，分别从现行世代、旧父计划和隔离旧备尝试重放旧终局 | 现行世代由 committedRuns 拒绝该旧 Run，过期计划无法发布，隔离旧备不会反向合并现行状态。无复发奖励或历史。与 OH07/OH18 共享重放场景，独立覆盖最近结算已被替换及旧父代闸门 | stale-generation.json、replay.json、reward-diff.json |

### 专项覆盖与计数

- OH13 验证第 128 条和非法超限。OH14 验证第 129 条、最旧提交裁剪和失败不提前裁剪。OH18 对照奖励、徽章、击杀、材料和已结算集合。
- OH03/OH15 验证同 Run 同目标重试、同 Run 不同目标冲突、不同 Run 同目标分别记录。OH07/OH18 既有裁剪后旧结算重试保留，OH20 只新增替换最近结算和过期世代的断言。
- OH04 已覆盖 Committed 跨进程读。OH10 已覆盖 Pending 恢复，按事务模型逐中断点拆变体。OH19 专门核对双时间采样与冻结。OH16 覆盖相同完成时间、相同提交时间及稳定键排序。OH17 保留改名与退役。
- 报告仅按 OH01–OH20 唯一用例 ID 计数。共享 Run、重复断言和补充变体引用同一原始证据，不作为额外通过项。OH19 的时间证据和 OH20 的过期世代判据各计一次。当前全套均未执行。

专项涉及的候选证据不得用注入达成标志替代真实输入。近满、坏档和时钟夹具允许预置边界数据，必须记录生成方式和原始指纹。 [需求、字段及展示](OBJECTIVE_HISTORY_DESIGN.md)
