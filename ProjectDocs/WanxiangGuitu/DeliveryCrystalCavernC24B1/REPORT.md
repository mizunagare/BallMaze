# C2.4-B.1 提示修正与定向复核

基线 `acbfbe3f567f1b0928559741f8370478bec6502c`；独立分支 `fix/cp06-crystal-warden-b1`。本报告对应提交中的产品树；最终完整提交 SHA 以交付回复及远端分支核对为准。不是地图整体验收或独立复审通过。

## 实际修改

仅修改三项产品源码：

|文件|行为变化|
|---|---|
|`CrystalCavernBossRewards.cs`|使用本次 `Earn` 返回值传递首奖提示上下文；不以旧回执是否存在推断本次首杀。|
|`AdventureFlow.Bosses.cs`|新增仅内存的 C24 提示上下文。死亡时提示保存中；既有写入成功或完整检查点读回确认成功后才显示成功。同一 Run 重试不重复播报。未新增存档字段或改变保存条件。|
|`CombatEnemy.cs`|仅稳定 ID、Boss 类型及 C24 Brain 同时匹配时返回晶脊守望者；旧森林目标保留古林狞猫守卫。|

冻结的瞄准、镜头、路线评分、危险区、武器和奖励算法均未修改。保护核对见 [protection-final.json](Evidence/protection-final.json)：1,448 项产品输入中仅上述三项授权变化，5 项用户文件不变，193 项冻结新纯包文件不变。

## 修复前后证据

旧 Player 死亡回调及 before-publish 故障前已显示“首奖记入营地待领”，尚未持久化；见 [BeforeNotice1](Evidence/Runs/BeforeNotice1/notices.tsv)。新版本先显示“检查点正在保存，失败可重试”，成功后才显示“首奖可回营领取”。真实写入失败、已写入但确认丢失以及旧首奖待领／已领／拆解后三种重复击杀，均有 Player 事件、消息、完整奖励快照及进程回执；独立复核见 [NoticeAudit1](Evidence/Runs/NoticeAudit1/results.json)。没有重跑整个奖励生命周期。

旧名称同帧上下不一致：[修复前](Evidence/Runs/BeforeNames1Run/names.png)；新 Player 同帧上下均为晶脊守望者：[修复后](Evidence/Runs/b1-name-cavern-A1/names.png)。[旧森林负例](Evidence/Runs/b1-name-forest-A1/names.tsv)仍为原名称。均为受控观察，不是原生输入或人工可读性结论。

## 只读取证

- N02 使用引入 C24 前的 `37b25bb641c72deefe4e7e48f19f270711f7fc01` 对照本候选；森林、遗迹、C21、C22、C23 开桥／闭桥六份同哈希合法合成档，35 个 POI 全字段及排序一致。见 [ROUTE_AUDIT.md](ROUTE_AUDIT.md)。只做 Editor 配对，不声称 Player 两版本评分配对已跑。
- C24 Boss 路线收益存在真实展示缺口：误计兽皮10、遗漏铁矿均值3和装备1、晶石预期5而工厂均值4。只报告，不修改评分或掉落。
- 晶环内外擦边的 Collider 伸入环带，根节点仍在安全侧，实际不扣血；环带对照扣22HP、完全外侧不扣。见 [RING_AUDIT.md](RING_AUDIT.md)。设计口径需要另行决定，本轮不改规则。

## 新纯包

`I:/WGCombat/C24B1-1107-A/PureBuild1/Release`，Unity 6000.6.5f1，Windows64，BuildReport Succeeded、0 errors、111 warnings、options=None；实际 Editor exit=0。完整原始日志未过滤。固定 Release Profile 与 Bee 五服务均关闭，见 [发行审计及193文件清单](Evidence/release-audit-PureBuild1.json)。构建先于隔离 Editor 驱动导入；观测 Player 在独立复制包中附加驱动，不改纯包。

[纯包运行](Evidence/Runs/PureTitle2/pure-runtime.json)：标题正常、未创建游戏对象、合成存档不变，真实进程退出码0。后台关闭消息不是物理键鼠或菜单退出验收。纯包不声称完成受控故障测试；这些属于 Editor 和非开发观测 Player。

本轮候选 Editor 原始断言 **71 PASS / 0 FAIL**；非开发观测 Player **113 PASS / 0 FAIL**；N02 逐 POI **35 PASS**。修复前复现的17项捕获断言另列，不计候选通过数。需求级仍有路线收益 FAIL 和晶环口径 UNRESOLVED。

原 B 的 `18 PASS / 2 FAIL / 1 INCOMPLETE / 6 NOT_RUN / 2 UNRESOLVED` 完整保留；C02、C04 不重采样不改容差，C05 保持 INCOMPLETE。原生输入、人工体验、平衡、性能及历史引擎／构建问题未关闭。详见 [ACCEPTANCE.md](ACCEPTANCE.md)、[FAILURE_HISTORY.md](FAILURE_HISTORY.md)、[TESTING.md](TESTING.md)。

