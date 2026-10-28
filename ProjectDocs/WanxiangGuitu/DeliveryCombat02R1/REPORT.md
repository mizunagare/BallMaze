# COMBAT-02-R1：启动竞态定位与最小夹具修复

开始本地/远端main：`fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a`。最终固定SHA见交付消息及本报告所在Git提交。仅修改文档目录内测试工具、证据、共享准备入口的夹具映射与开发计划记录；没有修改产品Assets、恢复、生成、武器或v9合同。

## 结论与因果证据

U07定位为旧B07Rules夹具抢在产品延迟Start完成前手动初始化/出征。不是把Boss查找放宽，也不是产品把已正确加载的森林奖励重抽。

|时刻|观察结果|
|---|---|
|旧夹具复现第1帧|手动InitializeStorage(b07-save)，新Run seed975140455，两个已初始化Boss；出征保存revision2|
|第2帧|原CombatSaveSystem.Start的yield return null结束，调用InitializeDefaultStorage→InitializeLocatedStorage→InitializeStorage；同一session变为营地，ActiveRun清空，路径改到另一隔离目录|
|40次导航后|夹具继续临时建图，却仍假定初始Run存在；LoadProgress读取的是当前营地存档路径，恢复营地是正确结果|
|Single前|同一场景/同一session，AtCamp=true、Tracking=false、RuntimeForest inactive，数组和实际活动场景均无森林Boss；原Single断言抛Sequence contains no matching element|

只读快照、实际保存调用栈、同一session EntityId/scene raw handle、Boss EntityId/Kind/初始化引用、实际数组映射及磁盘封装revision均有记录。最大重入深度1，不支持“递归Tick”解释；没有发现重复session或跨场景误选。前后Snapshot的Unity/Rewards/Placement/Events状态均不被观察器推进。

**原历史独立佐证**：旧storage-audit记录14:42:32先initialize/save b07-save；14:42:36再initialize/save Recovery/WanxiangGuitu/ForestRuins；14:43:39从后者load。这与本轮三进程的路径切换、清空Run和调用链一致，不是仅用新Run的PASS推断原根因。原瞬间内存缺失仍在INPUTS中明示。

源码对应：CombatSaveSystem.Start先yield一帧后执行默认初始化；旧B07Rules仅检查unscaledTime>.5，不能证明Start完成，首帧耗时可能已超过该阈值。初始化操作来自测试主动调用，随后产品正常启动流程继续；正常入口由同一Start接管，并不采用该夹具抢跑路径。无需修改产品恢复/生成。

## 最小修复

诊断版B07RulesReady与无探针的B07RulesStable测试源：在第一次手动InitializeStorage之前，观察产品IsInitialized，并等待其后一个实际player frame，再执行原夹具。保留非batch启动、原Single、全部原断言、40请求、存取/回执规则和360/600秒时限。普通夹具显式区分batch（原产品Start本来就跳过默认初始化，维持原手动初始化）和非batch就绪门控；未改成batch绕过原非batch问题，未禁用产品启动、未注入Boss或最终存档、未强制标记初始化完成。

56段Need语法片段（含声明）和2处Single片段与原源字节相同；实际编译的测试源码逐进程归档。原测试和新就绪版分别存放，未覆盖历史源。观察器最初使用废弃实例/句柄API产生编译错误，确认后只适配工具到本机GetEntityId/GetRawData，没有升级依赖。

## 实际运行

- 未加就绪门控：3个独立非batch进程，均真实exit1，3/3同类Single失败。各使用原seed975140455、独立新Run/合成根。
- 就绪门控后：3个独立非batch进程均真实exit0，无超时。第2帧观察产品初始化，第3帧执行夹具；40次请求后仍从b07-save恢复同一Run，两个真实Boss引用/Kind/初始化状态正确，原Run方法全部规则到末尾。
- 去掉探针/固定seed的普通中间版3个非batch进程也通过并留档；最终双模式普通夹具又经3个非batch与1个batch进程验证，均真实exit0、无超时。共享Invoke-Rules的PrepareOnly入口仅追加一条映射，实际复制SHA与最终Stable源相同；历史B07原源不修改。
- 42条派生证据检查PASS。它们是诊断断言，不是人工、正常AI或正式Player测试；不宣称平衡完成或整体验收通过。
- 本批未重跑后续Resume/Pending/Committed、全部无人值守All、正常AI、发行构建或原生操作，范围仅首次Run首因；旧后三次依赖exit1继续保留。

产品358项冻结源输入、115个C#副本绑定及产品Editor DLL哈希相同；用户5文件未变；原127项锁定文件/旧aggregate和59项原始证据均不变。缓存PDB可能显示旧C2源码路径，实际PID/命令/存档根均为R1-B，不能仅凭PDB路径误判运行目录。

## 失败历史与限制

R1-A观察器编译失败后Unity停在Safe Mode，外层600秒超时，实际Unity退出码未取得；不计入业务复现。预检修正后才在新B副本运行主要3+3诊断对照进程（另7个普通夹具兼容验证独立留档）。该编译失败及所有清理请求均保留；安全清理未完成，拥有者PID93960仍存在，未强杀或激活桌面。后置源码快照的文件名不等于执行证据，实际失败编译源为Trace-before-api-fix及编译日志；退出请求脚本没有执行回执。

原C15、D3D12 UNKNOWN、青色帧、Search、JobTempAlloc、旧Editor启动阻塞继续UNRESOLVED；原生U16、独立人工、发行实战和完整性能保持NOT_RUN。没有关闭用户程序、修改快捷键、访问真实存档、升级依赖或新增CI。

建议独立复审确认U07在本次已复现的测试初始化合同内关闭。原COMBAT02总表/aggregate仍FAIL不回写；本批交付不等于整体游戏、发行或独立审阅通过。

[输入边界](INPUTS.md) · [验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [证据](Evidence/INDEX.md)。交付后暂停。
