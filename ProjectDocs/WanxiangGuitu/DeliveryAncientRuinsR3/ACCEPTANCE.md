# C1-R3 验收

| 检查项 | 结论 | 证据 |
| --- | --- | --- |
| 白色双刃、巨剑、镰刀独立产出 | PASS | White1–8，55 个实际新 Run |
| 白色产物、铁矿和晶屑同冻结公式及实际持久化一致 | PASS | Audit/white-audit.json 与实际地面分页 |
| 两套隔离工程启动前与仓库跟踪字节一致 | PASS | frozen-inputs.json 与独立 inputs-before 快照 |
| 构建期间跟踪文件保持原始字节 | FAIL | 实际观察到导入和 BuildPipeline 写回 |
| 所有变化的实际构建输入语义等同性 | UNRESOLVED | URP、GraphicsSettings 等字段出现实际差异。发行可用与所审 IL 一致不能证明全量等同性 |
| 两个纯包构建、标题启动、退出和实际 Bee 五项关闭 | PASS | CleanA、CleanB 原始回执与 PureBootA、PureBootB |
| A/B 全部发行文件字节一致 | FAIL | 5/189 不同，分文件定位 |
| 原生输入、人工体验和最终平衡 | NOT_RUN | 本轮仅隔离自动化和只读证据 |
| 历史 JobTempAlloc、内存漂移及版本标签 | UNRESOLVED | 继续分开记录 |
| GC/GPU 校准与性能验收 | NOT_RUN | 本轮未采样 |

封存门槛要求白色多样性和构建输入等同性均有通过证据。构建等同性仍开放，C1 候选等待独立复审。
