# C2.2 验收

| 验收项 | Editor | 非开发测试 Player |
| --- | --- | --- |
| 关门物理阻挡及 NavMesh 断开；开门、顶盖和玩家双向通行 | PASS | PASS |
| 正常机关和宝箱交互；重复拒绝；保存和新进程恢复 | PASS | PASS |
| 实际撤离后新出征，普通宝箱再次产出，不复用掉落 ID | PASS | PASS |
| 晶壳与暴露实测伤害差、精英预警攻击、恢复、暂停和规避 | PASS | PASS |
| 精英实际击杀、掉落唯一性、死亡和落地奖励恢复 | PASS | PASS |
| 能量恢复和预警期不受伤、翻滚拒伤、死亡卸载 | PASS | PASS |
| 组合避险、侧道和实际精英通行 | PASS | PASS |
| 七武器各自普攻和默认技能对活体的真实命中 | PASS | PASS |
| 铁矿和晶石真实采集、拾取、跨进程撤离入仓及重复确认 | PASS | PASS |
| C2.1 旧在途档，森林与遗迹入口、保存及在途读取 | PASS | PASS |
| 新资源的支持检查与肩后实机证据 | PASS | PASS |

| 独立验收或限制 | 状态 |
| --- | --- |
| C2.1 冻结包七武器、材料闭环、能量区补测 | PASS |
| Windows64 正式构建，Development=false，Bee 五项关闭，纯包无驱动 | PASS |
| 纯发行标题和正常退出，合成存档不变 | PASS |
| Resources.meta 生成内容、GUID、构建前后哈希和可搜索序列化引用 | PASS |
| 全量发行包语义等同性及 C1 的历史写回因果 | UNRESOLVED |
| 构建结束 JobTempAlloc 原因 | UNRESOLVED |
| 原生物理键鼠 | NOT_RUN |
| 人工体验与可读性 | NOT_RUN |
| 最终平衡 | NOT_RUN |
| 校准后的 GC/GPU 及预算验收 | NOT_RUN |

表中产品失败项为 0。原始运行共保留 8 条明确失败断言，另有编译、启动前拒绝与超时记录。历史 C1/R7 状态另计。通过断言数按 [选定运行](Evidence/selected-runs.json) 计算，单项的完整原始结果见 [证据索引](Evidence/INDEX.md)。
