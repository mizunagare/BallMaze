# UX-05 测试记录

## R2 原生交互及独立复算

使用 computer-use 技能的 `@oai/sky` Windows 原生输入。Player 侧 [观察器](UX05-IMGUI-R2/Tools/HistoryObserver.cs) 只读记录窗口事实和产品查询；隔离配置选择UI、打开营地背包、延后定时自动保存。所有历程交互由原生点击/滚轮执行。并列时间与混合地区使用R1已归档夹具，不声称本轮重新生成目标历史。

`Start-ObservedPlayer.ps1 -Monitor` 以新的 evidence 子目录和唯一Run ID启动隔离进程，保存产品/Driver SHA、输入参数、前后指纹及数字退出码。最终MIXED-A06、EMPTY-A03、UNKNOWN-A03均退出0；早先成功的EMPTY-A01/UNKNOWN-A02未使用Monitor，数字退出码NOT_CAPTURED。EMPTY-A02补跑被输入工具拒绝，诊断与退出-1保留。后续新Run使用显式全局Run上下文、Run/PID/HWND守卫和新选择的观察副本窗口，实际完成输入，不修改旧结果补造退出码。最终Driver还归档两种UI的滚动位置变化，避免截图只停留在滚动前。

仓库根执行 `python UX05-IMGUI-R2/Tools/verify_results.py` 时应传入完整工具路径及参数 `ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation`；本机使用Codex运行时自带Python 3.12，系统WindowsApps python别名不可用。精确工具位于 [verify_results.py](UX05-IMGUI-R2/Tools/verify_results.py)。随后执行 [finalize_delivery.py](UX05-IMGUI-R2/Tools/finalize_delivery.py) 复核构建、生成增量矩阵；完整命令形式：

```text
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/Tools/verify_results.py ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/Tools/finalize_delivery.py
```

独立复算不覆盖原Run result.json，另写verified-result.json。检查真实前台身份、未投递意图排除、六字段排序/分页、双UI一致、交互期间Profile/主档不变。额外核对退出保存：原主档成为备份、校验正确、revision加1，差异仅营地events/randomStateJson/resources和revision，历史/结算/收益不变。保留147条历史分类及4142个旧文件字节。

最终三类完整Unity构建A02退出码0，NoDefine/Release验收标记扫描为0且无sidecar；新版本NoDefine/Release本轮结论为构建及静态验证，不冒充完整Player回归。[本轮完整报告](UX05-IMGUI-R2/REPORT.md)

## 构建与源码

Unity 6000.6.5f1 Windows x64 Mono。隔离工程位于 Builds/ux05-validation-01/Project。以当前产品 Assets、Packages 和 ProjectSettings 为输入，排除接手时已有未跟踪 Assets/Resources.meta。仅在构建副本加入探针源和构建入口。Unity 执行方法为 AcceptanceBuild.BuildNoDefine、ObjectiveHistoryProbeBuild.Run 和 WanxiangBuild.ValidateBuild。Acceptance 使用 extraScriptingDefines，NoDefine 不包含目标历史探针和既有验收标记。正式 Release 的原有隐私门保留。输出写到隔离项目之外的绝对目录，以满足 Bee 后检的绝对路径匹配。

Unity Roslyn 探针使用 Player 引用文件，首轮旧响应文件缺 B2 三个源码，修正后通过。部分探针将独立编译的 Assembly-CSharp 安装到复制的既有 B2 Mono 外壳。旧版探针源码基于指定 B2 HEAD，新版基于本次实现，Boot 入口加测试桥仅存在于探针副本。不能将这个外壳替换计作完整 Unity 构建。最终产品源码已完成完整 Unity Acceptance-07、NoDefine-07 和 Release-08。旧构建的运行证据保留其各自 build ID。

## 执行与复核

