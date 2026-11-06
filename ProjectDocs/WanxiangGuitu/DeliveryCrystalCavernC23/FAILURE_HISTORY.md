# C2.3 失败历史

所有首次尝试在 I:/WGCombat/C23-1106-A 独立目录保留。C2.1/C2.2/C1 原始目录不变。

- 审计工具第一次尝试读取 WorldEventDirector.cs，发现该文件不存在（PowerShell exit 1）；已转向实际 WorldEventPoint 和现有 Events 入口。此为工具路径错误，非产品失败。
- Bake1：首次隔离导入与固定湖区烘焙已退出 0。原始 Unity 日志完整保留，不能以退出码代替路线验收。
- EditorLake1：首次完整导入与运行，最终断言与进程通过，原记录保留。
- PureBuild2：首次 C2.3 纯发行构建成功，0 错误 / 105 警告。目录命名保留原构建工具约定，不表示覆盖过一次本批构建。

历史保留：C1/R7 7 PASS / 1 FAIL / 2 NOT_RUN / 2 UNRESOLVED；严格像素失败、三个阶段指纹、GraphicsSettings 写回因果与发行语义等同性、JobTempAlloc。C2.2 原 8 条失败断言及工具失败继续保留。

- 首次连续 EditorLake1：断言已完成并写入 complete.txt；Editor 仍在 Cleanup mono 阶段。随后尝试启动 EditorLakeLive2 被占用保护拒绝（exit 1），没有启动第二个 Editor；不将退出尚未完成视作进程成功。该尝试保留于本轮工具记录。后续只在原进程退出后重试。

- Observed1：测试副本驱动缺少 UnityEngine.JSONSerializeModule 引用，C# 编译出现两条 CS0103。未改产品；补充编译引用后 Observed2 成功。原编译日志保留。
- EditorLakeLive2：启动停留在独立桌面的 Scene Backup Detected 对话框。只读窗口清单定位后，针对已核对 PID/Unity 路径/独立非输入桌面选择 Keep Backups；保留备份，没有删除用户内容、切换桌面或关闭程序。过程的第一次 PowerShell 线程 Attach 失败、.NET8 默认运行缺失失败也保留，之后使用现有 .NET 的 roll-forward 执行独立工具。该操作不算原生游戏验收。
- PlayerLake1：业务断言通过，但实机图确认顶盖露天空及方正湖岸，表现审核 FAIL。Bake3/PureBuild4 修正新湖区表现后，再发现湖口过渡边肩缺口；Bake5/PureBuild6 补齐新区域过渡墙。旧包和截图不删除、不改写。

- PlayerLegacy22Final：legacy-c22-original-prefab 首次 FAIL。前两项完整版本/实体检查通过；错误断言预期根对象名以 C2.2 开头，而历史固定 Prefab 序列化的根名称实际为 Cavern（原文件第2626行），Unity 按资产名保存。修订工具为精确资源映射、实际克隆名称、地面/阻挡数量、每块地面的名称/位置/尺寸/材质引用比对；不修改旧产品资源，不放宽版本或身份条件，原 FAIL 保留。

- EditorLegacy22Final：同一个工具断言也在 Editor 产生 FAIL / 进程 exit 1。两个原失败均进入 Evidence/runs.json 与 Raw，不以 Verified 重跑覆盖。
- ObservedFault：新增导航故障工具错误地把 WorldEventPoint 传给要求 InteractionOffer 的 API，编译出现 3 条 CS1503。该副本未运行，源快照与原日志保留；ObservedFault2 使用现有 WorldEventPoint.Interact 业务入口后编译成功。未修改产品来适配工具。
- 调查中曾读取不存在的 Tools/Editor.cs.txt 和 PureBoot6/process.json，均为工具路径错误；实际 Editor 入口在 Driver.cs.txt 的 UNITY_EDITOR 条件段，纯包回执为 pure-runtime.json，未据缺失文件推断成功。
- 导航负例会产生预期产品错误日志“洞窟路线、矿室门或免费出口的导航状态不符”。这是真实重建校验拒绝，不过滤日志、不伪装没有异常；用例判定要求拒绝、闭门、旧导航可返回且合法重试成功。

完整日志见 Evidence/Logs.zip 与 log-archive.json；首轮表现截图见 Raw/PlayerLake1，第二轮见 Final 目录，最终见 Verified/Audited。历史目录不修改。

- 最终归档第一次调用PATH中的python.exe落到WindowsApps占位程序（exit1，无输出），没有生成汇总。随后使用已有Codex运行时的Python绝对路径成功。没有安装/升级依赖，原始测试结果未改。
- 首次 git add 因本工作树 sparse-checkout 不包含新交付目录而拒绝（exit1）。使用 --sparse 显式加入本批新目录，不修改稀疏规则或历史文件。
- Git暂存后的全文件whitespace检查返回2：原始CRLF回执、日志及Unity生成YAML空字段尾空格触发格式诊断。未为消除格式提示重写原始证据或已构建资源。仅产品源码/工具/Markdown的检查返回0，记录见Evidence/staged-code-doc-check.txt；资源检查原输出也保留。
