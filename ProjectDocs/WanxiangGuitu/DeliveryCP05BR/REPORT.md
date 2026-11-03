# CP05-BR：Player可见性与性能专项

开始基准：`b27bda440201937a01a3add69311d3f982789194`。独立分支 `verify/cp05-player-visual-performance`，不合并main，不改变原型分支。最终SHA为本报告所在提交，由交付消息及远端核对确定。

本批修复的是**验证工具的启动/视觉判定条件**，没有修改产品Assets、评分/滞回、CombatAim、剑枪转角、战斗参数或存档。已取得可验证的非开发Player真实训练画面；Editor及非开发Player均获得正/零校准有效的分配数据。但**不能宣称整体可发布或人工体验通过**：另外观察到两项训练场产品缺陷，按冻结边界只交提案，未修复。

## 主要结论

1. 历史运行器 `StartChild(...,$false)` 使用独立桌面的 **SW_HIDE**。同一B3验收二进制及原截图代码，改为已有Worker支持的 **SW_SHOWNOACTIVATE** 后，71/71帧正常。新的同包隐藏对照8/8黑；诊断包进一步得到隐藏7/7黑、相机回调0，对应显示D3D12/D3D11各7/7正常、相机回调持续增长。并非由READY、焦点或进程exit0推导画面。详见 [PLAYER_RENDER_AUDIT](PLAYER_RENDER_AUDIT.md)。
2. 新运行器默认在**不活动测试桌面显示窗口**，不切换桌面或抢焦点；隐藏只能显式负例控制。视觉回执检查实际窗口、相机、回调、完整PNG和进程退出。隐藏负例仍报告FAIL/1，必要证据缺失INCOMPLETE/3，不自动改PASS。
3. 最终Editor **1,116**条采样；PlayerFinal **2,172**、独立重复 **2,215**，带最终门禁的PlayerGated **2,223**条。各进程24条校准均有效；六类负载覆盖通过。Editor的472个查询作用域与Unity Profiler原始GC metadata逐条一致。数字是采样数量，**不是游戏功能PASS数量**。
4. 原B3完整API矩阵在显示条件重跑：**157 PASS / 0 FAIL / 1 NOT_RUN**。历史无效线程GC计数的NOT_RUN保留；本批使用另一条经过校准的原生Mono profiler路径，不改写旧结果。
5. 新纯发行包构建 **0错误、96条BuildReport警告**，另有Editor退出JobTempAlloc诊断未解决。固定PRIVACY-A Profile、Development=false、Bee五服务false。无本批驱动或分配桥引用；八类关键产品类型与最终验收包IL一致。纯包启动/普通关闭实际exit0，未进行自动战斗/人工操作。

## 成果与边界

- [PERFORMANCE](PERFORMANCE.md)：六模式、真实物理查询、材料数组/实例、扫描缓存、逐方法数据和等待授权的优化方向。未修改产品以迁就采样。
- [PRODUCT_FINDINGS](PRODUCT_FINDINGS.md)：第二次训练重开场景重名；训练敌人死亡时缺少CombatSession导致掉落空引用。均有实际Editor堆栈，未推断所有正式森林路径同样失败。
- [PLAYER_PLAYTEST_GUIDE](PLAYER_PLAYTEST_GUIDE.md)：纯包路径、完整文件SHA、启动及四武器/自由辅助对照检查表，人工记录空白。
- [ACCEPTANCE](ACCEPTANCE.md)、[FAILURE_HISTORY](FAILURE_HISTORY.md)、[Evidence/INDEX](Evidence/INDEX.md)。所有早期工具失败、未充分负载、黑帧和原始报告保留。

源/用户工程开工2,347项保护文件全部未变；原CP05B历史文档和证据无diff。CombatAim SHA仍为 `9f5d9b7d8c1c39b7270839217562033b6425e2af2d357df51e1269558c4e346a`。[保护核验](Evidence/protection-final-2.json)也记录隔离副本的5项Unity序列化写回，不把它们宣称为逐字节输入等同，更没有回写用户ProjectSettings。

纯包：`I:/WGCombat/CP05BR-1103-A/PureBuild/Release`。exe SHA256 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`；Assembly-CSharp SHA256 `c7e9155d9440193ee206099a1de984af66515f7e49b7138d869cb90315d3d6bf`。[全部产物哈希](Evidence/release-files.json)。exe是Unity启动stub，单独相同不证明整个版本相同，必须同时核对程序集与全部清单。

**未执行/未关闭**：原生物理键鼠、独立人工试玩、纯包外部屏幕采集、长期森林/首领性能、整帧及GPU预算；旧D3D12 UNKNOWN/青色帧/Editor.Search/历史关闭根因不因本批关闭。一般窗口截图工具初始化失败已记录；运行时自己的窗口只读状态和真实Frame为本次替代证据。推送后暂停等待独立复审及产品修复授权。
