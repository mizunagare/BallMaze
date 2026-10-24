# 本机无人值守验证

PowerShell 7、.NET SDK 10、Python 3，以及工程指定的 Unity 6000.6.5f1。入口不会安装工具、升级依赖、修改全局快捷键或关闭用户程序。需要可用的 Windows 图形会话；没有条件时保留 NOT_RUN。

```powershell
& 'D:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1' `
  -SourceProject 'D:/unity/WanxiangGuitu' `
  -TestRoot 'C:/Users/guan/Documents/unitytest/WanxiangUnattended' `
  -ProcDumpPath 'C:/Users/guan/Documents/unitytest/WanxiangUI01Close/Tools/ProcDump/procdump64.exe'
```

路径均可参数化；`-UnityPath`、`-PythonPath` 可覆盖本机默认值。ProcDump 可不提供，缺失仅跳过独立转储实验。入口创建时间戳加随机 ID 的全新根，禁止 LocalLow、链接父目录和源工程内测试根。只复制 Assets、Packages、ProjectSettings 与既有合成夹具，**从不复制真实玩家档**。

默认选择 15 项受影响回归；`-FullRegression` 运行原有完整方法清单，未选择的项目逐项 NOT_RUN。复用 Invoke-Rules 的准备逻辑、原测试方法、正常 AI 入口、构建入口、92 帧受控视觉矩阵与只读退出分析器，没有另写业务断言。正常 AI 驱动在隔离副本中交接，避免重复编译同名驱动。源工程可以保持打开；测试只使用新副本，不关闭源 Editor。

`-UnityTimeoutSeconds 600` 设置每个规则/构建阶段上限，正常 AI 420 秒、受控截图 660 秒，Player 初始化 60 秒、正常关闭等待 30 秒。超时先保存进程诊断，保留活进程，后续依赖步骤跳过；独立步骤继续。没有自动强杀、删除或无限重试。确定性失败不会靠重试抹除。退出码 1 表示非预期 FAIL；退出码 0 仅表示没有非预期 FAIL，仍须阅读 NOT_RUN / UNRESOLVED。

输出 `results.json`（含命令）、`results.csv`、`counts.json`、`REPORT.md` 持续落盘。`owner.json` 标识运行根与协调进程；`preserved-processes.json` 列未结束的子进程。每阶段记录 UTC、实际退出码、超时和日志。故意的 exit7 与 1 秒超时探针仍记 FAIL，scope=harness-negative；另一个 self-check 检查这些故障被正确记录且后续任务继续，不能将探针 FAIL 解释为游戏失败或删掉。

可选 `-ShaderCacheSource <闲置隔离工程>` 只复制同版本 ShaderCache，拒绝忙碌/链接/版本不符缓存，记录来源；使用后不得声称干净 Shader 编译。默认不使用缓存。

## 单独复跑关闭矩阵

```powershell
& 'D:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1' `
  -Phase PlayerMatrix -ArtifactsFrom '<上次唯一运行根>' `
  -SourceProject 'D:/unity/WanxiangGuitu' -ProcDumpPath '<procdump64.exe>'
