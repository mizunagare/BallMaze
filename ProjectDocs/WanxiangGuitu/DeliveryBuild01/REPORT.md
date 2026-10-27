# BUILD-01：包资产导入与构建质量

本批解决的是隔离验证工程路径过长导致的目标导入错误；未修改 Unity/URP 导入器或产品生命周期。INPUT-01 限定复审原文归档于 [Reviews](Reviews/INPUT01_78cd89ee_REVIEW_AND_BUILD01_TASK.md)。I01–I13 的历史自动化范围被审核方接受，不代表审核方重新执行，也不代表原生/人工验收通过。

## 输入与实现边界

- 开始、本批产品源码输入：`78cd89ee13eff8a80925ee388ba5dfcc797568b6`。
- INPUT-01 历史产品/测试冻结：`f16bdcaee45553c9d53d525bdceecdd2e2238a1a`；其后至本批开始未修改 Assets/Packages 产品代码。
- 首轮诊断工具提交：`9f30f29b8a220e6de63324f84f0bc6e85323a7b7`。
- 路径修复与重复验证工具冻结：`d7c253698a533657c8286db412f96cce50c1f5f3`。
- 最终提交是上述工具加本报告与证据；完整最终 SHA 由 Git 提交及交付回复给出，避免自引用提交号。
- Unity `6000.6.5f1 (3ff58d469c8a)`；URP/Core 均 `17.6.0 / BuiltIn`，未升级。
- Unity.exe SHA256：`35de3c28bd96c521c396251d18acfd2b67eb1b1c68711023232955abb4b705af`。
- manifest SHA256：`0b0877e7b6b46e10165ba211d9f6d9178f1239f70237ae498ebee16f350fb67e`。
- lock SHA256：`0abcfda7c4723ebd8777c1355faefa45f6e42401f5d3a918d2194d71211cef88`。

用户场景与项目设置作为明确保护的本地覆盖层复制进入隔离工程，不声称整个执行输入等于无修改的 Git 树。复制前后身份及全部源文件清单均归档；源文件从未被导入、构建或改写。所有新工程均无 Library/ShaderCache 复制，使用相同锁重新解析；允许使用 Unity 自身已有全局下载/编译缓存，未声称全机器冷启动或断网解析。

## 因果证据

错误原文：

```text
Host type is not matching any asset type at Path Packages/com.unity.render-pipelines.core/Editor/Lighting/ProbeVolume/RenderingLayerMask/TraceRenderingLayerMask.urtshader.
```

1. 旧 INPUT-01 目标文件为 3011 bytes，SHA256 `72ea623e6c49392d5895a4339ffe8e02db3bc56bad7cd7a239f403ddf308c661`，GUID `94a070d33e408384bafc1dea4a565df9`。三份历史缓存副本内容一致，Core/URP package.json 与锁一致，没有目标内容损坏或混用包版本的证据。
2. 失败日志在首次导入同一 GUID 时，先出现 `File.ReadAllText → UnifiedRTShaderImporter.OnImportAsset:11` 的 `DirectoryNotFoundException`；后续构建两阶段报告类型不匹配。旧日志没有逐条可靠墙钟时间，证据按原始行序关联，不虚构异常时间。
3. 新建 260 字符目标绝对路径工程，重复得到普通读取失败、扩展路径只读探针成功、相同文件哈希、`DefaultAsset`，随后同样两阶段 2 Error。扩展路径读取仅用于诊断，未修改缓存或替换导入器。
4. 新建 251 字符对照正常读取目标并导入为 `ComputeShader`，构建 0 Error；但它仍可触及更长 USS/UXML 路径，不能称所有包导入干净。
5. 两份新的短根工程独立解析/导入并重复构建，目标类型正确且不再出现包 `DirectoryNotFoundException`。完整 BuildReport 消息另行检查，不用进程 exit 0 推导构建质量。

因此，本机复现支持的原因是 **Windows 路径长度与 Unity 包导入器所用普通托管文件 API 的组合限制**。系统只读检查 `LongPathsEnabled=0`；未改注册表。文件存在并不表示当前导入器能读取其长路径。USS/UXML/URT 的关联来自具体路径、长度、文件身份、调用栈与长短对照；没有将所有 URP 或历史引擎异常都归为同一原因。

## 最小修复

仅修改仓库内验证工具：

