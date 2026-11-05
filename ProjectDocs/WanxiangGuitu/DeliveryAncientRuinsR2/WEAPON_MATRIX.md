# 七武器矩阵

| 武器 | 五区受控真实攻击及大厅扩展技能 | 活体守护者普攻、取消、暂停与切换 |
| --- | --- | --- |
| 长剑 | R2Sword | GuardianSword |
| 长枪 | R2Spear | GuardianSpear |
| 法杖 | R2Staff | GuardianStaff |
| 弓 | R2Bow | GuardianBow |
| 双刃 | R2Twin | GuardianTwin |
| 巨剑 | R2Great | GuardianGreat |
| 镰刀 | R2Scythe | GuardianScythe |

五区矩阵用明确标注的高生命碰撞夹具保持七种武器的接触条件。真实守护者补测用原场景中实际存活并运行 AI 的 Boss，正式攻击、弹体或近战碰撞改变其生命。第二部分针对每种武器发起技能，在释放前用正式背包暂停。暂停中模拟时间冻结，恢复后已取消技能没有迟发伤害，再经正式主副武器切换。镰刀牵引按真实位移与生命不变验证。

软锁定实际弹体接触和剑有限自动面向在 R2Assist 复跑。法杖、弓走廊实体墙体遮挡为 R2WallStaff、R2WallBow。各武器与所有区域、每种辅助和遮挡组合的全排列 NOT_RUN。七种武器的完整守护者两阶段击杀矩阵 NOT_RUN，实际两阶段击杀与下一局复杀样本使用长剑。

[五区逐项](Evidence/Derived/weapon-matrix.json) · [守护者逐武器证据](Evidence/INDEX.md)