- [Run-IsolatedPlayer.ps1](Tools/Run-IsolatedPlayer.ps1) 使用唯一 Run ID、产品识别哈希、独立 PID、显式便携测试根和文件指纹。通过共享一个全新便携根有意制造旧/新或同版本并发，所有其他实验使用自己的根。
- [目标及入口探针](Tools/ObjectiveHistoryEntryProbe.cs) 触发实际标题按钮，保存测试通过 InputSystem 注入 F5。目标用例借用历史测试的受控导航，执行真实宝箱与撤离及结算业务入口。通过保存故障钩子区分替换前与已替换后的故障。未直接设置 History、目标完成标志或生命以制造成功。
- [纯合同探针](Tools/ObjectiveHistoryContractProbe.cs) 在 Mono 检验持久化 DTO、冻结时间、容量、旧局去重、wire 和派生分类。该测试没有接触游戏存档。
- A02 的迁移路径过长失败和合同启动参数失败均保留原日志、结果和 Run ID。修复后用新 Run ID。LOCK-CONTENDER-A04 探针的原始 FAIL 是继续入口拒绝，复核按负例记为预期阻断。
- v9 源夹具取自已归档 B2 验收，不读真实存档。归档核验比较文件 SHA-256 和长度，再将归档 collection 复制到另一个隔离根用 v9 客户端读回。另有旧版真实宝箱产生的分页夹具。已验证精确引用、旧 Pending 原样保留、旧版归档恢复及分页前终止进程后的安全重试。其余迁移中断点待测。

- P1C 使用既有 IntDriver.cs.txt 和原构建、启动工具。只向 Release-08 的独立副本注入驱动，产品 DLL 与正式 Release-08 哈希一致。三个独立 PID 和空根分别完成森林、遗迹、洞窟挑战。核对原断言、回营完成标记、v10 结算标记和相应历史条目。驱动编译清单和复核结果已入证据索引。

- CAPACITY-A02 的 129 局使用真实宝箱、普通撤离入口和结算调用。探针控制到达路径，并在撤离倒计时阶段设置 Unity timeScale=8 缩短测试。连续重复提交核对主档指纹，重启逐页查验。无加速的重复批次在证据齐备后关闭并保留。

- REPLAY-A01 复用容量测试实际产出的 v10 档案副本，在 Release-08 Mono 观察副本中调用产品计划入口。裁剪的局被 committedRuns 拒绝，Profile 与主档 SHA 均未变化。Acceptance-10 的测试探针变量重复声明导致编译失败，原日志保留，Acceptance-11 编译并运行恢复与放弃场景。

[构建身份](BUILD_IDENTITY.tsv) · [运行矩阵](PLAYER_RUN_MATRIX.csv) · [原始证据索引](EVIDENCE/INDEX.json)

## R1 复现与证据

- Unity 6000.6.5f1 Batchmode 依次执行 ObjectiveHistoryProbeBuild.Run、AcceptanceBuild.BuildNoDefine、WanxiangBuild.ValidateBuild。命令和产物身份见 [R1 构建](EVIDENCE/R1/final-build-identity.json) 及 [退出码](EVIDENCE/R1/build-exits.txt)。
- 在 EVIDENCE 下创建新的短名隔离根，从 PAGES-A01 的旧版外置分页夹具复制 ForestRuins 和已结束事务。用 Run-IsolatedPlayer.ps1 的 r1-migrate-* 模式执行一个切点，再用新 Run ID 从同一试验根执行 migrate 或 resume。宿主仅终止自己启动的 PID。
- 用独立空根运行 r1-save-readback 或 r1-save-stale。探针真实开箱、撤离和结算，再在受控发布位置注入读取拒绝或过期备份。核对旧 v10 主档指纹、双时间、重复提交和原结算计划。
- r1-ui-ugui、r1-ui-empty 和 r1-ui-unknown 同样使用独立根。混合和同时间夹具由真实保存的历史行派生，指定的时间和来源 SHA 记录在 [混合夹具记录](EVIDENCE/R1/mixed-ui-fixtures.json)。r1-ui-imgui 系列仅向确认处于前台的本 PID Player 发送鼠标事件。守卫拒绝操作作为未覆盖处理。
- r1-rules 使用相同运行时装备和 256 组固定掉落输入，依次只替换隔离内存中的地区记录做对比。14 项 UX-03 由 Run-CombatRegression.ps1 执行。两次长枪超时原样保留，串行用新 Run ID 重测，应用同一断言。
