# 版本和奖励事务

新 Run 使用 `C2.4-CAVERN-1`、revision 10、generation 13、`CrystalCavernC24/Cavern`。旧版本明确匹配各自 Prefab；没有新增存档字段或枚举。Boss `c24:boss:crystal-warden`，挑战 `c24:boss:challenge`，永久首奖 `c24.special.crystal-warden-first`。

首奖为紫色镰刀，`.gear` 和 `.pending` 身份派生稳定，沿用永久 specialRewards 和 pendingRewards。背包领取必须容量允许；拆解不删除 claimed 回执。新 Run 不覆盖原 earnedRunId。

普通奖励采用独立内容/Run/实例/种子/Boss 身份的 SHA 派生，不消耗旧奖励随机流：铁矿 2–4、晶石 3–5、新武器三类等权，品质候选白 50%/绿 40%/紫 10%。这是新增地图供给，不声称经济不变或最终平衡。普通装备进入现有拾取、撤离、仓库事务。

死亡专用路径先形成同一批实体及回执，再发布检查点。重复回调沿用实体 ID，不执行通用 Boss 奖励。未成功保存保留待重试；实际已写入但确认丢失，比较完整快照及 revision 后确认，不再发一批。测试在真实发布前/后分别抛出 IOException，未直接改档。

原始证据的 `reward-before-retry.json`、`expected.txt`、实际 save.json 含 Boss 死亡、普通地面物品 ID/数量/装备属性、首奖回执和待领物。新进程对照不是只比较物品总数。

正常再杀链的 profileId 为 `8ce43c9ce6a041528c5cf5f8e45dbba8`，首次 earnedRunId 为 `92783e072c3f4045bb8e65b463afcb54`；新 Run 以 `Evidence/Runs/PlayerNormalRepeat1/new-run.json` 为权威。普通材料本次实际铁矿 3、晶石 4，不借用上一局 3/5。

已通过范围与缺证边界见 ACCEPTANCE，不能将 v9 没有新增字段等同于重新执行全部历史迁移矩阵。
