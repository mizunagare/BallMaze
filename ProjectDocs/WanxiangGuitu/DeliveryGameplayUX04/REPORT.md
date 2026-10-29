# GAMEPLAY-UX04 交付报告

本批四项定向修复已经实现并分层验证；**整体仍为 UNRESOLVED，不是全绿验收或独立复审通过**。两次异常尝试和全部早期失败保留。原生鼠标键盘与独立人工仍未验收。

## 版本与边界

- 开工本地/远端main：`eb11dd3d8350f7e7a89d94d2e45d4cfd203f53e9`（已前进于任务书已知基线）。
- 主修复/共享制造业务：`2636d3ec`，完整值见[源绑定](Evidence/Bindings/source-bindings.json)。
- 最终产品冻结：`fb9dcb828787c6f73b9d5bc078df3d516593d85c`；最后差异只涉及营地HUD材料就绪读取/文案。
- 最终执行测试冻结：`5dfe7c39585a03549b67a1cdf675adbca33571a5`。
- 最终交付SHA为本报告所在固定提交；完整值及重新读取远端main的核对结果由交付回复提供，避免在提交内容中虚构自引用SHA。
- 工程外唯一测试根 `I:/WGCombat/GUX04-1029-A`；均为合成Profile、独立测试进程、启动前隔离。未访问真实玩家进度、抢桌面、关闭用户程序或强杀进程。
- 不改伤害/冷却/品质分支、经济、掉落、地图、随机流、结算语义、依赖或CI；用户场景/ProjectSettings/_Recovery五文件开工实际SHA256全部不变。历史交付以基线Git对象及工作区差异确认未改；没有补造不存在的全量开工工作区哈希。

## 问题、证据和最小修改

|项|修复前实测|实际修改|本轮证据|
|---|---|---|---|
|GAME04-01|根部+.08绘制半径1.800011；真实命中球心根部+1，对应地面截面1.547126。低矮资源非候选、HP70不变|共享MeleeGeometry；绘制真实球截面及细体积截线；保持原Overlap、方向、枪横向限制、自身Collider排除、遮挡及单目标去重，不扩大伤害|[旧顶点](Evidence/Before03/vertices.json)、[候选](Evidence/Before03/candidate.txt)、[120组矩阵](Evidence/Summary/range-matrix.csv)|
|GAME04-02|重复选择revision1→2；实际产出白剑但目标不结束；仓库取材制造后教程仍Withdraw|同目标无意义保存去重；真实CraftNow/CraftContainerNow消耗/产物完成后结束一次目标，营地仍由原事务原子保存/回滚；统一仓库制作推进教程；HUD统一读取营地库存|[修复前](Evidence/Before03/result.json)、[目标时间线](Evidence/Summary/goal-timeline.json)、[跨进程](Evidence/Shared07/matrix-resume.json)、[在途制造恢复](Evidence/Shared07/matrix-runcraftresume.json)|
|GAME04-03|选择配方后scrollY300→0|按页面、分区、列表、分类/筛选/搜索缓存像素位置；重建后clamp；独立列表不共享位置；筛掉选择时回退到当前可见行|[最终17项](Evidence/Scroll08/scroll.json)、[1280截图](Evidence/Scroll08/controlled-recipe-1280x720.png)、[1920截图](Evidence/Scroll08/controlled-recipe-1920x1080.png)|
|GAME04-04|抓取格旋转预期(2,0)，实际(0,0)；旧Ghost固定偏移/新Ghost固定32|连续抓取点+实际格尺寸；90度映射保持抓取位置；预览/落点同坐标；营地背包确定性预排一次提交、仓库列表排序；稳定ID双击委托原存取事务，拖动/重复/越权均拒绝|[完整规则](Evidence/Shared07/matrix-run.json)、[整理保存失败](Evidence/Scroll08/scroll.json)|

关键源码：`AdventureCombat.cs`、`CraftingTargets.cs`、`AdventureLoadout.cs`、`CampRuntime.cs`、`CampWorkbenchRuntime.cs`、`Onboarding.cs`、`AdventureState.cs`、`ContainerInventoryView.cs` 和 `CatInventoryPresenter*`，位于 Assets/CombatPrototype。14个修改/新增产品输入及隔离副本SHA256对应关系见源绑定。

### 目标持久化边界

Unity内联类的null经Clone/保存会重现默认白剑，本批真实恢复捕获了这一失败。结束目标使用既有字段 `type=-1, quality=White, containerId=""` 表示不追踪；既有Valid消费者原已将此值视为无目标。没有新增v9字段、额外奖励或制造历史。已有有效目标保留，不猜测旧白剑是否曾被误生成。成功后短通知表示完成，重启保持结束追踪，不提供新建的永久完成历史页面。

目标状态包括未选择、缺料、材料齐全待回营、打开工作台、可制作、未解锁、保存异常/待核对。完成/取消转为明确不追踪。营地失败原事务恢复库存、目标和教程；已发布回调失败按原完整Profile核对。冒险基础制作仍沿用原检查点保存时机，未保存内存不能宣称永久完成。详见[SAVE_COMPATIBILITY](SAVE_COMPATIBILITY.md)。

## 本轮实际验证

[统一JSON](Evidence/Summary/summary.json)、[856条明细CSV](Evidence/Summary/assertions.csv)与原始各轮结果分别保存；不是独特功能数量，也不包含旧批次PASS。

