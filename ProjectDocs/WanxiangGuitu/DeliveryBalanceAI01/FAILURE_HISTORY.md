# 失败、输入修订与未解决项

原始外部根 `I:/WGCombat/BAL01-1029-A`；公开副本按Evidence索引。原日志保留，日志压缩/凭据脱敏后保留源SHA256与公开SHA256。不覆盖旧批次。

| 尝试 | 实际结果 | 后续与边界 |
|---|---|---|
| Before | 编译exit1，另异常守卫FAIL | 测试使用Unity6.5已禁用GetInstanceID；改为HashSet对象跟踪，不是产品编译缺陷。原模板/日志留存 |
| Before02 | exit1，5P5F | 背后命中/远程近身/同步/隔墙/恢复负例；非预期游戏成功 |
| Before03 | exit1，5P8F | 增加软暂停余量、死主人弹体、全局暂停推进负例；后续13P不回写 |
| MatrixBefore | exit0，108行 | ResetEnemy的.8秒武装延迟使近身样本难解释；保留探索数据 |
| MatrixBeforeWarm | exit0，108行 | 加2.12秒预热；但Flow关闭后用旧全局随机，未逐样本固定，不用于严格配对 |
| Rules | NOT_RUN/exit=null/未超时 | 2.65GB可用提交内存<3GB，未启动Unity；随后观察一度.25GB，不杀用户程序/不改虚拟内存；用户释放后唯一一次重试 |
| RulesRetry/RulesResume | exit0，47+4P | v9与生命周期实际测试，不将此前NOT_RUN改成PASS |
| MatrixBeforeFrozen/AfterFrozen | 各exit0、108行 | 完整记录初始字段匹配；复查发现WrongDodge只读普通WindingUp，Boss未实际翻滚。该轮保留，不作为完整Boss错时覆盖 |
| MatrixBeforeFinal/AfterFinal | 各exit0、108行 | 只改测试对Boss.State的读取，加入实际Boss错时翻滚。前后使用同一模板/种子/全局状态，最终CSV来自此轮 |
| Final/UX02Regression | Unity exit -1073741819，外层exit1 | 我给需要Camera渲染的夹具错误加了-nographics；RenderTexture.Create失败后发生原生崩溃，完整栈在日志；同一启动日志的Editor.Search另列开放 |
| UX02GraphicsRetry | exit0，60P | 去掉不兼容参数，未改断言/产品；首次Final序列仍exit1。没有宣称底层引擎崩溃根因已解决 |
| 输入绑定初次 | source-bindings-working-input-failure.json为FAIL | 原准备脚本复制工作场景，非Git场景。其SHA确等开工用户场景，并非源文件被覆盖；原失败保留 |
| TrackedReplay / TrackedFinal | 13+47+4P、正常AI三进程exit0、0E96W构建 | 仅隔离副本写入已提交场景/设置，移走复制的Recovery；源码110文件和实际构建输入最终绑定PASS，用户5文件不变 |
| 发布完整性首检 | FAIL，10个合成save.json.tmp未暂存 | Git忽略规则跳过故障夹具临时文件；首检JSON保留为publication-check-first-fail.json，仅显式加入这10个已在清单中的隔离合成文件后复检1652条全部通过。此发布检查不混入34条Unity启动Step统计 |

所有过程没有强杀或伪称超时为正常结束。本轮各实际Unity进程均已退出；用户Unity Hub等原程序未关闭。已确认并修正的是夹具/输入配置；原生崩溃的引擎内部根因没有凭一次成功猜测关闭。

历史D3D12 UNKNOWN、青色帧、Editor.Search、JobTempAlloc、旧C15、UX04 GPU fatal和首次AI停滞继续开放。原生U16、独立人工与最终平衡/性能未执行。不将受控截图、领域断言或Editor输入机器人作为人工通过。
