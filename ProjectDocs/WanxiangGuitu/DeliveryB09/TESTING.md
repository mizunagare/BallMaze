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

## 本轮固定输入与后处理

最终运行目录：`D:/WanxiangValidationRuns/B09DisplayVerified/20261026-001243-cd1430ec`。
最终完整运行输入提交：`6ec68a88bc171af1c7e5926642b17899ab20f8ec`（产品 C# 仍与 b432ac0 一致，后续仅修正测试捕获）；之后只新增报告、证据与索引。最终交付提交 SHA 以推送后远端核对为准，不用报告自引用猜测 SHA。

完全退出后再发布本轮证据；以下 Python 命令均使用本机既有 Python，`<repo>` 为本工程绝对路径，`<run>` 为上述已结束的唯一运行根，`<target>` 为仓库内新的 Evidence/FinalAll：

```text
python -B DeliveryB09/Publish-Evidence.py --run <run> --target <target>
python -B DeliveryB09/Summarize-Evidence.py --run <run> --output <target>/b09-summary.json
python -B DeliveryB07/Seal-Evidence.py --project <repo> --run <run> --target <target> --commit 6ec68a88bc171af1c7e5926642b17899ab20f8ec
python -B DeliveryB4/Provenance.py --project <repo> --run <run> --target <target>
python -B DeliveryB09/Audit-Release.py --project <repo> --run <run> --target <target> --baseline c401dfbe6da944d980ae5045c7b52a09fd65193c
```

路径在命令中应展开为 `ProjectDocs/WanxiangGuitu/` 下的实际脚本全路径；输出必须为新目录。发布器只上传白名单日志、结果、审计摘要、源码指纹和截图；合成 save.json、分页、完整事务候选、构建二进制与 Library 均保留在测试根，不上传。发布的preferences数值试件与新游戏journal仅为显式合成设置/事务元数据，不是真实玩家设置或财产存档。

原始 `results.json` 的2个 FAIL 是已声明的编排非零/超时负探针；检查 `unexpectedFailures`，不能只看总 exit0。入口拒绝进程的预期退出码2也单列，不当作正常游戏退出。退出码0仍须结合无超时、完整 Player 日志、退出审计及修订核对；后台 WM_CLOSE 不证明标题栏鼠标路径。

旧版兼容分别由 B05LegacyMigrationCheck、B05V7MigrationCheck、B06V8MigrationCheck、WGLegacyForestCheck、B07/B08恢复与 B09Rules/Cases 覆盖；只读目录检查不会执行迁移。v1～v6列表检查与真正旧档加载回归不能混为一项。

完整 All 的截图资源检查不通过会跳过该步骤并保留 NOT_RUN，不通过缩小图片、强杀进程或关闭用户程序伪造完整运行。测试使用已有 Shader 缓存，源工程没有 Library导入/Shader重编译全清验收。

正式标题捕获显式使用 SW_SHOWNOACTIVATE，仅在未激活的 WGTest_ 测试桌面内显示；既不 SwitchDesktop，也不发送输入。默认其他工具仍 SW_HIDE。严格验证同时排除全黑/低变化空白与青色帧；需要实际复核PNG。历史黑帧不得作为可见菜单证据。改变捕获模式不使原生U16可用，也不是 D3D12 或 Editor 青色帧修复。
