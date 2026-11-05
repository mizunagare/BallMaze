# 五区连通审计

本轮重跑入口、石柱广场、机关走廊、地下祭坛、守护者大厅。R2Rewards 每段先求实际 NavMesh 角点，再由正式玩家 CharacterController 行走并核对到达高度。大厅返回地下祭坛后，继续走过走廊、广场和入口。地下高度约 -2.96 m，地面约 0.07 m，往返路径包含转角和高差。关门时物理线检查及跨门 NavMesh 路径均阻断，开门恢复，可从另一侧再次关开。密室使用实际胶囊检查，解读碑文后进入。

R2Assist 的遮挡射线首命中猫族十棱石柱。R2WallStaff、R2WallBow 各有实际弹体 Spawn 和墙面碰撞。真实精英和守护者运行保留 AI 的实际位置、追击与碰撞记录。相对首次采样的最大位移分别为 1.50 m 和 1.87 m。其他无关敌人按夹具隔离。没有执行让所有敌种通过每一扇门、每处楼梯或整条五区路线的独立矩阵。

[五区路径](Evidence/R2Rewards/path-corners.jsonl.gz) · [移动轨迹](Evidence/R2Rewards/runtime-trace.jsonl.gz) · [石柱和墙体](Evidence/INDEX.md)
