# UX-06 数据映射

基线 `1c3fb90bf5902c147fda35252dc59e3b3a5f8872`；D-23 A 只展示。根 AGENTS 从原工作区读取，相关目录未发现额外 AGENTS。

|显示|权威来源|投影规则|
|---|---|---|
|森林两首领已记录讨伐次数|BossHuntRecord.bossId/kills|仅按 forest:warden / forest:tide；不按 forest.challenge 数量|
|森林纪念|Profile.badges|两首领与 forest:dual-hunt 精确稳定 ID|
|遗迹五项收藏|Profile.specialRewards|c1.special.artifact / guardian-first / chronicle / collector-seal / gate-key；按永久回执与 claimed，不读当前背包|
|洞窟首次纪念|c24.special.crystal-warden-first|与遗迹明确分组；claimed=false 为已记录待领取|
|近期目标|独立回读已发布 Profile.objectiveHistory|同 UX-05 双 UTC 与身份键排序，名称快照；前三条预览，跳转原地区筛选/分页|
|历史覆盖|objectiveHistoryLegacyUnknown + 有界集合|全地区最近128条；缺失/裁剪不作为永久倒退或未完成|
|探索总次数|DATA_GAP|暂无足够地区出征账本；不使用全局 committedRuns|
|成功撤离总次数|DATA_GAP|有界目标记录不等于所有撤离|
|终身最高纪录/挑战耗时|DATA_GAP|既有 UTC 不表示出征起止时间|
|复访方向|ObjectiveCatalog / RuinsLayout / CrystalCavernLayout / CrystalCavernBossRewards.Drop|仅现有机关、矿晶、宝箱、挑战与新武器说明，无动作与收益|

仅地区档案读取独立已发布存档投影，不消费 Settlement.plan。保存受阻/待回读时入口不可用。浏览没有保存、结算、领取或发奖调用。

历史路线图关于 v10/v11、槽位和地区次数的旧推论被当前用户冻结决策覆盖；本批不重开设计、不新增字段。九局仅验证具体记录展示与连续/冷启动一致性，不证明留存或乐趣。
