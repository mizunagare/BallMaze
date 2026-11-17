# 独立只读保护审计

## 结论

**PASS_PROTECTION_WITH_EXPECTED_HISTORICAL_PAYLOAD_DRIFT。** 这是保护范围、文件身份和历史原件审计通过，不替代功能/浮点/Player验收，也不构成暂存或提交授权。

- 不采用旧summary作为事实来源：从原始manifest逐条读取当前和快照实际字节，独立计算SHA-256与长度。
- 原始 **12808** 条、合计 **451084890** 字节；快照12808/12808均与manifest一致；当前12804完全一致，恰好4条授权源变化，未授权变化/缺失均为0。
- 两份保护TSV各12808唯一数据行，与独立结果逐列比较baseline/snapshot/current SHA、bytes、classification，错误0、重复0、额外路径0；两份TSV自身字节哈希相同。
- 历史961路径全部实际存在，缺失0；其中5 tracked、956 untracked。旧TXT/CSV/AUDIT_INDEX原样未动，旧CSV中的四授权payload hash必须保留旧值，不能刷新。

完整逐文件双端重算结果、961逐路径现状及禁止域明细见 [PROTECTION_REVIEW.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/FINAL_AUDIT_EVIDENCE/20261117-0938/PROTECTION_REVIEW.json>)。

## 输入与算法

原始 [PRECHANGE_FIX_SHA256.json](<I:/unity/WanxiangGuitu-UX04B2R2FIX-snapshot-20261116-1536/PRECHANGE_FIX_SHA256.json>)，SHA-256：

5aaa2697e5b0807c91c9a128033167dc2ad2d82fee3406e5c4e235028456939d

对manifest全部条目分别读取工作区与快照workspace原始Buffer，按实际长度及原始字节SHA-256比较，不做编码、换行、空白归一化。原件范围分布：Assets 1472、Packages 2、ProjectSettings 28、UserSettings 2、ProjectDocs 7134、Evidence 4170。

计算方法保护块独立从精确签名至匹配闭合大括号提取，逐字节Buffer.equals后再算SHA，不使用历史guard结果代替比对。额外重新glob当前Assets/Packages/ProjectSettings路径集合，新增/缺失均为0。

## 四授权变化

| 当前授权源 | 当前SHA-256 |
|---|---|
| [AdventureLoadout.cs](<Assets/CombatPrototype/AdventureLoadout.cs>) | c6791285164e388f0b686b2558e89bead2bd985a216fb4ff21f21e8e9b074d48 |
| [B2AttackModel.cs](<Assets/CombatPrototype/B2AttackModel.cs>) | 6e45644e73ca6d5a8a4eaf560714d44bda5a69df2fcbdb4e05bf1b5e6a899e1d |
| [CatInventoryPresenter.cs](<Assets/CombatPrototype/CatInventoryPresenter.cs>) | c493e7b164c08a0be6477f9068da66c61cc5ce7286a9db7b714218870372b0fc |
| [ContainerInventoryView.cs](<Assets/CombatPrototype/ContainerInventoryView.cs>) | 93710dbd66bba1dd5cdd0ac5f57fbcf63eacb75a4dc57c38bd86f2ac50ef7466 |

4源授权不等于其所有行为自动获批；共享CanPlace/Place几何入口确有显式重构，不能宣称整个授权源或整个几何业务未改。权威尺寸定义及底层Fit/Find/ContainerFor原块实际未变。

## 两份保护表与summary

- [FINAL-PROTECTION保护表](<Evidence/Runs04B2R2FIX/FINAL-PROTECTION/PROTECTION_SHA256.tsv>)：12808行全部与实际一致。
- [交付根保护表](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/PROTECTION_SHA256.tsv>)：12808行全部与实际一致。
- [FINAL-PROTECTION summary](<Evidence/Runs04B2R2FIX/FINAL-PROTECTION/summary.json>)：baselineCount、授权变化集合、零errors、方法SHA及byteIdentical、历史两清单原样、ComputeAttack恢复single Sum链均可由本次独立结果支持。
- 本次只读重新核验HEAD 95caf234256613d4a6e4f89a8ab0dc09c397c6b2、分支feature/ux-progression-04-b2、staged空、diff --check返回0，与summary一致。Git提示一个授权源未来可能LF→CRLF；这是警告，不是本次实际字节变化，也未执行Git改写。

## 精确方法与禁止域

