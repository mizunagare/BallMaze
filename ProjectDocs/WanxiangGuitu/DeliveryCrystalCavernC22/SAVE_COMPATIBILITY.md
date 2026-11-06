# 存档与固定资源

| 内容 | 布局修订 | 地图生成版本 | Resources 路径 |
| --- | --- | --- | --- |
| C2.1-CAVERN-1 | 7 | 10 | CrystalCavern/Cavern |
| C2.2-CAVERN-1 | 8 | 11 | CrystalCavernC22/Cavern |

基线 093d0bfebd33747d4a2b035b22b26a701778a8ca 作为 C2.1 内部开发检查点。读取路径根据保存的布局身份选择资源，校验内容版本、布局、生成版本、seed 和事件。旧矿脉和危险区 ID 继续有效。

v9 结构无新增字段。C2.2 用原有 WorldEvent 保存 `c22:chamber:lever` 与 `c22:chamber:chest` 的 used 位。要求两条事件的身份、位置、类型与固定布局对应，箱已开必须有机关开启记录。精英 `c22:channel:crystal-core` 使用现有敌人快照与地面掉落快照。新地图没有永久特殊奖励。旧 C2.1 仍要求事件列表为空。

沿用旧 Run 的存档读写、来源账、结算身份与确认流程。危险区读取后的恢复窗保持 C2.1 行为。
