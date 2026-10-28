# 失败与边界

- UX02两轮修复前失败及COMBAT01/R1旧C15完整保留在原目录，未继承为本轮PASS。
- 本批基线与每次运行使用不同输出目录；Before/BeforeBoundary和After/AfterBoundary全部原始网格保留，包括未命中、帧波动和冷启动约.33s的释放样本。未删除离群值。
- 首次调用误用了不存在的C:/Program Files/PowerShell/7/pwsh.exe，外层exit1，没有启动该次Unity；改用宿主实际pwsh。随后After实际进程exit0。不是游戏失败，也不改写首次命令错误。
- LegacyOriginal：187 PASS/1 FAIL，原断言multi collider single basic hit 1：expected33 actual41.25，子进程exit1。是明确参数实验导致的旧预期不再适用，保留结果；仅把普攻预期替换为combat.BasicPower后LegacyAdapted 188 PASS，原历史测试文件没有改。
- UI01 D3D12 UNKNOWN、旧C15、Editor青色帧、Editor.Search、JobTempAlloc、旧Editor启动阻塞继续UNRESOLVED。未做无新线索关闭实验或改生命周期。受控图不证明这些问题已解决。
- 原生U16、独立人工理解与试玩、完整性能预算继续NOT_RUN。不把本批受控伤害、启用敌AI短战、Editor森林AI或构建通过替代它们。

- 首次附加B07Rules.Run在40 seed导航后，读取原出征的Single查找Boss失败。原清单仍启动三个依赖进程，均因缺少b07-expected.txt失败；四次exit1保留，不当作四个独立产品缺陷。重跑清单已加入依赖门控。后续诊断另建目录。

- 后续仅增加只读Dump的第二个新Run通过四阶段；新Run身份/种子不同，未取得首次出错瞬间状态，不能据此确定根因或关闭首次失败。新增U07保留，未做试探产品恢复改动。
- 一次文档作者工具使用系统默认GBK读取UTF8失败（UnicodeDecodeError），改为显式UTF8；该命令外层后续输出曾返回0，未把外层0计作测试通过。没有产品Unity测试因此通过或失败。
