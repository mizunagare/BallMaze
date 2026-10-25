# B09 本地复跑

沿用 DeliveryUI01/Automation/Invoke-LocalValidation.ps1；新批次参数 `-B09` 蕴含 B08/B07/B4。所有参数使用绝对工程外根。完整运行：

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 -SourceProject D:/unity/WanxiangGuitu -TestRoot D:/WanxiangValidationRuns/B09ReleaseAll -B09 -FullRegression -GameplayOnly -ShaderCacheSource <已结束、同版本测试副本的绝对 Project 路径>
```

`GameplayOnly` 不重做没有新因果线索的 D3D12 关闭诊断；仍执行全规则、正常 AI、正式构建、B09 正式标题启动，以及 D3D11 隔离恢复冒烟。ShaderCache 只在来源已退出且引擎版本一致时复制，不宣称干净 Shader 编译。

定向检查复用 DeliveryB4/Invoke-Directed.ps1，Methods 为 B09Probe.Run、B09Rules.Run/Resume/Interrupt/Recover、B09Visual.Run；NormalStrategies Entry 复用正常 AI 脚本。

## 严格分类

- B09Rules：批处理 Play 的领域规则与事务故障注入。
- B09Visual：实际 Unity 渲染与 uGUI 回调，受控移动、受伤和死亡姿态；不是键鼠/人工。
- normal-ai.Entry：从真实 Title 场景经真实按钮回调进入游戏，原正常 NPC AI 保留，采集、拾取、撤离、结算、入仓、取材、制造和再次森林出征，三进程精确恢复断言。
- B09-Title：最终非开发 Player 不带测试跳过参数，实际 Title 启动；观察截图与目录状态，后台 WM_CLOSE，不是原生标题栏鼠标。
- B09-Entry Player：显式受控 gameplay 参数继续正常 AI 合成集合，严格核对保存和新进程恢复，不冒充正式菜单鼠标点击。
- 原生 U16、菜单原生键鼠、人工可理解性仍 NOT_RUN。UNKNOWN 与 Editor 青色帧根因 UNRESOLVED。

测试不激活私有桌面，不向用户桌面输入，不改系统快捷键，不强杀超时进程；超时保留进程并阻断依赖任务。保留每次命令、退出码、超时、日志、构建清单及错误历史。自动报告 exit0 不等于全部通过。

资源检查：`-MinimumUnityCommitGB` 默认3。每个 Unity 启动前写 `*.resources-before.json`，截图/构建/正常 AI 再加2GB余量；不足记 NOT_RUN 并保留指标，不触碰用户程序或页面文件。这是防护门槛，不是崩溃根因证明，最终 All 不能继承首轮成功。

`-wanxiang-test-gameplay` 与仅诊断用 `-wanxiang-entry-evidence` 都要求有效的启动前隔离根。Runtime BeforeSceneLoad 共用校验器先拒绝，再禁止标题初始化；Player 退出码2，Editor不关闭编辑器。负向参数用纯解析测试验证，不实际启动可能落入真实目录的无根进程；正式正向 Player 测试均有显式根。

最终 Player 额外验证两个带显式 relative 根的入口（截图/测试 gameplay）在场景前以预期退出码2拒绝，保留完整日志与进程回执。它们不计作正常游戏退出。相对根在原解析器中也会先于默认目录构造失败；不启动真正缺根的负向 Player，避免回归时接触真实目录。
