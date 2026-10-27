# INPUT-01 失败与尝试历史

所有目录均在START_BASELINE.json所列工程外拥有者根下；不覆盖前轮输出，不删除失败，不用后续通过重命名旧结果。这里区分产品输入分支、测试夹具与环境，原始日志/源码快照见Evidence/Attempts。

1. **启动器路径错误**：尝试使用本机不存在的`C:/Program Files/PowerShell/7/pwsh.exe`；未启动编排或Unity。外层因未设置LASTEXITCODE返回0不能称PASS，留存launcher-first-failure.json；后改用当前进程实际PowerShell路径。早期两个只读检索命令分别有PowerShell花括号语法和rg参数错误，未执行产品/测试，不能算产品失败。
2. **InitialValidation**：规则24项通过；Input01Play在I03恢复焦点仍移动处失败。既有UI01Rules在首个E/H等待超时，其余独立回归、构建和正常AI继续；失败没有被编排器exit或后续步骤掩盖。未满足依赖的Resume记NOT_RUN。
3. **DirectedTrace**：保留相同I03断言和诊断，恢复焦点前后z从172.34062到172.43903，MoveDirection为前进、有效held=true，而Editor侧deviceHeld=false。屏障仅看调用时控件缓冲会漏掉上一有效按住快照，修复把该快照对应控制一并加入释放门禁；不调整移动数值或放宽位移断言。
4. **旧UI夹具门禁适配**：增加上下文/关闭帧保护后，原UI01夹具首次输入可能仍落在门禁帧。仅在设备与出征准备之后等待3个真实帧；保留全部原预期断言。注入Editor专用的合成焦点桥只为非原生测试设备、显式隔离启动生效，不激活桌面，不进入正式包。后续UI01Rules通过，初次超时保留。
5. **DirectedInput2/3**：默认鼠标攻击观测失败。保留单帧及扩展观测输出，不将其直接归因为原生鼠标产品失败。为消除测试进程中多设备的current竞争，在该隔离Editor的InputSystem中禁用已有键鼠设备，再创建测试设备；没有禁用Windows设备或其他程序输入。真实消费窗口连续采样，后续默认/自定义四武器输入通过；不冒称取得原生键鼠证据。
6. **DirectedInput4**：I03、捕获、取消、真实拾取通过，渡口断言读到旧`ExtractionConfig`快照的repaired=false而失败。实际检查点已记录`exit:ferry`修复和唯一回执。测试改为按相同出口ID读取当前权威Capture，未改渡口扣费或放宽经济断言；旧失败及当时源码保留。
7. **DirectedInput5**：规则24、输入67、新进程10项；是中间定向结果，不继承为最终冻结验收。完整走默认/自定义武器输入、设置、修复与标题继续。后续新增布局和保存失败UI断言另跑。
8. **06e3d04e首个完整受影响All**：完成规则、实际虚拟UI、既有回归、正常AI三进程、非开发构建及正式Player标题验证。收尾源码审计发现通用Esc屏障会抢先使相机Update返回；此项当时是源码发现，不伪称旧运行曾覆盖Esc释放。移除该通用屏障，保留设置/关闭帧门禁，增加相机真实消费断言。并完善管理鼠标快捷键与旧武器/目标文案；该All保留为历史，不冒称最终代码执行结果。
9. **最终f16bdcae冻结复验**：用新FinalFrozenValidation根重新执行本批受影响All，不拼接旧PASS。最终逐项结果、命令、退出码、超时和警告在REPORT/ACCEPTANCE及Evidence中，不靠编排器exit0推断全体验收。

## 环境与开放项

初轮Editor日志出现`ArgumentOutOfRangeException`，栈进入`UnityEditor.Search.SearchDatabase.EnumerateAll`、`GetDefaultSearchDatabase`及`SearchInit.IndexationOnStartup`。保存原栈，继续UNRESOLVED，不将其归为新输入代码异常或声明已解决。D3D12 UNKNOWN、Editor青色帧、JobTempAlloc根因同样不因新输入通过而关闭。

所有超时按原脚本诊断并保留进程，没有强杀用户或测试进程。原生U16/独立人工/完整性能未执行，不能以虚拟设备、截图或后台WM_CLOSE替代。源用户场景及ProjectSettings不覆盖、不提交；真实玩家存档不作为测试输入。

10. **只读构建报告辅助工具**：发布构建完成后，临时审计类第一次把int总数写入uint字段，CS0266退出1；修正辅助类后在新诊断目录成功读取同一报告。不是产品源码/原正式构建失败，没有改旧日志或计数。
11. **最终构建质量**：Succeeded但BuildReport有2 Error和91 Warning。两个Error都指向URP Core的TraceRenderingLayerMask.urtshader host-type不匹配；初始包导入还有USS/UXML/URT路径DirectoryNotFoundException。原文、栈、97条BuildReport消息保留。I14质量标UNRESOLVED，不归为输入缺陷，也不宣称已经证明无运行影响；不擅自修/升级/删包。
12. **隔离设置序列化**：源用户ProjectSettings原字节不变；Unity在隔离副本把两行中文改成等价引号Unicode转义。克隆哈希不同如实记录，不能宣称所有输入字节相同。用户场景副本原字节相同，31份产品源码规范化文本与冻结提交一致。
