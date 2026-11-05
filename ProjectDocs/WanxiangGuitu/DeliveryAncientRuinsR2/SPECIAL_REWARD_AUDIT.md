# 特殊奖励唯一性审计

固定源码的永久键为 c1.special.artifact、c1.special.guardian-first、c1.special.chronicle、c1.special.collector-seal、c1.special.gate-key。奖励由当前 Profile 的 specialRewards 记录，回执包含首次 Run ID 与 claimed。相同奖励在两个独立档案使用相同定义键，各自保有自己的获得 Run。定义键和玩家存档身份是两层。

- R2Rewards 通过真实交互取得四类探索回执。隐藏箱普通装备落地，遗镰进入营地待领。R2Salvage 从前一进程复制的原始存档恢复同一档案与待领项。
- R2Salvage 使用真实背包装入接口填满合成档格子。满包拒绝领取并保持待领，保存读取后继续保留。营地领取发布前失败回滚，发布后异常通过存档内容核对确认。重复领取拒绝。
- R2Salvage 从仓库取出遗镰，实际拆解产生铁矿，随后保存、读取、新出征并再次开启隐藏箱。装备已经消失，永久回执仍为已领取，特殊装备没有再发。
- R2Boss 与 R2ResumeBoss 验证首次守护者奖励、新进程、重复死亡回调、结算及再出征。下一 Run 重新真实击杀，只得到常规战利品，首次回执保持唯一。
- R2LegacyThree 与 R2LegacyFive 使用 R1 以前的真实合成 v9 检查点。保留旧在途行为。全量 v1–v8 迁移和恢复更早的外部备份不在本轮实测范围。

[存档审计](Evidence/Audit/v9-snapshots.json) · [运行证据](Evidence/INDEX.md)
