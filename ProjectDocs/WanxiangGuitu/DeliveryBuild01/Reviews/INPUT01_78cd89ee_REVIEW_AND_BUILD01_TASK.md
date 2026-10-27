# 万象归途 INPUT-01 复审结论与 BUILD-01 Codex 任务书

## 0. 固定基线与复审结论

仓库：`mizunagare/BallMaze`  
开始基线：`a5e770064eedb8bfc478e54d54732b991f454658`  
产品/执行测试冻结：`f16bdcaee45553c9d53d525bdceecdd2e2238a1a`  
最终交付：`78cd89ee13eff8a80925ee388ba5dfcc797568b6`

**限定复审结论：INPUT-01 的实现与交付方自动化范围可接受；I14 构建质量仍为 `UNRESOLVED`，I15 原生与独立人工验收仍为 `NOT_RUN`。因此 INPUT-01、阶段2和发行验收整体均不能宣称完全通过。**

我已核对远端 `main` 指向用户提供的最终 SHA，并读取产品输入层、设置面板、首选项、角色/战斗/交互消费者、动作映射、报告、验收表、失败历史和构建证据。冻结执行提交之后的两次提交仅归档计划、验收与证据，没有继续修改产品源码。

本次未运行 Unity、Windows Player、原生键鼠、独立人工试玩或性能测试。规则26、虚拟输入/uGUI239、新进程11项、All计数及构建结果均是交付方已提交证据，不算本次审核重新执行的结果。静态审查范围内没有发现足以要求回滚 INPUT-01 的明确阻断性源码问题；这不等于真实玩家体验通过。

### 当前状态

- I01–I13：交付方声明的有限自动化范围 PASS；不等于13次独立玩家实验。
- I14：`UNRESOLVED`。BuildReport 为 `Succeeded`，但包含 **2 Error、91 Warning**，不能称零错误构建。
- I15：`NOT_RUN`。没有安全且获授权的独立原生输入/人工试玩环境；虚拟 InputSystem、截图和后台 `WM_CLOSE` 均不能替代原生验收。
- 完整性能基准、D3D12 `UNKNOWN`、Editor 青色帧、Editor.Search、JobTempAlloc 根因继续开放。

## 1. 下一批唯一目标：BUILD-01

**定位 INPUT-01 最终非开发构建中两条 URP 包资产 Error 的根因，并建立可复现的构建质量结论。** 本批先做诊断，不新增玩法功能，也不为了获得绿色报告而屏蔽日志。只有根因有可复现证据、修复范围最小且不违反下述保护条件时，才实施修复；否则提交根因证据与未解决项，暂停等待授权。

### 已知错误

```text
Host type is not matching any asset type at Path
Packages/com.unity.render-pipelines.core/Editor/Lighting/ProbeVolume/RenderingLayerMask/TraceRenderingLayerMask.urtshader.
```

该错误分别出现在 `Build player` 与 `Preprocess Player` 阶段。现有构建记录：Unity `6000.6.5f1`、URP `17.6.0`、BuildReport `Succeeded`、2 Error、91 Warning、产物 `127363354` bytes。