- 现有无人值守入口默认测试根改为系统盘的短目录 `WGValidation`，仍可显式传入工程外短根。
- 现有 `Invoke-Rules.ps1` 在复制/导入前检查锁定 Unity/Core/URP 对应的六条已审计深层导入路径；达到 260 字符时明确失败并要求缩短测试根。未把单个前缀常数扩大或修改错误等级。
- 新策略不覆盖未来任意包的全部路径；版本改变需要重新审计。正式项目在现有短路径下不需要改动。
- 仅诊断工具允许显式 `PrepareOnly + AllowLongPackagePathsForDiagnosis` 复现长路径。普通验证无绕过开关；该例外及命令保留在证据中。
- 诊断入口复用原协调器的进程、超时、非活动桌面 worker 与退出回执，不激活桌面，不关闭原有 Unity PID 30340，不强杀，不访问真实存档。

没有改动 Assets、存档 v9、玩法、随机流、经济、结算、依赖、CI、用户场景或 ProjectSettings。没有修改 Library/PackageCache 内文件。路径规避解决当前验证环境故障，**不是声称修复了引擎的长路径能力**。

## 真实运行与质量

完整逐次结果见 [RESULTS.json](Evidence/RESULTS.json)、[CSV](Evidence/RESULTS.csv) 与 [证据索引](Evidence/INDEX.md)。首个诊断脚本因 `PackageInfo` 类型名歧义编译失败，已保留源、日志、退出码 1；修复为类型别名后在新目录重跑。该失败不归因于游戏。

| 尝试 | 目标路径字符 | BuildReport | Error / Warning / Log | 解释 |
|---|---:|---|---|---|
| 首次工具尝试 | 未运行到方法 | NOT_RUN | 无 BuildReport | 工具编译失败，保留 FAIL |
| 近边界对照 | 251 | Succeeded | 0 / 91 / 4 | 目标导入成功，其他长包路径仍须审查 |
| 旧失败边界复现 | 260 | Succeeded | 2 / 91 / 4 | 预期复现质量 FAIL；进程 exit 0 不抵消错误 |
| 短根修复验证 | 194 | Succeeded | 0 / 91 / 4 | 新 Library，目标正常 |
| 短根独立重复 | 195 | Succeeded | 0 / 91 / 4 | 新 Library，目标正常 |

91 条警告逐条保留：86 条 `CS0618` 旧 API、3 条 `CS0414` 未使用字段、2 条 Boot/Title 旧序列化版本。未顺带改动产品代码或重存场景。另有原始 Editor 日志 JobTempAlloc 提示，不属于这 91 条 BuildReport Warning，仍保留开放状态。

## 产物与回归边界

exe 与 UnityPlayer.dll 对比历史最终构建完全相同：

- exe：`001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`。
- UnityPlayer.dll：`3bdc6e4cd1b5eb85e1562b1c6018949145cdedf50cf7aceab0d1518143f9aa7c`。

各次 Assembly-CSharp.dll 原始 SHA、MVID、PE 时间戳和与历史比较见 `FINAL_AUDIT.json` 与 `AssemblyIdentity/`。原始哈希有差异，不宣称字节可复现；已核对的方法签名与 IL 字节指纹另行列出，不把它冒充实际游戏行为回归。正式 DLL 未包含本批或 INPUT-01 的 Editor 诊断类名。

本批执行：资产身份、包解析、首次导入、脚本编译、非开发构建、报告消息与产物身份、路径预检边界。未重跑正常 AI、原生 UI、独立人工试玩、性能、结算/跨进程完整冒险；这些为本批 `NOT_RUN`，不继承历史 PASS。

## 用户文件与剩余项

- ForestRuins.unity 原始/结束 SHA256：`ebc46ce7104b6d6ce90b7f510a59a401d7cdf64ae8babc85a7ebbf881c9d16d4`。
- ProjectSettings.asset 原始/结束 SHA256：`7d06ea8265edaaf0a1a7402cff1e94da015450c58899438ebf4a5d97e37fd451`。
- 两项用户修改继续留在工作区，未纳入提交；完整清单及核对见机器证据。
- INPUT-01 两条目标 Error：本批短路径规避及重复验证范围内已消除，等待固定 SHA 复审；不改写历史 `2 Error` 结果。
- 91 条警告未解决；D3D12 UNKNOWN、Editor 青色帧、Editor.Search、JobTempAlloc 根因继续 `UNRESOLVED`。
- 原生 U16、独立人工、完整性能基准继续 `NOT_RUN`。未进行无新证据的关闭实验。

完成后暂停，不自动进入下一批；推送不等于独立复审通过。
