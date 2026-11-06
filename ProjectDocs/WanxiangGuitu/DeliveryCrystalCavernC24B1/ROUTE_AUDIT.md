# 路线只读对照

参考产品 `37b25bb641c72deefe4e7e48f19f270711f7fc01`，候选为本分支三文件提示修正版。六组实际 Editor 加载同份隔离档；复制文件哈希、恢复后的完整检查点、全部评分字段、实际 Ranked 顺序均存档。比较口径先在 PLAN 登记：离散精确，浮点 abs≤0.0001 或 rel≤0.00001。未改变原 C02/C04 规则。

[ScoreComparison1](Evidence/Runs/ScoreComparison1/summary.json) 原始结果8 PASS/27 FAIL保留：按数组下标比较运行时无序资源／掉落集合造成身份错配；此时所有35个POI评分本身已一致。新审核 [ScoreComparison2](Evidence/Runs/ScoreComparison2/per-poi.json) 读取同批输入，按稳定 entityId 排序，并拒绝空／重复ID；不改任何值或容差，35 PASS。原数组、输入哈希、差异均保留。没有重跑场景或挑选样本。

完整覆盖：森林、遗迹、C21、C22、C23闭桥、C23开桥；每项包含可达性、出口、路径、目标、风险分项、全部预期材料、装备、总分、排名。结论仅限这六份合成状态，不外推所有随机种子。

## 新 Boss 收益缺口

[实际 arena-route](Evidence/Runs/b1-name-cavern-A1/arena-route.json) 中 Boss 区：1活敌、0资源节点、0箱、0地面物；因此此样本没有混入其他收益源。内部 expectedMaterials=兽皮10/晶石5，装备0，totalScore≈24.41984。[实际 UI](Evidence/Runs/b1-name-cavern-A1/route-ui.txt)显示“野怪皮/晶石碎片”，没有铁矿、装备机会。

|普通收益|当前路线预测|专用工厂规则／理论均值|问题|
|---|---:|---:|---|
|兽皮|10|0|误计10|
|铁矿|0|2–4，均值3|漏计3|
|晶石|5|3–5，均值4|高估1|
|装备|0|恰好1|漏计1|

工厂是 `CrystalCavernBossRewards.Drop` 的独立身份哈希派生，种类三选一；品质候选50/40/10。均值依据离散取模设计，不能把一局实际掉落当均值。新运行死亡／确认完整快照在各提示用例 `death-checkpoint.json` / `confirmed-checkpoint.json`，均有实际地面普通装备、铁矿、晶石及稳定ID；[NoticeAudit1](Evidence/Runs/NoticeAudit1/results.json)确认重试不重抽。永久首奖另在 Profile，不计重复收益。

原因：通用 Boss 配置仍有 ExpectedHideYield=10、crystalAmount=5、GearDropChance=0；RouteScoring 通用敌人分支使用这些字段，未投影 C24 专用工厂。最小提案是在只读收益投影中精确识别 C24版本及Boss身份，给出上述普通工厂预期；不改权重、不改真实工厂/RNG/首奖。**待单独授权，本批未实施。**