证据入口：
- [INPUT-01 报告](https://github.com/mizunagare/BallMaze/blob/78cd89ee13eff8a80925ee388ba5dfcc797568b6/ProjectDocs/WanxiangGuitu/DeliveryInput01/REPORT.md)
- [验收表](https://github.com/mizunagare/BallMaze/blob/78cd89ee13eff8a80925ee388ba5dfcc797568b6/ProjectDocs/WanxiangGuitu/DeliveryInput01/ACCEPTANCE.md)
- [构建汇总](https://github.com/mizunagare/BallMaze/blob/78cd89ee13eff8a80925ee388ba5dfcc797568b6/ProjectDocs/WanxiangGuitu/DeliveryInput01/Evidence/Runtime/FinalFrozenValidation/Build/BuildSummary.txt)
- [完整构建日志](https://github.com/mizunagare/BallMaze/blob/78cd89ee13eff8a80925ee388ba5dfcc797568b6/ProjectDocs/WanxiangGuitu/DeliveryInput01/Evidence/Runtime/FinalFrozenValidation/Build/WanxiangBuild.ValidateBuild.log)
- [BuildReport 97 条消息](https://github.com/mizunagare/BallMaze/blob/78cd89ee13eff8a80925ee388ba5dfcc797568b6/ProjectDocs/WanxiangGuitu/DeliveryInput01/Evidence/Runtime/BuildReportInspection2/build-report-messages.json)

## 2. 实施步骤

### B01-1：固定输入与保护

1. 重新读取远端 `main`，确认完整 SHA 为 `78cd89ee13eff8a80925ee388ba5dfcc797568b6`；记录本地 HEAD、工作区和未提交内容。
2. 记录 Unity 版本、`Packages/manifest.json`、`Packages/packages-lock.json` 的 SHA256，以及 URP/Core 包的解析版本与来源。
3. 记录源 `Assets/CombatPrototype/ForestRuins.unity` 和 `ProjectSettings/ProjectSettings.asset` 的原始 SHA256，结束时再次核对。
4. 所有导入/构建使用工程外新建的隔离工程与唯一拥有者根；不访问真实玩家存档、默认 LocalLow、用户正在使用的 Unity 工程或活动桌面。
5. 不覆盖旧日志、BuildReport、失败历史、产物哈希或历史测试根。每次尝试使用全新输出目录。

### B01-2：只读资产与包完整性审计

核实并记录：

- `TraceRenderingLayerMask.urtshader` 在冻结工程的实际路径、文件大小、SHA256、`.meta` GUID 和导入状态。
- 锁定的 `com.unity.render-pipelines.core` 版本、包来源、实际解析路径及 lock 文件一致性。
- 隔离工程 `Library/PackageCache` 中对应包和文件是否存在、是否完整，是否存在同名但哈希不同的副本。
- 日志中的 USS/UXML/URT `DirectoryNotFoundException` 与两条 BuildReport Error 是否存在时间、路径和调用栈上的联系。不得仅因都属于 URP 就认定同一根因。
- 判断问题属于资产类型识别、包路径/导入缓存、版本资产合同不匹配，还是其他原因；结论须有可复现证据等级。

不得手工编辑 `Library/PackageCache` 或缓存中的包文件来制造通过。

### B01-3：最小可复现对照

在不干扰用户环境的前提下：

1. 使用相同冻结源码、Unity 版本和依赖锁，在隔离工程复现基线构建，确认错误是否仍出现在相同路径/阶段。
2. 若假设是缓存或导入状态，再创建全新隔离工程/Library，以同一 manifest/lock 重新解析并导入；不改包版本。
3. 对比两次 BuildReport Error、包解析路径、资产哈希和导入异常。
4. 若无法获得有效对照，明确记 `NOT_RUN` 及阻断原因，不以静态猜测代替。
5. 不要求无差别重跑 INPUT-01 所有旧测试；只执行直接依赖构建导入和发行产物身份的必要步骤。

### B01-4：修复门槛

只有同时满足以下条件才允许改动：

- 根因可复现，不是凭错误文本猜测。
- 修复范围最小，能够解释为何消除目标错误。
- 不升级 Unity、URP 或其他依赖；不删除包、不屏蔽日志、不修改 BuildReport、不把 Error 降为 Warning。
- 不修改用户场景和 ProjectSettings。若根因确实需要触及它们，立即停止并报告，不擅自修改。
- 保留修复前失败与对照结果；在新目录重跑相同构建及必要的受影响回归。

若证据指向 Unity/URP 导入器缺陷且当前约束内无安全修复方案，不做伪修复；提交诊断和后续环境/版本方案建议，保持 `UNRESOLVED` 并暂停。

## 3. 验收基线

| ID | 验收内容 | 通过标准 |
|---|---|---|
| B01-01 | 固定输入 | 完整 SHA、Unity 版本、依赖锁、源码输入及保护文件哈希齐全 |
| B01-02 | 资产身份 | 错误资产的存在性、哈希、GUID、包来源和解析路径有证据 |
| B01-03 | 根因判定 | 至少一个可复现对照支持结论；不以相关性代替因果 |
| B01-04 | 修复有效性（如实施） | 同一冻结输入下目标错误消失，且没有屏蔽/篡改错误记录 |
| B01-05 | 构建质量 | 明确列出真实 Error、Warning、Log 数；不以 exit 0 代替消息审查 |
| B01-06 | 产物身份 | 记录 exe、UnityPlayer.dll、Assembly-CSharp.dll SHA256，并说明与基线差异 |
| B01-07 | 用户文件保护 | 源场景与 ProjectSettings 哈希不变，用户未提交修改不入提交 |
| B01-08 | 回归范围 | 运行直接受影响回归；未运行项明确标 `NOT_RUN` |
| B01-09 | 历史保留 | 修复前失败、每次尝试、命令、退出码、日志与输入哈希均保留 |

### 结果解释

- **PASS**：目标根因已证实且在允许范围内修复，重复构建不再出现目标 Error，必要回归通过。
- **UNRESOLVED**：根因证据不足，或安全修复超出当前授权/约束；不得宣称构建质量通过。
- **NOT_RUN**：缺少必要环境或对照条件，必须说明原因。

91条警告须单独保留与分类；即使两条 Error 消失，也不自动代表全部警告已解决。

## 4. Git 与交付

- 不升级依赖，不新增 CI，不修改存档格式，不改变游戏玩法、随机流、结算、掉落或经济。
- 不覆盖用户场景、ProjectSettings 和未提交工作；不强制推送、不重写 Git 历史。
- 只有代码/配置有经证据支持的最小修复时才修改产品文件；纯诊断结果以 Markdown 和证据清单提交。
- 提交前运行文档/脚本静态检查；若实施修复则运行规定的隔离构建与受影响回归。
- 推送后重新读取远端 `main`，核对完整 SHA；报告起始 SHA、冻结输入 SHA、最终 SHA、文件变更、命令、退出码、完整消息计数、产物哈希、用户文件保护结果和所有未关闭项。
- 完成本批后暂停，等待固定 SHA 独立复审。不得自动开始新地图或下一阶段。

## 5. 给 Codex 的执行指令

```text
读取《WanxiangGuitu_INPUT01_Review_and_BUILD01_Task.md》。
先固定远端 main=78cd89ee13eff8a80925ee388ba5dfcc797568b6，
按 B01-1～B01-4 诊断两条 TraceRenderingLayerMask.urtshader BuildReport Error。
先复现与取证，不要先改包、升级依赖或屏蔽日志。
只有根因可复现且最小修复符合任务书约束时才实施；否则保留 UNRESOLVED，提交诊断。
保护用户场景、ProjectSettings、真实存档和未提交修改；不新增 CI。
推送 GitHub 后重新核对远端完整 SHA，按第3、4节返回逐项结果，然后暂停等待复审。
```
