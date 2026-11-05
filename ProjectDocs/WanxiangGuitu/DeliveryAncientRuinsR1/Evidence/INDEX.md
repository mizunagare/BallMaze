# CP06-C1-R1 证据索引

原始运行位于 I:/WGCombat/C1R1-1105-A。仓库发布副本保留源文件 SHA256 与发布文件 SHA256。日志及逐帧记录使用 gzip，已脱敏的路径和许可字段在清单中标注。发行二进制仍在本机隔离根，用完整构建文件清单核对。

| 事项 | 原始证据 |
| --- | --- |
| 分类、各次实际退出和断言明细 | [语义汇总](Derived/case-summary.json)、各运行目录的 probe.json 和 process.json |
| 固定种子规则检查 | [33 个规则断言](CompileRules1/rules.json) |
| 五区 NavMesh、真实移动、门和密室 | [Editor](RewardsEditor1/)、[非开发 Player](RewardsPlayer1/)，各有 path-corners 和 runtime-trace |
| 事件故障事务 | [Editor](FaultEditor2/)、[非开发 Player](FaultPlayer2/) |
| Boss 阶段切换、实际命中、实际躲避与普通掉落 | [Editor](BossEditor2/)、[非开发 Player](BossPlayer2/)、[时间实测](Derived/boss-timing.json) |
| 满包和跨进程领取、下一 Run 重新击杀 | [Editor](ResumeBossEditor2/)、[非开发 Player](ResumeBossPlayer2/) |
| 满包、首领以外的永久回执和退出 | [Editor](ResumeRewardsEditor2/)、[非开发 Player](ResumeRewardsPlayer2/) |
| 实际拆解、读取与新 Run 不补发 | [Editor](SalvageEditor4/)、[非开发 Player](SalvagePlayer4/) |
| 旧森林随机流及首领奖励受控测试 | [四组流检查](LegacyStreamsEditor/b3-stream-results.txt)、[两组经济检查](LegacyEconomyEditor/b07-economy.txt) |
| 旧三区在途 | [Editor](LegacyFrontierEditor2/)、[非开发 Player](LegacyFrontierPlayer2/) |
| 旧五区在途 | [非开发 Player](LegacyFivePlayer2/) |
| 石柱、远程软锁和近战有限面向 | [Editor](AssistEditor2/)、[非开发 Player](AssistPlayer2/) |
| 纯发行构建、实际 Bee、程序哈希、运行 | [构建清单](build-configuration.json)、[类型与 IL 审计](assembly-audit-r1.json)、[纯发行运行](PurePlayer1/pure-runtime.json) |
| 构建警告和构建产物 SHA256 | [警告与原始构建回执](Derived/)、[全包文件清单](build-files.json) |
| 保护哈希及隔离配置差异 | [保护核对](protection-final.json)、[输入差异](lab-input-differences.json) |
| 首次 Boss 失败 | [BossPlayer1](BossPlayer1/) |
| 七武器普攻、技能与牵引逐项结果 | [矩阵结果](Derived/weapon-matrix.json) |
| 首次武器矩阵失败 | [矩阵断言及失败](Derived/case-summary.json) |
| 真实源与发布副本逐项哈希 | [manifest](manifest.json) |

受控截图与正常产品代码运行证据分层。这里的脚本操作与后台关闭回执不作为独立人工或原生键鼠验收。
