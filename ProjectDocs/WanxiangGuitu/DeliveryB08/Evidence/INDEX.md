# B08 证据索引

最终结果以FinalAll及验收表为准；旧尝试与All1分别封存，不继承PASS。不上传save.json、ground-loot、构建二进制、Library、Temp或凭据。

## 最终新All

- [完整结果JSON](FinalAll/results.json) / [CSV](FinalAll/results.csv) / [逐项报告](FinalAll/REPORT.md)：命令、UTC区间、真实退出码、超时和范围。
- [汇总](FinalAll/review-summary.json)：18正常AI进程与14正式Player进程的独立明细；实际数量以文件为准，不把机器人当原生输入。
- [产品与执行源码](FinalAll/frozen-product-proof.json)、[源码/构建输入](FinalAll/source-build-provenance.json)、[构建文件哈希](FinalAll/build-manifest.json)。原场景按用户工作字节进入副本，不能宣称等于干净Git场景。
- [构建摘要](FinalAll/build-summary.json)、[完整warning标记行](FinalAll/build-warning-lines.json)、[正式包元数据](FinalAll/release-onboarding-check.json)、[用户文件保护](FinalAll/user-input-proof.json)。元数据检查不是原生操作验收。
- [异常起始行](FinalAll/exception-inventory.json)与[故障夹具附加分类](FinalAll/b08-exception-annotations.json)：原日志不删除，未知来源不猜测。完整规则/构建日志在[归档](FinalAll/Logs/logs-redacted.zip)，B08专项另有[B08Logs](FinalAll/B08Logs/logs-redacted.zip)。
- [B08规则](FinalAll/B08Diagnostics/Rules/b08-rules.txt)、[营地时钟](FinalAll/B08Diagnostics/Rules/b08-camp-clock.json)、[40显示夹具](FinalAll/B08Diagnostics/Rules/b08-visual.txt)、[PNG尺寸/哈希](FinalAll/b08-screens.json)。停用NPC的显示夹具不是真实输入或人工试玩。
- [代表性截图复核](FinalAll/visual-review.json)：代理读图，不是独立人工可理解性验收；帮助首屏为可滚动裁切，旧IMGUI缩放未重构。
- [首次正常教学轨迹](FinalAll/B08Diagnostics/Normal-Tutorial/b08-normal-ai.csv)、[真实攻击资源记录](FinalAll/B08Diagnostics/Normal-Tutorial/b08-attacks.csv)、[流程日志](FinalAll/B4Diagnostics/Normal-Tutorial/normal-results.txt)、[实际结算摘要](FinalAll/SettlementSummaries/Normal-Tutorial.json)。不发布完整提交计划。
- [在途快照](FinalAll/B08Diagnostics/Normal-Tutorial/b08-checkpoint-1.json)、[后继森林](FinalAll/B08Diagnostics/Normal-Tutorial/b08-checkpoint-2.json)、[新进程继续](FinalAll/B08Diagnostics/Normal-Tutorial/b08-checkpoint-3.json)、[保存定位审计](FinalAll/B4Diagnostics/Normal-Tutorial/storage-audit.jsonl)。均为派生断言，不是玩家存档封装。
- [正式Player首进程断言](FinalAll/B08Diagnostics/B08-Tutorial/b08-analysis-1.json)、[次进程断言](FinalAll/B08Diagnostics/B08-Tutorial/b08-analysis-2.json)、[退出/保存定位审计](FinalAll/B08Diagnostics/B08-Tutorial/storage-audit.jsonl)、[协调器退出观察](FinalAll/coordinator-exit.json)。关闭方法是后台WM_CLOSE，不能替代标题栏或原生U16。

## 失败和先前尝试

- [逐轮解释](../FAILURE_HISTORY.md)、[最早八次尝试](History/attempts.json)。日志脱敏前后哈希各自保留；来源不是相同字节时不能混称。
- [最初缺失契约](History/Before/results.json)、[84份基线源码](History/Before/frozen-product-proof.json)。旧档默认值、发布后核对、低帧率移动、GC/CLR及标签边界失败均各有目录。
- [All1完整结果](All1/results.json)、[All1封存输入](All1/frozen-product-proof.json)、[替代原因](All1/run-disposition.json)：没有营地时钟新断言，不能作为最后产品的验收。
- [时钟夹具入口错误](ClockEntryFailure/results.json)、[旧产品真实失败](ClockBefore/B08Diagnostics/Rules/b08-camp-clock.json)、[修复后通过](ClockAfter/B08Diagnostics/Rules/b08-camp-clock.json)、[共同测试源码与数据核对](clock-input-proof.json)。旧产品印证4d48，修复后印证c7ae；之前的夹具超时不当作产品失败。
- [临时调度包装源码](Support/manifest.json)复用同一Step与既有入口；正常复跑使用仓库内TESTING说明，不另建CI或框架。
- [发布字节/允许列表检查](Checks/final-publication.json)与[最终暂存检查](Checks/staged-bytes-final.json)属于发布工具检查，不计入游戏PASS数量；首次顺序错误和原始证据空白检查均单独保留。

## 读取边界

PNG来自实际Unity运行。B08Screens为受控夹具；Screens/Normal-*为正常NPC与领域机器人；最终Player仅启动/后台关闭/保存继续。任何一类都不能替代原生UI或独立人工理解。入口撤离青色立柱在部分照片中遮住角色，未改其几何；40%纯青帧阈值不是全画面无遮挡证明。既有Editor青色帧原因与D3D12 UNKNOWN各自UNRESOLVED。

最终完整SHA由所在Git提交及交付消息给出。交付不等于复审通过，结束后暂停，不自动启动下一批。