```

只接受此入口已成功构建、成功生成 SYNTHETIC 夹具且 source 匹配的运行根。将完整构建与合成目录复制到新的唯一根，核对 exe 哈希；不会把原轮规则/AI结果继承为本轮 PASS。用于调试编排器时避免重复运行无关业务测试。

矩阵是默认渲染器与 D3D11 各两组，每组退出后再开新进程；第九次是单独的默认渲染器 ProcDump 实验。构建、夹具和关闭方式一致；每组独立存档。保存初始化审计、关闭请求、完整 Player 日志、真实退出码、退出审计、保存校验与修订、恢复摘要。异常标记即使 exit0 也使严格分析失败。找不到调用栈/原因仍 UNRESOLVED。

ProcDump 使用 `-mm -e -t -n 1`，捕获未处理异常及终止，不用窄字符串过滤；不保证捕获 Unity 自行处理的所有异常，不用“无 dump”证明无异常。最多捕获首个未处理异常或终止事件，不保证获取所有异常。终止 dump 也不自动证明崩溃。转储本地保留，不上传内存。实验不与未附加对照混为一组。

## 桌面安全和证据边界

NativeProbe 是 Assets 之外的独立 .NET 进程。Win32 CreateDesktop / CreateProcess 启动测试，**不调用 SwitchDesktop、不激活窗口、不发送 Esc/F1、不改 Snipaste**。启动失败不退回用户桌面。正常关闭是对核对 PID 与 exe 的自有窗口发送 WM_CLOSE，然后由持有进程句柄的父进程读取真实退出码；这不是物理点击标题栏的证据。

原生输入要求目标确属本轮、可见、在输入桌面并处于前台，否则零输入且 NOT_RUN。私有桌面不是输入桌面，因此当前非干扰模式的原生 UI 完整语义验收为 NOT_RUN；即使输入送达，也不能把送达当作按钮效果通过。需后续配置专用交互测试会话/机器和可靠的 UI 语义观察，才能补齐无人值守原生 U16。入口不要求用户守候，也不擅自修改系统来取得这些条件。

领域/Play Mode、正常 AI 驱动、受控截图、后台正式 Player 关闭恢复、原生输入与人工理解分别记 scope，不能互相代替。人工理解始终需要独立人员，未执行 NOT_RUN。

所有运行目录默认保留。清理前先确认进程结束，核对 owner 与绝对根，人工选择删除明确的测试根；本入口不递归清理。提交证据时不包含存档、构建、Library、缓存、凭据和转储；Unity 编辑器日志可能含许可证命令参数，发布副本须脱敏并注明，原始日志只保留本地。

## 辅助退出码与定向故障检查

每个子进程都有 .command.json / .exit.json（进程句柄真实退出码，观察时间），包括不经 Step 等待的 ProcDump。辅助工具仍保留实际退出码；默认非0记FAIL并使入口返回1。唯一例外是经固定签名/SHA校准的ProcDump，同时验证正退出与数量、完成日志、转储结构，才记捕获PASS/rawExit1。未知工具或校验失败仍FAIL，Player分析独立继续；捕获PASS不代表游戏根因解决。参数含义参照[微软ProcDump文档](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)，文档没有给出能证明本次exit1含义的保证。

`-Phase DumpOnly -ArtifactsFrom <成功All运行根>` 只重跑独立转储实验，复用同一构建/完整合成夹具到新根；规则/AI不继承为新PASS。可使用 Automation/FaultMonitor 项目（独立 .NET 控制台）作为明确故障监视器，构建输出和 obj 必须指向测试根，再通过 -ProcDumpPath <FaultMonitor.exe> 运行 DumpOnly。预期工具exit7、协调器exit1，Player分析仍继续PASS；这不是实际调试器，也不接触游戏状态。正式运行不要把它当ProcDump。

## 当前固定工具校准与完整复验

微软签名12.02 / SHA256 `22C2A2B09ADE73A342A18DAB838354385F73FC98E324B9903FD61FFF949C5124`，独立实验观测单份exit1、双份exit2、无效PID -2。这是固定版本经验，不是通用非零白名单。procdump-calibration.json绑定已审阅证明；证明用局部Git -text固定原始字节。工具/证明变更需重新校准，入口不自动放宽。

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Investigate-ProcDump.ps1' -ProcDumpPath '<procdump64.exe>' -TestRoot '<绝对外部测试根>'
```

控制脚本只操作自建Win32窗口，自动正常关闭，不加载Unity或存档；输出签名、命令、日志、实际退出及新calibration-proof，不覆盖已审阅证明。inspect-minidump.py做结构检查，不是符号化栈；classify-procdump.py还验证校准、完成数量和真实返回值。详见[本轮报告](../FOLLOWUP_REPORT.md)。

最终复验使用原入口加 -FullRegression，新项目/构建/合成根，不继承旧All。build-manifest.json关联本轮所有正式Player命令；Editor规则与正常AI不是原生UI验收。当前只有用户工作console，不激活私有桌面、不发Esc、不改Snipaste、不要求用户守候。专用Windows机器/会话还需租约、GPU/DPI和可靠语义观察，当前U16/人工NOT_RUN。


## 独立交互环境只读检查

```powershell
& '<工程>/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Inspect-InteractiveEnvironment.ps1' `
  -OutputDirectory '<全新绝对路径，例如 C:/Tests/Wanxiang/Environment-唯一ID>'
