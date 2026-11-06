# 失败历史

- Bake1 复用运行器时继承的 Assets/Editor 目录不存在，在启动 Unity 前失败。Bake2 隔离烘焙实际退出 0。[Bake1](Evidence/Bake1/) · [Bake2](Evidence/Bake2/)
- EditorStart1 用批处理进入正式启动。CombatSaveSystem 的运行时启动有既有 batch guard，game-ready 超时。改用私有桌面的非批处理 Editor，保留首次运行及 Editor.Search 启动异常。[第一次](Evidence/EditorStart1/) · [第二次](Evidence/EditorStart2/)
- 首轮纯包构建的桌面宿主先退出 -1。核对实际 Editor PID 后，Unity 完成构建并实际退出 0。最终构建的宿主与实际进程均为 0。历史 JobTempAlloc 或引擎警告按原日志留存。[首次构建](Evidence/PureBuild1/) · [最终构建](Evidence/PureBuild2/)
- 首次外部 Player 验证程序集编译缺少 UnityEngine.ScriptingModule。补充该引用后，新副本测试实际运行。[原始编译失败](Evidence/player-driver-first-failure.log.gz)
- 第一轮 Editor 和 Player 巨剑技能请求发生在普攻收招期间并按现有规则被拒绝。测试改为等待真实收招后再试，战斗时序未改动。[Editor 原始 FAIL](Evidence/Editor-weapons/) · [Player 原始 FAIL](Evidence/Player-weapons/) · [最终 Player](Evidence/PlayerFinal-weapons/)
- 第一轮实机截图暴露 HUD 中的字面换行符。首轮材质的自发光关键字在隔离构建导入时被移除。修正换行，统一相位只用基色，重建并在最终 Player 复核。[首次画面](Evidence/Player-start/04-warning.png) · [最终画面](Evidence/PlayerFinal-start/04-warning.png) · [最终包材质](Evidence/Audit/packaged-cavern-materials.json)
- C1 历史 FAIL、NOT_RUN 与 UNRESOLVED 状态保留。[C1 检查点](C1_INTERNAL_CHECKPOINT.md)
\
- 首次 Git 空白检查标出 Unity 写入的空 YAML 值后的空格。保留已经构建验证的资源字节，代码和文档继续执行空白检查。