|层次|本轮结果|范围|
|---|---|---|
|定向规则/物理矩阵|466 PASS，120个实际释放样本|剑/枪、距离×角度×两种资源高度、实心墙、多Collider、真实HP、抓取旋转、目标、事务与整理|
|准备/营地/在途新进程|2+3+2 PASS|同Profile、一次目标结束、真实库存、Run/区域/seed/随机流/来源账|
|UI受控回调|10+17 PASS|实际制作按钮、列表/筛选/切页/缩放、仓库、HUD、保存失败回滚；非原生输入|
|受控时序|188 PASS|四武器普攻/技能、取消/冷却、遮挡、多Collider、暂停/恢复、投射物与生命周期；batch不创建额外GameView/截图|
|相关历史业务本轮重跑|60+15+34+33+26 PASS|UX02制造/容器、品质合同、远程范围、恢复负例、输入合同|
|正常AI|最终3进程PASS，均exit0/无超时|采集木8→渡口扣木2→撤离入仓6→取木2制造→仓库木4→再次森林出征→新进程一致；实际材料账以回执为准|
|B07经济|PASS（独立脚本）|满包、地面奖励、重复讨伐、徽章、死亡语义|
|非开发Windows构建|PASS，0错误/96警告，19.606秒|Unity6000.6.5f1，BuildOptions.None；不是正式Player原生操作通过|
|发行程序集排除|PASS|PE元数据无UX04/旧Editor验收驱动或UnityEditor引用|
|原生UI / 人工 / 性能|NOT_RUN|受控PointerEventData、回调、截图、Editor AI不得替代|

正常AI最终第一Run seed716339420、后继Run seed360772144，layout revision5；三轮身份/账本/随机状态有[原始轨迹](Evidence/Final3/Normal-Gather/normal-ai.csv)与[完整标记](Evidence/Final3/Normal-Gather/normal-results.txt)。各次独立运行seed不同，不把收益差异作为平衡改善。

最终HUD只读差异后重跑了UI、三进程AI和非开发构建；其他本轮规则对应前一产品冻结，相关战斗/事务实现未再改变，没有继承旧批次通过。详见[验收表](ACCEPTANCE.md)。

## 构建与输入证据

[完整警告](Evidence/Final3/Build/build-report-messages.json)、[PE与哈希](Evidence/Final3/Build/release-inspection.json)、[输入差异](Evidence/Bindings/build-input-comparison.json)。

- exe SHA256：`001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A`。
- Assembly-CSharp.dll SHA256：`F8D16DADB8657BE46CA8C090CD0000CB14B211FDFB77E25AE62314D6DD2DA27E`。
- 1387个构建输入中1386个保持原字节；后续只更正一个Editor测试源的关闭面板入口，旧/新输入可追溯。该驱动不在发行程序集。14个产品输入全部与仓库匹配，不将测试夹具变化伪称全输入不变。
- 未测性能，不根据零计数或构建成功宣称性能良好。没有升级/修复96条既有警告。

## 失败与限制（不可因后续PASS关闭）

1. 原正常AI续程停在phase31、活动时间1.64，按自带有界deadline exit1；原因尚未确定。没有强行推进时间或结算。后续独立Run的只读暂停观测和三进程成功不证明旧样本根因已解决。
2. Editor时序尝试出现 `d3d12: Unrecoverable GPU device error`，exit `-1073740771`，无超时/强杀。完整日志/原生栈保留为UNRESOLVED；不是正式Player样本，不能直接归并历史UNKNOWN。去除batch非必需GameView采集后188条领域断言通过，不据此宣称GPU根因修复。
3. 旧COMBAT01驱动在batch等待默认存档初始化而deadline失败。适配仅显式隔离初始化，并用现有Spear BasicPower保留125%合同；未降低伤害断言。旧结果不改。
4. 所有首次失败、夹具LastReleaseFrame误读、null/空串、null内联序列化、GeometryStore门禁/存储根、营地关闭入口用错均见[失败历史](FAILURE_HISTORY.md)。失败的完整编排exit1保留，不能用后续编排exit0外推验收全过。
5. 自动整理首版仅营地且数据就绪；冒险中保留手动拖放。贪心预排不是最优装箱，失败保持原布局；稀有无解形状穷举未执行。装备盘/穿戴/overflow不自动重排；永久仓库为列表，不虚构格子。
6. 120组证实一个范围显示缺陷；不能证明所有历史截图未命中都同因。体积/地面截线仍需Collider、方向和遮挡共同成立，并非保证伤害。原生抓取的手感/像素级鼠标观察未执行。
7. 首次修复前夹具源码没有单独的字节冻结；原始结果、日志、候选与顶点仍保留，后续已执行源在各Output中保存。目标时间线为真实断言顺序，未逐事件捕获墙钟时间；final存档含实际ID/位置/修订/账本。不将逻辑顺序伪称逐帧录屏。
8. UI-01 UNKNOWN、Editor青色帧/Search/JobTempAlloc、旧C15继续UNRESOLVED，原生U16/独立人工继续NOT_RUN。本批未进行无新线索的产品生命周期试探。

弓蓄力、法杖和可选追踪仅在[设计提案](COMBAT_DESIGN_PROPOSALS.md)，未实施新机制。提交推送后暂停，等待固定SHA独立复审，不自动开下一批。
