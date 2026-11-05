# 两次干净工程构建输入核查

从与 R2 固定提交产品树一致的本地参考工作树复制 Assets、Packages 和 ProjectSettings 的 1,370 个跟踪文件。两个副本的每一文件均对参考 SHA256 核对。复制排除 Library、用户存档和未跟踪输入，拒绝未实体化的 LFS 指针。所有 Unity 写回限于工程外的两个独立测试项目。

A 先以 Unity 6000.6.5f1 执行独立批量打开和导入，退出后再调用项目已有 WanxiangBuild.ValidateBuild。B 从全新副本首次打开直接进入同一正式构建入口。两套测试不注入 Editor 或运行时验收驱动。

每次启动前和退出后重新核对全部跟踪输入。对历史差异路径另按约 220 ms 轮询，保存每个观察到的版本、SHA256 与时间。Unity 日志地标用于区分打开与构建。轮询可以证明实际观察到的写回顺序，对采样之间的临时状态和引擎内部精确读取点不作保证。原始日志及完整字段 diff 保留。

仓库字节等同性、两个独立构建的运行文件一致性、40 个核查产品类型的 IL、实际 Bee 诊断配置是不同结论。采用固定的 Windows Release Profile 和原生保护，不手改派生 UnityConnect 字段。实际 Bee Development 和五项服务布尔值、BuildReport、exe 与核心程序集 SHA256 单独记录。

实际观察到 ProjectA 单独首次导入只重写 EditorBuildSettings.asset 的编码标记。随后在正式构建开始后的预处理附近观察到 URP 与 GraphicsSettings 变化。安装的 URP 17.6.0 源码中，ShaderBuildPreprocessor 计算预筛选字段并调用 SaveAssetIfDirty，与观察到的 PC_RPAsset 变化吻合。Input System 1.20.0 的 ProjectWideActionsBuildProvider 在构建预处理临时加入项目动作资产，后处理通过同一帮助类移除。监控到的 GUID 对应仓库的 InputSystem_Actions.inputactions.meta。预加载临时写回需要看构建期间快照，仅比较退出后无法发现。其他全局渲染设置的原生逐字段写入调用不据相邻日志推断。

[安装包源码核对](Evidence/Audit/package-callbacks.json) · [写回时序和字段](Evidence/INDEX.md)

## 结果

两次正式非开发构建均成功，各 0 错误、104 警告。实际 Bee 五项诊断服务全部为 false。两次纯包均在私有非活动桌面实际启动到标题并退出 0，合成存档哈希保持不变。

独立导入后有 1 个跟踪文件的字节变化。两次构建结束均有 5 个相同路径发生相同哈希变化。EditorBuildSettings 的 UTF-8 BOM 变化在独立导入可复现。构建阶段另变更 PC_RPAsset、URP 全局配置、GraphicsSettings 和 ProjectSettings。ProjectSettings 的临时 preloadedAssets 与最终文本变化分开保存。原 R2 隔离缓存的 16 项差异不能整体视为此次干净构建产生。

排除运行不使用的回执及备份目录后，比较了 189 个发行文件，184 个相同。五个差异为 Assembly-CSharp.dll、lib_burst_generated.dll、boot.config、globalgamemanagers 和 resources.assets。两套核心程序集的 40 个核查产品类型 IL 一致。boot.config 的差异是独立 build-guid。Burst DLL 的两个差异字节均在 PE 时间戳字段。Assembly-CSharp.dll 还有其他差异字节。globalgamemanagers 相差 2 字节，resources.assets 相差 2,799 字节，尚无足够证据证明这些差异都与运行语义无关。

两套构建日志按命名 Shader、Pass 和 API 对照的 1,178 项剥离后变体计数一致。计数一致与资源字节一致分别判定。冻结检出在整个构建过程中保持原始字节的条件为 FAIL，实际输入和成品的全面语义等同性为 UNRESOLVED。

[构建审计](Evidence/Audit/build-audit.json) · [Shader 计数](Evidence/Audit/shader-variant-counts.json) · [二进制差异定位](Evidence/Audit/runtime-byte-deltas.json)