```

拒绝已有输出目录；只记录 quser 及其实际返回码、当前会话、虚拟化服务/工具/进程及调试工具发现。脚本成功不是原生 U16 PASS，也不自动授予任何会话或主机使用权。不登录/RDP、不创建或激活桌面、不发输入、不启用系统功能、不访问游戏存档。只有用户工作 console、只有 mstsc 客户端或只发现 VM 工具均不足以执行原生测试；需另外核对专用测试主机授权和独占租约。发现结果有限，不宣称已穷尽所有网络测试机。

缺少安全条件则停止原生部分并记 NOT_RUN；后台 WM_CLOSE/领域驱动不能补齐。独立环境提供后还须同时验证原生输入送达与实际 UI/业务变化，焦点不符停止输入，不用 Esc，不修改外部软件配置。最新 [边界报告](../ENVIRONMENT_BOUNDARY_REPORT.md)没有重跑 All 或追加无新线索的关闭实验。


## B2 增量验证

`-GameplayOnly` 保留原有预检、唯一隔离副本、规则/Play Mode、正常 AI/Resume、非开发构建与受控截图，只跳过 Player 关闭诊断矩阵（包括 ProcDump）。这不是标题栏关闭验收或新的完整关闭 All。原生 U16 单列 NOT_RUN，UNKNOWN 单列 UNRESOLVED；旧证据不改写。B2Rules.Run/Resume 新增到计划与依赖表；正常 AI 通过 `Invoke-NormalAI.ps1 -B2` 选择在原B1场景上增补目标断言和按需实际补采的驱动。旧驱动仍可独立选择，不更改玩家掉落来满足测试。

本轮结果见 [DeliveryB2/REPORT.md](../../DeliveryB2/REPORT.md)。环境冲突/超时按原机制记录，不结束用户程序，不访问真实存档，不要求守候。


### B3增量（2026-10-24）

默认GameplayOnly选定套件增加B3StreamRules及B3Checks/Resume，正常AI新增-B3驱动并核对新进程随机状态；原-B2及历史测试保留。明确启用标志解决旧档JsonUtility空对象语义，不重写编排。完整范围、四轮失败记录与最终结果见[DeliveryB3](../../DeliveryB3/REPORT.md)。不因此关闭UI-01；原生U16/人工理解NOT_RUN、UNKNOWN UNRESOLVED仍保留。

## B4 增量入口（2026-10-24）

`-Phase All -FullRegression -B4` 复用既有编排并添加 B4 拓扑、物理通行、旧布局/收益查询和宝箱拾取回归。正常 AI 分 Gather/Treasure/Bypass 三策略，每项 Normal/Resume/FinalResume 三个独立进程，最后阶段核对再次出征确为森林。缺少依赖按 NOT_RUN；任何非预期失败继续传播，两个故障探针单列。来源与过程见 [DeliveryB4](../../DeliveryB4/REPORT.md)。不开启原生 U16 或人工理解的自动 PASS；UNKNOWN 状态保留。

### B4-R1 高度地形与真实导航

统一评分增量沿用同一All，加入RouteScoringProbe/RouteScoringRules.Run/Resume和新依赖表。score-components.jsonl记录实际NavMesh与全部分项，score-order.csv为固定种子的默认/仅距离反事实排序；正常AI另记score-normal-{stage}-{finish/restored}.json并核对查询不推进随机状态。数据纯读、无出口的可见文案和新进程组件一致性一并断言。首次模型缺失FAIL、源码审计发现的旧无出口文案矛盾及未覆盖该新UI断言的首轮All分别保留，最终完整All使用新根。入口不变，范围见[统一评分首版](../../DeliveryB4-R1/SCORING_V1.md)，不因此关闭原生U16/人工理解/UNKNOWN。

同一完整入口增量加入R1Audit/R1Shore/R1Rules/Resume、非batch受控TerrainScreens；沿用既有worker、规则和三策略正常AI，不另建框架。30种子地形/离路/实际路径/岸线碰撞与旧revision4单独计证。Unity/Player按文件名强制经过私有worker，缺失时启动前拒绝；worker.no-direct-unity是不启动任何真实程序的拒绝探针。临时辅助调用曾绕过worker的历史、首次截图失败与磁盘预检失败均保留在[DeliveryB4-R1](../../DeliveryB4-R1/REPORT.md)。原生U16、人工理解和UNKNOWN不因地形回归通过而关闭。
