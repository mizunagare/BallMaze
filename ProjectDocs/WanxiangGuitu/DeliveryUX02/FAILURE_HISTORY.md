# 失败与限制历史

- Before：15 PASS/12 FAIL；Before2扩展同机位对照：27 PASS/22 FAIL。失败包括仓库支付、当前容器显示、普通/精英/两种Boss死亡清理与已死恢复。原件保留，未把负例失败归为工具问题。
- After1：可用commit内存2.65GB低于原3GB门槛，NOT_RUN，无新Unity子进程；没有降低门槛。
- After2/After3：27/49项通过。原GameView截图有历史青色帧；后来增加受控RenderRequest层，不删除原图，不宣称青色帧根因解决。
- Regression/Combat01Checks.Run：batch mode中产品有意不自动初始化存档，旧驱动等待Saves.IsInitialized至专用240秒期限，exit1。最小Editor启动适配UX02BatchEntry只调用原InitializeStorage，原断言/伤害/冷却不变；CombatBatchFinal188项通过。
- Normal-Gather初次：未经协调器准备的重复Editor类导致CS0101/CS0111；编译失败关闭请求无有效桌面句柄，进程保留。没有业务完成或原生通过，不强杀。后续改用原Invoke-Regression协调器的非活动桌面和临时驱动准备，AffectedFinal三阶段实际完成。此失败进程/原始目录继续保留。
- 初版Invoke-UX02在同一PowerShell连续调用时可能继承先前LASTEXITCODE，导致外层打印exit1，即使其独立子进程JSON为0/PASS。已增加明确exit0，原始打印和子回执均保留，不回写旧结果。
- FinalRulesR2：正常AI结束清理临时类后，旧WGA1Check仍有typeof(WGNormalAICheck)引用，CS0246。仅在已退出的测试副本恢复Deferred三类，保留原副本与失败，后续R3/R4重新运行。
- Editor.Search完整调用栈仍为UnityEditor.Search.SearchDatabase/IndexationOnStartup内部异常；单列UNRESOLVED，不归因于产品代码。旧C15/D3D12 UNKNOWN/青色帧/JobTempAlloc/旧额外Editor阻塞均不关闭。

版本轮次和每项真实退出码、超时、日志路径以Evidence/FINAL_SUMMARY.json及独立attempt目录为准。后续PASS不替换早期FAIL。原生、人工和长期压力未执行，继续NOT_RUN。
