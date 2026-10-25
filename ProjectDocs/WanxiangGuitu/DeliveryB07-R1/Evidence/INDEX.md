# B07-R1 证据索引

## 最终新的完整 All

- [逐项命令、时刻、退出码、超时与状态](FinalAll/results.json)、[CSV](FinalAll/results.csv)、[统计](FinalAll/counts.json)。协调器exit0不等于全部验收通过；两个标准负探针保留FAIL。
- [实际收益、15个正常AI与12个Player进程摘要](FinalAll/review-summary.json)。以实际执行完整时的数据为准，缺项不补PASS。
- [冻结输入证明](FinalAll/frozen-product-proof.json)、[源工程/隔离副本/构建输入哈希](FinalAll/Provenance/source-build-provenance.json)、[构建文件哈希](FinalAll/build-manifest.json)、[构建摘要](FinalAll/build-summary.json)。
- [R1渲染与生命周期断言](FinalAll/Readability/Rules/b07r1-live.txt)、[几何对照](FinalAll/Readability/Rules/b07r1-geometry.csv)、[布局矩形](FinalAll/Readability/Rules/b07r1-layout.csv)、[像素检查](FinalAll/Readability/Rules/b07r1-pixels.csv)、[稳定帧记录](FinalAll/Readability/Rules/b07r1-render-ready.csv)。
- [38张攻击与2张遮挡对照截图清单](FinalAll/readability-screens.json)，图片在ReadabilityScreens；停用NPC的受控实际相机渲染，不是正常AI、原生UI或人工试玩。
- [R1完整日志](FinalAll/ReadabilityLogs/logs-redacted.zip)、[B07完整日志](FinalAll/B07Logs/logs-redacted.zip)、[全部规则与构建日志](FinalAll/Logs/logs-redacted.zip)。日志只脱敏/规范编码，不删除错误。

## 正常 AI 与真实战斗

- 陆地：[流程](FinalAll/B4Diagnostics/Normal-Land/normal-results.txt)、[行走/生命/物资轨迹](FinalAll/B4Diagnostics/Normal-Land/normal-ai.csv)、[首领状态](FinalAll/B07Diagnostics/Normal-Land/boss-world.csv)。
- 湖中：[流程](FinalAll/B4Diagnostics/Normal-Lake/normal-results.txt)、[行走/生命/物资轨迹](FinalAll/B4Diagnostics/Normal-Lake/normal-ai.csv)、[首领状态](FinalAll/B07Diagnostics/Normal-Lake/boss-world.csv)。
- [正常AI截图清单](FinalAll/b4-screens.json)，图片在Screens/Normal-Land与Screens/Normal-Lake。角色与怪物照常行动；领域机器人，不是人工或最终Player原生战斗。
- [18个真实命中/闪避/越界子例](FinalAll/combat-case-results.csv)、[原始伤害记录](FinalAll/B07Diagnostics/Rules/b07-hits.csv)、[逐攻击中断和恢复时钟](FinalAll/B07Diagnostics/Rules/b07-interrupts.csv)。这是受控规则，不能代替正常AI。
- 正式Player的B07Diagnostics/B07-Land与B07-Lake、Default/D3D11各cell保存完整Player日志、process、analysis、timeline和storage-audit。后台关闭路径不替代真实标题栏。

## 修复前与失败历史

- [修复前两张B07正常AI截图及来源](Before/screens.json)、[固定提交源码](Before/Sources)。来自91c6664，不声称本轮重跑。
- [本轮实施前失败探针](Attempts/Before/Readability/Rules/b07r1-probe.txt)、[旧80个产品脚本核对](Attempts/Before/frozen-product-proof.json)、[新探针独立来源](Attempts/Before/probe-origin.json)。
- [各轮尝试和失败解释](../FAILURE_HISTORY.md)。Attempts内每个目录保留独立results、命令、退出码、原始日志、PNG和可取得的输入快照；后续PASS不覆盖首次FAIL。
- [青色像素首次FAIL](Checks/cyan-before.json)、[证据相对路径检查首次FAIL](Checks/attempts.json)、[修正后PASS](Checks/attempts2.json)。图片字节未变，Before/screens-before-fix.json保留原清单。
- UI01历史65/2/20/1、原生U16与人工理解NOT_RUN、D3D12 UNKNOWN UNRESOLVED仍保留；新增Editor首帧诊断单列，不混为同一根因。

仓库不上传原始存档、ground-loot页、凭据、Library、Temp、构建二进制或dump。所有断言使用合成存档，发布日志记录原始/发布哈希及脱敏策略。

## 透明遮挡与遗漏保留

- [All1自动结果](Attempts/All1/results.json)及[正常聚怪照片复核FAIL](Attempts/All1/Readability/b07r1-visual-review.json)分别保留，不能把exit0当验收通过。
- [受控淡化开关对照](Attempts/OcclusionFinal/readability-screens.json)、[实际Renderer/状态断言](Attempts/OcclusionFinal/Readability/Rules/b07r1-occlusion.txt)。
- 最终All的同类证据在ReadabilityScreens/b07r1-occlusion-controlled-off.png与on.png、Readability/Rules/b07r1-occlusion.txt；最终正常AI截图仍单独存放Screens/Normal-Land和Normal-Lake。

## 最终封存补充

- [真实协调器退出](FinalAll/coordinator-exit.json)、[代表性截图代理复核](FinalAll/visual-review.json)。
- [用户输入保护哈希](FinalAll/user-input-proof.json)、[正式程序集组件/Editor入口检查](FinalAll/release-hud-check.json)。
- [59处Editor.Search异常](FinalAll/exception-inventory.json)、[完整构建warning标记行](FinalAll/build-warning-lines.json)。
- [最终发布字节、压缩包与哈希检查](Checks/final.json)、[Git暂存字节检查](Checks/staged-bytes.json)。这些后处理检查不计入游戏120个PASS。

最终完整All：120 PASS、2预期负探针FAIL、27 NOT_RUN、2 UNRESOLVED、0非预期FAIL。15正常AI、12正式Player、40专项截图；正式构建0错误77警告。原生与人工事项保持开放，推送不代表复审通过。
