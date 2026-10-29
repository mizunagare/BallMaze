# 失败历史（各轮原始目录独立保留）

- Before：提交内存2.04GB低于原3GB门槛，未启动Unity，NOT_RUN；未降门槛，用户自行释放后才继续。
- Before02：同目标revision1→2、配方滚动300→0、白剑真实产物出现但目标不结束、教程仍Withdraw、抓取旋转错误；均为修复前失败。短暂轮廓首次采集太晚，没有捕获到，不能据此断言几何。
- Before03：按实际release帧采集；真实攻击接受、资源非Overlap候选、HP70保持；旧地面轮廓1.800011而真实球截面1.547126。保留全部候选与顶点证据。
- After01：首组10项通过，尚不代表跨进程通过。
- Matrix01：58失败/406通过。4条制造追踪失败涉及恢复后的null/空串标识不一致；其余大部分命中失败为夹具使用前次LastReleaseFrame提前读取HP。保留原始结果，修正夹具按本次输入帧等待，不修改产品伤害/释放时间。
- Matrix02：464通过；Resume02两项失败，暴露null目标经Unity内联序列化重新出现，以及同一测试存档被后续几何Run合法写入，不能拿营地快照比较在途状态。
- Matrix03：加入实心墙对照461通过；Resume03剩余状态差异由几何验证覆盖同一存储根引起。改为GeometryStore独立合成档，不篡改旧存档或预期文件。
- Matrix04/Resume04：461/3通过；新Profile默认目标的独立round-trip补测后，再冻结最终输入执行Target05/Matrix05/Resume05。旧结果不删除、不改写。

完整日志中的Editor.Search内部索引异常独立保留，不归咎于产品；历史UNKNOWN、青色帧、Search、JobTempAlloc、旧C15根因继续UNRESOLVED。原生U16、独立人工和性能不因本批受控验证而关闭。

## 最后补充的真实失败（不覆盖前面的尝试）

- CombatTiming（原COMBAT01）：batch等待默认存档初始化，240秒夹具deadline后exit1，无工具强杀。原文件和日志未修改；新UX04适配显式初始化隔离档，并以现有Spear BasicPower（125%）作为单次命中精确期望，不能重新用未乘系数的旧断言要求产品回退。
- 原Normal-Gather/Resume：身份核对通过后phase31停滞，活动时间1.64，有界驱动exit1；FinalResume依赖项NOT_RUN。没有强改时间或结算。根因仍未确认。后续Final2、Final3独立Run三进程完整通过，不抹去它。
- Final2/CombatTiming：原始错误 `Fatal Error! d3d12: Unrecoverable GPU device error`，实际exit -1073740771、无超时/强杀，完整原生栈和预算上下文保留。不能归因于产品，也不能把去除非必需batch GameView后的188条PASS说成GPU根因修复。
- Final2/Matrix06：主要461条通过；追加在途制造夹具沿用了测试主动SuspendEntry造成的门禁，后续新档初始化仍阻塞，出现6个FAIL（含夹具NullReference）。没有因此更改产品初始化/恢复门禁。改用独立GeometryStore、保持受控测试保存入口就绪，在Shared07实际Run中5项追加检查通过；恢复两项另一个进程通过。
- Final3/Scroll：16PASS/1FAIL。夹具用SetOpen(false)关闭营地面板，但产品合同明确要求先走Camp.Explore（真实关闭按钮入口）。未改变产品门禁；Scroll08调用该真实入口并记录具体HUD文字，17PASS。

各轮命令、输出、exit、timedOut与实际结果独立保留；后续包装器复制了执行源。首次修复前夹具没有单独的源码字节冻结，不能补造这一记录。状态总览分开统计当前断言、历史包装器执行和正常AI进程，不把不同计量单位相加。新异常和历史引擎开放项维持UNRESOLVED。