[B2AttackModel.cs:96–127](<Assets/CombatPrototype/B2AttackModel.cs#L96-L127>) 中：

| 原始保护块 | 长度 | 当前/快照共同SHA-256 | 原始字节相等 |
|---|---:|---|---|
| ComputeDefense | 383 | 691495d74f53e9b3a58e58614af740dea3136380faf7a2f985a5e69f9b6626af | 是 |
| Active | 522 | dbf3f6ac88d66fcfa47a50a7abbaa58c77f54a1d717b3386a494ef85641ecfc3 | 是 |

[AdventureLoadout.cs:166–208](<Assets/CombatPrototype/AdventureLoadout.cs#L166-L208>) 原底层ContainerFor(329字节)、Fit(729字节)、Find(497字节)亦独立原始字节相等，完整SHA见JSON。

- v9/v10/v11：[CombatSaveSystem.cs:89](<Assets/CombatPrototype/CombatSaveSystem.cs#L89>) 仍写冒险v9/其他v6；[CombatSaveSystem.cs:232](<Assets/CombatPrototype/CombatSaveSystem.cs#L232>) 仍仅接受1..9。该文件及全部原有存档/迁移/验证数据文件与pre-FIX完全同一字节身份；本FIX未新增v10/v11版本支持。
- D24 coeff/物品属性/尺寸：[AdventureItems.cs](<Assets/CombatPrototype/AdventureItems.cs>)、[ContainerDefinition.cs](<Assets/CombatPrototype/ContainerDefinition.cs>)及所有非授权权威源未变；以上原几何核心方法也实际未变。
- 掉落/随机：[AdventureRandom.cs](<Assets/CombatPrototype/AdventureRandom.cs>)、[NewWeaponDrop.cs](<Assets/CombatPrototype/NewWeaponDrop.cs>)、[NewWeaponDropRules.cs](<Assets/CombatPrototype/NewWeaponDropRules.cs>)实际SHA/bytes未变。
- BossP1P1C：全部12个Boss相关产品源实际未变（含ForestBoss/AdventureFlow.Bosses）；JSON列出路径与当前SHA。
- 场景/prefab：109个资产及其109个meta，共218条，全量SHA/bytes未变。
- Packages全部2项、ProjectSettings全部28项当前实际未变且路径集合无新增/缺失；Assets当前1472项同样无新增/缺失，仅上述4授权变化。
- 全部16个原有INDEX/AUDIT_INDEX条目均与pre-FIX manifest和快照一致；没有更新旧901 INDEX或任何旧文件。

## 历史961原件及payload区别

| 历史原件 | 当前/快照共同SHA-256 | 字节数 |
|---|---|---:|
| [SUBMIT_WHITELIST.txt](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/SUBMIT_WHITELIST.txt>) | efd037946e4f3acd859c39e771a8c8a534f86a537821e4650476cd36a756b2e5 | 113026 |
| [SUBMIT_WHITELIST.csv](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/SUBMIT_WHITELIST.csv>) | 5203aa4c87f7370a80de4693d45f99b67e6bb5284fd901c82e8809e483880b49 | 279391 |
| [AUDIT_INDEX.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/AUDIT_INDEX.json>) | 580e08f5ba36a0d99e1082a3dbd9050cb43edbf8be3c0218fb11b0e18294d542 | 28414 |

TXT和CSV各961路径、集合完全相同，961均实际读取/重算且存在。CSV的实际SHA payload漂移恰为4授权源；另有3行SELF_REFERENTIAL_META是原有自引用占位（旧CSV/旧AUDIT_INDEX/WHITELIST_SUMMARY），不是3个额外hash损坏。没有其他历史SHA payload漂移。

5个已跟踪历史路径：[AdventureLoadout.cs](<Assets/CombatPrototype/AdventureLoadout.cs>)、[CampInventoryView.cs](<Assets/CombatPrototype/CampInventoryView.cs>)、[CampRuntime.cs](<Assets/CombatPrototype/CampRuntime.cs>)、[CatInventoryPresenter.cs](<Assets/CombatPrototype/CatInventoryPresenter.cs>)、[ContainerInventoryView.cs](<Assets/CombatPrototype/ContainerInventoryView.cs>)。956个其余路径均为当前Git索引未跟踪；逐路径标志见JSON。未跟踪不代表缺失、失败或默认应提交。

历史961分布：产品Assets/CombatPrototype 11；Evidence/Runs04B2 256；Evidence/Runs04B2R1 513；B2交付文档26；R1交付文档155。未见其他无关顶层目录混入这961项，但它们是旧B2/R1候选，不是新FIX自动提交授权。

## 给lead的新精确提交白名单建议

1. 以本次4源当前SHA固定产品payload；新FIX交付文档/工具/证据和本次审计输出按实际依赖逐路径列出，不复用旧CSV的futureStaging命令。
2. 若交付必须附带旧B2/R1依赖，只逐路径显式纳入所需历史原件，保持旧TXT/CSV/INDEX原样；旧名单内四授权源旧hash作为历史事实保留，新hash只写新证据。
3. 不因956项untracked就整目录纳入；不得无差别加入历史Evidence/docs，也不纳入无关目录、Builds/Library/Temp/UserSettings/Packages/ProjectSettings/场景/prefab或用户改动。
4. 本审计未执行git add/stage/commit、Build、Player或启动Unity；仅新增本目录两个PROTECTION_REVIEW输出。没有更新或修复任一旧表。

## 严谨限制

结论针对采样期间manifest原件与明确禁止域的文件身份保护，不证明所有新交付文件都具备正确的运行时语义。授权4源内部的功能正确性、预览事务和浮点行为应结合独立源代码/运行证据审计；本审计没有进行Build或Player重跑。
